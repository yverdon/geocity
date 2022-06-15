from datetime import datetime, timedelta

from permits import forms, models

from .. import factories
from ..geocity_test_case import GeocityTestCase


class TestPermitRequestInquiry(GeocityTestCase):
    def setUp(self):
        super().setUp()

        self.login(email="user@test.com")

        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_RECEIVED,
            administrative_entity=self.administrative_entity,
        )
        self.permit_request.works_object_types.add(factories.WorksObjectTypeFactory())

    def test_inquiries_cant_overlap(self):
        start_date = datetime.today() + timedelta(days=10)
        end_date = start_date + timedelta(days=10)
        factories.PermitRequestInquiryFactory(
            permit_request=self.permit_request, start_date=start_date, end_date=end_date
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
            form = forms.PermitRequestInquiryForm(
                permit_request=self.permit_request, data=data
            )

            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors,
                {"__all__": ["Une enquête est déjà en cours pendant cette période"]},
            )
