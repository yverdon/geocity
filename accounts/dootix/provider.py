from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.conf import settings


class DootixAccount(ProviderAccount):
    pass


class DootixProvider(OAuth2Provider):

    id = "dootix"
    name = "Dootix"
    account_class = DootixAccount

    def extract_uid(self, data):
        """
        Unique ID in geomapfish is the username.
        """
        return str(data["username"])

    def extract_common_fields(self, data):
        """
        Extract common fields to populate the User instance.
        """
        # permitauthor
        return dict(
            username=data["username"], email=data["email"], roles=data["roles"],
        )

    def get_default_scope(self):
        scope = ["read"]
        return scope


provider_classes = [DootixProvider]
