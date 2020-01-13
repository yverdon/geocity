from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class WorksObjectTypeChoice(models.Model):
    """
    This intermediary model represents the selected objects for a permit
    request. Property values will then point to this model.
    """
    # TODO unicity constraints
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.CASCADE)
    works_object_type = models.ForeignKey('WorksObjectType', on_delete=models.CASCADE)


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
    works_objects_types = models.ManyToManyField('WorksObjectType', through=WorksObjectTypeChoice)

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


class WorksObjectType(models.Model):
    """
    Represents a works object for a specific works type.
    """
    works_type = models.ForeignKey(WorksType, on_delete=models.CASCADE)
    works_object = models.ForeignKey('WorksObject', on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({})".format(self.works_object.name, self.works_type.name)


class WorksObject(models.Model):
    name = models.CharField(_("nom"), max_length=255)
    works_types = models.ManyToManyField(
        WorksType, through=WorksObjectType, related_name='works_objects', verbose_name=_("types de travaux")
    )

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
    works_objects_types = models.ManyToManyField(WorksObjectType, verbose_name=_("objets des travaux"), related_name='properties')

    class Meta:
        verbose_name = _("caractéristique")
        verbose_name_plural = _("caractéristiques")

    def __str__(self):
        return self.name


class WorksObjectPropertyValue(models.Model):
    """
    Value of a property for a selected object in a permit request.
    """
    property = models.ForeignKey(
        WorksObjectProperty, verbose_name=_("caractéristique"),
        on_delete=models.PROTECT, related_name='+'
    )
    works_object_type_choice = models.ForeignKey(
        WorksObjectTypeChoice, verbose_name=_("objet des travaux"),
        on_delete=models.CASCADE, related_name='properties'
    )
    value = JSONField()
