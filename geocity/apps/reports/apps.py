from django.apps import AppConfig


class ReportsConfig(AppConfig):
    name = "geocity.apps.reports"
    verbose_name = "3 - Rapports"

    def ready(self):
        from . import signals  # noqa
