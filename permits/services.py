import enum
import itertools
import os
import urllib

from collections import defaultdict
from constance import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mass_mail
from django.db import transaction
from django.db.models import Max, Min, Q
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _

from . import fields, forms, geoservices, models
from .exceptions import BadPermitRequestStatus
from .utils import reverse_permit_request_url


class GeoTimeInfo(enum.Enum):
    DATE = enum.auto()
    GEOMETRY = enum.auto()


def get_works_object_type_choices(permit_request):
    return (
        models.WorksObjectTypeChoice.objects.filter(permit_request=permit_request)
        .select_related("permit_request", "works_object_type")
        .prefetch_related("works_object_type__properties")
    )


@transaction.atomic
def set_object_property_value(permit_request, object_type, prop, value):
    """
    Create or update the `WorksObjectPropertyValue` object for the given property, object type and permit request. The
    record will be deleted if value is an empty string or None. `value` can be a variety of types: str in the case of
    a text property, bool in the case of a boolean property, int in the case of a number property, and File or bool in
    the case of a file property (the latter being `False` if the user is asking for the file to be removed).
    """
    existing_value_obj = models.WorksObjectPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request,
        works_object_type_choice__works_object_type=object_type,
        property=prop,
    )
    is_file = prop.input_type == models.WorksObjectProperty.INPUT_TYPE_FILE
    is_date = prop.input_type == models.WorksObjectProperty.INPUT_TYPE_DATE

    if value == "" or value is None:
        existing_value_obj.delete()
    else:
        if is_file:

            # Prevent large file upload
            if value.size > config.MAX_FILE_UPLOAD_SIZE:
                return
            # Use private storage to prevent uploaded files exposition to the outside world
            private_storage = fields.PrivateFileSystemStorage()
            # If the given File has a `url` attribute, it means the value comes from the `initial` form data, so the
            # value hasn't changed
            if getattr(value, "url", None):
                return

            # Remove the previous file, if any
            try:
                current_value = existing_value_obj.get()
            except models.WorksObjectPropertyValue.DoesNotExist:
                pass
            else:
                private_storage.delete(current_value.value["val"])
            # User has asked to remove the file. The file has already been removed from the storage, remove the property
            # value record and we're done
            if value is False:
                existing_value_obj.delete()
                return

            # Add the file to the storage
            directory = "permit_requests_uploads/{}".format(permit_request.pk)
            ext = os.path.splitext(value.name)[1]
            path = os.path.join(
                directory, "{}_{}{}".format(object_type.pk, prop.pk, ext)
            )
            private_storage.save(path, value)
            value = path

        elif is_date:
            value = value.isoformat()

        value_dict = {"val": value}
        nb_objs = existing_value_obj.update(value=value_dict)

        # No existing property value record, create it
        if nb_objs == 0:
            (
                works_object_type_choice,
                created,
            ) = models.WorksObjectTypeChoice.objects.get_or_create(
                permit_request=permit_request, works_object_type=object_type
            )
            models.WorksObjectPropertyValue.objects.create(
                works_object_type_choice=works_object_type_choice,
                property=prop,
                value=value_dict,
            )


def get_properties_values(permit_request):
    """
    Return a queryset of `WorksObjectPropertyValue` objects for the given `permit_request`, excluding properties of type
    file.
    """
    return (
        models.WorksObjectPropertyValue.objects.filter(
            works_object_type_choice__permit_request=permit_request
        )
        .exclude(property__input_type=models.WorksObjectProperty.INPUT_TYPE_FILE)
        .select_related(
            "works_object_type_choice",
            "works_object_type_choice__works_object_type",
            "property",
        )
    )


def get_appendices_values(permit_request):
    """
    Return a queryset of `WorksObjectPropertyValue` objects of type file for the given `permit_request`.
    """
    return models.WorksObjectPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request,
        property__input_type=models.WorksObjectProperty.INPUT_TYPE_FILE,
    ).select_related(
        "works_object_type_choice",
        "works_object_type_choice__works_object_type",
        "property",
    )


def get_permit_request_properties(permit_request):
    """
    Yield `(WorksObjectType, WorksObjectProperty)` tuples for every `works_object_type_choices`.
    """
    objects_props = get_properties(permit_request)
    for works_object_type, props in objects_props:
        for prop in props:
            yield (works_object_type, prop)


