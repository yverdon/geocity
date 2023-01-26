from constance import config
from django.contrib.sites.shortcuts import get_current_site


def site_customization(request):
    site = get_current_site(request)
    template = site.site_profile.custom_template

    if template:
        customization = {
            "PRIMARY_COLOR": template.primary_color
            if template.primary_color
            else config.PRIMARY_COLOR,
            "SECONDARY_COLOR": template.secondary_color
            if template.secondary_color
            else config.SECONDARY_COLOR,
            "BACKGROUND_COLOR": template.primary_color
            if template.primary_color
            else config.BACKGROUND_COLOR,
            "LOGIN_BACKGROUND_COLOR": template.primary_color
            if template.primary_color
            else config.LOGIN_BACKGROUND_COLOR,
            "TEXT_COLOR": template.primary_color
            if template.primary_color
            else config.TEXT_COLOR,
            "TITLE_COLOR": template.primary_color
            if template.primary_color
            else config.TITLE_COLOR,
            "TABLE_COLOR": template.primary_color
            if template.primary_color
            else config.TABLE_COLOR,
        }
        return customization

    customization = {
        "PRIMARY_COLOR": config.PRIMARY_COLOR,
        "SECONDARY_COLOR": config.SECONDARY_COLOR,
        "BACKGROUND_COLOR": config.BACKGROUND_COLOR,
        "LOGIN_BACKGROUND_COLOR": config.LOGIN_BACKGROUND_COLOR,
        "TEXT_COLOR": config.TEXT_COLOR,
        "TITLE_COLOR": config.TITLE_COLOR,
        "TABLE_COLOR": config.TABLE_COLOR,
    }

    return customization
