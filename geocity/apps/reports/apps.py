from django.apps import AppConfig


class ReportsConfig(AppConfig):
    name = "geocity.apps.reports"

    def ready(self):
        from . import signals  # noqa
