from django.db import models

import io
import typing
import urllib
from urllib.request import urlopen
from django.utils.translation import gettext_lazy as _
from streamfield.fields import StreamField
from weasyprint import HTML, default_url_fetcher
from .streamblocks.models import STREAMBLOCKS_MODELS
from django.template.loader import render_to_string
from django.conf import settings
from permits import models as permits_models
from django.contrib.auth.models import Group


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
    stream = StreamField(model_list=STREAMBLOCKS_MODELS)
    type = models.ForeignKey(
        "permits.ComplementaryDocumentType", on_delete=models.RESTRICT
    )
    work_object_types = models.ForeignKey(
        "permits.WorksObjectType",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Objets"),
        related_name="available_reports",
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    def render_string(self, permit_request) -> str:
        from permits.serializers import PermitRequestPrintSerializer

        context = {
            "report": self,
            "permit_request": permit_request,
            "permit_request_data": PermitRequestPrintSerializer(permit_request).data,
        }
        return render_to_string("reports/report.html", context)

    def render_pdf(self, permit_request) -> typing.IO:
        # Note: rendering is done with weasyprint, which does not fully support modern CSS (such as grid).
        # If this proves limiting, consider trying out another solution such as
        # https://github.com/bedrockio/export-html

        # Define a fetcher, translating URLs so they work internally
        def my_fetcher(url):
            if url.startswith("http://localhost:9096/"):
                internal_url = url.replace(
                    "http://localhost:9096/", "http://qgisserver/"
                )
                return {"file_obj": urlopen(internal_url)}

            if url.startswith("http://relative/media/"):
                local_path = url.replace("http://relative/media", settings.MEDIA_ROOT)
                return {"file_obj": open(local_path, "rb")}
            return default_url_fetcher(url)

        buffer = io.BytesIO()
        HTML(
            string=self.render_string(permit_request),
            url_fetcher=my_fetcher,
            base_url="http://relative",  # seems required to get relative URLs to work
        ).write_pdf(buffer)
        buffer.seek(io.SEEK_SET)
        return buffer

    def __str__(self):
        return self.name
