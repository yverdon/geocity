from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from djmoney.money import Money

from geocity.apps.submissions.payments.models import ServicesFees
from geocity.tests import factories
from geocity.tests.utils import LoggedInSecretariatMixin, LoggedInUserMixin


class PilotSubmissionServiceFeesTestCase(LoggedInSecretariatMixin, TestCase):
    def setUp(self):

        super().setUp()

        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permit_department.administrative_entity
        )

        self.administrative_entity.save()
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        self.submission = factories.SubmissionFactory()

        self.pilot_service_fee_type = factories.ServicesFeesTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Analyse du dossier",
            fix_price=Money("10", "CHF"),
            is_visible_by_validator=False,
        )

    def test_pilot_user_can_create_pilot_service_fee(self):

        initial_service_fees_count = ServicesFees.objects.count()

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission.pk},
        )
        url = f"{url}?action=create&mode=hourly_rate"
        response = self.client.get(
            url,
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


class UntrustedSubmissionServiceFeesTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):

        super().setUp()

        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permit_department.administrative_entity
        )
        self.administrative_entity.save()

        self.submission = factories.SubmissionFactory(author=self.user)

        self.service_fee_type = factories.ServicesFeesTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Analyse du dossier",
            fix_price=Money("10", "CHF"),
            is_visible_by_validator=False,
        )

    def test_unstrusted_user_cannot_create_pilot_service_fee(self):

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission.pk},
        )
        response = self.client.post(
            f"{url}?action=create&mode=hourly_rate",
            data={
                "permit_department": self.secretariat_group.permit_department,
                "services_fees_type": self.service_fee_type,
                "time_spent_on_task": timedelta(hours=8),
            },
        )

        self.assertEqual(response.status_code, 403)

    # class ValidatorSubmissionServiceFeesTestCase(LoggedInSecretariatMixin, TestCase):

    # def setUp(self):

    #     self.secretariat_group = factories.SecretariatGroupFactory()
    #     self.administrative_entity = (
    #         self.secretariat_group.permit_department.administrative_entity
    #     )

    #     self.administrative_entity.save()
    #     self.secretariat_user = factories.SecretariatUserFactory(
    #         groups=[self.secretariat_group]
    #     )

    #     self.first_entity_validator_group = factories.ValidatorGroupFactory(
    #         department=self.secretariat_group.permit_department
    #     )
    #     self.submission = factories.SubmissionFactory(author=self.untrusted_user)

    #     self.pilot_service_fee_type = factories.ServicesFeesTypesFactory(
    #         administrative_entity=self.administrative_entity,
    #         name="Analyse du dossier",
    #         fix_price = Money("10", "CHF"),
    #         is_visible_by_validator=False,
    #     )

    #     self.validator_service_fee_type = factories.ServicesFeesTypesFactory(
    #         administrative_entity=self.administrative_entity,
    #         name="Analyse du dossier",
    #         fix_price = Money("10", "CHF"),
    #         is_visible_by_validator=True,
    #     )

    # def test_validator_cannot_create_pilot_service_fee(self):

    #     url = reverse(
    #                 "submissions:create_submission_service_fees",
    #                 kwargs={"submission_id": self.submission.pk},
    #             )
    #     response = self.client.post(
    #             f'{url}?action=create&mode=hourly_rate',
    #             data={
    #                 "permit_department": self.secretariat_group.permit_department,
    #                 "services_fees_type": self.validator_service_fee_type,
    #                 "time_spent_on_task": timedelta(hours=8),
    #             },
    #     )

    #     self.assertNotEqual(response.status_code, 200)