def get_permit_request_appendices(permit_request):
    """
    Yield `(WorksObjectType, WorksObjectProperty)` tuples for every `works_object_type_choices`, only returning
    properties with input type file.
    """
    objects_props = get_appendices(permit_request)
    for works_object_type, props in objects_props:
        for prop in props:
            yield (works_object_type, prop)


def get_works_types(administrative_entity, user):

    queryset = (
        models.WorksType.objects.filter(
            pk__in=models.WorksObjectType.objects.filter(
                administrative_entities=administrative_entity
            ).values_list("works_type_id", flat=True)
        )
        .order_by("name")
        .distinct()
    )

    if not user.has_perm("see_private_demands"):
        queryset = queryset.filter(works_object_types__is_public=True)

    return queryset


def get_works_objects(administrative_entity):
    queryset = (
        models.WorksObject.objects.filter(
            pk__in=models.WorksObjectType.objects.filter(
                administrative_entities=administrative_entity
            ).values_list("works_object_id", flat=True)
        )
        .order_by("name")
        .distinct()
    )

    if not user.has_perm("see_private_demands"):
        queryset = queryset.filter(works_object_types__is_public=True)

    return queryset


def get_administrative_entities(user):
    queryset = (
        models.PermitAdministrativeEntity.objects.filter(
            pk__in=models.WorksObjectType.objects.filter(is_public=True,).values_list(
                "administrative_entities", flat=True
            ),
        )
        .order_by("ofs_id", "-name")
        .distinct()
    )

    if not user.has_perm("see_private_demands"):
        queryset = queryset = queryset.filter(works_object_types__is_public=True)

    return queryset


def get_permit_request_works_types(permit_request):
    return (
        models.WorksType.objects.filter(
            works_object_types__permit_requests=permit_request
        )
        .order_by("name")
        .distinct()
    )


def _get_properties_filtered(permit_request, props_filter):
    """
    Return a list of `(WorksObjectType, QuerySet[WorksObjectTypeProperty])` for all object types of the given
    `permit_request`. `props_filter` is passed the properties queryset and should return it (or a filtered version of
    it).
    """
    props_by_object_type = [
        (
            works_object_type,
            props_filter(works_object_type.properties.all()).order_by("order", "name"),
        )
        for works_object_type in permit_request.works_object_types.order_by(
            "works_object__name", "works_type__name"
        )
    ]

    return [
        (works_object_type, props)
        for works_object_type, props in props_by_object_type
        if props
    ]


def get_properties(permit_request):
    return _get_properties_filtered(
        permit_request,
        lambda qs: qs.exclude(input_type=models.WorksObjectProperty.INPUT_TYPE_FILE),
    )


def get_appendices(permit_request):
    return _get_properties_filtered(
        permit_request,
        lambda qs: qs.filter(input_type=models.WorksObjectProperty.INPUT_TYPE_FILE),
    )


def set_works_types(permit_request, new_works_types):
    """
    Delete `WorksObjectTypeChoice` records that relate to a `WorksType` that is not in `new_works_types` (which must be
    an iterable of `WorksType` instances).
    """
    get_works_object_type_choices(permit_request).exclude(
        works_object_type__works_type__in=new_works_types
    ).delete()


@transaction.atomic
def set_works_object_types(permit_request, new_works_object_types):
    """
    Add the given `new_works_object_types`, which should be an iterable of `WorksObjectType` instances to the given
    `permit_request`. Existing `WorksObjectType` are ignored.
    """
    # Check which object type are new or have been removed. We can't just remove them all and recreate them
    # because there might be data related to these relations (eg. WorksObjectPropertyValue)
    get_works_object_type_choices(permit_request).exclude(
        works_object_type__in=new_works_object_types
    ).delete()

    for works_object_type in new_works_object_types:
        models.WorksObjectTypeChoice.objects.get_or_create(
            permit_request=permit_request, works_object_type=works_object_type
        )

    geotime_objects = get_geotime_objects(permit_request.id)

    if len(geotime_objects) > 0:
        geotime_required_info = get_geotime_required_info(permit_request)
        # Reset the geometry/date if the new_works_object_type do not need Date/Geom
        if len(geotime_required_info) == 0:
            geotime_objects.delete()
        # Reset the date only
        if GeoTimeInfo.DATE not in geotime_required_info:
            geotime_objects.update(starts_at=None, ends_at=None)
        # Reset the geometry only
        if GeoTimeInfo.GEOMETRY not in geotime_required_info:
            geotime_objects.update(geom=None)


