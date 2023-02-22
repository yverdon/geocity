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
        # ///////////////////////////
        # First entity
        # ///////////////////////////

        # Creation of the groups
        self.first_entity_pilot_group = factories.SecretariatGroupFactory()
        self.first_entity_validator_group = factories.ValidatorGroupFactory()
        self.first_entity_integrator_group = factories.IntegratorGroupFactory()
        self.first_entity_integrator_group.department = (
            factories.IntegratorPermitDepartmentFactory()
        )
        self.first_entity_integrator_group.save()

        # Creation of the entity
        self.first_entity_administrative_entity = factories.AdministrativeEntityFactory(
            integrator=self.first_entity_integrator_group
        )

        # Create two public and one private forms
        self.first_entity_public_form = factories.FormFactory(
            integrator=self.first_entity_integrator_group,
            administrative_entities=[self.first_entity_administrative_entity],
            is_public=True,
        )

        self.first_entity_public_form_2 = factories.FormFactory(
            integrator=self.first_entity_integrator_group,
            administrative_entities=[self.first_entity_administrative_entity],
            is_public=True,
        )

        self.first_entity_private_form = factories.FormFactory(
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

        # Creation of the groups
        self.second_entity_pilot_group = factories.SecretariatGroupFactory()
        self.second_entity_validator_group = factories.ValidatorGroupFactory()
        self.second_entity_integrator_group = factories.IntegratorGroupFactory()
        self.second_entity_integrator_group.department = (
            factories.IntegratorPermitDepartmentFactory()
        )
        self.second_entity_integrator_group.save()

        # Creation of the entity
        self.second_entity_administrative_entity = (
            factories.AdministrativeEntityFactory(
                integrator=self.second_entity_integrator_group
            )
        )

        # Create two public and one private forms
        self.second_entity_public_form = factories.FormFactory(
            integrator=self.second_entity_integrator_group,
            administrative_entities=[self.second_entity_administrative_entity],
            is_public=True,
        )

        self.second_entity_public_form_2 = factories.FormFactory(
            integrator=self.second_entity_integrator_group,
            administrative_entities=[self.second_entity_administrative_entity],
            is_public=True,
        )

        self.second_entity_private_form = factories.FormFactory(
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
        self.assertInHTML(self.first_entity_public_form.name, content)
        self.assertInHTML(self.first_entity_public_form_2.name, content)

    # Public are shown, private are not shown
    def test_pilot_can_see_only_public_forms_without_perms(self):
        pass

    # Public are shown, private are shown only for his entity, other entities private aren't shown
    def test_pilot_can_see_private_forms_with_perms_of_his_entity(self):
        pass

    # Public are shown, private are not shown
    def test_validator_can_see_only_public_forms_without_perms(self):
        pass

    # Public are shown, private are shown only for his entity, other entities private aren't shown
    def test_validator_can_see_private_forms_with_perms_of_his_entity(self):
        pass

    # Public are shown, private are shown only for his entity, other entities private aren't shown
    def test_integrator_can_see_everything_without_perms_of_his_entity(self):
        pass
