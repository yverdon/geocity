import dataclasses
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils import timezone
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from . import fields


ACTOR_TYPE_OTHER = 0
ACTOR_TYPE_REQUESTOR = 1
ACTOR_TYPE_OWNER = 2
ACTOR_TYPE_COMPANY = 3
ACTOR_TYPE_CLIENT = 4
ACTOR_TYPE_SECURITY = 5
ACTOR_TYPE_ASSOCIATION = 6
ACTOR_TYPE_CHOICES = (
    (ACTOR_TYPE_OTHER, _("Autres")),
    (ACTOR_TYPE_OWNER, _("Propriétaire")),
    (ACTOR_TYPE_COMPANY, _("Entreprise")),
    (ACTOR_TYPE_CLIENT, _("Maître d'ouvrage")),
    (ACTOR_TYPE_REQUESTOR, _("Requérant si différent de l'auteur de la demande")),
    (ACTOR_TYPE_SECURITY, _("Sécurité")),
    (ACTOR_TYPE_ASSOCIATION, _("Association")),
)


class PermitDepartment(models.Model):

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE
    )
    description = models.CharField(
        _('description'),
        max_length=100,
        default='Service'
    )
    is_validator = models.BooleanField(
        _("is_validator")
    )
    is_admin = models.BooleanField(
        _("is_admin")
    )
    is_archeologist = models.BooleanField(
        _("is_archeologist")
    )
    administrative_entity = models.ForeignKey(
        'PermitAdministrativeEntity',
        null=True,
        on_delete=models.SET_NULL,
        related_name='departments',
        verbose_name=_("permit_administrative_entity")
    )
    is_default_validator = models.BooleanField(
        _("sélectionné par défaut pour les validations"),
        default=False
    )

    class Meta:
        verbose_name = _("Configuration du service")
        verbose_name_plural = _("Configuration des services")

    def __str__(self):
        return str(self.group)


class PermitAdministrativeEntity(models.Model):
    name = models.CharField(
        _('name'),
        max_length=128
    )
    ofs_id = models.PositiveIntegerField(
        _("ofs_id")
    )
    link = models.URLField(
        _("Lien"),
        max_length=200,
        blank=True
    )
    archive_link = models.URLField(
        _("Archives externes"),
        max_length=1024,
        blank=True
    )
    legal_document = fields.AministrativeEntityFileField(
        _('Directive'), blank=True, upload_to='administrative_entity_files/')
    general_informations = models.CharField(
        _("Informations"),
        blank=True,
        max_length=1024,
    )
    link = models.URLField(
        _("Lien"),
        max_length=200,
        blank=True
    )
    logo_main = fields.AministrativeEntityFileField(
        _('Logo principal'), blank=True, upload_to='administrative_entity_files/')
    logo_secondary = fields.AministrativeEntityFileField(
        _('Logo secondaire'), blank=True, upload_to='administrative_entity_files/')
    title_signature_1 = models.CharField(
        _('Signature Gauche'),
        max_length=128,
        blank=True
    )
    image_signature_1 = fields.AministrativeEntityFileField(
        _('Signature gauche'), blank=True, upload_to='administrative_entity_files/')
    title_signature_2 = models.CharField(
        _('Signature Droite'),
        max_length=128,
        blank=True
    )
    image_signature_2 = fields.AministrativeEntityFileField(
        _('Signature droite'), blank=True, upload_to='administrative_entity_files/')
    phone = models.CharField(
        _("Téléphone"),
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$',
                message='Seuls les chiffres et les espaces sont autorisés.'
            )
        ]
    )
    geom = geomodels.MultiPolygonField(
        _("geom"),
        null=True,
        srid=2056
    )

    class Meta:
        verbose_name = _('Configuration de l\'entité administrative (commune, organisation)')
        verbose_name_plural = _('Configuration de l\'entité administrative (commune, organisation)')

    def __str__(self):
        return self.name


