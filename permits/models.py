import collections
import dataclasses
import enum
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.gis.db import models as geomodels
from django.db.models import (
    JSONField,
    UniqueConstraint,
    F,
    ExpressionWrapper,
    BooleanField,
)
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models import Q, Max, Min
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager

from . import fields

# public types: for public/restricted features
PUBLIC_TYPE_CHOICES = (
    (True, _("Visible par tous les utilisateurs")),
    (False, _("Visible uniquement par les utilisateur autorisés")),
)

# Contact types
ACTOR_TYPE_OTHER = 0
ACTOR_TYPE_REQUESTOR = 1
ACTOR_TYPE_OWNER = 2
ACTOR_TYPE_COMPANY = 3
ACTOR_TYPE_CLIENT = 4
ACTOR_TYPE_SECURITY = 5
ACTOR_TYPE_ASSOCIATION = 6
ACTOR_TYPE_ENGINEER = 7
ACTOR_TYPE_WORKDIRECTOR = 8
ACTOR_TYPE_CHOICES = (
    (ACTOR_TYPE_ENGINEER, _("Architecte/Ingénieur")),
    (ACTOR_TYPE_ASSOCIATION, _("Association")),
    (ACTOR_TYPE_OTHER, _("Autres")),
    (ACTOR_TYPE_WORKDIRECTOR, _("Direction des travaux")),
    (ACTOR_TYPE_COMPANY, _("Entreprise")),
    (ACTOR_TYPE_CLIENT, _("Maître d'ouvrage")),
    (ACTOR_TYPE_OWNER, _("Propriétaire")),
    (ACTOR_TYPE_REQUESTOR, _("Requérant (si différent de l'auteur de la demande)")),
    (ACTOR_TYPE_SECURITY, _("Sécurité")),
)

# Input types
INPUT_TYPE_ADDRESS = "address"
INPUT_TYPE_CHECKBOX = "checkbox"
INPUT_TYPE_DATE = "date"
INPUT_TYPE_FILE = "file"
INPUT_TYPE_FILE_DOWNLOAD = "file_download"
INPUT_TYPE_LIST_MULTIPLE = "list_multiple"
INPUT_TYPE_LIST_SINGLE = "list_single"
INPUT_TYPE_NUMBER = "number"
INPUT_TYPE_REGEX = "regex"
INPUT_TYPE_TEXT = "text"
INPUT_TYPE_TITLE = "title"

# Actions
ACTION_AMEND = "amend"
ACTION_REQUEST_VALIDATION = "request_validation"
ACTION_VALIDATE = "validate"
ACTION_POKE = "poke"
ACTION_PROLONG = "prolong"
# If you add an action here, make sure you also handle it in `views.get_form_for_action`,  `views.handle_form_submission`
# and services.get_actions_for_administrative_entity
ACTIONS = [
    ACTION_AMEND,
    ACTION_REQUEST_VALIDATION,
    ACTION_VALIDATE,
    ACTION_POKE,
    ACTION_PROLONG,
]


def printed_permit_request_storage(instance, filename):
    return f"permit_requests_uploads/{instance.permit_request.pk}/{filename}"


@dataclasses.dataclass
class Step:
    name: str
    url: str
    completed: bool = False
    enabled: bool = False
    errors_count: int = 0


class StepType(enum.Enum):
    ADMINISTRATIVE_ENTITY = "administrative_entity"
    WORKS_TYPES = "works_types"
    WORKS_OBJECTS = "works_objects"
    PROPERTIES = "properties"
    GEO_TIME = "geo_time"
    APPENDICES = "appendices"
    ACTORS = "actors"
    SUBMIT = "submit"


# Required to be able to use the enum in Django templates
StepType.do_not_call_in_templates = True


