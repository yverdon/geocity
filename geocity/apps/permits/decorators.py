from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django_otp import user_has_device

from geocity.apps.permits import models, services


def check_mandatory_2FA(
    view=None, redirect_field_name="next", login_url="profile", if_configured=False
):
    """
    Do same as :func:`django_otp.decorators.otp_required`, then verify if the user
    is in a group where 2FA is required.
    """

    def test(user):
        if services.is_2FA_mandatory(user):
            permit_department = (
                models.PermitDepartment.filter_active_duo_configurations_for_user_as_qs(
                    user
                )
            )

            return (
                user.is_verified()
                or (
                    if_configured
                    and user.is_authenticated
                    and not user_has_device(user)
                )
                or permit_department
            )
        else:
            return True

    decorator = user_passes_test(
        test, login_url=login_url, redirect_field_name=redirect_field_name
    )

    return decorator if (view is None) else decorator(view)


def permanent_user_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorate after login required, to enforce that the user is also not temporary.
    """

    def test(user):
        try:
            permitauthor = user.permitauthor
        except ObjectDoesNotExist:
            return True
        else:
            return not permitauthor.is_temporary

    decorator = user_passes_test(
        test, login_url=login_url, redirect_field_name=redirect_field_name
    )
    if function:
        return decorator(function)
    return decorator
