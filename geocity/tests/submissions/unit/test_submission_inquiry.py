from datetime import datetime, timedelta

from geocity.apps.submissions import forms
from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.geocity_test_case import GeocityTestCase


class TestSubmissionInquiry(GeocityTestCase):
    def test_inquiries_cant_overlap(self):
        self.login(email="user@test.com")

        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_RECEIVED,
            administrative_entity=self.administrative_entity,
        )
        submission.forms.add(factories.FormFactory())

        start_date = datetime.today() + timedelta(days=10)
        end_date = start_date + timedelta(days=10)
        factories.SubmissionInquiryFactory(
            submission=submission, start_date=start_date, end_date=end_date
        )

        test_data = [
            {
                "start_date": (start_date + timedelta(days=2)).strftime("%d.%m.%Y"),
                "end_date": (end_date + timedelta(days=2)).strftime("%d.%m.%Y"),
            },
            {
                "start_date": (start_date - timedelta(days=2)).strftime("%d.%m.%Y"),
                "end_date": (end_date - timedelta(days=2)).strftime("%d.%m.%Y"),
            },
            {
                "start_date": (start_date - timedelta(days=2)).strftime("%d.%m.%Y"),
                "end_date": (end_date + timedelta(days=2)).strftime("%d.%m.%Y"),
            },
            {
                "start_date": (start_date + timedelta(days=2)).strftime("%d.%m.%Y"),
                "end_date": (end_date - timedelta(days=2)).strftime("%d.%m.%Y"),
            },
        ]

        for data in test_data:
            form = forms.SubmissionInquiryForm(submission=submission, data=data)

            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors,
                {"__all__": ["Une enquête est déjà en cours pendant cette période"]},
            )
