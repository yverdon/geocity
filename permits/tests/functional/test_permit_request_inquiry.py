from datetime import datetime, timedelta

from django.urls import reverse

from permits import models

from .. import factories
from ..geocity_test_case import GeocityTestCase


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

        today = datetime.today().date()
        self.data = {
            "start_date": today.strftime("%d.%m.%Y"),
            "end_date": (today + timedelta(days=5)).strftime("%d.%m.%Y"),
            "action": self.action,
        }

    @classmethod
    def assertInquiryCreated(cls, inquiry, expected_data):
        if inquiry.pk is None:
            raise AssertionError("Give inquiry doesn't have an ID")

        if not inquiry.start_date.strftime("%d.%m.%Y") == expected_data["start_date"]:
            raise AssertionError(
                "Starting date doesn't match! Actual: {}, Expected {}".format(
                    inquiry.start_date.strftime("%d.%m.%Y"), expected_data["start_date"]
                )
            )

        if not inquiry.end_date.strftime("%d.%m.%Y") == expected_data["end_date"]:
            raise AssertionError(
                "Ending date doesn't match! Actual: {}, Expected {}".format(
                    inquiry.end_date.strftime("%d.%m.%Y"), expected_data["end_date"]
                )
            )

        if not list(inquiry.documents.all()) == expected_data["documents"]:
            raise AssertionError(
                "Expected {} but got {}".format(
                    expected_data["documents"], list(inquiry.documents.all())
                )
            )

    def test_start_inquiry_without_documents(self):

        detail = self.execute_permit_request_action(data=self.data)
        inquiry = detail.context["forms"][self.action].instance

        self.assertInquiryCreated(
            inquiry=inquiry,
            expected_data={
                "start_date": self.data["start_date"],
                "end_date": self.data["end_date"],
                "documents": [],
            },
        )
        self.assertEqual(
            self.permit_request.status, models.PermitRequest.STATUS_INQUIRY_IN_PROGRESS
        )

    def test_start_inquiry_with_public_documents(self):
        document = factories.ComplementaryDocumentFactory.create(
            permit_request=self.permit_request,
            authorised_departments=[self.departments[self.VALIDATOR].pk],
            is_public=True,
        )

        detail = self.execute_permit_request_action(
            data={
                **self.data,
                **{
                    "documents": document.pk,
                },
            }
        )
        inquiry = detail.context["forms"][self.action].instance

        self.assertInquiryCreated(
            inquiry=inquiry,
            expected_data={
                "start_date": self.data["start_date"],
                "end_date": self.data["end_date"],
                "documents": [document],
            },
        )

    def test_start_inquiry_with_non_public_documents_asks_confirmation(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)

        document = factories.ComplementaryDocumentFactory.create(
            permit_request=self.permit_request,
            authorised_departments=[self.departments[self.VALIDATOR].pk],
        )

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={
                **self.data,
                **{
                    "documents": document.pk,
                },
            },
        )

        expected = '<input name="confirmation" type="hidden" value="confirmed">'
        self.assertInHTML(expected, response.content.decode())

    def test_inquiry_with_non_public_documents_changes_to_public(self):
        document = factories.ComplementaryDocumentFactory.create(
            permit_request=self.permit_request,
            authorised_departments=[self.departments[self.VALIDATOR].pk],
        )

        detail = self.execute_permit_request_action(
            data={
                **self.data,
                **{
                    "documents": document.pk,
                    "confirmation": "confirmed",
                },
            }
        )
        inquiry = detail.context["forms"][self.action].instance

        document.refresh_from_db()

        self.assertInquiryCreated(
            inquiry=inquiry,
            expected_data={
                "start_date": self.data["start_date"],
                "end_date": self.data["end_date"],
                "documents": [document],
            },
        )

        self.assertTrue(document.is_public)
