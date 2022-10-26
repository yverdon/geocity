from django.contrib.gis.db.models.functions import GeomOutputGeoFunc
from django.db.models import Aggregate, CharField


class GeomStAsText(GeomOutputGeoFunc):
    function = "ST_asText"
    geom_param_pos = (0,)
    output_field = CharField()


class JoinGeometries(Aggregate):
    name = "joined_geometries"
    template = "ST_SetSRID(ST_Expand(ST_Extent(%(expressions)s), 1), 2056)"
    allow_distinct = False


class ExtractPoints(Aggregate):
    name = "extracted_points"
    template = "ST_CollectionExtract(ST_Collect(%(expressions)s), 1)"


class ExtractLines(Aggregate):
    name = "extracted_lines"
    template = "ST_CollectionExtract(ST_Collect(%(expressions)s), 2)"


class ExtractPolys(Aggregate):
    name = "extracted_polys"
    template = "ST_CollectionExtract(ST_Collect(%(expressions)s), 3)"
