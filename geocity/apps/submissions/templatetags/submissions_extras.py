import json
import os.path
from datetime import date, datetime, timezone

from django import template
from django.forms import modelformset_factory
from django.template.defaultfilters import floatformat
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from geocity.apps.accounts.models import PermitDepartment
from geocity.apps.submissions import forms, models, permissions

register = template.Library()


@register.inclusion_tag("submissions/_submission_progressbar.html", takes_context=True)
def submission_progressbar(context, steps, active_step):
    return (
        {}
        if context["user"].userprofile.is_temporary
        else {
            "steps": steps,
            "active_step": active_step,
        }
    )


@register.filter
def basename(value):
    return os.path.basename(value)


def get_contacts_summary(submission):
    contacts = [
        (
            models.ContactType.objects.get(id=contact["contact_form"].value()).name,
            [
                (field.label, field.value())
                for field in contact
                if field.name not in {"id", "contact_form"}
            ],
        )
        for contact in forms.get_submission_contacts_formset_initiated(submission)
    ]

    return contacts


@register.inclusion_tag("submissions/_submission_summary.html", takes_context=True)
def submission_summary(context, submission):
    forms_infos = forms.get_submission_forms(submission)
    contacts = get_contacts_summary(submission)
    requires_payment = submission.requires_payment()
    submission_price = submission.get_submission_price()
    documents = submission.get_complementary_documents(user=context.request.user)
    is_validator = permissions.has_permission_to_validate_submission(
        context.request.user, submission
    )

    SubmissionGeoTimeFormSet = modelformset_factory(
        models.SubmissionGeoTime,
        form=forms.SubmissionGeoTimeForm,
        extra=0,
    )

    geo_time_formset = SubmissionGeoTimeFormSet(
        None,
        form_kwargs={"submission": submission, "disable_fields": True},
        queryset=submission.geo_time.all(),
    )

    creditor = ""
    if requires_payment:
        if submission.creditor_type is not None:
            creditor = submission.creditor_type.name
        elif submission.author and submission.creditor_type is None:
            creditor = (
                _("Auteur de la demande, ")
                + submission.author.first_name
                + " "
                + submission.author.last_name
            )

    selected_price = (
        {
            "text": submission_price.text,
            "amount": submission_price.amount,
            "currency": submission_price.currency,
        }
        if submission_price
        else None
    )

    return {
        "user": context.request.user,
        "author": submission.author,
        "creditor": creditor,
        "contacts": contacts,
        "forms_infos": forms_infos,
        "documents": documents,
        "geo_time_formset": geo_time_formset,
        "requires_payment": requires_payment,
        "selected_price": selected_price,
        "is_validator": is_validator,
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
    elif isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    elif isinstance(value, list):
        return render_to_string("submissions/_field_value_list.html", {"values": value})
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


@register.simple_tag(takes_context=True)
def can_always_be_updated(context):
    if context["record"] is not None:
        return permissions.can_always_be_updated(
            context["request"].user, context["record"]
        )


@register.simple_tag(takes_context=True)
def can_download_archive(context):
    return permissions.can_download_archive(
        context["user"], context["record"].archivist
    )


@register.simple_tag(takes_context=True)
def can_archive(context):
    department = PermitDepartment.objects.filter(
        group__in=context["user"].groups.all()
    ).first()
    return context["user"].is_superuser or (
        department is not None
        and (department.is_backoffice or department.is_integrator_admin)
    )


@register.simple_tag(takes_context=True)
def can_revert_refund_transaction(context):
    return permissions.can_revert_refund_transaction(context["user"], context["record"])


@register.simple_tag(takes_context=True)
def can_refund_transaction(context):
    return permissions.can_refund_transaction(context["user"], context["record"])


@register.inclusion_tag("submissions/_directives_and_legal.html", takes_context=True)
def directives_and_legal(context, submission):

    return {
        "directives": submission.get_submission_directives(),
    }


@register.inclusion_tag(
    "submissions/_directives_and_legal_cta.html", takes_context=True
)
def directives_and_legal_cta(context, submission):

    return {
        "directives": submission.get_submission_directives(),
    }
