import datetime
import logging
import mimetypes
import os
import urllib.parse
from datetime import datetime

import django_tables2 as tableslib
from constance import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
    SuspiciousOperation,
)
from django.db import transaction
from django.db.models import Prefetch, Q, Sum
from django.forms import formset_factory, modelformset_factory
from django.http import Http404, HttpResponse, JsonResponse, StreamingHttpResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import View
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from . import fields, filters, forms, models, services, tables
from .decorators import check_mandatory_2FA, permanent_user_required
from .exceptions import BadPermitRequestStatus, NonProlongablePermitRequest
from .search import search_permit_requests, search_result_to_json
from .tables import CustomPropertyValueAccessiblePermitRequest, get_custom_dynamic_table

logger = logging.getLogger(__name__)


def user_has_permitauthor(user):
    try:
        user.permitauthor
    except models.PermitAuthor.DoesNotExist:
        return False

    return True


def get_permit_request_for_edition(user, permit_request_id):
    permit_request = models.PermitRequest.objects.get(pk=permit_request_id)
    if permit_request.can_always_be_updated(user):
        allowed_statuses = {
            models.PermitRequest.STATUS_DRAFT,
            models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            models.PermitRequest.STATUS_APPROVED,
            models.PermitRequest.STATUS_PROCESSING,
            models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
            models.PermitRequest.STATUS_AWAITING_VALIDATION,
            models.PermitRequest.STATUS_REJECTED,
            models.PermitRequest.STATUS_RECEIVED,
        }
    else:
        allowed_statuses = {
            models.PermitRequest.STATUS_DRAFT,
            models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
            models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
        }

    permit_request = services.get_permit_request_for_user_or_404(
        user,
        permit_request_id,
        statuses=allowed_statuses,
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
        user,
        permit_request_id,
        statuses=allowed_statuses,
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


def disable_form(form, editable_fields=None):
    for field in form.fields.values():
        if editable_fields and field.label in editable_fields:
            continue
        field.disabled = True

    if not editable_fields:
        form.disabled = True


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


def permit_requests_can_have_multiple_ranges(permit_request):
    return True in [
        permit.can_have_multiple_ranges
        for permit in permit_request.works_object_types.all()
    ]


@method_decorator(login_required, name="dispatch")
@method_decorator(permanent_user_required, name="dispatch")
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

        action_forms = {
            action: self.get_form_for_action(action) for action in current_actions
        }
        action_formsets = {
            action: self.get_formset_for_action(action) for action in current_actions
        }
        available_actions = [
            action
            for action in current_actions
            if action_forms[action] or action_formsets[action]
        ]

        active_forms = [
            action
            for action in available_actions
            if not getattr(action_forms[action], "disabled", False)
            or not getattr(action_formsets[action], "disabled", False)
        ]

        if kwargs.get("active_form") or self.request.GET.get("prev_active_form"):
            active_form = (
                kwargs.get("active_form")
                if kwargs.get("active_form")
                else self.request.GET.get("prev_active_form")
            )

            if "poke" in active_forms and "validate" in active_forms:
                active_form = active_forms[active_forms.index("validate")]
        else:
            active_form = active_forms[0]

        kwargs["has_validations"] = self.permit_request.has_validations()

        if action_forms.get(models.ACTION_POKE):
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
                "forms": action_forms,
                "formsets": action_formsets,
                "active_form": active_form,
                "has_permission_to_classify": services.has_permission_to_classify_permit_request(
                    self.request.user, self.permit_request
                ),
                "can_classify": services.can_classify_permit_request(
                    self.request.user, self.permit_request
                ),
                "can_validate_permit_request": can_validate_permit_request,
                "directives": services.get_permit_request_directives(
                    self.permit_request
                ),
                "prolongation_enabled": prolongation_enabled,
                "document_enabled": services.has_document_enabled_for_wots(
                    self.permit_request
                ),
                "publication_enabled": self.permit_request.works_object_types.filter(
                    publication_enabled=True
                ).count()
                == self.permit_request.works_object_types.count(),
                "inquiry_in_progress": self.permit_request.status
                == models.PermitRequest.STATUS_INQUIRY_IN_PROGRESS,
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

        form = self.get_form_for_action(action, data=request.POST, files=request.FILES)
        form_type = "forms"
        # if no form was found, it might be a formset
        if not form:
            form = self.get_formset_for_action(
                action, data=request.POST, files=request.FILES
            )
            form_type = "formsets"

        if not form:
            raise PermissionDenied
        elif getattr(form, "disabled", False):
            raise SuspiciousOperation

        if form.is_valid():
            return self.handle_form_submission(form, action)

        # Replace unbound form by bound form in the context
        context = self.get_context_data(active_form=action)
        context[form_type][action] = form

        return self.render_to_response(context)

    def get_form_for_action(self, action, data=None, files=None):
        actions_forms = {
            models.ACTION_AMEND: self.get_amend_form,
            models.ACTION_REQUEST_VALIDATION: self.get_request_validation_form,
            models.ACTION_VALIDATE: self.get_validation_form,
            models.ACTION_POKE: self.get_poke_form,
            models.ACTION_PROLONG: self.get_prolongation_form,
            models.ACTION_REQUEST_INQUIRY: self.get_request_inquiry_form,
        }

        return (
            actions_forms[action](data=data, files=files)
            if action in actions_forms
            else None
        )

    def get_formset_for_action(self, action, data=None, files=None):
        actions_formset = {
            models.ACTION_COMPLEMENTARY_DOCUMENTS: self.get_complementary_documents_formset,
        }

        return (
            actions_formset[action](data=data, files=files)
            if action in actions_formset
            else None
        )

    def get_amend_form(self, data=None, **kwargs):

        if services.has_permission_to_amend_permit_request(
            self.request.user, self.permit_request
        ):

            # Get the first object type selected as a shorname suggestion for pilot
            first_wot = services.get_works_object_type_choices(
                self.permit_request
            ).first()
            shortname_value_proposal = (
                first_wot.works_object_type.works_object.name
                if first_wot
                and len(first_wot.works_object_type.works_object.name)
                <= models.PermitRequest._meta.get_field("shortname").max_length
                else None
            )
            # Only set the `status` default value if it's submitted for validation, to prevent accidentally resetting
            # the status

            initial = (
                {
                    "shortname": shortname_value_proposal,
                    "status": models.PermitRequest.STATUS_PROCESSING,
                }
                if self.permit_request.status
                == models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
                else {}
            )

            form = forms.PermitRequestAdditionalInformationForm(
                instance=self.permit_request,
                initial=initial,
                data=data,
                user=self.request.user,
            )

            if not services.can_amend_permit_request(
                self.request.user, self.permit_request
            ) and not self.permit_request.can_always_be_updated(self.request.user):

                disable_form(
                    form, self.permit_request.get_amend_property_list_always_amendable()
                )

            return form

        return None

    def get_request_inquiry_form(self, data=None, **kwargs):
        if not services.has_permission_to_amend_permit_request(
            self.request.user, self.permit_request
        ):
            return None

        current_inquiry = models.PermitRequestInquiry.get_current_inquiry(
            permit_request=self.permit_request
        )

        form = forms.PermitRequestInquiryForm(
            data=data,
            permit_request=self.permit_request,
            instance=current_inquiry,
        )

        if current_inquiry:
            disable_form(form, editable_fields=[form.fields["documents"].label])

        return form

    def get_request_validation_form(self, data=None, **kwargs):
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

    def get_validation_form(self, data=None, **kwargs):
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

    def get_poke_form(self, data=None, **kwargs):
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

    def get_prolongation_form(self, data=None, **kwargs):
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

    def get_complementary_documents_formset(self, data=None, **kwargs):
        ComplementaryDocumentsFormSet = formset_factory(
            form=forms.PermitRequestComplementaryDocumentsForm,
            extra=1,
        )

        return ComplementaryDocumentsFormSet(
            data,
            kwargs["files"],
            form_kwargs={
                "request": self.request,
                "permit_request": self.permit_request,
            },
        )

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
        elif action == models.ACTION_COMPLEMENTARY_DOCUMENTS:
            return self.handle_complementary_documents_form_submission(form)
        elif action == models.ACTION_REQUEST_INQUIRY:
            return self.handle_request_inquiry_form_submission(form)

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
            success_message += " " + _(
                "Le statut de la demande a été passé à en attente de compléments."
            )

        if form.cleaned_data.get("notify_author"):
            success_message += _("Le requérant a été notifié du changement par email.")

        messages.success(self.request, success_message)

        if (
            form.instance.status == models.PermitRequest.STATUS_RECEIVED
            and form.instance.status is not initial_status
        ):
            permit_request = form.instance

            # Notify the permit author
            data = {
                "subject": "{} ({})".format(
                    _("Votre annonce a été prise en compte et classée"),
                    services.get_works_type_names_list(permit_request),
                ),
                "users_to_notify": [permit_request.author.user.email],
                "template": "permit_request_received.txt",
                "permit_request": permit_request,
                "absolute_uri_func": self.request.build_absolute_uri,
            }
            services.send_email_notification(data)

            # Notify the services
            mailing_list = services.get_services_to_notify_mailing_list(permit_request)

            if mailing_list:
                data = {
                    "subject": "{} ({})".format(
                        _(
                            "Une annonce a été prise en compte et classée par le secrétariat"
                        ),
                        services.get_works_type_names_list(permit_request),
                    ),
                    "users_to_notify": set(mailing_list),
                    "template": "permit_request_received_for_services.txt",
                    "permit_request": permit_request,
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
                        "subject": "{} ({})".format(
                            _(
                                "Les services chargés de la validation d'une demande ont donné leur préavis"
                            ),
                            services.get_works_type_names_list(self.permit_request),
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

    def handle_complementary_documents_form_submission(self, form):
        for f in form:
            f.instance.owner = self.request.user
            f.instance.permit_request = self.permit_request
            f.save()
            f.save_m2m()

        success_message = (
            _("Les documents ont bien été ajoutés à la demande #%s.")
            % self.permit_request.pk
        )
        messages.success(self.request, success_message)

        if "save_continue" in self.request.POST:
            target = reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
            query_string = urllib.parse.urlencode(
                {"prev_active_form": models.ACTION_COMPLEMENTARY_DOCUMENTS}
            )
            return redirect(f"{target}?{query_string}")

        return redirect("permits:permit_requests_list")

    def handle_request_inquiry_form_submission(self, form):
        # check if we're coming from the confirmation page
        if not form.data.get("confirmation"):
            non_public_documents = []
            for document in form.cleaned_data["documents"]:
                if not document.is_public:
                    non_public_documents.append(document)

            # check if any of the documents aren't public
            # if so, redirect to confirmation page
            if non_public_documents:
                return render(
                    self.request,
                    "permits/permit_request_confirm_inquiry.html",
                    {
                        "non_public_documents": non_public_documents,
                        "inquiry_form": form,
                        "permit_request": self.permit_request,
                    },
                )
        form.instance.submitter = self.request.user
        form.instance.permit_request = self.permit_request

        if form.cleaned_data.get("start_date") == datetime.today().date():
            self.permit_request.start_inquiry()

        form.save()

        success_message = _("La mise en consultation publique a bien été enregistrée")
        messages.success(self.request, success_message)

        return redirect(
            "permits:permit_request_detail",
            permit_request_id=self.permit_request.pk,
        )


class PermitRequestComplementaryDocumentDeleteView(DeleteView):
    model = models.PermitRequestComplementaryDocument
    success_message = _("Le document '%s' a été supprimé avec succès")
    final_error_message = _("Les documents finaux ne peuvent pas être supprimés")
    owner_error_message = _("Vous pouvez seulement supprimer vos documents")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()

        if not obj.owner == self.request.user and not self.request.user.is_superuser:
            messages.add_message(request, messages.ERROR, self.owner_error_message)
            return redirect(self.get_success_url())

        # Final documents can't be deleted!
        if obj.status == models.PermitRequestComplementaryDocument.STATUS_FINALE:
            messages.add_message(request, messages.ERROR, self.final_error_message)
            return redirect(self.get_success_url())

        try:
            res = super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            messages.add_message(
                request,
                messages.ERROR,
                _("%s. [%s]") % (error.args[0], error.args[1].args[1]),
            )
            return redirect(self.get_success_url())

        messages.success(self.request, self.success_message % obj.document)
        return res

    def get_success_url(self):
        return reverse_lazy(
            "permits:permit_request_detail",
            kwargs={"permit_request_id": self.get_object().permit_request_id},
        )


@method_decorator(login_required, name="dispatch")
@method_decorator(permanent_user_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ComplementaryDocumentDownloadView(View):
    def get(self, request, path, *args, **kwargs):
        return services.download_file(path)


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedPermitRequestListView(SingleTableMixin, ListView):
    model = models.ArchivedPermitRequest
    template_name = "permits/archived_permit_request_list.html"

    permission_error_message = _(
        "Vous n'avez pas les permissions pour archiver cette demande"
    )
    archive_failed_error_message = _("Une erreur est survenue lors de l'archivage")

    def post(self, request, *args, **kwargs):

        if request.POST.get("action") == "archive-requests":
            return self.archive()

        return HttpResponseNotFound(_("Aucune action spécifiée"))

    def get_queryset(self):
        return services.get_archived_request_list_for_user(self.request.user).order_by(
            "-archived_date"
        )

    def get_table_class(self):
        return tables.ArchivedPermitRequestsTable

    def archive(self):
        permit_request_ids = self.request.POST.getlist("to_archive[]")

        if not permit_request_ids:
            return HttpResponseNotFound(_("Rien à archiver"))

        department = models.PermitDepartment.objects.filter(
            group__in=self.request.user.groups.all()
        ).first()

        if (
            not self.request.user.is_superuser
            and not department.is_backoffice
            and not department.is_integrator_admin
        ):
            return JsonResponse(
                data={"error": True, "message": self.permission_error_message},
                status=403,
            )
        try:
            with transaction.atomic():
                for permit_request_id in permit_request_ids:
                    permit_request = services.get_permit_request_for_user_or_404(
                        self.request.user, permit_request_id
                    )
                    permit_request.archive(self.request.user)
        except Exception:
            return JsonResponse(
                data={"message": self.archive_failed_error_message}, status=500
            )

        return JsonResponse({"message": _("Demandes archivées avec succès")})


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedPermitRequestDeleteView(DeleteView):
    model = models.ArchivedPermitRequest
    success_url = reverse_lazy("permits:archived_permit_request_list")

    success_message = _("L'archive #%s a été supprimé avec succès")
    error_message = _("Vous n'avez pas les permissions pour supprimer cette archive")

    def post(self, request, *args, **kwargs):

        try:
            archive = models.ArchivedPermitRequest.objects.get(pk=kwargs.get("pk"))

            if not self.request.user == archive.archivist:
                messages.error(self.request, self.error_message)
                return redirect(self.success_url)

            return super(ArchivedPermitRequestDeleteView, self).post(
                request, *args, **kwargs
            )
        except models.ArchivedPermitRequest.DoesNotExist:
            raise SuspiciousOperation

    def get_success_url(self):
        messages.success(self.request, self.success_message % self.object.pk)
        return self.success_url


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedPermitRequestDownloadView(View):
    permission_error_message = _(
        "Vous n'avez pas les permissions pour télécharger cette archive"
    )
    not_exist_error_message = _("L'archive demandée n'existe pas")

    def get(self, request, *args, **kwargs):
        try:
            return services.download_archives(
                archive_ids=[kwargs.get("pk")], user=self.request.user
            )
        except PermissionDenied:
            error_message = self.permission_error_message
        except ObjectDoesNotExist:
            error_message = self.not_exist_error_message
        except Exception:
            error_message = _(
                "Une erreur est survenue lors de la création du fichier compressé. Veuillez contacter votre administrateur"
            )

        messages.error(request, error_message)
        return redirect(reverse_lazy("permits:archived_permit_request_list"))


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedPermitRequestBulkDownloadView(View):
    permission_error_message = _(
        "Vous n'avez pas les permissions pour télécharger ces archives"
    )
    info_message = _("Rien à télécharger")
    not_exist_error_message = _("Une des archives demandées n'existe pas")

    def get(self, request, *args, **kwargs):
        to_download = self.request.GET.getlist("to_download")
        if not to_download:
            messages.info(request, self.info_message)
            return redirect(reverse_lazy("permits:archived_permit_request_list"))

        try:
            return services.download_archives(
                archive_ids=to_download, user=self.request.user
            )
        except PermissionDenied:
            error_message = self.permission_error_message
        except ObjectDoesNotExist:
            error_message = self.not_exist_error_message
        except Exception:
            error_message = _(
                "Une erreur est survenue lors de la création du fichier compressé. Veuillez contacter votre administrateur"
            )

        messages.error(request, error_message)
        return redirect(reverse_lazy("permits:archived_permit_request_list"))


def anonymous_permit_request_sent(request):
    return render(
        request,
        "permits/permit_request_anonymous_sent.html",
        {},
    )


def anonymous_permit_request(request):
    # Logout silently any real user
    if request.user.is_authenticated and not request.user.permitauthor.is_temporary:
        logout(request)

    # Accept only non-logged users, or temporary users
    if not request.user.is_anonymous and not request.user.permitauthor.is_temporary:
        raise Http404

    # Validate tags
    services.store_tags_in_session(request)
    entityfilter = request.session.get("entityfilter", [])
    typefilter = request.session.get("typefilter", [])
    if not len(entityfilter) > 0 or not len(typefilter) > 0:
        raise Http404

    # Validate entity
    entities_by_tag = models.PermitAdministrativeEntity.objects.public().filter_by_tags(
        entityfilter
    )
    if len(entities_by_tag) != 1:
        raise Http404
    entity = entities_by_tag[0]

    # Validate captcha and temporary user connection
    captcha_refresh_url = (
        "/" + settings.PREFIX_URL + "captcha/refresh/"
        if settings.PREFIX_URL
        else "/captcha/refresh/"
    )
    if not services.is_anonymous_request_logged_in(request, entity):
        # Captcha page
        if request.method == "POST":
            anonymous_request_form = forms.AnonymousRequestForm(request.POST)
            if anonymous_request_form.is_valid():
                # Perform temporary login
                services.login_for_anonymous_request(request, entity)
            else:
                return render(
                    request,
                    "permits/permit_request_anonymous_captcha.html",
                    {
                        "anonymous_request_form": anonymous_request_form,
                        "captcha_refresh_url": captcha_refresh_url,
                    },
                )
        else:
            return render(
                request,
                "permits/permit_request_anonymous_captcha.html",
                {
                    "anonymous_request_form": forms.AnonymousRequestForm(),
                    "captcha_refresh_url": captcha_refresh_url,
                },
            )

    # Validate type
    work_types = (
        models.WorksType.objects.filter(works_object_types__is_anonymous=True)
        .filter_by_tags(typefilter)
        .distinct()
        .values_list("pk", flat=True)
    )

    if len(work_types) != 1:
        raise Http404
    work_type = work_types[0]

    # Validate available work objects types
    works_object_types = models.WorksObjectType.anonymous_objects.filter(
        administrative_entities=entity,
        works_type=work_type,
    )

    if not works_object_types:
        raise Http404

    # Permit request page

    # Never create a second permit request for the same temp_author
    permit_request, _ = models.PermitRequest.objects.get_or_create(
        administrative_entity=entity,
        author=request.user.permitauthor,
    )

    # If filter combinations return only one works_object_types object,
    # this combination must be set on permit_request object
    if len(works_object_types) == 1:
        permit_request.works_object_types.set(works_object_types)

    steps = services.get_anonymous_steps(
        type=work_type, user=request.user, permit_request=permit_request
    )

    for step_type, step in steps.items():
        if step and step.enabled and not step.completed:
            return redirect(step.url)


@redirect_bad_status_to_detail
@login_required
@user_passes_test(user_has_permitauthor)
@permanent_user_required
@check_mandatory_2FA
def permit_request_select_administrative_entity(request, permit_request_id=None):

    services.store_tags_in_session(request)
    current_site = get_current_site(request)

    if permit_request_id:
        permit_request = get_permit_request_for_edition(request.user, permit_request_id)
    else:
        permit_request = None

    # Manage redirect to type step when only 1 item is shown
    # Handle single tag filters combinations
    entityfilter = (
        request.session["entityfilter"] if "entityfilter" in request.session else []
    )

    entities = services.get_administrative_entities(request.user, current_site)

    # Manage entities by tag and by site. If site has already 1 result, dont check the tag
    entities_after_filter = (
        entities.filter_by_tags(entityfilter)
        if entityfilter and len(entities) != 1
        else entities
    )

    # If entityfilter returns only one entity, permit_request oject can already be created
    if len(entities_after_filter) == 1 and not permit_request:
        administrative_entity_instance = models.PermitAdministrativeEntity.objects.get(
            pk=entities_after_filter.first().pk
        )

        permit_request = models.PermitRequest.objects.create(
            administrative_entity=administrative_entity_instance,
            author=request.user.permitauthor,
        )

        candidate_works_object_types = None

        if request.session["typefilter"] == []:
            candidate_works_object_types = models.WorksObjectType.objects.filter(
                administrative_entities__in=entities_after_filter,
            )
        else:
            works_types_by_tag = models.WorksType.objects.filter_by_tags(
                request.session["typefilter"]
            ).values_list("pk", flat=True)

            candidate_works_object_types = models.WorksObjectType.objects.filter(
                administrative_entities__in=entities_after_filter,
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
            instance=permit_request,
            user=request.user,
            session=request.session,
            site=current_site,
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
@permanent_user_required
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
                ).filter(is_anonymous=False)
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
                + urllib.parse.urlencode(
                    {"types": selected_works_types},
                    doseq=True,
                )
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
    Step to select works objects. This view supports either editing an existing permit
    request (if `permit_request_id` is set) or creating a new permit request.
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
@permanent_user_required
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
        {
            "permit_request": permit_request,
            "permit_request_prolongation_form": form,
        },
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
            try:
                form.save()

                return redirect(
                    services.get_next_step(
                        steps_context["steps"], models.StepType.APPENDICES
                    ).url
                )
            except:
                messages.error(
                    request,
                    _("Une erreur est survenue lors de l'upload de fichier."),
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
    can_have_multiple_ranges = permit_requests_can_have_multiple_ranges(permit_request)

    PermitRequestGeoTimeFormSet = modelformset_factory(
        models.PermitRequestGeoTime,
        form=forms.PermitRequestGeoTimeForm,
        extra=0,
        min_num=1,
        can_delete=can_have_multiple_ranges,
    )
    formset = PermitRequestGeoTimeFormSet(
        request.POST if request.method == "POST" else None,
        form_kwargs={"permit_request": permit_request},
        queryset=permit_request.geo_time.filter(
            comes_from_automatic_geocoding=False
        ).all(),
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
            "can_have_multiple_ranges": can_have_multiple_ranges,
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
@method_decorator(permanent_user_required, name="dispatch")
class PermitRequestList(ExportMixin, SingleTableMixin, FilterView):
    paginate_by = int(os.environ["PAGINATE_BY"])
    template_name = "permits/permit_requests_list.html"

    def _get_wot_filter(self):
        return self.request.GET.get("works_object_types__works_object", None)

    def get_queryset(self):
        works_object_filter = self._get_wot_filter()
        qs = (
            (
                services.get_permit_requests_list_for_user(
                    self.request.user,
                    works_object_filter=works_object_filter,
                )
            )
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

        if works_object_filter is not None:
            qs = qs.prefetch_related("worksobjecttypechoice_set__properties__property")

        return qs

    def get_table_data(self):
        works_object_filter = self._get_wot_filter()
        if works_object_filter:
            return [
                CustomPropertyValueAccessiblePermitRequest(obj)
                for obj in self.object_list
            ]
        else:
            return self.object_list

    def is_department_user(self):
        return self.request.user.groups.filter(permitdepartment__isnull=False).exists()

    def _get_extra_column_specs(self, works_object_filter):
        extra_column_specs = dict()
        for permit_request in self.object_list:
            for wot, properties in services.get_properties(
                permit_request,
                [
                    models.WorksObjectProperty.INPUT_TYPE_FILE_DOWNLOAD,
                    models.WorksObjectProperty.INPUT_TYPE_TITLE,
                ],
            ):
                if str(wot.works_object_id) != works_object_filter:
                    continue
                for property in properties:
                    property_id = f"{works_object_filter}_{property.id}"
                    if property_id not in extra_column_specs:
                        extra_column_specs[property_id] = tableslib.Column(
                            verbose_name=property.name,
                            orderable=True,
                            accessor=f"#{property_id}",
                        )
        return list(extra_column_specs.items())

    def is_exporting(self):
        return bool(self.request.GET.get(self.export_trigger_param, None))

    def get_table_class(self):
        works_object_filter = self._get_wot_filter()

        if self.is_department_user():
            if works_object_filter:
                extra_columns = self._get_extra_column_specs(works_object_filter)
                extra_column_names = tuple([col_name for col_name, __ in extra_columns])
            else:
                extra_column_names = tuple()

            if config.ENABLE_GEOCALENDAR:
                extra_column_names += tuple(["shortname", "is_public"])

            table_class = (
                tables.DepartmentPermitRequestsExportTable
                if self.is_exporting()
                else tables.DepartmentPermitRequestsHTMLTable
            )
            table_class = get_custom_dynamic_table(table_class, extra_column_names)
        else:
            table_class = (
                tables.OwnPermitRequestsExportTable
                if self.is_exporting()
                else tables.OwnPermitRequestsHTMLTable
            )
        return table_class

    def get_table_kwargs(self):
        wot_filter = self._get_wot_filter()
        if wot_filter:
            return {"extra_column_specs": self._get_extra_column_specs(wot_filter)}
        return {}

    def get_filterset_class(self):
        return (
            filters.DepartmentPermitRequestFilterSet
            if self.is_department_user()
            else filters.OwnPermitRequestFilterSet
        )

    def get_context_data(self, **kwargs):
        context = super(PermitRequestList, self).get_context_data(**kwargs)
        params = {key: value[0] for key, value in dict(self.request.GET).items()}
        context["display_clear_filters"] = bool(params)
        params.update({"_export": "csv"})
        context["export_csv_url_params"] = urllib.parse.urlencode(params)
        return context


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

    checkbox_to_notify = models.WorksObjectPropertyValue.objects.filter(
        works_object_type_choice__permit_request=permit_request, value={"val": True}
    ).values_list("property__services_to_notify", flat=True)

    if checkbox_to_notify.exists():
        mailing_list = []
        for emails in checkbox_to_notify:
            emails_addresses = emails.replace("\n", ",").split(",")
            mailing_list += [
                ea.strip()
                for ea in emails_addresses
                if services.validate_email(ea.strip())
            ]
        if mailing_list:
            data = {
                "subject": _("Votre service à été mentionné dans une demande"),
                "users_to_notify": set(mailing_list),
                "template": "permit_request_submitted_with_mention.txt",
                "permit_request": permit_request,
                "absolute_uri_func": request.build_absolute_uri,
            }
            services.send_email_notification(data)

    # Only submit request when it's editable by author, to prevent a "raise SuspiciousOperation"
    # When editing a permit_request, submit isn't required to save the modifications, as every view saves the updates
    if permit_request.can_be_edited_by_author():
        services.submit_permit_request(permit_request, request)

    user_is_backoffice_or_integrator_for_administrative_entity = request.user.groups.filter(
        Q(permitdepartment__administrative_entity=permit_request.administrative_entity),
        Q(permitdepartment__is_backoffice=True)
        | Q(permitdepartment__is_integrator_admin=True),
    )

    # Backoffice and integrators creating a permit request for their own administrative
    # entity, are directly redirected to the permit detail
    # Same flow for requests when permit_request can't be edited by author
    if (
        user_is_backoffice_or_integrator_for_administrative_entity
        and not permit_request.can_be_edited_by_author()
    ):
        return redirect(
            "permits:permit_request_detail", permit_request_id=permit_request_id
        )
    else:

        if (
            request.user.permitauthor.is_temporary
            and permit_request.author == request.user.permitauthor
        ):
            try:
                anonymous_user = permit_request.administrative_entity.anonymous_user
            except ObjectDoesNotExist:
                # Might happen only if the entity's anonymous user has been removed
                # between the creation and the submission of the permit request
                raise Http404
            else:
                permit_request.author = anonymous_user
                permit_request.save()
                temp_user = request.user
                logout(request)
                temp_user.delete()
                return redirect("permits:anonymous_permit_request_sent")

        return redirect("permits:permit_requests_list")


@redirect_bad_status_to_detail
@login_required
@permanent_user_required
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
@permanent_user_required
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
                "subject": "{} ({})".format(
                    _("Votre demande a été traitée et classée"),
                    services.get_works_type_names_list(permit_request),
                ),
                "users_to_notify": [permit_request.author.user.email],
                "template": "permit_request_classified.txt",
                "permit_request": permit_request,
                "absolute_uri_func": request.build_absolute_uri,
            }
            services.send_email_notification(data)

            # Notify the services
            mailing_list = services.get_services_to_notify_mailing_list(permit_request)

            if mailing_list:
                data = {
                    "subject": "{} ({})".format(
                        _("Une demande a été traitée et classée par le secrétariat"),
                        services.get_works_type_names_list(permit_request),
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


@login_required
@permanent_user_required
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
    return services.download_file(path)


@login_required
def works_object_property_file_download(request, path):
    """
    Download the wot file at the given `path` as an attachment.
    """
    return services.download_file(path)


@login_required
@permanent_user_required
@check_mandatory_2FA
def administrative_entity_file_download(request, path):
    """
    Only allows logged user to download administrative entity files
    """

    mime_type, encoding = mimetypes.guess_type(path)
    storage = fields.PrivateFileSystemStorage()

    return StreamingHttpResponse(storage.open(path), content_type=mime_type)


@login_required
@permanent_user_required
@check_mandatory_2FA
def genericauthorview(request, pk):

    instance = get_object_or_404(models.PermitAuthor, pk=pk)
    form = forms.GenericAuthorForm(request.POST or None, instance=instance)

    for field in form.fields:

        form.fields[field].disabled = True

    return render(request, "permits/permit_request_author.html", {"form": form})


@login_required
@permanent_user_required
def permit_requests_search(request):
    terms = request.GET.get("search")

    if len(terms) >= 2:
        permit_requests = services.get_permit_requests_list_for_user(request.user)
        results = search_permit_requests(
            search_str=terms, permit_requests_qs=permit_requests, limit=5
        )
    else:
        results = []

    return JsonResponse(
        {"results": [search_result_to_json(result) for result in results]}
    )
