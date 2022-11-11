import dataclasses
import enum
import itertools

from constance import config
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from geocity.apps.forms.models import Form

from . import forms, models
from .utils import reverse_submission_url


@dataclasses.dataclass
class Step:
    name: str
    url: str
    completed: bool = False
    enabled: bool = False
    errors_count: int = 0


class StepType(enum.Enum):
    ADMINISTRATIVE_ENTITY = "administrative_entity"
    FORMS = "forms"
    FIELDS = "fields"
    GEO_TIME = "geo_time"
    APPENDICES = "appendices"
    CONTACTS = "contacts"
    SUBMIT = "submit"


# Required to be able to use the enum in Django templates
StepType.do_not_call_in_templates = True


def get_administrative_entity_step(submission):
    return Step(
        name=_("Entité"),
        url=reverse_submission_url(
            "submissions:submission_select_administrative_entity", submission
        )
        if submission
        else reverse("submissions:submission_select_administrative_entity"),
        completed=submission is not None,
        enabled=True,
    )


def get_forms_step(
    submission,
    enabled,
    user,
    current_site,
    restrict_to_categories=None,
    restrict_to_entities=None,
):
    restrict_to_categories = restrict_to_categories or []
    restrict_to_entities = restrict_to_entities or []

    # If there are default forms it means the forms can be automatically selected and so
    # the step shouldn’t be visible
    if submission:
        candidate_forms = Form.objects.all()
        # FIXME: should forms here be restricted to public forms?
        candidate_forms_filter = Q(pk__in=submission.administrative_entity.forms.all())

        if restrict_to_categories:
            candidate_forms_filter &= Q(category__in=restrict_to_categories)

        if restrict_to_entities:
            candidate_forms_filter &= Q(category__in=restrict_to_categories)

        candidate_forms_filter |= Q(pk__in=submission.forms.all())
    else:
        administrative_entities = Form.objects.get_administrative_entities_with_forms(
            user, current_site
        )

        candidate_forms = Form.objects.filter(
            administrative_entities__in=administrative_entities
        )
        candidate_forms_filter = Q()

        if restrict_to_entities:
            candidate_forms_filter &= Q(
                administrative_entities__in=administrative_entities
            )

        if restrict_to_categories:
            candidate_forms_filter &= Q(category__in=restrict_to_categories)

        if not user.has_perm("submissions:see_private_requests"):
            candidate_forms_filter &= Q(is_public=True)

    candidate_forms = candidate_forms.filter(candidate_forms_filter)

    if candidate_forms.count() <= 1:
        return None

    return Step(
        name=_("Objets"),
        url=(
            reverse_submission_url("submissions:submission_select_forms", submission)
            if submission
            else ""
        ),
        completed=enabled,
        enabled=enabled,
    )


def get_fields_step(submission, enabled):
    fields_form = (
        forms.FieldsForm(
            instance=submission, enable_required=True, disable_fields=True, data={}
        )
        if submission
        else None
    )
    fields_errors = len(fields_form.errors) if fields_form else 0
    fields_url = (
        reverse_submission_url("submissions:submission_fields", submission)
        if submission
        else ""
    )

    return Step(
        name=_("Détails"),
        url=fields_url,
        completed=enabled and fields_form and not fields_form.errors,
        errors_count=fields_errors,
        enabled=enabled,
    )


def get_geo_time_step(submission, enabled):
    geo_time_errors = (
        0 if submission is None or submission.get_geotime_objects().exists() else 1
    )
    geo_time_url = (
        reverse_submission_url("submissions:submission_geo_time", submission)
        if submission
        else ""
    )
    required_info = submission.get_geotime_required_info() if submission else set()

    if not (
        models.GeoTimeInfo.DATE in required_info
        or models.GeoTimeInfo.GEOMETRY in required_info
    ):
        return None

    return Step(
        name=get_geo_step_name_title(required_info)["step_name"],
        url=geo_time_url,
        completed=geo_time_errors == 0,
        errors_count=geo_time_errors,
        enabled=enabled,
    )


def get_geo_step_name_title(required_info):
    name_title = {}
    if models.GeoTimeInfo.DATE not in required_info:
        name_title["title"] = config.GEO_STEP
        name_title["step_name"] = _("Localisation")
    elif models.GeoTimeInfo.GEOMETRY not in required_info:
        name_title["title"] = config.TIME_STEP
        name_title["step_name"] = _("Planning")
    else:
        name_title["title"] = config.GEO_TIME_STEP
        name_title["step_name"] = _("Planning et localisation")

    return name_title


