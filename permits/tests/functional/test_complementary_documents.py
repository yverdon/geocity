from .. import factories
from permits import models
from ..geocity_test_case import GeocityTestCase
from django.urls import reverse


class TestComplementaryDocuments(GeocityTestCase):
    def setUp(self):
        self.works_types = factories.WorksTypeFactory.create_batch(2)
        self.works_objects = factories.WorksObjectFactory.create_batch(2)

        models.WorksObjectType.objects.create(
            works_type=self.works_types[0],
            works_object=self.works_objects[0],
            is_public=True,
        )
        models.WorksObjectType.objects.create(
            works_type=self.works_types[1],
            works_object=self.works_objects[1],
            is_public=True,
        )

    def test_pilot_can_upload_single_complementary_document(self):
        self.login(email="user@test.com", group=self.SECRETARIAT)
        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_RECEIVED,
            administrative_entity=department.administrative_entity,
        )

        with open("permits/tests/files/real_pdf.pdf", "rb") as file:
            response = self.client.post(
                reverse(
                    "permits:permit_request_detail",
                    kwargs={"permit_request_id": permit_request.pk},
                ),
                data={
                    "form-TOTAL_FORMS": ["1"],
                    "form-INITIAL_FORMS": ["0"],
                    "form-MIN_NUM_FORMS": ["0"],
                    "form-MAX_NUM_FORMS": ["1000"],
                    "form-0-description": ["Form description"],
                    "form-0-status": [
                        models.PermitRequestComplementaryDocument.STATUS_OTHER
                    ],
                    "form-0-authorised_departments": ["3"],
                    "form-0-is_public": ["0"],
                    "form-0-document": [file],
                    "action": "complementary_documents",
                    "save_continue": "",
                },
            )
        permit_request.refresh_from_db()
        self.assertEqual(response.status_code, 302)

        permit_request_detail = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        expected = "<div class='alert alert-success'>Les documents ont bien été ajoutés à la demande #{pk}.</div>".format(
            pk=permit_request.pk,
        )
        self.assertInHTML(expected, permit_request_detail.content.decode())
