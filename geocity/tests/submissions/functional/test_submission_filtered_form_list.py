import io

import tablib
from django.test import TestCase
from django.urls import reverse

from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInSecretariatMixin


class SubmissionFilteredFormListTestCase(LoggedInSecretariatMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.form_normal = factories.FormFactory()
        self.submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        self.submission.forms.set([self.form_normal])
        factories.SubmissionGeoTimeFactory(submission=self.submission)

        selected_form = self.submission.selected_forms.first()
        field = factories.FieldFactory()
        field.forms.add(selected_form.form)
        self.field_value = factories.FieldValueFactory(
            selected_form=selected_form, field=field
        )

    def test_secretariat_user_can_see_filtered_submission_details(
        self,
    ):
        response = self.client.get(
            "{}?forms={}".format(
                reverse(
                    "submissions:submissions_list",
                ),
                self.submission.forms.first().id,
            )
        )

        self.assertInHTML(self.field_value.value["val"], response.content.decode())

    def test_secretariat_user_can_see_filtered_submission_details_in_xlsx(
        self,
    ):
        response = self.client.get(
            "{}?forms={}&_export=xlsx".format(
                reverse(
                    "submissions:submissions_list",
                ),
                self.submission.forms.first().id,
            )
        )
        content = io.BytesIO(response.getvalue())

        # Replace content in bytes with the readable one
        response = str(tablib.import_set(content.read(), format="xlsx"))

        self.assertIn(str(self.field_value.value["val"]), response)
        self.assertIn(str(self.field_value.field), response)
