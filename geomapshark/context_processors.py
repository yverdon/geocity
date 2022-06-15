from django.conf import settings


def two_factor_setting(request):
    return {"ENABLE_2FA": settings.ENABLE_2FA}
