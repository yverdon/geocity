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
        "background_color": config.BACKGROUND_COLOR,
        "login_background_color": config.LOGIN_BACKGROUND_COLOR,
        "primary_color": config.PRIMARY_COLOR,
        "secondary_color": config.SECONDARY_COLOR,
        "text_color": config.TEXT_COLOR,
        "title_color": config.TITLE_COLOR,
        "table_color": config.TABLE_COLOR,
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
                "background_color": template.background_color
                if template.background_color
                else config.BACKGROUND_COLOR,
                "login_background_color": template.login_background_color
                if template.login_background_color
                else config.LOGIN_BACKGROUND_COLOR,
                "primary_color": template.primary_color
                if template.primary_color
                else config.PRIMARY_COLOR,
                "secondary_color": template.secondary_color
                if template.secondary_color
                else config.SECONDARY_COLOR,
                "text_color": template.text_color
                if template.text_color
                else config.TEXT_COLOR,
                "title_color": template.title_color
                if template.title_color
                else config.TITLE_COLOR,
                "table_color": template.table_color
                if template.table_color
                else config.TABLE_COLOR,
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
