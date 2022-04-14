from .settings import *


def show_toolbar(request):
    from django.conf import settings

    return settings.DEBUG


INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware",] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]

DEBUG_TOOLBAR_CONFIG = dict(
    SHOW_TOOLBAR_CALLBACK="geomapshark.settings_dev.show_toolbar"
)

SITE_HTTPS = False
SESSION_COOKIE_HTTPONLY = False
CORS_ALLOW_CREDENTIALS = True
