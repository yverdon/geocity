import dataclasses

from django import template
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from permits import forms, services

register = template.Library()


@dataclasses.dataclass
class Step:
    name: str
    url: str
    completed: bool = False
    enabled: bool = False
    errors_count: int = 0


@register.inclusion_tag('permits/_permit_progressbar.html', takes_context=True)
def permit_progressbar(context, permit_request, active_step):
    def reverse_permit_request_url(name):
        if permit_request:
            return reverse(name, kwargs={'permit_request_id': permit_request.pk})
        else:
            return None

    request = context['request']
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
    actor_errors = len(services.get_missing_actors_types(permit_request)) if permit_request else 0
    total_errors = sum([properties_errors, appendices_errors, actor_errors])

    steps = {
        "location": Step(
            name=_("Localisation"),
            url=localisation_url,
            completed=bool(permit_request),
            enabled=True,
        ),
        "works_types": Step(
            name=_("Type"),
            url=works_types_url,
            completed=has_objects_types or request.GET.getlist('types'),
            enabled=has_objects_types,
        ),
        "objects_types": Step(
            name=_("Objets"),
            url=objects_types_url,
            completed=has_objects_types,
            enabled=has_objects_types,
        ),
        "properties": Step(
            name=_("Détails"),
            url=properties_url,
            completed=has_objects_types and properties_form and not properties_form.errors,
            errors_count=properties_errors,
            enabled=has_objects_types,
        ),
        "geo_time": Step(
            name=_("Agenda et plan"),
            url=geo_time_url,
            completed=has_objects_types,
            enabled=has_objects_types,
        ),
        "appendices": Step(
            name=_("Documents"),
            url=appendices_url,
            completed=has_objects_types and appendices_form and not appendices_form.errors,
            errors_count=appendices_errors,
            enabled=has_objects_types,
        ),
        "actors": Step(
            name=_("Contacts"),
            url=actors_url,
            enabled=has_objects_types,
            errors_count=actor_errors,
            completed=not actor_errors,
        ),
        "submit": Step(
            name=_("Résumé et envoi"),
            url=submit_url,
            enabled=has_objects_types,
            errors_count=total_errors,
            completed=total_errors == 0,
        ),
    }
    steps_states = {
        'steps': steps,
        'active_step': active_step,
    }

    return steps_states
