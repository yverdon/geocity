"""
WSGI config for geomapshark project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/fr/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geomapshark.settings")

application = get_wsgi_application()
application = WhiteNoise(application, root=os.environ["STATIC_FILES_ABSOLUTE_PATH"])
# TODO: serve media from PUBLIC_DOCUMENTS_DIR files with WhiteNoise
