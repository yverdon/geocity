from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.conf import settings


class MapnvAccount(ProviderAccount):
    pass


class MapnvProvider(OAuth2Provider):

    id = "mapnv"
    name = 'Mapnv'
    account_class = MapnvAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        from pprint import pprint
        return dict(username=data['username'],
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],)

    def get_default_scope(self):
        scope = ['read']
        return scope


provider_classes = [MapnvProvider]
