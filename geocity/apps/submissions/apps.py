from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SubmissionsConfig(AppConfig):
    name = "geocity.apps.submissions"
    verbose_name = _("Traitement et documents")

    def ready(self):
        from . import signal_receivers

