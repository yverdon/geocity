from django.urls import reverse


def reverse_permit_request_url(name, permit_request):
    return reverse(name, kwargs={"permit_request_id": permit_request.pk})
