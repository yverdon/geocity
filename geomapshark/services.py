from constance import config
from urllib import parse
from permits import models


def get_context_data(context, request):

    customization = {
        "application_title": config.APPLICATION_TITLE,
        "application_subtitle": config.APPLICATION_SUBTITLE,
        "application_description": config.APPLICATION_DESCRIPTION,
        "background_image": None,
    }
    uri = parse.unquote(request.build_absolute_uri()).replace("next=/", "")
    params_str = parse.urlsplit(uri).query.replace("?", "")
    request.session["templatename"] = None
    url_qs = ""

    if "template" in parse.parse_qs(params_str).keys():
        template_value = parse.parse_qs(params_str)["template"][0]
        template = models.TemplateCustomization.objects.filter(
            templatename=template_value
        ).first()
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
            }
            request.session["templatename"] = template.templatename
        url_qs = "&template_value"
        # use anonymous session
        request.session["template"] = template_value
    context.update({"customization": customization})
    if "filter" in parse.parse_qs(params_str).keys():
        for value in parse.parse_qs(params_str)["filter"]:
            url_qs += "&filter=" + value

    if "typefilter" in parse.parse_qs(params_str).keys():
        typesfilter_qs = ""
        for value in parse.parse_qs(params_str)["typefilter"]:
            url_qs += "&typefilter=" + value

    if url_qs:
        context.update({"query_string": url_qs[1:]})
    return context
