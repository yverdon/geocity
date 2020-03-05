from django.core.exceptions import ValidationError
from . import models
from django.utils.translation import gettext_lazy as _


def validate_administrative_entity(value):
    administrative_entity = models.AdministrativeEntity.objects.filter(geom__contains=value)
    if not administrative_entity:
        raise ValidationError(
            _('La localisation n\' est pas située à sur un territoire communal géré par cette application'),
            params={'value': value},
        )
