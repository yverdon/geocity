from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from geocity.tests import factories
from geocity.tests.utils import get_parser


class SubmissionSelectFormsTestCase(TestCase):
    def setUp(self):
        super().setUp()
        """Generate two entities with the following (per entity) :
        - groups : [integrator, pilot, validator]
        - users : One for each group and a normal user without permissions
        - forms : One private and wo public (prevents from automatically redirect when only 1 form found)
        """

        self.view_private_submission_permission = Permission.objects.get(
            codename="view_private_submission", content_type__app_label="submissions"
        )
        # ///////////////////////////
        # First entity
        # ///////////////////////////

        # Creation of the groups without a default department
        self.first_entity_pilot_group = factories.SecretariatGroupFactory(
            department=None
        )
        self.first_entity_validator_group = factories.ValidatorGroupFactory(
            department=None
        )
        self.first_entity_integrator_group = factories.IntegratorGroupFactory(
            department=None
        )

        # Creation of the entity
        self.first_entity_administrative_entity = factories.AdministrativeEntityFactory(
            integrator=self.first_entity_integrator_group
        )

        # Assign department.administrative_entity for groups
        factories.PermitDepartmentFactory(
            group=self.first_entity_pilot_group,
            administrative_entity=self.first_entity_administrative_entity,
        )
        factories.PermitDepartmentFactory(
            group=self.first_entity_validator_group,
            administrative_entity=self.first_entity_administrative_entity,
        )
        factories.IntegratorPermitDepartmentFactory(
            group=self.first_entity_integrator_group,
            administrative_entity=self.first_entity_administrative_entity,
        )

        # Create two public and one private forms
        self.first_entity_public_form = factories.FormFactory(
            name="a_form",
            integrator=self.first_entity_integrator_group,
            administrative_entities=[self.first_entity_administrative_entity],
            is_public=True,
        )

        self.first_entity_public_form_2 = factories.FormFactory(
            name="b_form",
            integrator=self.first_entity_integrator_group,
            administrative_entities=[self.first_entity_administrative_entity],
            is_public=True,
        )

        self.first_entity_private_form = factories.FormFactory(
            name="c_form",
            integrator=self.first_entity_integrator_group,
            administrative_entities=[self.first_entity_administrative_entity],
            is_public=False,
        )

        # Create the users and assign to the groups
        self.first_entity_user = factories.UserFactory()
        self.first_entity_pilot = factories.SecretariatUserFactory(
            groups=[self.first_entity_pilot_group]
        )
        self.first_entity_validator = factories.ValidatorUserFactory(
            groups=[self.first_entity_validator_group]
        )
        self.first_entity_integrator = factories.IntegratorUserFactory(
            groups=[self.first_entity_integrator_group]
        )

        # ///////////////////////////
        # Second entity
        # ///////////////////////////

        # Creation of the groups without a default department
        self.second_entity_pilot_group = factories.SecretariatGroupFactory(
            department=None
        )
        self.second_entity_validator_group = factories.ValidatorGroupFactory(
            department=None
        )
        self.second_entity_integrator_group = factories.IntegratorGroupFactory(
            department=None
        )

        # Creation of the entity
        self.second_entity_administrative_entity = (
            factories.AdministrativeEntityFactory(
                integrator=self.second_entity_integrator_group
            )
        )

        # Assign department.administrative_entity for groups
        factories.PermitDepartmentFactory(
            group=self.second_entity_pilot_group,
            administrative_entity=self.second_entity_administrative_entity,
        )
        factories.PermitDepartmentFactory(
            group=self.second_entity_validator_group,
            administrative_entity=self.second_entity_administrative_entity,
        )
        factories.IntegratorPermitDepartmentFactory(
            group=self.second_entity_integrator_group,
            administrative_entity=self.second_entity_administrative_entity,
        )

        # Create two public and one private forms
        self.second_entity_public_form = factories.FormFactory(
            name="a_form",
            integrator=self.second_entity_integrator_group,
            administrative_entities=[self.second_entity_administrative_entity],
            is_public=True,
        )

        self.second_entity_public_form_2 = factories.FormFactory(
            name="b_form",
            integrator=self.second_entity_integrator_group,
            administrative_entities=[self.second_entity_administrative_entity],
            is_public=True,
        )

        self.second_entity_private_form = factories.FormFactory(
            name="c_form",
            integrator=self.second_entity_integrator_group,
            administrative_entities=[self.second_entity_administrative_entity],
            is_public=False,
        )

        # Create the users and assign to the groups
        self.second_entity_user = factories.UserFactory()
        self.second_entity_pilot = factories.SecretariatUserFactory(
            groups=[self.second_entity_pilot_group]
        )
        self.second_entity_validator = factories.ValidatorUserFactory(
            groups=[self.second_entity_validator_group]
        )
        self.second_entity_integrator = factories.IntegratorUserFactory(
            groups=[self.second_entity_integrator_group]
        )

    # Public are shown, private are not shown
    def test_user_can_see_only_public_forms(self):
        self.client.login(username=self.first_entity_user, password="password")
        submission = factories.SubmissionFactory(
            author=self.first_entity_user,
            administrative_entity=self.first_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # Contains only two elements. The 2 public are visible and the private is hidden
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            2,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertNotIn(self.first_entity_private_form.name, content)

    # Public are shown, private are not shown
    def test_pilot_can_see_only_public_forms_without_perms(self):
        self.client.login(username=self.first_entity_pilot, password="password")
        submission = factories.SubmissionFactory(
            author=self.first_entity_pilot,
            administrative_entity=self.first_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # User should not have this perm to make the test work properly via group
        self.assertFalse(
            self.first_entity_pilot.has_perm("submissions.view_private_submission")
        )

        # Contains only two elements. The 2 public are visible and the private is hidden
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            2,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertNotIn(self.first_entity_private_form.name, content)

    # Public are shown, private are shown only for his entity, other entities private aren't shown
    def test_pilot_can_see_private_forms_with_perms_of_his_entity(self):
        # Own entity
        # Show everything with submissions.view_private_submission

        # Add permissions to view private submissions
        self.first_entity_pilot_group.permissions.set(
            [self.view_private_submission_permission]
        )
        self.assertTrue(
            self.first_entity_pilot.has_perm("submissions.view_private_submission")
        )

        self.client.login(username=self.first_entity_pilot, password="password")
        first_entity_submission = factories.SubmissionFactory(
            author=self.first_entity_pilot,
            administrative_entity=self.first_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": first_entity_submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # Contains 3 elements. The 2 public are visible and the private is also visible via permission
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            3,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertIn(self.first_entity_private_form.name, content)

        # Other entity
        # Show only public with submissions.view_private_submission
        second_entity_submission = factories.SubmissionFactory(
            author=self.first_entity_pilot,
            administrative_entity=self.second_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": second_entity_submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # Contains only two elements. The 2 public are visible and the private is hidden
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            2,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertNotIn(self.first_entity_private_form.name, content)

    # Public are shown, private are not shown
    def test_validator_can_see_only_public_forms_without_perms(self):
        self.client.login(username=self.first_entity_validator, password="password")
        submission = factories.SubmissionFactory(
            author=self.first_entity_validator,
            administrative_entity=self.first_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # User should not have this perm to make the test work properly via group
        self.assertFalse(
            self.first_entity_validator.has_perm("submissions.view_private_submission")
        )

        # Contains only two elements. The 2 public are visible and the private is hidden
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            2,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertNotIn(self.first_entity_private_form.name, content)

    # Public are shown, private are shown only for his entity, other entities private aren't shown
    def test_validator_can_see_private_forms_with_perms_of_his_entity(self):
        # Own entity
        # Show everything with submissions.view_private_submission

        # Add permissions to view private submissions
        self.first_entity_validator_group.permissions.set(
            [self.view_private_submission_permission]
        )
        self.assertTrue(
            self.first_entity_validator.has_perm("submissions.view_private_submission")
        )

        self.client.login(username=self.first_entity_validator, password="password")
        first_entity_submission = factories.SubmissionFactory(
            author=self.first_entity_validator,
            administrative_entity=self.first_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": first_entity_submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # Contains 3 elements. The 2 public are visible and the private is also visible via permission
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            3,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertIn(self.first_entity_private_form.name, content)

        # Other entity
        # Show only public with submissions.view_private_submission
        second_entity_submission = factories.SubmissionFactory(
            author=self.first_entity_validator,
            administrative_entity=self.second_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": second_entity_submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # Contains only two elements. The 2 public are visible and the private is hidden
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            2,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertNotIn(self.first_entity_private_form.name, content)

    # Public are shown, private are shown only for his entity, other entities private aren't shown
    def test_integrator_can_see_everything_without_perms_of_his_entity(self):
        # Remove permissions, cause integrator don't need permissions to see private
        self.first_entity_integrator_group.permissions.clear()
        self.assertFalse(
            self.first_entity_integrator.has_perm("submissions.view_private_submission")
        )

        self.client.login(username=self.first_entity_integrator, password="password")
        first_entity_submission = factories.SubmissionFactory(
            author=self.first_entity_integrator,
            administrative_entity=self.first_entity_administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": first_entity_submission.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)
        content = response.content.decode()

        # Contains 3 elements. The 2 public are visible and the private is also visible via permission
        self.assertEqual(
            len(parser.select('input[name="forms-selected_forms"]')),
            3,
        )
        self.assertIn(self.first_entity_public_form.name, content)
        self.assertIn(self.first_entity_public_form_2.name, content)
        self.assertIn(self.first_entity_private_form.name, content)
