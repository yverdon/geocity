import urllib.parse
from datetime import date

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInUserMixin, get_parser


class SubmissionUpdateTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=self.submission)
        self.submission.administrative_entity.forms.set(self.submission.forms.all())

    def test_form_step_submit_updates_submission(self):
        new_form = factories.FormFactory()
        self.submission.administrative_entity.forms.add(new_form)
        current_forms = list(self.submission.forms.all())

        self.client.post(
            (
                reverse(
                    "submissions:submission_select_forms",
                    kwargs={"submission_id": self.submission.pk},
                )
            ),
            data={
                "forms-selected_forms": [form.pk for form in current_forms + [new_form]]
            },
        )

        self.submission.refresh_from_db()

        self.assertEqual(submissions_models.Submission.objects.count(), 1)
        self.assertEqual(
            set(self.submission.forms.all()),
            set(current_forms + [new_form]),
        )

    def test_fields_step_submit_updates_submission(self):
        new_field = factories.FieldFactory()
        new_field.forms.set(self.submission.forms.all())
        data = {
            "fields-{}_{}".format(form.pk, new_field.pk): "value-{}".format(form.pk)
            for form in self.submission.forms.all()
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        self.assertEqual(
            set(
                item["val"]
                for item in self.submission.get_fields_values().values_list(
                    "value", flat=True
                )
            ),
            set(data.values()),
        )

    def test_missing_mandatory_address_field_gives_invalid_feedback(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeAddress(
            input_type=submissions_models.Field.INPUT_TYPE_ADDRESS, is_mandatory=True
        )
        field.forms.set(submission.forms.all())

        data = {
            "fields-{}_{}".format(form.pk, field.pk): ""
            for form in submission.forms.all()
        }

        response = self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )
        parser = get_parser(response.content)
        self.assertEqual(1, len(parser.select(".invalid-feedback")))

    def test_fields_step_submit_updates_submission_with_address(self):
        address_field = factories.FieldFactoryTypeAddress(
            input_type=submissions_models.Field.INPUT_TYPE_ADDRESS
        )
        address_field.forms.set(self.submission.forms.all())
        form = self.submission.forms.first()
        data = {f"fields-{form.pk}_{address_field.pk}": "Hôtel Martinez, Cannes"}
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        self.submission.refresh_from_db()
        field_val = self.submission.get_fields_values().get(
            field__input_type=submissions_models.Field.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(field_val.value, {"val": "Hôtel Martinez, Cannes"})

    def test_fields_step_submit_updates_geotime_with_address_store_geometry_for_address_field(
        self,
    ):

        address_field = factories.FieldFactoryTypeAddress(
            input_type=submissions_models.Field.INPUT_TYPE_ADDRESS,
            store_geometry_for_address_field=True,
        )
        address_field.forms.set(self.submission.forms.all())
        form = self.submission.forms.first()
        data = {
            f"fields-{form.pk}_{address_field.pk}": "Place pestalozzi 2, 1400 Yverdon-les-Bains"
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        self.submission.refresh_from_db()
        field_val = self.submission.get_fields_values().get(
            field__input_type=submissions_models.Field.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(
            field_val.value, {"val": "Place pestalozzi 2, 1400 Yverdon-les-Bains"}
        )
        geocoded_geotime_row = submissions_models.SubmissionGeoTime.objects.filter(
            submission=self.submission, comes_from_automatic_geocoding=True
        ).count()
        self.assertEqual(1, geocoded_geotime_row)

    def test_fields_step_submit_updates_submission_with_date(self):

        date_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_DATE, name="datum"
        )
        today = date.today()
        form = self.submission.forms.first()
        date_field.forms.set([form])
        data = {
            f"fields-{form.pk}_{date_field.pk}": today.strftime(
                settings.DATE_INPUT_FORMAT
            )
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        field_val = self.submission.get_fields_values().get(field__name="datum")
        self.assertEqual(
            field_val.value,
            {"val": today.isoformat()},
        )
        self.assertEqual(
            field_val.field.input_type,
            submissions_models.Field.INPUT_TYPE_DATE,
        )
