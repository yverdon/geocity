import os, datetime
from weasyprint import HTML, CSS
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import urllib.parse
import urllib.request
from uuid import uuid4
from . import services, models


def get_permit_request_for_edition(user, permit_request_id):
    return services.get_permit_request_for_user_or_404(
        user,
        permit_request_id,
        statuses=[
            models.PermitRequest.STATUS_DRAFT,
            models.PermitRequest.STATUS_AWAITING_SUPPLEMENT
        ]
    )


def printreport(request, permit_request_id):

    permit_request = get_permit_request_for_edition(request.user, permit_request_id)

    print_date = datetime.datetime.now()

    html = render(request, "permits/print/printpermit.html", {
        'permit_request': permit_request,
    })

    pdf_file = HTML(string=html.content,  base_url=request.build_absolute_uri()).write_pdf()
    file_path = 'tutu'
    return pdf_file, file_path
