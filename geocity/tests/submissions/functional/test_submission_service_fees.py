from datetime import timedelta

from django.contrib.auth.models import Permission
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from djmoney.money import Money

from geocity.apps.submissions import models as submissions_models
from geocity.apps.submissions.models import Submission, SubmissionValidation
from geocity.tests import factories
from geocity.tests.utils import LoggedInSecretariatMixin, get_parser
from geocity.apps.submissions.payments.models import ServicesFees, ServicesFeesType


class SubmissionServiceFeesTestCase(LoggedInSecretariatMixin, TestCase):

    def setUp(self):
        self.untrusted_user = factories.UserFactory()
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permit_department.administrative_entity
        )

        self.administrative_entity.save()
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        self.first_entity_validator_group = factories.ValidatorGroupFactory(
            department=self.secretariat_group.permit_department
        )
        self.submission = factories.SubmissionFactory(author=self.untrusted_user)

        self.pilot_service_fee_type = factories.ServicesFeesTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Analyse du dossier",
            fix_price = Money("10", "CHF"),
            is_visible_by_validator=False,
        )

        self.validator_service_fee_type = factories.ServicesFeesTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Analyse du dossier",
            fix_price = Money("10", "CHF"),
            is_visible_by_validator=True,
        )



    def test_unstrusted_user_cannot_create_pilot_service_fee(self):

        url = reverse(
                    "submissions:create_submission_service_fees",
                    kwargs={"submission_id": self.submission.pk},
                )
        response = self.client.post(
                f'{url}?action=create&mode=hourly_rate',
                data={
                    "permit_department": self.secretariat_group.permit_department,
                    "services_fees_type": self.pilot_service_fee_type,
                    "time_spent_on_task": timedelta(hours=8),
                },
        )

        self.assertEqual(response.status_code, 403)



    def test_pilot_user_can_create_pilot_service_fee(self):

        initial_service_fees_count = ServicesFees.objects.count()

        self.client.login(username=self.user.username, password=password)

        url = reverse(
                    "submissions:create_submission_service_fees",
                    kwargs={"submission_id": self.submission.pk},
                )

        self.client.post(
                f'{url}?action=create&mode=hourly_rate',
                data={
                    "permit_department": self.secretariat_group.permit_department,
                    "services_fees_type": self.pilot_service_fee_type,
                    "time_spent_on_task": timedelta(hours=8),
                },
        )

        after_create_service_fees_count = ServicesFees.objects.count()

        self.assertEqual(
            after_create_service_fees_count - initial_service_fees_count, 0
        )


    def test_validator_cannot_create_pilot_service_fee(self):

        url = reverse(
                    "submissions:create_submission_service_fees",
                    kwargs={"submission_id": self.submission.pk},
                )
        response = self.client.post(
                f'{url}?action=create&mode=hourly_rate',
                data={
                    "permit_department": self.secretariat_group.permit_department,
                    "services_fees_type": self.validator_service_fee_type,
                    "time_spent_on_task": timedelta(hours=8),
                },
        )

        self.assertNotEqual(response.status_code, 200)
 