@transaction.atomic
def set_administrative_entity(permit_request, administrative_entity):
    """
    Set the given `administrative_entity`, which should be an instance of `models.PermitAdministrativeEntity`.
    `WorksObjectTypeChoice` records that don't exist in the new `administrative_entity` will be deleted.
    """
    get_works_object_type_choices(permit_request).exclude(
        works_object_type__in=administrative_entity.works_object_types.all()
    ).delete()

    permit_request.administrative_entity = administrative_entity
    permit_request.save()


def get_property_value(object_property_value):
    value = object_property_value.value["val"]
    if (
        object_property_value.property.input_type
        == models.WorksObjectProperty.INPUT_TYPE_DATE
    ):
        return parse_date(value)

    elif (
        object_property_value.property.input_type
        == models.WorksObjectProperty.INPUT_TYPE_FILE
    ):
        private_storage = fields.PrivateFileSystemStorage()
        f = private_storage.open(value)
        # The `url` attribute of the file is used to detect if there was already a file set (it is used by
        # `ClearableFileInput` and by the `set_object_property_value` function)
        f.url = reverse(
            "permits:permit_request_media_download",
            kwargs={"property_value_id": object_property_value.pk},
        )

        return f

    return value


def get_user_administrative_entities(user):
    return models.PermitAdministrativeEntity.objects.filter(
        departments__group__in=user.groups.all(),
    ).order_by("ofs_id", "-name")


def get_user_departments(user):
    return models.PermitDepartment.objects.filter(group__in=user.groups.all())


def get_permit_request_for_user_or_404(user, permit_request_id, statuses=None):
    """
    Return the permit request with `permit_request_id` or raise an Http404 if there is no such permit request. The
    permit request must either belong to the given user, or the given user should be in the same administrative entity.
    If `statuses` is set and a permit request is found but its status doesn't match any value in `statuses`,
    `BadPermitRequestStatus` will be raised.
    """
    permit_request = get_object_or_404(
        get_permit_requests_list_for_user(user), pk=permit_request_id
    )

    if statuses is not None and permit_request.status not in statuses:
        raise BadPermitRequestStatus(permit_request, statuses)

    return permit_request


def get_permit_requests_list_for_user(user):
    """
    Return the list of permit requests this user has access to.
    """
    if not user.is_authenticated:
        return models.PermitRequest.objects.none().annotate(
            starts_at_min=Min("geo_time__starts_at"),
            ends_at_max=Max("geo_time__ends_at"),
        )

    if user.is_superuser:
        return models.PermitRequest.objects.all().annotate(
            starts_at_min=Min("geo_time__starts_at"),
            ends_at_max=Max("geo_time__ends_at"),
        )
    else:
        qs = Q(author=user.permitauthor)

        if user.has_perm("permits.amend_permit_request"):
            qs |= Q(
                administrative_entity__in=get_user_administrative_entities(user),
            ) & ~Q(status=models.PermitRequest.STATUS_DRAFT)

        if user.has_perm("permits.validate_permit_request"):
            qs |= Q(
                validations__department__in=models.PermitDepartment.objects.filter(
                    group__in=user.groups.all()
                )
            )

        return models.PermitRequest.objects.filter(qs).annotate(
            starts_at_min=Min("geo_time__starts_at"),
            ends_at_max=Max("geo_time__ends_at"),
        )


def get_actors_types(permit_request):
    """
        Get actors type defined for each work type defined for the permit_request
    """

    return models.PermitActorType.objects.filter(
        works_type__in=get_permit_request_works_types(permit_request)
    ).values_list("type", "is_mandatory")


def filter_only_missing_actor_types(actor_types, permit_request):
    """
        Filter the given `actor_types` to return only the ones that have not been set in the given `permit_request`.
    """

    existing_actor_types = permit_request.permit_request_actors.values_list(
        "actor_type", flat=True
    )

    return [
        actor_type
        for actor_type in actor_types
        if actor_type[0] not in existing_actor_types
    ]


def get_missing_required_actor_types(permit_request):
    """
        Get actors type required but not filled
    """

    return filter_only_missing_actor_types(
        [
            (actor_type, is_mandatory)
            for actor_type, is_mandatory in get_actors_types(permit_request)
            if is_mandatory
        ],
        permit_request,
    )


