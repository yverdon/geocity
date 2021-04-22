from rest_framework import viewsets
from django.db.models import Prefetch, Q, F, CharField
from django.contrib.gis.db.models.functions import GeomOutputGeoFunc
from . import models, serializers, services
from rest_framework.exceptions import APIException
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


class GeomToText(GeomOutputGeoFunc):
    function = "ST_asText"
    geom_param_pos = (0,)
    output_field = CharField()


class PermitRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Permit request endpoint Usage:
        1.- /rest/permits/?permit-request-id=1
        2.- /rest/permits/?works-object-type=1&status=0
        3.- /rest/permits/?geom-type=lines | points | polygons
    """

    serializer_class = serializers.PermitRequestPrintSerializer

    def get_queryset(self):
        """
        This view should return a list of permits for which the logged user has
        view permissions
        """
        user = self.request.user

        if not user.is_authenticated:
            raise APIException(services.EndpointErrors.NO_AUTH.value)

        work_objects_type = self.request.query_params.get("works-object-type", None)
        status = self.request.query_params.get("status", None)
        geom_type = self.request.query_params.get("geom-type", None)
        permitrequest_id = self.request.query_params.get("permit-request-id", None)

        base_filter = Q()

        if work_objects_type:
            if work_objects_type.isdigit():
                base_filter &= Q(works_object_types=work_objects_type)
            else:
                raise APIException(services.EndpointErrors.WOT_NOT_INT.value)

        if status:
            if status.isdigit():
                base_filter &= Q(status=status)
            else:
                raise APIException(services.EndpointErrors.STATUS_NOT_INT.value)

        if permitrequest_id:
            if permitrequest_id.isdigit():
                base_filter &= Q(pk=permitrequest_id)
            else:
                raise APIException(services.EndpointErrors.PR_NOT_INT.value)

        works_object_types_prefetch = Prefetch(
            "works_object_types",
            queryset=models.WorksObjectType.objects.select_related("works_type"),
        )

        geom_qs = models.PermitRequestGeoTime.objects.only("geom")

        if geom_type:
            if geom_type not in ("lines", "points", "polygons"):
                raise APIException(services.EndpointErrors.GEO_NOT_VALID.value)
            geom_qs = geom_qs.annotate(geom_type=GeomToText(F("geom"),))
            if geom_type == "lines":
                geom_qs = geom_qs.filter(geom_type__icontains="line")
            if geom_type == "points":
                geom_qs = geom_qs.filter(geom_type__icontains="point")
            if geom_type == "polygons":
                geom_qs = geom_qs.filter(geom_type__icontains="poly")
            base_filter &= Q(id__in=geom_qs)

        geotime_prefetch = Prefetch("geo_time", queryset=geom_qs)

        try:
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
        except ValueError as e:
            raise APIException(e)

        if not qs:
            raise APIException(services.EndpointErrors.PR_NOT_EXISTS.value)

        return qs
