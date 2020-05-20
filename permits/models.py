import dataclasses

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils import timezone
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from gpf import models as gpfmodels


ACTOR_TYPE_OTHER = 0
ACTOR_TYPE_REQUESTOR = 1
ACTOR_TYPE_OWNER = 2
ACTOR_TYPE_COMPANY = 3
ACTOR_TYPE_CLIENT = 4
ACTOR_TYPE_SECURITY = 5
ACTOR_TYPE_ASSOCIATION = 6
ACTOR_TYPE_CHOICES = (
    (ACTOR_TYPE_OTHER, _("Autres")),
    (ACTOR_TYPE_OWNER, _("Popriétaire")),
    (ACTOR_TYPE_COMPANY, _("Entreprise")),
    (ACTOR_TYPE_CLIENT, _("Maître d'ouvrage")),
    (ACTOR_TYPE_REQUESTOR, _("Requérant si différent de l'auteur de la demande")),
    (ACTOR_TYPE_SECURITY, _("Sécurité")),
    (ACTOR_TYPE_ASSOCIATION, _("Association")),
)


class PermitActor(models.Model):

    name = models.CharField(_("name"), max_length=100, blank=True)
    firstname = models.CharField(_("firstname"), max_length=100, blank=True)
    company_name = models.CharField(_("company_name"), max_length=100, blank=True)
    vat_number = models.CharField(_("vat_number"),
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                regex='([CHE-])+\d{3}[.]+\d{3}[.]+\d{3}',
                message='Le code d\'entreprise doit être de type CHE-123.456.789 et vous pouvez le trouver sur \
                le registe fédéral des entreprises \
                https://www.uid.admin.ch/search.aspx'
        )])
    address = models.CharField(_("address"), max_length=100, blank=True)
    zipcode = models.PositiveIntegerField(_("zipcode"), null=True)
    city = models.CharField(_("city"), max_length=100, blank=True)
    phone = models.CharField(_("Téléphone"),
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex='^(\s*[0-9]+\s*)+$',
                message='Seuls les chiffres et les espaces sont autorisés'
        )])
    email = models.EmailField(_("email"), blank=True)

    class Meta:
        verbose_name = _('Demandeur')


    def __str__(self):
        return self.name


class WorksObjectTypeChoice(models.Model):
    """
    This intermediary model represents the selected objects for a permit
    request. Property values will then point to this model.
    """
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.CASCADE)
    works_object_type = models.ForeignKey('WorksObjectType', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('permit_request', 'works_object_type')]


class PermitActorType(models.Model):

    type = models.PositiveSmallIntegerField(
        _("type de contact"), choices=ACTOR_TYPE_CHOICES, default=ACTOR_TYPE_OTHER
    )
    works_type = models.ForeignKey(
        'WorksType', on_delete=models.CASCADE, verbose_name=_("type de travaux"), related_name='works_contact_types'
    )

    class Meta:
        verbose_name = _("contact à saisir")
        verbose_name_plural = _("contacts à saisir")

    def __str__(self):
        return self.get_type_display() + ' (' + str(self.works_type) + ')'


class PermitRequestActor(models.Model):
    actor = models.ForeignKey(PermitActor, on_delete=models.CASCADE)
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.CASCADE, related_name='permit_request_actors')
    actor_type = models.PositiveSmallIntegerField(
        _("type de contact"), choices=ACTOR_TYPE_CHOICES, default=ACTOR_TYPE_OTHER
    )

    def __str__(self):
        return "{} - {}".format(str(self.actor), str(self.get_actor_type_display()))


