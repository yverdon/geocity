from django.apps import AppConfig


class SubmissionsConfig(AppConfig):
    name = "geocity.apps.submissions"
    verbose_name = "2 - Traitement"

    def ready(self):
        from . import signal_receivers  # noqa
