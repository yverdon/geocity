from rest_framework import viewsets
from django.db.models import Prefetch, Q, F, Func, Value
from django.contrib.gis.db.models.functions import GeoFunc
from django.contrib.gis.db import models as geomodels
from . import models, serializers, services
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)

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

        works_object_types_prefetch = Prefetch(
            "permit_request__works_object_types",
            queryset=models.WorksObjectType.objects.select_related("works_type"),
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


class GetPoints(GeoFunc):
    function = "ST_CollectionExtract"
    geom_param_pos = (0,)
    output_field = geomodels.MultiPointField(srid=2056)


class GetLines(GeoFunc):
    function = "ST_CollectionExtract"
    geom_param_pos = (0,)
    output_field = geomodels.MultiLineStringField(srid=2056)


class GetPolygons(GeoFunc):
    function = "ST_CollectionExtract"
    geom_param_pos = (0,)
    output_field = geomodels.MultiPolygonField(srid=2056)


class PermitRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Permit request endpoint Usage:
        1.- /rest/permits/?permit-request-id=1
        2.- /rest/permits/?works-object-type=1&status=0
    """

    serializer_class = serializers.PermitRequestPrintSerializer

    def get_queryset(self):
        """
        This view should return a list of permits for which the logged user has
        view permissions
        """
        user = self.request.user
        work_objects_type = self.request.query_params.get("works-object-type", None)
        status = self.request.query_params.get("status", None)
        geom_type = self.request.query_params.get("geom-type", None)
        permitrequest_id = self.request.query_params.get("permit-request-id", None)

        base_filter = Q()
        if work_objects_type:
            base_filter &= Q(works_object_types=work_objects_type)
        if status:
            base_filter &= Q(status=status)
        if permitrequest_id:
            base_filter &= Q(pk=permitrequest_id)

        works_object_types_prefetch = Prefetch(
            "works_object_types",
            queryset=models.WorksObjectType.objects.select_related("works_type"),
        )

        geom_qs = models.PermitRequestGeoTime.objects.only("geom")

        if geom_type and geom_type == "points":
            geom_qs = geom_qs.annotate(geom_point=GetPoints(F("geom"), 1),)

        if geom_type and geom_type == "lines":
            geom_qs = geom_qs.annotate(geom_line=GetLines(F("geom"), 2),)

        if geom_type and geom_type == "polygons":
            geom_qs = geom_qs.annotate(geom_polygons=GetPolygons(F("geom"), 3),)

        geotime_prefetch = Prefetch("geo_time", queryset=geom_qs)

        qs = (
            models.PermitRequest.objects.filter(base_filter)
            .filter(
                Q(id__in=services.get_permit_requests_list_for_user(user))
                | Q(is_public=True)
            )
            .prefetch_related(works_object_types_prefetch)
            .prefetch_related(geotime_prefetch)
            .select_related("administrative_entity")
        )

        return qs
