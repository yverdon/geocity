from constance import config
from django.contrib.sites.shortcuts import get_current_site


def site_customization(request):
    site = get_current_site(request)
    template = site.site_profile.custom_template

    if template:
        customization = {
            "primary_color": template.primary_color
            if template.primary_color
            else config.PRIMARY_COLOR,
            "secondary_color": template.secondary_color
            if template.secondary_color
            else config.SECONDARY_COLOR,
            "background_color": template.background_color
            if template.background_color
            else config.BACKGROUND_COLOR,
            "login_background_color": template.login_background_color
            if template.login_background_color
            else config.LOGIN_BACKGROUND_COLOR,
            "text_color": template.text_color
            if template.text_color
            else config.TEXT_COLOR,
            "title_color": template.title_color
            if template.title_color
            else config.TITLE_COLOR,
            "table_color": template.table_color
            if template.table_color
            else config.TABLE_COLOR,
            "application_title": template.application_title
            if template.application_title
            else config.APPLICATION_TITLE,
            "application_subtitle": template.application_subtitle
            if template.application_subtitle
            else config.APPLICATION_SUBTITLE,
            "application_description": template.application_description
            if template.application_description
            else config.APPLICATION_DESCRIPTION,
        }
        return customization

    customization = {
        "primary_color": config.PRIMARY_COLOR,
        "secondary_color": config.SECONDARY_COLOR,
        "background_color": config.BACKGROUND_COLOR,
        "login_background_color": config.LOGIN_BACKGROUND_COLOR,
        "text_color": config.TEXT_COLOR,
        "title_color": config.TITLE_COLOR,
        "table_color": config.TABLE_COLOR,
        "application_title": config.APPLICATION_TITLE,
        "application_subtitle": config.APPLICATION_SUBTITLE,
        "application_description": config.APPLICATION_DESCRIPTION,
    }

    return customization
