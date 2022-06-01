from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from permits.serializers import PermitRequestPrintSerializer
from django.shortcuts import get_object_or_404
from django_weasyprint.views import WeasyTemplateView


from permits.decorators import permanent_user_required

from permits.models import PermitRequest
from .models import Report
from django.http import FileResponse, HttpResponse


@login_required
@permanent_user_required
def report_view(request, permit_request_id, report_id, as_html=False):

    # TODO CRITICAL: ensure user has permissions on permit
    permit_request = get_object_or_404(PermitRequest, pk=permit_request_id)
    # TODO CRITICAL: ensure print setup is part of WorksObjectType
    report = get_object_or_404(Report, pk=report_id)

    if as_html:
        return HttpResponse(report.render_string(permit_request))
    else:
        file = report.render_pdf(permit_request)
        response = FileResponse(file)
        response["Content-Disposition"] = 'inline; filename="report.pdf"'
        response["Content-Type"] = 'application/pdf'
        return response
