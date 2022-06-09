import typing
import io
import tarfile
from django import template
from django.utils.safestring import mark_safe
from jinja2.sandbox import SandboxedEnvironment
from rest_framework.authtoken.models import Token
import base64
import docker
import os
from django.contrib.staticfiles import finders

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
    """Includes a QGIS map as an image (embedded as dataurl). The image is generated in an isolated container."""

    request = context["request"]

    token, _ = Token.objects.get_or_create(user=request.user)
    project_file = context["block_content"].qgis_project_file.file
    template_name = context["block_content"].qgis_print_template_name
    permit_request_id = context["permit_request"].id

    # Create a docker container to generate the image
    client = docker.from_env()
    commands = [
        "/io/project.qgs",
        "/io/output.png",
        str(template_name),
        str(permit_request_id),
        str(token.key),
    ]
    container = client.containers.create(
        "geocity_qgis", commands, network="geocity_pdf_generation"
    )

    # Copy QGIS project to the container
    _put_file(container, "/io/project.qgs", project_file)

    # Run the container
    container.start()
    r = container.wait(timeout=30)

    # Debug
    # print(container.logs().decode("utf-8"))

    # Check if it succeeded
    if r["StatusCode"] == 0:
        # Retrieve the output
        output = _get_file(container, "/io/output.png")
    else:
        # Return error image
        path = finders.find("reports/error.png")
        output = open(path, "rb")

    # Cleanup container
    container.remove()

    # Prepare the dataurl
    data = base64.b64encode(output.read()).decode("ascii")
    data_url = f"data:image/png;base64,{data}"

    # Render
    return mark_safe(f'<img src="{data_url}">')


def _put_file(container, path, project_file):
    """Copies the given file to path in the given container"""
    # TODO: rewrite this in a more readable way
    dirname, filename = os.path.split(path)
    project_file.seek(0)
    tar_input_data = io.BytesIO()
    tar_input_file = tarfile.TarFile(mode="w", fileobj=tar_input_data)
    tarinfo = tarfile.TarInfo(filename)
    tarinfo.size = project_file.size
    tar_input_file.addfile(tarinfo, project_file)
    tar_input_file.close()
    tar_input_data.seek(0)
    input_tar = tar_input_data
    container.put_archive(dirname, input_tar)


def _get_file(container, path):
    """Retrieves the given file from the given container"""
    # TODO: rewrite this in a more readable way
    _, filename = os.path.split(path)
    output_tar, stat = container.get_archive(path)
    tar_output_data = io.BytesIO()
    for chunk in output_tar:
        tar_output_data.write(chunk)
    tar_output_data.flush()
    tar_output_data.seek(0)
    tar_output_file = tarfile.TarFile(mode="r", fileobj=tar_output_data)
    return tar_output_file.extractfile(filename)
