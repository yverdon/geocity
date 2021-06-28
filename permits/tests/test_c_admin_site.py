import re
import urllib.parse
import uuid
from datetime import date
from permits import admin

from django.conf import settings
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from . import factories
from .utils import LoggedInIntegratorMixin, get_parser

# TODO: Write update/delete/create tests for [PermitAdministrativeEntity, WorksType, WorksObject, WorksObjectType, WorksObjectProperty, PermitActorType, PermitActorType, PermitRequestAmendProperty]

# "$ ./manage.py show_urls" to show admin routes
class IntegratorAdminSiteTestCase(LoggedInIntegratorMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.administrative_entity = factories.PermitAdministrativeEntityFactory.create_batch(
            3
        )
        self.integrator_administrative_entity = factories.PermitAdministrativeEntityFactory(
            integrator=self.group
        )

        self.works_type = factories.WorksTypeFactory.create_batch(3)
        self.integrator_works_type = factories.WorksTypeFactory(integrator=self.group)

        self.works_object = factories.WorksObjectFactory.create_batch(3)
        self.integrator_works_object = factories.WorksObjectFactory(
            integrator=self.group
        )

        self.works_object_type = factories.WorksObjectTypeFactory.create_batch(3)
        self.integrator_works_object_type = factories.WorksObjectTypeFactory(
            integrator=self.group
        )

        self.works_object_property = factories.WorksObjectPropertyFactory.create_batch(
            3
        )
        self.integrator_works_object_property = factories.WorksObjectPropertyFactory(
            integrator=self.group
        )

        self.permit_actor_type = factories.PermitActorTypeFactory.create_batch(3)
        self.integrator_permit_actor_type = factories.PermitActorTypeFactory(
            integrator=self.group
        )

        self.permit_actor_type = factories.PermitActorTypeFactory.create_batch(3)
        self.integrator_permit_actor_type = factories.PermitActorTypeFactory(
            integrator=self.group
        )

        self.permit_request_amend_property = factories.PermitRequestAmendPropertyFactory.create_batch(
            3
        )
        self.integrator_permit_request_amend_property = factories.PermitRequestAmendPropertyFactory(
            integrator=self.group
        )

    def test_integrator_can_only_see_own_permitadministrativeentity(self):
        response = self.client.get(
            reverse("admin:permits_permitadministrativeentity_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 1)

    def test_admin_can_see_all_permitadministrativeentity(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        response = self.client.get(
            reverse("admin:permits_permitadministrativeentity_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 5)

    def test_integrator_can_only_see_own_workstype(self):
        response = self.client.get(reverse("admin:permits_workstype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 1)

    def test_admin_can_see_all_workstype(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        response = self.client.get(reverse("admin:permits_workstype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 16)

    def test_integrator_can_only_see_own_worksobject(self):
        response = self.client.get(reverse("admin:permits_worksobject_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 1)

    def test_admin_can_see_all_worksobject(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        response = self.client.get(reverse("admin:permits_worksobject_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 8)

    def test_integrator_can_only_see_own_worksobjecttype(self):
        response = self.client.get(reverse("admin:permits_worksobjecttype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 1)

    def test_admin_can_see_all_worksobjecttype(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        response = self.client.get(reverse("admin:permits_worksobjecttype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 4)

    def test_integrator_can_only_see_own_worksobjectproperty(self):
        response = self.client.get(
            reverse("admin:permits_worksobjectproperty_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 1)

    def test_admin_can_see_all_worksobjectproperty(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        response = self.client.get(
            reverse("admin:permits_worksobjectproperty_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 4)

    def test_integrator_can_only_see_own_permitactortype(self):
        response = self.client.get(reverse("admin:permits_permitactortype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 2)

    def test_admin_can_see_all_permitactortype(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        response = self.client.get(reverse("admin:permits_permitactortype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-__str__")), 8)

    def test_integrator_can_only_see_own_permitrequestamendproperty(self):
        response = self.client.get(
            reverse("admin:permits_permitrequestamendproperty_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".grp-row")), 3)

    def test_admin_can_see_all_permitrequestamendproperty(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        response = self.client.get(
            reverse("admin:permits_permitrequestamendproperty_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".grp-row")), 6)

    # An user can only have 1 integrator group, updating a group shouldn't bypass this rule
    def test_cannot_change_a_group_as_integrator_if_an_user_of_this_group_has_already_an_integrator_group(
        self,
    ):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        group = factories.SecretariatGroupFactory()
        factories.IntegratorUserFactory(groups=[self.group, group])

        data = {
            "name": group.name,
            "permissions": 1,
            "permitdepartment-TOTAL_FORMS": 1,
            "permitdepartment-INITIAL_FORMS": 1,
            "permitdepartment-MIN_NUM_FORMS": 1,
            "permitdepartment-MAX_NUM_FORMS": 1,
            "permitdepartment-0-is_integrator_admin": True,
            "permitdepartment-0-group": group.id,
        }

        response = self.client.post(
            reverse("admin:auth_group_change", kwargs={"object_id": group.id},),
            data=data,
        )
        content = response.content.decode()

        expected = "{error_msg}".format(
            error_msg=admin.MULTIPLE_INTEGRATOR_ERROR_MESSAGE,
        )
        self.assertInHTML(expected, content)

    # A user can only have 1 integrator group, updating a group shouldn't bypass this rule
    def test_cannot_add_a_new_integrator_group_to_an_user_who_has_already_an_integrator_group(
        self,
    ):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")

        integrator_group = factories.IntegratorGroupFactory()

        data = {
            "username": self.user.username,
            "groups": [self.group.id, integrator_group.id],
        }

        response = self.client.post(
            reverse("admin:auth_user_change", kwargs={"object_id": self.user.id},),
            data=data,
        )
        content = response.content.decode()

        expected = "<li>{error_msg}</li>".format(
            error_msg=admin.MULTIPLE_INTEGRATOR_ERROR_MESSAGE,
        )
        self.assertInHTML(expected, content)
