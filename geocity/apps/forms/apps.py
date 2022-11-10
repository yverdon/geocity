from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FormsConfig(AppConfig):
    name = "geocity.apps.forms"
    verbose_name = _("Formulaires")
