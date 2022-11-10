import dataclasses
import enum
import itertools
import urllib

from constance import config
from django.contrib.sites.shortcuts import get_current_site
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


def get_forms_step(submission, enabled, form_categories, user, typefilter):
    # If there are default forms it means the forms can be automatically selected and so
    # the step shouldn’t be visible

    if submission:
        selected_categories = form_categories or submission.forms.values_list(
            "category", flat=True
        )
        candidate_forms = (
            models.Form.objects.filter(category__in=selected_categories)
            if selected_categories
            else submission.administrative_entity.forms.all()
        ).distinct()

        if (
            models.Form.objects.get_default_forms(
                submission.administrative_entity,
                user,
                form_categories=selected_categories or None,
            )
            # Also check if the candidates categories would all result in a single form
            # (which will anyway get automatically selected)
            or candidate_forms.count() <= 1
        ):
            return None

    # If the user is editing a permit request and the administrative entity only has 1
    # works type, there won’t be a works type step, so the works object step should have
    # it in the URL
    # return None
    if submission and not form_categories:
        if user.has_perm("submissions.see_private_requests"):
            administrative_entity_categories = (
                submission.administrative_entity.forms.values_list(
                    "category", flat=True
                ).distinct()
            )
        else:
            administrative_entity_categories = (
                submission.administrative_entity.forms.filter(is_public=True)
                .values_list("category", flat=True)
                .distinct()
            )

        if len(administrative_entity_categories) == 1:
            form_categories = administrative_entity_categories

        if typefilter:
            filtered_works_type = (
                models.FormCategory.objects.filter_by_tags(typefilter)
                .values_list("id", flat=True)
                .distinct()
            )

            if filtered_works_type.count() == 1:
                form_categories = filtered_works_type

    form_categories_qs = (
        urllib.parse.urlencode(
            {"types": form_categories},
            doseq=True,
        )
        if form_categories
        else ""
    )

    return Step(
        name=_("Objets"),
        url=(
            reverse_submission_url("submissions:submission_select_forms", submission)
            + (f"?{form_categories_qs}" if form_categories_qs else "")
        )
        if submission
        else "",
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


def get_anonymous_steps(form_category, user, submission):
    has_forms = submission.forms.exists()

    objects_step = get_forms_step(
        submission=submission,
        enabled=not has_forms,
        form_categories=[form_category],
        user=user,
        typefilter=[form_category],
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
    selected_categories = request.GET.getlist("types")
    entityfilter = (
        request.session["entityfilter"] if "entityfilter" in request.session else []
    )
    single_entity_for_site = False
    entities_by_tag = None
    current_site = get_current_site(request)
    entities_for_site = Form.objects.get_administrative_entities_with_forms(
        request.user, current_site
    )
    single_entity_for_site = len(entities_for_site) == 1

    # Don't care about filter if there is only one entity for the current site
    if entityfilter and not single_entity_for_site:
        entities_by_tag = Form.objects.get_administrative_entities_with_forms(
            request.user, current_site
        ).filter_by_tags(
            entityfilter,
        )

    # Get work objects types if there is only one entity filtered
    # Skipped if only one entity for site
    if entities_by_tag:
        if (
            not selected_categories
            and "typefilter" in request.session
            and len(entities_by_tag) == 1
        ):
            forms_by_category = (
                models.FormCategory.objects.filter_by_tags(
                    request.session["typefilter"]
                )
                .filter(forms__administrative_entities__in=entities_by_tag)
                .values_list("pk", flat=True)
            )
            if len(forms_by_category) == 1:
                selected_categories = [str(forms_by_category[0])]

    # Get forms if there is only one entity filtered
    if single_entity_for_site and not selected_categories:
        form_categories_for_single_entity = models.FormCategory.objects.filter(
            forms__administrative_entities__in=entities_for_site
        ).values_list("pk", flat=True)
        if len(form_categories_for_single_entity) == 1:
            selected_categories = [str(form_categories_for_single_entity[0])]

    all_steps = {
        StepType.ADMINISTRATIVE_ENTITY: get_administrative_entity_step(submission),
        StepType.FORMS: get_forms_step(
            submission=submission,
            enabled=has_forms,
            form_categories=selected_categories,
            user=request.user,
            typefilter=request.session["typefilter"]
            if "typefilter" in request.session
            else [],
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
