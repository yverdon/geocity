from django.urls import reverse


def reverse_permit_request_url(name, permit_request):
    return reverse(name, kwargs={"permit_request_id": permit_request.pk})

def comma_splitter(tag_string):
    return [t.strip().lower() for t in tag_string.split(',') if t.strip()]