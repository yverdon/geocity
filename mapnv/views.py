import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from .provider import MapnvProvider
from django.conf import settings


class MapnvAdapter(OAuth2Adapter):
    provider_id = MapnvProvider.id

    # Fetched programmatically, must be reachable from container
    access_token_url = "{}/oauth/token".format(settings.AUTH_PROVIDER_MAPNV_URL)

    # URL to reach Mapnv login form
    authorize_url = "{}/oauth/login".format(settings.AUTH_PROVIDER_MAPNV_URL)
    profile_url = '{}/loginuser'.format(settings.AUTH_PROVIDER_MAPNV_URL)

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        new_user = self.get_provider().sociallogin_from_response(request, extra_data)
        return new_user


oauth2_login = OAuth2LoginView.adapter_view(MapnvAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(MapnvAdapter)
