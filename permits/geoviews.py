from . import models
import requests
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseNotFound, FileResponse
from django.contrib.auth.decorators import login_required
import json
from django.forms.models import model_to_dict
import urllib
from django.utils.translation import gettext_lazy as _


@login_required
def qgisserver_proxy(request):


    # Secure QGISSERVER as it potentially has access to whole DB
    # Event getcapabilities requests are disabled
    if request.GET['REQUEST'] == 'GetMap' and request.GET['LAYERS'] == 'permits_permitadministrativeentity':
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
