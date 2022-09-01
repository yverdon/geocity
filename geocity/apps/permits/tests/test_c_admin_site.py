from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django_otp import DEVICE_ID_SESSION_KEY
from permits import admin, models
from permits.tests.factories import SecretariatUserFactory, UserFactory
from two_factor.utils import default_device

from . import factories
from .utils import LoggedInIntegratorMixin, get_parser

# TODO: Write update/delete/create tests for [PermitAdministrativeEntity, WorksType, WorksObject, WorksObjectType, WorksObjectProperty, PermitActorType, PermitActorType, PermitRequestAmendProperty]

# "$ ./manage.py show_urls" to show admin routes
class IntegratorAdminSiteTestCase(LoggedInIntegratorMixin, TestCase):
    def enable_otp_session(self, user=None):
        user.totpdevice_set.create(name="default")
        assert self.client.login(username=user.username, password="password")
        if default_device(user):
            session = self.client.session
            session[DEVICE_ID_SESSION_KEY] = default_device(user).persistent_id
            session.save()

    def setUp(self):
        super().setUp()
        self.administrative_entity = (
            factories.PermitAdministrativeEntityFactory.create_batch(3)
        )
        self.integrator_administrative_entity = (
            factories.PermitAdministrativeEntityFactory(integrator=self.group)
        )

        self.parent_type = factories.ParentComplementaryDocumentTypeFactory()
        self.integrator_parent_type = factories.ParentComplementaryDocumentTypeFactory(
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

        self.permit_request_amend_property = (
            factories.PermitRequestAmendPropertyFactory.create_batch(3)
        )
        self.integrator_permit_request_amend_property = (
            factories.PermitRequestAmendPropertyFactory(integrator=self.group)
        )

        if settings.ENABLE_2FA:
            self.enable_otp_session(user=self.user)
            self.group2fa = factories.GroupFactory()
            factories.PermitDepartmentFactory(group=self.group2fa, mandatory_2fa=True)

    def test_integrator_cannot_see_user_if_no_integrator_email_domains_is_configured_by_admin(
        self,
    ):
        user = User.objects.create_user(
            email=f"yverdon-squad+admin@notalloweddomain.ch",
            first_name="nonadminuser",
            last_name="user",
            username="standard",
            password="demo",
            is_staff=False,
            is_superuser=False,
        )
        response = self.client.get(reverse("admin:auth_user_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select("tbody")), 0)

    def test_integrator_can_see_user_if_integrator_email_domains_is_configured_by_admin(
        self,
    ):
        self.group.permitdepartment.integrator_email_domains = "notalloweddomain.ch"
        self.group.permitdepartment.save()
        user = User.objects.create_user(
            email=f"yverdon-squad+admin@notalloweddomain.ch",
            first_name="nonadminuser",
            last_name="user",
            username="standard",
            password="demo",
            is_staff=False,
            is_superuser=False,
        )
        response = self.client.get(reverse("admin:auth_user_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select("tbody")), 1)

    def test_integrator_cannot_see_user_if_no_integrator_emails_exceptions_is_configured_by_admin(
        self,
    ):
        user = User.objects.create_user(
            email=f"dummyuser@notalloweddomain.ch",
            first_name="nonadminuser",
            last_name="user",
            username="standard",
            password="demo",
            is_staff=False,
            is_superuser=False,
        )
        response = self.client.get(reverse("admin:auth_user_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select("tbody")), 0)

    def test_integrator_can_see_user_if_integrator_emails_exceptions_is_configured_by_admin(
        self,
    ):
        self.group.permitdepartment.integrator_emails_exceptions = (
            "dummyuser@notalloweddomain.ch"
        )
        self.group.permitdepartment.save()
        user = User.objects.create_user(
            email=f"dummyuser@notalloweddomain.ch",
            first_name="nonadminuser",
            last_name="user",
            username="standard",
            password="demo",
            is_staff=False,
            is_superuser=False,
        )
        response = self.client.get(reverse("admin:auth_user_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select("tbody")), 1)

    def test_integrator_can_only_see_own_permitadministrativeentity(self):
        response = self.client.get(
            reverse("admin:permits_permitadministrativeentity_changelist")
        )
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_permitadministrativeentity(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(
            reverse("admin:permits_permitadministrativeentity_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(parser.select(".field-sortable_str")), 2)

    def test_integrator_can_only_see_own_workstype(self):
        response = self.client.get(reverse("admin:permits_workstype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_workstype(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:permits_workstype_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".field-sortable_str")),
            models.WorksType.objects.all().count(),
        )

    def test_integrator_can_only_see_own_worksobject(self):
        response = self.client.get(reverse("admin:permits_worksobject_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_worksobject(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:permits_worksobject_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".field-sortable_str")),
            models.WorksObject.objects.all().count(),
        )

    def test_integrator_can_only_see_own_worksobjecttype(self):
        response = self.client.get(reverse("admin:permits_worksobjecttype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_worksobjecttype(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:permits_worksobjecttype_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".field-sortable_str")),
            models.WorksObjectType.objects.all().count(),
        )

    def test_integrator_can_only_see_own_worksobjectproperty(self):
        response = self.client.get(
            reverse("admin:permits_worksobjectproperty_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_worksobjectproperty(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(
            reverse("admin:permits_worksobjectproperty_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 4)

    def test_integrator_can_only_see_own_permitactortype(self):
        response = self.client.get(reverse("admin:permits_permitactortype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 2)

    def test_admin_can_see_all_permitactortype(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:permits_permitactortype_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 8)

    def test_integrator_can_only_see_own_permitrequestamendproperty(self):
        response = self.client.get(
            reverse("admin:permits_permitrequestamendproperty_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".grp-row")), 3)

    def test_integrator_can_only_see_own_complementarydocumenttype(self):
        response = self.client.get(
            reverse("admin:permits_complementarydocumenttype_changelist")
        )
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".grp-row-even")), 1)

    def test_admin_can_see_all_permitrequestamendproperty(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

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
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

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
            reverse(
                "admin:auth_group_change",
                kwargs={"object_id": group.id},
            ),
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
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        integrator_group = factories.IntegratorGroupFactory()

        data = {
            "username": self.user.username,
            "groups": [self.group.id, integrator_group.id],
        }

        response = self.client.post(
            reverse(
                "admin:auth_user_change",
                kwargs={"object_id": self.user.id},
            ),
            data=data,
        )
        content = response.content.decode()

        expected = "<li>{error_msg}</li>".format(
            error_msg=admin.MULTIPLE_INTEGRATOR_ERROR_MESSAGE,
        )
        self.assertInHTML(expected, content)

    def test_admin_can_see_all_permit_requests(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:permits_permitrequest_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3.1 Consultation des demandes")

    def test_integrator_cannot_see_permit_requests(self):
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=self.user)
        response = self.client.get(reverse("admin:permits_permitrequest_changelist"))
        self.assertEqual(response.status_code, 403)

    if settings.ENABLE_2FA:

        def test_user_of_group_with_mandatory_2FA_is_asked_to_set_it_up(self):
            user = SecretariatUserFactory()
            user.groups.set([self.group2fa])
            self.client.login(username=user.username, password="password")

            response = self.client.get(
                reverse(settings.LOGIN_REDIRECT_URL),
                follow=True,
            )

            self.assertEqual(response.status_code, 200)
            self.assertRedirects(
                response, "/account/two_factor/?next=/permit-requests/"
            )
            self.assertContains(response, "Activer l'authentification à deux facteurs")

        def test_user_of_group_with_mandatory_2FA_setup_can_see_permits_list(self):
            user = UserFactory()
            user.groups.set([self.group2fa])
            self.enable_otp_session(user)
            response = self.client.get(
                reverse(settings.LOGIN_REDIRECT_URL),
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Vue d'ensemble de vos demandes")

        def test_user_of_group_with_mandatory_2FA_not_setup_can_access_change_password(
            self,
        ):
            user = UserFactory()
            user.groups.set([self.group2fa])
            self.client.login(username=user.username, password="password")
            response = self.client.get(
                reverse("password_change"),
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Confirmation du nouveau mot de passe")

        def test_user_of_group_with_mandatory_2FA_not_setup_can_access_modify_account(
            self,
        ):
            user = UserFactory()
            group = factories.GroupFactory()
            factories.PermitDepartmentFactory(group=group, mandatory_2fa=True)
            user.groups.set([self.group2fa])
            self.client.login(username=user.username, password="password")
            response = self.client.get(
                reverse("permit_author_edit"),
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Mon compte")

        def test_user_of_group_with_mandatory_2FA_not_setup_can_access_account_security(
            self,
        ):
            user = UserFactory()
            group = factories.GroupFactory()
            factories.PermitDepartmentFactory(group=group, mandatory_2fa=True)
            user.groups.set([self.group2fa])
            self.client.login(username=user.username, password="password")
            response = self.client.get(
                reverse("profile"),
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Sécurité du compte")
