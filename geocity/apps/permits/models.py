from . import fields  # noqa


def printed_permit_request_storage(instance, filename):
    return f"permit_requests_uploads/{instance.permit_request.pk}/{filename}"
