from rest_framework import routers
import itertools
from collections import OrderedDict, namedtuple

from django.core.exceptions import ImproperlyConfigured
from django.contrib.gis.db.models import Extent
from django.urls import NoReverseMatch, re_path

from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.views import SchemaView
from rest_framework.settings import api_settings
from rest_framework.urlpatterns import format_suffix_patterns


class RootView(views.APIView):
    """WFS3 index view.

    This is currently more or less static
    """

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "title": "Geocity OGC Features API Endpoint",  # TODO : make customizable
                "description": "Access to data from Geocity.",  # TODO : make customizable
                "links": [
                    {
                        "href": request.build_absolute_uri("/"),
                        "rel": "self",
                        "type": "application/json",
                        "title": "this document",
                    },
                    {
                        "href": request.build_absolute_uri("api"),
                        "rel": "service-desc",
                        "type": "application/vnd.oai.openapi+json;version=3.0",
                        "title": "the API definition",
                    },
                    {
                        "href": request.build_absolute_uri("conformance"),
                        "rel": "conformance",
                        "type": "application/json",
                        "title": "OGC API conformance classes implemented by this server",
                    },
                    {
                        "href": request.build_absolute_uri("collections"),
                        "rel": "data",
                        "type": "application/json",
                        "title": "Information about the feature collections",
                    },
                ],
            }
        )


class CollectionsView(routers.APIRootView):
    """Collections index view.

    This is extends DRF's APIRootView as it works in the same way, but just
    adds some more elements.
    """

    schema = None  # exclude from schema
    registry = None

    def get(self, request, *args, **kwargs):

        collections = []
        namespace = request.resolver_match.namespace
        for prefix, Viewset, basename in self.registry:
            key = prefix
            url_name = f"{basename}-list"
            if namespace:
                url_name = namespace + ":" + url_name
            try:
                url = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get("format", None),
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue

            # Instantiating the viewset to get access to the ORM
            viewset = Viewset(request=request)
            queryset = viewset.get_queryset()
            geo_field = "geo_time__geom"  # TODO : make this customizable (viewset.get_serializer_class().Meta.geo_field doesn't work, it's a field on the serializer, not on the queryset)
            extents = queryset.aggregate(e=Extent(geo_field))["e"]

            crs = "http://www.opengis.net/def/crs/EPSG/0/2056"  # TODO : retrieve from geo_field

            collections.append({
                "id": key,
                "title": key,
                "description": "?",
                "extent": {
                    "spatial": {"bbox": extents},
                    # "crs": crs,  # TODO : doesn't work yet
                },
                "links": [
                    {
                        "href": url,
                        "rel": "items",
                        "type": "application/geo+json",
                        "title": key,
                    },
                ],
            })

        return Response(
            {
                "links": [
                    {
                        "href": request.build_absolute_uri(""),
                        "rel": "self",
                        "type": "application/json",
                        "title": "this document",
                    },
                ],
                "collections": collections,
            }
        )