class PermitAuthor(models.Model):
    """ User
    """
    company_name = models.CharField(
        _("Raison Sociale"),
        max_length=100, blank=True
    )
    vat_number = models.CharField(
        _("Numéro TVA"),
        max_length=19,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^(CHE-)+\d{3}\.\d{3}\.\d{3}(\sTVA)?$',
                message='Le code d\'entreprise doit être de type \
                         CHE-123.456.789 (TVA) \
                         et vous pouvez le trouver sur \
                         le registe fédéral des entreprises \
                         https://www.uid.admin.ch/search.aspx'
            )
        ]
    )
    address = models.CharField(
        _("Rue"),
        max_length=100,
    )
    zipcode = models.PositiveIntegerField(
        _("NPA"),
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(9999)
        ],
    )
    city = models.CharField(
        _("Ville"),
        max_length=100,
    )
    phone_first = models.CharField(
        _("Téléphone principal"),
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$',
                message='Seuls les chiffres et les espaces sont autorisés.'
            )
        ]
    )
    phone_second = models.CharField(
        _("Téléphone secondaire"),
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$',
                message='Seuls les chiffres et les espaces sont autorisés.'
            )
        ]
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Auteur')

    def get_absolute_url(self):

        return reverse('permits:genericauthorview', args=[str(self.id)])

    def __str__(self):

        return str(self.user.first_name) + ' ' + str(self.user.last_name) if self.user else str(self.pk)


class PermitActor(models.Model):
    """ Contacts
    """
    first_name = models.CharField(
        _("Prénom"),
        max_length=150,
    )
    last_name = models.CharField(
        _("Nom"),
        max_length=100,
    )
    company_name = models.CharField(
        _("Entreprise"),
        max_length=100,
    )
    vat_number = models.CharField(
        _("Numéro TVA"),
        max_length=19,
        blank=True
    )
    address = models.CharField(
        _("Adresse"),
        max_length=100,
    )
    zipcode = models.PositiveIntegerField(
        _("NPA"),
    )
    city = models.CharField(
        _("Ville"),
        max_length=100,
    )
    phone = models.CharField(
        _("Téléphone"),
        max_length=20,
    )
    email = models.EmailField(
        _("Email"),
    )

    class Meta:
        verbose_name = _('Contact')


    def __str__(self):
        return self.name