def get_appendices_step(submission, enabled):
    if submission and len(submission.get_appendices_fields_by_form()) == 0:
        return None

    appendices_url = (
        reverse_submission_url("submissions:submission_appendices", submission)
        if submission
        else ""
    )
    appendices_form = (
        forms.AppendicesForm(
            instance=submission, enable_required=True, disable_fields=True, data={}
        )
        if submission
        else None
    )
    appendices_errors = len(appendices_form.errors) if appendices_form else 0

    return Step(
        name=_("Documents"),
        url=appendices_url,
        completed=enabled and appendices_errors == 0,
        errors_count=appendices_errors,
        enabled=enabled,
    )


def get_contacts_step(submission, enabled):
    if submission and len(submission.get_contacts_types()) == 0:
        return None

    contact_errors = (
        len(submission.get_missing_required_contact_types()) if submission else 0
    )
    contacts_url = (
        reverse_submission_url("submissions:submission_contacts", submission)
        if submission
        else ""
    )
    return Step(
        name=_("Contacts"),
        url=contacts_url,
        enabled=enabled,
        errors_count=contact_errors,
        completed=contact_errors == 0,
    )


def get_submit_step(submission, enabled, total_errors):
    submit_url = (
        reverse_submission_url("submissions:submission_submit", submission)
        if submission
        else ""
    )

    return Step(
        name=_("Résumé et envoi"),
        url=submit_url,
        enabled=enabled,
        errors_count=total_errors,
        completed=total_errors == 0,
    )


def get_anonymous_steps(form_category, user, submission, current_site):
    has_forms = submission.forms.exists()

    objects_step = get_forms_step(
        submission=submission,
        enabled=not has_forms,
        user=user,
        current_site=current_site,
        restrict_to_categories=[form_category],
    )

    if objects_step:
        objects_step.completed = has_forms

    steps = {
        StepType.FORMS: objects_step,
        StepType.FIELDS: get_fields_step(submission=submission, enabled=has_forms),
        StepType.GEO_TIME: get_geo_time_step(submission=submission, enabled=has_forms),
        StepType.APPENDICES: get_appendices_step(
            submission=submission, enabled=has_forms
        ),
        StepType.CONTACTS: get_contacts_step(submission=submission, enabled=has_forms),
    }

    total_errors = sum([step.errors_count for step in steps.values() if step])
    steps[StepType.SUBMIT] = get_submit_step(
        submission=submission,
        enabled=has_forms,
        total_errors=total_errors,
    )

    return {step_type: step for step_type, step in steps.items() if step is not None}


def get_progress_bar_steps(request, submission):
    """
    Return a dict of `Step` items that can be used to track the user progress through
    the submission wizard. The dict only contains reachable steps (which don’t
    necessarily have a `url` though, eg. before selecting the administrative entity).
    """
    has_forms = submission.forms.exists() if submission else False
    current_site = get_current_site(request)
    entityfilter = (
        request.session["entityfilter"] if "entityfilter" in request.session else []
    )

    if entityfilter:
        entities_by_tag = models.Form.objects.get_administrative_entities_with_forms(
            request.user, current_site
        ).filter_by_tags(
            entityfilter,
        )
    else:
        entities_by_tag = None

    selected_categories = None
    if entities_by_tag:
        if "typefilter" in request.session and len(entities_by_tag) == 1:
            categories_by_tag = (
                models.FormCategory.objects.filter_by_tags(
                    request.session["typefilter"]
                )
                .filter(forms__administrative_entities__in=entities_by_tag)
                .values_list("pk", flat=True)
            )
            if len(categories_by_tag) == 1:
                selected_categories = [str(categories_by_tag[0])]

    all_steps = {
        StepType.ADMINISTRATIVE_ENTITY: get_administrative_entity_step(submission),
        StepType.FORMS: get_forms_step(
            submission=submission,
            enabled=has_forms,
            user=request.user,
            current_site=current_site,
            restrict_to_categories=selected_categories,
            restrict_to_entities=entities_by_tag,
        ),
        StepType.FIELDS: get_fields_step(submission=submission, enabled=has_forms),
        StepType.GEO_TIME: get_geo_time_step(submission=submission, enabled=has_forms),
        StepType.APPENDICES: get_appendices_step(
            submission=submission, enabled=has_forms
        ),
        StepType.CONTACTS: get_contacts_step(submission=submission, enabled=has_forms),
    }

    total_errors = sum([step.errors_count for step in all_steps.values() if step])
    all_steps[StepType.SUBMIT] = get_submit_step(
        submission=submission,
        enabled=has_forms,
        total_errors=total_errors,
    )

    return {
        step_type: step for step_type, step in all_steps.items() if step is not None
    }


def get_previous_step(steps, current_step):
    """
    Return the previous step in the list or raise `IndexError` if there’s no such
    step.
    """
    return list(
        itertools.takewhile(lambda step: step[0] != current_step, steps.items())
    )[-1][1]


def get_next_step(steps, current_step):
    """
    Return the next step in the list or raise `IndexError` if there’s no such
    step.
    """
    return list(
        itertools.dropwhile(lambda step: step[0] != current_step, steps.items())
    )[1][1]
