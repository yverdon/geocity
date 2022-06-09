from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from permits.serializers import PermitRequestPrintSerializer
from django.shortcuts import get_object_or_404
from django_weasyprint.views import WeasyTemplateView
from django.urls import reverse
import requests
import io
from permits.decorators import permanent_user_required
from rest_framework.authtoken.models import Token
from permits.models import PermitRequest
from .models import Report
from django.http import FileResponse, HttpResponse, HttpResponseServerError
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


@api_view(http_method_names=['GET'])  # enable token authentication
@authentication_classes([TokenAuthentication, SessionAuthentication])  # enable token authentication
@login_required
@permanent_user_required
def report_view_contents(request, permit_request_id, report_id):
    """This views renders a report content as a regular Django view returning HTML.
    It is meant for internal access by the PDF generation service."""

    # TODO CRITICAL: ensure user has permissions on permit
    permit_request = get_object_or_404(PermitRequest, pk=permit_request_id)
    # TODO CRITICAL: ensure print setup is part of WorksObjectType
    report = get_object_or_404(Report, pk=report_id)
    return HttpResponse(report.render_string(permit_request, request))


@login_required
@permanent_user_required
def report_view(request, permit_request_id, report_id):
    """This views returns a PDF."""
    # TODO CRITICAL: ensure user has permissions on permit
    permit_request = get_object_or_404(PermitRequest, pk=permit_request_id)
    # TODO CRITICAL: ensure print setup is part of WorksObjectType
    report = get_object_or_404(Report, pk=report_id)
    pdf_content = report.render_pdf(permit_request, generated_by=request.user)
    response = FileResponse(io.BytesIO(pdf_content))
    response["Content-Disposition"] = 'inline; filename="report.pdf"'
    response["Content-Type"] = "application/pdf"
    return response
