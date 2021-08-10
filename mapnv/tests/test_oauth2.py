import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from ..provider import MapnvProvider
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase


User = get_user_model()

# Mapnv profile_url success response mock.
# Happen if login succeeded.
# That's all the data we can get from MAPNV.
profile_response_mock = {
    "username": "test",
    "email": "olm@ylb.ch",
    "functionalities": {
        "default_basemap": [],
        "default_theme": [],
        "filterable_layers": [
            "station_armoire_depart",
            "ELE_tube",
            "VD_batiment_rcb",
            "qwat_conduites",
            "YLB - Gestion des surface par service responsable",
            "qgep_conduites",
            "WAS_conduite",
            "MO_bf_bien_fonds",
            "ELE_branchement_immeuble",
            "GAS_conduite_bp",
        ],
        "open_panel": [],
        "preset_layer_filter": [],
        "print_template": [
            "2 A4 Portrait",
            "4 A3 Portrait",
            "3 A3 Paysage",
            "6 A1 Paysage",
            "5 A2 Paysage",
            "1 A4 Paysage",
            "8 A5 Paysage",
        ],
    },
    "is_intranet": False,
    "roles": [{"id": 2, "name": "role_yverdon"}],
    "two_factor_enable": False,
}


class MapnvOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = MapnvProvider.id

    def get_mocked_response(self, email="foo@bar.ch", username="test"):
        profile_response_mock.update(
            {"email": email, "username": username,}
        )
        return MockedResponse(200, json.dumps(profile_response_mock))

    def test_login_redirects_to_social_signup(self):
        email = "foo@bar.ch"
        response = self.login(self.get_mocked_response(email))
        self.assertRedirects(response, expected_url=reverse("socialaccount_signup"))

    def test_social_signup_form_display_socialaccount_data(self):
        sociallogin_redirect = self.login(
            self.get_mocked_response("example@test.org", "Victoire"),
        )
        signup_response = self.client.get(sociallogin_redirect.url)

        self.assertContains(signup_response, "example@test.org")
        self.assertContains(signup_response, "Victoire")
