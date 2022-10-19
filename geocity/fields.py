from django import forms
from django.conf import settings
from django.contrib.gis import forms as geoforms
from django.core.files.storage import FileSystemStorage


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
