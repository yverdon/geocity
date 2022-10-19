import tempfile
import zipfile
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.gis.db import models as geomodels
from django.core.exceptions import SuspiciousOperation
from django.core.validators import (
    FileExtensionValidator,
)
from django.db import models
from django.db.models import (
    JSONField,
    Max,
    Min,
    ProtectedError,
    Q,
)
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from django_tables2.export import TableExport
from simple_history.models import HistoricalRecords

from geocity.apps.accounts.models import AdministrativeEntity, PermitDepartment
from geocity.apps.forms.models import (
    Field,
    Form,
    FormCategory,
)

from . import fields


# Contact types
CONTACT_TYPE_OTHER = 0
CONTACT_TYPE_REQUESTOR = 1
CONTACT_TYPE_OWNER = 2
CONTACT_TYPE_COMPANY = 3
CONTACT_TYPE_CLIENT = 4
CONTACT_TYPE_SECURITY = 5
CONTACT_TYPE_ASSOCIATION = 6
CONTACT_TYPE_ENGINEER = 7
CONTACT_TYPE_WORKDIRECTOR = 8
CONTACT_TYPE_CHOICES = (
    (CONTACT_TYPE_ENGINEER, _("Architecte/Ingénieur")),
    (CONTACT_TYPE_ASSOCIATION, _("Association")),
    (CONTACT_TYPE_OTHER, _("Autres")),
    (CONTACT_TYPE_WORKDIRECTOR, _("Direction des travaux")),
    (CONTACT_TYPE_COMPANY, _("Entreprise")),
    (CONTACT_TYPE_CLIENT, _("Maître d'ouvrage")),
    (CONTACT_TYPE_OWNER, _("Propriétaire")),
    (CONTACT_TYPE_REQUESTOR, _("Requérant (si différent de l'auteur de la demande)")),
    (CONTACT_TYPE_SECURITY, _("Sécurité")),
)


def printed_permit_request_storage(instance, filename):
    return f"permit_requests_uploads/{instance.permit_request.pk}/{filename}"


