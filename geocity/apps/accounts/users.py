"""
TODO We should swap the default user model for a custom one.

Using a proxy model has a lot of limitations, eg. `request.user` is still the default
Django user, and traversing relationships won’t return the custom user model.
"""
import functools
import operator

from django.conf import settings
from django.contrib.auth.models import Permission
from django.db.models import Q

from . import models, permissions_groups


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


def get_integrator_permissions():
    permission_filters = functools.reduce(
        operator.or_,
        [
            Q(content_type__app_label=app_label)
            & Q(content_type__model__in=permissions)
            for app_label, permissions in permissions_groups.INTEGRATOR_PERMISSIONS_BY_APP.items()
        ],
    )

    return Permission.objects.filter(
        permission_filters
        | Q(codename__in=permissions_groups.OTHER_PERMISSIONS_CODENAMES)
    )
