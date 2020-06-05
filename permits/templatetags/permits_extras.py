import os.path

from django import template

from permits import services

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

    objects_infos = services.get_permit_objects(permit_request)
    contacts = services.get_contacts_summary(permit_request)

    return {
        'contacts': contacts,
        'objects_infos': objects_infos,
    }
