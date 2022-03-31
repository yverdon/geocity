from .. import factories
from permits import models
from ..geocity_test_case import GeocityTestCase
from django.urls import reverse


class TestComplementaryDocuments(GeocityTestCase):

    management_form = {
        "form-TOTAL_FORMS": ["1"],
        "form-INITIAL_FORMS": ["0"],
        "form-MIN_NUM_FORMS": ["0"],
        "form-MAX_NUM_FORMS": ["1000"],
        "action": "complementary_documents",
        "save_continue": "",
    }

    def setUp(self):
        super().setUp()

        self.login(email="user@test.com")
        self.parent_type = factories.ParentComplementaryDocumentTypeFactory()
        self.child_type = factories.ChildComplementaryDocumentTypeFactory(
            parent=self.parent_type
        )
        self.department = models.PermitDepartment.objects.filter(
            group=self.groups[self.SECRETARIAT]
        ).get()
        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_RECEIVED,
            administrative_entity=self.department.administrative_entity,
        )
        self.permit_request.works_object_types.add(self.parent_type.work_object_types)

    def execute_complementary_document_upload_test(self, data):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={**self.management_form, **data},
        )
        self.assertEqual(response.status_code, 302)

        permit_request_detail = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        expected = "<div class='alert alert-success'>Les documents ont bien été ajoutés à la demande #{pk}.</div>".format(
            pk=self.permit_request.pk,
        )
        self.assertInHTML(expected, permit_request_detail.content.decode())

    def test_pilot_can_upload_single_complementary_document(self):
        with open("permits/tests/files/real_pdf.pdf", "rb") as file:
            data = {
                "form-0-description": ["Single document upload"],
                "form-0-status": [
                    models.PermitRequestComplementaryDocument.STATUS_OTHER
                ],
                "form-0-authorised_departments": [self.department.pk],
                "form-0-is_public": ["0"],
                "form-0-document": [file],
                "form-0-document_type": [self.parent_type.pk],
                "form-0-parent_{}".format(self.parent_type.pk): [self.child_type.pk],
            }

            self.execute_complementary_document_upload_test(data)

    def test_pilot_can_upload_multiple_complementary_documents(self):
        with open("permits/tests/files/real_pdf.pdf", "rb") as file:
            data = {
                "form-0-description": ["Multiple document upload. #1"],
                "form-0-status": [
                    models.PermitRequestComplementaryDocument.STATUS_OTHER
                ],
                "form-0-authorised_departments": [self.department.pk],
                "form-0-is_public": ["0"],
                "form-0-document": [file],
                "form-0-document_type": [self.parent_type.pk],
                "form-0-parent_{}".format(self.parent_type.pk): [self.child_type.pk],
                "form-1-description": ["Multiple document upload. #2"],
                "form-1-status": [
                    models.PermitRequestComplementaryDocument.STATUS_FINALE
                ],
                "form-1-authorised_departments": [self.department.pk],
                "form-1-is_public": ["0"],
                "form-1-document": [file],
                "form-1-document_type": [self.parent_type.pk],
                "form-1-parent_{}".format(self.parent_type.pk): [self.child_type.pk],
            }

            self.execute_complementary_document_upload_test(data)
