import typing
from django import template
from django.utils.safestring import mark_safe
from jinja2.sandbox import SandboxedEnvironment
from rest_framework.authtoken.models import Token
import requests
import base64

register = template.Library()


@register.simple_tag
def render_user_template(template_str, data):
    """Renders a user given template in a hopefully safe way"""
    env = SandboxedEnvironment()
    contents = env.from_string(template_str).render({"data": data})
    return mark_safe(contents)


@register.filter
def iterate_nested_dict(data):
    """Iterate recursively through a dict, returning keys, value and class in a flat list."""

    def _iterate(val, keys: list):
        if isinstance(val, dict):
            for k, v in val.items():
                yield from _iterate(v, [*keys, str(k)])
        else:
            yield (".".join(keys), repr(val), val.__class__.__name__)

    return _iterate(data, ["data"])


@register.simple_tag(takes_context=True)
def include_qgis_map(context):

    request = context["request"]

    project_path = context["block_content"].qgis_project_file.path
    project_content = open(project_path, "rb").read()
    template_name = context["block_content"].qgis_print_template_name
    permit_request_id = context["permit_request"].id

    # TODO CRITICAL: add expiration to token
    token, _ = Token.objects.get_or_create(user=request.user)
    data = {
        "template_name": template_name,
        "token": token.key,
        "permit_request_id": permit_request_id,
    }
    files = {
        "project_content": project_content,
    }
    img_response = requests.post("http://qgis:5000/", data=data, files=files)


    # return mark_safe(img_response.content.decode("utf-8"))

    data = base64.b64encode(img_response.content).decode('ascii')
    return mark_safe(f"<img src=\"data:image/png;base64,{data}\">")
