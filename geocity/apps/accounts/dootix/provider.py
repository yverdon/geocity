from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class DootixAccount(ProviderAccount):
    pass


class DootixProvider(OAuth2Provider):

    id = "dootix"
    name = "Dootix"
    account_class = DootixAccount

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        """
        Extract available/matching fields to populate the User instance.
        """
        # User profile
        return dict(
            name=data["name"],
            email=data["email"],
        )

    def get_default_scope(self):
        return []


provider_classes = [DootixProvider]
