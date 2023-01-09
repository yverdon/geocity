import enum
import logging
import os
import tempfile
import urllib.parse
import zipfile
from datetime import date, datetime, timedelta

import PIL
import requests
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import GeometryCollection, MultiPoint, Point
from django.core.exceptions import SuspiciousOperation
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models, transaction
from django.db.models import Count, F, JSONField, Max, Min, ProtectedError, Q, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.functional import cached_property
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _
from django_tables2.export import TableExport
from pdf2image import convert_from_path
from PIL import Image
from simple_history.models import HistoricalRecords

from geocity.apps.accounts.models import AdministrativeEntity, PermitDepartment, User
from geocity.apps.accounts.validators import validate_email
from geocity.apps.forms.models import Field, Form, FormCategory

from . import fields
from .payments.models import SubmissionPrice

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

# Actions
ACTION_AMEND = "amend"
ACTION_REQUEST_VALIDATION = "request_validation"
ACTION_VALIDATE = "validate"
ACTION_POKE = "poke"
ACTION_PROLONG = "prolong"
ACTION_COMPLEMENTARY_DOCUMENTS = "complementary_documents"
ACTION_REQUEST_INQUIRY = "request_inquiry"
ACTION_TRANSACTION = "transactins"
# If you add an action here, make sure you also handle it in `views.get_form_for_action`,  `views.handle_form_submission`
# and services.get_actions_for_administrative_entity
ACTIONS = [
    ACTION_AMEND,
    ACTION_REQUEST_VALIDATION,
    ACTION_VALIDATE,
    ACTION_POKE,
    ACTION_PROLONG,
    ACTION_COMPLEMENTARY_DOCUMENTS,
    ACTION_REQUEST_INQUIRY,
]

logger = logging.getLogger(__name__)


def printed_submission_storage(instance, filename):
    return f"permit_requests_uploads/{instance.submission.pk}/{filename}"


class GeoTimeInfo(enum.Enum):
    DATE = enum.auto()
    GEOMETRY = enum.auto()
    # Geometry automatically genrerate from address field using geoadmin API
    GEOCODED_GEOMETRY = enum.auto()


