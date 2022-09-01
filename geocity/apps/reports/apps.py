from django.apps import AppConfig


class ReportsConfig(AppConfig):
    name = "reports"

    def ready(self):
        from . import signals  # noqa
