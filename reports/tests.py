from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from permits.models import PermitRequest
from permits.tests import factories
from reports.models import Report, ReportLayout

from .models import Report, ReportLayout


# TODO: expand this
class ReportsIntegrationTests(TestCase):
    """Integration tests for reports"""

    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create(username="superuser")

    def test_pdf_generation(self):
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
        # TODO: include some map blocks here to ensure it works

        response = self.client.get(
            reverse(
                "reports:permit_request_report",
                kwargs={"permit_request_id": permit_request.pk, "report_id": report.pk},
            )
        )

        # TODO: see if we can somehow test PDF appearance

        self.assertEqual(response.status_code, 200)