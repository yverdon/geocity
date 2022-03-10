from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geos.collections import (
    GeometryCollection,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
)
from django.db.models import CharField, F, Prefetch, Q
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_gis.fields import GeometrySerializerMethodField
from rest_framework.throttling import ScopedRateThrottle
from django_wfs3.mixins import WFS3DescribeModelViewSetMixin

from . import geoservices, models, serializers, services
from constance import config
import datetime


# ///////////////////////////////////
# DJANGO REST API
# ///////////////////////////////////


class PermitRequestGeoTimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Events request endpoint Usage:
        1.- /rest/permits/?show_only_future=true (past events get filtered out)
        2.- /rest/permits/?starts_at=2022-01-01
        2.- /rest/permits/?ends_at=2020-01-01
        3.- /rest/permits/?adminentities=1,2,3
    
    """

    serializer_class = serializers.PermitRequestGeoTimeSerializer
    throttle_scope = "events"

    def get_queryset(self):
        """
        This view should return a list of events for which the logged user has
        view permissions or events set as public by pilot
        """

        show_only_future = self.request.query_params.get("show_only_future", None)
        starts_at = self.request.query_params.get("starts_at", None)
        ends_at = self.request.query_params.get("ends_at", None)
        administrative_entities = self.request.query_params.get("adminentities", None)

        base_filter = Q()
        if starts_at:
            start = datetime.datetime.strptime(starts_at, "%Y-%m-%d")
            base_filter &= Q(starts_at__gte=start)
        if ends_at:
            end = datetime.datetime.strptime(ends_at, "%Y-%m-%d")
            base_filter &= Q(ends_at__lte=end)
        if show_only_future == "true":
            base_filter &= Q(ends_at__gte=datetime.datetime.now())
        if administrative_entities:
            base_filter &= Q(
                permit_request__administrative_entity__in=administrative_entities.split(
                    ","
                )
            )
        base_filter &= ~Q(permit_request__status=models.PermitRequest.STATUS_DRAFT)
        # Only allow WOTs that have at least one geometry type mandatory
        works_object_types_prefetch = Prefetch(
            "permit_request__works_object_types",
            queryset=models.WorksObjectType.objects.filter(
                (
                    Q(has_geometry_point=True)
                    | Q(has_geometry_line=True)
                    | Q(has_geometry_polygon=True)
                )
                & Q(needs_date=True)
            ).select_related("works_type"),
        )

        qs = (
            models.PermitRequestGeoTime.objects.filter(base_filter)
            .filter(
                Q(
                    permit_request__in=services.get_permit_requests_list_for_user(
                        self.request.user,
                        request_comes_from_internal_qgisserver=services.check_request_comes_from_internal_qgisserver(
                            self.request
                        ),
                    )
                )
                | Q(permit_request__is_public=True)
            )
            .prefetch_related(works_object_types_prefetch)
            .select_related("permit_request__administrative_entity")
        )

        return qs.order_by("starts_at")


# //////////////////////////////////
# PERMIT REQUEST ENDPOINT
# //////////////////////////////////


class BlockRequesterUserPermission(BasePermission):
    """
    Block access to Permit Requesters (General Public)
    Only superuser or integrators can use these endpoints
    """

    def has_permission(self, request, view):

        if request.user.is_authenticated and services.check_request_ip_is_allowed(
            request
        ):

            is_integrator_admin = request.user.groups.filter(
                permitdepartment__is_integrator_admin=True
            ).exists()
            return is_integrator_admin or request.user.is_superuser
        else:
            return services.check_request_comes_from_internal_qgisserver(request)


class PermitRequestViewSet(
    WFS3DescribeModelViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    """
    Permit request endpoint Usage:
        1.- /rest/permits/?permit_request_id=1
        2.- /rest/permits/?works_object_type=1
        3.- /rest/permits/?status=0
        
        Notes:
            1.- For works objects types that do not have geometry, the returned 
                geometry is a 2x2 square around the centroid of the administrative entity geometry
            2.- This endpoint does not filter out items without geometry.
                For works objects types that have only point geometry, the returned geometry
                is a polygon of 2 x 2 meters

            This endpoint is mainly designed for atlas print generation with QGIS Server
            For standard geometric endpoints, please use the following endpoints
            1.- Points: /rest/permits_point/
            2.- Lines: /rest/permits_line/
            3.- Polygons: /rest/permits_polygon/
    """

    throttle_scope = "permits"
    serializer_class = serializers.PermitRequestPrintSerializer
    permission_classes = [BlockRequesterUserPermission]

    wfs3_title = "Demandes"
    wfs3_description = "Toutes les demandes"
    wfs3_geom_lookup = "geo_time__geom"  # lookup for the geometry (on the queryset), used to determine bbox
    wfs3_srid = 2056

    def get_throttles(self):
        # Do not throttle API if request is used py print internal service
        if services.check_request_comes_from_internal_qgisserver(self.request):
            throttle_classes = []
        else:
            throttle_classes = [ScopedRateThrottle]
        return [throttle() for throttle in throttle_classes]

    def get_queryset(self, geom_type=None):
        """
        This view should return a list of permits for which the logged user has
        view permissions
        """
        user = self.request.user
        filters_serializer = serializers.PermitRequestFiltersSerializer(
            data={
                "works_object_type": self.request.query_params.get("works_object_type"),
                "status": self.request.query_params.get("status"),
                "permit_request_id": self.request.query_params.get("permit_request_id"),
            }
        )
        filters_serializer.is_valid(raise_exception=True)
        filters = filters_serializer.validated_data

        base_filter = Q()

        if filters["works_object_type"]:
            base_filter &= Q(works_object_types=filters["works_object_type"])

        if filters["status"]:
            base_filter &= Q(status=filters["status"])

        if filters["permit_request_id"]:
            base_filter &= Q(pk=filters["permit_request_id"])

        geom_qs = models.PermitRequestGeoTime.objects.all()
        # filter item which have the geom_type in their geometry column
        if geom_type:
            geom_qs = geom_qs.annotate(geom_type=geoservices.GeomStAsText(F("geom"),))
            if geom_type == "lines":
                geom_qs = geom_qs.filter(geom_type__contains="LINE")
            if geom_type == "points":
                geom_qs = geom_qs.filter(geom_type__contains="POINT")
            if geom_type == "polygons":
                geom_qs = geom_qs.filter(geom_type__contains="POLY")
            base_filter &= Q(
                id__in=set(geom_qs.values_list("permit_request_id", flat=True))
            )

        geotime_prefetch = Prefetch("geo_time", queryset=geom_qs)
        works_object_types_prefetch = Prefetch(
            "works_object_types",
            queryset=models.WorksObjectType.objects.select_related("works_type"),
        )
        request_comes_from_internal_qgisserver = services.check_request_comes_from_internal_qgisserver(
            self.request
        )

        qs = (
            models.PermitRequest.objects.filter(base_filter)
            .filter(
                Q(
                    id__in=services.get_permit_requests_list_for_user(
                        user,
                        request_comes_from_internal_qgisserver=request_comes_from_internal_qgisserver,
                    )
                )
                | Q(is_public=True)
            )
            .prefetch_related(works_object_types_prefetch)
            .prefetch_related(geotime_prefetch)
            .prefetch_related("worksobjecttypechoice_set__properties__property")
            .prefetch_related("worksobjecttypechoice_set__amend_properties__property")
            .select_related("administrative_entity")
        )
        if request_comes_from_internal_qgisserver:
            qs = qs[: config.MAX_FEATURE_NUMBER_FOR_QGISSERVER]

        return qs


class PermitRequestDetailsViewSet(
    WFS3DescribeModelViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    """
    Permit request details endpoint Usage:
        1.- /rest/permits_details/?permit_request_id=1
    """

    throttle_scope = "permits"
    # serializer_class = serializers.PermitRequestPrintSerializer
    serializer_class = serializers.PermitRequestDetailsSerializer
    permission_classes = [BlockRequesterUserPermission]

    def get_queryset(self, geom_type=None):
        """
        This view should return a list of permits for which the logged user has
        view permissions
        """
        user = self.request.user
        filters_serializer = serializers.PermitRequestFiltersSerializer(
            data={
                "permit_request_id": self.request.query_params.get("permit_request_id"),
            }
        )
        filters_serializer.is_valid(raise_exception=True)
        filters = filters_serializer.validated_data

        base_filter = Q()

        if filters["permit_request_id"]:
            base_filter &= Q(pk=filters["permit_request_id"])

        request_comes_from_internal_qgisserver = services.check_request_comes_from_internal_qgisserver(
            self.request
        )

        qs = models.PermitRequest.objects.filter(base_filter).filter(
            Q(
                id__in=services.get_permit_requests_list_for_user(
                    user,
                    request_comes_from_internal_qgisserver=request_comes_from_internal_qgisserver,
                )
            )
            | Q(is_public=True)
        )
        if request_comes_from_internal_qgisserver:
            qs = qs[: config.MAX_FEATURE_NUMBER_FOR_QGISSERVER]

        return qs


def permitRequestViewSetSubsetFactory(geom_type_name):
    """Returns a subclass of PermitRequestViewSet with a specific multi-geometry instead
    of the bounding box"""

    if geom_type_name == "lines":
        geom_serializer = (
            serializers.PermitRequestGeoTimeGeoJSONSerializer.EXTRACT_LINES
        )
    elif geom_type_name == "points":
        geom_serializer = (
            serializers.PermitRequestGeoTimeGeoJSONSerializer.EXTRACT_POINTS
        )
    elif geom_type_name == "polygons":
        geom_serializer = (
            serializers.PermitRequestGeoTimeGeoJSONSerializer.EXTRACT_POLYS
        )
    else:
        raise Exception(f"Unsupported geom type name {geom_type_name}")

    class Serializer(serializers.PermitRequestPrintSerializer):
        geo_envelop = serializers.PermitRequestGeoTimeGeoJSONSerializer(
            source="geo_time", read_only=True, extract_geom=geom_serializer,
        )

    # DRF want's the serializer to have a specific class name
    Serializer.__name__ = f"PermitRequestViewSetSerializer{geom_type_name}"

    class ViewSet(PermitRequestViewSet):
        """
        Permits request endpoint Usage:
            1.- /rest/permits/?permit_request_id=1
            2.- /rest/permits/?works_object_type=1
            3.- /rest/permits/?status=0
        """

        throttle_scope = "permits"
        wfs3_title = f"{PermitRequestViewSet.wfs3_title} ({geom_type_name})"
        wfs3_description = f"{PermitRequestViewSet.wfs3_description} (géométries de type {geom_type_name})"
        serializer_class = Serializer

        def get_throttles(self):
            # Do not throttle API if request is used py print internal service
            if services.check_request_comes_from_internal_qgisserver(self.request):
                throttle_classes = []
            else:
                throttle_classes = [ScopedRateThrottle]
            return [throttle() for throttle in throttle_classes]

        def get_queryset(self):
            # Inject the geometry filter
            return super().get_queryset(geom_type=geom_type_name)

    return ViewSet


PermitRequestPointViewSet = permitRequestViewSetSubsetFactory("points")
PermitRequestLineViewSet = permitRequestViewSetSubsetFactory("lines")
PermitRequestPolyViewSet = permitRequestViewSetSubsetFactory("polygons")
