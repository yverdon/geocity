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
        return str(data["id"])

    def extract_common_fields(self, data):
        """
        Extract common fields to populate the User instance.
        From Dootix :
        {
            'id': 5,
            'name': 'Geocity Sports',
            'email': 'geocity@dootix.com',
            'email_verified_at': None,
            'use_2fa': 0,
            'created_at': '2021-08-31T12:26:15.000000Z',
            'updated_at': '2021-10-14T14:44:58.000000Z',
            'locale': 'fr_CH',
            'last_login': '2021-10-14 16:44:58'
        }
        FIXME:
         Provide from Dootix: username, first_name, last_name
        """
        # permitauthor
        return dict(name=data["name"], email=data["email"],)

    def get_default_scope(self):
        return []


provider_classes = [DootixProvider]
