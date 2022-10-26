from django.apps import AppConfig


class SubmissionsConfig(AppConfig):
    name = "geocity.apps.submissions"

    def ready(self):
        from . import signal_receivers
