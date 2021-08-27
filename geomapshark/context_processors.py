from django.conf import settings
from allauth.socialaccount.models import SocialApp


def two_factor_setting(request):
    return {"ENABLE_2FA": settings.ENABLE_2FA}


def social_login_geomapfish_setting(request):
    return {
        "has_social_login_geomapfish": "APP"
        in settings.SOCIALACCOUNT_PROVIDERS["accounts.geomapfish"].keys()
        or SocialApp.objects.filter(provider="geomapfish").exists()
    }
