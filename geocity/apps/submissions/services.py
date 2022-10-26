import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime

import filetype
from constance import config
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
    SuspiciousOperation,
    ValidationError,
)
from django.core.mail import send_mass_mail
from django.db import transaction
from django.db.models import Q
from django.http.response import FileResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from geocity.apps.accounts.models import AdministrativeEntity
from geocity.apps.accounts.validators import validate_email

from . import fields, forms, models


def get_works_types(administrative_entity, user):
    queryset = (
        models.WorksType.objects.filter(
            pk__in=models.WorksObjectType.objects.filter(
                administrative_entities=administrative_entity
            ).values_list("works_type_id", flat=True),
            works_object_types__is_anonymous=False,
        )
        .order_by("name")
        .distinct()
    )

    if not user.has_perm("permits.see_private_requests"):
        queryset = queryset.filter(works_object_types__is_public=True)

    return queryset


def get_property_value_based_on_property(prop):
    property_object = models.WorksObjectPropertyValue.objects.get(
        property__name=prop["properties__property__name"],
        works_object_type_choice__id=prop["id"],
    )
    # get_property_value return None if file does not exist
    return get_property_value(property_object)


def get_total_error_count(permit_request):
    """
    Return the total count of errors in forms for a given permit request
    """
    properties_form = forms.WorksObjectsPropertiesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    )
    appendices_form = forms.WorksObjectsAppendicesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    )

    missing_actor_types = get_missing_required_actor_types(permit_request)

    actor_errors = [
        _('Contact de type "%s" manquant.') % models.ACTOR_TYPE_CHOICES[actor_type][1]
        for actor_type in missing_actor_types
    ]

    return sum(
        len(errors)
        for errors in [appendices_form.errors, properties_form.errors, actor_errors]
    )


def submit_submission(submission, request):
    """
    Change the permit request status to submitted and send notification e-mails. `absolute_uri_func` should be a
    callable that takes a path and returns an absolute URI, usually `request.build_absolute_uri`.
    FIXME: rename to `request_submission_validation`?
    """
    if not submission.can_be_submitted_by_author():
        raise SuspiciousOperation

    is_awaiting_supplement = (
        submission.status == models.Submission.STATUS_AWAITING_SUPPLEMENT
    )

    if is_awaiting_supplement:
        data = {
            "subject": "{} ({})".format(
                _("La demande de compléments a été traitée"),
                submission.get_categories_names_list(),
            ),
            "users_to_notify": submission.get_secretary_email(),
            "template": "permit_request_complemented.txt",
            "submission": submission,
            "absolute_uri_func": request.build_absolute_uri,
            "objects_list": submission.get_forms_names_list(),
        }
        send_email_notification(data)

    else:
        # Here we create a new Permit Request, therefore if it contains one or more
        # WOTs that can be prolonged with no Date required but can be renewed, we need
        # to calculate the dates automatically
        submission.set_dates_for_renewable_forms()

        users_to_notify = set(
            get_user_model()
            .objects.filter(
                Q(
                    groups__permitdepartment__administrative_entity=submission.administrative_entity,
                    author__email__isnull=False,
                    groups__permitdepartment__is_integrator_admin=False,
                ),
                Q(
                    Q(
                        groups__permitdepartment__is_validator=False,
                    )
                    | Q(
                        groups__permitdepartment__is_validator=True,
                        groups__permitdepartment__is_backoffice=True,
                    )
                ),
                Q(author__userprofile__notify_per_email=True),
            )
            .values_list("author__email", flat=True)
        )

        data = {
            "subject": "{} ({})".format(
                _("Nouvelle demande"), submission.get_categories_names_list()
            ),
            "users_to_notify": users_to_notify,
            "template": "permit_request_submitted.txt",
            "submission": submission,
            "absolute_uri_func": request.build_absolute_uri,
            # FIXME rename in template (was `objects_list`)
            "forms_list": submission.get_forms_names_list(),
        }
        send_email_notification(data)

        if submission.author.notify_per_email:
            data["subject"] = "{} ({})".format(
                _("Votre demande"), submission.get_categories_names_list()
            )
            data["users_to_notify"] = [submission.author.user.email]
            data["template"] = "permit_request_acknowledgment.txt"
            # FIXME rename in template (was `objects_list`)
            data["forms_list"] = submission.get_forms_names_list()
            send_email_notification(data)

    submission.status = models.Submission.STATUS_SUBMITTED_FOR_VALIDATION
    if models.GeoTimeInfo.GEOMETRY in submission.get_geotime_required_info():
        submission.intersected_geometries = submission.get_intersected_geometries()
    submission.save()
    clear_session_filters(request)


