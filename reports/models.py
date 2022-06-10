from django.db import models

import io
import typing
from typing import Union
import requests
import urllib
from urllib.request import urlopen
from django.utils.translation import gettext_lazy as _
from streamfield.fields import StreamField
from .streamblocks.models import STREAMBLOCKS_MODELS
from django.template.loader import render_to_string
from django.conf import settings
from permits import models as permits_models
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.authtoken.models import Token

from .utils import run_docker_container, DockerRunFailedError


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


    def render_pdf(self, permit_request, generated_by, as_string=False) -> Union[bytes,str]:
        """Renders a PDF by calling the PDF generator service"""

        from permits.serializers import PermitRequestPrintSerializer

        # Generate a token
        # TODO CRITICAL: add expiration to token and/or ensure it gets deleted
        # (fix by using better token implementation than DRF)
        token, token_was_created = Token.objects.get_or_create(user=generated_by)

        context = {
            "report": self,
            "permit_request": permit_request,
            "permit_request_data": PermitRequestPrintSerializer(permit_request).data,
            "token": token.key,
        }
        html_string = render_to_string("reports/report.html", context)

        if as_string:
            return html_string

        commands = [
            "/io/input.html",
            "/io/output.pdf",
            token.key,
        ]

        try:
            output = run_docker_container(
                "geocity_pdf",
                commands,
                file_input=("/io/input.html", io.BytesIO(html_string.encode("utf-8"))),
                file_output="/io/output.pdf",
            )
        finally:
            # TODO: race condition if two PDFs are generated at the same time
            # (fix by using better token implementation than DRF)
            if token_was_created:
                token.delete()

        return output

    def __str__(self):
        return self.name
