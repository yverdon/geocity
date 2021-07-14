import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
from .provider import DootixProvider
from django.conf import settings


class DootixAdapter(OAuth2Adapter):
    provider_id = DootixProvider.id

    # Fetched programmatically, must be reachable from container
    access_token_url = "{}/oauth/token".format(settings.AUTH_PROVIDER_DOOTIX_URL)
    profile_url = '{}/profile/'.format(settings.AUTH_PROVIDER_DOOTIX_URL)

    # Accessed by the user browser, must be reachable by the host
    authorize_url = '{}/o/authorize/'.format('http://localhost:9977')

    # NOTE: trailing slashes in URLs are important, don't miss it

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(DootixAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DootixAdapter)
