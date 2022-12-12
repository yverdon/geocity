from django.http import Http404
from django.shortcuts import get_object_or_404

from geocity.apps.forms.models import Form
from geocity.apps.submissions.models import ComplementaryDocumentType, Submission


def user_is_allowed_to_generate_report(user, submission_id, form_id, report_id):

    # Check that user has permission to generate pdf
    if not (user.has_perm("reports.can_generate_pdf") or user.is_superuser):
        raise Http404

    # Check that user is allowed to see the current permit_request
    permit_request = get_object_or_404(
        Submission.objects.filter_for_user(user), pk=submission_id
    )

    # Check the current form_id is allowed for user
    # The form list is associated to a submission, thus a user that have
    # access to the submission, also has access to all forms associated with it
    if int(form_id) not in permit_request.forms.values_list("pk", flat=True):
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
    if not children_document_exists:
        raise Http404

    return permit_request, form
