from django.urls import path

from . import views

app_name = "forms"

urlpatterns = [
    path(
        "mapwidgetconfiguration/<int:form_id>/",
        views.map_widget_configuration,
        name="map_widget_configuration",
    ),
]
