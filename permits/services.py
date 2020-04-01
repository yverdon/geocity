import os

from django.core.files.storage import default_storage
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.forms import modelformset_factory


from gpf.models import AdministrativeEntity

from . import models, forms


def get_works_object_type_choices(permit_request):
    return models.WorksObjectTypeChoice.objects.filter(
        permit_request=permit_request
    ).select_related(
        'permit_request', 'works_object_type'
    ).prefetch_related('works_object_type__properties')


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
        property=prop
    )
    is_file = prop.input_type == models.WorksObjectProperty.INPUT_TYPE_FILE

    if value == "" or value is None:
        existing_value_obj.delete()
    else:
        if is_file:
            # If the given File has a `url` attribute, it means the value comes from the `initial` form data, so the
            # value hasn't changed
            if getattr(value, 'url', None):
                return

            # Remove the previous file, if any
            try:
                current_value = existing_value_obj.get()
            except models.WorksObjectPropertyValue.DoesNotExist:
                pass
            else:
                default_storage.delete(current_value.value['val'])

            # User has asked to remove the file. The file has already been removed from the storage, remove the property
            # value record and we're done
            if value is False:
                existing_value_obj.delete()
                return

            # Add the file to the storage
            directory = 'permit_requests_uploads/{}'.format(permit_request.pk)
            ext = os.path.splitext(value.name)[1]
            path = os.path.join(directory, '{}_{}{}'.format(object_type.pk, prop.pk, ext))
            default_storage.save(path, value)
            value = path

        value_dict = {'val': value}
        nb_objs = existing_value_obj.update(value=value_dict)

        # No existing property value record, create it
        if nb_objs == 0:
            works_object_type_choice, created = models.WorksObjectTypeChoice.objects.get_or_create(
                permit_request=permit_request, works_object_type=object_type
            )
            models.WorksObjectPropertyValue.objects.create(
                works_object_type_choice=works_object_type_choice,
                property=prop,
                value=value_dict
            )


def get_properties_values(permit_request):
    """
    Return a queryset of `WorksObjectPropertyValue` objects for the given `permit_request`, excluding properties of type
    file.
    """
    return models.WorksObjectPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request
    ).exclude(
        property__input_type=models.WorksObjectProperty.INPUT_TYPE_FILE
    ).select_related('works_object_type_choice', 'works_object_type_choice__works_object_type', 'property')


def get_appendices_values(permit_request):
    """
    Return a queryset of `WorksObjectPropertyValue` objects of type file for the given `permit_request`.
    """
    return models.WorksObjectPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request,
        property__input_type=models.WorksObjectProperty.INPUT_TYPE_FILE
    ).select_related('works_object_type_choice', 'works_object_type_choice__works_object_type', 'property')


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


def get_works_types(administrative_entity):
    return models.WorksType.objects.filter(
        pk__in=models.WorksObjectType.objects.values_list('works_type_id', flat=True)
    ).order_by('name')


def get_administrative_entities():
    return AdministrativeEntity.objects.order_by('name')


def get_permit_request_works_types(permit_request):
    return models.WorksType.objects.filter(
        works_object_types__permit_requests=permit_request
    ).order_by('name').distinct()


def _get_properties_filtered(permit_request, props_filter):
    """
    Return a list of `(WorksObjectType, QuerySet[WorksObjectTypeProperty])` for all object types of the given
    `permit_request`. `props_filter` is passed the properties queryset and should return it (or a filtered version of
    it).
    """
    props_by_object_type = [
        (works_object_type, props_filter(works_object_type.properties.all()).order_by('name'))
        for works_object_type in permit_request.works_object_types.order_by('works_object__name', 'works_type__name')
    ]

    return [(works_object_type, props) for works_object_type, props in props_by_object_type if props]


def get_properties(permit_request):
    return _get_properties_filtered(
        permit_request, lambda qs: qs.exclude(input_type=models.WorksObjectProperty.INPUT_TYPE_FILE)
    )


def get_appendices(permit_request):
    return _get_properties_filtered(
        permit_request, lambda qs: qs.filter(input_type=models.WorksObjectProperty.INPUT_TYPE_FILE)
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


@transaction.atomic
def set_administrative_entity(permit_request, administrative_entity):
    """
    Set the given `administrative_entity`, which should be an instance of `gpf.AdministrativeEntity`.
    `WorksObjectTypeChoice` records that don't exist in the new `administrative_entity` will be deleted.
    """
    get_works_object_type_choices(permit_request).exclude(
        works_object_type__in=administrative_entity.works_object_types.all()
    ).delete()

    permit_request.administrative_entity = administrative_entity
    permit_request.save()


def get_property_value(object_property_value):
    value = object_property_value.value['val']

    if object_property_value.property.input_type == models.WorksObjectProperty.INPUT_TYPE_FILE:
        f = default_storage.open(value)
        # The `url` attribute of the file is used to detect if there was already a file set (it is used by
        # `ClearableFileInput` and by the `set_object_property_value` function)
        f.url = reverse('permits:permit_request_media_download', kwargs={'property_value_id': object_property_value.pk})
        value = f

    return value


def get_permit_request_for_user_or_404(user, permit_request_id):
    """
    Return the permit request with `permit_request_id` and associated to the `user` actor.
    """
    return get_object_or_404(models.PermitRequest, author=user.actor, pk=permit_request_id)


def get_permitactorformset_initiated(permit_request, data=None):
    """
    Return PermitActorFormSet with initial values set
    """
    missing_actor_types = get_missing_actors_types(permit_request)

    actor_initial_forms = [
        {'actor_type': actor_type}
        for actor_type in missing_actor_types
    ]

    PermitActorFormSet = modelformset_factory(
        models.PermitRequestActor,
        form=forms.PermitRequestActorForm,
        extra=len(actor_initial_forms)
    )

    formset = PermitActorFormSet(
        initial=actor_initial_forms,
        queryset=models.PermitRequestActor.objects.filter(permit_request=permit_request),
        data=data
    )

    return formset


def get_missing_actors_types(permit_request):
    """
    Return PermitRequestActor yet to be filled
    """
    existing_actor_types = set(permit_request.permit_request_actors.values_list('actor_type', flat=True))
    required_actor_types = set(models.PermitActorType.objects.filter(
        works_type__in=get_permit_request_works_types(permit_request)
    ).values_list('type', flat=True))

    return required_actor_types - existing_actor_types


def get_total_error_count(permit_request):
    """
    Return the total count of errors in forms for a given permit request
    """
    properties_form = forms.WorksObjectsPropertiesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    ) if permit_request else None
    appendices_form = forms.WorksObjectsAppendicesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    ) if permit_request else None

    remaining_actors = len(get_missing_actors_types(permit_request))
    actor_errors = []
    i = 0
    while i < remaining_actors:
        actor_errors.append(1)
        i+=1

    actor_completed = False
    if remaining_actors <= 0:
        actor_completed = True

    errors = {**appendices_form.errors, **properties_form.errors, **dict.fromkeys(actor_errors, 1)}

    return len(errors)
