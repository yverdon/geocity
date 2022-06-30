from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from knox.models import AuthToken
from rest_framework.decorators import api_view

from permits import services
from permits.decorators import permanent_user_required
from permits.models import ComplementaryDocumentType, WorksObjectType
from permits.serializers import PermitRequestPrintSerializer

from .models import Report
from .utils import run_docker_container


def user_is_allowed_to_generate_report(
    request, permit_request_id, work_object_type_id, report_id
):

    # Check that user has permission to generate pdf
    if not (
        request.user.has_perm("reports.can_generate_pdf") or request.user.is_superuser
    ):
        raise Http404

    # Check that user is allowed to see the current permit_request
    permit_request = get_object_or_404(
        services.get_permit_requests_list_for_user(request.user), pk=permit_request_id
    )

    # Check the current work_object_type_id is allowed for user
    # The wot list is associated to a permitrequest, thus a user that have
    # access to the permitrequest, also has access to all wots associated with it
    if int(work_object_type_id) not in permit_request.works_object_types.values_list(
        "pk", flat=True
    ):
        raise Http404

    work_object_type = get_object_or_404(WorksObjectType, pk=work_object_type_id)

    # Check the user is allowed to use this report template

    # List parents documents for a given WOT
    document_parent_list = ComplementaryDocumentType.objects.filter(
        work_object_types__pk=work_object_type_id, parent__isnull=True
    )

    # Check if there's a children document with the same report id as the request
    children_document_exists = ComplementaryDocumentType.objects.filter(
        parent__in=document_parent_list, reports__id=report_id
    ).exists()
    if not children_document_exists:
        raise Http404

    return permit_request, work_object_type


# TODO: instead of taking PermitRequest and WorksObjectType arguments, we should take
# in WorksObjectTypeChoice, which already joins both, so they are consistent.
@api_view(["GET"])  # pretend it's a DRF view, so we get token auth
@login_required
@permanent_user_required
def report_content(request, permit_request_id, work_object_type_id, report_id):
    """This views returns the content of a report in HTML. It is mainly meant to be rendered
    to PDF (but could also work as a PDF)"""

    # Ensure user is allowed to generate pdf
    permit_request, work_object_type = user_is_allowed_to_generate_report(
        request, permit_request_id, work_object_type_id, report_id
    )

    report = get_object_or_404(Report, pk=report_id)

    # Prepare the base context for rendering sections
    request_json_data = PermitRequestPrintSerializer(permit_request).data
    wot_key = (
        f"{work_object_type.works_object.name} ({work_object_type.works_type.name})"
    )
    request_props = request_json_data["properties"]["request_properties"][wot_key]
    amend_props = request_json_data["properties"]["amend_properties"][wot_key]
    base_section_context = {
        "permit_request": permit_request,
        "request_data": request_json_data,
        "wot_data": {
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


# TODO: instead of taking PermitRequest and WorksObjectType arguments, we should take
# in WorksObjectTypeChoice, which already joins both, so they are consistent.
@login_required
@permanent_user_required
def report_pdf(request, permit_request_id, work_object_type_id, report_id):

    # Ensure user is allowed to generate pdf
    user_is_allowed_to_generate_report(
        request, permit_request_id, work_object_type_id, report_id
    )

    authtoken, token = AuthToken.objects.create(
        request.user, expiry=timedelta(minutes=5)
    )

    url = reverse(
        "reports:permit_request_report_content",
        kwargs={
            "permit_request_id": permit_request_id,
            "work_object_type_id": work_object_type_id,
            "report_id": report_id,
        },
    )

    commands = [
        f"http://web:9000{url}",
        "/io/output.pdf",
        token,
    ]

    output = run_docker_container(
        "geocity_pdf",
        commands,
        file_output="/io/output.pdf",
    )

    authtoken.delete()

    now = timezone.now()

    response = FileResponse(
        output, filename=f"autogenerated_report_{now:%Y-%m-%d}.pdf", as_attachment=False
    )
    # response["Content-Disposition"] = 'inline; filename="report.pdf"'
    response["Content-Type"] = "application/pdf"
    return response


@api_view(["GET"])  # pretend it's a DRF view, so we get token auth
@login_required
@permanent_user_required
def background_download(request, path):
    """
    Download the background file at the given `path` as an attachment.
    """
    return services.download_file(path)
