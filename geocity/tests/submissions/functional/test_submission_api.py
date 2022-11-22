from datetime import datetime, timedelta

from constance import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    Point,
)
from django.test import TestCase
from knox.models import AuthToken
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories

User = get_user_model()


class SubmissionAPITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.administrative_entity = factories.AdministrativeEntityFactory()
        self.group = factories.SecretariatGroupFactory()
        self.administrative_entity = self.group.permit_department.administrative_entity

        # Users and Permissions
        self.normal_user = factories.UserFactory()

        self.secretariat_user = factories.SecretariatUserFactory(groups=[self.group])
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.secretariat_group.user_set.add(self.secretariat_user)

        self.admin_user = factories.UserFactory(is_staff=True, is_superuser=True)
        self.admin_group = factories.IntegratorGroupFactory()
        self.admin_group.user_set.add(self.admin_user)

        # Works object Types
        self.forms = factories.FormFactory.create_batch(2, is_public=True)
        self.administrative_entity.forms.set(self.forms)

        # Create the different types of Permit Requests by different authors
        ## Normal User ##
        self.submission_normal_user = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission_normal_user,
            form=self.forms[0],
        )
        factories.FieldValueFactory(selected_form=selected_form)
        factories.SubmissionGeoTimeFactory(submission=self.submission_normal_user)

        ## Admin User ##
        self.submission_admin_user = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
            author=self.admin_user,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission_admin_user,
            form=self.forms[0],
        )
        factories.FieldValueFactory(selected_form=selected_form)
        factories.SubmissionGeoTimeFactory(submission=self.submission_admin_user)

        ## Secretary User ##
        self.submission_secretary_user = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.secretariat_user,
            is_public=True,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission_secretary_user,
            form=self.forms[1],
        )
        factories.FieldValueFactory(selected_form=selected_form)
        self.form_geotime_secretary_user = factories.SubmissionGeoTimeFactory(
            submission=self.submission_secretary_user,
            geom=GeometryCollection(
                MultiLineString(
                    LineString(
                        (2539096.09997796, 1181119.41274907),
                        (2539094.37477054, 1181134.07701214),
                    ),
                    LineString(
                        (2539196.09997796, 1181219.41274907),
                        (2539294.37477054, 1181134.07701214),
                    ),
                )
            ),
        )
        start_date = datetime.today()
        end_date = start_date + timedelta(days=10)
        factories.SubmissionInquiryFactory(
            submission=self.submission_secretary_user,
            start_date=start_date,
            end_date=end_date,
        )

        ## For Validator User ##
        self.submission_validator_user = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission_validator_user,
            form=self.forms[1],
        )
        factories.FieldValueFactory(selected_form=selected_form)
        factories.SubmissionGeoTimeFactory(
            submission=self.submission_validator_user,
            geom=GeometryCollection(MultiPoint(Point(0, 0), Point(1, 1))),
        )

        ## IP and NEWTORK restrictions setup
        config.IP_WHITELIST = "localhost,127.0.0.1"
        config.NETWORK_WHITELIST = "172.16.0.0/12,192.168.0.0/16"

    def test_api_normal_user(self):
        self.client.login(username=self.normal_user.username, password="password")
        response = self.client.get(reverse("submissions-list"), {})
        response_json = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["detail"],
            "Vous n'avez pas la permission d'effectuer cette action.",
        )

    def test_logout_next_action_if_redirect_uri_not_whitelisted(self):
        config.LOGOUT_REDIRECT_HOSTNAME_WHITELIST = ""
        self.client.login(username=self.admin_user.username, password="password")
        redirect_uri = "http://testserver" + reverse("accounts:user_profile_create")
        logout_page = reverse("logout") + "?next=" + redirect_uri
        response = self.client.post(logout_page)
        self.assertRedirects(response, expected_url=reverse("accounts:account_login"))

    def test_logout_next_action_if_redirect_uri_is_whitelisted(self):
        config.LOGOUT_REDIRECT_HOSTNAME_WHITELIST = "testserver"
        self.client.login(username=self.admin_user.username, password="password")
        redirect_uri = "http://testserver" + reverse("accounts:user_profile_create")
        logout_page = reverse("logout") + "?next=" + redirect_uri
        response = self.client.post(logout_page)
        self.assertRedirects(response, expected_url=redirect_uri)

    def test_api_admin_user(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("submissions-list"), {})
        response_json = response.json()
        submissions = submissions_models.Submission.objects.all().only("id")
        submissions_ids = [submission.id for submission in submissions]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json["features"]), submissions.count())
        for i, perm in enumerate(submissions):
            self.assertIn(
                response_json["features"][i]["properties"]["submission_id"],
                submissions_ids,
            )

    def test_api_validator_user(self):
        # This permit was explicitly set for validation
        submission = self.submission_validator_user
        validation = factories.SubmissionValidationFactory(submission=submission)
        validator_user = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )
        self.client.login(username=validator_user.username, password="password")
        response = self.client.get(reverse("submissions-list"), {})
        self.assertEqual(response.status_code, 200)

    def test_api_secretariat_user(self):
        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.get(reverse("submissions-list"), {})
        response_json = response.json()
        submissions = submissions_models.Submission.objects.all().only("id")
        submissions_ids = [submission.id for submission in submissions]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json["features"]), submissions.count())
        for i, perm in enumerate(submissions):
            self.assertIn(
                response_json["features"][i]["properties"]["submission_id"],
                submissions_ids,
            )

    def test_api_filtering_by_status(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions-list"),
            {"status": submissions_models.Submission.STATUS_APPROVED},
        )
        response_json = response.json()
        submissions_all = submissions_models.Submission.objects.all().only("id")
        submissions = submissions_all.filter(
            status=submissions_models.Submission.STATUS_APPROVED
        ).only("id")
        submissions_ids = [submission.id for submission in submissions]
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(submissions.count(), submissions_all.count())
        self.assertEqual(len(response_json["features"]), submissions.count())
        self.assertLess(len(response_json["features"]), submissions_all.count())
        for i, perm in enumerate(submissions):
            self.assertIn(
                response_json["features"][i]["properties"]["submission_id"],
                submissions_ids,
            )
            self.assertEqual(
                response_json["features"][i]["properties"]["submission_status"],
                submissions_models.Submission.STATUS_APPROVED,
            )

    def test_api_filtering_by_permit_id(self):
        self.client.login(username=self.admin_user.username, password="password")
        submissions_all = submissions_models.Submission.objects.all().only("id")
        submissions_all_ids = [perm.id for perm in submissions_all]
        submissions = submissions_all.filter(id=submissions_all_ids[0])
        response = self.client.get(
            reverse("submissions-list"),
            {"submission_id": submissions_all_ids[0]},
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response_json["features"]), submissions_all.count())
        self.assertLess(len(response_json["features"]), submissions_all.count())
        self.assertNotEqual(submissions.count(), submissions_all.count())
        self.assertEqual(submissions.count(), 1)
        self.assertEqual(
            response_json["features"][0]["properties"]["submission_id"],
            submissions_all_ids[0],
        )

    def test_api_filtering_by_forms(self):
        self.client.login(username=self.admin_user.username, password="password")
        submissions_all = submissions_models.Submission.objects.all()
        submissions = submissions_all.filter(forms=self.forms[1].id)
        submissions_ids = [submission.id for submission in submissions]
        response = self.client.get(
            reverse("submissions-list"),
            {"form": self.forms[1].id},
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response_json["features"]), submissions_all.count())
        self.assertLess(len(response_json["features"]), submissions_all.count())
        for i, perm in enumerate(submissions):
            self.assertEqual(
                response_json["features"][i]["properties"]["submission_forms"],
                [self.forms[1].id],
            )
            self.assertIn(
                response_json["features"][i]["properties"]["submission_id"],
                submissions_ids,
            )

    def test_api_bad_permit_id_type_parameter_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions-list"), {"submission_id": "bad_submission_id_type"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["submission_id"],
            ["Un nombre entier valide est requis."],
        )

    def test_api_bad_form_id_type_parameter_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions-list"),
            {"form": "bad_form_id_type"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["form"],
            ["Un nombre entier valide est requis."],
        )

    def test_api_bad_status_type_parameter_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions-list"), {"status": "bad_status_type"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["status"],
            ["«\xa0bad_status_type\xa0» n'est pas un choix valide."],
        )

    def test_api_bad_status_choice_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("submissions-list"), {"status": 25})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["status"],
            ["«\xa025\xa0» n'est pas un choix valide."],
        )

    def test_non_authenticated_user_raises_exception(self):
        response = self.client.get(reverse("submissions-list"), {})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"], "Informations d'authentification non fournies."
        )

    def test_non_existent_form_raises_exception(self):
        submissions = submissions_models.Submission.objects.all().only("id")
        submissions_ids = [submission.id for submission in submissions]
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions-list"), {"submission_id": max(submissions_ids) + 1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "type": "FeatureCollection",
                "crs": {
                    "type": "name",
                    "properties": {"name": "urn:ogc:def:crs:EPSG::2056"},
                },
                "features": [],
            },
        )

    def test_api_submissions_point_returns_only_points(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions_point-list"),
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("multilinestring", str(response_json).lower())
        self.assertNotIn("multipolygon", str(response_json).lower())

    def test_api_submissions_line_returns_only_lines(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions_line-list"),
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("multipoint", str(response_json).lower())
        self.assertNotIn("multipolygon", str(response_json).lower())

    def test_api_submissions_poly_returns_only_polygons(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions_poly-list"),
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("multipoint", str(response_json).lower())
        self.assertNotIn("multilinestring", str(response_json).lower())

    def test_api_submissions_does_not_contain_empty_geometry(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions-list"),
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        for feature in response_json["features"]:
            self.assertEqual(feature["geometry"]["type"], "Polygon")
            self.assertNotEqual(feature["geometry"]["coordinates"], [])

    def test_api_is_accessible_with_token_authentication(self):
        # Create token
        auth_token, token = AuthToken.objects.create(user=self.admin_user)
        # Set token in header
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(reverse("submissions-list"), {})
        response_json = response.json()
        submissions = submissions_models.Submission.objects.all().only("id")
        submissions_ids = [submission.id for submission in submissions]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json["features"]), submissions.count())
        for i, perm in enumerate(submissions):
            self.assertIn(
                response_json["features"][i]["properties"]["submission_id"],
                submissions_ids,
            )

    def test_api_submissions_details_is_accessible_with_credentials(self):
        # Need Submission to create absolut_url in api for file type
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("submissions_details-list"),
        )
        self.assertEqual(response.status_code, 200)

    def test_non_authorized_ip_raises_exception_with_tokenauth(self):
        # login as admin with token
        authtoken, token = AuthToken.objects.create(user=self.admin_user)
        META = {"HTTP_AUTHORIZATION": f"Token {token}"}
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("submissions-list"), {}, **META)
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = "127.0.0.1"
        config.NETWORK_WHITELIST = ""
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("submissions-list"), {}, REMOTE_ADDR="112.144.0.0", **META
        )
        self.assertEqual(response.status_code, 401)

    def test_authorized_ip_does_not_raise_exception_with_tokenauth(self):
        # login as admin with token
        authtoken, token = AuthToken.objects.create(user=self.admin_user)
        META = {"HTTP_AUTHORIZATION": f"Token {token}"}
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("submissions-list"), {}, **META)
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = "112.144.0.0"
        config.NETWORK_WHITELIST = ""
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("submissions-list"), {}, REMOTE_ADDR="112.144.0.0", **META
        )
        self.assertEqual(response.status_code, 200)

    def test_non_authorized_network_raises_exception_with_tokenauth(self):
        # login as admin with token
        authtoken, token = AuthToken.objects.create(user=self.admin_user)
        META = {"HTTP_AUTHORIZATION": f"Token {token}"}
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("submissions-list"), {}, **META)
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = ""
        config.NETWORK_WHITELIST = "172.16.0.0/12,192.168.0.0/16"
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("submissions-list"), {}, REMOTE_ADDR="112.144.0.0", **META
        )
        self.assertEqual(response.status_code, 401)

    def test_authorized_network_does_not_raise_exception_with_tokenauth(self):
        # login as admin with token
        authtoken, token = AuthToken.objects.create(user=self.admin_user)
        META = {"HTTP_AUTHORIZATION": f"Token {token}"}
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("submissions-list"), {}, **META)
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = ""
        config.NETWORK_WHITELIST = "172.16.0.0/12,192.168.0.0/16"
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("submissions-list"), {}, REMOTE_ADDR="172.19.0.0", **META
        )
        self.assertEqual(response.status_code, 200)

    def test_search_api_found(self):
        self.client.login(username=self.admin_user.username, password="password")
        author = submissions_models.Submission.objects.first().author.get_full_name()
        response = self.client.get(reverse("search-list"), {"search": author})
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response_json, [])

    def test_search_api_nothing_found_for_not_logged(self):
        author = submissions_models.Submission.objects.first().author.get_full_name()
        response = self.client.get(reverse("search-list"), {"search": author})
        response_json = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json, {"detail": "Informations d'authentification non fournies."}
        )

    def test_search_api_nothing_found_for_not_authorized(self):
        user_wo_form = factories.UserFactory()
        self.client.login(username=user_wo_form.username, password="password")
        author_form = submissions_models.Submission.objects.first().author
        response = self.client.get(reverse("search-list"), {"search": author_form})
        response_json = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json,
            {"detail": "Vous n'avez pas la permission d'effectuer cette action."},
        )

    def test_search_api_nothing_found_for_wrong_string(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("search-list"), {"search": "InexistantStringReturningNoResult"}
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json, [])

    def test_current_user_returns_user_informations(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("current_user"), {})
        response_json = response.json()
        login_datetime = User.objects.get(username=self.admin_user.username).last_login
        expiration_datetime = login_datetime + timedelta(
            seconds=settings.SESSION_COOKIE_AGE
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "is_logged": True,
                "username": self.admin_user.username,
                "email": self.admin_user.email,
                "login_datetime": login_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "expiration_datetime": expiration_datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            },
        )

    def test_not_logged_returns_nothing_on_current_user(self):
        response = self.client.get(reverse("current_user"), {})
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "is_logged": False,
            },
        )

    def test_events_api_returns_current_inquiries(self):
        self.client.login(username=self.secretariat_user.username, password="password")

        response = self.client.get(
            reverse(
                "events-detail",
                kwargs={"pk": self.form_geotime_secretary_user.pk},
            )
        )
        request = response.json()["properties"]["submission"]
        self.assertIn("current_inquiry", request)
        self.assertEqual(
            self.submission_secretary_user.current_inquiry.pk,
            request["current_inquiry"]["id"],
        )

    def test_events_api_returns_current_inquiries_for_anonymous_user(self):

        response = self.client.get(
            reverse(
                "events-detail",
                kwargs={"pk": self.form_geotime_secretary_user.pk},
            )
        )
        request = response.json()["properties"]["submission"]
        self.assertIn("current_inquiry", request)
        self.assertEqual(
            self.submission_secretary_user.current_inquiry.pk,
            request["current_inquiry"]["id"],
        )
