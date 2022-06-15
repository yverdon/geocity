from .settings import *

# Disable Axes for tests
# TODO: enable it later
AXES_ENABLED = False
# Speed up tests by using a fast password hasher
# https://docs.djangoproject.com/en/3.0/topics/testing/overview/#speeding-up-the-tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
# For tests, Token authentication is set to True
DRF_ALLOW_TOKENAUTHENTICATION = True
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (
    "rest_framework.authentication.TokenAuthentication",
)
SITE_ID = 1
SITE_DOMAIN = "localhost"

ARCHIVE_ROOT = os.environ.get(
    "ARCHIVE_ROOT", os.path.join(BASE_DIR, "permits/tests/files/archive")
)
