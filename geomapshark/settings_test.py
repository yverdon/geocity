from .settings import *

# Disable Axes for tests
# TODO: enable it later
AXES_ENABLED = False
# Speed up tests by using a fast password hasher
# https://docs.djangoproject.com/en/3.0/topics/testing/overview/#speeding-up-the-tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
