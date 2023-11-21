from django.urls import include, path

from . import views

app_name = "agenda"

agenda_urlpatterns = [
    path("", views.agenda, name="agenda"),
    path("sports/", views.agenda_sports, name="agenda_sports"),
    path("culture/", views.agenda_culture, name="agenda_culture"),
]

urlpatterns = [
    path("", include(agenda_urlpatterns)),
]