class PermitDepartment(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.CharField(_("description"), max_length=100, default="Service")
    is_validator = models.BooleanField(
        _("validateur"),
        help_text=_(
            "Cocher si les membres doivent apparaître dans la liste des services consultables pour la validation"
        ),
    )
    is_backoffice = models.BooleanField(
        _("secrétariat"),
        default=False,
        help_text=_(
            "Cocher si les membres font partie du secrétariat. Ils seront notifiés des évolutions de la demande"
        ),
    )
    administrative_entity = models.ForeignKey(
        "PermitAdministrativeEntity",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="departments",
        verbose_name=_("entité administrative"),
    )
    is_default_validator = models.BooleanField(
        _("sélectionné par défaut pour les validations"), default=False
    )
    integrator = models.IntegerField(
        _("Groupe des administrateurs"),
        help_text=_("Identifiant du groupe"),
        default=0,
    )
    is_integrator_admin = models.BooleanField(
        _("Intégrateur"),
        help_text=_("Cocher si les membres peuvent accéder à l'admin de Django"),
        default=False,
    )
    mandatory_2fa = models.BooleanField(
        _("2FA obligatoire"),
        help_text=_(
            "Cocher si les membres doivent obligatoirement utiliser la double authentification"
        ),
        default=False,
    )
    integrator_email_domains = models.CharField(
        _("Domaines d'emails visibles pour l'intégrateur"),
        help_text=_(
            "Liste de domaines séparés par des virgules ',' correspondant aux utilisateurs rattachés à l'entité administrative (ex: ma-commune.ch,commune.ch)"
        ),
        blank=True,
        max_length=254,
    )
    integrator_emails_exceptions = models.CharField(
        _("Emails complets visibles pour l'intégrateur"),
        help_text=_(
            "Liste d'emails séparés par des virgules ',' d'utilisateurs spécifiques rattachés à l'entité administrative (ex: greffe@nowhere.com)"
        ),
        blank=True,
        max_length=254,
    )

    class Meta:
        verbose_name = _("2.1 Configuration du service (pilote, validateur...)")
        verbose_name_plural = _(
            "2.1 Configuration des services (pilote, validateur...)"
        )

    def __str__(self):
        return str(self.group)


class PermitAdministrativeEntityQuerySet(models.QuerySet):
    def filter_by_tags(self, tags):
        return self.filter(tags__name__in=[tag.lower() for tag in tags])


class PermitAdministrativeEntityManager(models.Manager):
    def get_queryset(self):
        return PermitAdministrativeEntityQuerySet(self.model)

    def public(self):
        return self.get_queryset().filter(anonymous_user__isnull=False)


class PermitAdministrativeEntity(models.Model):
    name = models.CharField(_("name"), max_length=128)
    ofs_id = models.PositiveIntegerField(_("Numéro OFS"))
    link = models.URLField(_("Lien"), max_length=200, blank=True)
    archive_link = models.URLField(_("Archives externes"), max_length=1024, blank=True)
    general_informations = models.CharField(
        _("Informations"), blank=True, max_length=1024,
    )
    custom_signature = models.TextField(
        _("Signature des emails"),
        help_text=_("Si vide, le nom de l'entité sera utilisé"),
        max_length=1024,
        blank=True,
    )
    phone = models.CharField(
        _("Téléphone"),
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message="Seuls les chiffres et les espaces sont autorisés.",
            )
        ],
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )
    geom = geomodels.MultiPolygonField(_("geom"), null=True, srid=2056)
    tags = TaggableManager(
        blank=True,
        verbose_name="Mots-clés",
        help_text="Mots clefs sans espaces, séparés par des virgules permettant de filtrer les entités par l'url: https://geocity.ch/?entityfilter=yverdon",
    )
    objects = PermitAdministrativeEntityManager()
    expeditor_name = models.CharField(
        _("Nom de l'expéditeur des notifications"), max_length=255, blank=True
    )
    expeditor_email = models.CharField(
        _("Adresse email de l'expéditeur des notifications"),
        max_length=255,
        blank=True,
        validators=[
            RegexValidator(
                regex="^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$",
                message="Le format de l'adresse email n'est pas valable.",
            )
        ],
    )

    class Meta:
        verbose_name = _(
            "1.1 Configuration de l'entité administrative (commune, organisation)"
        )
        verbose_name_plural = _(
            "1.1 Configuration de l'entité administrative (commune, organisation)"
        )
        permissions = [
            ("see_private_requests", _("Voir les demandes restreintes")),
        ]

    def __str__(self):
        return self.name


class PermitAuthorManager(models.Manager):
    def create_temporary_user(self, entity):
        # Multiple temp users might exist at the same time
        last_temp_user = self.get_queryset().filter(is_temporary=True).last()
        if last_temp_user:
            nb = int(last_temp_user.user.username.split("_")[2]) + 1
        else:
            nb = 0

        username = "%s%s" % (settings.TEMPORARY_USER_PREFIX, nb)
        email = "%s@%s" % (username, settings.SITE_DOMAIN)
        zipcode = settings.TEMPORARY_USER_ZIPCODE

        temp_user = User.objects.create_user(
            username, email, password=None, first_name="Temporaire", last_name="Anonyme"
        )

        new_temp_author = super().create(user=temp_user, zipcode=zipcode,)

        return new_temp_author

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_temporary=ExpressionWrapper(
                    Q(user__username__startswith=settings.TEMPORARY_USER_PREFIX),
                    output_field=BooleanField(),
                )
            )
        )


