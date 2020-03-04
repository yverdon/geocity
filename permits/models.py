from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from gpf.models import Actor, AdministrativeEntity

ACTOR_TYPE_OTHER= 0
ACTOR_TYPE_REQUESTOR = 1
ACTOR_TYPE_OWNER = 2
ACTOR_TYPE_COMPANY = 3
ACTOR_TYPE_CLIENT = 4
ACTOR_TYPE_SECURITY= 5
ACTOR_TYPE_ASSOCIATION= 6
ACTOR_TYPE_CHOICES = (
    (ACTOR_TYPE_OTHER, _("Autres")),
    (ACTOR_TYPE_OWNER, _("Popriétaire")),
    (ACTOR_TYPE_COMPANY, _("Entreprise")),
    (ACTOR_TYPE_CLIENT, _("Maître d'ouvrage")),
    (ACTOR_TYPE_REQUESTOR, _("Requérant si différent de l'auteur de la demande")),
    (ACTOR_TYPE_SECURITY, _("Sécurité")),
    (ACTOR_TYPE_ASSOCIATION, _("Association")),
)


class WorksObjectTypeChoice(models.Model):
    """
    This intermediary model represents the selected objects for a permit
    request. Property values will then point to this model.
    """
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.CASCADE)
    works_object_type = models.ForeignKey('WorksObjectType', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('permit_request', 'works_object_type')]


class PermitRequestActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)


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
    created_at = models.DateTimeField(_("date de création"), default=timezone.now)
    validated_at = models.DateTimeField(_("date de validation"), null=True)
    works_object_types = models.ManyToManyField(
        'WorksObjectType', through=WorksObjectTypeChoice, related_name='permit_requests'
    )
    administrative_entity = models.ForeignKey(
        AdministrativeEntity, on_delete=models.CASCADE, verbose_name=_("commune"), related_name='permit_requests'
    )
    author = models.ForeignKey(
        Actor, null=True, on_delete=models.SET_NULL, verbose_name=_("auteur"), related_name='permit_requests'
    )
    actors = models.ManyToManyField(Actor, related_name='+', through=PermitRequestActor)

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
    works_type = models.ForeignKey(
        'WorksType', on_delete=models.CASCADE, verbose_name=_("type de travaux"), related_name='works_object_types'
    )
    works_object = models.ForeignKey(
        'WorksObject', on_delete=models.CASCADE, verbose_name=_("objet des travaux"), related_name='works_object_types'
    )
    administrative_entities = models.ManyToManyField(AdministrativeEntity, verbose_name=_("communes"), related_name='works_object_types')

    class Meta:
        verbose_name = _("objet pour types de travaux")
        verbose_name_plural = _("objets pour types de travaux")
        unique_together = [('works_type', 'works_object')]

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
    works_object_types = models.ManyToManyField(WorksObjectType, verbose_name=_("objets des travaux"), related_name='properties')

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
    # Storing the value in a JSON field allows to keep the value type (eg. boolean, int) instead of transforming
    # everything to str
    value = JSONField()

    class Meta:
        unique_together = [('property', 'works_object_type_choice')]