def get_permitactorformset_initiated(permit_request, data=None):
    """
    Return PermitActorFormSet with initial values set
    """

    # Queryset with all configured actor type for this permit_request
    configured_actor_types = get_actors_types(permit_request)

    # Get actor type that are not filled yet for the permit_request
    missing_actor_types = filter_only_missing_actor_types(
        configured_actor_types, permit_request
    )

    actor_initial_forms = [
        {"actor_type": actor_type[0]} for actor_type in missing_actor_types
    ]

    PermitActorFormSet = modelformset_factory(
        models.PermitRequestActor,
        form=forms.PermitRequestActorForm,
        extra=len(actor_initial_forms),
    )

    formset = PermitActorFormSet(
        initial=actor_initial_forms,
        queryset=models.PermitRequestActor.objects.filter(
            permit_request=permit_request
        ).select_related("actor"),
        data=data,
    )

    mandatory_actor_types = {
        actor_type
        for actor_type, is_mandatory in configured_actor_types
        if is_mandatory
    }

    for form in formset:
        form.empty_permitted = (
            "actor_type" not in form.initial
            or form.initial["actor_type"] not in mandatory_actor_types
        )

    return formset


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


#########
# STEPS #
#########


def get_administrative_entity_step(permit_request):
    return models.Step(
        name=_("Entité"),
        url=reverse_permit_request_url(
            "permits:permit_request_select_administrative_entity", permit_request
        )
        if permit_request
        else reverse("permits:permit_request_select_administrative_entity"),
        completed=permit_request is not None,
        enabled=True,
    )


def get_works_types_step(permit_request, completed):
    # When there’s only 1 works type it will be automatically selected, so there’s no
    # reason to show the step
    if (
        permit_request
        and len(
            get_works_types(
                permit_request.administrative_entity, permit_request.author.user
            )
        )
        <= 1
    ):
        return None

    return models.Step(
        name=_("Type"),
        url=reverse_permit_request_url(
            "permits:permit_request_select_types", permit_request
        )
        if permit_request
        else None,
        completed=completed,
        enabled=True,
    )


def get_works_objects_step(permit_request, enabled, works_types, user):
    # If there are default works objects types it means the object types can be
    # automatically selected and so the step shouldn’t be visible
    if permit_request:
        selected_works_types = (
            works_types
            or permit_request.works_object_types.values_list("works_type", flat=True)
        )
        candidate_works_object_types = (
            models.WorksObjectType.objects.filter(works_type__in=selected_works_types)
            if selected_works_types
            else permit_request.administrative_entity.works_object_types.all()
        )

        if (
            get_default_works_object_types(
                permit_request.administrative_entity,
                user,
                works_types=selected_works_types or None,
            )
            # Also check if the candidates works types would all result in a single
            # works object (which will anyway get automatically selected)
            or candidate_works_object_types.values_list("works_object", flat=True)
            .distinct()
            .count()
            <= 1
        ):
            return None

    # If the user is editing a permit request and the administrative entity only has 1
    # works type, there won’t be a works type step, so the works object step should have
    # it in the URL
    if permit_request and not works_types:
        if user.has_perm("see_private_demands"):
            administrative_entity_works_types = permit_request.administrative_entity.works_object_types.values_list(
                "works_type", flat=True
            ).distinct()
        else:
            administrative_entity_works_types = (
                permit_request.administrative_entity.works_object_types.filter(
                    is_public=True
                )
                .values_list("works_type", flat=True)
                .distinct()
            )

        if len(administrative_entity_works_types) == 1:
            works_types = administrative_entity_works_types

    works_types_qs = (
        urllib.parse.urlencode({"types": works_types}, doseq=True,)
        if works_types
        else ""
    )

    return models.Step(
        name=_("Objets"),
        url=(
            reverse_permit_request_url(
                "permits:permit_request_select_objects", permit_request
            )
            + (f"?{works_types_qs}" if works_types_qs else "")
        )
        if permit_request
        else "",
        completed=enabled,
        enabled=enabled,
    )


def get_properties_step(permit_request, enabled):
    properties_form = (
        forms.WorksObjectsPropertiesForm(
            instance=permit_request, enable_required=True, disable_fields=True, data={}
        )
        if permit_request
        else None
    )
    properties_errors = len(properties_form.errors) if properties_form else 0
    properties_url = (
        reverse_permit_request_url("permits:permit_request_properties", permit_request)
        if permit_request
        else ""
    )

    return models.Step(
        name=_("Détails"),
        url=properties_url,
        completed=enabled and properties_form and not properties_form.errors,
        errors_count=properties_errors,
        enabled=enabled,
    )


