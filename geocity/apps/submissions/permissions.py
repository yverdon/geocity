from geocity.apps.accounts.users import get_administrative_entities_associated_to_user

from . import models


def has_permission_to_amend_submission(user, submission):
    return user.has_perm(
        "submissions.amend_submission"
    ) and submission.administrative_entity in get_administrative_entities_associated_to_user(
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
    ) and submission.administrative_entity in get_administrative_entities_associated_to_user(
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
    ) and submission.administrative_entity in get_administrative_entities_associated_to_user(
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
