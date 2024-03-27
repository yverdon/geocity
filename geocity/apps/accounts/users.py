"""
TODO We should swap the default user model for a custom one.

Using a proxy model has a lot of limitations, eg. `request.user` is still the default
Django user, and traversing relationships won’t return the custom user model.
"""
import functools
import operator

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.db.models import Q, Value
from django.db.models.functions import StrIndex, Substr

from . import models, permissions_groups


def has_profile(user):
    try:
        user.userprofile
    except models.UserProfile.DoesNotExist:
        return False

    return True


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


def get_users_list_for_integrator_admin(user, remove_anonymous=False):
    qs = User.objects.select_related("userprofile")

    # Remove anonymous users
    anonymous_users = []
    if remove_anonymous:
        for qs_user in qs:
            if qs_user.userprofile.is_anonymous:
                anonymous_users.append(qs_user.pk)
        qs = qs.exclude(pk__in=anonymous_users)

    # Integrators can only view users for restricted email domains.
    if not user.is_superuser:
        user_integrator_group = user.groups.get(
            permit_department__is_integrator_admin=True
        )

        email_domains = [
            domain.strip()
            for domain in user_integrator_group.permit_department.integrator_email_domains.split(
                ","
            )
        ]

        emails = [
            email.strip()
            for email in user_integrator_group.permit_department.integrator_emails_exceptions.split(
                ","
            )
        ]

        qs = (
            qs.annotate(
                email_domain=Substr("email", StrIndex("email", Value("@")) + 1),
            )
            # hide anynomous user not belonging to the actual integrator
            .filter(
                Q(is_superuser=False),
                Q(email_domain__in=email_domains) | Q(email__in=emails),
                Q(groups__permit_department__integrator=user_integrator_group.pk)
                | Q(groups__isnull=True)
                | Q(groups__permit_department__is_integrator_admin=True),
            )
            .exclude()
            .distinct()
        )

    return qs
