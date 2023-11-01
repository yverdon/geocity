import os, requests

from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from constance import config


def image_display(request, form_id, image_name, thumbor_params):

    if config.THUMBOR_SERVICE_URL:
        # TODO: use reverse to get the image URL and setup communication between geocity and thumbor composition
        test_url = 'https%3A%2F%2Fgithub.com%2Fthumbor%2Fthumbor%2Fraw%2Fmaster%2Fexample.jpg'
        resp = requests.get(f'{config.THUMBOR_SERVICE_URL}/unsafe/{thumbor_params}/{test_url}')
        
        thumbor_response =  FileResponse(resp, content_type="image/jpeg")
        return thumbor_response
    else:
        # thumbor service not configured
        return image_service(request, form_id, image_name)

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
