import logging
import mimetypes
import os
import urllib.parse

import requests
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Prefetch, Sum
from django.forms import modelformset_factory
from django.http import (
    Http404,
    HttpResponse,
    JsonResponse,
    StreamingHttpResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import View
from django_filters.views import FilterView
from django_otp import user_has_device
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin, SingleTableView

from . import fields, filters, forms, models, services, tables
from .exceptions import BadPermitRequestStatus, NonProlongablePermitRequest
from .search import match_type_label, search_permit_requests

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


def get_permit_request_for_prolongation(user, permit_request_id):

    allowed_statuses = models.PermitRequest.PROLONGABLE_STATUSES

    permit_request = services.get_permit_request_for_user_or_404(
        user, permit_request_id, statuses=allowed_statuses,
    )

    if not permit_request.works_object_types.filter(permit_duration__gte=0).exists():
        raise NonProlongablePermitRequest(permit_request)
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


def check_mandatory_2FA(
    view=None, redirect_field_name="next", login_url="profile", if_configured=False
):
    """
    Do same as :func:`django_otp.decorators.otp_required`, but verify first if the user
    is in a group where 2FA is required.
    """

    def test(user):
        if services.is_2FA_mandatory(user):
            return user.is_verified() or (
                if_configured and user.is_authenticated and not user_has_device(user)
            )
        else:
            return True

    decorator = user_passes_test(
        test, login_url=login_url, redirect_field_name=redirect_field_name
    )

    return decorator if (view is None) else decorator(view)


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
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
            # This is to maintain the prolongation tab active in case of POST error
            if "action=prolong" in str(self.request.body):
                active_form = active_forms[active_forms.index("prolong")]

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

            kwargs["validations"] = self.permit_request.validations.select_related(
                "department", "department__group"
            )
        can_validate_permit_request = services.can_validate_permit_request(
            self.request.user, self.permit_request
        )
        history = (
            self.permit_request.history.all()
            if services.has_permission_to_amend_permit_request(
                self.request.user, self.permit_request
            )
            or can_validate_permit_request
            else None
        )
        prolongation_enabled = (
            services.get_works_object_type_choices(self.permit_request).aggregate(
                Sum("works_object_type__permit_duration")
            )["works_object_type__permit_duration__sum"]
            is not None
        )

        return {
            **kwargs,
            **{
                "permit_request": self.permit_request,
                "history": history,
                "forms": forms,
                "active_form": active_form,
                "has_permission_to_classify": services.has_permission_to_classify_permit_request(
                    self.request.user, self.permit_request
                ),
                "can_classify": services.can_classify_permit_request(
                    self.request.user, self.permit_request
                ),
                "can_validate_permit_request": can_validate_permit_request,
                "print_templates": services.get_permit_request_print_templates(
                    self.permit_request
                ),
                "directives": services.get_permit_request_directives(
                    self.permit_request
                ),
                "prolongation_enabled": prolongation_enabled,
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
            models.ACTION_PROLONG: self.get_prolongation_form,
        }

        return actions_forms[action](data=data)

    def get_amend_form(self, data=None):

        if services.has_permission_to_amend_permit_request(
            self.request.user, self.permit_request
        ):
            # Only set the `status` default value if it's submitted for validation, to prevent accidentally resetting
            # the status

            first_wot_type = (
                (
                    services.get_works_object_type_choices(self.permit_request)
                    .first()
                    .works_object_type.works_object.name
                )
                if self.permit_request
                else None
            )

            initial = (
                {
                    "shortname": first_wot_type,
                    "status": models.PermitRequest.STATUS_PROCESSING,
                }
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

            if not services.can_request_permit_validation(
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

    def get_prolongation_form(self, data=None):
        if services.has_permission_to_poke_permit_request(
            self.request.user, self.permit_request
        ):
            form = forms.PermitRequestProlongationForm(
                instance=self.permit_request, data=data
            )

            if not services.can_prolonge_permit_request(
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
        elif action == models.ACTION_PROLONG:
            return self.handle_prolongation_form_submission(form)

    def handle_amend_form_submission(self, form):
        initial_status = (
            models.PermitRequest.objects.filter(id=form.instance.id).first().status
        )
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

        if (
            form.instance.status == models.PermitRequest.STATUS_RECEIVED
            and form.instance.status is not initial_status
        ):
            data = {
                "subject": _("Votre annonce a été prise en compte et classée"),
                "users_to_notify": [form.instance.author.user.email],
                "template": "permit_request_received.txt",
                "permit_request": form.instance,
                "absolute_uri_func": self.request.build_absolute_uri,
            }
            services.send_email_notification(data)

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
        validation_object = models.PermitRequestValidation.objects.filter(
            permit_request_id=self.permit_request.id,
            validated_by_id=self.request.user.id,
        )
        initial_validation_status = (
            (validation_object.first().validation_status)
            if validation_object.exists()
            else models.PermitRequestValidation.STATUS_REQUESTED
        )
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

        try:

            if not self.permit_request.get_pending_validations():

                initial_permit_status = self.permit_request.status
                self.permit_request.status = models.PermitRequest.STATUS_PROCESSING
                self.permit_request.save()

                if (
                    initial_permit_status
                    is models.PermitRequest.STATUS_AWAITING_VALIDATION
                    or (
                        initial_permit_status is models.PermitRequest.STATUS_PROCESSING
                        and initial_validation_status
                        is not form.instance.validation_status
                    )
                ):
                    data = {
                        "subject": _(
                            "Les services chargés de la validation d'une demande ont donné leur préavis"
                        ),
                        "users_to_notify": services._get_secretary_email(
                            self.permit_request
                        ),
                        "template": "permit_request_validated.txt",
                        "permit_request": self.permit_request,
                        "absolute_uri_func": self.request.build_absolute_uri,
                    }
                    services.send_email_notification(data)
            else:
                self.permit_request.status = (
                    models.PermitRequest.STATUS_AWAITING_VALIDATION
                )
                self.permit_request.save()

        except AttributeError:
            # This is the case when the administrative entity does not have a
            # secretary department associated to a group to which
            # the secretary user belongs.
            pass

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

    def handle_prolongation_form_submission(self, form):
        form.save()
        if form.instance.prolongation_status:
            success_message = (
                _(
                    "La prolongation de la demande #%s a été traitée et un émail envoyé à l'auteur-e."
                )
                % self.permit_request.pk
            )

            messages.success(self.request, success_message)

            subject = (
                _("Votre demande #%s a bien été prolongée.") % self.permit_request.pk
                if form.instance.prolongation_status
                == self.permit_request.PROLONGATION_STATUS_APPROVED
                else _("La prolongation de votre demande #%s a été refusée.")
                % self.permit_request.pk
            )
            data = {
                "subject": subject,
                "users_to_notify": [form.instance.author.user.email],
                "template": "permit_request_prolongation.txt",
                "permit_request": form.instance,
                "absolute_uri_func": self.request.build_absolute_uri,
            }
            services.send_email_notification(data)

        if "save_continue" in self.request.POST:
            return redirect(
                "permits:permit_request_detail",
                permit_request_id=self.permit_request.pk,
            )
        else:
            return redirect("permits:permit_requests_list")


def permit_request_print(request, permit_request_id, template_id):
    permit_request = services.get_permit_request_for_user_or_404(
        request.user, permit_request_id
    )
    template = get_object_or_404(models.QgisProject.objects, pk=template_id)
    generated_document, created_at = models.QgisGeneratedDocument.objects.get_or_create(
        permit_request=permit_request, qgis_project=template
    )

    # Uses customize qgis-atlasprint plugin adapted from 3liz
    # https://github.com/3liz/qgis-atlasprint
    values = {
        "SERVICE": "ATLAS",
        "REQUEST": "GETPRINT",
        "FORMAT": "PDF",
        "TRANSPARENT": "true",
        "SRS": "EPSG:2056",
        "DPI": "150",
        "MAP": "/io/data/report_template.qgs"
        if template.qgis_project_file.name == "report_template.qgs"
        else "/private_documents/" + template.qgis_project_file.name,
        "TEMPLATE": template.qgis_print_template_name,
        "EXP_FILTER": f"$id={permit_request_id}",
        "PERMIT_REQUEST_ID": permit_request_id,
    }

    qgisserver_url = "http://qgisserver/ogc/?" + urllib.parse.urlencode(values)
    qgisserver_response = requests.get(
        qgisserver_url, headers={"Accept": "application/pdf"}, stream=True
    )

    if not qgisserver_response:
        return HttpResponse(_("Une erreur est survenue lors de l'impression"))

    file_name = f"demande_{permit_request_id}_geocity_{template_id}.pdf"
    generated_document.printed_file.save(
        file_name, ContentFile(qgisserver_response.content), True
    )
    generated_document.printed_at = timezone.now()
    generated_document.printed_by = request.user.get_full_name()
    generated_document.save()

    response = StreamingHttpResponse(
        qgisserver_response.iter_content(chunk_size=128), content_type="application/pdf"
    )
    response["Content-Disposition"] = 'attachment; filename="' + file_name + '"'

    return response


@redirect_bad_status_to_detail
@login_required
@user_passes_test(user_has_permitauthor)
@check_mandatory_2FA
def permit_request_select_administrative_entity(request, permit_request_id=None):

    services.store_tags_in_session(request)

    if permit_request_id:
        permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    else:
        permit_request = None

    # Prevent unecessary queries to DB if no tag filter is applied anyway
    if request.session["entityfilter"]:
        # Handle single tag filters combinations
        entityfilter = (
            request.session["entityfilter"] if "entityfilter" in request.session else []
        )
        entities_by_tag = services.get_administrative_entities(
            request.user
        ).filter_by_tags(entityfilter)
        # If entityfilter returns only one entity, permit_request oject can alread be created
        if len(entities_by_tag) == 1 and not permit_request:
            administrative_entity_instance = models.PermitAdministrativeEntity.objects.get(
                pk=entities_by_tag.first().pk
            )
            permit_request = models.PermitRequest.objects.create(
                administrative_entity=administrative_entity_instance,
                author=request.user.permitauthor,
            )
            candidate_works_object_types = None
            if request.session["typefilter"] == []:
                candidate_works_object_types = models.WorksObjectType.objects.filter(
                    administrative_entities__in=entities_by_tag,
                )
            else:
                works_types_by_tag = models.WorksType.objects.filter_by_tags(
                    request.session["typefilter"]
                ).values_list("pk", flat=True)

                candidate_works_object_types = models.WorksObjectType.objects.filter(
                    administrative_entities__in=entities_by_tag,
                    works_type__in=works_types_by_tag,
                )
            # If filter combinations return only one works_object_types object, this combination must be set on permitrequest object
            if len(candidate_works_object_types) == 1:
                permit_request.works_object_types.set(candidate_works_object_types)

            steps = services.get_progress_bar_steps(
                request=request, permit_request=permit_request
            )
            return redirect(
                services.get_next_step(steps, models.StepType.ADMINISTRATIVE_ENTITY).url
            )

    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.ADMINISTRATIVE_ENTITY,
    )

    if request.method == "POST":
        administrative_entity_form = forms.AdministrativeEntityForm(
            instance=permit_request,
            data=request.POST,
            user=request.user,
            session=request.session,
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
            instance=permit_request, user=request.user, session=request.session,
        )
    return render(
        request,
        "permits/permit_request_select_administrative_entity.html",
        {
            "form": administrative_entity_form,
            "permit_request": permit_request,
            "entityfilter": request.session["entityfilter"]
            if "entityfilter" in request.session
            else None,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def permit_request_select_types(request, permit_request_id):
    """
    Step to select works types (eg. demolition). No permit request is created at this step since we only store (works
    object, works type) couples in the database.
    """
    services.store_tags_in_session(request)
    # returns error or redirects to details depending on user permissions and permit_request status
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.WORKS_TYPES,
    )
    if request.method == "POST":
        works_types_form = forms.WorksTypesForm(
            data=request.POST,
            instance=permit_request,
            user=request.user,
            session=request.session,
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
            instance=permit_request, user=request.user, session=request.session
        )
    return render(
        request,
        "permits/permit_request_select_types.html",
        {
            "works_types_form": works_types_form,
            "permit_request": permit_request,
            "typefilter": request.session["typefilter"]
            if "typefilter" in request.session
            else [],
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
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
            data=request.GET,
            instance=permit_request,
            user=request.user,
            session=request.session,
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

    # Add the permit request works types to the ones in the querystring and remove duplicates
    works_types = (
        works_types | services.get_permit_request_works_types(permit_request)
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
            "typefilter": request.session["typefilter"]
            if "typefilter" in request.session
            else [],
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
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

    return render(
        request,
        "permits/permit_request_properties.html",
        {
            "permit_request": permit_request,
            "permit_request_form": form,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def permit_request_prolongation(request, permit_request_id):
    """
    Request prolongation interface for the Permit author.
    """

    if not permit_request_id:
        messages.success(request, _("Un id de permis valable est requis"))
        return redirect("permits:permit_requests_list")

    try:
        permit_request = get_permit_request_for_prolongation(
            request.user, permit_request_id
        )
    except NonProlongablePermitRequest:
        messages.error(request, _("La demande de permis ne peut pas être prolongée."))
        return redirect("permits:permit_requests_list")

    if request.method == "POST":

        form = forms.PermitRequestProlongationForm(
            instance=permit_request, data=request.POST
        )
        del form.fields["prolongation_status"]
        del form.fields["prolongation_comment"]

        if form.is_valid():
            obj = form.save(commit=False)
            obj.prolongation_status = permit_request.PROLONGATION_STATUS_PENDING
            obj.save()

            # Send the email to the services
            messages.success(request, _("Votre demande de prolongation a été envoyée"))

            subject = (
                _(
                    "Une demande de prolongation vient d'être soumise pour le permis #%s."
                )
                % permit_request_id
            )
            data = {
                "subject": subject,
                "users_to_notify": services._get_secretary_email(permit_request),
                "template": "permit_request_prolongation_for_services.txt",
                "permit_request": form.instance,
                "absolute_uri_func": request.build_absolute_uri,
            }
            services.send_email_notification(data)

            return redirect("permits:permit_requests_list")
    else:
        if permit_request.author != request.user.permitauthor:
            messages.error(
                request,
                _("Vous ne pouvez pas demander une prolongation pour le permis #%s.")
                % permit_request.pk,
            )
            return redirect("permits:permit_requests_list")

        if permit_request.prolongation_date and (
            permit_request.prolongation_status
            in [
                permit_request.PROLONGATION_STATUS_PENDING,
                permit_request.PROLONGATION_STATUS_REJECTED,
            ]
        ):
            messages.error(
                request,
                _(
                    "Une demande de prolongation pour le permis #%s est en attente ou a été refusée."
                )
                % permit_request.pk,
            )
            return redirect("permits:permit_requests_list")

        form = forms.PermitRequestProlongationForm(instance=permit_request)
        del form.fields["prolongation_status"]
        del form.fields["prolongation_comment"]

    return render(
        request,
        "permits/permit_request_prolongation.html",
        {"permit_request": permit_request, "permit_request_prolongation_form": form,},
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
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
@check_mandatory_2FA
def permit_request_actors(request, permit_request_id):
    permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    steps_context = progress_bar_context(
        request=request,
        permit_request=permit_request,
        current_step_type=models.StepType.ACTORS,
    )
    requires_payment = services.permit_requests_has_paid_wot(permit_request)

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
            "requires_payment": requires_payment,
            **steps_context,
        },
    )


@login_required
@check_mandatory_2FA
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
@check_mandatory_2FA
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

    response = StreamingHttpResponse(file, content_type=mime_type)
    response["Content-Disposition"] = 'attachment; filename="' + file.name + '"'
    return response


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
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
@method_decorator(check_mandatory_2FA, name="dispatch")
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
@check_mandatory_2FA
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

        services.submit_permit_request(permit_request, request)
        return redirect("permits:permit_requests_list")

    return render(
        request,
        "permits/permit_request_submit.html",
        {
            "permit_request": permit_request,
            "directives": services.get_permit_request_directives(permit_request),
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
@check_mandatory_2FA
def permit_request_submit_confirmed(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    incomplete_steps = [
        step.url
        for step in services.get_progress_bar_steps(request, permit_request).values()
        if step.errors_count and step.url
    ]

    if incomplete_steps:
        raise SuspiciousOperation

    services.submit_permit_request(permit_request, request)
    return redirect("permits:permit_requests_list")


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
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
@check_mandatory_2FA
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
            # Notify the permit author
            data = {
                "subject": _("Votre demande a été traitée et classée"),
                "users_to_notify": [permit_request.author.user.email],
                "template": "permit_request_classified.txt",
                "permit_request": permit_request,
                "absolute_uri_func": request.build_absolute_uri,
            }
            services.send_email_notification(data)

            # Notify the services
            works_object_types_to_notify = permit_request.works_object_types.filter(
                notify_services=True
            )

            if works_object_types_to_notify.exists():
                mailing_list = []
                for emails in works_object_types_to_notify.values_list(
                    "services_to_notify", flat=True
                ):
                    emails_addresses = emails.replace("\n", ",").split(",")
                    mailing_list += [
                        ea.strip()
                        for ea in emails_addresses
                        if services.validate_email(ea.strip())
                    ]

                if mailing_list:
                    data = {
                        "subject": _(
                            "Une demande a été traitée et classée par le secrétariat"
                        ),
                        "users_to_notify": set(mailing_list),
                        "template": "permit_request_classified_for_services.txt",
                        "permit_request": permit_request,
                        "absolute_uri_func": request.build_absolute_uri,
                    }
                    services.send_email_notification(data)

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
    file = storage.open(path)
    response = StreamingHttpResponse(file, content_type=mime_type)
    response["Content-Disposition"] = 'attachment; filename="' + file.name + '"'
    return response


@login_required
@check_mandatory_2FA
def administrative_entity_file_download(request, path):
    """
    Only allows logged user to download administrative entity files
    """

    mime_type, encoding = mimetypes.guess_type(path)
    storage = fields.PrivateFileSystemStorage()

    return StreamingHttpResponse(storage.open(path), content_type=mime_type)


@login_required
@check_mandatory_2FA
def genericauthorview(request, pk):

    instance = get_object_or_404(models.PermitAuthor, pk=pk)
    form = forms.GenericAuthorForm(request.POST or None, instance=instance)

    for field in form.fields:

        form.fields[field].disabled = True

    return render(request, "permits/permit_request_author.html", {"form": form})


@login_required
@check_mandatory_2FA
def administrative_infos(request):

    administrative_entities = models.PermitAdministrativeEntity.objects.all()

    return render(
        request,
        "permits/administrative_infos.html",
        {"administrative_entities": administrative_entities},
    )


@login_required
def permit_requests_search(request):
    def to_json_result(result):
        return {
            "permitRequest": {
                "id": result.permit_request_id,
                "url": reverse(
                    "permits:permit_request_detail",
                    kwargs={"permit_request_id": result.permit_request_id,},
                ),
                "author": result.author_name,
                "status": result.permit_request_status,
                "createdAt": result.permit_request_created_at.strftime("%d.%m.%Y"),
            },
            "match": {
                "fieldLabel": result.field_label,
                "fieldValue": result.field_value,
                "score": result.score,
                "type": result.match_type.value,
                "typeLabel": match_type_label(result.match_type),
            },
        }

    terms = request.GET.get("search")

    if len(terms) >= 2:
        permit_requests = services.get_permit_requests_list_for_user(request.user)
        results = search_permit_requests(
            search_str=terms, permit_requests_qs=permit_requests, limit=5
        )
    else:
        results = []

    return JsonResponse({"results": [to_json_result(result) for result in results]})
