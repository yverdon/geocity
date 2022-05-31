import json
import urllib

import requests
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import FileResponse, HttpResponseNotFound, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import GEOSGeometry

from . import models


@login_required
def qgisserver_proxy(request):
    # Only GetMap request are allowed
    if request.GET["REQUEST"] == "GetMap":
        data = urllib.parse.urlencode(request.GET)
        # geocity.qgs is the default WMS user in geocity maps for mask layers for instance
        url = "http://qgisserver/ogc/?" + data + "&MAP=/io/data/geocity.qgs"
        response = requests.get(url)
        return FileResponse(response, content_type=format)

    else:
        return HttpResponseNotFound(
            _(
                "Seules les requêtes GetMap sur la couche"
                + "permits_permitadministrativeentity sont autorisées"
            )
        )


@login_required
def administrative_entities_geojson(request, administrative_entity_id):

    administrative_entity = models.PermitAdministrativeEntity.objects.filter(
        id=administrative_entity_id
    )

    geojson = json.loads(
        serialize(
            "geojson",
            administrative_entity,
            geometry_field="geom",
            srid=2056,
            fields=("id", "name"),
        )
    )

    return JsonResponse(geojson, safe=False)


@login_required
def administrative_entities_mask_geojson(request, administrative_entity_id):

    administrative_entity = models.PermitAdministrativeEntity.objects.filter(
        id=administrative_entity_id
    )
    square_buffer = administrative_entity.geom
    geojson = json.loads(
        serialize(
            "geojson",
            administrative_entity,
            geometry_field="geom",
            srid=2056,
            fields=("id", "name"),
        )
    )

    return JsonResponse(geojson, safe=False)
