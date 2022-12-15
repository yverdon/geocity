from django.http import Http404
from django.shortcuts import get_object_or_404

from geocity.apps.accounts.models import AdministrativeEntity

from ..forms.models import Form
from . import models
from .models import ComplementaryDocumentType, Submission


def has_permission_to_amend_submission(user, submission):
    return user.has_perm(
        "submissions.amend_submission"
    ) and submission.administrative_entity in AdministrativeEntity.objects.associated_to_user(
        user
    )


def can_amend_submission(user, submission):
    return submission.can_be_amended() and has_permission_to_amend_submission(
        user, submission
    )


def can_prolonge_submission(user, submission):
    return submission.can_be_prolonged() and has_permission_to_amend_submission(
        user, submission
    )


def can_request_submission_validation(user, submission):
    return (
        submission.can_be_sent_for_validation()
        and has_permission_to_amend_submission(user, submission)
    )


def has_permission_to_validate_submission(user, submission):
    return (
        user.has_perm("submissions.validate_submission")
        and models.Submission.objects.filter_for_user(user)
        .filter(pk=submission.pk)
        .exists()
    )


def can_validate_submission(user, submission):
    return submission.can_be_validated() and has_permission_to_validate_submission(
        user, submission
    )


def has_permission_to_poke_submission(user, submission):
    return user.has_perm(
        "submissions.amend_submission"
    ) and submission.administrative_entity in AdministrativeEntity.objects.associated_to_user(
        user
    )


def can_poke_submission(user, submission):
    return (
        submission.status == models.Submission.STATUS_AWAITING_VALIDATION
        and has_permission_to_poke_submission(user, submission)
    )


def has_permission_to_classify_submission(user, submission):
    return user.has_perm(
        "submissions.amend_submission"
    ) and submission.administrative_entity in AdministrativeEntity.objects.associated_to_user(
        user
    )


def can_classify_submission(user, submission):
    status_choices_for_administrative_entity = (
        models.SubmissionWorkflowStatus.objects.get_statuses_for_administrative_entity(
            submission.administrative_entity
        )
    )
    no_validation_process = (
        models.Submission.STATUS_AWAITING_VALIDATION
        not in status_choices_for_administrative_entity
        and models.Submission.STATUS_APPROVED
        in status_choices_for_administrative_entity
        and models.Submission.STATUS_REJECTED
        in status_choices_for_administrative_entity
        and submission.status == models.Submission.STATUS_PROCESSING
    )
    return (
        submission.status == models.Submission.STATUS_PROCESSING
        and submission.get_pending_validations().count() == 0
        and has_permission_to_classify_submission(user, submission)
    ) or no_validation_process


def has_permission_to_edit_submission(user, submission):
    return (
        user.has_perm("submissions.edit_submission")
        and models.Submission.objects.filter_for_user(user)
        .filter(pk=submission.pk)
        .exists()
    )


def can_edit_submission(user, submission):
    return (
        submission.can_be_edited_by_pilot()
        and has_permission_to_edit_submission(user, submission)
        or can_always_be_updated(user, submission)
    )


def can_always_be_updated(user, submission):
    can_always_update = submission.forms.filter(can_always_update=True).exists()
    user_is_integrator_admin = user.groups.filter(
        permit_department__is_integrator_admin=True
    ).exists()
    user_is_backoffice = user_is_integrator_admin = user.groups.filter(
        permit_department__is_backoffice=True
    ).exists()
    user_is_superuser = user.is_superuser
    return can_always_update and (
        user_is_integrator_admin or user_is_backoffice or user_is_superuser
    )


def can_download_archive(user, archivist):
    return (
        user == archivist
        or user.is_superuser
        or (user.groups.all() & archivist.groups.all()).exists()
    )


def can_revert_refund_transaction(user, transaction):
    submission = transaction.submission_price.submission
    return user.is_superuser or (
        user.has_perm("submissions.can_revert_refund_transactions")
        and submission.administrative_entity
        in AdministrativeEntity.objects.associated_to_user(user)
    )


def can_refund_transaction(user, transaction):
    submission = transaction.submission_price.submission
    return user.is_superuser or (
        user.has_perm("submissions.can_refund_transactions")
        and submission.administrative_entity
        in AdministrativeEntity.objects.associated_to_user(user)
    )


def user_has_permission_to_change_transaction_status(user, transaction, new_status):
    if new_status in (transaction.STATUS_REFUNDED, transaction.STATUS_TO_REFUND):
        permission_check = can_refund_transaction
    elif new_status == transaction.STATUS_PAID:
        permission_check = can_revert_refund_transaction
    else:
        return False
    return permission_check(user, transaction)


def user_is_allowed_to_generate_report(user, submission_id, form_id, report_id):
    # Check that user is allowed to see the current permit_request
    submission = get_object_or_404(
        Submission.objects.filter_for_user(user), pk=submission_id
    )

    # Check if report is linked to payments
    form_for_payment = submission.get_form_for_payment()
    is_linked_to_payment = (
        form_for_payment
        and form_for_payment.payment_settings
        and (
            form_for_payment.payment_settings.payment_confirmation_report.pk
            == report_id
            or form_for_payment.payment_settings.payment_refund_report.pk == report_id
        )
    )

    # Check that user has permission to generate pdf
    if not is_linked_to_payment and (
        not (user.has_perm("reports.can_generate_pdf") or user.is_superuser)
    ):
        raise Http404

    # Check the current form_id is allowed for user
    # The form list is associated to a submission, thus a user that have
    # access to the submission, also has access to all forms associated with it
    if int(form_id) not in submission.forms.values_list("pk", flat=True):
        raise Http404

    form = get_object_or_404(Form, pk=form_id)

    # Check the user is allowed to use this report template

    # List parents documents for a given form
    document_parent_list = ComplementaryDocumentType.objects.filter(
        form_id=form_id, parent__isnull=True
    )

    # Check if there's a children document with the same report id as the request
    children_document_exists = ComplementaryDocumentType.objects.filter(
        parent__in=document_parent_list, reports__id=report_id
    ).exists()

    # FIXME
    #  - Add children documents in fixtures ?
    #  - Raise a more specific error ?
    # if not children_document_exists:
    #     raise Http404

    return submission, form
