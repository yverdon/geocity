from django.test import TestCase
from django.urls import reverse

from geocity.apps.forms import models as forms_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInUserMixin, get_parser


def extract_nav_items(content):
    nav_items = get_parser(content).select(".progress-nav-item .step-name")
    return [nav_item.text.strip() for nav_item in nav_items]


class SubmissionProgressBarTestCase(LoggedInUserMixin, TestCase):
    def create_submission(self):
        submission = factories.SubmissionFactory(author=self.user)
        return submission

    def test_contacts_step_does_not_appear_when_no_contacts_required(self):
        submission = self.create_submission()
        form = factories.FormFactory()
        submission.administrative_entity.forms.set([form])
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertNotIn("Contacts", nav_items)

    def test_contacts_step_appears_when_contacts_required(self):
        submission = self.create_submission()
        form = factories.FormFactory()
        submission.administrative_entity.forms.set([form])
        submission.forms.set([form])
        factories.ContactFormFactory(form_category=form.category)

        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Contacts", nav_items)

    def test_appendices_step_does_not_appear_when_no_appendices_required(self):
        submission = self.create_submission()
        form = factories.FormFactory()
        submission.administrative_entity.forms.set([form])
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertNotIn("Documents", nav_items)

    def test_appendices_step_appears_when_appendices_required(self):
        submission = self.create_submission()
        form = factories.FormFactory()
        submission.administrative_entity.forms.set([form])
        submission.forms.set([form])
        field = factories.FieldFactory(
            input_type=forms_models.Field.INPUT_TYPE_FILE,
        )
        field.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Documents", nav_items)

    def test_geotime_step_does_not_appear_when_no_date_nor_geometry_types_are_required(
        self,
    ):
        submission = self.create_submission()
        form = factories.FormWithoutGeometryFactory(
            needs_date=False,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertNotIn("Planning et localisation", nav_items)
        self.assertNotIn("Planning", nav_items)
        self.assertNotIn("Localisation", nav_items)

    def test_geotime_step_appears_when_date_and_geometry_types_are_required(self):
        submission = self.create_submission()
        form = factories.FormFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=True,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Planning et localisation", nav_items)

    def test_geotime_step_appears_when_only_date_is_required(self):
        submission = self.create_submission()
        form = factories.FormWithoutGeometryFactory(
            needs_date=True,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Planning", nav_items)
        self.assertNotIn("Planning et localisation", nav_items)
        self.assertNotIn("Localisation", nav_items)

    def test_geotime_step_appears_when_only_geometry_types_are_required(self):
        submission = self.create_submission()
        form = factories.FormFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=False,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Localisation", nav_items)
        self.assertNotIn("Planning et localisation", nav_items)
        self.assertNotIn("Planning", nav_items)
