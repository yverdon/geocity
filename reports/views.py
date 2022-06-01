from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from permits.serializers import PermitRequestPrintSerializer
from django.shortcuts import get_object_or_404
from django_weasyprint.views import WeasyTemplateView

from permits.decorators import permanent_user_required

from permits.models import PermitRequest
from .models import Report


@method_decorator(login_required, name="dispatch")
@method_decorator(permanent_user_required, name="dispatch")
class ReportView(WeasyTemplateView):
    # uncomment to download file as attachment
    # pdf_filename = 'download.pdf'
    template_name = "reports/report.html"

    def get_context_data(self, permit_request_id, report_id):
        # TODO CRITICAL: ensure user has permissions on permit
        permit_request = get_object_or_404(PermitRequest, pk=permit_request_id)
        # TODO CRITICAL: ensure print setup is part of WorksObjectType
        report = get_object_or_404(Report, pk=report_id)

        return {
            "report": report,
            "permit_request": permit_request,
            "permit_request_data": PermitRequestPrintSerializer(permit_request).data,
        }
