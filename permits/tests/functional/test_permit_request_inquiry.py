from ..geocity_test_case import GeocityTestCase
from .. import factories
from permits import models
from django.urls import reverse
from datetime import datetime, timedelta

class TestPermitRequestInquiry(GeocityTestCase):

    action = models.ACTION_REQUEST_INQUIRY

    def setUp(self):
        super().setUp()

        self.login(email="user@test.com")
        self.parent_type = factories.ParentComplementaryDocumentTypeFactory()

        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_RECEIVED,
            administrative_entity=self.administrative_entity,
        )
        self.permit_request.works_object_types.add(factories.WorksObjectTypeFactory())


    def test_pilot_can_start_inquiry_without_documents(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)

        today = datetime.today().date()

        data = {
            "start_date": today.strftime("%d.%m.%Y"),
            "end_date": (today + timedelta(days=5)).strftime("%d.%m.%Y"),
            "action": self.action
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)

        permit_request_detail = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )

        inquiry = permit_request_detail.context['forms'][self.action].instance
        self.assertIsNotNone(inquiry.pk)
        self.assertEqual(inquiry.start_date.strftime("%d.%m.%Y"), data["start_date"])
        self.assertEqual(inquiry.end_date.strftime("%d.%m.%Y"), data["end_date"])
        self.assertFalse(inquiry.documents.all().exists())

