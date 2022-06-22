import base64
import io
import re
from datetime import timedelta
from typing import Union

from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from jinja2.sandbox import SandboxedEnvironment
from knox.models import AuthToken
from polymorphic.models import PolymorphicModel

from permits.fields import AdministrativeEntityFileField

from .utils import DockerRunFailedError, run_docker_container


class ReportLayout(models.Model):
    """Page size/background/marings/fonts/etc, used by reports"""

    class Meta:
        verbose_name = _("5.1 Configuration du modèle d'impression de rapport")
        verbose_name_plural = _("5.1 Configuration des modèles d'impression de rapport")

    name = models.CharField(max_length=150)
    width = models.PositiveIntegerField(default=210)
    height = models.PositiveIntegerField(default=297)
    margin_top = models.PositiveIntegerField(default=10)
    margin_right = models.PositiveIntegerField(default=10)
    margin_bottom = models.PositiveIntegerField(default=10)
    margin_left = models.PositiveIntegerField(default=10)
    font = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=_(
            'La liste des polices disponbiles est visible sur <a href="https://fonts.google.com/" target="_blank">Goole Fonts</a>'
        ),
    )
    # TODO: move these to private storage
    background = models.ImageField(
        null=True, blank=True, help_text=_('Image d\'arrière plan ("papier à en-tête")')
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    def __str__(self):
        return self.name


class Report(models.Model):
    """Report definition, allowing to generate reports for permit requests"""

    class Meta:
        verbose_name = _("5.2 Configuration du rapport")
        verbose_name_plural = _("5.2 Configuration des rapports")

    name = models.CharField(max_length=150)
    layout = models.ForeignKey(ReportLayout, on_delete=models.RESTRICT)
    # reverse relationship is manually defined on permits.ComplementaryDocumentType so it shows up on both sides in admin
    document_types = models.ManyToManyField(
        "permits.ComplementaryDocumentType", blank=True, related_name="+"
    )

    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    def render_pdf(
        self, permit_request, work_object_type, generated_by, as_string=False
    ) -> Union[bytes, str]:
        """Renders a PDF by calling the PDF generator service"""

        # Generate a token
        authtoken, token = AuthToken.objects.create(
            generated_by, expiry=timedelta(minutes=5)
        )

        context = {
            "report": self,
            "permit_request": permit_request,
            "work_object_type": work_object_type,
            "token": token,
        }
        html_string = render_to_string("reports/report.html", context)

        if as_string:
            return html_string

        commands = [
            "/io/input.html",
            "/io/output.pdf",
            token,
        ]

        output = run_docker_container(
            "geocity_pdf",
            commands,
            file_input=("/io/input.html", io.BytesIO(html_string.encode("utf-8"))),
            file_output="/io/output.pdf",
        )

        authtoken.delete()

        return output

    def __str__(self):
        return self.name


# https://github.com/django-polymorphic/django-polymorphic/issues/229#issuecomment-398434412
def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class Section(PolymorphicModel):
    class Meta:

        ordering = [
            "order",
        ]

    report = models.ForeignKey(
        Report, on_delete=NON_POLYMORPHIC_CASCADE, related_name="sections"
    )
    order = models.PositiveIntegerField(null=True, blank=True)

    def get_template(self):
        class_name = self.__class__.__name__.lower()
        return f"reports/sections/{class_name}.html"

    def get_context(self, context):
        return {
            **context,
            "section": self,
            "permit_request": context["permit_request"],
            "work_object_type": context["work_object_type"],
        }

    def render(self, report_context):
        template = self.get_template()
        section_context = self.get_context(report_context)
        return render_to_string(template, section_context)

    @property
    def css_class(self):
        return re.sub("^Section", "section-", self.__class__.__name__).lower()

    def __str__(self):
        return self._meta.verbose_name


class SectionMap(Section):
    qgis_project_file = AdministrativeEntityFileField(
        _("Projet QGIS '*.qgs'"),
        validators=[FileExtensionValidator(allowed_extensions=["qgs"])],
        upload_to="qgis_templates",
    )
    qgis_print_template_name = models.CharField(max_length=30)

    def get_context(self, context):
        context = super().get_context(context)

        # Create a docker container to generate the image
        commands = [
            "/io/project.qgs",
            "/io/output.png",
            self.qgis_print_template_name,
            str(context["permit_request"].id),
            str(context["token"]),
        ]

        try:
            output = run_docker_container(
                "geocity_qgis",
                commands,
                file_input=("/io/project.qgs", self.qgis_project_file.file),
                file_output="/io/output.png",
            )
        except DockerRunFailedError:
            # Return error image
            path = finders.find("reports/error.png")
            output = open(path, "rb")

        # Prepare the dataurl
        data = base64.b64encode(output.read()).decode("ascii")
        data_url = f"data:image/png;base64,{data}"

        # Return updated context
        return {**context, "map": mark_safe(f'<img src="{data_url}">')}


class SectionParagraph(Section):
    title = models.CharField(default="", blank=True, max_length=2000)
    content = RichTextField(
        # TODO: reverse_lazy and parametrize URL instead of hardcode
        help_text=(
            _(
                'Il est possible d\'inclure des variables et de la logique avec la <a href="https://jinja.palletsprojects.com/en/3.1.x/templates/">syntaxe Jinja</a>. Vous pouvez afficher les variables diponibles avec la balise `{{data}}`'
            )
        )
    )

    def get_context(self, context):
        from permits.serializers import PermitRequestPrintSerializer

        env = SandboxedEnvironment()
        request_data = PermitRequestPrintSerializer(context["permit_request"]).data

        wot = context["work_object_type"]
        wot_key = (
            f"{wot.works_object.name} ({wot.works_type.name})"  # defined by serializer
        )
        request_props = request_data["properties"]["request_properties"][wot_key]
        amend_props = request_data["properties"]["amend_properties"][wot_key]

        inner_context = {
            "request_data": request_data,
            "wot_data": {
                "request_properties": request_props,
                "amend_properties": amend_props,
            },
        }
        rendered_content = env.from_string(self.content).render(inner_context)

        return {
            **super().get_context(context),
            "rendered_content": mark_safe(rendered_content),
        }


class SectionAuthor(Section):
    pass
