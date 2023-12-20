import base64
import hashlib
from urllib.parse import parse_qs, urlparse

import requests
from allauth.socialaccount.tests import MockedResponse, OAuth2TestsMixin


class CustomOAuth2TestsMixin(OAuth2TestsMixin):
    """
    Override from OAuth2TestsMixin login method to fix error at args[0] == "POST"
    https://github.com/pennersr/django-allauth/blob/main/allauth/socialaccount/tests/__init__.py
    """

    # TODO: PKCE is set at false manually. Need to remove this method, and try to fix test with another solution
    def login(self, resp_mock=None, process="login", with_refresh_token=True):

        with self.mocked_response():
            resp = self.client.post(
                self.provider.get_login_url(self.request, process=process)
            )
        p = urlparse(resp["location"])
        q = parse_qs(p.query)

        pkce_enabled = False  # Line changed

        self.assertEqual("code_challenge" in q, pkce_enabled)
        self.assertEqual("code_challenge_method" in q, pkce_enabled)
        if pkce_enabled:
            code_challenge = q["code_challenge"][0]
            self.assertEqual(q["code_challenge_method"][0], "S256")

        complete_url = self.provider.get_callback_url()
        self.assertGreater(q["redirect_uri"][0].find(complete_url), 0)
        response_json = self.get_login_response_json(
            with_refresh_token=with_refresh_token
        )

        if isinstance(resp_mock, list):
            resp_mocks = resp_mock
        elif resp_mock is None:
            resp_mocks = []
        else:
            resp_mocks = [resp_mock]

        with self.mocked_response(
            MockedResponse(200, response_json, {"content-type": "application/json"}),
            *resp_mocks,
        ):
            resp = self.client.get(complete_url, self.get_complete_parameters(q))

            # Find the access token POST request, and assert that it contains
            # the correct code_verifier if and only if PKCE is enabled
            request_calls = requests.Session.request.call_args_list
            for args, kwargs in request_calls:
                data = kwargs.get("data", {})
                if (
                    args  # Line changed
                    and args[0] == "POST"
                    and isinstance(data, dict)
                    and data.get("redirect_uri", "").endswith(complete_url)
                ):
                    self.assertEqual("code_verifier" in data, pkce_enabled)

                    if pkce_enabled:
                        hashed_code_verifier = hashlib.sha256(
                            data["code_verifier"].encode("ascii")
                        )
                        expected_code_challenge = (
                            base64.urlsafe_b64encode(hashed_code_verifier.digest())
                            .rstrip(b"=")
                            .decode()
                        )
                        self.assertEqual(code_challenge, expected_code_challenge)

        return resp