class PermitAuthor(models.Model):
    """User"""

    company_name = models.CharField(_("Raison Sociale"), max_length=100, blank=True)
    vat_number = models.CharField(
        _("Numéro TVA"),
        max_length=19,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^(CHE-)+\d{3}\.\d{3}\.\d{3}(\sTVA)?$",
                message="Le code d'entreprise doit être de type \
                         CHE-123.456.789 (TVA) \
                         et vous pouvez le trouver sur \
                         le registe fédéral des entreprises \
                         https://www.uid.admin.ch/search.aspx",
            )
        ],
    )
    address = models.CharField(_("Rue"), max_length=100,)
    zipcode = models.PositiveIntegerField(
        _("NPA"), validators=[MinValueValidator(1000), MaxValueValidator(9999)],
    )
    city = models.CharField(_("Ville"), max_length=100,)
    phone_first = models.CharField(
        _("Téléphone principal"),
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message="Seuls les chiffres et les espaces sont autorisés.",
            )
        ],
    )
    phone_second = models.CharField(
        _("Téléphone secondaire"),
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message="Seuls les chiffres et les espaces sont autorisés.",
            )
        ],
    )
    notify_per_email = models.BooleanField(_("Me notifier par e-mail"), default=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    history = HistoricalRecords()

    administrative_entity = models.OneToOneField(
        "PermitAdministrativeEntity",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="anonymous_user",
        verbose_name=_("entité administrative"),
    )

    objects = PermitAuthorManager()

    def clean(self):
        if self.user and self.user.is_active and self.administrative_entity is not None:
            raise ValidationError(
                _(
                    "Seul·e un·e auteur désactivé·e peut être relié directement "
                    "à une entité administrative, et ainsi être considéré·e "
                    "auteur·e anonyme de l'entité."
                )
            )

    @cached_property
    def is_anonymous(self):
        """
        PermitAuthor unique per AdministrativeEntity.
        Never logged in. Used to save anonymous requests.
        """
        return (
            self.user
            and not self.user.is_active
            and self.administrative_entity is not None
        )

    @cached_property
    def is_temporary(self):
        """
        PermitAuthor created when starting an anonymous permit request,
        then deleted at the submission (replaced by an anonymous user).
        """
        return self.user and self.user.username.startswith(
            settings.TEMPORARY_USER_PREFIX
        )

    class Meta:
        verbose_name = _("3.2 Consultation de l'auteur")
        verbose_name_plural = _("3.2 Consultation des auteurs")

    def get_absolute_url(self):

        return reverse("permits:genericauthorview", args=[str(self.id)])

    def __str__(self):

        return (
            str(self.user.first_name) + " " + str(self.user.last_name)
            if self.user
            else str(self.pk)
        )


class PermitActor(models.Model):
    """Contacts"""

    first_name = models.CharField(_("Prénom"), max_length=150,)
    last_name = models.CharField(_("Nom"), max_length=100,)
    company_name = models.CharField(_("Entreprise"), max_length=100, blank=True)
    vat_number = models.CharField(_("Numéro TVA"), max_length=19, blank=True)
    address = models.CharField(_("Adresse"), max_length=100,)
    zipcode = models.PositiveIntegerField(_("NPA"),)
    city = models.CharField(_("Ville"), max_length=100,)
    phone = models.CharField(_("Téléphone"), max_length=20,)
    email = models.EmailField(_("Email"),)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Contact")

    def __str__(self):
        return self.first_name + " " + self.last_name


class WorksObjectTypeChoice(models.Model):
    """
    This intermediary model represents the selected objects for a permit
    request. Property values will then point to this model.
    """

    permit_request = models.ForeignKey("PermitRequest", on_delete=models.CASCADE)
    works_object_type = models.ForeignKey("WorksObjectType", on_delete=models.CASCADE)

    class Meta:
        unique_together = [("permit_request", "works_object_type")]


class PermitActorType(models.Model):

    type = models.PositiveSmallIntegerField(
        _("type de contact"), choices=ACTOR_TYPE_CHOICES, default=ACTOR_TYPE_OTHER
    )
    works_type = models.ForeignKey(
        "WorksType",
        on_delete=models.CASCADE,
        verbose_name=_("type de demande"),
        related_name="works_contact_types",
    )
    is_mandatory = models.BooleanField(_("obligatoire"), default=True)
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    class Meta:
        verbose_name = _("1.6 Configuration du contact")
        verbose_name_plural = _("1.6 Configuration des contacts")
        unique_together = [["type", "works_type"]]

    def __str__(self):
        return self.get_type_display() + " (" + str(self.works_type) + ")"


class PermitRequestActor(models.Model):
    actor = models.ForeignKey(PermitActor, on_delete=models.CASCADE)
    permit_request = models.ForeignKey(
        "PermitRequest", on_delete=models.CASCADE, related_name="permit_request_actors"
    )
    actor_type = models.PositiveSmallIntegerField(
        _("type de contact"), choices=ACTOR_TYPE_CHOICES, default=ACTOR_TYPE_OTHER
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
    STATUS_RECEIVED = 7

    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Brouillon")),
        (STATUS_SUBMITTED_FOR_VALIDATION, _("Envoyée, en attente de traitement")),
        (STATUS_AWAITING_SUPPLEMENT, _("Demande de compléments")),
        (STATUS_PROCESSING, _("En traitement")),
        (STATUS_AWAITING_VALIDATION, _("En validation")),
        (STATUS_APPROVED, _("Approuvée")),
        (STATUS_REJECTED, _("Refusée")),
        (STATUS_RECEIVED, _("Réceptionnée")),
    )
    AMENDABLE_STATUSES = {
        STATUS_SUBMITTED_FOR_VALIDATION,
        STATUS_PROCESSING,
        STATUS_AWAITING_SUPPLEMENT,
        STATUS_RECEIVED,
    }

    # Statuses that can be edited by pilot service if granted permission "edit_permit_request"
    EDITABLE_STATUSES = {
        STATUS_DRAFT,
        STATUS_AWAITING_SUPPLEMENT,
        STATUS_SUBMITTED_FOR_VALIDATION,
        STATUS_PROCESSING,
        STATUS_RECEIVED,
    }

    PROLONGABLE_STATUSES = {
        STATUS_APPROVED,
        STATUS_PROCESSING,
        STATUS_AWAITING_SUPPLEMENT,
    }

    PROLONGATION_STATUS_PENDING = 0
    PROLONGATION_STATUS_APPROVED = 1
    PROLONGATION_STATUS_REJECTED = 2
    PROLONGATION_STATUS_CHOICES = (
        (PROLONGATION_STATUS_PENDING, _("En attente")),
        (PROLONGATION_STATUS_APPROVED, _("Approuvée")),
        (PROLONGATION_STATUS_REJECTED, _("Refusée")),
    )

    status = models.PositiveSmallIntegerField(
        _("état"), choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    shortname = models.CharField(
        _("nom court de la demande, de l'événement, etc."),
        max_length=32,
        help_text=_(
            "Sera affiché dans le calendrier si la demande est rendue tout publique, ex: Brandons (max. 32 caractères)"
        ),
        blank=True,
    )
    created_at = models.DateTimeField(_("date de création"), default=timezone.now)
    validated_at = models.DateTimeField(_("date de validation"), null=True)
    works_object_types = models.ManyToManyField(
        "WorksObjectType",
        through=WorksObjectTypeChoice,
        related_name="permit_requests",
        verbose_name=_("Objets et types de demandes"),
    )
    administrative_entity = models.ForeignKey(
        PermitAdministrativeEntity,
        on_delete=models.CASCADE,
        verbose_name=_("commune"),
        related_name="permit_requests",
    )
    author = models.ForeignKey(
        "PermitAuthor",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("auteur"),
        related_name="permit_requests",
    )
    actors = models.ManyToManyField(
        "PermitActor", related_name="+", through=PermitRequestActor
    )
    intersected_geometries = models.TextField(
        _("Entités géométriques concernées"), max_length=1024, null=True
    )
    validation_pdf = fields.PermitRequestFileField(
        _("pdf de validation"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        upload_to="validations",
    )
    creditor_type = models.PositiveSmallIntegerField(
        _("Destinataire de la facture"),
        choices=ACTOR_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    is_public = models.BooleanField(_("Publier"), default=False)
    prolongation_date = models.DateTimeField(
        _("Nouvelle date de fin"), null=True, blank=True
    )
    prolongation_comment = models.TextField(_("Commentaire"), blank=True)
    prolongation_status = models.PositiveSmallIntegerField(
        _("Décision"), choices=PROLONGATION_STATUS_CHOICES, null=True, blank=True,
    )
    additional_decision_information = models.TextField(
        _("Information complémentaire"),
        max_length=2048,
        blank=True,
        help_text=_("Facultative, sera transmise au requérant"),
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("3.1 Consultation de la demande")
        verbose_name_plural = _("3.1 Consultation des demandes")
        permissions = [
            ("amend_permit_request", _("Traiter les demandes de permis")),
            ("validate_permit_request", _("Valider les demandes de permis")),
            ("classify_permit_request", _("Classer les demandes de permis")),
            ("edit_permit_request", _("Éditer les demandes de permis")),
        ]
        indexes = [models.Index(fields=["created_at"])]

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

    def get_amend_property_list_always_amendable(self):
        amend_properties = []
        qs = PermitRequestAmendProperty.objects.filter(
            Q(
                works_object_types__administrative_entities__name=self.administrative_entity
            )
            & Q(can_always_update=True)
        ).distinct()
        for object in qs:
            amend_properties.append(object.name)
        return amend_properties

    def can_be_sent_for_validation(self):
        """
        This check Enables/disables the send for validation form after the permit status
        changes to STATUS_PROCESSING, which means all the validators made a decision.
        """
        statuses = self.AMENDABLE_STATUSES.copy()
        return self.status in statuses

    def can_be_edited_by_pilot(self):
        return self.status in self.EDITABLE_STATUSES

    def can_be_validated(self):
        return self.status in {self.STATUS_AWAITING_VALIDATION, self.STATUS_PROCESSING}

    def works_objects_list(self):
        return [
            f"{item.works_object.name} ({item.works_type.name})"
            for item in self.works_object_types.all()
        ]

    def works_objects_html(self):
        """
        Return the works objects as a string, separated by <br> characters.
        """
        return format_html(
            "<br>".join([escape(wo) for wo in self.works_objects_list()])
        )

    def works_objects_str(self):
        return " / ".join(self.works_objects_list())

    def get_pending_validations(self):
        return self.validations.filter(
            validation_status=PermitRequestValidation.STATUS_REQUESTED
        )

    def has_validations(self):
        return True if self.validations.all().count() > 0 else False

    def get_min_starts_at(self):
        """
        Calculate the minimum `start_at` datetime of an event, using the current date
        + the biggest `start_delay` (in days, integer pos/neg/zero) from the existing
        works_object_types. If no works_object_types exists or none of them has a
        `start_delay`, use the current date + the default setting.
        """
        today = timezone.make_aware(datetime.today())
        max_delay = None
        if self.works_object_types.exists():
            max_delay = self.works_object_types.aggregate(Max("start_delay"))[
                "start_delay__max"
            ]

        return (
            today + timedelta(days=max_delay)
            if max_delay is not None
            else today + timedelta(days=int(settings.MIN_START_DELAY))
        )

    @cached_property
    def max_validity(self):
        """
        Calculate the maximum end date interval based on the SMALLEST permit_duration.
        Return this interval (number of days), intended to pass as a custom option
        to the widget, so the value can be used by Javascript.
        """
        return self.works_object_types.aggregate(Min("permit_duration"))[
            "permit_duration__min"
        ]

    def get_max_ends_at(self):
        return self.geo_time.aggregate(Max("ends_at"))["ends_at__max"]

    def can_be_prolonged(self):
        return (
            self.status in self.PROLONGABLE_STATUSES and self.max_validity is not None
        )

    def is_prolonged(self):
        return (
            self.prolongation_status == self.PROLONGATION_STATUS_APPROVED
            and self.prolongation_date
        )

    def has_expiration_reminder(self):
        return self.works_object_types.filter(expiration_reminder=True).exists()

    def can_prolongation_be_requested(self):
        if self.can_be_prolonged():
            today = date.today()
            # Early opt-outs:
            # None of the WOTs of the permit have a required date nor are renewables
            if self.get_max_ends_at() is None:
                return False

            if self.prolongation_status in [
                self.PROLONGATION_STATUS_REJECTED,
                self.PROLONGATION_STATUS_PENDING,
            ]:
                return False

            # Check the reminder options
            reminder = self.has_expiration_reminder()

            if reminder:
                # Here, if the reminder is active, we must have
                # the days_before_reminder value (validation on the admin)
                days_before_reminder = self.works_object_types.aggregate(
                    Max("days_before_reminder")
                )["days_before_reminder__max"]

                if self.is_prolonged():
                    return today > (
                        self.prolongation_date.date()
                        - timedelta(days=days_before_reminder)
                    )
                else:
                    return today > (
                        self.get_max_ends_at().date()
                        - timedelta(days=days_before_reminder)
                    )
            else:
                if self.is_prolonged():
                    return today > (self.prolongation_date.date())
                else:
                    return today > (self.get_max_ends_at().date())

        else:
            # It definitively can not be prolonged
            return False

    def set_dates_for_renewables_wots(self):
        """
        Calculate and set starts_at and ends_at for the WOTs that have no date
        required, but can be prolonged, so they have a value in their
        permit_duration field
        """

        works_object_types = self.works_object_types.filter(needs_date=False).filter(
            permit_duration__gte=1
        )
        if works_object_types.exists():
            # Determine starts_at_min and ends_at_max to check if the WOTs are combined
            # between one(s) that needs_date and already set the time interval and those
            # that do not needs_date.
            # If that's the case, the end_date must have already been limited upon
            # permit's creation to be AT MOST the minimum of the permit_duration(s).
            # Therefore we do nothing, otherwise we set both dates.
            # What a good sweat!!!

            if not self.geo_time.exists():
                # At this point following the permit request steps, the Geotime object
                # must have been created only if Geometry or Dates are required,
                # if the WOT does not need require either, we need to create the object.
                PermitRequestGeoTime.objects.create(permit_request_id=self.pk)

            starts_at_min = self.geo_time.aggregate(Min("starts_at"))["starts_at__min"]
            ends_at_max = self.geo_time.aggregate(Max("ends_at"))["ends_at__max"]
            permit_duration_max = self.max_validity
            if starts_at_min is None and ends_at_max is None:
                today = timezone.make_aware(datetime.today())
                self.geo_time.update(starts_at=today)
                self.geo_time.update(
                    ends_at=today + timedelta(days=permit_duration_max)
                )

    @staticmethod
    def get_absolute_url(relative_url):
        protocol = "https" if settings.SITE_HTTPS else "http"
        port = (
            f":{settings.DJANGO_DOCKER_PORT}"
            if settings.SITE_DOMAIN == "localhost"
            else ""
        )
        return f"{protocol}://{settings.SITE_DOMAIN}{port}{relative_url}"


class WorksTypeQuerySet(models.QuerySet):
    def filter_by_tags(self, tags):
        return self.filter(tags__name__in=[tag.lower() for tag in tags])


class WorksType(models.Model):
    name = models.CharField(_("nom"), max_length=255)

    META_TYPE_OTHER = 0
    META_TYPE_ROADWORK = 1
    META_TYPE_BUILDINGWORK = 2
    META_TYPE_EVENT_SPORT = 3
    META_TYPE_EVENT_CULTURE = 4
    META_TYPE_EVENT_COMMERCIAL = 5
    META_TYPE_EVENT_POLICE = 6
    META_TYPE_CHOICES = (
        (META_TYPE_OTHER, _("Autres")),
        (META_TYPE_ROADWORK, _("Chantier")),
        (META_TYPE_BUILDINGWORK, _("Construction")),
        (META_TYPE_EVENT_SPORT, _("Événement sportif")),
        (META_TYPE_EVENT_CULTURE, _("Événement culturel")),
        (META_TYPE_EVENT_COMMERCIAL, _("Événement commercial")),
        (META_TYPE_EVENT_POLICE, _("Dispositif de police")),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )
    meta_type = models.IntegerField(
        _("Type générique"), choices=META_TYPE_CHOICES, default=META_TYPE_OTHER
    )
    tags = TaggableManager(
        blank=True,
        verbose_name="Mots-clés",
        help_text="Mots clefs sans espaces, séparés par des virgules permettant de filtrer les types par l'url: https://geocity.ch/?typefilter=stationnement",
    )
    objects = WorksTypeQuerySet.as_manager()

    class Meta:
        verbose_name = _("1.2 Configuration du type")
        verbose_name_plural = _("1.2 Configuration des types")

    def __str__(self):
        return self.name


class AnonymousWorksObjectTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_anonymous=True)


class WorksObjectType(models.Model):
    """
    Represents a works object for a specific works type.
    """

    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    works_type = models.ForeignKey(
        "WorksType",
        on_delete=models.CASCADE,
        verbose_name=_("type"),
        related_name="works_object_types",
    )
    works_object = models.ForeignKey(
        "WorksObject",
        on_delete=models.CASCADE,
        verbose_name=_("objet"),
        related_name="works_object_types",
    )
    administrative_entities = models.ManyToManyField(
        PermitAdministrativeEntity,
        verbose_name=_("entités administratives"),
        related_name="works_object_types",
    )
    has_geometry_point = models.BooleanField(_("Point"), default=True)
    has_geometry_line = models.BooleanField(_("Ligne"), default=True)
    has_geometry_polygon = models.BooleanField(_("Surface"), default=True)
    directive = fields.AdministrativeEntityFileField(
        _("directive"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
    )
    directive_description = models.CharField(
        _("description de la directive"), max_length=200, blank=True
    )
    additional_information = models.TextField(_("autre information"), blank=True)
    needs_date = models.BooleanField(_("avec période de temps"), default=True)
    start_delay = models.IntegerField(
        _("délai de commencement"),
        blank=True,
        null=True,
        help_text=_(
            "Délai minimum en jours avant la date de début "
            "(nombre entier positif ou négatif)."
        ),
    )
    requires_payment = models.BooleanField(
        _("Demande soumise à des frais"), default=True
    )
    requires_validation_document = models.BooleanField(
        _("Document de validation obligatoire"), default=True
    )
    is_public = models.BooleanField(_("Public"), default=False)
    is_anonymous = models.BooleanField(
        _("Demandes anonymes uniquement"), default=False,
    )
    notify_services = models.BooleanField(_("Notifier les services"), default=False)
    services_to_notify = models.TextField(
        _("Emails des services à notifier"),
        blank=True,
        help_text='Veuillez séparer les emails par une virgule ","',
    )
    permit_duration = models.IntegerField(
        _("Durée de validité de la demande (jours)"),
        blank=True,
        null=True,
        help_text=_(
            "Le permis pour l'objet sera prolongeable uniquement si cette valeur est fournie."
        ),
    )
    expiration_reminder = models.BooleanField(
        _("Activer la fonction de rappel"), default=False,
    )
    days_before_reminder = models.IntegerField(
        _("Délai de rappel (jours)"), blank=True, null=True
    )

    # All objects
    objects = models.Manager()

    # Only anonymous objects
    anonymous_objects = AnonymousWorksObjectTypeManager()

    class Meta:
        verbose_name = _("1.4 Configuration type-objet-entité administrative")
        verbose_name_plural = _("1.4 Configurations type-objet-entité administrative")
        unique_together = [("works_type", "works_object")]

    def __str__(self):
        return "{}: {}".format(self.works_type.name, self.works_object.name)

    @property
    def has_geometry(self):
        return (
            self.has_geometry_point
            or self.has_geometry_line
            or self.has_geometry_polygon
        )

    def clean(self):
        if bool(self.directive_description) ^ bool(self.directive):
            raise ValidationError(
                {
                    "directive_description": _(
                        "La description de directive ne devrait pas être définie car cet objet n’a pas de directive associée."
                    )
                    if not self.directive
                    else _("Ce champ est obligatoire lorsqu’une directive est définie.")
                }
            )


class WorksObject(models.Model):
    name = models.CharField(_("nom"), max_length=255)
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )
    works_types = models.ManyToManyField(
        WorksType,
        through=WorksObjectType,
        related_name="works_objects",
        verbose_name=_("types"),
    )
    order = models.PositiveIntegerField(
        _("ordre"), default=0, blank=False, null=False, db_index=True
    )
    wms_layers = models.URLField(_("Couche(s) WMS"), blank=True, max_length=1024)
    wms_layers_order = models.PositiveIntegerField(
        _("Ordre de(s) couche(s)"), default=1
    )

    class Meta:
        ordering = ["order"]
        verbose_name = _("1.3 Configuration de l'objet")
        verbose_name_plural = _("1.3 Configuration des objets")

    def __str__(self):
        return self.name


class WorksObjectProperty(models.Model):
    INPUT_TYPE_TEXT = INPUT_TYPE_TEXT
    INPUT_TYPE_CHECKBOX = INPUT_TYPE_CHECKBOX
    INPUT_TYPE_NUMBER = INPUT_TYPE_NUMBER
    INPUT_TYPE_FILE = INPUT_TYPE_FILE
    INPUT_TYPE_FILE_DOWNLOAD = INPUT_TYPE_FILE_DOWNLOAD
    INPUT_TYPE_ADDRESS = INPUT_TYPE_ADDRESS
    INPUT_TYPE_DATE = INPUT_TYPE_DATE
    INPUT_TYPE_REGEX = INPUT_TYPE_REGEX
    INPUT_TYPE_LIST_SINGLE = INPUT_TYPE_LIST_SINGLE
    INPUT_TYPE_LIST_MULTIPLE = INPUT_TYPE_LIST_MULTIPLE
    INPUT_TYPE_TITLE = INPUT_TYPE_TITLE
    # The choices are sorted according to their values
    INPUT_TYPE_CHOICES = (
        (INPUT_TYPE_ADDRESS, _("Adresse")),
        (INPUT_TYPE_CHECKBOX, _("Case à cocher")),
        (INPUT_TYPE_LIST_MULTIPLE, _("Choix multiple")),
        (INPUT_TYPE_LIST_SINGLE, _("Choix simple")),
        (INPUT_TYPE_DATE, _("Date")),
        (INPUT_TYPE_FILE, _("Fichier")),
        (INPUT_TYPE_FILE_DOWNLOAD, _("Fichier (à télécharger)")),
        (INPUT_TYPE_NUMBER, _("Nombre")),
        (INPUT_TYPE_TEXT, _("Texte")),
        (INPUT_TYPE_REGEX, _("Texte (regex)")),
        (INPUT_TYPE_TITLE, _("Titre")),
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )
    name = models.CharField(_("nom"), max_length=255)
    placeholder = models.CharField(
        _("exemple de donnée à saisir"), max_length=255, blank=True
    )
    help_text = models.CharField(
        _("information complémentaire"), max_length=255, blank=True
    )
    input_type = models.CharField(
        _("type de caractéristique"), max_length=30, choices=INPUT_TYPE_CHOICES
    )
    order = models.PositiveIntegerField(
        _("ordre"), default=0, blank=False, null=False, db_index=True
    )
    line_number_for_textarea = models.PositiveIntegerField(
        _("Nombre de lignes de la zone de texte"),
        blank=True,
        default=1,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
    )
    is_mandatory = models.BooleanField(_("obligatoire"), default=False)
    works_object_types = models.ManyToManyField(
        WorksObjectType, verbose_name=_("objets"), related_name="properties"
    )
    choices = models.TextField(
        verbose_name=_("valeurs à choix"),
        blank=True,
        help_text=_("Entrez un choix par ligne"),
    )
    regex_pattern = models.CharField(
        _("regex pattern"),
        max_length=255,
        blank=True,
        help_text=_("Exemple: ^[0-9]{4}$"),
    )
    services_to_notify = models.TextField(
        _("Emails des services à notifier"),
        blank=True,
        help_text='Veuillez séparer les emails par une virgule ","',
    )
    file_download = fields.WorkObjectTypeFileField(
        _("Fichier"),
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        blank=True,
        upload_to="wot_files",
    )

    class Meta(object):
        ordering = ["order"]
        verbose_name = _("1.5 Configuration du champ")
        verbose_name_plural = _("1.5 Configuration des champs")
        constraints = [
            models.CheckConstraint(
                check=~(
                    Q(input_type__in=[INPUT_TYPE_LIST_SINGLE, INPUT_TYPE_LIST_MULTIPLE])
                    & Q(choices="")
                ),
                name="choices_not_empty_for_lists",
            ),
            models.CheckConstraint(
                check=~(Q(input_type=INPUT_TYPE_REGEX) & Q(regex_pattern="")),
                name="pattern_not_empty_for_regex",
            ),
        ]
        indexes = [models.Index(fields=["input_type"])]

    def __str__(self):
        return self.name

    def is_value_property(self):
        return self.input_type in [
            WorksObjectProperty.INPUT_TYPE_TEXT,
            WorksObjectProperty.INPUT_TYPE_CHECKBOX,
            WorksObjectProperty.INPUT_TYPE_NUMBER,
            WorksObjectProperty.INPUT_TYPE_FILE,
            WorksObjectProperty.INPUT_TYPE_ADDRESS,
            WorksObjectProperty.INPUT_TYPE_DATE,
            WorksObjectProperty.INPUT_TYPE_LIST_SINGLE,
            WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE,
            WorksObjectProperty.INPUT_TYPE_REGEX,
        ]

    def clean(self):
        if self.input_type in [INPUT_TYPE_LIST_SINGLE, INPUT_TYPE_LIST_MULTIPLE]:
            if not self.choices:
                raise ValidationError({"choices": _("This field is required.")})
            else:
                split_choices = [
                    choice.strip() for choice in self.choices.strip().splitlines()
                ]
                counter = collections.Counter(split_choices)
                duplicates = [choice for choice, count in counter.items() if count > 1]

                if duplicates:
                    raise ValidationError(
                        {
                            "choices": _(
                                "Les valeurs suivantes apparaissent plusieurs fois dans la liste : {} "
                            ).format(", ".join(duplicates))
                        }
                    )

                self.choices = "\n".join(split_choices)
        else:
            self.choices = ""

        if self.input_type == INPUT_TYPE_REGEX:
            if not self.regex_pattern:
                raise ValidationError({"regex_pattern": _("This field is required.")})


class WorksObjectPropertyValue(models.Model):
    """
    Value of a property for a selected object in a permit request.
    """

    property = models.ForeignKey(
        WorksObjectProperty,
        verbose_name=_("caractéristique"),
        on_delete=models.PROTECT,
        related_name="+",
    )
    works_object_type_choice = models.ForeignKey(
        WorksObjectTypeChoice,
        verbose_name=_("objet"),
        on_delete=models.CASCADE,
        related_name="properties",
    )
    # Storing the value in a JSON field allows to keep the value type
    # (eg. boolean, int) instead of transforming everything to str
    value = JSONField()
    history = HistoricalRecords()

    class Meta:
        unique_together = [("property", "works_object_type_choice")]


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
        PermitRequest, on_delete=models.CASCADE, related_name="validations"
    )
    department = models.ForeignKey(
        "PermitDepartment",
        on_delete=models.CASCADE,
        related_name="permit_request_validations",
    )
    validation_status = models.IntegerField(
        _("Statut de validation"), choices=STATUS_CHOICES, default=STATUS_REQUESTED
    )
    comment_before = models.TextField(
        _("Commentaire (avant)"),
        blank=True,
        help_text=_("Information supplémentaire facultative transmise au requérant"),
    )
    comment_during = models.TextField(
        _("Commentaire (pendant)"),
        blank=True,
        help_text=_("Information supplémentaire facultative transmise au requérant"),
    )
    comment_after = models.TextField(
        _("Commentaire (après)"),
        blank=True,
        help_text=_("Information supplémentaire facultative transmise au requérant"),
    )
    validated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    validated_at = models.DateTimeField(_("Validé le"), null=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("permit_request", "department")
        verbose_name = _("3.5 Consultation de la validation par le service")
        verbose_name_plural = _("3.5 Consultation des validations par les services")

    def is_pending(self):
        return self.validation_status == self.STATUS_REQUESTED


class PermitRequestGeoTime(models.Model):
    """
    Permit location in space and time
    """

    permit_request = models.ForeignKey(
        "PermitRequest", on_delete=models.CASCADE, related_name="geo_time"
    )
    starts_at = models.DateTimeField(
        _("Date planifiée de début"), blank=True, null=True
    )
    ends_at = models.DateTimeField(_("Date planifiée de fin"), blank=True, null=True)
    comment = models.CharField(_("Commentaire"), max_length=1024, blank=True)
    external_link = models.URLField(_("Lien externe"), blank=True)
    geom = geomodels.GeometryCollectionField(_("Localisation"), null=True, srid=2056)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("3.3 Consultation de l'agenda et de la géométrie")
        verbose_name_plural = _("3.3 Consultation des agenda et géométries")
        indexes = [
            models.Index(fields=["starts_at"]),
            models.Index(fields=["ends_at"]),
        ]


class GeomLayer(models.Model):
    """
    Geometric entities that might be touched by the PermitRequest
    """

    layer_name = models.CharField(
        _("Nom de la couche source"), max_length=128, blank=True
    )
    description = models.CharField(_("Commentaire"), max_length=1024, blank=True)
    source_id = models.CharField(_("Id entité"), max_length=128, blank=True)
    source_subid = models.CharField(
        _("Id entité secondaire"), max_length=128, blank=True
    )
    external_link = models.URLField(_("Lien externe"), blank=True)
    geom = geomodels.MultiPolygonField(_("Géométrie"), null=True, srid=2056)

    class Meta:
        verbose_name = _("3.4 Consultation de l'entité géographique à intersecter")
        verbose_name_plural = _(
            "3.4 Consultation des entités géographiques à intersecter"
        )


class PermitWorkflowStatus(models.Model):
    """
    Represents a status in the administrative workflow
    """

    status = models.PositiveSmallIntegerField(
        _("statut"), choices=PermitRequest.STATUS_CHOICES,
    )
    administrative_entity = models.ForeignKey(
        "PermitAdministrativeEntity",
        on_delete=models.CASCADE,
        related_name="enabled_statuses",
    )

    def __str__(self):
        return str(self.get_status_display())

    class Meta:
        verbose_name = _("Status disponible pour l'entité administrative")
        verbose_name_plural = _("Status disponibles pour l'entité administratives")
        unique_together = ("status", "administrative_entity")


class PermitRequestAmendProperty(models.Model):
    name = models.CharField(_("nom"), max_length=255)
    is_mandatory = models.BooleanField(_("obligatoire"), default=False)
    is_visible_by_author = models.BooleanField(
        _("Visible par l'auteur de la demande"), default=True
    )
    can_always_update = models.BooleanField(
        _("Editable même après classement de la demande"), default=False
    )
    works_object_types = models.ManyToManyField(
        WorksObjectType, verbose_name=_("objets"), related_name="amend_properties",
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    class Meta:
        verbose_name = _("2.2 Configuration de champ de traitement de demande")
        verbose_name_plural = _(
            "2.2 Configuration des champs de traitement des demandes"
        )

    def __str__(self):
        return self.name


class PermitRequestAmendPropertyValue(models.Model):
    """
    Value of a property for a selected object to be amended by the Secretariat.
    """

    property = models.ForeignKey(
        PermitRequestAmendProperty,
        verbose_name=_("caractéristique"),
        on_delete=models.PROTECT,
        related_name="+",
    )
    works_object_type_choice = models.ForeignKey(
        WorksObjectTypeChoice,
        verbose_name=_("objet"),
        on_delete=models.CASCADE,
        related_name="amend_properties",
    )
    value = models.TextField(_("traitement info"), blank=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = [("property", "works_object_type_choice")]


class QgisProject(models.Model):
    qgis_project_file = fields.AdministrativeEntityFileField(
        _("Projet QGIS '*.qgs'"),
        validators=[FileExtensionValidator(allowed_extensions=["qgs"])],
        upload_to="qgis_templates",
    )
    qgis_print_template_name = models.CharField(
        _("Nom du template d'impression QGIS"), max_length=150,
    )
    description = models.CharField(max_length=150)
    works_object_type = models.ForeignKey(WorksObjectType, on_delete=models.CASCADE)


class QgisGeneratedDocument(models.Model):
    permit_request = models.ForeignKey(
        "PermitRequest", on_delete=models.CASCADE, related_name="qgis_permit"
    )
    qgis_project = models.ForeignKey(
        "QgisProject", on_delete=models.CASCADE, related_name="qgis_project"
    )
    printed_at = models.DateTimeField(_("date d'impression"), null=True)
    printed_by = models.CharField(_("imprimé par"), max_length=255, blank=True)
    printed_file = fields.AdministrativeEntityFileField(
        _("Permis imprimé"),
        null=True,
        blank=True,
        upload_to=printed_permit_request_storage,
    )


class TemplateCustomization(models.Model):

    templatename = models.CharField(
        _("Identifiant"),
        max_length=64,
        blank=True,
        help_text="Permettant d'afficher la page de login par l'url: https://geocity.ch/?template=vevey",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]*$",
                message="Seuls les caractères sans accents et les chiffres sont autorisés. Les espaces et autres caractères spéciaux ne sont pas autorisés",
            )
        ],
    )
    application_title = models.CharField(_("Titre"), max_length=255, blank=True)
    application_subtitle = models.CharField(_("Sous-titre"), max_length=255, blank=True)
    application_description = models.TextField(
        _("Description"), max_length=2048, blank=True
    )
    background_image = models.ImageField(
        _("Image de fond"),
        blank=True,
        upload_to="background_images/",
        validators=[
            FileExtensionValidator(allowed_extensions=["svg", "png", "jpg", "jpeg"])
        ],
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["templatename"], name="unique_templatename")
        ]
        verbose_name = _("4.1 Configuration de la page de login")
        verbose_name_plural = _("4.1 Configuration des pages de login")

    def __str__(self):
        return self.templatename
