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
    Return a queryset of `WorksObjectPropertyValue` objects for the given `permit_request`.
    """
    return models.WorksObjectPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request
    ).select_related('works_object_type_choice', 'works_object_type_choice__works_object_type', 'property')


def properties_for_choices(works_object_type_choices):
    """
    Yield `(WorksObjectTypeChoice, WorksObjectProperty)` tuples for every `works_object_type_choices`.
    """
    for choice in works_object_type_choices:
        for prop in choice.works_object_type.properties.exclude(input_type=models.WorksObjectProperty.INPUT_TYPE_FILE):
            yield (choice, prop)


def get_works_types():
    return models.WorksType.objects.order_by('name')
