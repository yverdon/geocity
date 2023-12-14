import json

from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from geocity.apps.accounts.dootix.provider import DootixProvider

User = get_user_model()

# Dootix profile_url success response mock.
# Happen if login succeeded.
profile_response_mock = {
    "id": 5,
    "name": "Geocity Sports",
    "email": "geocity@dootix.com",
    "email_verified_at": None,
    "use_2fa": 0,
    "created_at": "2021-08-31T12:26:15.000000Z",
    "updated_at": "2021-10-14T14:44:58.000000Z",
    "locale": "fr_CH",
    "last_login": "2021-10-14 16:44:58",
}


class DootixOAuth2Tests(OAuth2TestsMixin, TestCase):
    """
    Default OAuth2 automated tests + dootix specific tests.
    """

    provider_id = DootixProvider.id

    def get_mocked_response(self, email="foo@bar.ch"):
        profile_response_mock.update(
            {
                "email": email,
            }
        )
        return MockedResponse(200, json.dumps(profile_response_mock))

    def test_login_redirects_to_social_signup(self):
        email = "foo@bar.ch"
        response = self.login(self.get_mocked_response(email))
        self.assertRedirects(response, expected_url=reverse("socialaccount_signup"))

    def test_social_signup_form_display_socialaccount_data(self):
        sociallogin_redirect = self.login(
            self.get_mocked_response("example@test.org"),
        )
        signup_response = self.client.get(sociallogin_redirect.url)
        self.assertContains(signup_response, "example@test.org")

    def test_authentication_error(self):
        pass
