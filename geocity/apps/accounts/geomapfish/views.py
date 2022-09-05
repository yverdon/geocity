import requests
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from django.conf import settings

from .provider import GeomapfishProvider


class GeomapfishAdapter(OAuth2Adapter):
    provider_id = GeomapfishProvider.id

    # Fetched programmatically, must be reachable from container
    access_token_url = "{}/oauth/token".format(settings.AUTH_PROVIDER_GEOMAPFISH_URL)

    # URL to reach Geomapfish login form
    authorize_url = "{}/oauth/login".format(settings.AUTH_PROVIDER_GEOMAPFISH_URL)
    profile_url = "{}/loginuser".format(settings.AUTH_PROVIDER_GEOMAPFISH_URL)

    def complete_login(self, request, app, token, **kwargs) -> SocialLogin:
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(GeomapfishAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(GeomapfishAdapter)
