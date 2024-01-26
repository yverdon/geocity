from datetime import timedelta

from django.test import TestCase
from django.urls import reverse

from geocity.apps.submissions.models import Submission
from geocity.apps.submissions.payments.models import ServiceFee
from geocity.tests import factories
from geocity.tests.utils import LoggedInSecretariatMixin, LoggedInUserMixin, get_parser


class PilotSubmissionServiceFeesTestCase(LoggedInSecretariatMixin, TestCase):
    def setUp(self):

        super().setUp()

        self.normal_user = factories.UserFactory()
        self.submission_normal_user = factories.SubmissionFactory(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
        )

        self.pilot_service_fee_type_hourly = factories.ServiceFeeTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Hourly Rate",
            fix_price=None,
            is_visible_by_validator=False,
        )

        self.pilot_service_fee_type_fix_price = factories.ServiceFeeTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Fix Price",
            fix_price=452,
            is_visible_by_validator=False,
        )

        self.test_service_fee_hourly = factories.ServiceFeeFactory(
            time_spent_on_task=timedelta(minutes=60),
            service_fee_type=self.pilot_service_fee_type_hourly,
            submission=self.submission_normal_user,
        )

        self.test_service_fee_fix_price = factories.ServiceFeeFactory(
            monetary_amount=255,
            service_fee_type=self.pilot_service_fee_type_fix_price,
            submission=self.submission_normal_user,
        )

    def test_pilot_user_can_create_pilot_service_fee_hourly(self):

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission_normal_user.pk},
        )
        url = f"{url}?action=create&mode=hourly_rate"

        response = self.client.post(
            url,
            data={
                "service_fee_type": self.pilot_service_fee_type_hourly.pk,
                "provided_by": self.user.pk,
                "provided_at": "23.01.2024",
                "time_spent_on_task": 59712,
                "save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        is_fee_saved = ServiceFee.objects.filter(
            time_spent_on_task=timedelta(minutes=59712)
        ).exists()

        self.assertEqual(is_fee_saved, True)

    def test_pilot_user_can_create_pilot_service_fee_fix_price(self):

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission_normal_user.pk},
        )
        url = f"{url}?action=create&mode=fix_price"

        response = self.client.post(
            url,
            data={
                "service_fee_type": self.pilot_service_fee_type_fix_price.pk,
                "provided_by": self.user.pk,
                "provided_at": "23.01.2024",
                "monetary_amount": self.pilot_service_fee_type_fix_price.fix_price,
                "save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        is_fee_saved = ServiceFee.objects.filter(
            monetary_amount=self.pilot_service_fee_type_fix_price.fix_price
        ).exists()

        self.assertEqual(is_fee_saved, True)

    def test_pilot_user_can_update_pilot_service_fee_hourly(self):

        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": self.test_service_fee_hourly.pk,
            },
        )
        url = f"{url}?action=update&mode=hourly_rate"

        new_time_spent_on_task = timedelta(minutes=55)
        response = self.client.post(
            url,
            data={
                "service_fee_type": self.pilot_service_fee_type_hourly.pk,
                "provided_by": self.user.pk,
                "provided_at": "23.01.2024",
                "time_spent_on_task": 55,
                "save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        updated_fee = ServiceFee.objects.get(pk=self.test_service_fee_hourly.pk)

        self.assertEqual(
            updated_fee.time_spent_on_task.total_seconds(),
            new_time_spent_on_task.total_seconds(),
        )

    def test_pilot_user_can_update_pilot_service_fee_fix_price(self):

        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": self.test_service_fee_fix_price.pk,
            },
        )
        url = f"{url}?action=update&mode=fix_price"

        new_monetary_amount = 66
        response = self.client.post(
            url,
            data={
                "service_fee_type": self.pilot_service_fee_type_fix_price.pk,
                "provided_by": self.user.pk,
                "provided_at": "23.01.2024",
                "monetary_amount": new_monetary_amount,
                "save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        updated_fee = ServiceFee.objects.get(pk=self.test_service_fee_fix_price.pk)

        self.assertEqual(updated_fee.monetary_amount, new_monetary_amount)

    def test_pilot_user_can_delete_service_fee(self):

        service_fee = factories.ServiceFeeFactory(
            time_spent_on_task=timedelta(minutes=60),
            service_fee_type=self.pilot_service_fee_type_hourly,
            submission=self.submission_normal_user,
        )
        service_fee.refresh_from_db()

        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": service_fee.pk,
            },
        )
        url = f"{url}?action=delete"

        response = self.client.post(
            url,
            data={"confirm": "Confirm"},
        )

        self.assertEqual(response.status_code, 302)

        is_fee_deleted = not ServiceFee.objects.filter(pk=service_fee.pk).exists()

        self.assertEqual(is_fee_deleted, True)

    # IMPORTANT: this ensures that pilot don't have access to whole user entries
    def test_pilot_only_sees_users_in_provided_by_dropdown_that_are_allowed_for_display(
        self,
    ):

        # create additional pilot users in the same group
        pilot_user_2 = factories.SecretariatUserFactory(groups=self.user.groups.all())
        validator_user = factories.ValidatorUserFactory(groups=self.user.groups.all())
        untrusted_user = factories.UserFactory()

        other_group = factories.GroupFactory()
        pilot_user_not_in_same_entity = factories.SecretariatUserFactory(
            groups=[other_group]
        )

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission_normal_user.pk},
        )
        url = f"{url}?action=create&mode=hourly_rate"

        response = self.client.get(
            url,
        )

        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)

        select_provided_by = get_parser(str(parser.select("#id_provided_by")))

        # Assert correct options are displayed
        self.assertIn(self.user.username, str(select_provided_by))
        self.assertIn(pilot_user_2.username, str(select_provided_by))
        self.assertIn(validator_user.username, str(select_provided_by))

        # Assert default select user is the current user
        select_user = select_provided_by.select_one("option:checked")
        self.assertEqual(self.user.pk, int(select_user["value"]))

        # Assert untrusted user not in options
        self.assertNotIn(untrusted_user.username, str(select_provided_by))
        # Assert pilot in other user not in options
        self.assertNotIn(
            pilot_user_not_in_same_entity.username, str(select_provided_by)
        )


class UntrustedSubmissionServiceFeesTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):

        super().setUp()

        self.administrative_entity = factories.AdministrativeEntityFactory()
        self.submission_normal_user = factories.SubmissionFactory(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.user,
        )

        self.pilot_service_fee_type_hourly = factories.ServiceFeeTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Hourly Rate",
            fix_price=None,
            is_visible_by_validator=False,
        )

    def test_unstrusted_user_cannot_create_pilot_service_fee(self):

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission_normal_user.pk},
        )
        url = f"{url}?action=create&mode=hourly_rate"

        response = self.client.post(
            url,
            data={
                "service_fee_type": self.pilot_service_fee_type_hourly.pk,
                "provided_by": self.user.pk,
                "provided_at": "23.01.2024",
                "time_spent_on_task": 87453,
                "save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        is_fee_saved = ServiceFee.objects.filter(
            time_spent_on_task=timedelta(minutes=87453)
        ).exists()

        self.assertEqual(is_fee_saved, False)

    def test_untrusted_user_cannot_delete_service_fee(self):

        service_fee = factories.ServiceFeeFactory(
            time_spent_on_task=timedelta(minutes=60),
            service_fee_type=self.pilot_service_fee_type_hourly,
            submission=self.submission_normal_user,
        )
        service_fee.refresh_from_db()
        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": service_fee.pk,
            },
        )
        url = f"{url}?action=delete"

        response = self.client.post(
            url,
            data={"confirm": "Confirm"},
        )

        self.assertEqual(response.status_code, 302)

        is_fee_still_existing = ServiceFee.objects.filter(pk=service_fee.pk).exists()

        self.assertEqual(is_fee_still_existing, True)


