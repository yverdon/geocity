from distutils.util import strtobool

from .settings import *


def show_toolbar(request):
    """Shows the debug toolbar when `?DEBUG=true` is your URL and DEBUG is enabled."""
    return DEBUG and strtobool(request.GET.get("DEBUG", "false"))


INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

DEBUG_TOOLBAR_CONFIG = dict(SHOW_TOOLBAR_CALLBACK="geocity.settings_dev.show_toolbar")

SITE_HTTPS = False
SESSION_COOKIE_HTTPONLY = False
CORS_ALLOW_CREDENTIALS = True
