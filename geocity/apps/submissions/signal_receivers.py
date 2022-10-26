from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from . import services


@receiver(user_logged_in)
def store_tags_in_session_on_log_in(sender, request, *args, **kwargs):
    services.store_tags_in_session(request)
