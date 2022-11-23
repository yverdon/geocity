from allauth.account import utils
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from allauth.utils import build_absolute_uri
from django.conf import settings
from django.db import transaction

from geocity.apps.accounts.models import UserProfile


class GeomapfishAdapterError(Exception):
    pass


class GeomapfishSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_signup_form_initial_data(self, sociallogin):
        user = sociallogin.user
        initial = {
            "email": utils.user_email(user) or "",
            "username": utils.user_username(user) or "",
            "first_name": utils.user_field(user, "first_name") or "",
            "last_name": utils.user_field(user, "last_name") or "",
        }
        return initial

    @transaction.atomic
    def save_user(self, request, sociallogin: SocialLogin, form=None):
        if not form:
            # A subscription form is enforced by settings.SOCIALACCOUNT_AUTO_SIGNUP
            # If subscription form is bypassed, the subscription can't proceed.
            raise GeomapfishAdapterError("Subscription form is missing.")

        user = sociallogin.user
        user.set_unusable_password()
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")

        sociallogin.save(request)

        user_profile = UserProfile(
            user=user,
            address=form.cleaned_data["address"],
            zipcode=form.cleaned_data["zipcode"],
            city=form.cleaned_data["city"],
            phone_first=form.cleaned_data["phone_first"],
            phone_second=form.cleaned_data["phone_second"],
            company_name=form.cleaned_data["company_name"],
            vat_number=form.cleaned_data["vat_number"],
        )

        if settings.AUTHOR_IBAN_VISIBLE:
            user_profile.iban = form.cleaned_data["iban"]

        user_profile.save()

        return user

    def get_connect_redirect_url(self, request, socialaccount):
        return build_absolute_uri(request, settings.LOGIN_REDIRECT_URL)