@transaction.atomic
def request_submission_validation(submission, departments, absolute_uri_func):
    submission.status = models.Submission.STATUS_AWAITING_VALIDATION
    submission.save()

    for department in departments:
        models.SubmissionValidation.objects.get_or_create(
            submission=submission, department=department
        )

    users_to_notify = set(
        User.objects.filter(
            Q(
                groups__permitdepartment__in=departments,
                userprofile__notify_per_email=True,
            )
        ).values_list("userprofile__user__email", flat=True)
    )

    data = {
        "subject": "{} ({})".format(
            _("Nouvelle demande en attente de validation"),
            submission.get_categories_names_list(),
        ),
        "users_to_notify": users_to_notify,
        # FIXME rename template
        "template": "submission_validation_request.txt",
        "submission": submission,
        "absolute_uri_func": absolute_uri_func,
        # FIXME rename in template (was `objects_list`)
        "forms_list": submission.get_forms_names_list(),
    }
    send_email_notification(data)


def send_validation_reminder(permit_request, absolute_uri_func):
    """
    Send a reminder to departments that have not yet processed the given `permit_request` and return the list of pending
    validations.
    """
    pending_validations = permit_request.get_pending_validations()
    users_to_notify = set(
        get_user_model()
        .objects.filter(
            Q(
                groups__permitdepartment__in=pending_validations.values_list(
                    "department", flat=True
                ),
                permitauthor__notify_per_email=True,
            )
        )
        .values_list("permitauthor__user__email", flat=True)
        .distinct()
    )

    data = {
        "subject": "{} ({})".format(
            _("Demande toujours en attente de validation"),
            permit_request.get_categories_names_list(),
        ),
        "users_to_notify": users_to_notify,
        "template": "permit_request_validation_reminder.txt",
        "permit_request": permit_request,
        "absolute_uri_func": absolute_uri_func,
        "objects_list": permit_request.get_forms_names_list(),
    }
    send_email_notification(data)
    return pending_validations


def send_email_notification(data):
    from_email_name = (
        f'{data["permit_request"].administrative_entity.expeditor_name} '
        if data["permit_request"].administrative_entity.expeditor_name
        else ""
    )
    sender = (
        f'{from_email_name}<{data["permit_request"].administrative_entity.expeditor_email}>'
        if data["permit_request"].administrative_entity.expeditor_email
        else settings.DEFAULT_FROM_EMAIL
    )
    send_email(
        template=data["template"],
        sender=sender,
        receivers=data["users_to_notify"],
        subject=data["subject"],
        context={
            "permit_request_url": data["absolute_uri_func"](
                reverse(
                    "permits:permit_request_detail",
                    kwargs={"permit_request_id": data["permit_request"].pk},
                )
            ),
            "administrative_entity": data["permit_request"].administrative_entity,
            "name": data["permit_request"].author.user.get_full_name(),
            "permit_request": data["permit_request"],
            "objects_list": data["objects_list"],
        },
    )


def send_email(template, sender, receivers, subject, context):
    email_content = render_to_string(f"permits/emails/{template}", context)
    emails = [
        (
            subject,
            email_content,
            sender,
            [email_address],
        )
        for email_address in receivers
        if validate_email(email_address)
    ]

    if emails:
        send_mass_mail(emails, fail_silently=True)


