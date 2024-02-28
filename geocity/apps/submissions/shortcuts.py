from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from . import models
from .exceptions import BadSubmissionStatus


def get_submission_for_user_or_404(user, submission_id, statuses=None):
    """
    Return the submission with `submission_id` or raise an Http404 if there is no such submission. The
    submission must either belong to the given user, or the given user should be in the same administrative entity.
    If `statuses` is set and a submission is found but its status doesn't match any value in `statuses`,
    `BadSubmissionStatus` will be raised.
    """
    permit_request = get_object_or_404(
        models.Submission.objects.filter_for_user(user), pk=submission_id
    )
    if statuses is not None and permit_request.status not in statuses:
        raise BadSubmissionStatus(permit_request, statuses)

    return permit_request


def get_displayable_service_fee_provided_by_for_validators(administrative_entity, user):
    """
    Return list of validator users for provided_by field.
    The value is based on the logged user
    Mostly used to manage ServiceFee view and what should be displayed
    """

    administrative_entity_filter = Q(
        permit_department__administrative_entity=administrative_entity,
    )
    validator_filter = Q(permit_department__is_validator=True)

    current_user_groups = user.groups.all()

    current_user_administrative_entity_groups = current_user_groups.filter(
        administrative_entity_filter & validator_filter
    )

    displayable_provided_by_users = User.objects.filter(
        groups__in=current_user_administrative_entity_groups
    ).distinct()

    return displayable_provided_by_users