def get_geo_time_step(permit_request, enabled):
    geo_time_errors = (
        0
        if permit_request is None or get_geotime_objects(permit_request.id).exists()
        else 1
    )
    geo_time_url = (
        reverse_permit_request_url("permits:permit_request_geo_time", permit_request)
        if permit_request
        else ""
    )
    required_info = get_geotime_required_info(permit_request)

    if not (GeoTimeInfo.DATE in required_info or GeoTimeInfo.GEOMETRY in required_info):
        return None

    return models.Step(
        name=get_geo_step_name_title(required_info)["step_name"],
        url=geo_time_url,
        completed=geo_time_errors == 0,
        errors_count=geo_time_errors,
        enabled=enabled,
    )


def get_geo_step_name_title(required_info):
    name_title = {}
    if GeoTimeInfo.DATE not in required_info:
        name_title["title"] = config.GEO_STEP
        name_title["step_name"] = _("Localisation")
    elif GeoTimeInfo.GEOMETRY not in required_info:
        name_title["title"] = config.TIME_STEP
        name_title["step_name"] = _("Planning")
    else:
        name_title["title"] = config.GEO_TIME_STEP
        name_title["step_name"] = _("Planning et localisation")

    return name_title


def get_geotime_required_info(permit_request):
    if not permit_request:
        return set()
    works_object_types = permit_request.works_object_types.all()
    required_info = set()
    if any(works_object_type.needs_date for works_object_type in works_object_types):
        required_info.add(GeoTimeInfo.DATE)

    if any(
        works_object_type.needs_geometry for works_object_type in works_object_types
    ):
        required_info.add(GeoTimeInfo.GEOMETRY)

    return required_info


def get_geotime_objects(permit_request_id):
    return models.PermitRequestGeoTime.objects.filter(
        permit_request_id=permit_request_id
    )


def get_appendices_step(permit_request, enabled):
    if permit_request and len(get_appendices(permit_request)) == 0:
        return None

    appendices_url = (
        reverse_permit_request_url("permits:permit_request_appendices", permit_request)
        if permit_request
        else ""
    )
    appendices_form = (
        forms.WorksObjectsAppendicesForm(
            instance=permit_request, enable_required=True, disable_fields=True, data={}
        )
        if permit_request
        else None
    )
    appendices_errors = len(appendices_form.errors) if appendices_form else 0

    return models.Step(
        name=_("Documents"),
        url=appendices_url,
        completed=enabled and appendices_errors == 0,
        errors_count=appendices_errors,
        enabled=enabled,
    )


def get_actors_step(permit_request, enabled):
    if permit_request and len(get_actors_types(permit_request)) == 0:
        return None

    actor_errors = (
        len(get_missing_required_actor_types(permit_request)) if permit_request else 0
    )
    actors_url = (
        reverse_permit_request_url("permits:permit_request_actors", permit_request)
        if permit_request
        else ""
    )
    return models.Step(
        name=_("Contacts"),
        url=actors_url,
        enabled=enabled,
        errors_count=actor_errors,
        completed=actor_errors == 0,
    )


def get_submit_step(permit_request, enabled, total_errors):
    submit_url = (
        reverse_permit_request_url("permits:permit_request_submit", permit_request)
        if permit_request
        else ""
    )

    return models.Step(
        name=_("Résumé et envoi"),
        url=submit_url,
        enabled=enabled,
        errors_count=total_errors,
        completed=total_errors == 0,
    )


def get_progress_bar_steps(request, permit_request):
    """
    Return a dict of `Step` items that can be used to track the user progress through
    the permit request wizard. The dict only contains reachable steps (which don’t
    necessarily have a `url` though, eg. before selecting the administrative entity).
    """
    has_works_objects_types = (
        permit_request.works_object_types.exists() if permit_request else False
    )
    selected_works_types = request.GET.getlist("types")

    all_steps = {
        models.StepType.ADMINISTRATIVE_ENTITY: get_administrative_entity_step(
            permit_request
        ),
        models.StepType.WORKS_TYPES: get_works_types_step(
            permit_request=permit_request,
            completed=has_works_objects_types or selected_works_types,
        ),
        models.StepType.WORKS_OBJECTS: get_works_objects_step(
            permit_request=permit_request,
            enabled=has_works_objects_types,
            works_types=selected_works_types,
            user=request.user,
        ),
        models.StepType.PROPERTIES: get_properties_step(
            permit_request=permit_request, enabled=has_works_objects_types
        ),
        models.StepType.GEO_TIME: get_geo_time_step(
            permit_request=permit_request, enabled=has_works_objects_types
        ),
        models.StepType.APPENDICES: get_appendices_step(
            permit_request=permit_request, enabled=has_works_objects_types
        ),
        models.StepType.ACTORS: get_actors_step(
            permit_request=permit_request, enabled=has_works_objects_types
        ),
    }

    total_errors = sum([step.errors_count for step in all_steps.values() if step])
    all_steps[models.StepType.SUBMIT] = get_submit_step(
        permit_request=permit_request,
        enabled=has_works_objects_types,
        total_errors=total_errors,
    )

    return {
        step_type: step for step_type, step in all_steps.items() if step is not None
    }


