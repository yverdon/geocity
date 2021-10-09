from django.urls import include, path

from django_wfs3.urls import wfs3_router

from . import api, geoviews, views


wfs3_router.register(r"permits", api.PermitRequestViewSet, "permits")
wfs3_router.register(r"permits_point", api.PermitRequestPointViewSet, "permit_point")
wfs3_router.register(r"permits_line", api.PermitRequestLineViewSet, "permit_line")
wfs3_router.register(r"permits_poly", api.PermitRequestPolyViewSet, "permit_poly")

app_name = "permits"

permit_request_urlpatterns = [
    path(
        "administrative-entity/",
        views.permit_request_select_administrative_entity,
        name="permit_request_select_administrative_entity",
    ),
]

existing_permit_request_urlpatterns = [
    path("", views.PermitRequestDetailView.as_view(), name="permit_request_detail"),
    path(
        "types/", views.permit_request_select_types, name="permit_request_select_types"
    ),
    path(
        "objects/",
        views.permit_request_select_objects,
        name="permit_request_select_objects",
    ),
    path(
        "properties/", views.permit_request_properties, name="permit_request_properties"
    ),
    path(
        "appendices/", views.permit_request_appendices, name="permit_request_appendices"
    ),
    path("actors/", views.permit_request_actors, name="permit_request_actors"),
    path("submit/", views.permit_request_submit, name="permit_request_submit"),
    path(
        "submitconfirmed/",
        views.permit_request_submit_confirmed,
        name="permit_request_submit_confirmed",
    ),
    path("geotime/", views.permit_request_geo_time, name="permit_request_geo_time"),
    path("delete/", views.permit_request_delete, name="permit_request_delete"),
    path("approve/", views.permit_request_approve, name="permit_request_approve"),
    path("reject/", views.permit_request_reject, name="permit_request_reject"),
    path(
        "print/<int:template_id>/",
        views.permit_request_print,
        name="permit_request_print",
    ),
]

urlpatterns = [
    path(
        "<int:permit_request_id>/",
        include(permit_request_urlpatterns + existing_permit_request_urlpatterns),
    ),
    path(
        "permits-files/<path:path>",
        views.permit_request_file_download,
        name="permit_request_file_download",
    ),
    path(
        "admin-data/<path:path>",
        views.administrative_entity_file_download,
        name="administrative_entity_file_download",
    ),
    path("", views.PermitRequestList.as_view(), name="permit_requests_list"),
    path("", include(permit_request_urlpatterns)),
    path(
        "media/<int:property_value_id>/",
        views.permit_request_media_download,
        name="permit_request_media_download",
    ),
    path("listexport/", views.PermitExportView.as_view(), name="listexport"),
    path(
        "adminentitiesgeojson/<int:administrative_entity_id>/",
        geoviews.administrative_entities_geojson,
        name="administrative_entities_geojson",
    ),
    path("qgisserverproxy/", geoviews.qgisserver_proxy, name="qgisserver_proxy"),
    path("search/", views.permit_requests_search, name="permit_requests_search"),
]
