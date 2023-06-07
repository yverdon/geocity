import datetime
import json
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
from django.core.serializers import serialize
from django.db import transaction
from django.db.models import Prefetch, Q, Sum
from django.forms import formset_factory, modelformset_factory
from django.http import Http404, HttpResponse, JsonResponse, StreamingHttpResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from geocity.apps.accounts.decorators import (
    check_mandatory_2FA,
    permanent_user_required,
)
from geocity.apps.accounts.models import AdministrativeEntity, PermitDepartment
from geocity.apps.accounts.users import get_departments, has_profile
from geocity.apps.forms.models import Field, Form

from . import filters, forms, models, permissions, services, tables
from .exceptions import BadSubmissionStatus, NonProlongableSubmission
from .payments.services import (
    get_payment_processor,
    get_transaction_from_id,
    get_transaction_from_merchant_reference,
)
from .search import search_result_to_json, search_submissions
from .services import send_refund_email
from .shortcuts import get_submission_for_user_or_404
from .steps import (
    StepType,
    get_anonymous_steps,
    get_geo_step_name_title,
    get_next_step,
    get_previous_step,
    get_progress_bar_steps,
    get_selectable_categories,
    get_selectable_entities,
)
from .tables import (
    CustomFieldValueAccessibleSubmission,
    TransactionsTable,
    get_custom_dynamic_table,
)

logger = logging.getLogger(__name__)


def get_submission_for_edition(user, submission_id):
    submission = models.Submission.objects.get(pk=submission_id)
    if permissions.can_always_be_updated(user, submission):
        allowed_statuses = {
            models.Submission.STATUS_DRAFT,
            models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            models.Submission.STATUS_APPROVED,
            models.Submission.STATUS_PROCESSING,
            models.Submission.STATUS_AWAITING_SUPPLEMENT,
            models.Submission.STATUS_AWAITING_VALIDATION,
            models.Submission.STATUS_REJECTED,
            models.Submission.STATUS_RECEIVED,
        }
    else:
        allowed_statuses = {
            models.Submission.STATUS_DRAFT,
            models.Submission.STATUS_AWAITING_SUPPLEMENT,
            models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        }

    submission = get_submission_for_user_or_404(
        user,
        submission_id,
        statuses=allowed_statuses,
    )

    can_pilot_edit_submission = permissions.can_edit_submission(user, submission)

    if (
        submission.status == models.Submission.STATUS_SUBMITTED_FOR_VALIDATION
        and not can_pilot_edit_submission
    ):
        raise BadSubmissionStatus(
            submission,
            [
                models.Submission.STATUS_DRAFT,
                models.Submission.STATUS_AWAITING_SUPPLEMENT,
            ],
        )
    return submission


def get_submission_for_prolongation(user, submission_id):
    allowed_statuses = models.Submission.PROLONGABLE_STATUSES

    submission = get_submission_for_user_or_404(
        user,
        submission_id,
        statuses=allowed_statuses,
    )

    if not submission.forms.filter(permit_duration__gte=0).exists():
        raise NonProlongableSubmission(submission)
    return submission