def get_previous_step(steps, current_step):
    """
    Return the previous step in the list or raise `IndexError` if there’s no such
    step.
    """
    return list(
        itertools.takewhile(lambda step: step[0] != current_step, steps.items())
    )[-1][1]


def get_next_step(steps, current_step):
    """
    Return the next step in the list or raise `IndexError` if there’s no such
    step.
    """
    return list(
        itertools.dropwhile(lambda step: step[0] != current_step, steps.items())
    )[1][1]


def submit_permit_request(permit_request, absolute_uri_func):
    """
    Change the permit request status to submitted and send notification e-mails. `absolute_uri_func` should be a
    callable that takes a path and returns an absolute URI, usually `request.build_absolute_uri`.
    """
    if not permit_request.can_be_submitted_by_author():
        raise SuspiciousOperation

    permit_request.status = models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
    if GeoTimeInfo.GEOMETRY in get_geotime_required_info(permit_request):
        permit_request.intersected_geometries = geoservices.get_intersected_geometries(
            permit_request
        )
    permit_request.save()
    permit_request_url = absolute_uri_func(
        reverse(
            "permits:permit_request_detail",
            kwargs={"permit_request_id": permit_request.pk},
        )
    )

    users_to_notify = set(
        get_user_model()
        .objects.filter(
            groups__permitdepartment__administrative_entity=permit_request.administrative_entity,
            permitauthor__user__email__isnull=False,
            groups__permitdepartment__is_validator=False,
        )
        .values_list("permitauthor__user__email", flat=True)
    )

    email_contents = render_to_string(
        "permits/emails/permit_request_submitted.txt",
        {"permit_request_url": permit_request_url},
    )
    emails = [
        (
            "Nouvelle demande de permis",
            email_contents,
            settings.DEFAULT_FROM_EMAIL,
            [email_address],
        )
        for email_address in users_to_notify
    ]

    acknowledgment_email_contents = render_to_string(
        "permits/emails/permit_request_acknowledgment.txt",
        {
            "permit_request_url": permit_request_url,
            "name": permit_request.author.user.get_full_name(),
            "administrative_entity_name": permit_request.administrative_entity.name,
        },
    )
    emails.append(
        (
            "Votre demande de permis",
            acknowledgment_email_contents,
            settings.DEFAULT_FROM_EMAIL,
            [permit_request.author.user.email],
        )
    )

    if emails:
        send_mass_mail(emails)


@transaction.atomic
def request_permit_request_validation(permit_request, departments, absolute_uri_func):
    permit_request.status = models.PermitRequest.STATUS_AWAITING_VALIDATION
    permit_request.save()

    for department in departments:
        models.PermitRequestValidation.objects.get_or_create(
            permit_request=permit_request, department=department
        )

    users_to_notify = {
        email
        for department in departments
        for email in department.group.user_set.values_list(
            "permitauthor__user__email", flat=True
        )
    }

    email_contents = render_to_string(
        "permits/emails/permit_request_validation_request.txt",
        {
            "permit_request_url": absolute_uri_func(
                reverse(
                    "permits:permit_request_detail",
                    kwargs={"permit_request_id": permit_request.pk},
                )
            ),
            "administrative_entity": permit_request.administrative_entity,
        },
    )
    emails = [
        (
            "Nouvelle demande de permis",
            email_contents,
            settings.DEFAULT_FROM_EMAIL,
            [email_address],
        )
        for email_address in users_to_notify
    ]

    if emails:
        send_mass_mail(emails)


