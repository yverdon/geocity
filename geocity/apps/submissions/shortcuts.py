from django.shortcuts import get_object_or_404

from . import models
from .exceptions import BadSubmissionStatus
from .payments.models import ServicesFees


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
        # TODO: this is not raised properly: FIXME.
        raise BadSubmissionStatus(permit_request, statuses)

    return permit_request


def get_service_fee_for_user_or_404(user, service_fee_id, statuses=None):
    """
    Return the submission with `submission_id` or raise an Http404 if there is no such submission. The
    submission must either belong to the given user, or the given user should be in the same administrative entity.
    If `statuses` is set and a submission is found but its status doesn't match any value in `statuses`,
    `BadSubmissionStatus` will be raised.
    """
    service_fee = get_object_or_404(ServicesFees.objects.filter(pk=service_fee_id))

    return service_fee
