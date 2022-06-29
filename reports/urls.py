from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path(
        "report/<int:permit_request_id>/<int:work_object_type_id>/<int:report_id>.html",
        views.report_content,
        name="permit_request_report_content",
    ),
    path(
        "report/<int:permit_request_id>/<int:work_object_type_id>/<int:report_id>.pdf",
        views.report_pdf,
        name="permit_request_report_pdf",
    ),
    path(
        "report/<path:path>/download",
        views.background_download,
        name="background_download",
    ),
]
