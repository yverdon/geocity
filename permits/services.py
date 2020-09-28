import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mass_mail
from django.db import transaction
from django.db.models import Q, Max, Min
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from . import models, forms, geoservices, fields
from .exceptions import BadPermitRequestStatus


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

            # Use private storage to prevent uploaded files exposition to the outside world
            private_storage = fields.PrivateFileSystemStorage()
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
                private_storage.delete(current_value.value['val'])
            # User has asked to remove the file. The file has already been removed from the storage, remove the property
            # value record and we're done
            if value is False:
                existing_value_obj.delete()
                return

            # Add the file to the storage
            directory = 'permit_requests_uploads/{}'.format(permit_request.pk)
            ext = os.path.splitext(value.name)[1]
            path = os.path.join(directory, '{}_{}{}'.format(object_type.pk, prop.pk, ext))
            private_storage.save(path, value)
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
        pk__in=models.WorksObjectType.objects.filter(
            administrative_entities=administrative_entity
        ).values_list('works_type_id', flat=True)
    ).order_by('name')


def get_administrative_entities():
    return models.PermitAdministrativeEntity.objects.order_by('name')


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
    Set the given `administrative_entity`, which should be an instance of `models.PermitAdministrativeEntity`.
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
        private_storage = fields.PrivateFileSystemStorage()
        f = private_storage.open(value)
        # The `url` attribute of the file is used to detect if there was already a file set (it is used by
        # `ClearableFileInput` and by the `set_object_property_value` function)
        f.url = reverse('permits:permit_request_media_download', kwargs={
                        'property_value_id': object_property_value.pk})

        return f

    return value


def get_user_administrative_entities(user):
    return models.PermitAdministrativeEntity.objects.filter(departments__group__in=user.groups.all())


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
        get_permit_requests_list_for_user(user), pk=permit_request_id)

    if statuses is not None and permit_request.status not in statuses:
        raise BadPermitRequestStatus(permit_request, statuses)

    return permit_request


def get_permit_requests_list_for_user(user):
    """
    Return the list of permit requests this user has access to.
    """
    if not user.is_authenticated:
        return models.PermitRequest.objects.none().annotate(starts_at_min=Min('geo_time__starts_at'), ends_at_max=Max('geo_time__ends_at'))

    if user.is_superuser:
        return models.PermitRequest.objects.all().annotate(starts_at_min=Min('geo_time__starts_at'), ends_at_max=Max('geo_time__ends_at'))
    else:
        qs = Q(author=user.permitauthor)

        if user.has_perm("permits.amend_permit_request"):
            qs |= Q(
                administrative_entity__in=get_user_administrative_entities(user),
            ) & ~Q(
                status=models.PermitRequest.STATUS_DRAFT
            )

        if user.has_perm("permits.validate_permit_request"):
            qs |= Q(
                validations__department__in=models.PermitDepartment.objects.filter(
                    group__in=user.groups.all())
            )

        return models.PermitRequest.objects.filter(qs).annotate(starts_at_min=Min('geo_time__starts_at'), ends_at_max=Max('geo_time__ends_at'))


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
    existing_actor_types = set(
        permit_request.permit_request_actors.values_list('actor_type', flat=True))
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
    )
    appendices_form = forms.WorksObjectsAppendicesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    )

    missing_actor_types = get_missing_actors_types(permit_request)

    actor_errors = [
        _('Contact de type "%s" manquant.') % models.ACTOR_TYPE_CHOICES[actor_type][1]
        for actor_type in missing_actor_types
    ]

    return sum(
        len(errors)
        for errors in [appendices_form.errors, properties_form.errors, actor_errors]
    )


