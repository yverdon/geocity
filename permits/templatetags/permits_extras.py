import os.path

from django import template

from permits import services, forms, models
from django.utils.translation import gettext as _

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
    geo_time_instance = permit_request.geo_time.first()
    geo_time_form = forms.PermitRequestGeoTimeForm(instance=geo_time_instance)
    geo_time_form.fields['geom'].widget.attrs['edit_geom'] = False
    geo_time_form.fields['geom'].widget.attrs['administrative_entity_json_url'] = \
        '/permit-requests/adminentitiesgeojson/' + str(permit_request.administrative_entity.id)
    geo_time_form.fields['geom'].widget.attrs['administrative_entity_id'] = str(permit_request.administrative_entity.id)

    if permit_request.creditor_type:
        creditor = models.ACTOR_TYPE_CHOICES[permit_request.creditor_type][1]
    else:
        creditor = _('Auteur de la demande, ') + \
            permit_request.author.user.first_name + ' ' + permit_request.author.user.last_name

    for elem in ['starts_at', 'ends_at', 'external_link', 'comment']:
        geo_time_form.fields[elem].widget.attrs['readonly'] = True

    return {
        'creditor': creditor,
        'contacts': contacts,
        'objects_infos': objects_infos,
        'geo_time_form': geo_time_form if geo_time_instance else None,
        'intersected_geometries': permit_request.intersected_geometries
        if permit_request.intersected_geometries != '' else None,
    }
