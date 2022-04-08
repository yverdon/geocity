from .. import factories
from permits import models, views
from ..geocity_test_case import GeocityTestCase
from django.urls import reverse
from django.contrib import messages


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

        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_RECEIVED,
            administrative_entity=self.administrative_entity,
        )
        self.permit_request.works_object_types.add(self.parent_type.work_object_types)

    def test_pilot_can_upload_single_complementary_document(self):
        with open("permits/tests/files/real_pdf.pdf", "rb") as file:
            data = {
                "form-0-description": ["Single document upload"],
                "form-0-status": [
                    models.PermitRequestComplementaryDocument.STATUS_OTHER
                ],
                "form-0-authorised_departments": [self.departments[self.VALIDATOR].pk],
                "form-0-is_public": ["0"],
                "form-0-document": [file],
                "form-0-document_type": [self.parent_type.pk],
                "form-0-parent_{}".format(self.parent_type.pk): [self.child_type.pk],
            }

            detail = self.execute_permit_request_action(
                data={**self.management_form, **data}
            )

            expected = "<div class='alert alert-success'>Les documents ont bien été ajoutés à la demande #{pk}.</div>".format(
                pk=self.permit_request.pk,
            )
            self.assertInHTML(expected, detail.content.decode())

    def test_pilot_can_upload_multiple_complementary_documents(self):
        with open("permits/tests/files/real_pdf.pdf", "rb") as file:
            data = {
                "form-0-description": ["Multiple document upload. #1"],
                "form-0-status": [
                    models.PermitRequestComplementaryDocument.STATUS_OTHER
                ],
                "form-0-authorised_departments": [self.departments[self.VALIDATOR].pk],
                "form-0-is_public": ["0"],
                "form-0-document": [file],
                "form-0-document_type": [self.parent_type.pk],
                "form-0-parent_{}".format(self.parent_type.pk): [self.child_type.pk],
                "form-1-description": ["Multiple document upload. #2"],
                "form-1-status": [
                    models.PermitRequestComplementaryDocument.STATUS_FINALE
                ],
                "form-1-authorised_departments": [self.departments[self.VALIDATOR].pk],
                "form-1-is_public": ["0"],
                "form-1-document": [file],
                "form-1-document_type": [self.parent_type.pk],
                "form-1-parent_{}".format(self.parent_type.pk): [self.child_type.pk],
            }

            detail = self.execute_permit_request_action(
                data={**self.management_form, **data}
            )

            expected = "<div class='alert alert-success'>Les documents ont bien été ajoutés à la demande #{pk}.</div>".format(
                pk=self.permit_request.pk,
            )
            self.assertInHTML(expected, detail.content.decode())

    def test_authorised_department_has_documents_in_summary(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={
                "action": "request_validation",
                "departments": [self.departments[self.VALIDATOR].pk],
            },
        )

        self.login(email="validator@geocity.lo", group=self.VALIDATOR)
        document = factories.ComplementaryDocumentFactory.create(
            permit_request=self.permit_request,
            authorised_departments=[self.departments[self.VALIDATOR].pk],
        )
        permit_request_detail = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )

        self.assertIn(document, list(permit_request_detail.context["documents"]))

    def test_public_document_visible_by_everyone(self):
        # we're logged in as the other of the request
        document = factories.ComplementaryDocumentFactory.create(
            permit_request=self.permit_request,
            authorised_departments=[self.departments[self.VALIDATOR].pk],
            is_public=True,
        )
        permit_request_detail = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        self.assertIn(document, list(permit_request_detail.context["documents"]))

    def prepare_document_test(self, document_args):

        document = factories.ComplementaryDocumentFactory.create(
            **{
                **{
                    "permit_request": self.permit_request,
                    "authorised_departments": [self.departments[self.VALIDATOR].pk],
                },
                **document_args,
            }
        )

        response = self.client.get(
            reverse(
                "permits:complementary_documents_delete", kwargs={"pk": document.pk},
            ),
            follow=True,
        )

        return document, response

    def test_document_owner_can_delete_file(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        document, _ = self.prepare_document_test(document_args={"owner": self.user,})

        self.assertFalse(
            models.PermitRequestComplementaryDocument.objects.filter(
                pk=document.pk
            ).exists()
        )

    def test_final_documents_can_not_be_deleted(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        document, response = self.prepare_document_test(
            document_args={
                "owner": self.user,
                "status": models.PermitRequestComplementaryDocument.STATUS_FINALE,
            }
        )

        message = [m for m in response.context["messages"]][0]
        actual = (message.message, message.level)
        expected = (
            views.PermitRequestComplementaryDocumentDeleteView.final_error_message,
            messages.ERROR,
        )
        self.assertResponseMessageContains(actual, expected)

    def test_non_owners_can_not_delete_documents(self):
        document, response = self.prepare_document_test(
            document_args={
                "status": models.PermitRequestComplementaryDocument.STATUS_FINALE,
            }
        )

        message = [m for m in response.context["messages"]][0]
        actual = (message.message, message.level)
        expected = (
            views.PermitRequestComplementaryDocumentDeleteView.owner_error_message,
            messages.ERROR,
        )
        self.assertResponseMessageContains(actual, expected)
