import logging
import mimetypes
import os
import urllib.parse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.db import transaction
from django.db.models import Prefetch
from django.forms import modelformset_factory
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import View
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin, SingleTableView

import requests

from . import fields, filters, forms, models, services, tables
from .exceptions import BadPermitRequestStatus

logger = logging.getLogger(__name__)


def user_has_permitauthor(user):
    try:
        user.permitauthor
    except models.PermitAuthor.DoesNotExist:
        return False

    return True


def get_permit_request_for_edition(user, permit_request_id):

    allowed_statuses = {
        models.PermitRequest.STATUS_DRAFT,
        models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
        models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
    }

    permit_request = services.get_permit_request_for_user_or_404(
        user, permit_request_id, statuses=allowed_statuses,
    )

    can_pilot_edit_permit_request = services.can_edit_permit_request(
        user, permit_request
    )

    if (
        permit_request.status == models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
        and not can_pilot_edit_permit_request
    ):
        raise BadPermitRequestStatus(
            permit_request,
            [
                models.PermitRequest.STATUS_DRAFT,
                models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
            ],
        )

    return permit_request


def redirect_bad_status_to_detail(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadPermitRequestStatus as e:
            return redirect(
                "permits:permit_request_detail", permit_request_id=e.permit_request.pk
            )

    return inner


def disable_form(form):
    for field in form.fields.values():
        field.disabled = True

    form.disabled = True

    return form


def progress_bar_context(request, permit_request, current_step_type):
    steps = services.get_progress_bar_steps(
        request=request, permit_request=permit_request
    )

    if current_step_type not in steps:
        raise Http404()

    try:
        previous_step = services.get_previous_step(steps, current_step_type)
    except IndexError:
        previous_step = None

    return {"steps": steps, "previous_step": previous_step}


@method_decorator(login_required, name="dispatch")
class PermitRequestDetailView(View):

    actions = models.ACTIONS

    def dispatch(self, request, *args, **kwargs):
        self.permit_request = services.get_permit_request_for_user_or_404(
            request.user, kwargs["permit_request_id"]
        )

        if (
            self.permit_request.is_draft()
            and self.permit_request.author.user == request.user
        ):
            return redirect(
                "permits:permit_request_select_administrative_entity",
                permit_request_id=self.permit_request.pk,
            )

        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context):

        return render(self.request, "permits/permit_request_detail.html", context)

    def get_context_data(self, **kwargs):

        current_actions = services.get_actions_for_administrative_entity(
            self.permit_request
        )

        forms = {action: self.get_form_for_action(action) for action in current_actions}
        available_actions = [action for action in current_actions if forms[action]]

        try:
            active_forms = [
                action
                for action in available_actions
                if not getattr(forms[action], "disabled", False)
            ]
            if "poke" in active_forms and "validate" in active_forms:
                active_form = active_forms[active_forms.index("validate")]
            else:
                active_form = active_forms[0]

        except IndexError:
            active_form = available_actions[-1] if len(available_actions) > 0 else None

        kwargs["has_validations"] = self.permit_request.has_validations()

        if forms.get(models.ACTION_POKE):
            kwargs[
                "nb_pending_validations"
            ] = self.permit_request.get_pending_validations().count()
            kwargs["validations"] = self.permit_request.validations.select_related(
                "department", "department__group"
            )
        else:
            kwargs["nb_pending_validations"] = 0

            if services.can_validate_permit_request(
                self.request.user, self.permit_request
            ):
                kwargs["validations"] = self.permit_request.validations.select_related(
                    "department", "department__group"
                )
            else:
                kwargs["validations"] = []

        return {
            **kwargs,
            **{
                "permit_request": self.permit_request,
                "forms": forms,
                "active_form": active_form,
                "has_permission_to_classify": services.has_permission_to_classify_permit_request(
                    self.request.user, self.permit_request
                ),
                "can_classify": services.can_classify_permit_request(
                    self.request.user, self.permit_request
                ),
                "print_templates": services.get_permit_request_print_templates(
                    self.permit_request
                ),
            },
        }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Instanciate the form matching the submitted POST `action`, checking if the user has the permissions to use it,
        save it, and call the related submission function.
        """

        action = request.POST.get("action")
        if action not in models.ACTIONS:
            return HttpResponse(status=400)

        form = self.get_form_for_action(action, data=request.POST)
        if not form:
            raise PermissionDenied
        elif getattr(form, "disabled", False):
            raise SuspiciousOperation

        if form.is_valid():
            return self.handle_form_submission(form, action)

        # Replace unbound form by bound form in the context
        context = self.get_context_data()
        context["forms"][action] = form

        return self.render_to_response(context)

    def get_form_for_action(self, action, data=None):
        actions_forms = {
            models.ACTION_AMEND: self.get_amend_form,
            models.ACTION_REQUEST_VALIDATION: self.get_request_validation_form,
            models.ACTION_VALIDATE: self.get_validation_form,
            models.ACTION_POKE: self.get_poke_form,
        }

        return actions_forms[action](data=data)

    def get_amend_form(self, data=None):

        if services.has_permission_to_amend_permit_request(
            self.request.user, self.permit_request
        ):
            # Only set the `status` default value if it's submitted for validation, to prevent accidentally resetting
            # the status
            initial = (
                {"status": models.PermitRequest.STATUS_PROCESSING}
                if self.permit_request.status
                == models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
                else {}
            )

            form = forms.PermitRequestAdditionalInformationForm(
                instance=self.permit_request, initial=initial, data=data
            )

            if not services.can_amend_permit_request(
                self.request.user, self.permit_request
            ):
                disable_form(form)

            return form

        return None

    def get_request_validation_form(self, data=None):
        if services.has_permission_to_amend_permit_request(
            self.request.user, self.permit_request
        ):
            form = forms.PermitRequestValidationDepartmentSelectionForm(
                instance=self.permit_request, data=data
            )

            if not services.can_amend_permit_request(
                self.request.user, self.permit_request
            ):
                disable_form(form)

            return form

        return None

    def get_validation_form(self, data=None):
        if not services.has_permission_to_validate_permit_request(
            self.request.user, self.permit_request
        ):
            return None

        departments = services.get_user_departments(self.request.user)

        try:
            validation, *rest = list(
                self.permit_request.validations.filter(department__in=departments)
            )
        # User is not part of the requested departments
        except ValueError:
            return None

        if rest:
            logger.error(
                "User %s is a member of more than 1 validation group for permit request %s. This is not"
                " implemented yet.",
                self.request.user,
                self.permit_request,
            )
            return None

        form = forms.PermitRequestValidationForm(instance=validation, data=data)
        if not services.can_validate_permit_request(
            self.request.user, self.permit_request
        ):
            disable_form(form)

        return form

    def get_poke_form(self, data=None):
        if services.has_permission_to_poke_permit_request(
            self.request.user, self.permit_request
        ):
            form = forms.PermitRequestValidationPokeForm(
                instance=self.permit_request, request=self.request, data=data
            )
            if not services.can_poke_permit_request(
                self.request.user, self.permit_request
            ):
                disable_form(form)

            return form

        return None

    def handle_form_submission(self, form, action):
        if action == models.ACTION_AMEND:
            return self.handle_amend_form_submission(form)
        elif action == models.ACTION_REQUEST_VALIDATION:
            return self.handle_request_validation_form_submission(form)
        elif action == models.ACTION_VALIDATE:
            return self.handle_validation_form_submission(form)
        elif action == models.ACTION_POKE:
            return self.handle_poke(form)

    def handle_amend_form_submission(self, form):

        form.save()
        success_message = (
            _("La demande #%s a bien été complétée par le service pilote.")
            % self.permit_request.pk
        )

        if form.instance.status == models.PermitRequest.STATUS_AWAITING_SUPPLEMENT:
            success_message += (
                " "
                + _(
                    "Le statut de la demande a été passé à en attente de compléments. Vous devez maintenant"
                    " contacter le requérant par email (%s) afin de lui demander de fournir les informations manquantes."
                )
                % self.permit_request.author.user.email
            )

        messages.success(self.request, success_message)

        if "save_continue" in self.request.POST:

            return redirect(
                "permits:permit_request_detail",
                permit_request_id=self.permit_request.pk,
            )
        else:
            return redirect("permits:permit_requests_list")

    def handle_request_validation_form_submission(self, form):
        services.request_permit_request_validation(
            self.permit_request,
            form.cleaned_data["departments"],
            self.request.build_absolute_uri,
        )
        messages.success(
            self.request,
            _("La demande #%s a bien été transmise pour validation.")
            % self.permit_request.pk,
        )
        return redirect("permits:permit_requests_list")

    def handle_validation_form_submission(self, form):

        form.instance.validated_at = timezone.now()
        form.instance.validated_by = self.request.user
        validation = form.save()

        if (
            validation.validation_status
            == models.PermitRequestValidation.STATUS_APPROVED
        ):
            validation_message = _("La demande a bien été validée.")
        elif (
            validation.validation_status
            == models.PermitRequestValidation.STATUS_REJECTED
        ):
            validation_message = _("La demande a bien été refusée.")
        else:
            validation_message = _("Les commentaires ont été enregistrés.")

        messages.success(self.request, validation_message)

        return redirect("permits:permit_requests_list")

    def handle_poke(self, form):
        validations = form.save()

        message = ngettext(
            "%s rappel a bien été envoyé.",
            "%s rappels ont bien été envoyés",
            len(validations),
        ) % (len(validations))
        messages.success(self.request, message)

        return redirect("permits:permit_requests_list")


def permit_request_print(request, permit_request_id, template_id):
    permit_request = services.get_permit_request_for_user_or_404(
        request.user, permit_request_id
    )
    template = get_object_or_404(models.QgisTemplate.objects, pk=template_id)

    values = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetPrint",
        "FORMAT": "pdf",
        "TRANSPARENT": "true",
        "SRS": "EPSG:2056",
        "DPI": "150",
        "SERVICE": "WMS",
        "MAP": "/qgis_templates/" + str(template.qgis_project_file),
        "TEMPLATE": template.qgis_print_template_name,
        "ATLAS_PK": permit_request_id,
        "LAYERS": template.qgis_layers,
    }

    qgisserver_url = "http://qgisserver/ogc/?" + urllib.parse.urlencode(values)
    qgisserver_response = requests.get(
        qgisserver_url, headers={"Accept": "application/pdf"}, stream=True
    )

    if not qgisserver_response:
        assert False, qgisserver_response.content
        # FIXME return a proper error here
        return HttpResponse(_("Une erreur est survenue lors de l'impression"))

    return StreamingHttpResponse(
        qgisserver_response.iter_content(chunk_size=128), content_type="application/pdf"
    )


@redirect_bad_status_to_detail
@login_required
@user_passes_test(user_has_permitauthor)
def permit_request_select_administrative_entity(request, permit_request_id=None):
    if permit_request_id:
        permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    else:
        permit_request = None

    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.ADMINISTRATIVE_ENTITY,
    )

    if request.method == "POST":
        administrative_entity_form = forms.AdministrativeEntityForm(
            instance=permit_request, data=request.POST, user=request.user
        )

        if administrative_entity_form.is_valid():
            permit_request = administrative_entity_form.save(
                author=request.user.permitauthor
            )

            works_object_types = services.get_default_works_object_types(
                administrative_entity=permit_request.administrative_entity,
                user=request.user,
            )
            if works_object_types:
                services.set_works_object_types(
                    permit_request=permit_request,
                    new_works_object_types=works_object_types,
                )

            steps = services.get_progress_bar_steps(
                request=request, permit_request=permit_request
            )

            return redirect(
                services.get_next_step(steps, models.StepType.ADMINISTRATIVE_ENTITY).url
            )
    else:
        administrative_entity_form = forms.AdministrativeEntityForm(
            instance=permit_request, user=request.user
        )

    return render(
        request,
        "permits/permit_request_select_administrative_entity.html",
        {
            "form": administrative_entity_form,
            "permit_request": permit_request,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
def permit_request_select_types(request, permit_request_id):
    """
    Step to select works types (eg. demolition). No permit request is created at this step since we only store (works
    object, works type) couples in the database.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.WORKS_TYPES,
    )

    if request.method == "POST":
        works_types_form = forms.WorksTypesForm(
            data=request.POST, instance=permit_request, user=request.user
        )
        if works_types_form.is_valid():
            redirect_kwargs = {"permit_request_id": permit_request_id}
            selected_works_types = [
                obj.pk for obj in works_types_form.cleaned_data["types"]
            ]

            with transaction.atomic():
                works_types_form.save()

                works_object_types = services.get_default_works_object_types(
                    administrative_entity=permit_request.administrative_entity,
                    user=request.user,
                    works_types=selected_works_types,
                )
                if works_object_types:
                    services.set_works_object_types(
                        permit_request=permit_request,
                        new_works_object_types=works_object_types,
                    )
                    steps = services.get_progress_bar_steps(
                        request=request, permit_request=permit_request
                    )

                    return redirect(
                        services.get_next_step(steps, models.StepType.WORKS_TYPES).url
                    )

            return redirect(
                reverse("permits:permit_request_select_objects", kwargs=redirect_kwargs)
                + "?"
                + urllib.parse.urlencode({"types": selected_works_types}, doseq=True,)
            )
    else:
        works_types_form = forms.WorksTypesForm(
            instance=permit_request, user=request.user
        )

    return render(
        request,
        "permits/permit_request_select_types.html",
        {
            "works_types_form": works_types_form,
            "permit_request": permit_request,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
def permit_request_select_objects(request, permit_request_id):
    """
    Step to select works objects. This view supports either editing an existing permit request (if `permit_request_id`
    is set) or creating a new permit request.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.WORKS_OBJECTS,
    )

    if request.GET:
        works_types_form = forms.WorksTypesForm(
            data=request.GET, instance=permit_request, user=request.user
        )
        if works_types_form.is_valid():
            works_types = works_types_form.cleaned_data["types"]
        else:
            try:
                return redirect(steps_context["steps"][models.StepType.WORKS_TYPES].url)
            except KeyError:
                raise Http404
    else:
        if not permit_request.works_object_types.exists():
            try:
                return redirect(steps_context["steps"][models.StepType.WORKS_TYPES].url)
            except KeyError:
                raise Http404

        works_types = models.WorksType.objects.none()

    # Add the permit request works types to the ones in the querystring
    works_types = works_types.union(
        services.get_permit_request_works_types(permit_request)
    ).distinct()

    if request.method == "POST":
        works_objects_form = forms.WorksObjectsForm(
            data=request.POST,
            instance=permit_request,
            works_types=works_types,
            user=request.user,
        )

        if works_objects_form.is_valid():
            permit_request = works_objects_form.save()
            steps = services.get_progress_bar_steps(
                request=request, permit_request=permit_request
            )

            return redirect(
                services.get_next_step(steps, models.StepType.WORKS_OBJECTS).url
            )
    else:
        works_objects_form = forms.WorksObjectsForm(
            instance=permit_request, works_types=works_types, user=request.user
        )

    return render(
        request,
        "permits/permit_request_select_objects.html",
        {
            "works_objects_form": works_objects_form,
            "permit_request": permit_request,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
def permit_request_properties(request, permit_request_id):
    """
    Step to input properties values for the given permit request.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.PROPERTIES,
    )

    if request.method == "POST":
        # Disable `required` fields validation to allow partial save
        form = forms.WorksObjectsPropertiesForm(
            instance=permit_request, data=request.POST, enable_required=False
        )

        if form.is_valid():
            form.save()

            return redirect(
                services.get_next_step(
                    steps_context["steps"], models.StepType.PROPERTIES
                ).url
            )
    else:
        form = forms.WorksObjectsPropertiesForm(
            instance=permit_request, enable_required=False
        )

    fields_by_object_type = form.get_fields_by_object_type()

    return render(
        request,
        "permits/permit_request_properties.html",
        {
            "permit_request": permit_request,
            "object_types": fields_by_object_type,
            "permit_request_form": form,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
def permit_request_appendices(request, permit_request_id):
    """
    Step to upload appendices for the given permit request.
    """
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.APPENDICES,
    )

    if request.method == "POST":
        form = forms.WorksObjectsAppendicesForm(
            instance=permit_request,
            data=request.POST,
            files=request.FILES,
            enable_required=False,
        )

        if form.is_valid():
            form.save()
            return redirect(
                services.get_next_step(
                    steps_context["steps"], models.StepType.APPENDICES
                ).url
            )
    else:
        form = forms.WorksObjectsAppendicesForm(
            instance=permit_request, enable_required=False
        )

    fields_by_object_type = form.get_fields_by_object_type()

    return render(
        request,
        "permits/permit_request_appendices.html",
        {
            "permit_request": permit_request,
            "object_types": fields_by_object_type,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
def permit_request_actors(request, permit_request_id):
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.ACTORS,
    )

    creditorform = forms.PermitRequestCreditorForm(
        request.POST or None, instance=permit_request
    )

    if request.method == "POST":
        formset = services.get_permitactorformset_initiated(
            permit_request, data=request.POST
        )
        if formset.is_valid() and creditorform.is_valid():
            for form in formset:
                if form.has_changed():
                    form.save(permit_request=permit_request)
            models.PermitRequest.objects.filter(pk=permit_request_id).update(
                creditor_type=creditorform.instance.creditor_type
            )

            return redirect(
                services.get_next_step(
                    steps_context["steps"], models.StepType.ACTORS
                ).url
            )
    else:

        formset = services.get_permitactorformset_initiated(permit_request)

    return render(
        request,
        "permits/permit_request_actors.html",
        {
            "formset": formset,
            "creditorform": creditorform,
            "permit_request": permit_request,
            **steps_context,
        },
    )


@login_required
def permit_request_geo_time(request, permit_request_id):
    permit_request = services.get_permit_request_for_user_or_404(
        request.user, permit_request_id
    )
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.GEO_TIME,
    )

    PermitRequestGeoTimeFormSet = modelformset_factory(
        models.PermitRequestGeoTime,
        form=forms.PermitRequestGeoTimeForm,
        extra=0,
        min_num=1,
        can_delete=True,
    )

    formset = PermitRequestGeoTimeFormSet(
        request.POST if request.method == "POST" else None,
        form_kwargs={"permit_request": permit_request},
        queryset=permit_request.geo_time.all(),
    )

    if request.method == "POST":
        if formset.is_valid():
            with transaction.atomic():
                formset.save()

                for obj in formset.deleted_objects:
                    if obj.pk:
                        obj.delete()

            return redirect(
                services.get_next_step(
                    steps_context["steps"], models.StepType.GEO_TIME
                ).url
            )

    title_step = services.get_geo_step_name_title(
        services.get_geotime_required_info(permit_request)
    )
    return render(
        request,
        "permits/permit_request_geo_time.html",
        {
            "formset": formset,
            "permit_request": permit_request,
            "geo_title": title_step["title"],
            "geo_step": title_step["step_name"],
            **steps_context,
        },
    )


@login_required
def permit_request_media_download(request, property_value_id):
    """
    Send the file referenced by the given property value.
    """
    property_value = get_object_or_404(
        models.WorksObjectPropertyValue.objects.filter(
            property__input_type=models.WorksObjectProperty.INPUT_TYPE_FILE
        ),
        pk=property_value_id,
        works_object_type_choice__permit_request__in=services.get_permit_requests_list_for_user(
            request.user
        ),
    )
    file = services.get_property_value(property_value)
    mime_type, encoding = mimetypes.guess_type(file.name)

    return StreamingHttpResponse(file, content_type=mime_type)


@method_decorator(login_required, name="dispatch")
class PermitRequestList(SingleTableMixin, FilterView):
    paginate_by = int(os.environ["PAGINATE_BY"])
    template_name = "permits/permit_requests_list.html"

    def get_queryset(self):
        return (
            services.get_permit_requests_list_for_user(self.request.user)
            .prefetch_related(
                Prefetch(
                    "works_object_types",
                    queryset=models.WorksObjectType.objects.select_related(
                        "works_type", "works_object"
                    ),
                )
            )
            .order_by("-created_at")
        )

    def is_department_user(self):
        return self.request.user.groups.filter(permitdepartment__isnull=False).exists()

    def get_table_class(self):
        return (
            tables.DepartmentPermitRequestsTable
            if self.is_department_user()
            else tables.OwnPermitRequestsTable
        )

    def get_filterset_class(self):
        return (
            filters.DepartmentPermitRequestFilterSet
            if self.is_department_user()
            else filters.OwnPermitRequestFilterSet
        )


@method_decorator(login_required, name="dispatch")
class PermitExportView(ExportMixin, SingleTableView):
    table_class = tables.OwnPermitRequestsTable
    template_name = "django_tables2/bootstrap.html"

    def get_queryset(self):
        return (
            services.get_permit_requests_list_for_user(self.request.user)
            .prefetch_related(
                Prefetch(
                    "works_object_types",
                    queryset=models.WorksObjectType.objects.select_related(
                        "works_type", "works_object"
                    ),
                )
            )
            .order_by("-created_at")
        )

    exclude_columns = ("actions",)


@redirect_bad_status_to_detail
@login_required
def permit_request_submit(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    incomplete_steps = [
        step.url
        for step in services.get_progress_bar_steps(request, permit_request).values()
        if step.errors_count and step.url
    ]

    if request.method == "POST":
        if incomplete_steps:
            raise SuspiciousOperation

        services.submit_permit_request(permit_request, request.build_absolute_uri)
        return redirect("permits:permit_requests_list")

    return render(
        request,
        "permits/permit_request_submit.html",
        {
            "permit_request": permit_request,
            "legal_document_exists": os.path.exists(
                permit_request.administrative_entity.legal_document.path
            ),
            "incomplete_steps": incomplete_steps,
            **progress_bar_context(
                request=request,
                permit_request=permit_request,
                current_step_type=models.StepType.SUBMIT,
            ),
        },
    )


@redirect_bad_status_to_detail
@login_required
def permit_request_submit_confirmed(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    incomplete_steps = [
        step.url
        for step in services.get_progress_bar_steps(request, permit_request).values()
        if step.errors_count and step.url
    ]

    if incomplete_steps:
        raise SuspiciousOperation

    services.submit_permit_request(permit_request, request.build_absolute_uri)
    return redirect("permits:permit_requests_list")


@redirect_bad_status_to_detail
@login_required
def permit_request_delete(request, permit_request_id):
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    if request.method == "POST":
        permit_request.delete()

        return redirect("permits:permit_requests_list")

    return render(
        request,
        "permits/permit_request_delete.html",
        {"permit_request": permit_request},
    )


def permit_request_approve(request, permit_request_id):
    return permit_request_classify(request, permit_request_id, approve=True)


def permit_request_reject(request, permit_request_id):
    return permit_request_classify(request, permit_request_id, approve=False)


@login_required
@permission_required("permits.classify_permit_request")
def permit_request_classify(request, permit_request_id, approve):

    permit_request = services.get_permit_request_for_user_or_404(
        request.user,
        permit_request_id,
        statuses=[
            models.PermitRequest.STATUS_AWAITING_VALIDATION,
            models.PermitRequest.STATUS_PROCESSING,
        ],
    )
    if not services.can_classify_permit_request(request.user, permit_request):
        raise Http404

    initial = {
        "status": (
            models.PermitRequest.STATUS_APPROVED
            if approve
            else models.PermitRequest.STATUS_REJECTED
        )
    }
    title = (
        _("Approbation de la demande #%s") if approve else _("Refus de la demande #%s")
    ) % permit_request.pk

    if request.method == "POST":
        classify_form = forms.PermitRequestClassifyForm(
            instance=permit_request,
            data=request.POST,
            files=request.FILES,
            initial=initial,
        )

        if classify_form.is_valid():
            classify_form.save()
            return redirect("permits:permit_requests_list")
    else:
        classify_form = forms.PermitRequestClassifyForm(
            instance=permit_request, initial=initial
        )

    return render(
        request,
        "permits/permit_request_classify.html",
        {
            "permit_request": permit_request,
            "approve": approve,
            "form": classify_form,
            "title": title,
        },
    )


def permit_request_file_download(request, path):
    """
    Securely download the permit request file at the given `path`. The path must start with the permit request id, such
    as returned by the `PermitRequestFieldFile`.

    If the user doesn't have access to the permit request identified by the given id, return an HTTP 404 error.
    """
    try:
        permit_request_id, _ = path.split("/", maxsplit=1)
    except ValueError:
        raise Http404

    services.get_permit_request_for_user_or_404(request.user, permit_request_id)

    mime_type, encoding = mimetypes.guess_type(path)
    storage = fields.PrivateFileSystemStorage()

    return StreamingHttpResponse(storage.open(path), content_type=mime_type)


@login_required
def administrative_entity_file_download(request, path):
    """
    Securely download the administrative entity customization files for member of the administrative_entity concerned
    """

    if (
        services.get_user_administrative_entities(request.user).count() == 0
        and not request.user.is_superuser
    ):
        raise Http404

    mime_type, encoding = mimetypes.guess_type(path)
    storage = fields.PrivateFileSystemStorage()

    return StreamingHttpResponse(storage.open(path), content_type=mime_type)


@login_required
def genericauthorview(request, pk):

    instance = get_object_or_404(models.PermitAuthor, pk=pk)
    form = forms.GenericAuthorForm(request.POST or None, instance=instance)

    for field in form.fields:

        form.fields[field].disabled = True

    return render(request, "permits/permit_request_author.html", {"form": form})


@login_required
def administrative_infos(request):

    administrative_entities = models.PermitAdministrativeEntity.objects.all()

    return render(
        request,
        "permits/administrative_infos.html",
        {"administrative_entities": administrative_entities},
    )


# /////////////////////
# FOR DEV ONLY UNITL YC-230 IS MERGED
# /////////////////////

from django.http import FileResponse, HttpResponseNotFound, JsonResponse


def demo_geojson(request):

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("*******************QGIS QUERYING JSON******************")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    demo_data = {
        "type": "FeatureCollection",
        "name": "poc",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::2056"}},
        "features": [
            {
                "type": "Feature",
                "properties": {"id": 1, "rueid": 75, "adrnumero": 6},
                "geometry": {
                    "type": "MultiPoint",
                    "coordinates": [[2539015.02199999988, 1181127.158599998801947]],
                },
            },
            {
                "type": "Feature",
                "properties": {"id": 2, "rueid": 109, "adrnumero": 4},
                "geometry": {
                    "type": "MultiPoint",
                    "coordinates": [[2539057.793000001460314, 1181175.138599999249]],
                },
            },
            {
                "type": "Feature",
                "properties": {"id": 3, "rueid": 75, "adrnumero": 8},
                "geometry": {
                    "type": "MultiPoint",
                    "coordinates": [[2539001.561999998986721, 1181128.48959999904]],
                },
            },
        ],
    }

    return JsonResponse(demo_data, safe=False)
