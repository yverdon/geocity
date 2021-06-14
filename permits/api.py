from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.db.models import CharField, F, Prefetch, Q
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from . import geoservices, models, serializers, services
from constance import config


# ///////////////////////////////////
# DJANGO REST API
# ///////////////////////////////////


class GeocityViewConfigViewSet(viewsets.ViewSet):
    def list(self, request):

        config = {
            "meta_types": dict(
                (str(x), y) for x, y in models.WorksType.META_TYPE_CHOICES
            )
        }

        config["map_config"] = {
            "wmts_capabilities": settings.WMTS_GETCAP,
            "wmts_layer": settings.WMTS_LAYER,
            "wmts_capabilities_alternative": settings.WMTS_GETCAP_ALTERNATIVE,
            "wmts_layer_aternative": settings.WMTS_LAYER_ALTERNATIVE,
        }

        geojson = json.loads(
            serialize(
                "geojson",
                models.PermitAdministrativeEntity.objects.all(),
                geometry_field="geom",
                srid=2056,
                fields=("id", "name", "ofs_id", "link",),
            )
        )

        config["administrative_entities"] = geojson

        return JsonResponse(config, safe=False)


class PermitRequestGeoTimeViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.PermitRequestGeoTimeSerializer

    def get_queryset(self):
        """
        This view should return a list of events for which the logged user has
        view permissions
        """
        user = self.request.user
        starts_at = self.request.query_params.get("starts_at", None)
        ends_at = self.request.query_params.get("ends_at", None)
        administrative_entity = self.request.query_params.get("adminentity", None)

        base_filter = Q()
        if starts_at:
            start = datetime.datetime.strptime(starts_at, "%Y-%m-%d")
            base_filter &= Q(starts_at__gte=start)
        if ends_at:
            end = datetime.datetime.strptime(ends_at, "%Y-%m-%d")
            base_filter &= Q(ends_at__lte=end)
        if administrative_entity:
            base_filter &= Q(
                permit_request__administrative_entity=administrative_entity
            )
        base_filter &= ~Q(permit_request__status=models.PermitRequest.STATUS_DRAFT)

        works_object_types_prefetch = Prefetch(
            "permit_request__works_object_types",
            queryset=models.WorksObjectType.objects.filter(
                Q(
                    has_geometry_point=True,
                    has_geometry_line=True,
                    has_geometry_polygon=True,
                )
                | Q(needs_date=True)
            ).select_related("works_type"),
        )

        qs = (
            models.PermitRequestGeoTime.objects.filter(base_filter)
            .filter(
                Q(permit_request__in=services.get_permit_requests_list_for_user(user))
                | Q(permit_request__is_public=True)
            )
            .prefetch_related(works_object_types_prefetch)
            .select_related("permit_request__administrative_entity")
        )

        return qs.order_by("starts_at")


# //////////////////////////////////
# PERMIT REQUEST ENDPOINT
# //////////////////////////////////


class BlockRequesterUserPermission(BasePermission):
    """
    Block access to Permit Requesters (General Public)
    """

    def has_permission(self, request, view):
        remote_addr = request.META["REMOTE_ADDR"]

        for whitelisted in config.ENDPOINT_WHITELIST.split(","):
            if remote_addr == whitelisted or remote_addr.startswith(valid_ip):
                return request.user.get_all_permissions()
        else:
            return []


class PermitRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Permit request endpoint Usage:
        1.- /rest/permits/?permit_request_id=1
        2.- /rest/permits/?works_object_type=1
        3.- /rest/permits/?status=0
        4.- /rest/permits/?geom_type=lines | points | polygons
    """

    serializer_class = serializers.PermitRequestPrintSerializer
    permission_classes = [IsAuthenticated, BlockRequesterUserPermission]

    def get_queryset(self):
        """
        This view should return a list of permits for which the logged user has
        view permissions
        """
        user = self.request.user

        filters_serializer = serializers.PermitRequestFiltersSerializer(
            data={
                "works_object_type": self.request.query_params.get("works_object_type"),
                "status": self.request.query_params.get("status"),
                "geom_type": self.request.query_params.get("geom_type"),
                "permit_request_id": self.request.query_params.get("permit_request_id"),
            }
        )

        filters_serializer.is_valid(raise_exception=True)
        filters = filters_serializer.validated_data

        base_filter = Q()

        if filters["works_object_type"]:
            base_filter &= Q(works_object_types=filters["works_object_type"])

        if filters["status"]:
            base_filter &= Q(status=filters["status"])

        if filters["permit_request_id"]:
            base_filter &= Q(pk=filters["permit_request_id"])

        geom_qs = models.PermitRequestGeoTime.objects.all()

        if filters["geom_type"]:
            geom_qs = geom_qs.annotate(geom_type=geoservices.GeomStAsText(F("geom"),))
            if filters["geom_type"] == "lines":
                geom_qs = geom_qs.filter(geom_type__contains="LINE")
            if filters["geom_type"] == "points":
                geom_qs = geom_qs.filter(geom_type__contains="POINT")
            if filters["geom_type"] == "polygons":
                geom_qs = geom_qs.filter(geom_type__contains="POLY")
            base_filter &= Q(
                id__in=set(geom_qs.values_list("permit_request_id", flat=True))
            )

        geotime_prefetch = Prefetch("geo_time", queryset=geom_qs)

        works_object_types_prefetch = Prefetch(
            "works_object_types",
            queryset=models.WorksObjectType.objects.select_related("works_type"),
        )

        qs = (
            models.PermitRequest.objects.filter(base_filter)
            .filter(
                Q(id__in=services.get_permit_requests_list_for_user(user))
                | Q(is_public=True)
            )
            .prefetch_related(works_object_types_prefetch)
            .prefetch_related(geotime_prefetch)
            .prefetch_related("worksobjecttypechoice_set__properties__property")
            .prefetch_related("worksobjecttypechoice_set__amend_properties__property")
            .select_related("administrative_entity")
        )

        return qs

# //////////////////////////////////
# OGC Feature API Base URLs
# //////////////////////////////////


class OGCOpenAPILandingView(viewsets.ViewSet):
    """
    OGCOpenAPILandingView usage:

    """
    # permission_classes = [IsAuthenticated, BlockRequesterUserPermission]

    def list(self, request):
        print("/////////////////")
        print("Landing")
        print("/////////////////")
        base = {
            "links": [
                {
                    "rel": "self",
                    "type": "application/json",
                    "title": "This document as JSON",
                    "href": "http://localhost:9095/ogc/?format=json"
                },
                {
                    "rel": "alternate",
                    "type": "application/ld+json",
                    "title": "This document as RDF (JSON-LD)",
                    "href": "http://localhost:9095/ogc/?format=jsonld"
                },
                {
                    "rel": "alternate",
                    "type": "text/html",
                    "title": "This document as HTML",
                    "href": "http://localhost:9095/ogc/?format=html",
                    "hreflang": "fr-CH"
                },
                {
                    "rel": "service-desc",
                    "type": "application/vnd.oai.openapi+json;version=3.0",
                    "title": "The OpenAPI definition as JSON",
                    "href": "http://localhost:9095/ogc/openapi/?format=json"
                },
                {
                    "rel": "service-doc",
                    "type": "text/html",
                    "title": "The OpenAPI definition as HTML",
                    "href": "http://localhost:9095/ogc/openapi/?format=html",
                    "hreflang": "fr-CH"
                },
                {
                    "rel": "conformance",
                    "type": "application/json",
                    "title": "Conformance",
                    "href": "http://localhost:9095/ogc/conformance/?format=json"
                },
                {
                    "rel": "data",
                    "type": "application/json",
                    "title": "Collections",
                    "href": "http://localhost:9095/ogc/collections/?format=json"
                }
            ],
            "title": "Geocity pygeoapi OGC services",
            "description": "Geocity pygeoapi OGC services"
        }
        return Response(base)


class OGCOpenAPICollectionsView(viewsets.ViewSet):
    """
    OGCOpenAPICollectionsView usage:

    """
    # permission_classes = [IsAuthenticated, BlockRequesterUserPermission]

    def list(self, request):
        print("/////////////////")
        print("Collections")
        print("/////////////////")
        collections = {
            "collections": [
                {
                    "id": "permits",
                    "title": "Geocity features",
                    "description": "Geocity REST API",
                    "keywords": [
                        "geocity",
                        "geojson"
                    ],
                    "links": [
                        {
                            "type": "application/json;",
                            "rel": "alternate",
                            "title": "data",
                            "href": "http://localhost:9095/rest/permits/?format=json",
                            "hreflang": "en-US"
                        },
                        {
                            "type": "application/json",
                            "rel": "self",
                            "title": "This document as JSON",
                            "href": "http://localhost:9095/ogc/collections/permits?f=json"
                        },
                        {
                            "type": "application/ld+json",
                            "rel": "alternate",
                            "title": "This document as RDF (JSON-LD)",
                            "href": "http://localhost:9095/ogc/collections/permits?f=jsonld"
                        },
                        {
                            "type": "text/html",
                            "rel": "alternate",
                            "title": "This document as HTML",
                            "href": "http://localhost:9095/ogc/collections/permits?f=html"
                        },
                        {
                            "type": "application/json",
                            "rel": "queryables",
                            "title": "Queryables for this collection as JSON",
                            "href": "http://localhost:9095/ogc/collections/permits/queryables?f=json"
                        },
                        {
                            "type": "text/html",
                            "rel": "queryables",
                            "title": "Queryables for this collection as HTML",
                            "href": "http://localhost:9095/ogc/collections/permits/queryables?f=html"
                        },
                        {
                            "type": "application/geo+json",
                            "rel": "items",
                            "title": "items as GeoJSON",
                            "href": "http://localhost:9095/ogc/collections/permits/items?f=json"
                        },
                        {
                            "type": "application/ld+json",
                            "rel": "items",
                            "title": "items as RDF (GeoJSON-LD)",
                            "href": "http://localhost:9095/ogc/collections/permits/items?f=jsonld"
                        },
                        {
                            "type": "text/html",
                            "rel": "items",
                            "title": "Items as HTML",
                            "href": "http://localhost:9095/ogc/collections/permits/items?f=html"
                        }
                    ],
                    "extent": {
                        "spatial": {
                            "bbox": [
                                [
                                    -180,
                                    -90,
                                    180,
                                    90
                                ]
                            ],
                            "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                        }
                    },
                    "itemType": "feature"
                }
            ],
            "links": [
                {
                    "type": "application/json",
                    "rel": "self",
                    "title": "This document as JSON",
                    "href": "http://localhost:9095/ogc/collections?fo=json"
                },
                {
                    "type": "application/ld+json",
                    "rel": "alternate",
                    "title": "This document as RDF (JSON-LD)",
                    "href": "http://localhost:9095/ogc/collections?f=jsonld"
                },
                {
                    "type": "text/html",
                    "rel": "alternate",
                    "title": "This document as HTML",
                    "href": "http://localhost:9095/ogc/collections?f=html"
                }
            ]
        }
        return Response(collections)
    
    

class OGCOpenAPICapabilitiesView(viewsets.ViewSet):
    """
    OGCOpenAPICapabilitiesView usage:

    """
    # permission_classes = [IsAuthenticated, BlockRequesterUserPermission]

    def list(self, request):

        print("/////////////////")
        print("Capabilities")
        print("/////////////////")
        capabilities = {
            "components": {
                "parameters": {
                    "f": {
                        "description": "The optional f parameter indicates the output format which the server shall provide as part of the response document.  The default format is GeoJSON.",
                        "explode": "false",
                        "in": "query",
                        "name": "f",
                        "required": "false",
                        "schema": {
                            "default": "json",
                            "enum": [
                                "json",
                                "html",
                                "jsonld"
                            ],
                            "type": "string"
                        },
                        "style": "form"
                    },
                    "lang": {
                        "description": "The optional lang parameter instructs the server return a response in a certain language, if supported.  If the language is not among the available values, the Accept-Language header language will be used if it is supported. If the header is missing, the default server language is used. Note that providers may only support a single language (or often no language at all), that can be different from the server language.  Language strings can be written in a complex (e.g. \"fr-CA,fr;q=0.9,en-US;q=0.8,en;q=0.7\"), simple (e.g. \"de\") or locale-like (e.g. \"de-CH\" or \"fr_BE\") fashion.",
                        "in": "query",
                        "name": "lang",
                        "required": "false",
                        "schema": {
                            "default": "fr-CH",
                            "enum": [
                                "fr-CH"
                            ],
                            "type": "string"
                        }
                    },
                    "properties": {
                        "description": "The properties that should be included for each feature. The parameter value is a comma-separated list of property names.",
                        "explode": "false",
                        "in": "query",
                        "name": "properties",
                        "required": "false",
                        "schema": {
                            "items": {
                                "type": "string"
                            },
                            "type": "array"
                        },
                        "style": "form"
                    },
                    "skipGeometry": {
                        "description": "This option can be used to skip response geometries for each feature.",
                        "explode": "false",
                        "in": "query",
                        "name": "skipGeometry",
                        "required": "false",
                        "schema": {
                            "default": "false",
                            "type": "boolean"
                        },
                        "style": "form"
                    },
                    "startindex": {
                        "description": "The optional startindex parameter indicates the index within the result set from which the server shall begin presenting results in the response document.  The first element has an index of 0 (default).",
                        "explode": "false",
                        "in": "query",
                        "name": "startindex",
                        "required": "false",
                        "schema": {
                            "default": 0,
                            "minimum": 0,
                            "type": "integer"
                        },
                        "style": "form"
                    }
                },
                "responses": {
                    "200": {
                        "description": "successful operation"
                    },
                    "Queryables": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/queryables"
                                }
                            }
                        },
                        "description": "successful queryables operation"
                    },
                    "default": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "https://raw.githubusercontent.com/opengeospatial/ogcapi-processes/master/core/openapi/schemas/exception.yaml"
                                }
                            }
                        },
                        "description": "Unexpected error"
                    }
                },
                "schemas": {
                    "queryable": {
                        "properties": {
                            "description": {
                                "description": "a human-readable narrative describing the queryable",
                                "type": "string"
                            },
                            "language": {
                                "default": [
                                    "en"
                                ],
                                "description": "the language used for the title and description",
                                "type": "string"
                            },
                            "queryable": {
                                "description": "the token that may be used in a CQL predicate",
                                "type": "string"
                            },
                            "title": {
                                "description": "a human readable title for the queryable",
                                "type": "string"
                            },
                            "type": {
                                "description": "the data type of the queryable",
                                "type": "string"
                            },
                            "type-ref": {
                                "description": "a reference to the formal definition of the type",
                                "format": "url",
                                "type": "string"
                            }
                        },
                        "required": [
                            "queryable",
                            "type"
                        ],
                        "type": "object"
                    },
                    "queryables": {
                        "properties": {
                            "queryables": {
                                "items": {
                                    "$ref": "#/components/schemas/queryable"
                                },
                                "type": "array"
                            }
                        },
                        "required": [
                            "queryables"
                        ],
                        "type": "object"
                    }
                }
            },
            "info": {
                "contact": {
                    "email": None,
                    "name": "Geocity Development Team",
                    "url": "https://geocity.ch"
                },
                "description": "Geocity pygeoapi OGC services",
                "license": {
                    "name": "CC-BY 4.0 license",
                    "url": "https://creativecommons.org/licenses/by/4.0/"
                },
                "termsOfService": "https://creativecommons.org/licenses/by/4.0/",
                "title": "Geocity pygeoapi OGC services",
                "version": "0.11.dev0",
                "x-keywords": [
                    "geospatial",
                    "data",
                    "api"
                ]
            },
            "openapi": "3.0.2",
            "paths": {
                "http://localhost:9095/": {
                    "get": {
                        "description": "Landing page",
                        "operationId": "getLandingPage",
                        "parameters": [
                            {
                                "$ref": "#/components/parameters/f"
                            },
                            {
                                "$ref": "#/components/parameters/lang"
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/LandingPage"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "500": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ServerError"
                            }
                        },
                        "summary": "Landing page",
                        "tags": [
                            "server"
                        ]
                    }
                },
                "http://localhost:9095/collections": {
                    "get": {
                        "description": "Collections",
                        "operationId": "getCollections",
                        "parameters": [
                            {
                                "$ref": "#/components/parameters/f"
                            },
                            {
                                "$ref": "#/components/parameters/lang"
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/Collections"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "500": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ServerError"
                            }
                        },
                        "summary": "Collections",
                        "tags": [
                            "server"
                        ]
                    }
                },
                "http://localhost:9095/collections/permits": {
                    "get": {
                        "description": "Geocity REST API",
                        "operationId": "describePermitsCollection",
                        "parameters": [
                            {
                                "$ref": "#/components/parameters/f"
                            },
                            {
                                "$ref": "#/components/parameters/lang"
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/Collection"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "404": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/NotFound"
                            },
                            "500": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ServerError"
                            }
                        },
                        "summary": "Get Geocity features metadata",
                        "tags": "permits"
                    }
                },
                "http://localhost:9095/collections/permits/items": {
                    "get": {
                        "description": "Geocity REST API",
                        "operationId": "getPermitsFeatures",
                        "parameters": [
                            {
                                "description": "The optional f parameter indicates the output format which the server shall provide as part of the response document.  The default format is GeoJSON.",
                                "explode": "false",
                                "in": "query",
                                "name": "f",
                                "required": "false",
                                "schema": {
                                    "default": "json",
                                    "enum": [
                                        "json",
                                        "html",
                                        "jsonld",
                                        "csv"
                                    ],
                                    "type": "string"
                                },
                                "style": "form"
                            },
                            {
                                "description": "The optional lang parameter instructs the server return a response in a certain language, if supported.  If the language is not among the available values, the Accept-Language header language will be used if it is supported. If the header is missing, the default server language is used. Note that providers may only support a single language (or often no language at all), that can be different from the server language.  Language strings can be written in a complex (e.g. \"fr-CA,fr;q=0.9,en-US;q=0.8,en;q=0.7\"), simple (e.g. \"de\") or locale-like (e.g. \"de-CH\" or \"fr_BE\") fashion.",
                                "in": "query",
                                "name": "lang",
                                "required": "false",
                                "schema": {
                                    "default": "fr-CH",
                                    "enum": [
                                        "fr-CH"
                                    ],
                                    "type": "string"
                                }
                            },
                            {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/parameters/bbox"
                            },
                            {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/parameters/limit"
                            },
                            {
                                "description": "The properties that should be included for each feature. The parameter value is a comma-separated list of property names.",
                                "explode": "false",
                                "in": "query",
                                "name": "properties",
                                "required": "false",
                                "schema": {
                                    "items": {
                                        "enum": [
                                            "id",
                                            "stn_id",
                                            "datetime",
                                            "value",
                                            "lat",
                                            "long"
                                        ],
                                        "type": "string"
                                    },
                                    "type": "array"
                                },
                                "style": "form"
                            },
                            {
                                "$ref": "#/components/parameters/skipGeometry"
                            },
                            {
                                "$ref": "https://raw.githubusercontent.com/opengeospatial/ogcapi-records/master/core/openapi/parameters/sortby.yaml"
                            },
                            {
                                "$ref": "#/components/parameters/startindex"
                            },
                            {
                                "explode": "false",
                                "in": "query",
                                "name": "id",
                                "required": "false",
                                "schema": {
                                    "type": {
                                        "type": "string"
                                    }
                                },
                                "style": "form"
                            },
                            {
                                "explode": "false",
                                "in": "query",
                                "name": "stn_id",
                                "required": "false",
                                "schema": {
                                    "type": {
                                        "type": "string"
                                    }
                                },
                                "style": "form"
                            },
                            {
                                "explode": "false",
                                "in": "query",
                                "name": "datetime",
                                "required": "false",
                                "schema": {
                                    "type": {
                                        "type": "string"
                                    }
                                },
                                "style": "form"
                            },
                            {
                                "explode": "false",
                                "in": "query",
                                "name": "value",
                                "required": "false",
                                "schema": {
                                    "type": {
                                        "type": "string"
                                    }
                                },
                                "style": "form"
                            },
                            {
                                "explode": "false",
                                "in": "query",
                                "name": "lat",
                                "required": "false",
                                "schema": {
                                    "type": {
                                        "type": "string"
                                    }
                                },
                                "style": "form"
                            },
                            {
                                "explode": "false",
                                "in": "query",
                                "name": "long",
                                "required": "false",
                                "schema": {
                                    "type": {
                                        "type": "string"
                                    }
                                },
                                "style": "form"
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/Features"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "404": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/NotFound"
                            },
                            "500": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ServerError"
                            }
                        },
                        "summary": "Get Geocity features items",
                        "tags": [
                            "permits"
                        ]
                    }
                },
                "http://localhost:9095/collections/permits/items/{featureId}": {
                    "get": {
                        "description": "Geocity REST API",
                        "operationId": "getPermitsFeature",
                        "parameters": [
                            {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/parameters/featureId"
                            },
                            {
                                "$ref": "#/components/parameters/f"
                            },
                            {
                                "$ref": "#/components/parameters/lang"
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/Feature"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "404": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/NotFound"
                            },
                            "500": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ServerError"
                            }
                        },
                        "summary": "Get Geocity features item by id",
                        "tags": [
                            "permits"
                        ]
                    }
                },
                "http://localhost:9095/collections/permits/queryables": {
                    "get": {
                        "description": "Geocity REST API",
                        "operationId": "getPermitsQueryables",
                        "parameters": [
                            {
                                "description": "The optional f parameter indicates the output format which the server shall provide as part of the response document.  The default format is GeoJSON.",
                                "explode": "false",
                                "in": "query",
                                "name": "f",
                                "required": "false",
                                "schema": {
                                    "default": "json",
                                    "enum": [
                                        "json",
                                        "html",
                                        "jsonld",
                                        "csv"
                                    ],
                                    "type": "string"
                                },
                                "style": "form"
                            },
                            {
                                "description": "The optional lang parameter instructs the server return a response in a certain language, if supported.  If the language is not among the available values, the Accept-Language header language will be used if it is supported. If the header is missing, the default server language is used. Note that providers may only support a single language (or often no language at all), that can be different from the server language.  Language strings can be written in a complex (e.g. \"fr-CA,fr;q=0.9,en-US;q=0.8,en;q=0.7\"), simple (e.g. \"de\") or locale-like (e.g. \"de-CH\" or \"fr_BE\") fashion.",
                                "in": "query",
                                "name": "lang",
                                "required": "false",
                                "schema": {
                                    "default": "fr-CH",
                                    "enum": [
                                        "fr-CH"
                                    ],
                                    "type": "string"
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "#/components/responses/Queryables"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "404": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/NotFound"
                            },
                            "500": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ServerError"
                            }
                        },
                        "summary": "Get Geocity features queryables",
                        "tags": [
                            "permits"
                        ]
                    }
                },
                "http://localhost:9095/conformance": {
                    "get": {
                        "description": "API conformance definition",
                        "operationId": "getConformanceDeclaration",
                        "parameters": [
                            {
                                "$ref": "#/components/parameters/f"
                            },
                            {
                                "$ref": "#/components/parameters/lang"
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ConformanceDeclaration"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "500": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/ServerError"
                            }
                        },
                        "summary": "API conformance definition",
                        "tags": [
                            "server"
                        ]
                    }
                },
                "http://localhost:9095/openapi": {
                    "get": {
                        "description": "This document",
                        "operationId": "getOpenapi",
                        "parameters": [
                            {
                                "$ref": "#/components/parameters/f"
                            },
                            {
                                "$ref": "#/components/parameters/lang"
                            }
                        ],
                        "responses": {
                            "200": {
                                "$ref": "#/components/responses/200"
                            },
                            "400": {
                                "$ref": "http://localhost:9095/ogc/schemas/ogcapi/features/part1/1.0/openapi/ogcapi-features-1.yaml#/components/responses/InvalidParameter"
                            },
                            "default": {
                                "$ref": "#/components/responses/default"
                            }
                        },
                        "summary": "This document",
                        "tags": [
                            "server"
                        ]
                    }
                }
            },
            "servers": [
                {
                    "description": "Geocity pygeoapi OGC services",
                    "url": "http://localhost:9095/ogc/"
                }
            ],
            "tags": [
                {
                    "description": "Geocity pygeoapi OGC services",
                    "externalDocs": {
                        "description": "information",
                        "url": "https://github.com/geopython/pygeoapi"
                    },
                    "name": "server"
                },
                {
                    "description": "SpatioTemporal Asset Catalog",
                    "name": "stac"
                },
                {
                    "description": "Geocity REST API",
                    "name": "permits"
                }
            ]
        }
        response = Response(capabilities)
        print(dict(response))
        return response

