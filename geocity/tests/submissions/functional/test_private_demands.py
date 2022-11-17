from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from geocity.apps.forms import models as forms_models
from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInUserMixin, get_parser


class PrivateDemandsTestCase(LoggedInUserMixin, TestCase):
    def test_administrative_entity_step_without_public_requests_is_empty_to_standard_user(
        self,
    ):

        form_category = factories.FormCategoryFactory()
        private_form = factories.FormFactory(
            category=form_category,
            is_public=False,
        )

        administrative_entity = factories.AdministrativeEntityFactory(
            name="privateEntity"
        )
        private_form.administrative_entities.set([administrative_entity])
        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
            ),
        )
        self.assertNotContains(response, "privateEntity")

    def test_administrative_entity_step_without_public_requests_is_visible_to_user_with_specific_permission(
        self,
    ):

        view_private_submission_permission = Permission.objects.get(
            codename="view_private_submission", content_type__app_label="submissions"
        )
        self.user.user_permissions.add(view_private_submission_permission)
        form_category = factories.FormCategoryFactory()
        private_form = factories.FormFactory(
            category=form_category,
            is_public=True,
        )

        administrative_entity_1 = factories.AdministrativeEntityFactory(
            name="privateEntity1"
        )
        administrative_entity_2 = factories.AdministrativeEntityFactory(
            name="privateEntity2"
        )
        private_form.administrative_entities.set(
            [administrative_entity_1, administrative_entity_2]
        )
        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
            ),
        )

        self.assertContains(response, "privateEntity1")
        self.assertContains(response, "privateEntity2")

    def test_form_step_show_public_requests_to_standard_user(
        self,
    ):
        public_forms = factories.FormFactory.create_batch(2, is_public=True)
        private_form = factories.FormFactory(is_public=False)
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set(public_forms + [private_form])

        submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=administrative_entity
        )

        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        submissions_models.SelectedForm.objects.create(
            submission=submission,
            form=public_forms[0],
        )

        submissions_models.SelectedForm.objects.create(
            submission=submission,
            form=public_forms[1],
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )
        self.assertEqual(
            len(get_parser(response.content).select("#id_forms-selected_forms label")),
            2,
        )

    def test_form_step_show_private_requests_to_user_with_specific_permission(
        self,
    ):

        view_private_submission_permission = Permission.objects.get(
            codename="view_private_submission", content_type__app_label="submissions"
        )
        self.user.user_permissions.add(view_private_submission_permission)

        public_forms = factories.FormFactory.create_batch(2, is_public=True)
        private_form = factories.FormFactory(is_public=False)
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set(public_forms + [private_form])

        submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=administrative_entity
        )

        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        submissions_models.SelectedForm.objects.create(
            submission=submission,
            form=public_forms[0],
        )

        submissions_models.SelectedForm.objects.create(
            submission=submission,
            form=public_forms[1],
        )

        submissions_models.SelectedForm.objects.create(
            submission=submission, form=private_form
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )
        self.assertEqual(
            len(get_parser(response.content).select("#id_forms-selected_forms label")),
            3,
        )
