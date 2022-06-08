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

    def render_string(self, permit_request) -> str:
        from permits.serializers import PermitRequestPrintSerializer

        context = {
            "report": self,
            "permit_request": permit_request,
            "permit_request_data": PermitRequestPrintSerializer(permit_request).data,
        }
        return render_to_string("reports/report.html", context)



    def __str__(self):
        return self.name
