from allauth.account import utils
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin

from permits.models import PermitAuthor


class MapnvAdapterError(Exception):
    pass


class MapnvSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_signup_form_initial_data(self, sociallogin):
        user = sociallogin.user
        initial = {
            "email": utils.user_email(user) or "",
            "username": utils.user_username(user) or "",
            "first_name": utils.user_field(user, "first_name") or "",
            "last_name": utils.user_field(user, "last_name") or "",
        }
        return initial

    def save_user(self, request, sociallogin: SocialLogin, form=None):
        if not form:
            # A subscription form is enforced by settings.SOCIALACCOUNT_AUTO_SIGNUP
            # If subscription form is bypassed, the subscription can't proceed.
            raise MapnvAdapterError("Subscription form is missing.")

        user = sociallogin.user
        user.set_unusable_password()
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")

        sociallogin.save(request)

        PermitAuthor.objects.create(
            user=user,
            address=form.cleaned_data["address"],
            zipcode=form.cleaned_data["zipcode"],
            city=form.cleaned_data["city"],
            phone_first=form.cleaned_data["phone_first"],
            phone_second=form.cleaned_data["phone_second"],
            company_name=form.cleaned_data["company_name"],
            vat_number=form.cleaned_data["vat_number"],
        )

        return user
