import json
import os.path

from django import template
from django.forms import modelformset_factory
from permits import services, forms, models
from django.utils.translation import gettext as _

from permits import forms, models, services

register = template.Library()


@register.inclusion_tag("permits/_permit_progressbar.html", takes_context=True)
def permit_progressbar(context, permit_request, active_step):
    steps = services.get_progressbar_steps(context["request"], permit_request)
    steps_states = {
        "steps": steps,
        "active_step": active_step,
    }

    return steps_states


@register.filter
def basename(value):
    return os.path.basename(value)


@register.inclusion_tag("permits/_permit_request_summary.html", takes_context=True)
def permit_request_summary(context, permit_request):

    objects_infos = services.get_permit_objects(permit_request)
    contacts = services.get_contacts_summary(permit_request)

    PermitRequestGeoTimeFormSet = modelformset_factory(
        models.PermitRequestGeoTime,
        form=forms.PermitRequestGeoTimeForm,
        extra=0,
    )

    geo_time_formset = PermitRequestGeoTimeFormSet(
        None,
        form_kwargs={"permit_request": permit_request, "disable_fields": True},
        queryset=permit_request.geo_time.all()
    )

    if permit_request.creditor_type is not None:
        creditor = models.ACTOR_TYPE_CHOICES[permit_request.creditor_type][1]
    elif permit_request.author.user and permit_request.creditor_type is None:
        creditor = (
            _("Auteur de la demande, ")
            + permit_request.author.user.first_name
            + " "
            + permit_request.author.user.last_name
        )
    else:
        creditor = ""

    return {
        'creditor': creditor,
        'contacts': contacts,
        'objects_infos': objects_infos,
        'geo_time_formset': geo_time_formset,
        'intersected_geometries': permit_request.intersected_geometries
        if permit_request.intersected_geometries != '' else None,
    }


@register.filter(name="json")
def json_(value):
    return json.dumps(value)
