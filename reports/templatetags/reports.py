import typing
import io
import tarfile
from django import template
from django.utils.safestring import mark_safe
from jinja2.sandbox import SandboxedEnvironment
from rest_framework.authtoken.models import Token
import base64
import os
from django.contrib.staticfiles import finders
from ..utils import run_docker_container, DockerRunFailedError

register = template.Library()

@register.simple_tag
def render_block(obj, **context):
    return obj.render(context)


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
    """Includes a QGIS map as an image (embedded as dataurl). The image is generated in an isolated container."""

    project_file = context["block_content"].qgis_project_file.file
    template_name = context["block_content"].qgis_print_template_name
    permit_request_id = context["permit_request"].id
    token = context["token"]

    # Create a docker container to generate the image
    commands = [
        "/io/project.qgs",
        "/io/output.png",
        str(template_name),
        str(permit_request_id),
        str(token),
    ]

    try:
        output = run_docker_container(
            "geocity_qgis",
            commands,
            file_input=("/io/project.qgs", project_file),
            file_output="/io/output.png",
        )
    except DockerRunFailedError:
        # Return error image
        path = finders.find("reports/error.png")
        output = open(path, "rb")

    # Prepare the dataurl
    data = base64.b64encode(output.read()).decode("ascii")
    data_url = f"data:image/png;base64,{data}"

    # Render
    return mark_safe(f'<img src="{data_url}">')
