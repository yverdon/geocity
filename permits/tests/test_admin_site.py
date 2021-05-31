import re
import urllib.parse
import uuid
from datetime import date

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from permits import models, services

from . import factories
from .utils import LoggedInIntegratorMixin, get_parser

# TODO: Write update/delete/create tests for admin page

# "$ ./manage.py show_urls" to show admin routes
class AdminSiteTestCase(LoggedInIntegratorMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.administrative_entity = factories.PermitAdministrativeEntityFactory.create_batch(3)

    def test_integrator_can_only_see_own_permitadministrativeentity(self):
        group = factories.IntegratorGroupFactory()
        integrator = factories.IntegratorUserFactory(groups=[group])

        self.client.login(username=integrator.username, password="password")
        
        response = self.client.get(reverse("admin:permits_permitadministrativeentity_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select("th")), 1)

    def test_admin_can_see_all_permitadministrativeentity(self):
        user = factories.SuperUserFactory()

        self.client.login(username=user.username, password="password")
        
        response = self.client.get(reverse("admin:permits_permitadministrativeentity_changelist"))
        parser = get_parser(response.content)

        print(parser)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select("th .field-__str__")), 3)




    def test_integrator_can_only_see_own_workstype(self):
        self.assertEqual(True, False)

    def test_admin_can_see_all_workstype(self):
        self.assertEqual(True, False)




    def test_integrator_can_only_see_own_worksobject(self):
        self.assertEqual(True, False)

    def test_admin_can_see_all_worksobject(self):
        self.assertEqual(True, False)




    def test_integrator_can_only_see_own_worksobjecttype(self):
        self.assertEqual(True, False)

    def test_admin_can_see_all_worksobjecttype(self):
        self.assertEqual(True, False)





    def test_integrator_can_only_see_own_worksobjectproperty(self):
        self.assertEqual(True, False)

    def test_admin_can_see_all_worksobjectproperty(self):
        self.assertEqual(True, False)





    def test_integrator_can_only_see_own_permitactortype(self):
        self.assertEqual(True, False)

    def test_admin_can_see_all_permitactortype(self):
        self.assertEqual(True, False)





    def test_integrator_can_only_see_own_permitrequestamendproperty(self):
        self.assertEqual(True, False)

    def test_admin_can_see_all_permitrequestamendproperty(self):
        self.assertEqual(True, False)

    

    # An user can only have 1 integrator group, updating a group shouldn't bypass this rule
    def test_cannot_change_a_group_as_integrator_if_an_user_of_this_group_has_already_an_integrator_group(self):
        self.assertEqual(True, False)

    # An user can only have 1 integrator group, updating a group shouldn't bypass this rule
    def test_cannot_add_a_new_integrator_group_to_an_user_who_has_already_an_integrator_group(self):
        self.assertEqual(True, False)