def get_submission_forms(submission):
    fields_form = forms.FieldsForm(instance=submission)
    appendices_form = forms.AppendicesForm(instance=submission)
    fields_by_object_type = dict(fields_form.get_form_fields_by_form())
    appendices_by_object_type = dict(appendices_form.get_form_fields_by_form())
    amend_custom_fields_values = submission.get_amend_custom_fields_values()
    amend_custom_properties_by_object_type = defaultdict(list)
    for value in amend_custom_fields_values:
        amend_custom_properties_by_object_type[value.selected_form.form].append(value)
    forms_infos = [
        (
            selected_form.form,
            fields_by_object_type.get(selected_form.form, []),
            appendices_by_object_type.get(selected_form.form, []),
            amend_custom_properties_by_object_type[selected_form.form],
        )
        for selected_form in submission.selected_forms.all()
    ]

    return forms_infos


# Validate a file, from checking the first bytes and detecting the kind of the file
# Exemple : User puts "my_malware.exe" and rename as "file.txt"
# kind.extension => will return "exe"
# kind.mime => will return "application/x-msdownload"
def validate_file(file):
    kind = filetype.guess(file)
    if kind is not None:
        extensions = config.ALLOWED_FILE_EXTENSIONS.replace(" ", "").split(",")
        if kind.extension not in extensions:
            raise ValidationError(
                _("%(file)s n'est pas du bon type"),
                params={"file": file},
            )
        elif file.size > config.MAX_FILE_UPLOAD_SIZE:
            raise ValidationError(
                _("%(file)s est trop volumineux"),
                params={"file": file},
            )
        # Check that image file is not corrupted
        if kind.extension != "pdf":
            # Check that image is not corrupted and that PIL can read it - Try to resize it
            try:
                with Image.open(file) as image:
                    image.thumbnail((128, 128))
            except:
                raise forms.ValidationError(
                    _("%(file)s n'est pas valide ou contient des erreurs"),
                    params={"file": file},
                )
    else:
        raise ValidationError(
            _(
                "Le type de %(file)s n'est pas supporté, assurez-vous que votre fichier soit du bon type"
            ),
            params={"file": file},
        )


def store_tags_in_session(request):

    if "entityfilter" not in request.session or request.GET.get(
        "clearentityfilter", None
    ):
        request.session["entityfilter"] = []

    if len(request.GET.getlist("entityfilter")) > 0:
        request.session["entityfilter"] = request.GET.getlist("entityfilter")
    else:
        request.session["entityfilter"] = []

    if "typefilter" not in request.session or request.GET.get("cleartypefilter", None):
        request.session["typefilter"] = []

    if len(request.GET.getlist("typefilter")) > 0:
        request.session["typefilter"] = request.GET.getlist("typefilter")
    else:
        request.session["typefilter"] = []


def clear_session_filters(request):
    request.session["entityfilter"] = []
    request.session["typefilter"] = []


def get_wot_properties(value, user_is_authenticated=None, value_with_type=False):
    """
    Return wot properties in a list for the api, in a dict for backend
    """
    obj = value.all()
    wot_props = obj.values(
        "properties__property__name",
        "properties__property__input_type",
        "properties__value__val",
        "works_object_type_id",
        "id",
        "works_object_type__works_object__name",
        "works_object_type__works_type__name",
        "properties__property__is_public_when_permitrequest_is_public",
    )

    wot_properties = dict()
    property = list()
    last_wot = ""

    if wot_props:
        # Flat view is used in the api for geocalandar, the WOT shows only the works_object__name and not the type
        if value_with_type:
            wot_properties = list()
            for prop in wot_props:
                wot = f'{prop["works_object_type__works_object__name"]} ({prop["works_object_type__works_type__name"]})'

                # List of a list, to split wot in objects. Check if last wot changed or never assigned. Means it's first iteration
                if property and wot != last_wot:
                    wot_properties.append(property)
                    property = []
                    # WOT
                    property.append(
                        {
                            "key": "work_object_type",
                            "value": wot,
                            "type": "text",
                        }
                    )

                if not last_wot:
                    property.append(
                        {
                            "key": "work_object_type",
                            "value": wot,
                            "type": "text",
                        }
                    )

                last_wot = f'{prop["works_object_type__works_object__name"]} ({prop["works_object_type__works_type__name"]})'

                if prop["properties__property__input_type"] == "file" and (
                    user_is_authenticated
                    or prop[
                        "properties__property__is_public_when_permitrequest_is_public"
                    ]
                ):
                    # get_property_value return None if file does not exist
                    file = get_property_value_based_on_property(prop)
                    # Check if file exist
                    if file:
                        # Properties of WOT
                        property.append(
                            {
                                "key": prop["properties__property__name"],
                                "value": file.url,
                                "type": prop["properties__property__input_type"],
                            }
                        )
                elif prop["properties__value__val"] and (
                    user_is_authenticated
                    or prop[
                        "properties__property__is_public_when_permitrequest_is_public"
                    ]
                ):
                    # Properties of WOT
                    property.append(
                        {
                            "key": prop["properties__property__name"],
                            "value": prop["properties__value__val"],
                            "type": prop["properties__property__input_type"],
                        }
                    )
            # Add last wot_properties, or show something when there's only one
            wot_properties.append(property)
        else:
            for prop in wot_props:
                wot = f'{prop["works_object_type__works_object__name"]} ({prop["works_object_type__works_type__name"]})'
                wot_properties[wot] = {
                    prop_i[
                        "properties__property__name"
                    ]: get_property_value_based_on_property(prop_i).url
                    # Check this is a file and the file exist
                    if prop_i["properties__property__input_type"] == "file"
                    and get_property_value_based_on_property(prop_i)
                    else prop_i["properties__value__val"]
                    for prop_i in wot_props
                    if prop_i["works_object_type_id"] == prop["works_object_type_id"]
                    and prop_i["properties__property__name"]
                }
    return wot_properties


