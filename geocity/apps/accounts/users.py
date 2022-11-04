"""
TODO We should swap the default user model for a custom one.

Using a proxy model has a lot of limitations, eg. `request.user` is still the default
Django user, and traversing relationships won’t return the custom user model.
"""
from django.conf import settings

from . import models


def has_profile(user):
    try:
        user.userprofile
    except models.UserProfile.DoesNotExist:
        return False

    return True


def get_administrative_entities_associated_to_user(user):
    return models.AdministrativeEntity.objects.filter(
        departments__group__in=user.groups.all(),
    ).order_by("ofs_id", "-name")


def get_departments(user):
    return models.PermitDepartment.objects.filter(group__in=user.groups.all())


def is_2FA_mandatory(user):
    return (
        settings.ENABLE_2FA
        and user.groups.filter(permit_department__mandatory_2fa=True).exists()
    )
