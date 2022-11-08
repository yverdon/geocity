from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ReportsConfig(AppConfig):
    name = "geocity.apps.reports"
    verbose_name = _("Rapports")

    def ready(self):
        from . import signals  # noqa