class SubmissionQuerySet(models.QuerySet):
    def filter_for_user(self, user, form_filter=None, ignore_archived=True):
        """
        Return the list of submissions this user has access to.
        """
        annotate_with = dict(
            starts_at_min=Min("geo_time__starts_at"),
            ends_at_max=Max("geo_time__ends_at"),
            permit_duration_max=Max("forms__permit_duration"),
            remaining_validations=Count("validations")
            - Count(
                "validations",
                filter=~Q(
                    validations__validation_status=SubmissionValidation.STATUS_REQUESTED
                ),
            ),
            required_validations=Count("validations"),
            author_fullname=Concat(
                F("author__first_name"),
                Value(" "),
                F("author__last_name"),
            ),
            author_details=Concat(
                F("author__email"),
                Value(" / "),
                F("author__userprofile__phone_first"),
                output_field=models.CharField(),
            ),
        )

        if form_filter is not None:
            annotate_with.update({"form_filter": Value(form_filter)})

        qs = self.annotate(**annotate_with)

        if ignore_archived:
            qs = qs.filter(~Q(status=Submission.STATUS_ARCHIVED))

        if not user.is_authenticated:
            return qs.none()

        if not user.is_superuser:
            qs_filter = Q(author=user)

            if user.has_perm("submissions.amend_submission"):
                qs_filter |= Q(
                    administrative_entity__in=AdministrativeEntity.objects.associated_to_user(
                        user
                    ),
                ) & ~Q(status=Submission.STATUS_DRAFT)

            if user.has_perm("submissions.validate_submission"):
                qs_filter |= Q(
                    validations__department__in=PermitDepartment.objects.filter(
                        group__in=user.groups.all()
                    )
                )
            return qs.filter(qs_filter)

        return qs


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
    }

    # Statuses that can be edited by pilot service if granted permission "edit_submission"
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

    # Statuses of submission visible in calendar (api => submissions_details)
    VISIBLE_IN_CALENDAR_STATUSES = {
        STATUS_APPROVED,
        STATUS_INQUIRY_IN_PROGRESS,
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
    validation_pdf = fields.SubmissionFileField(
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

    objects = SubmissionQuerySet().as_manager()

    class Meta:
        verbose_name = _("2.2 Consultation de la demande")
        verbose_name_plural = _("2.2 Consultation des demandes")
        permissions = [
            ("amend_submission", _("Traiter les demandes de permis")),
            ("validate_submission", _("Valider les demandes de permis")),
            ("classify_submission", _("Classer les demandes de permis")),
            ("edit_submission", _("Éditer les demandes de permis")),
            ("view_private_submission", _("Voir les demandes restreintes")),
            ("can_refund_transactions", _("Rembourser une transaction")),
            ("can_revert_refund_transactions", _("Revenir sur un remboursement")),
        ]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return self.shortname

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

    def get_amend_field_list_always_amendable(self):
        amend_properties = []
        qs = SubmissionAmendField.objects.filter(
            Q(forms__administrative_entities=self.administrative_entity)
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
            validation_status=SubmissionValidation.STATUS_REQUESTED
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
        if self.forms.exists():
            max_delay = self.forms.aggregate(Max("start_delay"))["start_delay__max"]

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
        return self.forms.aggregate(Min("permit_duration"))["permit_duration__min"]

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
        return self.forms.filter(expiration_reminder=True).exists()

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
                days_before_reminder = self.forms.aggregate(
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

    def set_dates_for_renewable_forms(self):
        """
        Calculate and set starts_at and ends_at for the forms that have no date
        required, but can be prolonged, so they have a value in their
        permit_duration field
        """
        forms = self.forms.filter(needs_date=False).filter(permit_duration__gte=1)

        if forms.exists():
            # Determine starts_at_min and ends_at_max to check if the WOTs are combined
            # between one(s) that needs_date and already set the time interval and those
            # that do not needs_date.
            # If that's the case, the end_date must have already been limited upon
            # permit's creation to be AT MOST the minimum of the permit_duration(s).
            # Therefore we do nothing, otherwise we set both dates.
            # What a good sweat!!!

            if not self.geo_time.exists():
                # At this point following the submission steps, the Geotime object
                # must have been created only if Geometry or Dates are required,
                # if the form does not need require either, we need to create the object.
                SubmissionGeoTime.objects.create(submission_id=self.pk)

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
            submission=self, start_date__lte=today, end_date__gte=today
        ).first()

    def get_forms_names_list(self):
        return ", ".join(
            list(
                self.forms.all()
                .values_list("name", flat=True)
                .distinct("name")
                .order_by("name")
            )
        )

    def archive(self, archivist):
        # make sure the request wasn't already archived
        if ArchivedSubmission.objects.filter(
            submission=self,
        ).first():
            raise SuspiciousOperation(_("La demande a déjà été archivée"))

        # make the archive
        with tempfile.SpooledTemporaryFile() as tmp_file:
            with zipfile.ZipFile(tmp_file, "w") as zip_file:
                # include the request data as CSV
                zip_file.writestr("submission.csv", self.to_csv())
                # include additional documents
                for document in self.complementary_documents.all():
                    zip_file.write(document.path, document.name)

            # Reset file pointer
            tmp_file.seek(0)
            archived_request = ArchivedSubmission(
                submission=self,
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
        return SubmissionComplementaryDocument.objects.filter(submission=self).all()

    def to_csv(self):
        from .tables import OwnSubmissionsExportTable

        table = OwnSubmissionsExportTable(data=Submission.objects.filter(id=self.id))

        exporter = TableExport(export_format=TableExport.CSV, table=table)

        return exporter.export()

    def requires_payment(self):
        return any(form.requires_payment for form in self.forms.all())

    @transaction.atomic
    def set_field_value(self, form, field, value):
        """
        Create or update the `FieldValue` object for the given field, form and
        submission. The record will be deleted if value is an empty string or None.
        `value` can be a variety of types: str in the case of a text field, bool in
        the case of a boolean field, int in the case of a number field, and File
        or bool in the case of a file field (the latter being `False` if the user is
        asking for the file to be removed).
        """
        existing_value_obj = FieldValue.objects.filter(
            selected_form__submission=self,
            selected_form__form=form,
            field=field,
        )
        is_file = field.input_type == Field.INPUT_TYPE_FILE
        is_date = field.input_type == Field.INPUT_TYPE_DATE
        # TODO this doesn’t seem to be used? Remove?
        is_address = field.input_type == Field.INPUT_TYPE_ADDRESS

        if value == "" or value is None:
            existing_value_obj.delete()
        else:
            if is_file:
                # Use private storage to prevent uploaded files exposition to the outside world
                private_storage = fields.PrivateFileSystemStorage()
                # If the given File has a `url` attribute, it means the value comes from the `initial` form data, so the
                # value hasn't changed
                if getattr(value, "url", None):
                    return

                # Remove the previous file, if any
                try:
                    current_value = existing_value_obj.get()
                except FieldValue.DoesNotExist:
                    pass
                else:
                    private_storage.delete(current_value.value["val"])
                # User has asked to remove the file. The file has already been removed from the storage, remove the property
                # value record and we're done
                if value is False:
                    existing_value_obj.delete()
                    return

                # TODO move all the low-level file processing mechanism elsewhere
                # Add the file to the storage
                directory = "permit_requests_uploads/{}".format(self.pk)
                ext = os.path.splitext(value.name)[1]
                upper_ext = ext[1:].upper()
                path = os.path.join(directory, "{}_{}{}".format(form.pk, field.pk, ext))

                private_storage.save(path, value)
                # Postprocess images: remove all exif metadata from for better security and user privacy
                if upper_ext != "PDF":

                    upper_ext = ext[1:].upper()
                    formats_map = {"JPG": "JPEG"}
                    with Image.open(value) as image_full:
                        data = list(image_full.getdata())
                        new_image = Image.new(image_full.mode, image_full.size)
                        new_image.putdata(data)
                        new_image.save(
                            private_storage.location + "/" + path,
                            formats_map[upper_ext]
                            if upper_ext in formats_map.keys()
                            else upper_ext,
                        )
                # Postprocess PDF: convert everything to image, do not keep other content
                elif upper_ext == "PDF":
                    # File size to fix decompression bomb error
                    PIL.Image.MAX_IMAGE_PIXELS = None

                    all_images = convert_from_path(
                        private_storage.location + "/" + path
                    )
                    first_image = all_images[0]
                    following_images = all_images[1:]
                    if len(following_images) > 0:
                        first_image.save(
                            private_storage.location + "/" + path,
                            save_all=True,
                            append_images=following_images,
                        )
                    else:
                        first_image.save(
                            private_storage.location + "/" + path, save_all=True
                        )

                value = path

            elif is_date:
                value = value.isoformat()

            value_dict = {"val": value}
            nb_objs = existing_value_obj.update(value=value_dict)

            # No existing property value record, create it
            if nb_objs == 0:
                (
                    selected_form,
                    created,
                ) = SelectedForm.objects.get_or_create(submission=self, form=form)
                FieldValue.objects.create(
                    selected_form=selected_form,
                    field=field,
                    value=value_dict,
                )

    def get_fields_values(self):
        """
        Return a queryset of `FieldValue` objects for this submission, excluding
        properties of type file.
        """
        return (
            FieldValue.objects.filter(selected_form__submission=self)
            .exclude(field__input_type=Field.INPUT_TYPE_FILE)
            .select_related(
                "selected_form",
                "selected_form__form",
                "field",
            )
        )

    def get_appendices_values(self):
        """
        Return a queryset of `FieldValue` objects of type file for this submission.
        """
        return FieldValue.objects.filter(
            selected_form__submission=self,
            field__input_type=Field.INPUT_TYPE_FILE,
        ).select_related(
            "selected_form__form",
            "field",
        )

    def get_form_categories(self):
        return (
            FormCategory.objects.filter(pk__in=self.forms.values_list("category_id"))
            .order_by("name")
            .distinct()
        )

    def _get_fields_filtered(self, props_filter):
        """
        Return a list of `(Form, QuerySet[Field])` for all forms of this submission.
        `props_filter` is passed the properties queryset and should return it (or a
        filtered version of it).

        TODO move this in forms app?
        """

        fields_by_form = [
            (
                form,
                props_filter(
                    form.fields.filter(form_fields__form=form).order_by(
                        "form_fields__order", "name"
                    )
                ),
            )
            for form in self.forms.order_by("order", "name")
        ]

        return [(form, fields) for form, fields in fields_by_form if fields]

    def get_fields_by_form(self, additional_type_exclusions=None):
        """
        FIXME docstring
        """
        exclusions = [
            Field.INPUT_TYPE_FILE,
        ]
        if additional_type_exclusions is not None:
            exclusions += additional_type_exclusions
        return self._get_fields_filtered(
            lambda qs: qs.exclude(
                input_type__in=[
                    Field.INPUT_TYPE_FILE,
                ]
                + exclusions
            ),
        )

    def get_appendices_fields_by_form(self):
        return self._get_fields_filtered(
            lambda qs: qs.filter(input_type=Field.INPUT_TYPE_FILE),
        )

    @transaction.atomic
    def set_selected_forms(self, new_forms):
        """
        Add the given `new_works_object_types`, which should be an iterable of `WorksObjectType` instances to the given
        `submission`. Existing `WorksObjectType` are ignored.
        """
        # Check which object type are new or have been removed. We can't just remove them all and recreate them
        # because there might be data related to these relations (eg. FieldValue)
        self.get_selected_forms().exclude(form__in=new_forms).delete()

        for form in new_forms:
            SelectedForm.objects.get_or_create(submission=self, form=form)

        geotime_objects = self.get_geotime_objects()

        if len(geotime_objects) > 0:
            geotime_required_info = self.get_geotime_required_info()
            # Reset the geometry/date if the new_works_object_type do not need Date/Geom
            if len(geotime_required_info) == 0:
                geotime_objects.delete()
            # Reset the date only
            if GeoTimeInfo.DATE not in geotime_required_info:
                geotime_objects.update(starts_at=None, ends_at=None)
            # Reset the geometry only
            if GeoTimeInfo.GEOMETRY not in geotime_required_info:
                geotime_objects.update(geom=None)

    def get_contacts_types(self):
        """
        Get contacts types defined for each form defined for the submission.
        """
        return (
            ContactType.objects.filter(form_category__in=self.get_form_categories())
            .values_list("type", "is_mandatory")
            .distinct()
            .order_by("-is_mandatory", "type")
        )

    def get_missing_required_contact_types(self):
        """
        Get contacts types required but not filled
        """

        return self.filter_only_missing_contact_types(
            [
                (actor_type, is_mandatory)
                for actor_type, is_mandatory in self.get_contacts_types()
                if is_mandatory
            ],
        )

    def get_geotime_required_info(self):
        forms = self.forms.all()
        required_info = set()
        if any(form.needs_date for form in forms):
            required_info.add(GeoTimeInfo.DATE)

        if any(form.has_geometry for form in forms):
            required_info.add(GeoTimeInfo.GEOMETRY)
        else:
            exclusions = [
                field[0]
                for field in Field.INPUT_TYPE_CHOICES
                if field[0] != Field.INPUT_TYPE_ADDRESS
            ]

            if (
                self.get_fields_by_form(exclusions)
                and self.get_geotime_objects()
                .filter(comes_from_automatic_geocoding=True)
                .exists()
            ):
                required_info.add(GeoTimeInfo.GEOCODED_GEOMETRY)
        return required_info

    def get_secretary_email(self):
        department = self.administrative_entity.departments.filter(is_backoffice=True)
        secretary_group_users = User.objects.filter(
            Q(
                groups__permit_department__in=department,
                userprofile__notify_per_email=True,
            )
        )

        return [user.email for user in secretary_group_users]

    def get_complementary_documents(self, user):
        qs = self.complementary_documents.all().order_by("pk").distinct()

        if user.is_superuser:
            return qs

        return qs.filter(
            Q(is_public=True)
            | Q(owner=user)
            | Q(authorised_departments__group__in=user.groups.all()),
        )

    def get_amend_custom_fields_by_form(self):
        forms = self.forms.prefetch_related("amend_fields").select_related("category")

        for form in forms:
            yield (form, form.amend_fields.all())

    @transaction.atomic
    def set_amend_custom_field_value(self, form, field, value):
        """
        Create or update the `SubmissionAmendFieldValue` object for the given
        field, form and submission. The record will be deleted if value is
        an empty string or None. Value is only str type.
        TODO: why is there a "custom" in this method name?
        """
        existing_value_obj = SubmissionAmendFieldValue.objects.filter(
            form__submission=self,
            form__form=form,
            field=field,
        )

        if value == "" or value is None:
            existing_value_obj.delete()
        else:
            nb_objs = existing_value_obj.update(value=value)
            # No existing field value record, create it
            if nb_objs == 0:
                (
                    selected_form,
                    created,
                ) = SelectedForm.objects.get_or_create(submission=self, form=form)
                SubmissionAmendFieldValue.objects.create(
                    form=selected_form,
                    field=field,
                    value=value,
                )

    def get_amend_custom_fields_values(self):
        """
        Return a queryset of `SubmissionAmendFieldValue` objects for this submission.
        """
        return SubmissionAmendFieldValue.objects.filter(
            form__submission=self
        ).select_related(
            "form__form",
            "field",
        )

    def get_submission_directives(self):
        return [
            (obj.directive, obj.directive_description, obj.additional_information)
            for obj in self.forms.exclude(
                directive="", directive_description="", additional_information=""
            )
        ]

    @transaction.atomic
    def set_administrative_entity(self, administrative_entity):
        """
        Set the given `administrative_entity`, which should be an instance of `models.PermitAdministrativeEntity`.
        `WorksObjectTypeChoice` records that don't exist in the new `administrative_entity` will be deleted.
        """
        self.selected_forms.exclude(form__in=administrative_entity.forms.all()).delete()

        self.administrative_entity = administrative_entity
        self.save()

    def get_services_to_notify_mailing_list(self):
        mailing_list = []

        forms_to_notify = self.forms.filter(notify_services=True)

        for emails in forms_to_notify.values_list("services_to_notify", flat=True):
            emails_addresses = emails.replace("\n", ",").split(",")
            mailing_list += [
                ea.strip() for ea in emails_addresses if validate_email(ea.strip())
            ]

        return mailing_list

    def has_document_enabled(self):
        return self.forms.filter(document_enabled=True).exists()

    def filter_only_missing_contact_types(self, contact_types):
        """
        Filter the given `contact_types` to return only the ones that have not been set in the given `submission`.
        """

        existing_contact_types = self.contacts.values_list(
            "submissioncontact__contact_type", flat=True
        )

        return [
            contact_type
            for contact_type in contact_types
            if contact_type[0] not in existing_contact_types
        ]

    def get_geotime_objects(self, exlude_geocoded_geom=False):
        return self.geo_time.filter(comes_from_automatic_geocoding=exlude_geocoded_geom)

    def get_actions_for_administrative_entity(self):
        """
        Filter out administrative workflow step that are not coherent
        with current submission status
        """

        # Statuses for which a given action should be available
        required_statuses_for_actions = {
            "amend": list(Submission.AMENDABLE_STATUSES),
            "request_validation": [Submission.STATUS_AWAITING_VALIDATION],
            "poke": [Submission.STATUS_AWAITING_VALIDATION],
            "validate": [
                Submission.STATUS_APPROVED,
                Submission.STATUS_REJECTED,
                Submission.STATUS_AWAITING_VALIDATION,
                Submission.STATUS_PROCESSING,
            ],
            "prolong": list(Submission.PROLONGABLE_STATUSES),
            "complementary_documents": [
                Submission.STATUS_AWAITING_VALIDATION,
                Submission.STATUS_PROCESSING,
            ],
            "request_inquiry": list(Submission.AMENDABLE_STATUSES),
            "transactions": [
                Submission.STATUS_APPROVED,
                Submission.STATUS_REJECTED,
                Submission.STATUS_AWAITING_VALIDATION,
                Submission.STATUS_PROCESSING,
            ],
        }

        available_statuses_for_administrative_entity = (
            SubmissionWorkflowStatus.objects.get_statuses_for_administrative_entity(
                self.administrative_entity
            )
        )
        available_actions = []
        for action in required_statuses_for_actions.keys():
            action_as_set = set(required_statuses_for_actions[action])
            enabled_actions = list(
                action_as_set.intersection(available_statuses_for_administrative_entity)
            )
            if enabled_actions:
                available_actions.append(action)

        distinct_available_actions = list(dict.fromkeys(available_actions))
        return distinct_available_actions

    def is_validation_document_required(self):
        return self.forms.filter(requires_validation_document=True).exists()

    def can_have_multiple_ranges(self):
        return any(form.can_have_multiple_ranges for form in self.forms.all())

    def get_selected_forms(self):
        return SelectedForm.objects.filter(submission=self)

    def reverse_geocode_and_store_address_geometry(self, to_geocode_addresses):
        # Delete the previous geocoded geometries
        SubmissionGeoTime.objects.filter(
            submission=self, comes_from_automatic_geocoding=True
        ).delete()

        if to_geocode_addresses:
            geoadmin_address_search_api = settings.LOCATIONS_SEARCH_API
            geom = GeometryCollection()
            for address in to_geocode_addresses:
                search_params = {
                    "searchText": address,
                    "limit": 1,
                    "partitionlimit": 1,
                    "type": "locations",
                    "sr": "2056",
                    "lang": "fr",
                    "origins": "address",
                }

                data = urllib.parse.urlencode(search_params)
                url = f"{geoadmin_address_search_api}?{data}"
                # GEOADMIN API might be down and we don't want to block the user
                try:
                    response = requests.get(url, timeout=2)
                except requests.exceptions.RequestException:
                    return None

                if response.status_code == 200 and response.json()["results"]:
                    x = response.json()["results"][0]["attrs"]["x"]
                    y = response.json()["results"][0]["attrs"]["y"]
                    geom.append(MultiPoint(Point(y, x, srid=2056)))
                # If geocoding matches nothing, set the address value on the administrative_entity centroid point
                else:
                    geom.append(MultiPoint(self.administrative_entity.geom.centroid))

            # Save the new ones
            SubmissionGeoTime.objects.create(
                submission=self,
                comes_from_automatic_geocoding=True,
                geom=geom,
            )

    def get_form_for_payment(self):
        """
        For online payments, only one form can exist on a Submission
        """
        if self.forms.count() != 1:
            logger.warning(
                f"Multiple forms in the submission ({self.pk}), in an "
                f"entity set to [single form submission]. Payment feature"
                f"not available."
            )
            return None
        return self.forms.first()

    def requires_online_payment(self):
        form_for_payment = self.get_form_for_payment()
        return form_for_payment and form_for_payment.requires_online_payment

    @property
    def submission_price(self):
        return self.get_submission_price()

    def get_submission_price(self):
        try:
            return SubmissionPrice.objects.get(submission=self)
        except SubmissionPrice.DoesNotExist:
            return None

    def get_transactions(self):
        # TODO: if more payment processors are implemented, change this to add all transaction types to queryset
        if self.submission_price is None:
            return None
        return self.submission_price.get_transactions()

    def get_history(self):
        # Transactions history
        if self.submission_price is None:
            transactions = []
        else:
            transactions = self.submission_price.transactions.all()
        transaction_versions = []
        last_status = ""
        for transaction in transactions:
            versions = []
            for version in transaction.history.all():
                # Include only updates that changed the transaction status
                if last_status != version.status:
                    versions.append(version)
                last_status = version.status
            transaction_versions += versions

        # Merge with Submission (self) history
        history = [
            (event.history_date, event)
            for event in (*self.history.all(), *transaction_versions)
        ]
        history.sort(reverse=True)
        return history

    def get_last_transaction(self):
        if self.get_transactions() is None:
            return None
        return self.get_transactions().order_by("-updated_date").last()

    def get_submission_payment_attachments(self, pdf_type):
        pdf_types = {
            "confirmation": lambda p: p.payment_confirmation_report,
            "refund": lambda p: p.payment_refund_report,
        }
        report_func = pdf_types[pdf_type]
        form = self.get_form_for_payment()
        payment_settings = form.payment_settings
        if not payment_settings or not report_func(payment_settings):
            return []
        child_doc_type = None
        for doc_type in report_func(payment_settings).document_types.all():
            if doc_type.parent.form.pk == form.pk:
                child_doc_type = doc_type
                break

        if not child_doc_type:
            return []

        comp_doc = (
            self.get_complementary_documents(self.author)
            .filter(document_type=child_doc_type)
            .last()
        )
        if not comp_doc:
            return []
        return [(comp_doc.name, comp_doc.document.file.read())]

    def generate_and_save_pdf(self, pdf_type, transaction):
        pdf_types = {
            "confirmation": (
                lambda t: t.get_confirmation_pdf(),
                lambda p: p.payment_confirmation_report,
                "Facture",
            ),
            "refund": (
                lambda t: t.get_refund_pdf(),
                lambda p: p.payment_refund_report,
                "Remboursement",
            ),
        }
        gen_func, report_func, description = pdf_types[pdf_type]
        file_name, file_bytes = gen_func(transaction)
        complementary_document_attrs = {
            "document": File(
                file_bytes,
                name=file_name,
            )
        }
        form = self.get_form_for_payment()
        child_doc_type = None
        for doc_type in report_func(form.payment_settings).document_types.all():
            if doc_type.parent.form.pk == form.pk:
                child_doc_type = doc_type
                break

        if child_doc_type is None:
            # Payment settings are not configured correctly, failing silently
            return None
        complementary_document_attrs["document_type"] = child_doc_type

        complementary_document_attrs[
            "description"
        ] = f"{description} {transaction.merchant_reference}"
        complementary_document_attrs["owner"] = self.author
        complementary_document_attrs["submission"] = self
        complementary_document_attrs[
            "status"
        ] = SubmissionComplementaryDocument.STATUS_FINALE

        complementary_document_attrs["is_public"] = False
        comp_doc = SubmissionComplementaryDocument.objects.create(
            **complementary_document_attrs
        )

        comp_doc.authorised_departments.set(PermitDepartment.objects.all())
        return comp_doc


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

    submission = models.ForeignKey(
        "Submission", on_delete=models.CASCADE, related_name="selected_forms"
    )
    form = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="selected_forms"
    )

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
        verbose_name = _("1.5 Contact")
        verbose_name_plural = _("1.5 Contacts")
        unique_together = [["type", "form_category"]]

    def __str__(self):
        return self.get_type_display() + " (" + str(self.form_category) + ")"


# Change the app_label in order to regroup models under the same app in admin
class ContactTypeForAdminSite(ContactType):
    class Meta:
        proxy = True
        app_label = "forms"
        verbose_name = _("1.5 Contact")
        verbose_name_plural = _("1.5 Contacts")


class SubmissionContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    submission = models.ForeignKey(
        "Submission", on_delete=models.CASCADE, related_name="submission_contacts"
    )
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
    Value of a property for a selected object in a submission.
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

    def get_value(self):
        value = self.value["val"]
        if self.field.input_type == Field.INPUT_TYPE_DATE:
            return parse_date(value)

        elif self.field.input_type == Field.INPUT_TYPE_FILE:
            private_storage = fields.PrivateFileSystemStorage()
            # TODO: handle missing files! Database pointing empty files should be removed
            try:
                f = private_storage.open(value)
                # The `url` attribute of the file is used to detect if there was already a file set (it is used by
                # `ClearableFileInput` and by the `set_object_property_value` function)
                f.url = reverse(
                    "submissions:submission_media_download",
                    kwargs={"property_value_id": self.pk},
                )
            except IOError:
                f = None

            return f

        return value


class SubmissionGeoTime(models.Model):
    """
    Permit location in space and time
    """

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="geo_time"
    )
    starts_at = models.DateTimeField(_("Date de début"), blank=True, null=True)
    ends_at = models.DateTimeField(_("Date de fin"), blank=True, null=True)
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


class SubmissionWorkflowStatusQuerySet(models.QuerySet):
    def get_statuses_for_administrative_entity(self, administrative_entity):
        """
        Returns the status availables for an administrative entity
        """
        return self.filter(administrative_entity=administrative_entity).values_list(
            "status", flat=True
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

    objects = SubmissionWorkflowStatusQuerySet().as_manager()

    def __str__(self):
        return str(self.get_status_display())

    class Meta:
        verbose_name = _("Status disponible pour l'entité administrative")
        verbose_name_plural = _("Status disponibles pour l'entité administratives")
        unique_together = ("status", "administrative_entity")


class ArchivedSubmissionQuerySet(models.QuerySet):
    def filter_for_user(self, user):
        """
        Return the list of archived requests this user has access to.
        """
        if not user.is_authenticated:
            return self.none()

        if user.is_superuser:
            return self

        qs_filter = Q(archivist=user)
        qs_filter |= Q(
            submission__administrative_entity__in=AdministrativeEntity.objects.associated_to_user(
                user
            )
        )

        return self.filter(qs_filter)


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

    objects = ArchivedSubmissionQuerySet().as_manager()

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
        verbose_name = _("2.3 Enquête publique")
        verbose_name_plural = _("2.3 Enquêtes publiques")

    @classmethod
    def get_current_inquiry(cls, submission):
        today = datetime.today()
        return cls.objects.filter(
            submission=submission, start_date__lte=today, end_date__gte=today
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


class ChildrenFormManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=False)

    def associated_to_parent(self, parent):
        """
        Get the complementary document types associated the parent
        """
        return self.get_queryset().filter(
            parent=parent,
        )


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
        through="reports.report_document_types",
    )

    objects = models.Manager()

    # Only children objects
    children_objects = ChildrenFormManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(Q(parent__isnull=False) & Q(form__isnull=True))
                | (Q(parent__isnull=True) & Q(form__isnull=False)),
                name="complementary_document_type_restrict_form_link_to_parents",
            )
        ]
        verbose_name = _("3.2 Catégorie de document")
        verbose_name_plural = _("3.2 Catégories de document")

    def __str__(self):
        return self.name


# Change the app_label in order to regroup models under the same app in admin
class ComplementaryDocumentTypeForAdminSite(ComplementaryDocumentType):
    class Meta:
        proxy = True
        app_label = "reports"
        verbose_name = _("3.2 Catégorie de document")
        verbose_name_plural = _("3.2 Catégories de document")


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
        verbose_name = _("2.1 Champ de traitement des demandes")
        verbose_name_plural = _("2.1 Champs de traitement des demandes")

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
        related_name="submission_validations",
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