class ValidatorSubmissionServiceFeesTestCase(TestCase):
    def setUp(self):

        super().setUp()

        self.administrative_entity = factories.AdministrativeEntityFactory()
        validator_department = factories.PermitDepartmentFactory(
            administrative_entity=self.administrative_entity, is_validator=True
        )
        validator_group = factories.ValidatorGroupFactory(
            department=validator_department
        )
        self.validator_user = factories.ValidatorUserFactory(
            groups=[validator_department.group, validator_group]
        )
        self.normal_user = factories.UserFactory()

        self.submission_normal_user = factories.SubmissionFactory(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
        )

        self.validator_service_fee_type = factories.ServiceFeeTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Hourly Rate Validator",
            fix_price=None,
            is_visible_by_validator=True,
        )

        self.pilot_service_fee_type = factories.ServiceFeeTypesFactory(
            administrative_entity=self.administrative_entity,
            name="Hourly Rate Pilot",
            fix_price=None,
            is_visible_by_validator=False,
        )

    def test_validator_user_can_create_validator_service_fee_for_authorized_service_fee_type(
        self,
    ):

        self.client.login(username=self.validator_user.username, password="password")

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission_normal_user.pk},
        )
        url = f"{url}?action=create&mode=hourly_rate"

        response = self.client.post(
            url,
            data={
                "service_fee_type": self.validator_service_fee_type.pk,
                "provided_by": self.validator_user.pk,
                "provided_at": "23.01.2024",
                "time_spent_on_task": 84752,
                "save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        is_fee_saved = ServiceFee.objects.filter(
            time_spent_on_task=timedelta(minutes=84752)
        ).exists()

        self.assertEqual(is_fee_saved, True)

    def test_validator_user_cannot_create_pilote_service_fee(
        self,
    ):

        self.client.login(username=self.validator_user.username, password="password")

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission_normal_user.pk},
        )
        url = f"{url}?action=create&mode=hourly_rate"
        response = self.client.post(
            url,
            data={
                "service_fee_type": self.pilot_service_fee_type.pk,
                "provided_by": self.validator_user.pk,
                "provided_at": "23.01.2024",
                "time_spent_on_task": 87265,
                "save": "Save",
            },
        )

        is_fee_saved = ServiceFee.objects.filter(
            time_spent_on_task=timedelta(minutes=87265)
        ).exists()

        self.assertEqual(is_fee_saved, False)

    def test_validator_can_update_validator_service_fee(self):

        service_fee = factories.ServiceFeeFactory(
            time_spent_on_task=timedelta(minutes=60),
            service_fee_type=self.validator_service_fee_type,
            submission=self.submission_normal_user,
        )

        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": service_fee.pk,
            },
        )
        url = f"{url}?action=update&mode=hourly_rate"

        new_time_spent_on_task = timedelta(minutes=55)
        self.client.login(username=self.validator_user.username, password="password")

        response = self.client.post(
            url,
            data={
                "service_fee_type": self.validator_service_fee_type.pk,
                "provided_by": self.validator_user.pk,
                "provided_at": "23.01.2024",
                "time_spent_on_task": 55,
                "save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        updated_fee = ServiceFee.objects.get(pk=service_fee.pk)

        self.assertEqual(
            updated_fee.time_spent_on_task.total_seconds(),
            new_time_spent_on_task.total_seconds(),
        )

    def test_validator_cannot_update_pilot_service_fee(self):

        service_fee = factories.ServiceFeeFactory(
            time_spent_on_task=timedelta(minutes=60),
            service_fee_type=self.pilot_service_fee_type,
            submission=self.submission_normal_user,
        )

        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": service_fee.pk,
            },
        )
        url = f"{url}?action=update&mode=hourly_rate"

        new_time_spent_on_task = timedelta(minutes=55)
        self.client.login(username=self.validator_user.username, password="password")

        response = self.client.post(
            url,
            data={
                "service_fee_type": self.pilot_service_fee_type.pk,
                "provided_by": self.validator_user.pk,
                "provided_at": "23.01.2024",
                "time_spent_on_task": 55,
                "save": "Save",
            },
        )

        updated_fee = ServiceFee.objects.get(pk=service_fee.pk)

        self.assertNotEqual(
            updated_fee.time_spent_on_task.total_seconds(),
            new_time_spent_on_task.total_seconds(),
        )

    def test_validator_user_can_delete_service_fee_visible_by_validator(self):

        service_fee = factories.ServiceFeeFactory(
            time_spent_on_task=timedelta(minutes=60),
            service_fee_type=self.validator_service_fee_type,
            submission=self.submission_normal_user,
        )
        service_fee.refresh_from_db()
        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": service_fee.pk,
            },
        )
        url = f"{url}?action=delete"

        self.client.login(username=self.validator_user.username, password="password")

        response = self.client.post(
            url,
            data={"confirm": "Confirm"},
        )
        self.assertEqual(response.status_code, 302)

        is_fee_still_existing = ServiceFee.objects.filter(pk=service_fee.pk).exists()

        self.assertEqual(is_fee_still_existing, False)

    def test_validator_user_cannot_delete_service_fee_not_visible_by_validator(self):

        service_fee = factories.ServiceFeeFactory(
            time_spent_on_task=timedelta(minutes=60),
            service_fee_type=self.pilot_service_fee_type,
            submission=self.submission_normal_user,
        )
        service_fee.refresh_from_db()
        url = reverse(
            "submissions:submission_service_fees",
            kwargs={
                "submission_id": self.submission_normal_user.pk,
                "service_fee_id": service_fee.pk,
            },
        )
        url = f"{url}?action=delete"

        self.client.login(username=self.validator_user.username, password="password")

        response = self.client.post(
            url,
            data={"confirm": "Confirm"},
        )
        self.assertEqual(response.status_code, 404)

        is_fee_still_existing = ServiceFee.objects.filter(pk=service_fee.pk).exists()

        self.assertEqual(is_fee_still_existing, True)

    # IMPORTANT: this ensures that validator has not access to users
    def test_provided_by_select_only_contains_himself(
        self,
    ):

        url = reverse(
            "submissions:create_submission_service_fees",
            kwargs={"submission_id": self.submission_normal_user.pk},
        )
        url = f"{url}?action=create&mode=hourly_rate"

        self.client.login(username=self.validator_user.username, password="password")

        response = self.client.get(
            url,
        )

        self.assertEqual(response.status_code, 200)

        parser = get_parser(response.content)

        select_provided_by = get_parser(str(parser.select("#id_provided_by")))
        options = select_provided_by.findAll("option")
        self.assertEqual(2, len(options))
