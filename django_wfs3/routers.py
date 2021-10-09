from rest_framework import routers

from django.urls import path
from django.conf import settings

from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.views import SchemaView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from .views import RootView, CollectionsView


class WFS3Router(routers.SimpleRouter):
    """Router to explose a WFS3 Endpoint.

    This works just like a regular DRF router, where you need
    to register your viewsets using `router.register(...)`.

    It will take care of creating the standard WFS3 routes according
    to https://app.swaggerhub.com/apis/cportele/ogcapi-features-1-example2/1.0.0#/Capabilities/getCollections
    """

    include_format_suffixes = True
    # default_schema_renderers = None
    APISchemaView = SchemaView
    SchemaGenerator = SchemaGenerator

    # This is the list of routes that get generated for viewsets.
    # It is adapted from routers.SimpleRouter but adapts URLs to the specs, and adds the describe URL
    # NOTE : we don't support routes created with @action(...), if needed copy implementation from SimpleRouter.routes here
    routes = [
        # List route.
        routers.Route(
            url=r"^collections/{prefix}/items{trailing_slash}$",
            mapping={
                "get": "list",
                # "post": "create",
            },
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        # Detail route.
        routers.Route(
            url=r"^collections/{prefix}/items/{lookup}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                # "put": "update",
                # "patch": "partial_update",
                # "delete": "destroy",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
        # Describe route.
        routers.Route(
            url=r"^collections/{prefix}{trailing_slash}$",
            mapping={"get": "describe",},
            name="{basename}-describe",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
    ]

    def __init__(self):
        super().__init__(trailing_slash=False)

    @property
    def urlpatterns(self):
        """Alias for self.urls, so that we can provide this instance directly to get_schema_view()"""
        return self.urls

    def get_urls(self):
        """Return all WFS3 routes"""
        urls = super().get_urls()

        title = getattr(settings, "WFS3_TITLE", "Django OGC Api Services Endpoint")
        description = getattr(settings, "WFS3_DESCRIPTION", "No description")

        # Root URL
        root_view = RootView.as_view(title=title, description=description,)
        root_url = path("", root_view, name="capabilities")
        urls.append(root_url)

        # Schema
        schema_view = get_schema_view(
            title=title, description=description, version="1.0.0", urlconf=self,
        )
        schema_url = path("api", schema_view, name="service-desc")
        urls.append(schema_url)

        # Collections (implementation adapted from DRF's DefaultRouter.get_api_root_view)
        collections_view = CollectionsView.as_view(registry=self.registry)
        collections_url = path("collections", collections_view, name="collections")
        urls.append(collections_url)

        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)

        return urls
