import os

import requests
from constance import config
from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import render


def image_display(request, form_id, image_name, thumbor_params):

    INTERNAL_WEB_ROOT_URL = "http://web:9000"
    image_url = f"{INTERNAL_WEB_ROOT_URL}/agenda/image/display/permit_requests_uploads/{form_id}/{image_name}"
    resp = requests.get(
        f"{config.THUMBOR_SERVICE_URL}/unsafe/{thumbor_params}/{image_url}"
    )
    thumbor_response = FileResponse(resp, content_type="image/jpeg")
    return thumbor_response


def image_service(request, form_id, image_name):

    image_dir = settings.PRIVATE_MEDIA_ROOT

    image_path = os.path.join(
        image_dir, f"permit_requests_uploads/{form_id}/{image_name}"
    )

    # TODO: Secure access
    if os.path.exists(image_path):
        image_file = open(image_path, "rb")
        # TODO: support PNG
        response = FileResponse(image_file, content_type="image/jpeg")
        return response
    else:
        return JsonResponse({"message": "Image non trouvée."}, status=404)


def agenda(request):
    return render(
        request,
        "agenda/agenda.html",
        {},
    )
