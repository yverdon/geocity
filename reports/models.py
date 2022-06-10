from django.db import models

import io
import typing
from typing import Union
from django.shortcuts import render
import requests
import urllib
from urllib.request import urlopen
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from permits import models as permits_models
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.authtoken.models import Token
import typing
import io
import tarfile
from django import template
from django.utils.safestring import mark_safe
from jinja2.sandbox import SandboxedEnvironment
from rest_framework.authtoken.models import Token
import base64
import os
from django.contrib.staticfiles import finders
from .utils import run_docker_container, DockerRunFailedError

from polymorphic.models import PolymorphicModel

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


        # Generate a token
        # TODO CRITICAL: add expiration to token and/or ensure it gets deleted
        # (fix by using better token implementation than DRF)
        token, token_was_created = Token.objects.get_or_create(user=generated_by)

        context = {
            "report": self,
            "permit_request": permit_request,
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


class Section(PolymorphicModel):
    class Meta:

        ordering = ['order',]

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="sections")
    order = models.PositiveIntegerField(null=True, blank=True)

    def get_template(self):
        class_name = self.__class__.__name__.lower()
        return f"reports/sections/{class_name}.html"

    def get_context(self, context):
        return {
            **context,
            "section": self,
            "permit_request": context["permit_request"],
        }

    def render(self, report_context):
        template = self.get_template()
        section_context = self.get_context(report_context)
        return render_to_string(template, section_context)

    def __str__(self):
        return self._meta.verbose_name

class SectionMap(Section):
    layout_name = models.CharField(max_length=30)

class SectionParagraph(Section):
    title = models.CharField(default="", blank=True, max_length=2000)
    content = models.TextField(
        help_text=(
            _(
                "Il est possible d'accéder aux données de l'API avec la syntaxe suivante: `{{data.properties.geotime_aggregated.start_date}}`. Consultez les résults de <a href=\"http://localhost:9095/wfs3/collections/permits/items/1\">l'API</a> pour voir les données disponibles."
            )
        )
    )

    def get_context(self, context):
        from permits.serializers import PermitRequestPrintSerializer
        env = SandboxedEnvironment()
        data = PermitRequestPrintSerializer(context["permit_request"]).data
        rendered_content = env.from_string(self.content).render({"data": data})
        return {
            **super().get_context(context),
            "rendered_content": mark_safe(rendered_content),
        }

class SectionAuthor(Section):
    pass