def get_progressbar_steps(request, permit_request):
    """
    Return a dict of `Step` items that can be used to track the user progress through the permit request wizard.
    """
    def reverse_permit_request_url(name):
        if permit_request:
            return reverse(name, kwargs={'permit_request_id': permit_request.pk})
        else:
            return None

    has_objects_types = permit_request.works_object_types.exists()

    localisation_url = (
        reverse_permit_request_url('permits:permit_request_select_administrative_entity')
        if permit_request
        else reverse('permits:permit_request_select_administrative_entity')
    )

    works_types_url = reverse_permit_request_url('permits:permit_request_select_types')

    if permit_request and has_objects_types:
        objects_types_url = reverse_permit_request_url('permits:permit_request_select_objects')
        properties_url = reverse_permit_request_url('permits:permit_request_properties')
        appendices_url = reverse_permit_request_url('permits:permit_request_appendices')
        geo_time_url = reverse_permit_request_url('permits:permit_request_geo_time')
        actors_url = reverse_permit_request_url('permits:permit_request_actors')
        submit_url = reverse_permit_request_url('permits:permit_request_submit')
    else:
        objects_types_url = properties_url = appendices_url = actors_url = submit_url = geo_time_url = ''

    properties_form = forms.WorksObjectsPropertiesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    ) if permit_request else None
    appendices_form = forms.WorksObjectsAppendicesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    ) if permit_request else None

    properties_errors = len(properties_form.errors) if properties_form else 0
    appendices_errors = len(appendices_form.errors) if appendices_form else 0
    geo_time_errors = 0 if models.PermitRequestGeoTime.objects.filter(
        permit_request=permit_request).count() == 1 else 1
    actor_errors = len(get_missing_actors_types(permit_request)) if permit_request else 0
    total_errors = sum([properties_errors, appendices_errors, actor_errors])

    steps = {
        "location": models.Step(
            name=_("Entité"),
            url=localisation_url,
            completed=bool(permit_request),
            enabled=True,
        ),
        "works_types": models.Step(
            name=_("Type"),
            url=works_types_url,
            completed=has_objects_types or request.GET.getlist('types'),
            enabled=True,
        ),
        "objects_types": models.Step(
            name=_("Objets"),
            url=objects_types_url,
            completed=has_objects_types,
            enabled=has_objects_types,
        ),
        "properties": models.Step(
            name=_("Détails"),
            url=properties_url,
            completed=has_objects_types and properties_form and not properties_form.errors,
            errors_count=properties_errors,
            enabled=has_objects_types,
        ),
        "geo_time": models.Step(
            name=_("Agenda et plan"),
            url=geo_time_url,
            completed=geo_time_errors == 0,
            errors_count=geo_time_errors,
            enabled=has_objects_types,
        ),
        "appendices": models.Step(
            name=_("Documents"),
            url=appendices_url,
            completed=has_objects_types and appendices_form and not appendices_form.errors,
            errors_count=appendices_errors,
            enabled=has_objects_types,
        ),
        "actors": models.Step(
            name=_("Contacts"),
            url=actors_url,
            enabled=has_objects_types,
            errors_count=actor_errors,
            completed=not actor_errors,
        ),
        "submit": models.Step(
            name=_("Résumé et envoi"),
            url=submit_url,
            enabled=has_objects_types,
            errors_count=total_errors,
            completed=total_errors == 0,
        ),
    }

    return steps


