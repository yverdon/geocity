from django.db import transaction

from . import models


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
    record will be deleted if value is an empty string or None.
    """
    existing_value_obj = models.WorksObjectPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request,
        works_object_type_choice__works_object_type=object_type,
        property=prop
    )

    if value == "" or value is None:
        existing_value_obj.delete()
    else:
        value_dict = {'val': value}

        nb_objs = models.WorksObjectPropertyValue.objects.filter(
            works_object_type_choice__permit_request=permit_request,
            works_object_type_choice__works_object_type=object_type,
            property=prop
        ).update(value=value_dict)

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
    for works_object_type in permit_request.works_objects_types.all():
        for prop in works_object_type.properties.exclude(input_type=models.WorksObjectProperty.INPUT_TYPE_FILE):
            yield (works_object_type, prop)


def get_permit_request_appendices(permit_request):
    """
    Yield `(WorksObjectType, WorksObjectProperty)` tuples for every `works_object_type_choices`, only returning
    properties with input type file.
    """
    for works_object_type in permit_request.works_objects_types.all():
        for prop in works_object_type.properties.filter(input_type=models.WorksObjectProperty.INPUT_TYPE_FILE):
            yield (works_object_type, prop)


def get_works_types():
    return models.WorksType.objects.order_by('name')


def get_permit_request_works_types(permit_request):
    return permit_request.works_objects_types.values_list(
        'works_type', flat=True
    ).order_by('works_type__name').distinct()


def get_properties(works_objects_types):
    works_objects_types = works_objects_types.prefetch_related('properties').filter(properties__input_type=...)
    return [(works_object_type, works_object_type.properties.all()) for works_object_type in works_objects_types]


def get_appendices(works_objects_types):
    works_objects_types = works_objects_types.prefetch_related('properties')
    return [(works_object_type, works_object_type.properties.all()) for works_object_type in works_objects_types]


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
