from django.conf import settings
from allauth.socialaccount.models import SocialApp


def two_factor_setting(request):
    return {"ENABLE_2FA": settings.ENABLE_2FA}


def social_login_mapnv_setting(request):
    return {
        "social_login_mapnv": "APP" in settings.SOCIALACCOUNT_PROVIDERS["mapnv"].keys()
        or SocialApp.objects.filter(provider="mapnv").exists()
    }