class WorksObjectTypeChoice(models.Model):
    """
    This intermediary model represents the selected objects for a permit
    request. Property values will then point to this model.
    """
    permit_request = models.ForeignKey(
        'PermitRequest',
        on_delete=models.CASCADE
    )
    works_object_type = models.ForeignKey(
        'WorksObjectType',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [('permit_request', 'works_object_type')]


class PermitActorType(models.Model):

    type = models.PositiveSmallIntegerField(
        _("type de contact"),
        choices=ACTOR_TYPE_CHOICES,
        default=ACTOR_TYPE_OTHER
    )
    works_type = models.ForeignKey(
        'WorksType',
        on_delete=models.CASCADE,
        verbose_name=_("type de travaux"),
        related_name='works_contact_types'
    )

    class Meta:
        verbose_name = _("Configuration du contact à saisir")
        verbose_name_plural = _("Configuration des contacts à saisir")

    def __str__(self):
        return self.get_type_display() + ' (' + str(self.works_type) + ')'


class PermitRequestActor(models.Model):
    actor = models.ForeignKey(
        PermitActor,
        on_delete=models.CASCADE
    )
    permit_request = models.ForeignKey(
        'PermitRequest',
        on_delete=models.CASCADE,
        related_name='permit_request_actors'
    )
    actor_type = models.PositiveSmallIntegerField(
        _("type de contact"),
        choices=ACTOR_TYPE_CHOICES,
        default=ACTOR_TYPE_OTHER
    )

    class Meta:
        verbose_name = _("Relation permis-contact")
        verbose_name_plural = _("Relations permis-contact")

    def __str__(self):
        return "{} - {}".format(str(self.actor), str(self.get_actor_type_display()))


class PermitRequest(models.Model):
    STATUS_DRAFT = 0
    STATUS_SUBMITTED_FOR_VALIDATION = 1
    STATUS_APPROVED = 2
    STATUS_PROCESSING = 3
    STATUS_AWAITING_SUPPLEMENT = 4
    STATUS_AWAITING_VALIDATION = 5
    STATUS_REJECTED = 6

    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Brouillon")),
        (STATUS_SUBMITTED_FOR_VALIDATION, _("Envoyée, en attente de traitement")),
        (STATUS_AWAITING_SUPPLEMENT, _("Demande de compléments")),
        (STATUS_PROCESSING, _("En traitement")),
        (STATUS_AWAITING_VALIDATION, _("En validation")),
        (STATUS_APPROVED, _("Approuvée")),
        (STATUS_REJECTED, _("Refusée")),
    )
    AMENDABLE_STATUSES = {
        STATUS_SUBMITTED_FOR_VALIDATION,
        STATUS_PROCESSING,
        STATUS_AWAITING_SUPPLEMENT
    }

    ARCHEOLOGY_STATUS_IRRELEVANT = 0
    ARCHEOLOGY_STATUS_UNKNOWN = 1
    ARCHEOLOGY_STATUS_NEVER = 2
    ARCHEOLOGY_STATUS_PARTIAL = 3
    ARCHEOLOGY_STATUS_DONE = 4
    ARCHEOLOGY_STATUS_CHOICES = (
        (ARCHEOLOGY_STATUS_IRRELEVANT, _("Non pertinent")),
        (ARCHEOLOGY_STATUS_UNKNOWN, _("Inconnu")),
        (ARCHEOLOGY_STATUS_NEVER, _("Pas fouillé")),
        (ARCHEOLOGY_STATUS_PARTIAL, _("Partiellement fouillé")),
        (ARCHEOLOGY_STATUS_DONE, _("Déjà fouillé")),
    )

    status = models.PositiveSmallIntegerField(
        _("état"),
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    created_at = models.DateTimeField(
        _("date de création"),
        default=timezone.now
    )
    validated_at = models.DateTimeField(
        _("date de validation"),
        null=True
    )
    printed_at = models.DateTimeField(
        _("date d'impression"),
        null=True
    )
    printed_by = models.CharField(
        _("imprimé par"),
        max_length=255,
        blank=True
    )
    printed_file = fields.AministrativeEntityFileField(
            _('Permis imprimé'), null=True, blank=True, upload_to='printed_permits/')
    works_object_types = models.ManyToManyField(
        'WorksObjectType',
        through=WorksObjectTypeChoice,
        related_name='permit_requests'
    )
    administrative_entity = models.ForeignKey(
        PermitAdministrativeEntity,
        on_delete=models.CASCADE,
        verbose_name=_("commune"),
        related_name='permit_requests'
    )
    author = models.ForeignKey(
        'PermitAuthor',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("auteur"),
        related_name='permit_requests'
    )
    actors = models.ManyToManyField(
        'PermitActor',
        related_name='+',
        through=PermitRequestActor
    )
    archeology_status = models.PositiveSmallIntegerField(
        _("Statut archéologique"),
        choices=ARCHEOLOGY_STATUS_CHOICES,
        default=ARCHEOLOGY_STATUS_IRRELEVANT
    )
    intersected_geometries = models.CharField(
        _("Entités géométriques concernées"),
        max_length=1024,
        null=True
    )
    price = models.DecimalField(
        _("Émolument"),
        decimal_places=2,
        max_digits=7,
        null=True,
        blank=True
    )
    exemption = models.TextField(
        _("Dérogation"),
        blank=True
    )
    opposition = models.TextField(
        _("Opposition"),
        blank=True
    )
    comment = models.TextField(
        _("Analyse du service pilote"),
        blank=True
    )
    validation_pdf = fields.PermitRequestFileField(
        _("pdf de validation"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        upload_to="validations"
    )
    creditor_type = models.PositiveSmallIntegerField(
        _("Destinaire de la facture"),
        choices=ACTOR_TYPE_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("demande de permis")
        verbose_name_plural = _("demandes de permis")
        permissions = [
            ('amend_permit_request', _("Traiter les demandes de permis")),
            ('validate_permit_request', _("Valider les demandes de permis")),
            ('classify_permit_request', _("Classer les demandes de permis")),
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

    def has_validations(self):
        return True if self.validations.all().count() > 0 else False


class WorksType(models.Model):
    name = models.CharField(
        _("nom"),
        max_length=255
    )

    class Meta:
        verbose_name = _("Configuration du type de travaux")
        verbose_name_plural = _("Configuration types de travaux")

    def __str__(self):
        return self.name


class WorksObjectType(models.Model):
    """
    Represents a works object for a specific works type.
    """
    works_type = models.ForeignKey(
        'WorksType',
        on_delete=models.CASCADE,
        verbose_name=_("type de travaux"),
        related_name='works_object_types'
    )
    works_object = models.ForeignKey(
        'WorksObject',
        on_delete=models.CASCADE,
        verbose_name=_("objet des travaux"),
        related_name='works_object_types'
    )
    administrative_entities = models.ManyToManyField(
        PermitAdministrativeEntity,
        verbose_name=_("communes"),
        related_name='works_object_types'
    )

    class Meta:
        verbose_name = _("Configuration type-objet-entité administrative")
        verbose_name_plural = _("Configurations type-objet-entité administrative")
        unique_together = [('works_type', 'works_object')]

    def __str__(self):
        return "{} ({})".format(
            self.works_object.name,
            self.works_type.name,self.administrative_entities.name
        )


class WorksObject(models.Model):
    name = models.CharField(_("nom"), max_length=255)
    works_types = models.ManyToManyField(
        WorksType,
        through=WorksObjectType,
        related_name='works_objects',
        verbose_name=_("types de travaux")
    )

    class Meta:
        verbose_name = _("Configuration de l\'objet des travaux")
        verbose_name_plural = _("Configuration des objets des travaux")

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

    name = models.CharField(
        _("nom"),
        max_length=255
    )
    input_type = models.CharField(
        _("type de caractéristique"),
        max_length=30,
        choices=INPUT_TYPE_CHOICES
    )
    is_mandatory = models.BooleanField(
        _("obligatoire"),
        default=False
    )
    works_object_types = models.ManyToManyField(
        WorksObjectType,
        verbose_name=_("objets des travaux"),
        related_name='properties'
    )

    class Meta:
        verbose_name = _("Configuration de la caractéristique")
        verbose_name_plural = _("Configuration des caractéristiques")

    def __str__(self):
        return self.name


class WorksObjectPropertyValue(models.Model):
    """
    Value of a property for a selected object in a permit request.
    """
    property = models.ForeignKey(
        WorksObjectProperty,
        verbose_name=_("caractéristique"),
        on_delete=models.PROTECT,
        related_name='+'
    )
    works_object_type_choice = models.ForeignKey(
        WorksObjectTypeChoice,
        verbose_name=_("objet des travaux"),
        on_delete=models.CASCADE,
        related_name='properties'
    )
    # Storing the value in a JSON field allows to keep the value type
    # (eg. boolean, int) instead of transforming everything to str
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

    permit_request = models.ForeignKey(
        PermitRequest,
        on_delete=models.CASCADE,
        related_name="validations"
    )
    department = models.ForeignKey(
        "PermitDepartment",
        on_delete=models.CASCADE,
        related_name="permit_request_validations"
    )
    validation_status = models.IntegerField(
        _("Statut de validation"),
        choices=STATUS_CHOICES,
        default=STATUS_REQUESTED
    )
    comment_before = models.TextField(
        _("Commentaires (avant)"),
        blank=True
    )
    comment_during = models.TextField(
        _("Commentaires (pendant)"),
        blank=True
    )
    comment_after = models.TextField(
        _("Commentaires (après)"),
        blank=True
    )
    validated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )
    validated_at = models.DateTimeField(
        _("Validé le"),
        null=True
    )

    class Meta:
        unique_together = ("permit_request", "department")
        verbose_name = _("Validation par le service")
        verbose_name_plural = _("Validations par les services")

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
    permit_request = models.ForeignKey(
        'PermitRequest',
        on_delete=models.CASCADE,
        related_name='geo_time'
    )
    starts_at = models.DateTimeField(
        _("Date planifiée de début")
    )
    ends_at = models.DateTimeField(
        _("Date planifiée de fin")
    )
    comment = models.CharField(
        _("Commentaire"),
        max_length=1024,
        blank=True
    )
    external_link = models.URLField(
        _("Lien externe"),
        blank=True
    )
    geom = geomodels.GeometryCollectionField(
        _("Localisation"),
        null=True,
        srid=2056
    )

    class Meta:
        verbose_name = _("Agenda et géométrie")
        verbose_name_plural = _("Agenda et géométries")


class GeomLayer(models.Model):
    """
    Geometric entities that might be touched by the PermitRequest
    """
    layer_name = models.CharField(
        _("Nom de la couche source"),
        max_length=128,
        blank=True
    )
    description = models.CharField(
        _("Commentaire"),
        max_length=1024,
        blank=True
    )
    source_id = models.CharField(
        _("Id entité"),
        max_length=128,
        blank=True
    )
    source_subid = models.CharField(
        _("Id entité secondaire"),
        max_length=128,
        blank=True
    )
    external_link = models.URLField(
        _("Lien externe"),
        blank=True
    )
    geom = geomodels.MultiPolygonField(
        _("Géométrie"),
        null=True,
        srid=2056
    )

    class Meta:
        verbose_name = _("Entité géographique à intersecter")
        verbose_name_plural = _("Entités géographiques à intersecter")
