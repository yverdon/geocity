from django.contrib.auth.models import Permission
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from geocity.apps.submissions import models as submissions_models
from geocity.apps.submissions.models import Submission, SubmissionValidation
from geocity.tests import factories
from geocity.tests.utils import LoggedInSecretariatMixin, get_parser


class SubmissionValidationRequestTestCase(LoggedInSecretariatMixin, TestCase):
    def test_secretariat_can_request_validation(self):
        validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity
        )
        validator_departments = [
            group.permit_department.pk for group in validator_groups
        ]

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "departments": validator_departments,
                "action": submissions_models.ACTION_REQUEST_VALIDATION,
            },
        )

        submission.refresh_from_db()

        self.assertEqual(
            submission.status, submissions_models.Submission.STATUS_AWAITING_VALIDATION
        )
        self.assertEqual(
            set(submission.validations.values_list("department", flat=True)),
            set(validator_departments),
        )

    def test_secretariat_cannot_request_validation_for_already_validated_submission(
        self,
    ):
        validator_group = factories.ValidatorGroupFactory(
            department__administrative_entity=self.administrative_entity
        )

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "departments": [validator_group.permit_department.pk],
                "action": submissions_models.ACTION_REQUEST_VALIDATION,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_default_departments_are_checked(self):
        default_validator_groups = factories.ValidatorGroupFactory.create_batch(
            2,
            department__administrative_entity=self.administrative_entity,
            department__is_default_validator=True,
        )
        non_default_validator_group = factories.ValidatorGroupFactory(
            department__administrative_entity=self.administrative_entity
        )

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

        parser = get_parser(response.content)
        inputs = {
            int(input_["value"]): input_.get("checked") is not None
            for input_ in parser.select('input[name="departments"]')
        }

        self.assertDictEqual(
            inputs,
            {
                **{
                    group.permit_department.id: True
                    for group in default_validator_groups
                },
                **{non_default_validator_group.permit_department.id: False},
            },
        )

    def test_validation_request_sends_mail_to_selected_validators(self):
        validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity
        )
        validator_user = factories.ValidatorUserFactory(
            groups=[validator_groups[0]], email="validator@geocity.ch"
        )
        factories.ValidatorUserFactory(groups=[validator_groups[1]])

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "departments": [validator_groups[0].permit_department.pk],
                "action": submissions_models.ACTION_REQUEST_VALIDATION,
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator_user.email])


class SubmissionValidationTestCase(TestCase):
    def test_validator_can_see_assigned_submissions(self):
        validation = factories.SubmissionValidationFactory()
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )
        factories.SubmissionGeoTimeFactory(submission=validation.submission)

        self.client.login(username=validator.username, password="password")

        response = self.client.get(reverse("submissions:submissions_list"))

        self.assertEqual(
            list(response.context["submission_list"]), [validation.submission]
        )

    def test_validator_can_validate_assigned_submissions(self):
        validation = factories.SubmissionValidationFactory()
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=validator.username, password="password")

        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={
                "action": submissions_models.ACTION_VALIDATE,
                "validation_status": submissions_models.SubmissionValidation.STATUS_APPROVED,
            },
        )

        validation.refresh_from_db()

        self.assertEqual(
            validation.validation_status,
            submissions_models.SubmissionValidation.STATUS_APPROVED,
        )

    def test_validator_cannot_validate_non_assigned_submissions(self):
        validation = factories.SubmissionValidationFactory()
        factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )
        validator = factories.ValidatorUserFactory()

        self.client.login(username=validator.username, password="password")

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={
                "action": submissions_models.ACTION_VALIDATE,
                "validation_status": submissions_models.SubmissionValidation.STATUS_APPROVED,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_validator_can_see_for_validators_amend_field(
        self,
    ):
        validation = factories.SubmissionValidationFactory()
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )
        submission = validation.submission
        factories.SubmissionGeoTimeFactory(submission=submission)

        self.client.login(username=validator.username, password="password")

        fields_quantity = 3
        selected_form = factories.SelectedFormFactory(submission=submission)
        fields_private = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, is_visible_by_author=False, is_visible_by_validators=False
        )
        fields_private_validators = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity,
            is_visible_by_author=False,
            is_visible_by_validators=True,
        )

        fields = fields_private + fields_private_validators

        data = {
            "action": submissions_models.ACTION_AMEND,
            "status": submissions_models.Submission.STATUS_PROCESSING,
        }
        forms_pk = submission.forms.first().pk
        for field in fields:
            field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=field,
                form=selected_form,
            )
            data[f"{forms_pk}_{field.pk}"] = "I am a new field value, I am alive!"

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

        parser = get_parser(response.content)
        # check that the 3 fields are visible by validator and 3 are hidden
        self.assertEqual(len(parser.select(".amend-property")), 3)

    def test_secretariat_can_send_validation_reminders(self):
        group = factories.SecretariatGroupFactory()
        administrative_entity = group.permit_department.administrative_entity
        secretariat = factories.SecretariatUserFactory(groups=[group])

        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=administrative_entity
        )
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()],
            email="validator@geocity.ch",
        )

        self.client.login(username=secretariat.username, password="password")

        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={
                "action": submissions_models.ACTION_POKE,
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator.email])

    def test_secretary_email_is_sent_when_submission_is_validated(self):
        validation = factories.SubmissionValidationFactory()
        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        factories.SecretariatUserFactory(
            groups=[secretary_group], email="secretary@geocity.ch"
        )
        validation.submission.administrative_entity.departments.set([department])
        form = factories.FormFactory()
        form_name = form.name
        validation.submission.forms.set([form])

        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()],
        )

        self.client.login(username=validator.username, password="password")

        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={
                "action": submissions_models.ACTION_VALIDATE,
                "validation_status": submissions_models.SubmissionValidation.STATUS_APPROVED,
            },
        )

        validation.refresh_from_db()

        self.assertEqual(
            validation.validation_status,
            submissions_models.SubmissionValidation.STATUS_APPROVED,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["secretary@geocity.ch"])
        self.assertEqual(
            mail.outbox[0].subject,
            "{} ({})".format(
                "Les services chargés de la validation d'une demande ont donné leur préavis",
                form_name,
            ),
        )
        self.assertIn(
            "Les services chargés de la validation d'une demande ont donné leur préavis",
            mail.outbox[0].message().as_string(),
        )