class Submission(models.Model):
    STATUS_DRAFT = 0
    STATUS_SUBMITTED_FOR_VALIDATION = 1
    STATUS_APPROVED = 2
    STATUS_PROCESSING = 3
    STATUS_AWAITING_SUPPLEMENT = 4
    STATUS_AWAITING_VALIDATION = 5
    STATUS_REJECTED = 6
    STATUS_RECEIVED = 7
    STATUS_INQUIRY_IN_PROGRESS = 8
    STATUS_ARCHIVED = 9

    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Brouillon")),
        (STATUS_SUBMITTED_FOR_VALIDATION, _("Envoyée, en attente de traitement")),
        (STATUS_AWAITING_SUPPLEMENT, _("Demande de compléments")),
        (STATUS_PROCESSING, _("En traitement")),
        (STATUS_AWAITING_VALIDATION, _("En validation")),
        (STATUS_APPROVED, _("Approuvée")),
        (STATUS_REJECTED, _("Refusée")),
        (STATUS_RECEIVED, _("Réceptionnée")),
        (STATUS_INQUIRY_IN_PROGRESS, _("Consultation publique en cours")),
        (STATUS_ARCHIVED, _("Archivée")),
    )
    AMENDABLE_STATUSES = {
        STATUS_SUBMITTED_FOR_VALIDATION,
        STATUS_PROCESSING,
        STATUS_AWAITING_SUPPLEMENT,
        STATUS_RECEIVED,
        STATUS_INQUIRY_IN_PROGRESS,
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
        _("nom court"),
        max_length=32,
        help_text=_(
            "Sera affiché dans le calendrier si la demande est rendue tout publique, ex: Brandons (max. 32 caractères)"
        ),
        blank=True,
    )
    created_at = models.DateTimeField(_("date de création"), default=timezone.now)
    validated_at = models.DateTimeField(_("date de validation"), null=True)
    forms = models.ManyToManyField(
        Form,
        through="SelectedForm",
        related_name="submissions",
        verbose_name=_("Formulaires"),
    )
    administrative_entity = models.ForeignKey(
        AdministrativeEntity,
        on_delete=models.CASCADE,
        verbose_name=_("entité administrative"),
        related_name="submissions",
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("auteur"),
        related_name="submissions",
    )
    contacts = models.ManyToManyField(
        "Contact", related_name="+", through="SubmissionContact"
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
        choices=CONTACT_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    is_public = models.BooleanField(_("Publication calendrier"), default=False)
    prolongation_date = models.DateTimeField(
        _("Nouvelle date de fin"), null=True, blank=True
    )
    prolongation_comment = models.TextField(_("Commentaire"), blank=True)
    prolongation_status = models.PositiveSmallIntegerField(
        _("Décision"),
        choices=PROLONGATION_STATUS_CHOICES,
        null=True,
        blank=True,
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

    def can_always_be_updated(self, user):
        can_always_update = self.works_object_types.filter(
            can_always_update=True
        ).exists()
        user_is_integrator_admin = user.groups.filter(
            permitdepartment__is_integrator_admin=True
        ).exists()
        user_is_backoffice = user_is_integrator_admin = user.groups.filter(
            permitdepartment__is_backoffice=True
        ).exists()
        user_is_superuser = user.is_superuser
        return can_always_update and (
            user_is_integrator_admin or user_is_backoffice or user_is_superuser
        )

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

    def start_inquiry(self):
        if self.status == self.STATUS_INQUIRY_IN_PROGRESS:
            return
        self.status = self.STATUS_INQUIRY_IN_PROGRESS
        self.save()

    @property
    def current_inquiry(self):
        today = datetime.today()
        return SubmissionInquiry.objects.filter(
            permit_request=self, start_date__lte=today, end_date__gte=today
        ).first()

    def get_works_type_names_list(self):

        return ", ".join(
            list(
                self.works_object_types.all()
                .values_list("works_type__name", flat=True)
                .distinct()
            )
        )

    def archive(self, archivist):
        # make sure the request wasn't already archived
        if ArchivedPermitRequest.objects.filter(
            permit_request=self,
        ).first():
            raise SuspiciousOperation(_("La demande a déjà été archivée"))

        # make the archive
        with tempfile.SpooledTemporaryFile() as tmp_file:
            with zipfile.ZipFile(tmp_file, "w") as zip_file:
                # include the request data as CSV
                zip_file.writestr("permit_request.csv", self.to_csv())
                # include additional documents
                for document in self.complementary_documents:
                    zip_file.write(document.path, document.name)

            # Reset file pointer
            tmp_file.seek(0)
            archived_request = ArchivedPermitRequest(
                permit_request=self,
                archivist=archivist,
            )
            archived_request.archive.save("archive.zip", tmp_file)
            archived_request.save()

        self.status = self.STATUS_ARCHIVED
        self.save()

    @property
    def is_archived(self):
        return self.status == self.STATUS_ARCHIVED

    @property
    def complementary_documents(self):
        return SubmissionComplementaryDocument.objects.filter(permit_request=self).all()

    def to_csv(self):
        from .tables import OwnPermitRequestsExportTable

        table = OwnPermitRequestsExportTable(
            data=PermitRequest.objects.filter(id=self.id)
        )

        exporter = TableExport(export_format=TableExport.CSV, table=table)

        return exporter.export()

    def __str__(self):
        return self.shortname


class Contact(models.Model):
    first_name = models.CharField(
        _("Prénom"),
        max_length=150,
    )
    last_name = models.CharField(
        _("Nom"),
        max_length=100,
    )
    company_name = models.CharField(_("Entreprise"), max_length=100, blank=True)
    vat_number = models.CharField(_("Numéro TVA"), max_length=19, blank=True)
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
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Contact")

    def __str__(self):
        return self.first_name + " " + self.last_name


class SelectedForm(models.Model):
    """
    This intermediary model represents the selected objects for a permit
    request. Property values will then point to this model.
    """

    submission = models.ForeignKey("Submission", on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        unique_together = [("submission", "form")]


class ContactType(models.Model):

    type = models.PositiveSmallIntegerField(
        _("type de contact"), choices=CONTACT_TYPE_CHOICES, default=CONTACT_TYPE_OTHER
    )
    form_category = models.ForeignKey(
        FormCategory,
        on_delete=models.CASCADE,
        verbose_name=_("type de demande"),
        related_name="contact_types",
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
        unique_together = [["type", "form_category"]]

    def __str__(self):
        return self.get_type_display() + " (" + str(self.form_category) + ")"


class SubmissionContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    submission = models.ForeignKey("Submission", on_delete=models.CASCADE)
    contact_type = models.PositiveSmallIntegerField(
        _("type de contact"), choices=CONTACT_TYPE_CHOICES, default=CONTACT_TYPE_OTHER
    )

    class Meta:
        verbose_name = _("Relation demande-contact")
        verbose_name_plural = _("Relations demande-contact")

    def __str__(self):
        return "{} - {}".format(str(self.contact), str(self.get_contact_type_display()))


class FieldValue(models.Model):
    """
    Value of a property for a selected object in a permit request.
    """

    field = models.ForeignKey(
        Field,
        verbose_name=_("caractéristique"),
        on_delete=models.PROTECT,
        related_name="+",
    )
    selected_form = models.ForeignKey(
        SelectedForm,
        verbose_name=_("objet"),
        on_delete=models.CASCADE,
        related_name="field_values",
    )
    # Storing the value in a JSON field allows to keep the value type
    # (eg. boolean, int) instead of transforming everything to str
    value = JSONField()
    history = HistoricalRecords()

    class Meta:
        unique_together = [("field", "selected_form")]


class SubmissionGeoTime(models.Model):
    """
    Permit location in space and time
    """

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="geo_time"
    )
    starts_at = models.DateTimeField(
        _("Date planifiée de début"), blank=True, null=True
    )
    ends_at = models.DateTimeField(_("Date planifiée de fin"), blank=True, null=True)
    comment = models.CharField(_("Commentaire"), max_length=1024, blank=True)
    external_link = models.URLField(_("Lien externe"), blank=True)
    comes_from_automatic_geocoding = models.BooleanField(
        _("Géométrie obtenue par géocodage d'adresse"), default=False
    )
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


class SubmissionWorkflowStatus(models.Model):
    """
    Represents a status in the administrative workflow
    """

    status = models.PositiveSmallIntegerField(
        _("statut"),
        choices=Submission.STATUS_CHOICES,
    )
    administrative_entity = models.ForeignKey(
        AdministrativeEntity,
        on_delete=models.CASCADE,
        related_name="enabled_statuses",
    )

    def __str__(self):
        return str(self.get_status_display())

    class Meta:
        verbose_name = _("Status disponible pour l'entité administrative")
        verbose_name_plural = _("Status disponibles pour l'entité administratives")
        unique_together = ("status", "administrative_entity")


class ArchivedSubmission(models.Model):
    archived_date = models.DateTimeField(auto_now_add=True)
    archivist = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Personne ayant archivé la demande"),
    )
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    archive = fields.ArchiveDocumentFileField(_("Archive"))

    @property
    def path(self):
        return self.archive.path

    def delete(self, using=None, keep_parents=False):
        # TODO: is this really wanted ?!!
        self.submission.delete()
        ret = super().delete(using, keep_parents)
        # delete the archive file
        self.archive.delete(save=False)
        return ret


class SubmissionInquiry(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    documents = models.ManyToManyField(
        "SubmissionComplementaryDocument",
        verbose_name=_("Documents complémentaires"),
        blank=True,
    )
    submission = models.ForeignKey(
        Submission,
        null=False,
        on_delete=models.CASCADE,
        verbose_name=_("Demande"),
    )
    submitter = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Demandeur de l'enquête"),
    )

    class Meta:
        verbose_name = _("3.2 Enquête public")
        verbose_name_plural = _("3.2 Enquêtes publics")

    @classmethod
    def get_current_inquiry(cls, permit_request):
        today = datetime.today().strftime("%Y-%m-%d")
        return cls.objects.filter(
            Q(permit_request=permit_request)
            & Q(start_date__lte=today)
            & Q(end_date__gte=today)
        ).first()


class SubmissionComplementaryDocument(models.Model):
    STATUS_TEMP = 0
    STATUS_FINALE = 1
    STATUS_OTHER = 2
    STATUS_CANCELED = 3

    STATUS_CHOICES = (
        (STATUS_TEMP, _("Provisoire")),
        (STATUS_FINALE, _("Final")),
        (STATUS_OTHER, _("Autre")),
        (STATUS_CANCELED, _("Annulé")),
    )

    document = fields.ComplementaryDocumentFileField(_("Document"))
    description = models.TextField(
        _("Description du document"),
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Propriétaire du document"),
        related_name="complementary_documents",
    )
    submission = models.ForeignKey(
        Submission,
        null=False,
        on_delete=models.CASCADE,
        verbose_name=_("Demande"),
        related_name="complementary_documents",
    )
    status = models.PositiveSmallIntegerField(
        _("Statut du document"),
        choices=STATUS_CHOICES,
    )
    authorised_departments = models.ManyToManyField(
        PermitDepartment,
        verbose_name=_("Département autorisé à visualiser le document"),
        related_name="complementary_documents",
    )
    is_public = models.BooleanField(default=False, verbose_name=_("Public"))
    document_type = models.ForeignKey(
        "ComplementaryDocumentType",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Type du document"),
        related_name="complementary_documents",
    )

    @property
    def uri(self):
        return self.document.url

    @property
    def name(self):
        return self.document.name

    @property
    def path(self):
        return self.document.path

    def delete(self, using=None, keep_parents=False):
        # delete the uploaded file
        try:
            os.remove(self.document.path)
            return super().delete(using, keep_parents)
        except OSError as e:
            raise ProtectedError(
                _("Le document {} n'a pas pu être supprimé".format(self)), e
            )

    def __str__(self):
        return self.document.name


class ComplementaryDocumentType(models.Model):
    name = models.CharField(_("nom"), max_length=255)
    parent = models.ForeignKey(
        "ComplementaryDocumentType",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Type parent"),
        related_name="children",
    )
    form = models.ForeignKey(
        Form,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Formulaires"),
        related_name="document_types",
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
        related_name="document_types",
    )

    # reverse relationship is manually defined on reports.Report so it shows up on both sides in admin
    # Note: theoretically, this should only be allowed on "child" ComplementaryDocumentType, but this will
    # be solved by a future refactoring
    # see https://github.com/yverdon/geocity/issues/526
    reports = models.ManyToManyField(
        "reports.Report",
        blank=True,
        related_name="+",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(Q(parent__isnull=False) & Q(form__isnull=True))
                | (Q(parent__isnull=True) & Q(form__isnull=False)),
                name="complementary_document_type_restrict_form_link_to_parents",
            )
        ]
        verbose_name = _("1.7 Configuration du type de document")
        verbose_name_plural = _("1.7 Configuration des types de document")

    def __str__(self):
        return self.name


class SubmissionAmendField(models.Model):
    name = models.CharField(_("nom"), max_length=255)
    is_mandatory = models.BooleanField(_("obligatoire"), default=False)
    is_visible_by_author = models.BooleanField(
        _("Visible par l'auteur de la demande"), default=True
    )
    is_visible_by_validators = models.BooleanField(
        _("Visible par les validateurs"), default=False
    )
    can_always_update = models.BooleanField(
        _("Editable même après classement de la demande"), default=False
    )
    forms = models.ManyToManyField(
        Form,
        verbose_name=_("formulaires"),
        related_name="amend_fields",
    )
    integrator = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Groupe des administrateurs"),
    )

    class Meta:
        verbose_name = _("2.2 Configuration du champ de traitement des demandes")
        verbose_name_plural = _(
            "2.2 Configuration des champs de traitement des demandes"
        )

    def __str__(self):
        return self.name


class SubmissionAmendFieldValue(models.Model):
    """
    Value of a property for a selected object to be amended by the Secretariat.
    """

    field = models.ForeignKey(
        SubmissionAmendField,
        verbose_name=_("caractéristique"),
        on_delete=models.PROTECT,
        related_name="+",
    )
    form = models.ForeignKey(
        SelectedForm,
        verbose_name=_("formulaire"),
        on_delete=models.CASCADE,
        related_name="amend_fields",
    )
    value = models.TextField(_("traitement info"), blank=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = [("field", "form")]


class SubmissionValidation(models.Model):
    STATUS_REQUESTED = 0
    STATUS_APPROVED = 1
    STATUS_REJECTED = 2
    STATUS_CHOICES = (
        (STATUS_REQUESTED, _("En attente")),
        (STATUS_APPROVED, _("Approuvé")),
        (STATUS_REJECTED, _("Refusé")),
    )

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="validations"
    )
    department = models.ForeignKey(
        PermitDepartment,
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
        unique_together = ("submission", "department")
        verbose_name = _("3.5 Consultation de la validation par le service")
        verbose_name_plural = _("3.5 Consultation des validations par les services")

    def is_pending(self):
        return self.validation_status == self.STATUS_REQUESTED
