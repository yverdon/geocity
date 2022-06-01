import json
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse

from . import models


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