def send_validation_reminder(permit_request, absolute_uri_func):
    """
    Send a reminder to departments that have not yet processed the given `permit_request` and return the list of pending
    validations.
    """
    pending_validations = permit_request.get_pending_validations()
    users_to_notify = set(
        get_user_model()
        .objects.filter(
            groups__permitdepartment__in=pending_validations.values_list(
                "department", flat=True
            )
        )
        .values_list("permitauthor__user__email", flat=True)
        .distinct()
    )

    email_contents = render_to_string(
        "permits/emails/permit_request_validation_reminder.txt",
        {
            "permit_request_url": absolute_uri_func(
                reverse(
                    "permits:permit_request_detail",
                    kwargs={"permit_request_id": permit_request.pk},
                )
            ),
            "administrative_entity": permit_request.administrative_entity,
        },
    )
    emails = [
        (
            "Rappel: une demande est en attente de validation",
            email_contents,
            settings.DEFAULT_FROM_EMAIL,
            [email_address],
        )
        for email_address in users_to_notify
    ]

    if emails:
        send_mass_mail(emails)

    return pending_validations


def has_permission_to_amend_permit_request(user, permit_request):
    return user.has_perm(
        "permits.amend_permit_request"
    ) and permit_request.administrative_entity in get_user_administrative_entities(user)


def can_amend_permit_request(user, permit_request):
    return permit_request.can_be_amended() and has_permission_to_amend_permit_request(
        user, permit_request
    )


def has_permission_to_validate_permit_request(user, permit_request):
    return (
        user.has_perm("permits.validate_permit_request")
        and get_permit_requests_list_for_user(user)
        .filter(pk=permit_request.pk)
        .exists()
    )


def can_validate_permit_request(user, permit_request):
    return permit_request.can_be_validated() and has_permission_to_validate_permit_request(
        user, permit_request
    )


def has_permission_to_poke_permit_request(user, permit_request):
    return user.has_perm(
        "permits.amend_permit_request"
    ) and permit_request.administrative_entity in get_user_administrative_entities(user)


def can_poke_permit_request(user, permit_request):
    return (
        permit_request.status == models.PermitRequest.STATUS_AWAITING_VALIDATION
        and has_permission_to_poke_permit_request(user, permit_request)
    )


def has_permission_to_classify_permit_request(user, permit_request):
    return user.has_perm(
        "permits.amend_permit_request"
    ) and permit_request.administrative_entity in get_user_administrative_entities(user)


def can_classify_permit_request(user, permit_request):

    status_choices_for_administrative_entity = get_status_choices_for_administrative_entity(
        permit_request.administrative_entity
    )
    no_validation_process = (
        models.PermitRequest.STATUS_AWAITING_VALIDATION
        not in status_choices_for_administrative_entity
        and models.PermitRequest.STATUS_APPROVED
        in status_choices_for_administrative_entity
        and models.PermitRequest.STATUS_REJECTED
        in status_choices_for_administrative_entity
        and permit_request.status == models.PermitRequest.STATUS_PROCESSING
    )
    return (
        permit_request.status == models.PermitRequest.STATUS_AWAITING_VALIDATION
        and permit_request.get_pending_validations().count() == 0
        and has_permission_to_classify_permit_request(user, permit_request)
    ) or no_validation_process


def has_permission_to_edit_permit_request(user, permit_request):
    return (
        user.has_perm("permits.edit_permit_request")
        and get_permit_requests_list_for_user(user)
        .filter(pk=permit_request.pk)
        .exists()
    )


def can_edit_permit_request(user, permit_request):
    return permit_request.can_be_edited_by_pilot() and has_permission_to_edit_permit_request(
        user, permit_request
    )


def get_contacts_summary(permit_request):

    actor_types = dict(models.ACTOR_TYPE_CHOICES)

    contacts = [
        (
            actor_types.get(contact["actor_type"].value(), ""),
            [
                (field.label, field.value())
                for field in contact
                if field.name not in {"id", "actor_type"}
            ],
        )
        for contact in get_permitactorformset_initiated(permit_request)
        if contact["id"].value()
    ]

    return contacts


def get_permit_objects(permit_request):

    properties_form = forms.WorksObjectsPropertiesForm(instance=permit_request)
    appendices_form = forms.WorksObjectsAppendicesForm(instance=permit_request)
    properties_by_object_type = dict(properties_form.get_fields_by_object_type())
    appendices_by_object_type = dict(appendices_form.get_fields_by_object_type())
    amend_custom_properties_values = get_amend_custom_properties_values(permit_request)
    amend_custom_properties_by_object_type = defaultdict(list)
    for value in amend_custom_properties_values:
        amend_custom_properties_by_object_type[
            value.works_object_type_choice.works_object_type
        ].append(value)
    objects_infos = [
        (
            obj,
            properties_by_object_type.get(obj, []),
            appendices_by_object_type.get(obj, []),
            amend_custom_properties_by_object_type[obj],
        )
        for obj in permit_request.works_object_types.all()
    ]

    return objects_infos


