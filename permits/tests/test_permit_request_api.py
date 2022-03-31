from django.contrib.gis.geos import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
)
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from geomapshark import settings

from permits import models

from . import factories
import urllib.parse
import requests
from constance import config
from rest_framework.authtoken.models import Token


class PermitRequestAPITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.administrative_entity = factories.PermitAdministrativeEntityFactory()
        self.group = factories.SecretariatGroupFactory()
        self.administrative_entity = self.group.permitdepartment.administrative_entity

        # Users and Permissions
        self.normal_user = factories.UserFactory()
        self.secretariat_user = factories.SecretariatUserFactory(groups=[self.group])
        self.admin_user = factories.UserFactory(is_staff=True, is_superuser=True)

        # Works object Types
        self.works_object_types = factories.WorksObjectTypeFactory.create_batch(
            2, is_public=True
        )
        self.administrative_entity.works_object_types.set(self.works_object_types)

        # Create the different types of Permit Requests by different authors
        ## Normal User ##
        self.permit_request_normal_user = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=self.normal_user.permitauthor,
        )
        works_object_type_choice = factories.WorksObjectTypeChoiceFactory(
            permit_request=self.permit_request_normal_user,
            works_object_type=self.works_object_types[0],
        )
        factories.WorksObjectPropertyValueFactory(
            works_object_type_choice=works_object_type_choice
        )
        factories.PermitRequestGeoTimeFactory(
            permit_request=self.permit_request_normal_user
        )

        ## Admin User ##
        self.permit_request_admin_user = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
            author=self.admin_user.permitauthor,
        )
        works_object_type_choice = factories.WorksObjectTypeChoiceFactory(
            permit_request=self.permit_request_admin_user,
            works_object_type=self.works_object_types[0],
        )
        factories.WorksObjectPropertyValueFactory(
            works_object_type_choice=works_object_type_choice
        )
        factories.PermitRequestGeoTimeFactory(
            permit_request=self.permit_request_admin_user
        )

        ## Secretary User ##
        self.permit_request_secretary_user = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.secretariat_user.permitauthor,
        )
        works_object_type_choice = factories.WorksObjectTypeChoiceFactory(
            permit_request=self.permit_request_secretary_user,
            works_object_type=self.works_object_types[1],
        )
        factories.WorksObjectPropertyValueFactory(
            works_object_type_choice=works_object_type_choice
        )
        factories.PermitRequestGeoTimeFactory(
            permit_request=self.permit_request_secretary_user,
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

        ## For Validator User ##
        self.permit_request_validator_user = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=self.normal_user.permitauthor,
        )
        works_object_type_choice = factories.WorksObjectTypeChoiceFactory(
            permit_request=self.permit_request_validator_user,
            works_object_type=self.works_object_types[1],
        )
        factories.WorksObjectPropertyValueFactory(
            works_object_type_choice=works_object_type_choice
        )
        factories.PermitRequestGeoTimeFactory(
            permit_request=self.permit_request_validator_user,
            geom=GeometryCollection(MultiPoint(Point(0, 0), Point(1, 1))),
        )

        ## IP and NEWTORK restrictions setup
        config.IP_WHITELIST = "localhost,127.0.0.1"
        config.NETWORK_WHITELIST = "172.16.0.0/12,192.168.0.0/16"

    def test_api_normal_user(self):
        self.client.login(username=self.normal_user.username, password="password")
        response = self.client.get(reverse("permits-list"), {})
        response_json = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["detail"],
            "Vous n'avez pas la permission d'effectuer cette action.",
        )

    def test_api_admin_user(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permits-list"), {})
        response_json = response.json()
        permit_requests = models.PermitRequest.objects.all().only("id")
        permit_requests_ids = [perm.id for perm in permit_requests]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json["features"]), permit_requests.count())
        for i, perm in enumerate(permit_requests):
            self.assertIn(
                response_json["features"][i]["properties"]["permit_request_id"],
                permit_requests_ids,
            )

    def test_api_validator_user(self):
        # This permit was explicitly set for validation
        permit_request = self.permit_request_validator_user
        validation = factories.PermitRequestValidationFactory(
            permit_request=permit_request
        )
        validator_user = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )
        self.client.login(username=validator_user.username, password="password")
        response = self.client.get(reverse("permits-list"), {})
        response_json = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["detail"],
            "Vous n'avez pas la permission d'effectuer cette action.",
        )

    def test_api_secretariat_user(self):
        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.get(reverse("permits-list"), {})
        response_json = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["detail"],
            "Vous n'avez pas la permission d'effectuer cette action.",
        )

    def test_api_filtering_by_status(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("permits-list"), {"status": models.PermitRequest.STATUS_APPROVED},
        )
        response_json = response.json()
        permit_requests_all = models.PermitRequest.objects.all().only("id")
        permit_requests = permit_requests_all.filter(
            status=models.PermitRequest.STATUS_APPROVED
        ).only("id")
        permit_requests_ids = [perm.id for perm in permit_requests]
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(permit_requests.count(), permit_requests_all.count())
        self.assertEqual(len(response_json["features"]), permit_requests.count())
        self.assertLess(len(response_json["features"]), permit_requests_all.count())
        for i, perm in enumerate(permit_requests):
            self.assertIn(
                response_json["features"][i]["properties"]["permit_request_id"],
                permit_requests_ids,
            )
            self.assertEqual(
                response_json["features"][i]["properties"]["permit_request_status"],
                models.PermitRequest.STATUS_APPROVED,
            )

    def test_api_filtering_by_permit_id(self):
        self.client.login(username=self.admin_user.username, password="password")
        permit_requests_all = models.PermitRequest.objects.all().only("id")
        permit_requests_all_ids = [perm.id for perm in permit_requests_all]
        permit_requests = permit_requests_all.filter(id=permit_requests_all_ids[0])
        response = self.client.get(
            reverse("permits-list"), {"permit_request_id": permit_requests_all_ids[0]},
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response_json["features"]), permit_requests_all.count())
        self.assertLess(len(response_json["features"]), permit_requests_all.count())
        self.assertNotEqual(permit_requests.count(), permit_requests_all.count())
        self.assertEqual(permit_requests.count(), 1)
        self.assertEqual(
            response_json["features"][0]["properties"]["permit_request_id"],
            permit_requests_all_ids[0],
        )

    def test_api_filtering_by_works_object_types(self):
        self.client.login(username=self.admin_user.username, password="password")
        permit_requests_all = models.PermitRequest.objects.all()
        permit_requests = permit_requests_all.filter(
            works_object_types=self.works_object_types[1].id
        )
        permit_requests_ids = [perm.id for perm in permit_requests]
        response = self.client.get(
            reverse("permits-list"),
            {"works_object_type": self.works_object_types[1].id},
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response_json["features"]), permit_requests_all.count())
        self.assertLess(len(response_json["features"]), permit_requests_all.count())
        for i, perm in enumerate(permit_requests):
            self.assertEqual(
                response_json["features"][i]["properties"][
                    "permit_request_works_object_types"
                ],
                [self.works_object_types[1].id],
            )
            self.assertIn(
                response_json["features"][i]["properties"]["permit_request_id"],
                permit_requests_ids,
            )

    def test_api_bad_permit_id_type_parameter_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("permits-list"), {"permit_request_id": "bad_permit_id_type"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["permit_request_id"],
            ["Un nombre entier valide est requis."],
        )

    def test_api_bad_works_object_type_id_type_parameter_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("permits-list"),
            {"works_object_type": "bad_works_object_type_id_type"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["works_object_type"],
            ["Un nombre entier valide est requis."],
        )

    def test_api_bad_status_type_parameter_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("permits-list"), {"status": "bad_status_type"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["status"],
            ["«\xa0bad_status_type\xa0» n'est pas un choix valide."],
        )

    def test_api_bad_status_choice_raises_exception(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permits-list"), {"status": 25})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["status"], ["«\xa025\xa0» n'est pas un choix valide."],
        )

    def test_non_authenticated_user_raises_exception(self):
        response = self.client.get(reverse("permits-list"), {})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"], "Informations d'authentification non fournies."
        )

    def test_non_existent_permit_request_raises_exception(self):
        permit_requests = models.PermitRequest.objects.all().only("id")
        permit_requests_ids = [perm.id for perm in permit_requests]
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(
            reverse("permits-list"), {"permit_request_id": max(permit_requests_ids) + 1}
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

    def test_api_permits_point_returns_only_points(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permits_point-list"),)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("multilinestring", str(response_json).lower())
        self.assertNotIn("multipolygon", str(response_json).lower())

    def test_api_permits_line_returns_only_lines(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permits_line-list"),)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("multipoint", str(response_json).lower())
        self.assertNotIn("multipolygon", str(response_json).lower())

    def test_api_permits_poly_returns_only_polygons(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permits_poly-list"),)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("multipoint", str(response_json).lower())
        self.assertNotIn("multilinestring", str(response_json).lower())

    def test_api_permits_does_not_contain_empty_geometry(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permits-list"),)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        for feature in response_json["features"]:
            self.assertEqual(feature["geometry"]["type"], "Polygon")
            self.assertNotEqual(feature["geometry"]["coordinates"], [])

    def test_qgisserver_is_up_and_atlas_plugin_is_working(self):
        values = {
            "SERVICE": "ATLAS",
            "REQUEST": "GETCAPABILITIES",
            "MAP": "/io/data/report_template.qgs",
        }

        qgisserver_url = "http://qgisserver/ogc/?" + urllib.parse.urlencode(values)
        qgisserver_response = requests.get(
            qgisserver_url, headers={"Accept": "application/pdf"}, stream=True
        )
        self.assertEqual(qgisserver_response.status_code, 200)
        self.assertEqual(qgisserver_response.json()["status"], "success")

    def test_print_service_is_working_with_default_template(self):

        values = {
            "SERVICE": "ATLAS",
            "REQUEST": "GETPRINT",
            "FORMAT": "PDF",
            "TRANSPARENT": "true",
            "SRS": "EPSG:2056",
            "DPI": "150",
            "MAP": "/io/data/report_template.qgs",
            "TEMPLATE": "print_template",
            "LAYERS": "background,permits,permits_point,permits_line,permits_poly",
            "EXP_FILTER": "permit_request_id in(1)",
            "PERMIT_REQUEST_ID": 1,
        }

        qgisserver_url = "http://qgisserver/ogc/?" + urllib.parse.urlencode(values)
        qgisserver_response = requests.get(
            qgisserver_url, headers={"Accept": "application/pdf"}, stream=True
        )
        self.assertEqual(qgisserver_response.status_code, 200)

    def test_api_is_accessible_with_token_authentication(self):
        # Create token
        token = Token.objects.create(user=self.admin_user)
        # Set token in header
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(reverse("permits-list"), {})
        response_json = response.json()
        permit_requests = models.PermitRequest.objects.all().only("id")
        permit_requests_ids = [perm.id for perm in permit_requests]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json["features"]), permit_requests.count())
        for i, perm in enumerate(permit_requests):
            self.assertIn(
                response_json["features"][i]["properties"]["permit_request_id"],
                permit_requests_ids,
            )

    def test_api_permits_details_is_accessible_with_credentials(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permits_details-list"),)
        self.assertEqual(response.status_code, 200)

    def test_api_permits_details_is_not_accessible_with_token_authentication(self):
        # Create token
        token = Token.objects.create(user=self.admin_user)
        # Set token in header
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(reverse("permits_details-list"),)
        self.assertEqual(response.status_code, 403)

    def test_non_authorized_ip_raises_exception(self):
        # login as admin
        self.client.login(username=self.admin_user.username, password="password")
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("permits-list"), {})
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = "127.0.0.1"
        config.NETWORK_WHITELIST = ""
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("permits-list"), {}, REMOTE_ADDR="112.144.0.0"
        )
        self.assertEqual(response.status_code, 403)

    def test_authorized_ip_does_not_raise_exception(self):
        # login as admin
        self.client.login(username=self.admin_user.username, password="password")
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("permits-list"), {})
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = "112.144.0.0"
        config.NETWORK_WHITELIST = ""
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("permits-list"), {}, REMOTE_ADDR="112.144.0.0"
        )
        self.assertEqual(response.status_code, 200)

    def test_non_authorized_network_raises_exception(self):
        # login as admin
        self.client.login(username=self.admin_user.username, password="password")
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("permits-list"), {})
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = ""
        config.NETWORK_WHITELIST = "172.16.0.0/12,192.168.0.0/16"
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("permits-list"), {}, REMOTE_ADDR="112.144.0.0"
        )
        self.assertEqual(response.status_code, 403)

    def test_authorized_network_does_not_raise_exception(self):
        # login as admin
        self.client.login(username=self.admin_user.username, password="password")
        # check that login admin user is allowed to get data
        response = self.client.get(reverse("permits-list"), {})
        self.assertEqual(response.status_code, 200)
        # Set only localhost allowed in constance settings
        config.IP_WHITELIST = ""
        config.NETWORK_WHITELIST = "172.16.0.0/12,192.168.0.0/16"
        # Fake the client ip to something not allowed
        response = self.client.get(
            reverse("permits-list"), {}, REMOTE_ADDR="172.19.0.0"
        )
        self.assertEqual(response.status_code, 200)

    def test_search_api_found(self):
        self.client.login(username=self.admin_user.username, password="password")
        author_permit_request = models.PermitRequest.objects.first().author
        response = self.client.get(
            reverse("search-list"), {"search": author_permit_request}
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response_json, [])

    def test_search_api_nothing_found_for_not_logged(self):
        author_permit_request = models.PermitRequest.objects.first().author
        response = self.client.get(
            reverse("search-list"), {"search": author_permit_request}
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json, [])

    def test_search_api_nothing_found_for_not_authorized(self):
        user_wo_permit_request = factories.UserFactory()
        self.client.login(username=user_wo_permit_request.username, password="password")
        author_permit_request = models.PermitRequest.objects.first().author
        response = self.client.get(
            reverse("search-list"), {"search": author_permit_request}
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json, [])

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
        response = self.client.get(reverse("current_user-list"), {})
        response_json = response.json()
        login_datetime = models.User.objects.get(
            username=self.admin_user.username
        ).last_login
        expiration_datetime = login_datetime + timedelta(
            seconds=settings.SESSION_COOKIE_AGE
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json[0],
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
        response = self.client.get(reverse("current_user-list"), {})
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json[0], {"is_logged": False,},
        )

    # ///////////////////////////////////
    # /rest/permitauthorcreate (user creation)
    # ///////////////////////////////////

    def test_permit_author_create_not_logged_message(self):
        response = self.client.post(
            reverse("permitauthorcreate"),
            {
                "username": "user_permitauthorcreate",
                "password": "password_permitauthorcreate",
                "email": "user_permitauthorcreate@ylb.ch",
                "address": "Place pestalozzi 2",
                "zipcode": "1401",
                "city": "Yverdon-les-Bains",
                "phone_first": "024 111 22 22",
                "first_name": "",
                "last_name": "",
                "phone_second": "",
                "company_name": "",
                "vat_number": "",
                "notify_per_email": True,
            },
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_json, {"detail": "Informations d'authentification non fournies."}
        )

    def test_permit_author_create_logged_as_unauthorized_simple_user(self):
        self.client.login(username=self.normal_user.username, password="password")
        response = self.client.post(
            reverse("permitauthorcreate"),
            {
                "username": "user_permitauthorcreate",
                "password": "password_permitauthorcreate",
                "email": "user_permitauthorcreate@ylb.ch",
                "address": "Place pestalozzi 2",
                "zipcode": "1401",
                "city": "Yverdon-les-Bains",
                "phone_first": "024 111 22 22",
                "first_name": "",
                "last_name": "",
                "phone_second": "",
                "company_name": "",
                "vat_number": "",
                "notify_per_email": True,
            },
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json,
            {"detail": "Vous n'avez pas la permission d'effectuer cette action."},
        )

    def test_permit_author_create_get_is_unauthorized(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.get(reverse("permitauthorcreate"))
        response_json = response.json()
        self.assertEqual(response.status_code, 405)
        # "detail": "Méthode « GET » non autorisée."
        self.assertEqual(
            response_json, {"detail": "Méthode «\xa0GET\xa0» non autorisée."}
        )

    def test_permit_author_create_missing_mandatory_elements(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.post(
            reverse("permitauthorcreate"),
            {
                "username": "",
                "password": "",
                "email": "",
                "address": "",
                "zipcode": "",
                "city": "",
                "phone_first": "",
                "first_name": "",
                "last_name": "",
                "phone_second": "",
                "company_name": "",
                "vat_number": "",
                "notify_per_email": "",
            },
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json,
            {
                "username": ["Ce champ ne peut être vide."],
                "password": ["Ce champ ne peut être vide."],
                "email": ["Ce champ ne peut être vide."],
                "address": ["Ce champ ne peut être vide."],
                "zipcode": ["Ce champ ne peut être vide."],
                "city": ["Ce champ ne peut être vide."],
                "phone_first": ["Ce champ ne peut être vide."],
            },
        )

    def test_permit_author_create_duplicate_email_and_username(self):
        self.client.login(username=self.admin_user.username, password="password")
        user = models.User.objects.first()
        response = self.client.post(
            reverse("permitauthorcreate"),
            {
                "username": user.username,
                "password": "password_permitauthorcreate",
                "email": user.email,
                "address": "Place pestalozzi 2",
                "zipcode": "1401",
                "city": "Yverdon-les-Bains",
                "phone_first": "024 111 22 22",
                "first_name": "",
                "last_name": "",
                "phone_second": "",
                "company_name": "",
                "vat_number": "",
                "notify_per_email": True,
            },
        )
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_json,
            {
                "Email": "This email already exists",
                "Username": "This username already exists",
            },
        )

    def test_permit_author_create_create_user_in_db(self):
        self.client.login(username=self.admin_user.username, password="password")
        response = self.client.post(
            reverse("permitauthorcreate"),
            {
                "username": "user_permitauthorcreate",
                "password": "password_permitauthorcreate",
                "email": "user_permitauthorcreate@ylb.ch",
                "address": "Place pestalozzi 2",
                "zipcode": "1401",
                "city": "Yverdon-les-Bains",
                "phone_first": "024 111 22 22",
                "first_name": "",
                "last_name": "",
                "phone_second": "",
                "company_name": "",
                "vat_number": "",
                "notify_per_email": True,
            },
        )
        response_json = response.json()
        user = models.User.objects.get(username="user_permitauthorcreate")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user)
        self.assertEqual(
            response_json,
            {
                "user": {
                    "id": user.id,
                    "username": "user_permitauthorcreate",
                    "password": user.password,
                    "first_name": "",
                    "last_name": "",
                    "email": "user_permitauthorcreate@ylb.ch",
                }
            },
        )

    # TODO: test also the permits:permit_request_print route
