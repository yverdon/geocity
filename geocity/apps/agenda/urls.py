from django.urls import include, path

from . import views

app_name = "agenda"

agenda_urlpatterns = [
    path("", views.agenda, name="agenda"),
]

urlpatterns = [
    path("", include(agenda_urlpatterns)),
]