def get_amend_properties(value):
    # FIXME what’s the type of value? QuerySet[SelectedForm]?
    obj = value.all()
    amend_props = obj.values(
        "amend_properties__property__name",
        "amend_properties__value",
        "works_object_type_id",
        "works_object_type__works_object__name",
        "works_object_type__works_type__name",
    )
    amend_properties = {}

    for prop in amend_props:
        amends = f'{prop["works_object_type__works_object__name"]} ({prop["works_object_type__works_type__name"]})'
        amend_properties[amends] = {
            prop_i["amend_properties__property__name"]: prop_i[
                "amend_properties__value"
            ]
            for prop_i in amend_props
            if prop_i["works_object_type_id"] == prop["works_object_type_id"]
            and prop_i["amend_properties__property__name"]
        }

    return amend_properties


def is_anonymous_request_logged_in(request, entity):
    """
    Verify the authentication for anonymous permit requests.
    """
    return (
        request.user.is_authenticated
        and request.user.userprofile.is_temporary
        and request.session.get("anonymous_request_token", None)
        == hash((request.user.userprofile, entity))
    )


def login_for_anonymous_request(request, entity):
    """
    Authenticate with a new temporary user to proceed with an anonymous permit request.
    """
    temp_author = models.UserProfile.objects.create_temporary_user(entity)
    login(request, temp_author.user, "django.contrib.auth.backends.ModelBackend")
    request.session["anonymous_request_token"] = hash((temp_author, entity))


def download_file(path):
    storage = fields.PrivateFileSystemStorage()
    # for some strange reason, firefox refuses to download the file.
    # so we need to set the `Content-Type` to `application/octet-stream` so
    # firefox will download it. For the time being, this "dirty" hack works
    return FileResponse(storage.open(path), content_type="application/octet-stream")


def download_archives(archive_ids, user):
    archives = []
    for archive_id in archive_ids:
        archive = models.ArchivedPermitRequest.objects.filter(
            permit_request=archive_id
        ).first()

        if not archive:
            raise ObjectDoesNotExist

        if not can_download_archive(user, archive.archivist):
            raise PermissionDenied

        archives.append(archive)

    filename = f"Archive_{datetime.today().strftime('%d.%m.%Y.%H.%M.%S')}.zip"

    if len(archives) == 1:
        return FileResponse(archives[0].archive, filename=filename)
    else:
        with tempfile.NamedTemporaryFile() as tmp_file:
            with zipfile.ZipFile(tmp_file, "w") as zip_file:
                for archive in archives:
                    zip_file.write(archive.archive.path, archive.archive.name)
            return FileResponse(open(tmp_file.name, "rb"), filename=filename)