def redirect_bad_status_to_detail(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadSubmissionStatus as e:
            return redirect(
                "submissions:submission_detail", submission_id=e.submission.pk
            )

    return inner


def progress_bar_context(request, submission, current_step_type):
    steps = get_progress_bar_steps(request=request, submission=submission)
    if current_step_type not in steps:
        raise Http404()

    try:
        previous_step = get_previous_step(steps, current_step_type)
    except IndexError:
        previous_step = None

    return {"steps": steps, "previous_step": previous_step}


@method_decorator(login_required, name="dispatch")
@method_decorator(permanent_user_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class SubmissionDetailView(View):

    actions = models.ACTIONS

    def dispatch(self, request, *args, **kwargs):
        self.submission = get_submission_for_user_or_404(
            request.user, kwargs["submission_id"]
        )

        if self.submission.is_draft() and self.submission.author == request.user:
            return redirect(
                "submissions:submission_select_administrative_entity",
                submission_id=self.submission.pk,
            )

        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context):
        context["settings"] = settings
        return render(self.request, "submissions/submission_detail.html", context)

    def get_context_data(self, **kwargs):
        current_actions = self.submission.get_actions_for_administrative_entity()

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
        elif len(active_forms) > 0:
            active_form = active_forms[0]
        else:
            active_form = None

        kwargs["has_validations"] = self.submission.has_validations()

        if action_forms.get(models.ACTION_POKE):
            kwargs[
                "nb_pending_validations"
            ] = self.submission.get_pending_validations().count()
            kwargs["validations"] = self.submission.validations.select_related(
                "department", "department__group"
            )
        else:
            kwargs["nb_pending_validations"] = 0

            kwargs["validations"] = self.submission.validations.select_related(
                "department", "department__group"
            )
        can_validate_submission = permissions.can_validate_submission(
            self.request.user, self.submission
        )

        history = []
        # Prepare history for the submission and transaction(s)
        if (
            permissions.has_permission_to_amend_submission(
                self.request.user, self.submission
            )
            or can_validate_submission
        ):
            history = self.submission.get_history()

        prolongation_enabled = (
            self.submission.get_selected_forms().aggregate(
                Sum("form__permit_duration")
            )["form__permit_duration__sum"]
            is not None
        )
        transactions_table = None
        if self.submission.requires_online_payment():
            transactions_table = TransactionsTable(
                data=self.submission.get_transactions()
            )

        return {
            **kwargs,
            **{
                "submission": self.submission,
                "history": history,
                "forms": action_forms,
                "formsets": action_formsets,
                "active_form": active_form,
                "has_permission_to_classify": permissions.has_permission_to_classify_submission(
                    self.request.user, self.submission
                ),
                "can_classify": permissions.can_classify_submission(
                    self.request.user, self.submission
                ),
                "has_permission_to_classify_submission": permissions.has_permission_to_classify_submission(
                    self.request.user, self.submission
                ),
                "can_validate_submission": can_validate_submission,
                "has_permission_to_validate_submission": permissions.has_permission_to_validate_submission(
                    self.request.user, self.submission
                ),
                "has_permission_to_edit_submission_validations": permissions.has_permission_to_edit_submission_validations(
                    self.request.user, self.submission
                ),
                "directives": self.submission.get_submission_directives(),
                "prolongation_enabled": prolongation_enabled,
                "document_enabled": self.submission.has_document_enabled(),
                "online_payment_enabled": self.submission.requires_online_payment(),
                "transactions_table": transactions_table,
                "publication_enabled": self.submission.forms.filter(
                    publication_enabled=True
                ).count()
                == self.submission.forms.count(),
                "inquiry_in_progress": self.submission.status
                == models.Submission.STATUS_INQUIRY_IN_PROGRESS,
                "current_user": self.request.user,
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
        if permissions.has_permission_to_amend_submission(
            self.request.user, self.submission
        ):

            # Get the first form selected as a shorname suggestion for pilot
            first_selected_form = (
                self.submission.get_selected_forms()
                .select_related("submission", "form")
                .prefetch_related("form__fields")
                .first()
            )
            shortname_value_proposal = (
                first_selected_form.form.name
                if first_selected_form
                and len(first_selected_form.form.name)
                <= models.Submission._meta.get_field("shortname").max_length
                else None
            )
            # Only set the `status` default value if it's submitted for validation, to prevent accidentally resetting
            # the status

            initial = (
                {
                    "shortname": shortname_value_proposal,
                    "status": models.Submission.STATUS_PROCESSING,
                }
                if self.submission.status
                == models.Submission.STATUS_SUBMITTED_FOR_VALIDATION
                else {}
            )

            form = forms.SubmissionAdditionalInformationForm(
                instance=self.submission,
                initial=initial,
                data=data,
                user=self.request.user,
            )

            if not permissions.can_amend_submission(
                self.request.user, self.submission
            ) and not permissions.can_always_be_updated(
                self.request.user, self.submission
            ):

                forms.disable_form(
                    form, self.submission.get_amend_field_list_always_amendable()
                )

            return form

        return None

    def get_request_inquiry_form(self, data=None, **kwargs):
        if not permissions.has_permission_to_amend_submission(
            self.request.user, self.submission
        ):
            return None

        form = forms.SubmissionInquiryForm(
            data=data,
            submission=self.submission,
            instance=self.submission.current_inquiry,
        )

        if self.submission.current_inquiry:
            forms.disable_form(form, editable_fields=[form.fields["documents"].label])

        return form

    def get_request_validation_form(self, data=None, **kwargs):
        if permissions.has_permission_to_amend_submission(
            self.request.user, self.submission
        ):
            form = forms.SubmissionValidationDepartmentSelectionForm(
                instance=self.submission, data=data
            )

            if not permissions.can_request_submission_validation(
                self.request.user, self.submission
            ):
                forms.disable_form(form)

            return form

        return None

    def get_validation_form(self, data=None, **kwargs):
        if not permissions.has_permission_to_validate_submission(
            self.request.user, self.submission
        ):
            return None

        departments = get_departments(self.request.user)

        try:
            validation, *rest = list(
                self.submission.validations.filter(department__in=departments)
            )
        # User is not part of the requested departments
        except ValueError:
            return None

        if rest:
            logger.error(
                "User %s is a member of more than 1 validation group for submission %s. This is not"
                " implemented yet.",
                self.request.user,
                self.submission,
            )
            return None

        form = forms.SubmissionValidationForm(
            instance=validation,
            data=data,
            user=self.request.user,
            submission=self.submission,
        )
        if not permissions.can_validate_submission(self.request.user, self.submission):
            forms.disable_form(form)

        return form

    def get_poke_form(self, data=None, **kwargs):
        if permissions.has_permission_to_poke_submission(
            self.request.user, self.submission
        ):
            form = forms.SubmissionValidationPokeForm(
                instance=self.submission, request=self.request, data=data
            )
            if not permissions.can_poke_submission(self.request.user, self.submission):
                forms.disable_form(form)

            return form

        return None

    def get_prolongation_form(self, data=None, **kwargs):
        if permissions.has_permission_to_poke_submission(
            self.request.user, self.submission
        ):
            form = forms.SubmissionProlongationForm(instance=self.submission, data=data)

            if not permissions.can_prolonge_submission(
                self.request.user, self.submission
            ):
                forms.disable_form(form)

            return form

        return None

    def get_complementary_documents_formset(self, data=None, **kwargs):
        ComplementaryDocumentsFormSet = formset_factory(
            form=forms.SubmissionComplementaryDocumentsForm,
            extra=1,
        )

        return ComplementaryDocumentsFormSet(
            data,
            kwargs["files"],
            form_kwargs={
                "request": self.request,
                "submission": self.submission,
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
            models.Submission.objects.filter(id=form.instance.id).first().status
        )
        form.save()
        success_message = (
            _("La demande #%s a bien été complétée par le service pilote.")
            % self.submission.pk
        )

        if form.instance.status == models.Submission.STATUS_AWAITING_SUPPLEMENT:
            success_message += " " + _(
                "Le statut de la demande a été passé à en attente de compléments."
            )

        if form.cleaned_data.get("notify_author"):
            success_message += " " + _(
                "Le requérant a été notifié du changement par email."
            )

        messages.success(self.request, success_message)
        if (
            form.instance.status == models.Submission.STATUS_RECEIVED
            and form.instance.status is not initial_status
        ):
            submission = form.instance

            # Notify the submission author
            data = {
                "subject": "{} ({})".format(
                    _("Votre demande/annonce a été prise en compte et classée"),
                    submission.get_forms_names_list(),
                ),
                "users_to_notify": [submission.author.email],
                "template": "submission_received.txt",
                "submission": submission,
                "absolute_uri_func": self.request.build_absolute_uri,
            }
            services.send_email_notification(data)

            # Notify the services
            mailing_list = submission.get_services_to_notify_mailing_list()

            if mailing_list:
                data = {
                    "subject": "{} ({})".format(
                        _(
                            "Une demande/annonce a été prise en compte et classée par le secrétariat"
                        ),
                        submission.get_forms_names_list(),
                    ),
                    "users_to_notify": set(mailing_list),
                    "template": "submission_received_for_services.txt",
                    "submission": submission,
                    "absolute_uri_func": self.request.build_absolute_uri,
                }
                services.send_email_notification(data)

        if "save_continue" in self.request.POST:
            return redirect(
                "submissions:submission_detail",
                submission_id=self.submission.pk,
            )
        else:
            return redirect("submissions:submissions_list")

    def handle_request_validation_form_submission(self, form):
        services.request_submission_validation(
            self.submission,
            form.cleaned_data["departments"],
            self.request.build_absolute_uri,
        )
        messages.success(
            self.request,
            _("La demande #%s a bien été transmise pour validation.")
            % self.submission.pk,
        )

        if "save_continue" in self.request.POST:
            return redirect(
                "submissions:submission_detail",
                submission_id=self.submission.pk,
            )
        else:
            return redirect("submissions:submissions_list")

    def handle_validation_form_submission(self, form):
        validation_object = models.SubmissionValidation.objects.filter(
            submission_id=self.submission.id,
            validated_by_id=self.request.user.id,
        )
        initial_validation_status = (
            (validation_object.first().validation_status)
            if validation_object.exists()
            else models.SubmissionValidation.STATUS_REQUESTED
        )
        form.instance.validated_at = timezone.now()
        form.instance.validated_by = self.request.user
        validation = form.save()

        if validation.validation_status == models.SubmissionValidation.STATUS_APPROVED:
            validation_message = _("Le préavis positif a été enregistré.")
        elif (
            validation.validation_status == models.SubmissionValidation.STATUS_REJECTED
        ):
            validation_message = _("Le préavis négatif a été enregistré.")
        else:
            validation_message = _("Le commentaire a été enregistré.")

        try:

            if not self.submission.get_pending_validations():

                initial_permit_status = self.submission.status
                self.submission.status = models.Submission.STATUS_PROCESSING
                self.submission.save()

                if (
                    initial_permit_status
                    is models.Submission.STATUS_AWAITING_VALIDATION
                    or (
                        initial_permit_status is models.Submission.STATUS_PROCESSING
                        and initial_validation_status
                        is not form.instance.validation_status
                    )
                ):

                    data = {
                        "subject": "{} ({})".format(
                            _(
                                "Les services chargés de la validation d'une demande ont donné leur préavis"
                            ),
                            self.submission.get_forms_names_list(),
                        ),
                        "users_to_notify": self.submission.get_secretary_email(),
                        "template": "submission_validated.txt",
                        "submission": self.submission,
                        "absolute_uri_func": self.request.build_absolute_uri,
                    }
                    services.send_email_notification(data)
            else:
                self.submission.status = models.Submission.STATUS_AWAITING_VALIDATION
                self.submission.save()

        except AttributeError:
            # This is the case when the administrative entity does not have a
            # secretary department associated to a group to which
            # the secretary user belongs.
            pass

        messages.success(self.request, validation_message)

        if "save_continue" in self.request.POST:
            return redirect(
                "submissions:submission_detail",
                submission_id=self.submission.pk,
            )
        else:
            return redirect("submissions:submissions_list")

    def handle_poke(self, form):
        validations = form.save()

        message = ngettext(
            "%s rappel a bien été envoyé.",
            "%s rappels ont bien été envoyés",
            len(validations),
        ) % (len(validations))
        messages.success(self.request, message)

        return redirect("submissions:submissions_list")

    def handle_prolongation_form_submission(self, form):
        form.save()
        if form.instance.prolongation_status:
            success_message = (
                _(
                    "La prolongation de la demande #%s a été traitée et un émail envoyé à l'auteur-e."
                )
                % self.submission.pk
            )

            messages.success(self.request, success_message)

            subject = (
                _("La prolongation de votre demande a été acceptée")
                if form.instance.prolongation_status
                == self.submission.PROLONGATION_STATUS_APPROVED
                else _("La prolongation de votre demande a été refusée")
            )
            data = {
                "subject": "{} ({})".format(
                    subject,
                    form.instance.get_forms_names_list(),
                ),
                "users_to_notify": [form.instance.author.email],
                "template": "submission_prolongation.txt",
                "submission": form.instance,
                "absolute_uri_func": self.request.build_absolute_uri,
            }
            services.send_email_notification(data)

        if "save_continue" in self.request.POST:
            return redirect(
                "submissions:submission_detail",
                submission_id=self.submission.pk,
            )
        else:
            return redirect("submissions:submissions_list")

    def handle_complementary_documents_form_submission(self, form):
        for f in form:
            f.instance.owner = self.request.user
            f.instance.submission = self.submission
            f.save()
            f.save_m2m()

        success_message = (
            _("Les documents ont bien été ajoutés à la demande #%s.")
            % self.submission.pk
        )
        messages.success(self.request, success_message)

        if "save_continue" in self.request.POST:
            target = reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            )
            query_string = urllib.parse.urlencode(
                {"prev_active_form": models.ACTION_COMPLEMENTARY_DOCUMENTS}
            )
            return redirect(f"{target}?{query_string}")

        return redirect("submissions:submissions_list")

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
                    "submissions/submission_confirm_inquiry.html",
                    {
                        "non_public_documents": non_public_documents,
                        "inquiry_form": form,
                        "submission": self.submission,
                    },
                )
        form.instance.submitter = self.request.user
        form.instance.submission = self.submission

        if form.cleaned_data.get("start_date") == datetime.today().date():
            self.submission.start_inquiry()

        form.save()

        success_message = _("La mise en consultation publique a bien été enregistrée")
        messages.success(self.request, success_message)

        return redirect(
            "submissions:submission_detail",
            submission_id=self.submission.pk,
        )


@require_POST
@login_required
@check_mandatory_2FA
def submission_complementary_document_delete(request, pk):
    document = get_object_or_404(models.SubmissionComplementaryDocument.objects, pk=pk)
    author = document.submission.author

    success_url = reverse(
        "submissions:submission_detail",
        kwargs={"submission_id": document.submission_id},
    )

    if author == request.user and not request.user.is_superuser:
        messages.add_message(
            request,
            messages.ERROR,
            _("L'auteur d'une soumission ne peut pas supprimer ses propres documents"),
        )
        return redirect(success_url)

    if document.owner != request.user and not request.user.is_superuser:
        messages.add_message(
            request,
            messages.ERROR,
            _(
                "Vous pouvez seulement supprimer les documents dont vous êtes propriétaire"
            ),
        )
        return redirect(success_url)

    # Final documents can't be deleted!
    if document.status == models.SubmissionComplementaryDocument.STATUS_FINALE:
        messages.add_message(
            request,
            messages.ERROR,
            _("Les documents finaux ne peuvent pas être supprimés"),
        )
        return redirect(success_url)

    document.delete()

    messages.success(
        request, _("Le document '%s' a été supprimé avec succès") % document.document
    )

    return redirect(success_url)


@method_decorator(login_required, name="dispatch")
@method_decorator(permanent_user_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ComplementaryDocumentDownloadView(View):
    def get(self, request, path, *args, **kwargs):
        return services.download_file(path)


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedSubmissionListView(SingleTableMixin, ListView):
    model = models.ArchivedSubmission
    template_name = "submissions/archived_submission_list.html"

    permission_error_message = _(
        "Vous n'avez pas les permissions pour archiver cette demande"
    )
    archive_failed_error_message = _("Une erreur est survenue lors de l'archivage")

    def post(self, request, *args, **kwargs):

        if request.POST.get("action") == "archive-requests":
            return self.archive()

        return HttpResponseNotFound(_("Aucune action spécifiée"))

    def get_queryset(self):
        return models.ArchivedSubmission.objects.filter_for_user(
            self.request.user
        ).order_by("-archived_date")

    def get_table_class(self):
        return tables.ArchivedSubmissionsTable

    def archive(self):
        submission_ids = self.request.POST.getlist("to_archive[]")

        if not submission_ids:
            return HttpResponseNotFound(_("Rien à archiver"))

        department = PermitDepartment.objects.filter(
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
                for submission_id in submission_ids:
                    submission = get_submission_for_user_or_404(
                        self.request.user, submission_id
                    )
                    submission.archive(self.request.user)
        except Exception:
            return JsonResponse(
                data={"message": self.archive_failed_error_message}, status=500
            )

        return JsonResponse({"message": _("Demandes archivées avec succès")})


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedSubmissionDeleteView(DeleteView):
    model = models.ArchivedSubmission
    success_url = reverse_lazy("submissions:archived_submission_list")

    success_message = _("L'archive #%s a été supprimé avec succès")
    error_message = _("Vous n'avez pas les permissions pour supprimer cette archive")

    def post(self, request, *args, **kwargs):

        try:
            archive = models.ArchivedSubmission.objects.get(pk=kwargs.get("pk"))

            if not self.request.user == archive.archivist:
                messages.error(self.request, self.error_message)
                return redirect(self.success_url)

            return super().post(request, *args, **kwargs)
        except models.ArchivedSubmission.DoesNotExist:
            raise SuspiciousOperation

    def get_success_url(self):
        messages.success(self.request, self.success_message % self.object.pk)
        return self.success_url


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedSubmissionDownloadView(View):
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
        return redirect(reverse_lazy("submissions:archived_submission_list"))


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ArchivedSubmissionBulkDownloadView(View):
    permission_error_message = _(
        "Vous n'avez pas les permissions pour télécharger ces archives"
    )
    info_message = _("Rien à télécharger")
    not_exist_error_message = _("Une des archives demandées n'existe pas")

    def get(self, request, *args, **kwargs):
        to_download = self.request.GET.getlist("to_download")
        if not to_download:
            messages.info(request, self.info_message)
            return redirect(reverse_lazy("submissions:archived_submission_list"))

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
        return redirect(reverse_lazy("submissions:archived_submission_list"))


def anonymous_submission_sent(request):
    return render(
        request,
        "submissions/submission_anonymous_sent.html",
        {},
    )


def anonymous_submission(request):
    # Logout silently any real user
    if request.user.is_authenticated and not request.user.userprofile.is_temporary:
        logout(request)

    # Accept only non-logged users, or temporary users
    if not request.user.is_anonymous and not request.user.userprofile.is_temporary:
        raise Http404

    # Validate tags
    entityfilter = request.GET.getlist("entityfilter")
    typefilter = request.GET.getlist("typefilter")
    if not entityfilter or not typefilter:
        raise Http404

    # Validate entity
    entities_by_tag = AdministrativeEntity.objects.public().filter_by_tags(entityfilter)
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
                    "submissions/submission_anonymous_captcha.html",
                    {
                        "anonymous_request_form": anonymous_request_form,
                        "captcha_refresh_url": captcha_refresh_url,
                    },
                )
        else:
            return render(
                request,
                "submissions/submission_anonymous_captcha.html",
                {
                    "anonymous_request_form": forms.AnonymousRequestForm(),
                    "captcha_refresh_url": captcha_refresh_url,
                },
            )

    # Validate type
    form_categories = (
        models.FormCategory.objects.filter(forms__is_anonymous=True)
        .filter_by_tags(typefilter)
        .distinct()
        .values_list("pk", flat=True)
    )

    if len(form_categories) != 1:
        raise Http404
    form_category = form_categories[0]

    # Validate available work objects types
    anonymous_forms = models.Form.anonymous_objects.filter(
        administrative_entities=entity,
        category=form_category,
    )

    if not anonymous_forms:
        raise Http404

    # Submission page

    # Never create a second submission for the same temp_author
    submission, _ = models.Submission.objects.get_or_create(
        administrative_entity=entity,
        author=request.user,
    )

    # If filter combinations return only one anonymous_forms object,
    # this combination must be set on submission object
    if len(anonymous_forms) == 1:
        submission.forms.set(anonymous_forms)

    steps = get_anonymous_steps(
        form_category=form_category,
        user=request.user,
        submission=submission,
        current_site=get_current_site(request),
    )

    for step_type, step in steps.items():
        if step and step.enabled and not step.completed:
            return redirect(step.url)


@redirect_bad_status_to_detail
@login_required
@user_passes_test(has_profile)
@permanent_user_required
@check_mandatory_2FA
def submission_select_administrative_entity(request, submission_id=None):
    current_site = get_current_site(request)

    submission = (
        get_submission_for_edition(request.user, submission_id)
        if submission_id
        else None
    )

    entity_tags = request.GET.getlist("entityfilter")
    entities = get_selectable_entities(
        user=request.user,
        current_site=current_site,
        submission=submission,
        entity_tags=entity_tags,
    )

    if not submission and len(entities) == 1:
        submission = models.Submission.objects.create(
            administrative_entity=entities[0],
            author=request.user,
        )

        selectable_categories = get_selectable_categories(
            submission=submission, category_tags=request.GET.getlist("typefilter")
        )

        candidate_forms = Form.objects.get_default_forms(
            administrative_entity=submission.administrative_entity,
            user=request.user,
            limit_to_categories=selectable_categories,
        )

        # If filter combinations return only one form object that is not exceeded,
        # this combination must be set on submission object
        if len(candidate_forms) == 1 and all(
            [
                not candidate_form.has_exceeded_maximum_submissions()
                for candidate_form in candidate_forms
            ]
        ):
            submission.forms.set(candidate_forms)

        steps = get_progress_bar_steps(request=request, submission=submission)
        return redirect(get_next_step(steps, StepType.ADMINISTRATIVE_ENTITY).url)

    steps_context = progress_bar_context(
        request=request,
        submission=submission,
        current_step_type=StepType.ADMINISTRATIVE_ENTITY,
    )

    administrative_entity_form = forms.AdministrativeEntityForm(
        instance=submission,
        administrative_entities=entities,
        data=request.POST if request.method == "POST" else None,
    )

    if request.method == "POST" and administrative_entity_form.is_valid():
        submission = administrative_entity_form.save(author=request.user)
        selectable_categories = get_selectable_categories(
            submission=submission, category_tags=request.GET.getlist("typefilter")
        )

        submission_forms = Form.objects.get_default_forms(
            administrative_entity=submission.administrative_entity,
            user=request.user,
            limit_to_categories=selectable_categories,
        )
        if submission_forms:
            submission.set_selected_forms(submission_forms)

        steps = get_progress_bar_steps(request=request, submission=submission)

        return redirect(get_next_step(steps, StepType.ADMINISTRATIVE_ENTITY).url)

    return render(
        request,
        "submissions/submission_select_administrative_entity.html",
        {
            "form": administrative_entity_form,
            "submission": submission,
            "entityfilter": entity_tags,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def submission_select_forms(request, submission_id):
    """
    Step to select forms. This view supports either editing an existing submission (if
    `submission_id` is set) or creating a new submission.
    """
    submission = get_submission_for_edition(request.user, submission_id)
    steps_context = progress_bar_context(
        request=request,
        submission=submission,
        current_step_type=StepType.FORMS,
    )

    if submission.administrative_entity.is_single_form_submissions:
        form_class = forms.FormsSingleSelectForm
        steps_context["current_step_title"] = config.FORMS_SINGLE_STEP
    else:
        form_class = forms.FormsSelectForm
        steps_context["current_step_title"] = config.FORMS_STEP

    categories_filters = request.GET.getlist("typefilter")
    if categories_filters:
        selectable_categories = models.FormCategory.objects.filter_by_tags(
            categories_filters
        ).values_list("pk", flat=True)
    else:
        selectable_categories = None

    if request.method == "POST":
        forms_selection_form = form_class(
            data=request.POST,
            instance=submission,
            user=request.user,
            form_categories=selectable_categories,
        )

        if forms_selection_form.is_valid():
            submission = forms_selection_form.save()
            steps = get_progress_bar_steps(request=request, submission=submission)

            return redirect(get_next_step(steps, StepType.FORMS).url)
    else:
        forms_selection_form = form_class(
            instance=submission,
            user=request.user,
            form_categories=selectable_categories,
        )

    return render(
        request,
        "submissions/submission_select_forms.html",
        {
            "forms_selection_form": forms_selection_form,
            "submission": submission,
            "typefilter": categories_filters,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def submission_fields(request, submission_id):
    """
    Step to input fields values for the given submission.
    """
    submission = get_submission_for_edition(request.user, submission_id)
    steps_context = progress_bar_context(
        request=request,
        submission=submission,
        current_step_type=StepType.FIELDS,
    )
    prices_form = None
    requires_online_payment = False

    if submission.requires_online_payment():
        form_payment = submission.get_form_for_payment()
        if form_payment is not None:
            requires_online_payment = form_payment.requires_online_payment

    if request.method == "POST":
        # Disable `required` fields validation to allow partial save
        form = forms.FieldsForm(
            instance=submission, data=request.POST, enable_required=False
        )
        prices_form_valid = True
        if (
            requires_online_payment
            and submission.status == models.Submission.STATUS_DRAFT
        ):
            prices_form = forms.FormsPriceSelectForm(
                instance=submission, data=request.POST
            )
            if prices_form.is_valid():
                prices_form.save()
            else:
                prices_form_valid = False
        if form.is_valid() and prices_form_valid:
            form.save()

            return redirect(get_next_step(steps_context["steps"], StepType.FIELDS).url)
    else:
        form = forms.FieldsForm(instance=submission, enable_required=False)
        if requires_online_payment:
            prices_form = forms.FormsPriceSelectForm(instance=submission)

    return render(
        request,
        "submissions/submission_fields.html",
        {
            "submission": submission,
            "submission_form": form,
            "prices_form": prices_form,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@permanent_user_required
@check_mandatory_2FA
def submission_prolongation(request, submission_id):
    """
    Request prolongation interface for the Permit author.
    """

    if not submission_id:
        messages.success(request, _("Un id de permis valable est requis"))
        return redirect("submissions:submissions_list")

    try:
        submission = get_submission_for_prolongation(request.user, submission_id)
    except NonProlongableSubmission:
        messages.error(request, _("La demande de permis ne peut pas être prolongée."))
        return redirect("submissions:submissions_list")

    if request.method == "POST":

        form = forms.SubmissionProlongationForm(instance=submission, data=request.POST)
        del form.fields["prolongation_status"]
        del form.fields["prolongation_comment"]

        if form.is_valid():
            obj = form.save(commit=False)
            obj.prolongation_status = submission.PROLONGATION_STATUS_PENDING
            obj.save()

            # Send the email to the services
            messages.success(request, _("Votre demande de prolongation a été envoyée"))

            data = {
                "subject": "{} ({})".format(
                    _("Une demande de prolongation vient d'être soumise"),
                    submission.get_forms_names_list(),
                ),
                "users_to_notify": submission.get_secretary_email(),
                "template": "submission_prolongation_for_services.txt",
                "submission": form.instance,
                "absolute_uri_func": request.build_absolute_uri,
            }
            services.send_email_notification(data)

            return redirect("submissions:submissions_list")
    else:
        if submission.author != request.user:
            messages.error(
                request,
                _("Vous ne pouvez pas demander une prolongation pour le permis #%s.")
                % submission.pk,
            )
            return redirect("submissions:submissions_list")

        if submission.prolongation_date and (
            submission.prolongation_status
            in [
                submission.PROLONGATION_STATUS_PENDING,
                submission.PROLONGATION_STATUS_REJECTED,
            ]
        ):
            messages.error(
                request,
                _(
                    "Une demande de prolongation pour le permis #%s est en attente ou a été refusée."
                )
                % submission.pk,
            )
            return redirect("submissions:submissions_list")

        form = forms.SubmissionProlongationForm(instance=submission)
        del form.fields["prolongation_status"]
        del form.fields["prolongation_comment"]

    return render(
        request,
        "submissions/submission_prolongation.html",
        {
            "submission": submission,
            "submission_prolongation_form": form,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def submission_appendices(request, submission_id):
    """
    Step to upload appendices for the given submission.
    """
    submission = get_submission_for_edition(request.user, submission_id)
    steps_context = progress_bar_context(
        request=request,
        submission=submission,
        current_step_type=StepType.APPENDICES,
    )

    if request.method == "POST":
        form = forms.AppendicesForm(
            instance=submission,
            data=request.POST,
            files=request.FILES,
            enable_required=False,
        )

        if form.is_valid():
            try:
                form.save()

                return redirect(
                    get_next_step(steps_context["steps"], StepType.APPENDICES).url
                )
            except:
                messages.error(
                    request,
                    _("Une erreur est survenue lors de l'upload de fichier."),
                )
    else:
        form = forms.AppendicesForm(instance=submission, enable_required=False)

    fields_by_form = form.get_form_fields_by_form()

    return render(
        request,
        "submissions/submission_appendices.html",
        {
            "submission": submission,
            "forms": fields_by_form,
            **steps_context,
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def submission_contacts(request, submission_id):
    submission = get_submission_for_edition(request.user, submission_id)
    steps_context = progress_bar_context(
        request=request,
        submission=submission,
        current_step_type=StepType.CONTACTS,
    )
    requires_payment = submission.requires_payment()

    creditorform = forms.SubmissionCreditorForm(
        request.POST or None, instance=submission
    )

    if request.method == "POST":
        formset = forms.get_submission_contacts_formset_initiated(
            submission, data=request.POST
        )
        if formset.is_valid() and creditorform.is_valid():
            for form in formset:
                if form.has_changed():
                    form.save(submission=submission)
            models.Submission.objects.filter(pk=submission_id).update(
                creditor_type=creditorform.instance.creditor_type
            )

            return redirect(
                get_next_step(steps_context["steps"], StepType.CONTACTS).url
            )
    else:
        formset = forms.get_submission_contacts_formset_initiated(submission)

    userprofile = {
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "company_name": request.user.userprofile.company_name,
        "vat_number": request.user.userprofile.vat_number,
        "address": request.user.userprofile.address,
        "zipcode": request.user.userprofile.zipcode,
        "city": request.user.userprofile.city,
        "phone": request.user.userprofile.phone_first,
    }

    if settings.AUTHOR_IBAN_VISIBLE:
        userprofile["iban"] = request.user.userprofile.iban

    return render(
        request,
        "submissions/submission_contacts.html",
        {
            "formset": formset,
            "creditorform": creditorform,
            "submission": submission,
            "requires_payment": requires_payment,
            "userprofile": userprofile,
            **steps_context,
        },
    )


@login_required
@check_mandatory_2FA
def submission_geo_time(request, submission_id):
    submission = get_submission_for_user_or_404(request.user, submission_id)
    steps_context = progress_bar_context(
        request=request,
        submission=submission,
        current_step_type=StepType.GEO_TIME,
    )
    can_have_multiple_ranges = submission.can_have_multiple_ranges()

    SubmissionGeoTimeFormSet = modelformset_factory(
        models.SubmissionGeoTime,
        form=forms.SubmissionGeoTimeForm,
        extra=0,
        min_num=1,
        can_delete=can_have_multiple_ranges,
    )
    formset = SubmissionGeoTimeFormSet(
        request.POST if request.method == "POST" else None,
        form_kwargs={"submission": submission},
        queryset=submission.geo_time.filter(comes_from_automatic_geocoding=False).all(),
    )

    if request.method == "POST":
        if formset.is_valid():
            with transaction.atomic():
                formset.save()

                for obj in formset.deleted_objects:
                    if obj.pk:
                        obj.delete()

            return redirect(
                get_next_step(steps_context["steps"], StepType.GEO_TIME).url
            )

    title_step = get_geo_step_name_title(submission.get_geotime_required_info())
    return render(
        request,
        "submissions/submission_geo_time.html",
        {
            "formset": formset,
            "submission": submission,
            "can_have_multiple_ranges": can_have_multiple_ranges,
            "geo_title": title_step["title"],
            "geo_step": title_step["step_name"],
            **steps_context,
        },
    )


@login_required
@check_mandatory_2FA
def submission_media_download(request, property_value_id):
    """
    Send the file referenced by the given property value.
    """
    field_value = get_object_or_404(
        models.FieldValue.objects.filter(field__input_type=Field.INPUT_TYPE_FILE),
        pk=property_value_id,
        selected_form__submission__in=models.Submission.objects.filter_for_user(
            request.user
        ),
    )
    file = field_value.get_value()
    mime_type, encoding = mimetypes.guess_type(file.name)

    response = StreamingHttpResponse(file, content_type=mime_type)
    response["Content-Disposition"] = 'attachment; filename="' + file.name + '"'
    return response


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
@method_decorator(permanent_user_required, name="dispatch")
class SubmissionList(ExportMixin, SingleTableMixin, FilterView):
    paginate_by = int(os.environ["PAGINATE_BY"])
    template_name = "submissions/submissions_list.html"

    def _get_form_filter(self):
        return self.request.GET.get("forms", None)

    def get_queryset(self):
        form_filter = self._get_form_filter()
        qs = (
            (
                models.Submission.objects.filter_for_user(
                    self.request.user,
                    form_filter=form_filter,
                )
            )
            .prefetch_related(
                Prefetch(
                    "forms",
                    queryset=Form.objects.select_related("category"),
                )
            )
            .order_by("-created_at")
        )

        if form_filter is not None:
            qs = qs.prefetch_related("selected_forms__field_values__field")

        return qs

    def get_table_data(self):
        form_filter = self._get_form_filter()
        if form_filter:
            return [
                CustomFieldValueAccessibleSubmission(obj) for obj in self.object_list
            ]
        else:
            return self.object_list

    def is_department_user(self):
        return self.request.user.groups.filter(permit_department__isnull=False).exists()

    def _get_extra_column_specs(self, form_filter):
        extra_column_specs = dict()
        for submission in self.object_list:
            for form, fields in submission.get_fields_by_form(
                [
                    models.Field.INPUT_TYPE_FILE_DOWNLOAD,
                    models.Field.INPUT_TYPE_TITLE,
                ],
            ):
                if str(form.pk) != form_filter:
                    continue
                for field in fields:
                    field_id = f"{form_filter}_{field.id}"
                    if field_id not in extra_column_specs:
                        extra_column_specs[field_id] = tableslib.Column(
                            verbose_name=field.name,
                            orderable=True,
                            accessor=f"#{field_id}",
                        )
        return list(extra_column_specs.items())

    def is_exporting(self):
        return bool(self.request.GET.get(self.export_trigger_param, None))

    def get_table_class(self):
        form_filter = self._get_form_filter()

        if self.is_department_user():
            if form_filter:
                extra_columns = self._get_extra_column_specs(form_filter)
                extra_column_names = tuple([col_name for col_name, __ in extra_columns])
            else:
                extra_column_names = tuple()

            if config.ENABLE_GEOCALENDAR:
                extra_column_names += tuple(["shortname", "is_public"])

            table_class = (
                tables.DepartmentSubmissionsExportTable
                if self.is_exporting()
                else tables.DepartmentSubmissionsHTMLTable
            )
            table_class = get_custom_dynamic_table(table_class, extra_column_names)
        else:
            table_class = (
                tables.OwnSubmissionsExportTable
                if self.is_exporting()
                else tables.OwnSubmissionsHTMLTable
            )
        return table_class

    def get_table_kwargs(self):
        form_filter = self._get_form_filter()
        if form_filter:
            return {"extra_column_specs": self._get_extra_column_specs(form_filter)}
        return {}

    def get_filterset_class(self):
        return (
            filters.DepartmentSubmissionFilterSet
            if self.is_department_user()
            else filters.OwnSubmissionFilterSet
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = {key: value[0] for key, value in dict(self.request.GET).items()}
        context["display_clear_filters"] = bool(params)
        params.update({"_export": "xlsx"})
        context["export_csv_url_params"] = urllib.parse.urlencode(params)
        return context


# FIXME rename to submission_request_validation?
@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def submission_submit(request, submission_id):

    submission = get_submission_for_edition(request.user, submission_id)

    incomplete_steps = [
        step.url
        for step in get_progress_bar_steps(request, submission).values()
        if step.errors_count and step.url
    ]

    if request.method == "POST":
        if incomplete_steps:
            raise SuspiciousOperation

        services.submit_submission(submission, request)
        return redirect("submissions:submissions_list")

    should_go_to_payment = (
        submission.requires_online_payment()
        and submission.status == models.Submission.STATUS_DRAFT
    )

    has_any_form_with_exceeded_submissions = (
        submission.has_any_form_with_exceeded_submissions()
    )

    return render(
        request,
        "submissions/submission_submit.html",
        {
            "submission": submission,
            "should_go_to_payment": should_go_to_payment,
            "has_any_form_with_exceeded_submissions": has_any_form_with_exceeded_submissions,
            "directives": submission.get_submission_directives(),
            "incomplete_steps": incomplete_steps,
            **progress_bar_context(
                request=request,
                submission=submission,
                current_step_type=StepType.SUBMIT,
            ),
        },
    )


@redirect_bad_status_to_detail
@login_required
@check_mandatory_2FA
def submission_submit_confirmed(request, submission_id):

    submission = get_submission_for_edition(request.user, submission_id)
    if submission.has_any_form_with_exceeded_submissions():
        messages.add_message(
            request,
            messages.ERROR,
            submission.get_maximum_submissions_message(),
        )
        return redirect("submissions:submission_submit", submission_id=submission_id)

    incomplete_steps = [
        step.url
        for step in get_progress_bar_steps(request, submission).values()
        if step.errors_count and step.url
    ]

    if incomplete_steps:
        raise SuspiciousOperation

    services_to_notify_and_message = models.FieldValue.objects.filter(
        selected_form__submission=submission, value={"val": True}
    ).values_list(
        "field__services_to_notify", "field__message_for_notified_services", named=True
    )

    if services_to_notify_and_message.exists():
        for notification in services_to_notify_and_message:
            services_to_notify = notification.field__services_to_notify
            message_for_notified_services = (
                notification.field__message_for_notified_services
                if notification.field__message_for_notified_services
                else None
            )
            mailing_list = []
            emails_addresses = services_to_notify.replace("\n", ",").split(",")
            mailing_list += [
                ea.strip()
                for ea in emails_addresses
                if services.validate_email(ea.strip())
            ]
            if mailing_list:
                data = {
                    "subject": "{} ({})".format(
                        _("Votre service à été mentionné dans une demande/annonce"),
                        submission.get_forms_names_list(),
                    ),
                    "users_to_notify": set(mailing_list),
                    "template": "submission_submitted_with_mention.txt",
                    "submission": submission,
                    "absolute_uri_func": request.build_absolute_uri,
                    "message_for_notified_services": message_for_notified_services,
                }
                services.send_email_notification(data)

    # Only submit request when it's editable by author, to prevent a "raise SuspiciousOperation"
    # When editing a submission, submit isn't required to save the modifications, as every view saves the updates
    if submission.can_be_edited_by_author():
        services.submit_submission(submission, request)

    user_is_backoffice_or_integrator_for_administrative_entity = request.user.groups.filter(
        Q(permit_department__administrative_entity=submission.administrative_entity),
        Q(permit_department__is_backoffice=True)
        | Q(permit_department__is_integrator_admin=True),
    )

    # Backoffice and integrators creating a submission for their own administrative
    # entity, are directly redirected to the permit detail
    # Same flow for requests when submission can't be edited by author
    if (
        user_is_backoffice_or_integrator_for_administrative_entity
        and not submission.can_be_edited_by_author()
    ):
        return redirect("submissions:submission_detail", submission_id=submission_id)
    else:

        if request.user.userprofile.is_temporary and submission.author == request.user:
            try:
                anonymous_user = submission.administrative_entity.anonymous_user
            except ObjectDoesNotExist:
                # Might happen only if the entity's anonymous user has been removed
                # between the creation and the submission of the submission
                raise Http404
            else:
                submission.author = anonymous_user.user
                submission.save()
                temp_user = request.user
                logout(request)
                temp_user.delete()
                return redirect("submissions:anonymous_submission_sent")

        return redirect("submissions:submissions_list")


@redirect_bad_status_to_detail
@login_required
@permanent_user_required
@check_mandatory_2FA
def submission_delete(request, submission_id):
    submission = get_submission_for_edition(request.user, submission_id)

    if request.method == "POST":
        submission.delete()

        return redirect("submissions:submissions_list")

    return render(
        request,
        "submissions/submission_delete.html",
        {"submission": submission},
    )


def submission_approve(request, submission_id):
    return submission_classify(request, submission_id, approve=True)


def submission_reject(request, submission_id):
    return submission_classify(request, submission_id, approve=False)


@login_required
@permanent_user_required
@permission_required("submissions.classify_submission")
@check_mandatory_2FA
def submission_classify(request, submission_id, approve):

    submission = get_submission_for_user_or_404(
        request.user,
        submission_id,
        statuses=[
            models.Submission.STATUS_AWAITING_VALIDATION,
            models.Submission.STATUS_PROCESSING,
        ],
    )
    if not permissions.can_classify_submission(request.user, submission):
        raise Http404

    initial = {
        "status": (
            models.Submission.STATUS_APPROVED
            if approve
            else models.Submission.STATUS_REJECTED
        )
    }
    title = (
        _("Approbation de la demande #%s") if approve else _("Refus de la demande #%s")
    ) % submission.pk

    if request.method == "POST":
        classify_form = forms.SubmissionClassifyForm(
            instance=submission,
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
                    submission.get_forms_names_list(),
                ),
                "users_to_notify": [submission.author.email],
                "template": "submission_classified.txt",
                "submission": submission,
                "absolute_uri_func": request.build_absolute_uri,
            }
            services.send_email_notification(data)

            # Notify the services
            mailing_list = submission.get_services_to_notify_mailing_list()

            if mailing_list:
                data = {
                    "subject": "{} ({})".format(
                        _("Une demande a été traitée et classée par le secrétariat"),
                        submission.get_forms_names_list(),
                    ),
                    "users_to_notify": set(mailing_list),
                    "template": "submission_classified_for_services.txt",
                    "submission": submission,
                    "absolute_uri_func": request.build_absolute_uri,
                }
                services.send_email_notification(data)

            return redirect("submissions:submissions_list")
    else:
        classify_form = forms.SubmissionClassifyForm(
            instance=submission, initial=initial
        )

    return render(
        request,
        "submissions/submission_classify.html",
        {
            "submission": submission,
            "approve": approve,
            "form": classify_form,
            "title": title,
        },
    )


@login_required
@permanent_user_required
def submission_file_download(request, path):
    """
    Securely download the submission file at the given `path`. The path must start with the submission id, such
    as returned by the `SubmissionFieldFile`.

    If the user doesn't have access to the submission identified by the given id, return an HTTP 404 error.
    """
    try:
        submission_id, _ = path.split("/", maxsplit=1)
    except ValueError:
        raise Http404

    get_submission_for_user_or_404(request.user, submission_id)
    return services.download_file(path)


@login_required
def field_file_download(request, path):
    """
    Download the wot file at the given `path` as an attachment.
    """
    return services.download_file(path)


@login_required
@permanent_user_required
def submissions_search(request):
    terms = request.GET.get("search")

    if len(terms) >= 2:
        submissions = models.Submission.objects.filter_for_user(
            request.user
        ).prefetch_related("price__transactions")
        results = search_submissions(
            search_str=terms, submissions_qs=submissions, limit=5
        )
    else:
        results = []

    return JsonResponse(
        {"results": [search_result_to_json(result) for result in results]}
    )


@login_required
def administrative_entities_geojson(request, administrative_entity_id):
    administrative_entity = AdministrativeEntity.objects.filter(
        id=administrative_entity_id
    )

    geojson = json.loads(
        serialize(
            "geojson",
            administrative_entity,
            geometry_field="geom",
            srid=2056,
            fields=(
                "id",
                "name",
            ),
        )
    )

    return JsonResponse(geojson, safe=False)


@method_decorator(login_required, name="dispatch")
@method_decorator(check_mandatory_2FA, name="dispatch")
class ChangeTransactionStatus(View):
    permission_error_message = _(
        "Vous n'avez pas les permissions pour changer le statut de cette transaction"
    )
    not_exist_error_message = _("La transaction demandée n'existe pas")

    def get(self, request, *args, **kwargs):
        try:
            merchant_reference = kwargs.get("merchant_reference")
            new_status = request.GET.get("new_status")

            transaction = get_transaction_from_merchant_reference(merchant_reference)
            submission = transaction.submission_price.submission
            if not permissions.user_has_permission_to_change_transaction_status(
                request.user, transaction, new_status
            ):
                raise PermissionDenied

            transaction.set_new_status(new_status)

            if new_status == transaction.STATUS_REFUNDED:
                submission.generate_and_save_pdf("refund", transaction)
                send_refund_email(request, submission)

            redirect_page = reverse_lazy(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            )
            redirect_page = f"{redirect_page}?prev_active_form=payments"

            new_status_display = transaction.get_status_display().lower()
            merchant_site = transaction.CHECKOUT_PROCESSOR_ID

            messages.success(
                request,
                mark_safe(
                    _(
                        """Le statut de la transaction {merchant_reference} a été mis à jour en
                    <strong>{new_status_display}</strong>
                    """
                    ).format(
                        new_status_display=new_status_display,
                        merchant_reference=merchant_reference,
                    )
                ),
            )
            if transaction.requires_action_on_merchant_site(new_status):
                messages.warning(
                    request,
                    _(
                        "Ne pas oublier d'également mettre à jour la transaction dans {merchant_site}"
                    ).format(merchant_site=merchant_site),
                )
            return redirect(redirect_page)
        except PermissionDenied:
            error_message = self.permission_error_message
        except ObjectDoesNotExist:
            error_message = self.not_exist_error_message

        messages.error(request, error_message)

        return redirect(reverse_lazy("submissions:submissions_list"))


@method_decorator(login_required, name="dispatch")
class ConfirmTransactionCallback(View):
    def get(self, request, pk, *args, **kwargs):
        transaction = get_transaction_from_id(pk)
        submission = transaction.submission_price.submission

        submission.generate_and_save_pdf("confirmation", transaction)

        if (
            not request.user == submission.author
            or not transaction.status == transaction.STATUS_UNPAID
        ):
            raise PermissionDenied

        processor = get_payment_processor(submission.get_form_for_payment())
        if processor.is_transaction_authorized(transaction):
            transaction.set_paid()
            submission_submit_confirmed(request, submission.pk)

            return render(
                request,
                "submissions/submission_payment_callback_confirm.html",
                {
                    "submission": submission,
                },
            )

        transaction.set_failed()
        return render(
            request,
            "submissions/submission_payment_callback_fail.html",
            {
                "submission": submission,
                "submission_url": reverse(
                    "submissions:submission_submit",
                    kwargs={"submission_id": submission.pk},
                ),
            },
        )


@method_decorator(login_required, name="dispatch")
class FailTransactionCallback(View):
    def get(self, request, pk, *args, **kwargs):
        transaction = get_transaction_from_id(pk)
        submission = transaction.submission_price.submission
        if not request.user == submission.author:
            raise PermissionDenied

        transaction.set_failed()

        return render(
            request,
            "submissions/submission_payment_callback_fail.html",
            {
                "submission": submission,
                "submission_url": reverse(
                    "submissions:submission_fields",
                    kwargs={"submission_id": submission.pk},
                ),
            },
        )


@method_decorator(login_required, name="dispatch")
class SubmissionPaymentRedirect(View):
    def get(self, request, pk, *args, **kwargs):
        submission = models.Submission.objects.get(pk=pk)

        if submission.has_any_form_with_exceeded_submissions():
            messages.add_message(
                request,
                messages.ERROR,
                submission.get_maximum_submissions_message(),
            )
            return redirect(
                "submissions:submission_submit", submission_id=submission.pk
            )

        if (
            submission.requires_online_payment()
            and submission.status == models.Submission.STATUS_DRAFT
        ) or request.user != submission.author:
            processor = get_payment_processor(submission.get_form_for_payment())
            payment_url = processor.create_transaction_and_return_payment_page_url(
                submission, request
            )
            return redirect(payment_url)

        return redirect(reverse_lazy("submissions:submissions_list"))


# TODO: SET PERMISSIONS
@login_required
@check_mandatory_2FA
def submission_validations_edit(request, submission_id):

    # Check that user is authorize to see submission
    submission = get_object_or_404(
        models.Submission.objects.filter_for_user(request.user), pk=submission_id
    )

    # Check that user is authorized to edit submission validations
    if not permissions.has_permission_to_edit_submission_validations(
        request.user, submission
    ):
        # TODO: be nicer whith user
        raise PermissionDenied

    submissionValidationFormset = modelformset_factory(
        models.SubmissionValidation,
        form=forms.SubmissionValidationsForm,
        edit_only=True,
        extra=0,
    )
    if request.method == "POST":
        if request.method == "POST":
            formset = submissionValidationFormset(request.POST)
            if formset.is_valid():
                formset.save()
                if "save_continue" in request.POST:
                    return redirect(
                        "submissions:submission_validations_edit",
                        submission_id=submission_id,
                    )
                else:
                    return redirect(
                        "submissions:submission_detail",
                        submission_id=submission_id,
                    )

    else:
        formset = submissionValidationFormset(
            queryset=models.SubmissionValidation.objects.filter(
                submission=submission_id
            )
        )
    return render(
        request,
        "submissions/submission_validations_edit.html",
        {
            "formset": formset,
        },
    )
