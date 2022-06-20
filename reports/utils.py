import io
import os
import tarfile
from typing import IO, Tuple

import docker


class DockerRunFailedError(Exception):
    def __init__(self, exit_code, logs):
        self.exit_code = exit_code
        self.logs = logs


def run_docker_container(image, commands, file_input: Tuple[str, IO], file_output):

    # Create a docker container to generate the image
    client = docker.from_env()
    container = client.containers.create(
        image,
        commands,
        network="geocity_isolated",
    )

    # Copy QGIS project to the container
    if file_input:
        path, file = file_input
        _put_file(container, path, file)

    # Run the container
    container.start()
    r = container.wait(timeout=60)

    logs = container.logs().decode("utf-8")
    print(logs)

    # Check if it succeeded
    exit_code = r["StatusCode"]
    try:
        if exit_code == 0:
            # Retrieve the output
            return _get_file(container, file_output)
    finally:
        container.remove()

    raise DockerRunFailedError(exit_code, logs)


def _put_file(container, path, project_file):
    """Copies the given file to path in the given container"""
    # TODO: rewrite this in a more readable way
    dirname, filename = os.path.split(path)
    project_file.seek(0)
    tar_input_data = io.BytesIO()
    tar_input_file = tarfile.TarFile(mode="w", fileobj=tar_input_data)
    tarinfo = tarfile.TarInfo(filename)
    tarinfo.size = _file_size(project_file)
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


def _file_size(file):
    _pos = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(_pos)
    return size
