from django.urls import include, path

from permits import api
from django_wfs3.routers import WFS3Router


wfs3_router = WFS3Router()

urlpatterns = [
    path("", include(wfs3_router.urls)),
]
