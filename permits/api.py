from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.db.models import CharField, F, Prefetch, Q
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from . import geoservices, models, serializers, services
from constance import config


# ///////////////////////////////////
# DJANGO REST API
# ///////////////////////////////////


class GeocityViewConfigViewSet(viewsets.ViewSet):
    def list(self, request):

        config = {
            "meta_types": dict(
                (str(x), y) for x, y in models.WorksType.META_TYPE_CHOICES
            )
        }

        config["map_config"] = {
            "wmts_capabilities": settings.WMTS_GETCAP,
            "wmts_layer": settings.WMTS_LAYER,
            "wmts_capabilities_alternative": settings.WMTS_GETCAP_ALTERNATIVE,
            "wmts_layer_aternative": settings.WMTS_LAYER_ALTERNATIVE,
        }

        geojson = json.loads(
            serialize(
                "geojson",
                models.PermitAdministrativeEntity.objects.all(),
                geometry_field="geom",
                srid=2056,
                fields=("id", "name", "ofs_id", "link",),
            )
        )

        config["administrative_entities"] = geojson

        return JsonResponse(config, safe=False)


class PermitRequestGeoTimeViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.PermitRequestGeoTimeSerializer

    def get_queryset(self):
        """
        This view should return a list of events for which the logged user has
        view permissions
        """
        user = self.request.user
        starts_at = self.request.query_params.get("starts_at", None)
        ends_at = self.request.query_params.get("ends_at", None)
        administrative_entity = self.request.query_params.get("adminentity", None)

        base_filter = Q()
        if starts_at:
            start = datetime.datetime.strptime(starts_at, "%Y-%m-%d")
            base_filter &= Q(starts_at__gte=start)
        if ends_at:
            end = datetime.datetime.strptime(ends_at, "%Y-%m-%d")
            base_filter &= Q(ends_at__lte=end)
        if administrative_entity:
            base_filter &= Q(
                permit_request__administrative_entity=administrative_entity
            )
        base_filter &= ~Q(permit_request__status=models.PermitRequest.STATUS_DRAFT)

        works_object_types_prefetch = Prefetch(
            "permit_request__works_object_types",
            queryset=models.WorksObjectType.objects.filter(
                Q(
                    has_geometry_point=True,
                    has_geometry_line=True,
                    has_geometry_polygon=True,
                )
                | Q(needs_date=True)
            ).select_related("works_type"),
        )

        qs = (
            models.PermitRequestGeoTime.objects.filter(base_filter)
            .filter(
                Q(permit_request__in=services.get_permit_requests_list_for_user(user))
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
    """

    def has_permission(self, request, view):
        remote_addr = request.META["REMOTE_ADDR"]

        for whitelisted in config.ENDPOINT_WHITELIST.split(","):
            if remote_addr == whitelisted or remote_addr.startswith(valid_ip):
                return request.user.get_all_permissions()
        else:
            return []


class PermitRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Permit request endpoint Usage:
        1.- /rest/permits/?permit_request_id=1
        2.- /rest/permits/?works_object_type=1
        3.- /rest/permits/?status=0
        4.- /rest/permits/?geom_type=lines | points | polygons
    """

    serializer_class = serializers.PermitRequestPrintSerializer
    permission_classes = [IsAuthenticated, BlockRequesterUserPermission]

    def get_queryset(self):
        """
        This view should return a list of permits for which the logged user has
        view permissions
        """
        user = self.request.user

        filters_serializer = serializers.PermitRequestFiltersSerializer(
            data={
                "works_object_type": self.request.query_params.get("works_object_type"),
                "status": self.request.query_params.get("status"),
                "geom_type": self.request.query_params.get("geom_type"),
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

        if filters["geom_type"]:
            geom_qs = geom_qs.annotate(geom_type=geoservices.GeomStAsText(F("geom"),))
            if filters["geom_type"] == "lines":
                geom_qs = geom_qs.filter(geom_type__contains="LINE")
            if filters["geom_type"] == "points":
                geom_qs = geom_qs.filter(geom_type__contains="POINT")
            if filters["geom_type"] == "polygons":
                geom_qs = geom_qs.filter(geom_type__contains="POLY")
            base_filter &= Q(
                id__in=set(geom_qs.values_list("permit_request_id", flat=True))
            )

        geotime_prefetch = Prefetch("geo_time", queryset=geom_qs)

        works_object_types_prefetch = Prefetch(
            "works_object_types",
            queryset=models.WorksObjectType.objects.select_related("works_type"),
        )

        qs = (
            models.PermitRequest.objects.filter(base_filter)
            .filter(
                Q(id__in=services.get_permit_requests_list_for_user(user))
                | Q(is_public=True)
            )
            .prefetch_related(works_object_types_prefetch)
            .prefetch_related(geotime_prefetch)
            .prefetch_related("worksobjecttypechoice_set__properties__property")
            .prefetch_related("worksobjecttypechoice_set__amend_properties__property")
            .select_related("administrative_entity")
        )

        return qs
