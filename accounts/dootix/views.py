import requests
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2Client,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from allauth.utils import build_absolute_uri
from django.urls import reverse

from .provider import DootixProvider
from django.conf import settings


class DootixAdapter(OAuth2Adapter):
    provider_id = DootixProvider.id

    client_class = OAuth2Client

    # Fetched programmatically, must be reachable from container
    access_token_url = "{}/oauth/token".format(settings.AUTH_PROVIDER_DOOTIX_URL)

    # URL to reach Dootix login form
    authorize_url = "{}/oauth/authorize".format(settings.AUTH_PROVIDER_DOOTIX_URL)
    profile_url = "{}/api/user".format(settings.AUTH_PROVIDER_DOOTIX_URL)

    def complete_login(self, request, app, token, **kwargs) -> SocialLogin:
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def get_callback_url(self, request, app):
        callback_url = reverse(self.provider_id + "_callback")
        protocol = self.redirect_uri_protocol
        callback_url = build_absolute_uri(request, callback_url, protocol)

        return build_absolute_uri(request, callback_url, protocol)


oauth2_login = OAuth2LoginView.adapter_view(DootixAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DootixAdapter)
