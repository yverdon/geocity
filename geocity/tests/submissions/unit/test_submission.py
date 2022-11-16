from babel.dates import format_datetime
from pytz import timezone

from geocity.apps.submissions import models
from geocity.tests import factories
from geocity.tests.geocity_test_case import GeocityTestCase


class PermitRequestTest(GeocityTestCase):
    def test_permit_request_to_csv(self):
        submission = factories.SubmissionFactory()

        status = models.Submission.STATUS_CHOICES[submission.status][1]
        date = format_datetime(
            submission.created_at,
            "dd.MM.yyyy HH:mm",
            tzinfo=timezone("GMT"),
            locale="fr_CH",
        )
        expected = f"ID,Date de création,État,Début,Fin,Objets et types de demandes,Entité administrative\r\n{submission.id},{date},{status},,"
        self.assertIn(expected, submission.to_csv())
