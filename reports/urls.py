from django.urls import path
from django.conf import settings

from . import views

app_name = "reports"

urlpatterns = [
    path(
        "report/<int:permit_request_id>/<int:report_id>/contents",
        views.report_view_contents,
        name="permit_request_report_contents",
    ),
    path(
        "report/<int:permit_request_id>/<int:report_id>.pdf",
        views.report_view,
        name="permit_request_report",
    ),
]
