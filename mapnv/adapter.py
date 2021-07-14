from allauth.account.adapter import get_adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

from permits.models import PermitAuthor


class MapnvSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Use this class to override actions done during social login.
    FIXME:
     Use get_connect_redirect_url & populate_user,
     to fill the missing fields with a form.

     => https://django-allauth.readthedocs.io/en/latest/forms.html#socialaccount-forms
    """
    def new_user(self, request, sociallogin):
        # FIXME: Use rather "populate_user"
        user = get_user_model()()
        permit_author = PermitAuthor(
            user=user,
            address="Required",
            zipcode="Required",
            city="Required",
            phone_first="Required",
        )

        return user
