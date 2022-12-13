from django.shortcuts import get_object_or_404

from . import models
from .exceptions import BadSubmissionStatus


def get_submission_for_user_or_404(user, submission, statuses=None):
    """
    Return the submission with `submission` or raise an Http404 if there is no such submission. The
    submission must either belong to the given user, or the given user should be in the same administrative entity.
    If `statuses` is set and a submission is found but its status doesn't match any value in `statuses`,
    `BadSubmissionStatus` will be raised.
    """
    permit_request = get_object_or_404(
        models.Submission.objects.filter_for_user(user), pk=submission
    )

    if statuses is not None and permit_request.status not in statuses:
        raise BadSubmissionStatus(permit_request, statuses)

    return permit_request
