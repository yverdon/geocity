import enum

from django.contrib.gis.db.models.functions import GeomOutputGeoFunc
from django.db.models import Aggregate, CharField
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

from . import models


def get_intersected_geometries(permit_request):

    intersected_geometries_ids = []
    intersected_geometries = ""
    geotimes = permit_request.geo_time.all()

    for geo_time in geotimes:

        # Django GIS GEOS API does not support intersection with GeometryCollection
        # For this reason, we have to iterate over collection content
        for geom in geo_time.geom:
            results = (
                models.GeomLayer.objects.filter(geom__intersects=geom)
                .exclude(pk__in=intersected_geometries_ids)
                .distinct()
            )
            for result in results:
                intersected_geometries_ids.append(result.pk)
                intersected_geometries += (
                    str(result.pk)
                    + " - "
                    + result.layer_name
                    + " - "
                    + result.description
                    + result.source_id
                    + " - "
                    + result.source_subid
                    + "<br>"
                )

    return intersected_geometries


class GeomStAsText(GeomOutputGeoFunc):
    function = "ST_asText"
    geom_param_pos = (0,)
    output_field = CharField()


class JoinGeometries(Aggregate):
    name = "joined_geometries"
    template = "ST_SetSRID(ST_Extent(%(expressions)s), 2056)"
    allow_distinct = False

    def __init__(self, expression, **extra):
        super().__init__(expression, **extra)


class EndpointErrors(enum.Enum):
    WOT_NOT_INT = _("Le paramètre works_object_type doit être un nombre")
    STATUS_NOT_INT = _("Le paramètre status doit être un nombre")
    PR_NOT_INT = _("Le paramètre permit_request_id doit être un nombre")
    GEO_NOT_VALID = _(
        "Les valeurs possibles du paramètre geom_type sont: lines, points ou polygons"
    )


class ParameterWorksObjectTypeNotInt(APIException):
    status_code = 400
    default_detail = EndpointErrors.WOT_NOT_INT.value
    default_code = "bad_request"


class ParameterStatusNotInt(APIException):
    status_code = 400
    default_detail = EndpointErrors.STATUS_NOT_INT.value
    default_code = "bad_request"


class ParameterPermitRequestNotInt(APIException):
    status_code = 400
    default_detail = EndpointErrors.PR_NOT_INT.value
    default_code = "bad_request"


class ParameterGeomTypeNotValid(APIException):
    status_code = 400
    default_detail = EndpointErrors.GEO_NOT_VALID.value
    default_code = "bad_request"
