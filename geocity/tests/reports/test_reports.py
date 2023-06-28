from django.contrib.staticfiles import finders
from django.core.files import File
from django.urls import reverse

from geocity.apps.reports.models import (
    HeaderFooterDateTime,
    HeaderFooterLogo,
    HeaderFooterPageNumber,
    HeaderFooterParagraph,
    SectionAmendProperty,
    SectionAuthor,
    SectionContact,
    SectionCreditor,
    SectionDetail,
    SectionHorizontalRule,
    SectionMap,
    SectionParagraph,
    SectionPlanning,
    SectionRecipient,
    SectionStatus,
    SectionValidation,
)

from .base import ReportsTestsBase


class ReportsTests(ReportsTestsBase):
    """Test report workflows"""

    def test_pdf_preview(self):
        """Test PDF generation through the reports:submission_report view"""

        # Get the PDF
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "reports:submission_report_pdf",
                kwargs={
                    "submission_id": self.submission.pk,
                    "form_id": self.form.pk,
                    "report_id": self.report.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 200)

        # Compare the generated PDF against the expected images
        pdf_bytes = b"".join(response.streaming_content)
        # open("output.pdf", "wb").write(pdf_bytes)  # help debugging
        self.assert_pdf_is_as_expected(pdf_bytes)

    def test_attach_pdf(self):
        """Test attachment of PDF to submission through the form"""

        # Ensure we have no document
        self.assertEqual(self.submission.complementary_documents.count(), 0)

        # Get the form
        self.client.force_login(self.user)
        url = reverse(
            "submissions:submission_detail",
            kwargs={"submission_id": self.submission.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Post the form
        post_data = {
            "form-INITIAL_FORMS": "0",
            "form-TOTAL_FORMS": "1",
            "form-0-generate_from_model": f"{self.form.pk}/{self.report.pk}/{self.doc_type.pk}/0",
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
            f"Les documents ont bien été ajoutés à la demande #{self.submission.pk}.",
        )
        self.assertEqual(response.status_code, 200)

        # Ensure a document was added
        self.assertEqual(self.submission.complementary_documents.count(), 1)

    def test_block_gallery(self):
        """Test rendering for all blocks"""

        # Clean all blocks
        for section in self.report.sections.all():
            section.delete()

        # Add one block of each type
        sections_config = {
            1: {
                SectionMap: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section map",
                    "title_size": "h1",
                }
            },
            2: {
                SectionParagraph: {
                    # "padding_top": int,
                    "is_new_page": True,
                    "title": "Section paragraph 2",
                    "title_size": "h3",
                    "text_align": "left",
                    "location": "left",
                    "content": """
                    <p>This paragraph has a title h3, is aligned to the left and is located on the left of the page</p>
                    <p>A paragraph <u>with</u> <b style='color: red;'>basic</b> <i>styling</i></p>
                    """,
                }
            },
            3: {
                SectionParagraph: {
                    "padding_top": 10,
                    "is_new_page": False,
                    "title": "Section paragraph 2",
                    "title_size": "h4",
                    "text_align": "right",
                    "location": "right",
                    "content": """
                    <p>This paragraph has a title h4, has a padding top of 10px, is aligned to the right and is located on the right of the page</p>
                    <p>A paragraph <u>with</u> <b style='color: red;'>basic</b> <i>styling</i></p>
                    """,
                }
            },
            4: {
                SectionParagraph: {
                    "padding_top": 20,
                    "is_new_page": False,
                    "title": "Section paragraph 3",
                    "title_size": "h5",
                    "text_align": "center",
                    "location": "content",
                    "content": """
                    <p>This paragraph has a title h5, has a padding top of 20px, is aligned to the center and is located on the center (content) of the page</p>
                    <p>A paragraph <u>with</u> <b style='color: red;'>basic</b> <i>styling</i></p>
                    """,
                }
            },
            5: {
                SectionParagraph: {
                    "padding_top": 30,
                    "is_new_page": False,
                    "title": "Section paragraph 4",
                    "title_size": "h6",
                    "text_align": "justify",
                    "location": "content",
                    "content": """
                    <p>This paragraph has a title h6, has a padding top of 30px, text is justify and is located on the center (content) of the page</p>
                    <p>A paragraph <u>with</u> <b style='color: red;'>basic</b> <i>styling</i></p>
                    """,
                }
            },
            5: {
                SectionContact: {
                    # "padding_top": int,
                    "is_new_page": True,
                    "title": "Section contact",
                    "title_size": "h2",
                }
            },
            6: {
                SectionAuthor: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section author",
                    "title_size": "h2",
                }
            },
            7: {
                SectionDetail: {
                    "padding_top": 20,
                    # "is_new_page": bool,
                    "title": "Section detail style 1 form_name 0",
                    "title_size": "h3",
                    "form_name": 0,
                    "style": 1,
                    "line_height": 20,
                    # "undesired_properties": char,
                }
            },
            8: {
                SectionDetail: {
                    "padding_top": 20,
                    # "is_new_page": bool,
                    "title": "Section detail style 2 form_name 1",
                    "title_size": "h3",
                    "form_name": 1,
                    "style": 2,
                    "line_height": 50,
                    # "undesired_properties": char,
                }
            },
            9: {
                SectionDetail: {
                    "padding_top": 20,
                    # "is_new_page": bool,
                    "title": "Section detail style 2 form_name 2",
                    "title_size": "h3",
                    "form_name": 2,
                    "style": 2,
                    "line_height": 50,
                    # "undesired_properties": char,
                }
            },
            10: {
                SectionDetail: {
                    "padding_top": 20,
                    # "is_new_page": bool,
                    "title": "Section detail style 2 form_name 3",
                    "title_size": "h3",
                    "form_name": 3,
                    "style": 2,
                    "line_height": 50,
                    # "undesired_properties": char,
                }
            },
            11: {
                SectionPlanning: {
                    # "padding_top": int,
                    "is_new_page": True,
                    "title": "Section planning",
                    "title_size": "h3",
                }
            },
            12: {
                SectionValidation: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section validation",
                    "title_size": "h3",
                }
            },
            13: {
                SectionAmendProperty: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section amend property form_name 0",
                    "title_size": "h3",
                    "form_name": 0,
                    # "undesired_properties": string,
                }
            },
            14: {
                SectionAmendProperty: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section amend property form_name 1",
                    "title_size": "h3",
                    "form_name": 1,
                    # "undesired_properties": string,
                }
            },
            15: {
                SectionAmendProperty: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section amend property form_name 2",
                    "title_size": "h3",
                    "form_name": 2,
                    # "undesired_properties": string,
                }
            },
            16: {
                SectionAmendProperty: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section amend property form_name 3",
                    "title_size": "h3",
                    "form_name": 3,
                    # "undesired_properties": string,
                }
            },
            17: {
                SectionStatus: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section status",
                    "title_size": "h3",
                }
            },
            18: {
                SectionCreditor: {
                    # "padding_top": int,
                    # "is_new_page": bool,
                    "title": "Section creditor",
                    "title_size": "h3",
                }
            },
            19: {
                SectionRecipient: {
                    "padding_top": 20,
                    # "is_new_page": bool,
                    "is_recommended": True,
                }
            },
        }

        header_footers_config = {
            1: {
                HeaderFooterPageNumber: {
                    "page": 2,  # Not first page
                    "location": "@bottom-center",
                }
            },
            2: {
                HeaderFooterDateTime: {
                    "page": 1,  # Only first page
                    "location": "@bottom-center",
                }
            },
            3: {
                HeaderFooterParagraph: {
                    "page": 0,  # All pages
                    "location": "@bottom-left",
                    "text_align": "Left",
                    "content": """
                    Place Pestalozzi, CH-1401 Yverdon-les-Bains
Second line
                    """,
                }
            },
            4: {
                HeaderFooterParagraph: {
                    "page": 2,  # Not first page
                    "location": "@bottom-right",
                    "text_align": "Right",
                    "content": """
                    Place Pestalozzi, CH-1401 Yverdon-les-Bains
Second line
                    """,
                }
            },
            5: {
                HeaderFooterLogo: {
                    "page": 1,  # Only first page
                    "location": "@bottom-right-corner",
                    "logo": "report-qr-code.png",
                    "logo_size": 80,
                }
            },
            6: {
                HeaderFooterLogo: {
                    "page": 1,  # Only first page
                    "location": "@top-left",
                    "logo": "report-logo.png",
                    "logo_size": 70,
                }
            },
        }

        for key, section_config in sections_config.items():
            for SectionClass, kwargs in section_config.items():
                SectionClass.objects.create(
                    order=key * 10,
                    report=self.report,
                    **kwargs,
                )
            SectionHorizontalRule.objects.create(
                order=key * 10 + 1,
                report=self.report,
            )

        for key, header_footer_config in header_footers_config.items():
            for HeaderFooterClass, kwargs in header_footer_config.items():
                if HeaderFooterClass == HeaderFooterLogo:
                    file_name = kwargs["logo"]
                    _logo_path = finders.find(f"reports/{file_name}")
                    logo = open(_logo_path, "rb")
                    kwargs.pop("logo")

                    obj = HeaderFooterLogo.objects.create(
                        report=self.report,
                        **kwargs,
                    )

                    obj.logo.save(file_name, File(logo), save=True)
                    obj.save()
                else:
                    HeaderFooterClass.objects.create(
                        report=self.report,
                        **kwargs,
                    )

        # Get the PDF
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "reports:submission_report_pdf",
                kwargs={
                    "submission_id": self.submission.pk,
                    "form_id": self.form.pk,
                    "report_id": self.report.pk,
                },
            )
        )
        pdf_bytes = b"".join(response.streaming_content)
        self.assert_pdf_is_as_expected(pdf_bytes)
