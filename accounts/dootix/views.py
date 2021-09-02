import requests
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2Client,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from .provider import DootixProvider
from django.conf import settings
from django.utils.http import urlencode


# Dootix oAuth backend does not accept redirect_uri param in request, thus, remove it
class OAuth2ClientCustom(OAuth2Client):
    def get_redirect_url(self, authorization_url, extra_params):
        params = {
            "client_id": self.consumer_key,
            "scope": self.scope,
            "response_type": "code",
        }
        if self.state:
            params["state"] = self.state
        params.update(extra_params)
        return "%s?%s" % (authorization_url, urlencode(params))


class DootixAdapter(OAuth2Adapter):
    provider_id = DootixProvider.id

    client_class = OAuth2ClientCustom

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


oauth2_login = OAuth2LoginView.adapter_view(DootixAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DootixAdapter)
