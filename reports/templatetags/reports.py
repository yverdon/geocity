import typing
import io
import tarfile
from django import template
from django.utils.safestring import mark_safe
from jinja2.sandbox import SandboxedEnvironment
from rest_framework.authtoken.models import Token
import requests
import base64
import docker
import tempfile

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
    token, _ = Token.objects.get_or_create(user=request.user)


    project_file = context["block_content"].qgis_project_file.file
    template_name = context["block_content"].qgis_print_template_name
    permit_request_id = context["permit_request"].id


    client = docker.from_env()


    print("-!"*60)
    # commands = [template_name, permit_request_id, token.key, base64.b64encode(project_content).decode("ascii"),]
    # commands = [template_name, permit_request_id, token.key, "abcabc"]
    # commands = [template_name, permit_request_id, token.key]
    # commands = [template_name, permit_request_id, token.key]
    # commands = ["echo", "1", "world", "dGVzdA=="]
    # data = client.containers.run("geocity_qgis", commands)


    # data = client.containers.run("alpine", ["echo", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",])
    # data = data.decode().strip()
    # print(str(data))

    commands = [str(template_name), str(permit_request_id), str(token.key), "/io/project.qgs", "/io/output.png",]
    container = client.containers.create("geocity_qgis", commands, network="geocity_pdf_generation")

    input_tar = _create_input_tar(project_file)
    container.put_archive("/io", input_tar)

    # Run the model
    container.start()
    container.wait(timeout=30)

    logs = container.logs().decode("utf-8")
    print("-."*60)
    print(logs)

    output_tar, stat = container.get_archive("/io")
    output = _extract_output_tar(output_tar)

    # Cleanup container
    container.remove()



    # TODO CRITICAL: add expiration to token
    # token, _ = Token.objects.get_or_create(user=request.user)
    # data = {
    #     "template_name": template_name,
    #     "token": token.key,
    #     "permit_request_id": permit_request_id,
    # }
    # files = {
    #     "project_content": project_content,
    # }
    # img_response = requests.post("http://qgis:5000/", data=data, files=files)


    # # return mark_safe(img_response.content.decode("utf-8"))

    data = base64.b64encode(output.read()).decode('ascii')
    return mark_safe(f"<img src=\"data:image/png;base64,{data}\">")


def _create_input_tar(uploaded_file):
    """
    Packs the provided file as `project.qgs` in a tar archive
    (to be used with `docker.container.put_archive(...)`)
    """
    uploaded_file.seek(0)
    tar_input_data = io.BytesIO()
    tar_input_file = tarfile.TarFile(mode="w", fileobj=tar_input_data)
    tarinfo = tarfile.TarInfo("project.qgs")
    tarinfo.size = uploaded_file.size
    tar_input_file.addfile(tarinfo, uploaded_file)
    tar_input_file.close()
    tar_input_data.seek(0)
    return tar_input_data


def _extract_output_tar(output_tar):
    """
    Extracts `output.png` from the given tar archive
    (to be used with `docker.container.get_archive(...)`)
    """
    tar_output_data = io.BytesIO()
    for chunk in output_tar:
        tar_output_data.write(chunk)
    tar_output_data.flush()
    tar_output_data.seek(0)
    tar_output_file = tarfile.TarFile(mode="r", fileobj=tar_output_data)
    print(tar_output_file.getmembers())
    return tar_output_file.extractfile("io/output.png")
