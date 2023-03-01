import json

from django import forms
from django.conf import settings
from django.contrib.gis import forms as geoforms
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext


class PrivateFileSystemStorage(FileSystemStorage):
    """
    Storage for files that MUST NOT get directly exposed by the web server.
    """

    def __init__(self):
        super().__init__(location=settings.PRIVATE_MEDIA_ROOT, base_url=None)


# extend django gis osm openlayers widget
class GeometryWidget(geoforms.OSMWidget):
    template_name = "geometrywidget/geometrywidget.html"
    map_srid = 2056

    @property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "libs/js/openlayers6/ol.css",
                    "customWidgets/RemoteAutocomplete/remoteautocomplete.css",
                    "libs/js/jquery-ui-custom/jquery-ui.min.css",
                    "css/geotime.css",
                )
            },
            js=(
                "libs/js/openlayers6/ol.js",
                "libs/js/proj4js/proj4-src.js",
                "customWidgets/GeometryWidget/geometrywidget.js",
                "libs/js/jquery-ui-custom/jquery-ui.js",
            ),
        )


class AddressWidget(forms.TextInput):
    @property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "customWidgets/RemoteAutocomplete/remoteautocomplete.css",
                    "libs/js/jquery-ui-custom/jquery-ui.min.css",
                )
            },
            js=(
                "customWidgets/RemoteAutocomplete/remoteautocomplete.js",
                "libs/js/jquery-ui-custom/jquery-ui.js",
            ),
        )

    def __init__(self, attrs=None, autocomplete_options=None):
        autocomplete_options = {
            "apiurl": settings.LOCATIONS_SEARCH_API,
            "apiurl_detail": settings.LOCATIONS_SEARCH_API_DETAILS,
            "origins": "address",
            "zipcode_field": "zipcode",
            "city_field": "city",
            "placeholder": gettext("ex: Place Pestalozzi 2, 1400 Yverdon"),
            "single_contact": True,
            "single_address_field": False,
            **(autocomplete_options or {}),
        }
        super().__init__(
            {
                **(attrs or {}),
                "data_remote_autocomplete": json.dumps(autocomplete_options),
            }
        )


class AdvancedGeometryWidget(forms.TextInput):
    template_name = "advancedgeometrywidget/advancedgeometrywidget.html"
