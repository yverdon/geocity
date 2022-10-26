from django.urls import reverse


def reverse_submission_url(name, submission):
    return reverse(name, kwargs={"submission_id": submission.pk})


def comma_splitter(tag_string):
    return [t.strip().lower() for t in tag_string.split(",") if t.strip()]
