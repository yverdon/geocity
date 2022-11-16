from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django_otp import DEVICE_ID_SESSION_KEY
from two_factor.utils import default_device

from geocity.apps.accounts.admin import MULTIPLE_INTEGRATOR_ERROR_MESSAGE
from geocity.apps.submissions import models
from geocity.tests import factories
from geocity.tests.utils import LoggedInIntegratorMixin, get_parser

# TODO: Write update/delete/create tests for [AdministrativeEntity, FormCategory, Form, Form, Field, ContactType, ContactType, SubmissionAmendField]

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
        self.administrative_entity = factories.AdministrativeEntityFactory.create_batch(
            3
        )
        self.integrator_administrative_entity = factories.AdministrativeEntityFactory(
            integrator=self.group
        )

        self.parent_type = factories.ParentComplementaryDocumentTypeFactory()
        self.integrator_parent_type = factories.ParentComplementaryDocumentTypeFactory(
            integrator=self.group
        )

        self.category = factories.FormCategoryFactory.create_batch(3)
        self.integrator_category = factories.FormCategoryFactory(integrator=self.group)

        self.forms = factories.FormFactory.create_batch(3)
        self.integrator_form = factories.FormFactory(integrator=self.group)

        self.fields = factories.FieldFactory.create_batch(3)
        self.integrator_field = factories.FieldFactory(integrator=self.group)

        self.contact_type = factories.ContactTypeFactory.create_batch(3)
        self.integrator_contact_type = factories.ContactTypeFactory(
            integrator=self.group
        )

        self.contact_type = factories.ContactTypeFactory.create_batch(3)
        self.integrator_contact_type = factories.ContactTypeFactory(
            integrator=self.group
        )

        self.submission_amend_field = (
            factories.SubmissionAmendFieldFactory.create_batch(3)
        )
        self.integrator_submission_amend_field = factories.SubmissionAmendFieldFactory(
            integrator=self.group
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
        self.group.permit_department.integrator_email_domains = "notalloweddomain.ch"
        self.group.permit_department.save()
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
        self.group.permit_department.integrator_emails_exceptions = (
            "dummyuser@notalloweddomain.ch"
        )
        self.group.permit_department.save()
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

    def test_integrator_can_only_see_own_administrativeentity(self):
        response = self.client.get(
            reverse("admin:forms_administrativeentityforadminsite_changelist")
        )
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_administrativeentity(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(
            reverse("admin:forms_administrativeentityforadminsite_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(parser.select(".field-sortable_str")), 2)

    def test_integrator_can_only_see_own_categories(self):
        response = self.client.get(reverse("admin:forms_formcategory_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_formcategory(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:forms_formcategory_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".field-sortable_str")),
            models.FormCategory.objects.all().count(),
        )

    def test_integrator_can_only_see_own_form(self):
        response = self.client.get(reverse("admin:forms_form_changelist"))
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 1)

    def test_admin_can_see_all_form(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:forms_form_changelist"))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".field-sortable_str")),
            models.Form.objects.all().count(),
        )

    def test_integrator_can_only_see_own_field(self):
        self.integrator_form.fields.add(self.integrator_field)
        response = self.client.get(
            reverse(
                "admin:forms_form_change", kwargs={"object_id": self.integrator_form.pk}
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        # 2 fields = 1 integrator field + empty choice
        self.assertEqual(
            len(parser.select(".grp-td.field")[0].select("select option")), 2
        )

    def test_admin_can_see_all_field(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(
            reverse(
                "admin:forms_form_change", kwargs={"object_id": self.integrator_form.pk}
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            # 5 fields = 4 fields + empty choice
            len(parser.select(".grp-td.field")[0].select("select option")),
            5,
        )

    def test_integrator_can_only_see_own_contacttype(self):
        response = self.client.get(
            reverse("admin:forms_contacttypeforadminsite_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 2)

    def test_admin_can_see_all_contacttype(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(
            reverse("admin:forms_contacttypeforadminsite_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".field-sortable_str")), 8)

    def test_integrator_can_only_see_own_amendfield(self):
        response = self.client.get(
            reverse("admin:submissions_submissionamendfield_changelist")
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".grp-row")), 3)

    def test_integrator_can_only_see_own_complementarydocumenttype(self):
        response = self.client.get(
            reverse("admin:submissions_complementarydocumenttype_changelist")
        )
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parser.select(".grp-row-even")), 1)

    def test_admin_can_see_all_amendfield(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(
            reverse("admin:submissions_submissionamendfield_changelist")
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
            "permit_department-TOTAL_FORMS": 1,
            "permit_department-INITIAL_FORMS": 1,
            "permit_department-MIN_NUM_FORMS": 1,
            "permit_department-MAX_NUM_FORMS": 1,
            "permit_department-0-is_integrator_admin": True,
            "permit_department-0-group": group.id,
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
            error_msg=MULTIPLE_INTEGRATOR_ERROR_MESSAGE,
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
            error_msg=MULTIPLE_INTEGRATOR_ERROR_MESSAGE,
        )
        self.assertInHTML(expected, content)

    def test_admin_can_see_all_submissions(self):
        user = factories.SuperUserFactory()
        self.client.login(username=user.username, password="password")
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=user)

        response = self.client.get(reverse("admin:submissions_submission_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3.1 Consultation des demandes")

    def test_integrator_cannot_see_submissions(self):
        if settings.ENABLE_2FA:
            self.enable_otp_session(user=self.user)
        response = self.client.get(reverse("admin:submissions_submission_changelist"))
        self.assertEqual(response.status_code, 403)

    if settings.ENABLE_2FA:

        def test_user_of_group_with_mandatory_2FA_is_asked_to_set_it_up(self):
            user = factories.SecretariatUserFactory()
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

        def test_user_of_group_with_mandatory_2FA_setup_can_see_submissions_list(self):
            user = factories.UserFactory()
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
            user = factories.UserFactory()
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
            user = factories.UserFactory()
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
            user = factories.UserFactory()
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
