from .settings import *


def show_toolbar(request):
    return DEBUG


INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware",] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

DEBUG_TOOLBAR_CONFIG = dict(
    SHOW_TOOLBAR_CALLBACK="geomapshark.settings_dev.show_toolbar"
)