class SubmissionValidationOnDetailsTestCase(TestCase):
    def setUp(self):
        super().setUp()
        """Generate validations and users
        """

        self.edit_submission_validations = Permission.objects.get(
            codename="edit_submission_validations",
            content_type__app_label="submissions",
        )

        # Create submission
        self.submission = factories.SubmissionFactory(
            status=Submission.STATUS_PROCESSING
        )

        # Create all cases of validations
        self.validation_1 = factories.SubmissionValidationFactory(
            comment_is_visible_by_author=True,
            submission=self.submission,
            comment="Requested and visible",
            validation_status=SubmissionValidation.STATUS_REQUESTED,
        )
        self.validation_2 = factories.SubmissionValidationFactory(
            comment_is_visible_by_author=False,
            submission=self.submission,
            comment="Approved and hidden",
            validation_status=SubmissionValidation.STATUS_APPROVED,
        )
        self.validation_3 = factories.SubmissionValidationFactory(
            comment_is_visible_by_author=True,
            submission=self.submission,
            comment="Approved and visible",
            validation_status=SubmissionValidation.STATUS_APPROVED,
        )
        self.validation_4 = factories.SubmissionValidationFactory(
            comment_is_visible_by_author=True,
            submission=self.submission,
            comment="Rejected and visible",
            validation_status=SubmissionValidation.STATUS_REJECTED,
        )

        # Create pilot group
        self.pilot_group = factories.GroupFactory(name="pilot")

        # Create department
        department = factories.PermitDepartmentFactory(
            group=self.pilot_group, is_backoffice=True
        )

        # Create pilot user
        self.pilot = factories.SecretariatUserFactory(
            groups=[self.pilot_group], email="secretary@geocity.ch"
        )

        # Create validator
        self.validator = factories.ValidatorUserFactory(
            groups=[
                self.validation_1.department.group,
                factories.ValidatorGroupFactory(),
            ],
        )

        # Define author
        self.author = self.submission.author

        # Set department for submission.administrative_entity
        self.submission.administrative_entity.departments.set([department])

        # Create used form
        self.form = factories.FormFactory()

        # Assign form to submission
        self.submission.forms.set([self.form])

    def test_author_can_only_see_visible_validation_comment(self):
        self.client.login(username=self.author.username, password="password")

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
        )

        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        # Button should not appear
        self.assertNotIn("Modifier les validations", content)

        # Check comment and status for comment_is_visible_by_author=True appears
        # Check comment and status for comment_is_visible_by_author=False dont appears
        self.assertIn(self.validation_1.comment, content)
        self.assertIn(self.validation_3.comment, content)
        self.assertIn(self.validation_4.comment, content)
        self.assertNotIn(self.validation_2.comment, content)

        self.assertIn("fa fa-check-circle", content)
        self.assertIn("fa fa-clock-o", content)
        self.assertIn("fa fa-times-circle", content)

        # Check comment_is_visible_by_author never appears
        self.assertNotIn("Commentaire visible par l'auteur de la demande", content)

    def test_pilot_can_edit_validation_only_with_perms(self):
        self.client.login(username=self.pilot.username, password="password")

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
        )

        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        # Button should not appear
        self.assertNotIn("Modifier les validations", content)

        # Can see all comments
        self.assertIn(self.validation_1.comment, content)
        self.assertIn(self.validation_2.comment, content)
        self.assertIn(self.validation_3.comment, content)
        self.assertIn(self.validation_4.comment, content)

        # See all icons
        self.assertIn("fa fa-check-circle", content)
        self.assertIn("fa fa-clock-o", content)
        self.assertIn("fa fa-times-circle", content)

        # Add permission
        self.pilot_group.permissions.add(self.edit_submission_validations)

        # Check permission is assigned correctly
        self.assertTrue(self.pilot.has_perm("submissions.edit_submission_validations"))

        # Refresh response
        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
        )

        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        # Button should appear
        self.assertIn("Modifier les validations", content)

    def test_validator_cant_edit_validation_even_with_perms(self):
        # Add permission
        self.validator.user_permissions.add(self.edit_submission_validations)

        # Check permission is assigned correctly
        self.assertTrue(
            self.validator.has_perm("submissions.edit_submission_validations")
        )

        self.client.login(username=self.pilot.username, password="password")

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
        )

        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        # Button should not appear
        self.assertNotIn("Modifier les validations", content)
