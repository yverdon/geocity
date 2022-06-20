import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from permits.models import PermitRequest
from permits.tests import factories
from reports.models import Report, ReportLayout, SectionMap, SectionParagraph

from .models import Report, ReportLayout, SectionMap, SectionParagraph


# TODO: expand this
class ReportsIntegrationTests(TestCase):
    """Integration tests for reports"""

    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create(username="superuser")

    def test_pdf_generation(self):
        # TODO: this test cannot fully work as expected with the current infra, because
        # the pdf/qgis container call the regular webserver running in the web container
        # instead of the test server, meaning it does not use test settings and has no
        # access to databsae changes because they are in a transaction.
        # We probably need to use LiveServerTestCase instead, and run tests with `run`
        # instead of `exec`.
        # Currently, the test passes, but the QGIS map is not rendered.

        self.client.force_login(self.superuser)

        group = factories.GroupFactory(
            name="Group",
        )
        dept = factories.PermitDepartmentFactory(
            group=group,
            is_backoffice=True,
        )
        permit_request = factories.PermitRequestFactory(
            # author=self.superuser.permitauthor,
            status=PermitRequest.STATUS_APPROVED,
            administrative_entity=dept.administrative_entity,
        )

        parent_doc_type = factories.ParentComplementaryDocumentTypeFactory()
        doc_type = factories.ChildComplementaryDocumentTypeFactory(
            parent=parent_doc_type,
        )
        layout = ReportLayout.objects.create(
            name="test",
        )
        report = Report.objects.create(
            name="test",
            layout=layout,
            type=doc_type,
        )
        SectionParagraph.objects.create(
            title="title",
            content="content",
            report=report,
        )
        section_map = SectionMap.objects.create(
            qgis_project_file="invalid",
            qgis_print_template_name="a4",
            report=report,
        )
        qgis_template_project_path = os.path.join(
            os.path.dirname(__file__), "static", "reports", "report-template.qgs"
        )
        qgis_template_project = open(qgis_template_project_path, "rb")
        section_map.qgis_project_file.save(
            "report-template.qgs", File(qgis_template_project), save=True
        )

        response = self.client.get(
            reverse(
                "reports:permit_request_report",
                kwargs={"permit_request_id": permit_request.pk, "report_id": report.pk},
            )
        )

        # Uncomment to see the PDF
        # f = open("test.pdf", "wb")
        # for chunk in response.streaming_content:
        #     f.write(chunk)
        # f.close()

        # TODO: see if we can somehow test PDF appearance

        self.assertEqual(response.status_code, 200)
