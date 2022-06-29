from urllib import parse

from constance import config
from django.conf import settings

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

    request.session["templatename"] = None
    url_qs = ""

    if "template" in parse.parse_qs(params_str).keys():
        template_value = parse.parse_qs(params_str)["template"][0]
        template = models.PermitSite.objects.filter(templatename=template_value).first()
        if template:
            customization = {
                "application_title": template.application_title
                if template.application_title
                else config.APPLICATION_TITLE,
                "application_subtitle": template.application_subtitle
                if template.application_subtitle
                else config.APPLICATION_SUBTITLE,
                "application_description": template.application_description
                if template.application_description
                else config.APPLICATION_DESCRIPTION,
                "background_image": template.background_image
                if template.background_image
                else None,
                "background_color": template.background_color,
                "login_background_color": template.login_background_color,
                "primary_color": template.primary_color,
                "secondary_color": template.secondary_color,
                "text_color": template.text_color,
                "title_color": template.title_color,
                "table_color": template.table_color,
            }
            request.session["templatename"] = template.templatename
            url_qs = "&template=" + template.templatename
        # use anonymous session
        request.session["template"] = template_value
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
