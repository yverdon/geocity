import json
import os.path

from django import template
from django.forms import modelformset_factory
from django.utils.translation import gettext as _
from permits import forms, models, services

register = template.Library()


@register.inclusion_tag("permits/_permit_progressbar.html", takes_context=True)
def permit_progressbar(context, steps, active_step):
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
    requires_payment = services.permit_requests_has_paid_wot(permit_request)

    PermitRequestGeoTimeFormSet = modelformset_factory(
        models.PermitRequestGeoTime, form=forms.PermitRequestGeoTimeForm, extra=0,
    )

    geo_time_formset = PermitRequestGeoTimeFormSet(
        None,
        form_kwargs={"permit_request": permit_request, "disable_fields": True},
        queryset=permit_request.geo_time.all(),
    )

    creditor = ""
    if requires_payment:
        if permit_request.creditor_type is not None:
            creditor = permit_request.get_creditor_type_display()
        elif permit_request.author.user and permit_request.creditor_type is None:
            creditor = (
                _("Auteur de la demande, ")
                + permit_request.author.user.first_name
                + " "
                + permit_request.author.user.last_name
            )

    return {
        "creditor": creditor,
        "contacts": contacts,
        "objects_infos": objects_infos,
        "geo_time_formset": geo_time_formset,
        "intersected_geometries": permit_request.intersected_geometries
        if permit_request.intersected_geometries != ""
        else None,
        "requires_payment": requires_payment,
    }


@register.filter(name="json")
def json_(value):
    return json.dumps(value)
