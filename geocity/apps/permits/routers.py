from rest_framework.routers import DefaultRouter

from geocity.apps.django_wfs3.urls import wfs3_router

from . import api

default = DefaultRouter()
default.register("events", api.PermitRequestGeoTimeViewSet, "events")
default.register("permits", api.PermitRequestViewSet, "permits")
default.register("permits_point", api.PermitRequestPointViewSet, "permit_point")
default.register("permits_line", api.PermitRequestLineViewSet, "permit_line")
default.register("permits_poly", api.PermitRequestPolyViewSet, "permit_poly")
default.register("search", api.SearchViewSet, "search")
default.register("permits_details", api.PermitRequestDetailsViewSet, "permits_details")
default.register("permits_details", api.PermitRequestDetailsViewSet, "permits_details")
default.register("current_user", api.CurrentUserAPIViewSet, "current_user")

wfs3 = wfs3_router
wfs3.register("permits", api.PermitRequestViewSet, "permits")
wfs3.register("permits_point", api.PermitRequestPointViewSet, "permits_point")
wfs3.register("permits_line", api.PermitRequestLineViewSet, "permits_line")
wfs3.register("permits_poly", api.PermitRequestPolyViewSet, "permits_poly")
