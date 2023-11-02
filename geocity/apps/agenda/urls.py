from django.urls import include, path

from . import views

app_name = "agenda"

agenda_urlpatterns = [
    path("", views.agenda, name="agenda"),
    # Without thumbor params
    path(
        "image/display/permit_requests_uploads/<int:form_id>/<str:image_name>",
        views.image_service,
        name="image_service",
    ),
    # With thumbor params
    path(
        "image/display/permit_requests_uploads/<str:thumbor_params>/<int:form_id>/<str:image_name>",
        views.image_display,
        name="image_display",
    ),
]

urlpatterns = [
    path("", include(agenda_urlpatterns)),
]
