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
