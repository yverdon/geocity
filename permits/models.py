from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from gpf.models import Actor, AdministrativeEntity


class WorksObjectTypeChoice(models.Model):
    """
    This intermediary model represents the selected objects for a permit
    request. Property values will then point to this model.
    """
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.CASCADE, null=True)
    works_object_type = models.ForeignKey('WorksObjectType', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = [('permit_request', 'works_object_type')]


class PermitRequestActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True)
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255, null=True)
    actor_type = models.ForeignKey('PermitActorType', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _("permis-acteur")
        verbose_name_plural = _("permis-acteurs")



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

    street_name = models.CharField(_("Rue"), max_length=512, null=True)
    street_number = models.CharField(_("Numero"), max_length=32, null=True)
    npa = models.PositiveIntegerField(_("NPA"), null=True)
    city_name = models.CharField(_("Ville"), max_length=255, null=True)

    actors = models.ManyToManyField(Actor, related_name='+', through=PermitRequestActor)
    geom = geomodels.PointField(_("geom"), srid=2056)

    class Meta:
        verbose_name = _("demande de permis")
        verbose_name_plural = _("demandes de permis")


class WorksType(models.Model):
    TYPE_BUILDING= 0
    TYPE_PUBLICDOMAINUSAGE = 1
    TYPE_EVENT = 2
    TYPE_CHOICES = (
        (TYPE_BUILDING, _("Permis de construire avec dispense")),
        (TYPE_PUBLICDOMAINUSAGE, _("Utilisation du domaine public")),
        (TYPE_EVENT, _("Événements")),
    )

    type = models.PositiveSmallIntegerField(
        _("type"), choices=TYPE_CHOICES, default=TYPE_BUILDING
    )

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


class PermitActorType(models.Model):
    TYPE_OTHER= 0
    TYPE_REQUESTOR = 1
    TYPE_OWNER = 2
    TYPE_COMPANY = 3
    TYPE_CLIENT = 4
    TYPE_SECURITY= 5
    TYPE_ASSOCIATION= 6
    TYPE_CHOICES = (
        (TYPE_OTHER, _("Autres")),
        (TYPE_OWNER, _("Popriétaire")),
        (TYPE_COMPANY, _("Entreprise")),
        (TYPE_CLIENT, _("Maître d\'ouvrage")),
        (TYPE_REQUESTOR, _("Requérant si différent de l\'auteur de la demande")),
        (TYPE_SECURITY, _("Sécurité")),
        (TYPE_ASSOCIATION, _("Association")),
    )
    type = models.PositiveSmallIntegerField(
        _("type de contact"), choices=TYPE_CHOICES, default=TYPE_OTHER
    )
    is_mandatory = models.BooleanField(_("obligatoire"), default=False)
    works_type = models.ForeignKey(
        'WorksType', on_delete=models.CASCADE, verbose_name=_("type de travaux"), related_name='works_contact_types'
    )

    class Meta:
        verbose_name = _("contact à saisir")
        verbose_name_plural = _("contacts à saisir")

    def __str__(self):
        return str(self.type) + '(' + str(self.works_type) + ')'
