from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path(
        "report/<int:submission_id>/<int:form_id>/<int:report_id>.html",
        views.report_content,
        name="submission_report_content",
    ),
    path(
        "report/<int:submission_id>/<int:form_id>/<int:report_id>/<int:transaction_id>.html",
        views.report_content,
        name="submission_report_content",
    ),
    path(
        "report/<int:submission_id>/<int:form_id>/<int:report_id>.pdf",
        views.report_pdf,
        name="submission_report_pdf",
    ),
    path(
        "report/<int:submission_id>/<int:form_id>/<int:report_id>/<int:transaction_id>.pdf",
        views.report_pdf,
        name="submission_report_pdf",
    ),
    path(
        "report/<path:path>/download",
        views.background_download,
        name="background_download",
    ),
]
