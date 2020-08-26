from . import models
import requests
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseNotFound, FileResponse
from django.contrib.auth.decorators import login_required
import json
import urllib
from django.utils.translation import gettext_lazy as _
import datetime


@login_required
def qgisserver_proxy(request):

    # Secure QGISSERVER as it potentially has access to whole DB
    # Event getcapabilities requests are disabled
    if request.GET['REQUEST'] == 'GetMap':
        data = urllib.parse.urlencode(request.GET)
        format = request.GET['FORMAT']
        url = "http://qgisserver" + '/?' + data
        response = requests.get(url)
        return FileResponse(response, content_type=format)

    else:
        return HttpResponseNotFound(_('Seules les requêtes GetMap sur la couche' +
                                      'permits_permitadministrativeentity sont autorisées'))


@login_required
def administrative_entities_geojson(request, administrative_entity_id):

    administrative_entity = models.PermitAdministrativeEntity.objects.filter(id=administrative_entity_id)

    geojson = json.loads(serialize('geojson', administrative_entity,
                                   geometry_field='geom',
                                   srid=2056,
                                   fields=('id', 'name', 'ofs_id', 'link',)))

    return JsonResponse(geojson, safe=False)


def public_geocity_front_events(request, administrative_entity_id, event_type, starts_at, ends_at):

    start = datetime.datetime.strptime(starts_at, '%Y-%m-%d')
    end = datetime.datetime.strptime(ends_at, '%Y-%m-%d')
    geo_times = models.PermitRequestGeoTime.objects.filter(
        permit_request__administrative_entity=administrative_entity_id,
        starts_at__gte=start,
        ends_at__lte=end,
        permit_request__is_public=True,
        ).all()

    json_permits = json.loads(serialize('geojson',
                                        geo_times,
                                        geometry_field='geom',
                                        srid=2056,
                                        ))

    return JsonResponse(json_permits, safe=False)


@login_required
def private_geocity_front_events(request, administrative_entity_id, event_type, starts_at, ends_at):

    start = datetime.datetime.strptime(starts_at, '%Y-%m-%d')
    end = datetime.datetime.strptime(ends_at, '%Y-%m-%d')
    geo_times = models.PermitRequestGeoTime.objects.filter(
        permit_request__administrative_entity=administrative_entity_id,
        starts_at__gte=start,
        ends_at__lte=end,
        ).all()

    json_permits = json.loads(serialize('geojson',
                                        geo_times,
                                        geometry_field='geom',
                                        srid=2056,
                                        ))

    return JsonResponse(json_permits, safe=False)


@login_required
def geocity_front_config(request, administrative_entity_id):

    json_config = {'meta_types': dict((str(x), y) for x, y in models.WorksType.META_TYPE_CHOICES)}

    return JsonResponse(json_config, safe=False)
