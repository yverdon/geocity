from . import models, services, serializers
import requests
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseNotFound, FileResponse
from django.contrib.auth.decorators import login_required
import json
import urllib
from django.utils.translation import gettext_lazy as _
import datetime
from rest_framework import viewsets


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


@login_required
def geocity_front_config(request, administrative_entity_id):

    json_config = {'meta_types': dict((str(x), y) for x, y in models.WorksType.META_TYPE_CHOICES)}

    return JsonResponse(json_config, safe=False)


# ///////////////////////////////////
# DJANGO REST API
# ///////////////////////////////////

# example query: http://localhost:9095/rest/events/?format=api&starts_at=2020-01-01&ends_at=2020-12-30&adminentity=1


class PermitRequestGeoTimeViewSet(viewsets.ModelViewSet):
    queryset = models.PermitRequestGeoTime.objects.all().order_by('starts_at')
    serializer_class = serializers.PermitRequestGeoTimeSerializer

    def get_queryset(self):
        """
        This view should return a list of events for which the loggued user has
        view permissions
        """
        start = datetime.datetime.strptime(self.request.query_params.get('starts_at', None), '%Y-%m-%d')
        end = datetime.datetime.strptime(self.request.query_params.get('ends_at', None), '%Y-%m-%d')
        administrative_entity = self.request.query_params.get('adminentity', None),
        user = self.request.user

        private_qs = models.PermitRequestGeoTime.objects.filter(
                permit_request__administrative_entity=administrative_entity,
                permit_request__in=services.get_permit_requests_list_for_user(user),
                starts_at__gte=start,
                ends_at__lte=end
        )

        public_qs = models.PermitRequestGeoTime.objects.filter(
                permit_request__is_public=True
        )

        return public_qs.union(private_qs).order_by('starts_at')
