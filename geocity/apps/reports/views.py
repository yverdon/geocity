from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

from geocity.apps.accounts.decorators import permanent_user_required
from geocity.apps.api.serializers import SubmissionPrintSerializer
from geocity.apps.submissions import services

from .models import Report
from .permissions import user_is_allowed_to_generate_report
from .services import generate_report_pdf_as_response


# TODO: instead of taking Submission and Form arguments, we should take
# in SelectedForm, which already joins both, so they are consistent.
@api_view(["GET"])  # pretend it's a DRF view, so we get token auth
@login_required
@permanent_user_required
def report_content(request, submission_id, form_id, report_id):
    """This views returns the content of a report in HTML. It is mainly meant to be rendered
    to PDF (but could also work as a PDF)"""

    # Ensure user is allowed to generate pdf
    submission, form = user_is_allowed_to_generate_report(
        request.user, submission_id, form_id, report_id
    )

    report = get_object_or_404(Report, pk=report_id)

    # Prepare the base context for rendering sections
    request_json_data = SubmissionPrintSerializer(submission).data
    form_key = form.name + (f" ({form.category.name})" if form.category_id else "")
    request_props = request_json_data["properties"]["submission_fields"][form_key]
    amend_props = request_json_data["properties"]["amend_fields"][form_key]
    base_section_context = {
        "submission": submission,
        "request_data": request_json_data,
        "form_data": {
            "request_properties": request_props,
            "amend_properties": amend_props,
        },
    }

    # Render all sections
    rendered_sections = []
    for section in report.sections.all():
        template = f"reports/sections/{section.__class__.__name__.lower()}.html"
        section_context = section.prepare_context(request, base_section_context)
        rendered_sections.append(render_to_string(template, section_context))

    # Render the report
    context = {
        **base_section_context,
        "report": report,
        "rendered_sections": rendered_sections,
    }
    return render(request, "reports/report.html", context)


# TODO: instead of taking Submission and Form arguments, we should take
# in SelectedForm, which already joins both, so they are consistent.
@login_required
@permanent_user_required
def report_pdf(request, submission_id, form_id, report_id):
    return generate_report_pdf_as_response(
        request.user, submission_id, form_id, report_id
    )


@api_view(["GET"])  # pretend it's a DRF view, so we get token auth
@login_required
@permanent_user_required
def background_download(request, path):
    """
    Download the background file at the given `path` as an attachment.
    """
    return services.download_file(path)
