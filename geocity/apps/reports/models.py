import base64
import re
from datetime import timedelta

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from jinja2.sandbox import SandboxedEnvironment
from knox.models import AuthToken
from polymorphic.models import PolymorphicModel

from geocity.apps.accounts.fields import AdministrativeEntityFileField

from .fields import BackgroundFileField
from .utils import DockerRunFailedError, run_docker_container


class ReportLayout(models.Model):
    """Page size/background/marings/fonts/etc, used by reports"""

    name = models.CharField(_("Nom"), max_length=150)
    width = models.PositiveIntegerField(_("Largeur"), default=210)
    height = models.PositiveIntegerField(_("Hauteur"), default=297)
    margin_top = models.PositiveIntegerField(_("Marge: haut"), default=10)
    margin_right = models.PositiveIntegerField(_("Marge: droite"), default=10)
    margin_bottom = models.PositiveIntegerField(_("Marge: bas"), default=10)
    margin_left = models.PositiveIntegerField(_("Marge: gauche"), default=10)
    font = models.CharField(
        _("Police"),
        max_length=1024,
        blank=True,
        null=True,
        help_text=_(
            'La liste des polices disponbiles est visible sur <a href="https://fonts.google.com/" target="_blank">Goole Fonts</a>'
        ),
    )

    class Meta:
        verbose_name = _("3.1 Format de papier")
        verbose_name_plural = _("3.1 Formats de papier")

    background = BackgroundFileField(
        _("Papier à entête"),
        null=True,
        blank=True,
        upload_to="backgound_paper",
        help_text=_("Image d'arrière plan (PNG)."),
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )

    class Meta:
        verbose_name = _("3.1 Format de papier")
        verbose_name_plural = _("3.1 Formats de papier")

    def __str__(self):
        return self.name


class Report(models.Model):
    """Report definition, allowing to generate reports for submissions"""

    class Meta:
        permissions = [
            ("can_generate_pdf", _("Générer des documents pdf")),
        ]
        verbose_name = _("3.3 Modèle d'impression")
        verbose_name_plural = _("3.3 Modèles d'impression")

    name = models.CharField(_("Nom"), max_length=150)
    layout = models.ForeignKey(
        ReportLayout,
        on_delete=models.RESTRICT,
        verbose_name=_("Format de papier"),
    )
    # reverse relationship is manually defined on submissions.ComplementaryDocumentType so it shows up on both sides in admin
    document_types = models.ManyToManyField(
        "submissions.ComplementaryDocumentType",
        blank=True,
        related_name="+",
        verbose_name=_("Types de documents"),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        limit_choices_to={"permit_department__is_integrator_admin": True},
    )

    def __str__(self):
        return self.name


# https://github.com/django-polymorphic/django-polymorphic/issues/229#issuecomment-398434412
def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class Section(PolymorphicModel):
    class Meta:
        verbose_name = _("Paragraphe")
        verbose_name_plural = _("Paragraphes")
        ordering = ["order"]

    report = models.ForeignKey(
        Report, on_delete=NON_POLYMORPHIC_CASCADE, related_name="sections"
    )
    order = models.PositiveIntegerField(_("Ordre du paragraphe"), null=True, blank=True)

    def prepare_context(self, request, base_context):
        """Subclass this to add elements to the context (make sure to return a copy if you change it)"""
        return {
            **base_context,
            "section": self,
            "settings": settings,
        }

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
        blank=True,
        help_text=(
            _("Si aucun projet n'est ajouté, le projet par défaut sera utilisé.")
        ),
    )
    qgis_print_template_name = models.CharField(
        _("Nom du modèle QGIS"),
        max_length=30,
        blank=True,
        default="paysage-cadastre",
        help_text=(_("Modèles du projet par défaut: paysage-cadastre, paysage-ortho")),
    )

    class Meta:
        verbose_name = _("Carte")

    def get_context(self, context):
        context = super().get_context(context)

    def _generate_image(self, request, base_context):

        # Generate a token
        authtoken, token = AuthToken.objects.create(
            request.user, expiry=timedelta(minutes=5)
        )

        # Create a docker container to generate the image
        commands = [
            "/io/project.qgs",
            "/io/output.png",
            self.qgis_print_template_name,
            str(base_context["submission"].id),
            str(token),
            ",".join(settings.ALLOWED_HOSTS),
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

        authtoken.delete()

        # Prepare the dataurl
        data = base64.b64encode(output.read()).decode("ascii")
        return f"data:image/png;base64,{data}"

    def prepare_context(self, request, base_context):
        # Return updated context
        return {
            **super().prepare_context(request, base_context),
            "map_data_url": self._generate_image(request, base_context),
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Upload a default project if none is provided
        if not self.qgis_project_file:
            # Open an existing file using Python's built-in open()
            _qgis_path = finders.find("reports/report-template.qgs")
            qgis_template_project = File(open(_qgis_path, "rb"))
            self.qgis_project_file.save(
                "report-template-dev.qgs", File(qgis_template_project)
            )


class SectionParagraph(Section):
    title = models.CharField(_("Titre"), default="", blank=True, max_length=2000)
    content = RichTextField(
        _("Contenu"),
        help_text=(
            _(
                'Il est possible d\'inclure des variables et de la logique avec la <a href="https://jinja.palletsprojects.com/en/3.1.x/templates/">syntaxe Jinja</a>. Les variables de la demande sont accessible dans `{{request_data}}` et celles du formulaire dans `{{form_data}}`.'
            )
        ),
    )

    class Meta:
        verbose_name = _("Paragraphe libre")

    def _render_user_template(self, base_context):
        # User template have only access to pure json elements for security reasons
        inner_context = {
            # TODO rename to `submission_data` (& migrate sections) to match new naming
            "request_data": base_context["request_data"],
            "form_data": base_context["form_data"],
        }
        env = SandboxedEnvironment()
        rendered_html = env.from_string(self.content).render(inner_context)
        return mark_safe(rendered_html)

    def prepare_context(self, request, base_context):
        # Return updated context
        return {
            **super().prepare_context(request, base_context),
            "rendered_content": self._render_user_template(base_context),
        }


class SectionContact(Section):
    class Meta:
        verbose_name = _("Contact·s")


class SectionAuthor(Section):
    class Meta:
        verbose_name = _("Auteur")


class SectionDetail(Section):
    class Meta:
        verbose_name = _("Détail·s")


class SectionPlanning(Section):
    class Meta:
        verbose_name = _("Planning")


class SectionHorizontalRule(Section):
    class Meta:
        verbose_name = _("Ligne horizontale")


class SectionValidation(Section):
    class Meta:
        verbose_name = _("Commentaire·s des services")


class SectionAmendProperty(Section):
    class Meta:
        verbose_name = _("Commentaire·s du secrétariat")


class SectionStatus(Section):
    class Meta:
        verbose_name = _("Statut")


class SectionCreditor(Section):
    class Meta:
        verbose_name = _("Adresse de facturation")
