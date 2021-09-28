from rest_framework import routers
import itertools
from collections import OrderedDict, namedtuple

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, re_path

from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.views import SchemaView
from rest_framework.settings import api_settings
from rest_framework.urlpatterns import format_suffix_patterns


class WFS3RootView(views.APIView):
    """WFS3 index view.

    This is currently more or less static
    """

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "title": "Buildings in Bonn",
                "description": "Access to data about buildings in the city of Bonn via a Web API that conforms to the OGC API Features specification.",
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
                    # {
                    #     "href": request.build_absolute_uri("api.html"),
                    #     "rel": "service-doc",
                    #     "type": "text/html",
                    #     "title": "the API documentation",
                    # },
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

        collections_dict = {}
        for prefix, viewset, basename in self.registry:
            collections_dict[prefix] = f"{basename}-list"

        collections = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in collections_dict.items():
            if namespace:
                url_name = namespace + ":" + url_name
            try:
                collections[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get("format", None),
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue

        return Response(
            {
                "links": [
                    {
                        "href": request.build_absolute_uri(""),
                        "rel": "self",
                        "type": "application/json",
                        "title": "this document",
                    },
                    # {
                    #     "href": "http://data.example.org/collections.html",
                    #     "rel": "alternate",
                    #     "type": "text/html",
                    #     "title": "this document as HTML",
                    # },
                    # {
                    #     "href": "http://schemas.example.org/1.0/buildings.xsd",
                    #     "rel": "describedBy",
                    #     "type": "application/xml",
                    #     "title": "GML application schema for Acme Corporation building data",
                    # },
                    # {
                    #     "href": "http://download.example.org/buildings.gpkg",
                    #     "rel": "enclosure",
                    #     "type": "application/geopackage+sqlite3",
                    #     "title": "Bulk download (GeoPackage)",
                    #     "length": 472546,
                    # },
                ],
                "collections": [
                    {
                        "id": key,
                        "title": key,
                        "description": "?",
                        "extent": {
                            "spatial": {"bbox": [[7.01, 50.63, 7.22, 50.78]]},
                            "temporal": {"interval": [["2010-02-15T12:34:56Z", None]]},
                        },
                        "links": [
                            {
                                "href": url,
                                "rel": "items",
                                "type": "application/geo+json",
                                "title": key,
                            },
                            # {
                            #     "href": "http://data.example.org/collections/buildings/items.html",
                            #     "rel": "items",
                            #     "type": "text/html",
                            #     "title": "Buildings",
                            # },
                            # {
                            #     "href": "https://creativecommons.org/publicdomain/zero/1.0/",
                            #     "rel": "license",
                            #     "type": "text/html",
                            #     "title": "CC0-1.0",
                            # },
                            # {
                            #     "href": "https://creativecommons.org/publicdomain/zero/1.0/rdf",
                            #     "rel": "license",
                            #     "type": "application/rdf+xml",
                            #     "title": "CC0-1.0",
                            # },
                        ],
                    }
                    for key, url in collections.items()
                ],
            }
        )
