import json
import os.path

from django import template
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.template.defaultfilters import floatformat
from django.utils.translation import gettext as _
from permits import forms, models, services
from datetime import datetime, timedelta, timezone
from django.utils.safestring import mark_safe

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


@register.filter
def human_field_value(value):
    if isinstance(value, bool):
        return _("Oui") if value else _("Non")
    elif isinstance(value, float):
        return floatformat(value, arg=-2)
    elif isinstance(value, list):
        return render_to_string("permits/_field_value_list.html", {"values": value})
    elif not value:
        return "-"

    return value


@register.simple_tag(takes_context=True)
def is_expired(context):
    if context["record"].max_validity is not None:
        ends_at_max = context["record"].ends_at_max
        prolongation_date = context["record"].prolongation_date
        permit_valid_until = (
            prolongation_date if context["record"].is_prolonged() else ends_at_max
        )
        if permit_valid_until:
            if (
                context["record"].is_prolonged()
                and datetime.now(timezone.utc) < permit_valid_until
            ):
                return mark_safe(
                    '<i class="fa fa-refresh fa-lg status2" title="Demande renouvelée"></i>'
                )
            elif datetime.now(timezone.utc) > permit_valid_until:
                return mark_safe(
                    '<i class="fa fa-exclamation-triangle fa-lg status0" title="Demande échue"></i>'
                )
            else:
                return ""
    else:
        return ""
