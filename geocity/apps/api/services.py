import os
import re
from io import BytesIO

from django.conf import settings
from django.db.models import Q
from django.utils.text import get_valid_filename
from PIL import Image
from unidecode import unidecode


def convert_string_to_api_key(string):
    # Convert to lower and remove accents
    string = unidecode(string.lower())
    # Delete special characters and spaces
    string = re.sub("[^a-z0-9_ ]", "", string)
    string = string.replace(" ", "_")
    return string


def get_mime_type(content):
    """
    Used to retrieve mime type in response.content of request
    """
    image = Image.open(BytesIO(content))
    image_format = image.format
    mime_type = "image/" + image_format.lower()
    return mime_type


def can_image_be_displayed_for_agenda(
    submission_id, image_name, Submission, FieldValue
):
    """
    Display image for :
    - Submission with
        - agenda activated
        - public
        - VISIBLE_IN_AGENDA_STATUSES
    - and FieldValue with
        - public_if_submission_public
    """
    safe_submission_id = get_valid_filename(submission_id)
    safe_image_name = get_valid_filename(image_name)

    submission_display_conditions = Submission.objects.filter(
        Q(pk=safe_submission_id)
        & Q(selected_forms__form__agenda_visible=True)
        & Q(is_public_agenda=True)
        & Q(status__in=Submission.VISIBLE_IN_AGENDA_STATUSES)
    ).exists()

    image_name_in_db = {
        "val": f"permit_requests_uploads/{safe_submission_id}/{safe_image_name}"
    }

    fieldvalue_display_conditions = FieldValue.objects.filter(
        Q(value=image_name_in_db) & Q(field__public_if_submission_public=True)
    ).exists()

    return submission_display_conditions and fieldvalue_display_conditions


def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height


def get_image_path(submission_id, image_name):
    image_dir = settings.PRIVATE_MEDIA_ROOT

    safe_submission_id = get_valid_filename(submission_id)
    safe_image_name = get_valid_filename(image_name)

    image_path = os.path.join(
        image_dir, f"permit_requests_uploads/{safe_submission_id}/{safe_image_name}"
    )

    return image_path
