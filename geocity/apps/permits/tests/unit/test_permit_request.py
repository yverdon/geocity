from babel.dates import format_datetime
from permits import models
from pytz import timezone

from .. import factories
from ..geocity_test_case import GeocityTestCase


class PermitRequestTest(GeocityTestCase):
    def test_permit_request_to_csv(self):
        permit_request = factories.PermitRequestFactory()

        status = models.PermitRequest.STATUS_CHOICES[permit_request.status][1]
        date = format_datetime(
            permit_request.created_at,
            "dd.MM.yyyy HH:mm",
            tzinfo=timezone("GMT"),
            locale="fr_CH",
        )
        expected = f"ID,Date de création,État,Début,Fin,Objets et types de demandes,Entité administrative\r\n{permit_request.id},{date},{status},,"
        self.assertIn(expected, permit_request.to_csv())