def submit_permit_request(permit_request, absolute_uri_func):
    """
    Change the permit request status to submitted and send notification e-mails. `absolute_uri_func` should be a
    callable that takes a path and returns an absolute URI, usually `request.build_absolute_uri`.
    """
    if not permit_request.can_be_submitted_by_author():
        raise SuspiciousOperation

    permit_request.status = models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
    permit_request.intersected_geometries = geoservices.get_intersected_geometries(permit_request)
    permit_request.save()
    permit_request_url = absolute_uri_func(
        reverse("permits:permit_request_detail", kwargs={"permit_request_id": permit_request.pk})
    )

    users_to_notify = set(get_user_model().objects.filter(
        groups__permitdepartment__administrative_entity=permit_request.administrative_entity,
        permitauthor__user__email__isnull=False,
    ).values_list("permitauthor__user__email", flat=True))

    email_contents = render_to_string("permits/emails/permit_request_submitted.txt", {
        "permit_request_url": permit_request_url
    })
    emails = [
        ("Nouvelle demande de permis", email_contents, settings.DEFAULT_FROM_EMAIL, [email_address])
        for email_address in users_to_notify
    ]

    acknowledgment_email_contents = render_to_string("permits/emails/permit_request_acknowledgment.txt", {
        "permit_request_url": permit_request_url,
        "name": permit_request.author.user.get_full_name(),
        "administrative_entity_name": permit_request.administrative_entity.name,
    })
    emails.append(
        (
            "Votre demande de permis", acknowledgment_email_contents, settings.DEFAULT_FROM_EMAIL,
            [permit_request.author.user.email]
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
        for email in department.group.user_set.values_list("permitauthor__user__email", flat=True)
    }

    email_contents = render_to_string("permits/emails/permit_request_validation_request.txt", {
        "permit_request_url": absolute_uri_func(
            reverse("permits:permit_request_detail", kwargs={
                    "permit_request_id": permit_request.pk})
        ),
        "administrative_entity": permit_request.administrative_entity,
    })
    emails = [
        ("Nouvelle demande de permis", email_contents, settings.DEFAULT_FROM_EMAIL, [email_address])
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
    users_to_notify = set(get_user_model().objects.filter(
        groups__permitdepartment__in=pending_validations.values_list("department", flat=True)
    ).values_list("permitauthor__user__email", flat=True).distinct())

    email_contents = render_to_string("permits/emails/permit_request_validation_reminder.txt", {
        "permit_request_url": absolute_uri_func(
            reverse("permits:permit_request_detail", kwargs={
                    "permit_request_id": permit_request.pk})
        ),
        "administrative_entity": permit_request.administrative_entity,
    })
    emails = [
        ("Rappel: une demande est en attente de validation",
         email_contents, settings.DEFAULT_FROM_EMAIL, [email_address])
        for email_address in users_to_notify
    ]

    if emails:
        send_mass_mail(emails)

    return pending_validations


def has_permission_to_amend_permit_request(user, permit_request):
    return (
        user.has_perm('permits.amend_permit_request')
        and permit_request.administrative_entity in get_user_administrative_entities(user)
    )


def can_amend_permit_request(user, permit_request):
    return (
        permit_request.can_be_amended()
        and has_permission_to_amend_permit_request(user, permit_request)
    )


def has_permission_to_validate_permit_request(user, permit_request):
    return (
        user.has_perm('permits.validate_permit_request')
        and get_permit_requests_list_for_user(user).filter(pk=permit_request.pk).exists()
    )


def can_validate_permit_request(user, permit_request):
    return (
        permit_request.can_be_validated()
        and has_permission_to_validate_permit_request(user, permit_request)
    )


def has_permission_to_poke_permit_request(user, permit_request):
    return (
        user.has_perm('permits.amend_permit_request')
        and permit_request.administrative_entity in get_user_administrative_entities(user)
    )


def can_poke_permit_request(user, permit_request):
    return (
        permit_request.status == models.PermitRequest.STATUS_AWAITING_VALIDATION
        and has_permission_to_poke_permit_request(user, permit_request)
    )


def has_permission_to_classify_permit_request(user, permit_request):
    return (
        user.has_perm('permits.amend_permit_request')
        and permit_request.administrative_entity in get_user_administrative_entities(user)
    )


def can_classify_permit_request(user, permit_request):
    return (
        (permit_request.status == models.PermitRequest.STATUS_AWAITING_VALIDATION
         and permit_request.get_pending_validations().count() == 0
         and has_permission_to_classify_permit_request(user, permit_request))
    )


def get_contacts_summary(permit_request):

    actor_types = dict(models.ACTOR_TYPE_CHOICES)

    contacts = [
        (actor_types.get(contact['actor_type'].value(), ''), [
            (field.label, field.value())
            for field in contact
            if field.name not in {'id', 'actor_type'}
        ])
        for contact in get_permitactorformset_initiated(permit_request)
        if contact['id'].value()
    ]

    return contacts


def get_permit_objects(permit_request):

    properties_form = forms.WorksObjectsPropertiesForm(instance=permit_request)
    appendices_form = forms.WorksObjectsAppendicesForm(instance=permit_request)
    properties_by_object_type = dict(properties_form.get_fields_by_object_type())
    appendices_by_object_type = dict(appendices_form.get_fields_by_object_type())

    objects_infos = [
        (
            obj,
            properties_by_object_type.get(obj, []),
            appendices_by_object_type.get(obj, [])
        )
        for obj in permit_request.works_object_types.all()
    ]

    return objects_infos


def get_status_choices_for_administrative_entity(administrative_entity):

    status = models.PermitWorkFlowStatus.objects.filter(
        administrative_entity=administrative_entity).all()

    availables_choices = []
    for value in status:
        # Prevent turning back to draft mode
        if value.status_choices.status in [models.PermitRequest.STATUS_PROCESSING,
                                           models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
                                           models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
                                           models.PermitRequest.STATUS_RECEIVED]:
            availables_choices.append(
                (value.status_choices.status,
                 value.status_choices.get_status_display()
                 )
            )

    return availables_choices


def administrative_entity_has_status(administrative_entity, status):
    is_status_enabled = models.PermitWorkFlowStatus.objects.filter(
        administrative_entity=administrative_entity,
        status_choices__status=status).first()
    return is_status_enabled
