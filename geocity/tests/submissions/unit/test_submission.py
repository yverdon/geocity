from django.utils import dateformat

from geocity.apps.submissions import models
from geocity.tests import factories
from geocity.tests.geocity_test_case import GeocityTestCase


class PermitRequestTest(GeocityTestCase):
    def test_permit_request_to_csv(self):
        submission = factories.SubmissionFactory()

        status = models.Submission.STATUS_CHOICES[submission.status][1]
        date = dateformat.format(submission.created_at, "d.m.Y H:i")
        expected = f"ID,Date de création,État,Début,Fin,Tarif,Objets et types de demandes,Entité administrative\r\n{submission.id},{date},{status},,"
        self.assertIn(expected, submission.to_csv())