def get_status_choices_for_administrative_entity(administrative_entity):
    """
    Returns the status availables for an administrative entity
    """
    return models.PermitWorkflowStatus.objects.filter(
        administrative_entity=administrative_entity
    ).values_list("status", flat=True)


def get_actions_for_administrative_entity(permit_request):
    """
    Filter out administrative workflow step that are not coherent
    with current permit_request status
    """

    actions = models.ACTIONS

    # Statuses for which a given action should be availble
    required_statuses_for_actions = {
        "amend": list(models.PermitRequest.AMENDABLE_STATUSES),
        "request_validation": [models.PermitRequest.STATUS_AWAITING_VALIDATION],
        "poke": [models.PermitRequest.STATUS_AWAITING_VALIDATION],
        "validate": [
            models.PermitRequest.STATUS_APPROVED,
            models.PermitRequest.STATUS_REJECTED,
            models.PermitRequest.STATUS_AWAITING_VALIDATION,
            models.PermitRequest.STATUS_PROCESSING,
        ],
    }

    available_statuses_for_administrative_entity = get_status_choices_for_administrative_entity(
        permit_request.administrative_entity
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


def get_permit_request_amend_custom_properties(permit_request):

    props_by_object_type = get_permit_request_amend_custom_properties_by_object_type(
        permit_request
    )
    for works_object_type, props in props_by_object_type:
        for prop in props:
            yield (works_object_type, prop)


def get_permit_request_amend_custom_properties_by_object_type(permit_request):

    works_object_types = permit_request.works_object_types.prefetch_related(
        "amend_properties"
    ).select_related("works_object", "works_type")

    for works_object_type in works_object_types:
        yield (works_object_type, works_object_type.amend_properties.all())


def get_default_works_object_types(
    administrative_entity, user, works_types=None,
):
    """
    Return the `WorksObjectType` that should be automatically selected for the given
    `administrative_entity`. `works_types` should be the works types the user has
    selected, if any.
    """
    if user.has_perm("see_private_demands"):
        works_object_types = administrative_entity.works_object_types.all()
    else:
        works_object_types = administrative_entity.works_object_types.filter(
            is_public=True
        ).all()

    if works_types is not None:
        works_object_types = works_object_types.filter(works_type__in=works_types)

    available_works_objects = {
        works_object_type.works_object_id for works_object_type in works_object_types
    }
    available_works_types = {
        works_object_type.works_type_id for works_object_type in works_object_types
    }

    # If `works_types` are not set, ie. the user has only selected an administrative
    # entity but no works types yes, and there’s more than 1 works type available, don’t
    # return any default works object type so the user can choose the works type(s)
    # first
    if (works_types is None and len(available_works_types) > 1) or len(
        available_works_objects
    ) > 1:
        return []

    return works_object_types


@transaction.atomic
def set_amend_custom_property_value(permit_request, object_type, prop, value):
    """
    Create or update the `PermitRequestAmendPropertyValues` object for the given
    property, object type and permit request. The record will be deleted if value is
    an empty string or None. Value is only str type.
    """
    existing_value_obj = models.PermitRequestAmendPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request,
        works_object_type_choice__works_object_type=object_type,
        property=prop,
    )

    if value == "" or value is None:
        existing_value_obj.delete()
    else:
        nb_objs = existing_value_obj.update(value=value)
        # No existing property value record, create it
        if nb_objs == 0:
            (
                works_object_type_choice,
                created,
            ) = models.WorksObjectTypeChoice.objects.get_or_create(
                permit_request=permit_request, works_object_type=object_type
            )
            models.PermitRequestAmendPropertyValue.objects.create(
                works_object_type_choice=works_object_type_choice,
                property=prop,
                value=value,
            )


def get_amend_custom_properties_values(permit_request):
    """
    Return a queryset of `PermitRequestAmendPropertyValue` objects for the given
    `permit_request`.
    """
    return models.PermitRequestAmendPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request
    ).select_related(
        "works_object_type_choice",
        "works_object_type_choice__works_object_type",
        "property",
    )
