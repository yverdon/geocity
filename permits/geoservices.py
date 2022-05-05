import enum

from django.contrib.gis.db.models.functions import GeomOutputGeoFunc
from django.db.models import Aggregate, CharField
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from .models import PermitRequestGeoTime
import urllib
import requests
from constance import config
from django.contrib.gis.geos import Point, MultiPoint, GeometryCollection

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
                intersected_geometries += f"""
                    {result.pk}: {result.layer_name} ; {result.description} ;
                    {result.source_id} ; {result.source_subid} <br>
                    """

    return intersected_geometries


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


def reverse_geocode_and_store_address_geometry(permit_request, to_geocode_addresses):

    # Delete the previous geocoded geometries
    models.PermitRequestGeoTime.objects.filter(
        permit_request=permit_request, comes_from_automatic_geocoding=True
    ).delete()

    if to_geocode_addresses:
        geoadmin_address_search_api = config.LOCATIONS_SEARCH_API
        geom = GeometryCollection()
        for address in to_geocode_addresses:
            search_params = {
                "searchText": address,
                "limit": 1,
                "partitionlimit": 1,
                "type": "locations",
                "sr": "2056",
                "lang": "fr",
                "origins": "address",
            }

            data = urllib.parse.urlencode(search_params)
            url = f"{geoadmin_address_search_api}?{data}"
            # GEOADMIN API might be down and we don't want to block the user
            try:
                response = requests.get(url, timeout=2)
            except requests.exceptions.RequestException:
                return None

            if response.status_code == 200 and response.json()["results"]:
                x = response.json()["results"][0]["attrs"]["x"]
                y = response.json()["results"][0]["attrs"]["y"]
                geom.append(MultiPoint(Point(y, x, srid=2056)))
            # If geocoding matches nothing, set the address value on the administrative_entity centroid point
            else:
                geom.append(MultiPoint(permit_request.administrative_entity.geom.centroid))

        # Save the new ones
        models.PermitRequestGeoTime.objects.create(
            permit_request=permit_request, comes_from_automatic_geocoding=True, geom=geom,
        )
