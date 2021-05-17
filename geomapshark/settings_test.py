from .settings import *

# Speed up tests by using a fast password hasher
# https://docs.djangoproject.com/en/3.0/topics/testing/overview/#speeding-up-the-tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

DEBUG = False