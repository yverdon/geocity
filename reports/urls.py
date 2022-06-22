from django.conf import settings
from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path(
        "report/<int:permit_request_id>/<int:work_object_type_id>/<int:report_id>.pdf",
        views.report_view,
        name="permit_request_report",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "report/<int:permit_request_id>/<int:work_object_type_id>/<int:report_id>.html",
            views.report_view,
            {"as_string": True},
        ),
    ]
