from urllib import parse

from constance import config
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from permits import models


def get_context_data(context, request):

    customization = {
        "application_title": config.APPLICATION_TITLE,
        "application_subtitle": config.APPLICATION_SUBTITLE,
        "application_description": config.APPLICATION_DESCRIPTION,
        "general_conditions_url": config.GENERAL_CONDITIONS_URL,
        "privacy_policy_url": config.PRIVACY_POLICY_URL,
        "background_image": None,
        "background_color": None,
        "login_background_color": None,
        "primary_color": None,
        "secondary_color": None,
        "text_color": None,
        "title_color": None,
        "table_color": None,
    }
    uri = parse.unquote(request.build_absolute_uri()).replace("next=/", "")

    params_str = (
        parse.urlsplit(uri).query.replace("?", "").replace(settings.PREFIX_URL, "")
    )

    current_site = get_current_site(request)
    url_qs = ""

    site = models.Site.objects.filter(name=current_site.name).first()
    if site:
        customization = {
            "application_title": site.application_title
            if site.application_title
            else config.APPLICATION_TITLE,
            "application_subtitle": site.application_subtitle
            if site.application_subtitle
            else config.APPLICATION_SUBTITLE,
            "application_description": site.application_description
            if site.application_description
            else config.APPLICATION_DESCRIPTION,
            "background_image": site.background_image
            if site.background_image
            else None,
            "background_color": site.background_color,
            "login_background_color": site.login_background_color,
            "primary_color": site.primary_color,
            "secondary_color": site.secondary_color,
            "text_color": site.text_color,
            "title_color": site.title_color,
            "table_color": site.table_color,
        }
    context.update({"customization": customization})
    if "entityfilter" in parse.parse_qs(params_str).keys():
        for value in parse.parse_qs(params_str)["entityfilter"]:
            url_qs += "&entityfilter=" + value

    if "typefilter" in parse.parse_qs(params_str).keys():
        typesfilter_qs = ""
        for value in parse.parse_qs(params_str)["typefilter"]:
            url_qs += "&typefilter=" + value
    if url_qs:
        context.update({"query_string": url_qs[1:]})
    return context
