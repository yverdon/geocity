from django.urls import reverse

from reports.models import (
    SectionAmendProperty,
    SectionAuthor,
    SectionContact,
    SectionDetail,
    SectionHorizontalRule,
    SectionMap,
    SectionParagraph,
    SectionPlanning,
    SectionStatus,
    SectionValidation,
)

from .base import ReportsTestsBase


class ReportsTests(ReportsTestsBase):
    """Test report workflows"""

    def test_pdf_preview(self):
        """Test PDF generation through the reports:permit_request_report view"""

        # Get the PDF
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "reports:permit_request_report_pdf",
                kwargs={
                    "permit_request_id": self.permit_request.pk,
                    "work_object_type_id": self.works_object_type.pk,
                    "report_id": self.report.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 200)

        # Compare the generated PDF against the expected images
        pdf_bytes = b"".join(response.streaming_content)
        self.assert_pdf_is_as_expected(pdf_bytes)

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

    def test_block_gallery(self):
        """Test rendering for all blocks"""

        # Clean all blocks
        for section in self.report.sections.all():
            section.delete()

        # Add one block of each type
        sections_config = {
            SectionMap: {},
            SectionParagraph: {
                "title": "A basic paragraph",
                "content": "<p>A paragraph <u>with</u> <b style='color: red;'>basic</b> <i>styling</i></p>",
            },
            SectionContact: {},
            SectionAuthor: {},
            SectionDetail: {},
            SectionPlanning: {},
            # SectionFiles: {}, # FIXME: TemplateDoesNotExist: sectionfiles.html
            SectionValidation: {},
            SectionAmendProperty: {},
            SectionStatus: {},
        }

        for i, (SectionKlass, kwargs) in enumerate(sections_config.items()):
            SectionKlass.objects.create(
                order=i * 10,
                report=self.report,
                **kwargs,
            )
            SectionHorizontalRule.objects.create(
                order=i * 10 + 1,
                report=self.report,
            )

        # Get the PDF
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "reports:permit_request_report_pdf",
                kwargs={
                    "permit_request_id": self.permit_request.pk,
                    "work_object_type_id": self.works_object_type.pk,
                    "report_id": self.report.pk,
                },
            )
        )
        pdf_bytes = b"".join(response.streaming_content)
        self.assert_pdf_is_as_expected(pdf_bytes)
