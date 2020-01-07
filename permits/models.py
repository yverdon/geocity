from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class PermitRequest(models.Model):
    STATUS_DRAFT = 0
    STATUS_SUBMITTED = 1
    STATUS_VALIDATED = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Brouillon")),
        (STATUS_SUBMITTED, _("Envoyée")),
        (STATUS_VALIDATED, _("Validée")),
    )

    status = models.PositiveSmallIntegerField(
        _("état"), choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    created_at = models.DateTimeField(_("date de création"), default=datetime.now)
    validated_at = models.DateTimeField(_("date de validation"), null=True)

    class Meta:
        verbose_name = _("demande de permis")
        verbose_name_plural = _("demandes de permis")


class WorksType(models.Model):
    name = models.CharField(_("nom"), max_length=255)

    class Meta:
        verbose_name = _("type de travaux")
        verbose_name_plural = _("types de travaux")

    def __str__(self):
        return self.name


class WorksObject(models.Model):
    name = models.CharField(_("nom"), max_length=255)
    works_types = models.ManyToManyField(WorksType, verbose_name=_("types de travaux"))

    class Meta:
        verbose_name = _("objet des travaux")
        verbose_name_plural = _("objets des travaux")

    def __str__(self):
        return self.name


class WorksObjectProperty(models.Model):
    INPUT_TYPE_TEXT = 'text'
    INPUT_TYPE_CHECKBOX = 'checkbox'
    INPUT_TYPE_NUMBER = 'number'
    INPUT_TYPE_FILE = 'file'
    INPUT_TYPE_CHOICES = (
        (INPUT_TYPE_TEXT, _("Texte")),
        (INPUT_TYPE_CHECKBOX, _("Case à cocher")),
        (INPUT_TYPE_NUMBER, _("Nombre")),
        (INPUT_TYPE_FILE, _("Fichier")),
    )

    name = models.CharField(_("nom"), max_length=255)
    input_type = models.CharField(
        _("type de caractéristique"), max_length=30, choices=INPUT_TYPE_CHOICES
    )
    is_mandatory = models.BooleanField(_("obligatoire"), default=False)
    works_objects = models.ManyToManyField(WorksObject, verbose_name=_("objets des travaux"))

    class Meta:
        verbose_name = _("caractéristique")
        verbose_name_plural = _("caractéristiques")

    def __str__(self):
        return self.name


class WorksObjectChoice(models.Model):
    works_type = models.ForeignKey(
        WorksType, verbose_name=_("type de travaux"), on_delete=models.PROTECT,
        related_name='+'
    )
    works_object = models.ForeignKey(
        WorksObject, verbose_name=_("objet des travaux"),
        on_delete=models.PROTECT, related_name='+'
    )
    permit_request = models.ForeignKey(
        PermitRequest, verbose_name=_("demande de permis"),
        on_delete=models.CASCADE, related_name='works_objects'
    )


class WorksObjectPropertyValue(models.Model):
    property = models.ForeignKey(
        WorksObjectProperty, verbose_name=_("caractéristique"),
        on_delete=models.PROTECT, related_name='+'
    )
    works_object = models.ForeignKey(
        WorksObjectChoice, verbose_name=_("objet des travaux"),
        on_delete=models.CASCADE, related_name='properties'
    )
    value = JSONField()
