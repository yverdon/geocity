import os
from distutils.util import strtobool

import diffimg
import pdf2image
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from permits.models import (
    ComplementaryDocumentType,
    PermitAdministrativeEntity,
    PermitAuthor,
    PermitDepartment,
    PermitRequest,
    PermitRequestAmendProperty,
    PermitRequestAmendPropertyValue,
    PermitRequestGeoTime,
    PermitWorkflowStatus,
    WorksObject,
    WorksObjectType,
    WorksObjectTypeChoice,
    WorksType,
)

from ..models import Report

UPDATE_EXPECTED_IMAGES = strtobool(os.getenv("TEST_UPDATED_EXPECTED_IMAGES", "false"))

# TODO: these tests cannot fully work as expected with the current infra, because
# the pdf/qgis container call the regular webserver running in the web container
# instead of the test server, meaning it has no access to database changes because
# they are on the test database (plus also in a transaction).
# We probably need to use LiveServerTestCase instead, and run tests with `run`
# instead of `exec`.
# Currently, the test passes but the QGIS map is not correctly rendered.
class ReportsTests(TestCase):
    def setUp(self):

        # Create the admin entity
        admin_entity = PermitAdministrativeEntity.objects.create(
            name="entity",
            ofs_id=1,
            geom="SRID=2056;MultiPolygon (((2500000 1000000, 2500100 1000000, 2500100 1000100, 2500000 1000100, 2500000 1000000)))",
        )

        # Create the user
        user = User.objects.create(
            username="user",
            is_superuser=True,
        )
        group = Group.objects.create(name="group")
        user.groups.set([group])
        dept = PermitDepartment.objects.create(
            administrative_entity=admin_entity,
            group=group,
            is_validator=True,
            is_integrator_admin=True,
            is_backoffice=True,
            is_default_validator=True,
        )
        author = PermitAuthor.objects.create(
            user=user,
            company_name="company_name",
            vat_number="vat_number",
            address="address",
            zipcode=1000,
            city="city",
            phone_first="phone_first",
            phone_second="phone_second",
        )

        # Create and configure the work object type
        works_type = WorksType.objects.create(name="type")
        works_obj = WorksObject.objects.create(name="object")
        works_object_type = WorksObjectType.objects.create(
            works_type=works_type,
            works_object=works_obj,
            is_public=True,
            document_enabled=True,
        )
        prop = PermitRequestAmendProperty.objects.create(
            name="prop",
        )
        prop.works_object_types.set([works_object_type])
        status = PermitWorkflowStatus.objects.create(
            status=PermitRequest.STATUS_PROCESSING,
            administrative_entity=admin_entity,
        )

        # Create the permit request
        permit_request = PermitRequest.objects.create(
            administrative_entity=admin_entity,
            author=author,
            status=PermitRequest.STATUS_PROCESSING,
        )
        works_obj_type_choice = WorksObjectTypeChoice.objects.create(
            permit_request=permit_request,
            works_object_type=works_object_type,
        )

        PermitRequestGeoTime.objects.create(
            permit_request=permit_request,
            geom="SRID=2056;GEOMETRYCOLLECTION (MultiPolygon (((2500025 1000025, 2500075 1000025, 2500075 1000075, 2500025 1000075, 2500025 1000025))))",
        )
        PermitRequestAmendPropertyValue.objects.create(
            property=prop,
            works_object_type_choice=works_obj_type_choice,
            value="myvalue",
        )

        # Create the document type
        parent_doc_type = ComplementaryDocumentType.objects.create(
            name="parent",
            work_object_types=works_object_type,
        )
        doc_type = ComplementaryDocumentType.objects.create(
            name="child",
            parent=parent_doc_type,
        )

        # Assign the report (normally, one should have been created automatically)
        report = Report.objects.filter(integrator=group).first()
        report.document_types.set([doc_type])

        # Make fixtures available to testcase
        self.permit_request = permit_request
        self.works_object_type = works_object_type
        self.report = report
        self.doc_type = doc_type
        self.user = user
        self.dept = dept

    @property
    def data_dir(self):
        """Where to find/store expected/generated images"""
        return os.path.join(os.path.dirname(__file__), "data", self._testMethodName)

    def test_pdf_preview(self):
        """Test PDF generation through the reports:permit_request_report view"""

        # Get the PDF
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "reports:permit_request_report",
                kwargs={
                    "permit_request_id": self.permit_request.pk,
                    "work_object_type_id": self.works_object_type.pk,
                    "report_id": self.report.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 200)

        # Compare the generated PDF against the expected images
        if UPDATE_EXPECTED_IMAGES:
            os.makedirs(self.data_dir, exist_ok=True)
        diff_ratios = {}
        pdf_bytes = b"".join(response.streaming_content)
        pages = pdf2image.convert_from_bytes(pdf_bytes, 200)
        for i, page in enumerate(pages):
            page_name = f"page-{i:0>3}"
            expected_path = os.path.join(self.data_dir, f"{page_name}.expected.png")
            generated_path = os.path.join(self.data_dir, f"{page_name}.generated.png")
            diff_path = os.path.join(self.data_dir, f"{page_name}.result.png")

            if UPDATE_EXPECTED_IMAGES:
                page.save(expected_path, "PNG")
            page.save(generated_path, "PNG")

            diff_ratios[page_name] = diffimg.diff(
                generated_path,
                expected_path,
                diff_img_file=diff_path,
            )

        # We do not tolerate the slighest rendering difference. At some point we may need to implement
        # support for masks (areas that are not compared) to allow negligible rendering differences,
        # e.g. for QGIS updates.
        differences = []
        for name, ratio in diff_ratios.items():
            if ratio:
                differences.append(f"{name}: {ratio*100:.2f}%")
        if differences:
            differences_txt = "\n".join(differences)
            raise AssertionError(
                f"The following rendering differences were detected:\n{differences_txt}"
            )

    def test_attach_pdf(self):
        """Test attachment of PDF to permit request through the form"""

        # Ensure we have no document
        self.assertEqual(
            self.permit_request.permitrequestcomplementarydocument_set.count(), 0
        )

        # Get the form
        self.client.force_login(self.user)
        url = reverse(
            "permits:permit_request_detail",
            kwargs={"permit_request_id": self.permit_request.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Post the form
        post_data = {
            "form-INITIAL_FORMS": "0",
            "form-TOTAL_FORMS": "1",
            "form-0-generate_from_model": f"{self.works_object_type.pk}/{self.report.pk}/{self.doc_type.pk}",
            "form-0-document": "",
            "form-0-description": "my document",
            "form-0-status": "0",
            "form-0-authorised_departments": f"{self.dept.pk}",
            "form-0-document_type": "",
            "form-0-parent_1": "",
            "action": "complementary_documents",
        }
        response = self.client.post(url, data=post_data, follow=True)
        # open("output.html", "wb").write(response.content)  # help debugging
        self.assertContains(
            response,
            f"Les documents ont bien été ajoutés à la demande #{self.permit_request.pk}.",
        )
        self.assertEqual(response.status_code, 200)

        # Ensure a document was added
        self.assertEqual(
            self.permit_request.permitrequestcomplementarydocument_set.count(), 1
        )