class PermitRequest(models.Model):
    STATUS_DRAFT = 0
    STATUS_SUBMITTED_FOR_VALIDATION = 1
    STATUS_VALIDATED = 2
    STATUS_PROCESSING = 3
    STATUS_AWAITING_SUPPLEMENT = 4
    STATUS_AWAITING_VALIDATION = 5

    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Brouillon")),
        (STATUS_SUBMITTED_FOR_VALIDATION, _("Envoyée, en attente de traitement")),
        (STATUS_PROCESSING, _("En traitement")),
        (STATUS_VALIDATED, _("Validée")),
        (STATUS_AWAITING_SUPPLEMENT, _("Demande de compléments")),
        (STATUS_AWAITING_VALIDATION, _("En validation")),
    )
    AMENDABLE_STATUSES = {
        STATUS_SUBMITTED_FOR_VALIDATION,
        STATUS_PROCESSING,
        STATUS_AWAITING_SUPPLEMENT
    }

    status = models.PositiveSmallIntegerField(
        _("état"), choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    created_at = models.DateTimeField(_("date de création"), default=timezone.now)
    validated_at = models.DateTimeField(_("date de validation"), null=True)
    printed_at = models.DateTimeField(_("date d'impression"), null=True)
    printed_by = models.CharField(_("imprimé par"), max_length=255, blank=True)
    printed_file = models.FileField(
            _('permis imprimé'),
            upload_to='printed_permits/',
            blank=True,
            validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    works_object_types = models.ManyToManyField(
        'WorksObjectType', through=WorksObjectTypeChoice, related_name='permit_requests'
    )
    administrative_entity = models.ForeignKey(
        gpfmodels.AdministrativeEntity, on_delete=models.CASCADE, verbose_name=_("commune"), related_name='permit_requests'
    )
    author = models.ForeignKey(
        gpfmodels.Actor, null=True, on_delete=models.SET_NULL, verbose_name=_("auteur"), related_name='permit_requests'
    )
    actors = models.ManyToManyField(PermitActor, related_name='+', through=PermitRequestActor)

    price = models.DecimalField(_("Prix"), decimal_places=2, max_digits=7, null=True, blank=True)
    exemption = models.TextField(_("Dérogation"), blank=True)
    opposition = models.TextField(_("Opposition"), blank=True)
    comment = models.TextField(_("Commentaire"), blank=True)

    class Meta:
        verbose_name = _("demande de permis")
        verbose_name_plural = _("demandes de permis")
        permissions = [
            ('amend_permit_request', _("Amender les demandes de permis")),
            ('validate_permit_request', _("Valider les demandes de permis")),
        ]

    def is_draft(self):
        return self.status == self.STATUS_DRAFT

    def can_be_submitted_by_author(self):
        return self.can_be_edited_by_author()

    def can_be_edited_by_author(self):
        return self.status in {self.STATUS_AWAITING_SUPPLEMENT, self.STATUS_DRAFT}

    def can_be_deleted_by_author(self):
        return self.is_draft()

    def can_be_amended(self):
        return self.status in self.AMENDABLE_STATUSES

    def can_be_validated(self):
        return self.status == self.STATUS_AWAITING_VALIDATION

    def works_objects_html(self):
        """
        Return the works objects as a string, separated by <br> characters.
        """
        return format_html(
            "<br>".join(
                escape(f"{item.works_object.name} ({item.works_type.name})")
                for item in self.works_object_types.all()
            )
        )

    def get_pending_validations(self):
        return self.validations.filter(
            validation_status=PermitRequestValidation.STATUS_REQUESTED
        )


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
    administrative_entities = models.ManyToManyField(gpfmodels.AdministrativeEntity, verbose_name=_("communes"), related_name='works_object_types')

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


class PermitRequestValidation(models.Model):
    STATUS_REQUESTED = 0
    STATUS_APPROVED = 1
    STATUS_REJECTED = 2
    STATUS_CHOICES = (
        (STATUS_REQUESTED, _("En attente")),
        (STATUS_APPROVED, _("Approuvé")),
        (STATUS_REJECTED, _("Refusé")),
    )

    permit_request = models.ForeignKey(PermitRequest, on_delete=models.CASCADE, related_name="validations")
    department = models.ForeignKey(
        "gpf.Department", on_delete=models.CASCADE, related_name="permit_request_validations"
    )
    validation_status = models.IntegerField(_("Statut de validation"), choices=STATUS_CHOICES, default=STATUS_REQUESTED)
    comment_before = models.TextField(_("Commentaires (avant)"), blank=True)
    comment_during = models.TextField(_("Commentaires (pendant)"), blank=True)
    comment_after = models.TextField(_("Commentaires (après)"), blank=True)

    class Meta:
        unique_together = ("permit_request", "department")

    def is_pending(self):
        return self.validation_status == self.STATUS_REQUESTED


@dataclasses.dataclass
class Step:
    name: str
    url: str
    completed: bool = False
    enabled: bool = False
    errors_count: int = 0


class PermitRequestGeoTime(models.Model):
    """
    Permit location in space and time
    """
    permit_request = models.ForeignKey('PermitRequest', on_delete=models.CASCADE, related_name='geo_time')
    starts_at = models.DateTimeField(_("Date de début"))
    ends_at =models.DateTimeField(_("Date de fin"))
    comment = models.CharField(_("Commentaire"), max_length=1024, blank=True)
    external_link = models.URLField(_("Lien externe"), blank=True)
    geom = geomodels.GeometryCollectionField(_("Localisation"), null=True, srid=2056)
