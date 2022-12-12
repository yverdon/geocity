from datetime import timedelta

from django.http import FileResponse
from django.urls import reverse
from django.utils import timezone
from knox.models import AuthToken

from .utils import run_docker_container


def generate_report_pdf(user, submission_id, form_id, report_id):
    authtoken, token = AuthToken.objects.create(user, expiry=timedelta(minutes=5))

    url = reverse(
        "reports:submission_report_content",
        kwargs={
            "submission_id": submission_id,
            "form_id": form_id,
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

    return output


def generate_report_pdf_as_response(user, submission_id, form_id, report_id):
    output = generate_report_pdf(user, submission_id, form_id, report_id)
    now = timezone.now()

    response = FileResponse(
        output, filename=f"autogenerated_report_{now:%Y-%m-%d}.pdf", as_attachment=False
    )
    response["Content-Type"] = "application/pdf"
    return response
