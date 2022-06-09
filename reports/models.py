from django.db import models

import io
import typing
import requests
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
from django.urls import reverse
from rest_framework.authtoken.models import Token


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
    work_object_types = models.ManyToManyField(
        "permits.WorksObjectType", related_name="reports"
    )

    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    def render_string(self, permit_request, request) -> str:
        from permits.serializers import PermitRequestPrintSerializer

        context = {
            "report": self,
            "permit_request": permit_request,
            "permit_request_data": PermitRequestPrintSerializer(permit_request).data,
            "request": request,
        }
        return render_to_string("reports/report.html", context)

    def render_pdf(self, permit_request, generated_by) -> bytes:
        """Renders a PDF by calling the PDF generator service"""

        # Generate a token
        # TODO CRITICAL: add expiration to token and/or ensure it gets deleted
        # (fix by using better token implementation than DRF)
        token, token_was_created = Token.objects.get_or_create(user=generated_by)
        data = {
            "url": reverse(
                "reports:permit_request_report_contents",
                args=[permit_request.pk, self.pk],
            ),
            "token": token.key,
        }
        pdf_response = requests.post("http://pdf:5000/", data=data)

        # TODO: race condition if two PDFs are generated at the same time
        # (fix by using better token implementation than DRF)
        if token_was_created:
            token.delete()

        if pdf_response.status_code != 200:
            raise RuntimeError(_("La génération du PDF a échoué."))

        return pdf_response.content

    def __str__(self):
        return self.name
