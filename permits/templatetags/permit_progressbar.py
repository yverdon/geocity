import dataclasses
from typing import Dict, List

from django import template
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from permits import forms, models, services

register = template.Library()


@dataclasses.dataclass
class Step:
    name: str
    url: str
    completed: bool = False
    enabled: bool = False
    errors: List[Dict[str, str]] = dataclasses.field(default_factory=list)


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
        actors_url = reverse_permit_request_url('permits:permit_request_actors')
        submit_url = reverse_permit_request_url('permits:permit_request_submit')
        print(submit_url)
    else:
        objects_types_url = properties_url = appendices_url = actors_url = submit_url = ''

    properties_form = forms.WorksObjectsPropertiesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    ) if permit_request else None
    appendices_form = forms.WorksObjectsAppendicesForm(
        instance=permit_request, enable_required=True, disable_fields=True, data={}
    ) if permit_request else None

    remaining_actors = services.check_permitrequestactor_state(permit_request)
    actor_errors = []
    i = 0
    while i < remaining_actors:
        actor_errors.append(1)
        i+=1

    actor_completed = False
    if remaining_actors <= 0:
        actor_completed = True

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
            errors=properties_form.errors if properties_form else [],
            enabled=has_objects_types,
        ),
        "appendices": Step(
            name=_("Documents"),
            url=appendices_url,
            completed=has_objects_types and appendices_form and not appendices_form.errors,
            errors=appendices_form.errors if appendices_form else [],
            enabled=has_objects_types,
        ),
        "actors": Step(
            name=_("Contacts"),
            url=actors_url,
            enabled=has_objects_types,
            errors=actor_errors,
            completed=actor_completed,
        ),
        "submit": Step(
            name=_("Résumé et envoi"),
            url=submit_url,
            enabled=has_objects_types,
            errors={**appendices_form.errors, **properties_form.errors, **dict.fromkeys(actor_errors, 1)},
            completed=len({**appendices_form.errors, **properties_form.errors, **dict.fromkeys(actor_errors, 1)})==0,
        ),
    }
    steps_states = {
        'steps': steps,
        'active_step': active_step,
    }

    return steps_states
