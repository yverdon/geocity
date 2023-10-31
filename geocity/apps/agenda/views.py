import os

from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import render


# TODO: Place this view in the form or submission, so we have direct access to the image settings, public or not ? From API
def image_display(request, form_id, image_name):
    image_dir = settings.PRIVATE_MEDIA_ROOT

    image_path = os.path.join(
        image_dir, f"permit_requests_uploads/{form_id}/{image_name}"
    )

    # TODO: Ajouter de la sécurité afin de savoir si l'image peut-être affichée ou non
    if os.path.exists(image_path):
        image_file = open(image_path, "rb")
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
