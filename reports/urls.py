from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path(
        "report/<int:permit_request_id>/<int:report_id>.pdf",
        views.report_view,
        name="permit_request_report"
    ),
]
