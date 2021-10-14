from django.conf import settings
from allauth.socialaccount.models import SocialApp


def two_factor_setting(request):
    return {"ENABLE_2FA": settings.ENABLE_2FA}


def social_apps(request):
    return {"social_apps": SocialApp.objects.all()}
