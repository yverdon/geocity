import os.path

from django import template

from permits import forms, models, services

register = template.Library()


@register.inclusion_tag('permits/_permit_progressbar.html', takes_context=True)
def permit_progressbar(context, permit_request, active_step):
    steps = services.get_progressbar_steps(context['request'], permit_request)
    steps_states = {
        'steps': steps,
        'active_step': active_step,
    }

    return steps_states


@register.filter
def basename(value):
    return os.path.basename(value)


@register.inclusion_tag('permits/_permit_request_summary.html', takes_context=True)
def permit_request_summary(context, permit_request):
    properties_form = forms.WorksObjectsPropertiesForm(instance=permit_request)
    properties_by_object_type = dict(properties_form.get_fields_by_object_type())

    appendices_form = forms.WorksObjectsAppendicesForm(instance=permit_request)
    appendices_by_object_type = dict(appendices_form.get_fields_by_object_type())

    objects_infos = [
        (
            obj,
            properties_by_object_type.get(obj, []),
            appendices_by_object_type.get(obj, [])
        )
        for obj in permit_request.works_object_types.all()
    ]

    actor_types = dict(models.ACTOR_TYPE_CHOICES)
    contacts = [
        (actor_types.get(contact['actor_type'].value(), ''), [
            (field.label, field.value())
            for field in contact
            if field.name not in {'id', 'actor_type'}
        ])
        for contact in services.get_permitactorformset_initiated(permit_request)
        if contact['id'].value()
    ]

    return {
        'contacts': contacts,
        'objects_infos': objects_infos,
    }
