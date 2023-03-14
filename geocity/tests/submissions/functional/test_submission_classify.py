from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories


class SubmissionClassifyTestCase(TestCase):
    def setUp(self):
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permit_department.administrative_entity
        )
        self.administrative_entity.custom_signature = "a custom signature for email"
        self.administrative_entity.save()
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity
        )
        self.validator_user = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

    def test_secretariat_can_approve_submission_and_email_to_author_is_sent(self):

        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            submission__status=submissions_models.Submission.STATUS_PROCESSING,
            validation_status=submissions_models.SubmissionValidation.STATUS_APPROVED,
            submission__author__email="user@geocity.com",
        )
        form = factories.FormFactory()
        form_name = form.name
        validation.submission.forms.set([form])

        self.client.login(username=self.secretariat_user.username, password="password")
        factories.SubmissionGeoTimeFactory(submission=validation.submission)
        response = self.client.post(
            reverse(
                "submissions:submission_approve",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={
                "validation_pdf": SimpleUploadedFile("file.pdf", "contents".encode())
            },
        )

        self.assertRedirects(
            response,
            reverse("submissions:submissions_list"),
            fetch_redirect_response=False,
        )
        validation.submission.refresh_from_db()
        self.assertEqual(
            validation.submission.status, submissions_models.Submission.STATUS_APPROVED
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "{} ({})".format(
                "Votre demande a été traitée et classée",
                form_name,
            ),
        )
        self.assertIn(
            "Nous vous informons que votre demande a été traitée et classée.",
            mail.outbox[0].message().as_string(),
        )
        self.assertIn(
            "a custom signature for email",
            mail.outbox[0].message().as_string(),
        )

    def test_secretariat_can_reject_submission_and_email_to_author_is_sent(self):

        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            submission__status=submissions_models.Submission.STATUS_PROCESSING,
            validation_status=submissions_models.SubmissionValidation.STATUS_REJECTED,
            submission__author__email="user@geocity.com",
        )
        form = factories.FormFactory()
        form_name = form.name
        validation.submission.forms.set([form])

        self.client.login(username=self.secretariat_user.username, password="password")
        factories.SubmissionGeoTimeFactory(submission=validation.submission)
        response = self.client.post(
            reverse(
                "submissions:submission_reject",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={
                "validation_pdf": SimpleUploadedFile("file.pdf", "contents".encode()),
            },
        )

        self.assertRedirects(
            response,
            reverse("submissions:submissions_list"),
            fetch_redirect_response=False,
        )
        validation.submission.refresh_from_db()
        self.assertEqual(
            validation.submission.status, submissions_models.Submission.STATUS_REJECTED
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "{} ({})".format(
                "Votre demande a été traitée et classée",
                form_name,
            ),
        )
        self.assertIn(
            "Nous vous informons que votre demande a été traitée et classée.",
            mail.outbox[0].message().as_string(),
        )
        self.assertIn(
            "a custom signature for email",
            mail.outbox[0].message().as_string(),
        )

    def test_secretariat_cannot_classify_submission_with_pending_validations(self):

        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.post(
            reverse(
                "submissions:submission_approve",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={"validation_pdf": SimpleUploadedFile("file.pdf", "")},
        )

        self.assertEqual(response.status_code, 404)

    def test_secretariat_does_not_see_classify_form_when_pending_validations(self):
        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": validation.submission.pk},
            )
        )

        self.assertNotContains(
            response,
            reverse(
                "submissions:submission_approve",
                kwargs={"submission_id": validation.submission.pk},
            ),
        )

    def test_user_without_permission_cannot_classify_submission(self):
        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            validation_status=submissions_models.SubmissionValidation.STATUS_APPROVED,
        )
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

        approve_url = reverse(
            "submissions:submission_approve",
            kwargs={"submission_id": validation.submission.pk},
        )

        response = self.client.post(
            approve_url, data={"validation_pdf": SimpleUploadedFile("file.pdf", "")}
        )

        self.assertRedirects(
            response, "%s?next=%s" % (reverse(settings.LOGIN_URL), approve_url)
        )

    def test_submission_validation_file_accessible_to_submission_author(self):
        author_user = factories.UserFactory()
        submission = factories.SubmissionFactory(
            validated_at=timezone.now(),
            status=submissions_models.Submission.STATUS_APPROVED,
            author=author_user,
        )
        # This cannot be performed in the factory because we need the submission to have an id to upload a file
        submission.validation_pdf = SimpleUploadedFile("file.pdf", b"contents")
        submission.save()

        self.client.login(username=author_user, password="password")
        response = self.client.get(submission.validation_pdf.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"contents")

    def test_submission_validation_file_not_accessible_to_other_users(self):
        non_author_user = factories.UserFactory()
        submission = factories.SubmissionFactory(
            validated_at=timezone.now(),
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        # This cannot be performed in the factory because we need the submission to have an id to upload a file
        submission.validation_pdf = SimpleUploadedFile("file.pdf", b"contents")
        submission.save()

        self.client.login(username=non_author_user, password="password")
        response = self.client.get(submission.validation_pdf.url)
        self.assertEqual(response.status_code, 404)

    def test_classify_sets_validation_date(self):
        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            submission__status=submissions_models.Submission.STATUS_PROCESSING,
            validation_status=submissions_models.SubmissionValidation.STATUS_APPROVED,
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        self.client.post(
            reverse(
                "submissions:submission_approve",
                kwargs={"submission_id": validation.submission.pk},
            ),
            data={"validation_pdf": SimpleUploadedFile("file.pdf", b"contents")},
        )

        validation.submission.refresh_from_db()
        self.assertIsNotNone(validation.submission.validated_at)

    def test_email_to_services_is_sent_when_secretariat_classifies_submission(self):
        form = factories.FormFactory(
            requires_validation_document=False,
            notify_services=True,
            services_to_notify="test-send-1@geocity.ch, test-send-2@geocity.ch, test-i-am-not-an-email,  ,\n\n\n",
        )
        form_name_1 = form.name
        form2 = factories.FormFactory(
            requires_validation_document=False,
            notify_services=True,
            services_to_notify="not-repeated-email@liip.ch, test-send-1@geocity.ch, \n, test-send-2@geocity.ch, test-i-am-not-an-email,  ,",
        )
        form_name_2 = form2.name
        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            submission__status=submissions_models.Submission.STATUS_PROCESSING,
            validation_status=submissions_models.SubmissionValidation.STATUS_APPROVED,
            submission__author__email="user@geocity.com",
        )
        validation.submission.forms.set([form, form2])
        factories.SubmissionGeoTimeFactory(submission=validation.submission)

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.post(
            reverse(
                "submissions:submission_approve",
                kwargs={"submission_id": validation.submission.pk},
            ),
        )

        self.assertRedirects(
            response,
            reverse("submissions:submissions_list"),
            fetch_redirect_response=False,
        )
        validation.submission.refresh_from_db()
        self.assertEqual(
            validation.submission.status, submissions_models.Submission.STATUS_APPROVED
        )
        # Only valid emails are sent, not repeated emails.
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])

        self.assertIn(
            "Votre demande a été traitée et classée",
            mail.outbox[0].subject,
        )

        self.assertIn(
            form_name_1,
            mail.outbox[0].subject,
        )

        self.assertIn(
            form_name_2,
            mail.outbox[0].subject,
        )

        self.assertIn(
            "Nous vous informons que votre demande a été traitée et classée.",
            mail.outbox[0].message().as_string(),
        )

        services_message_content = "Nous vous informons qu'une demande a été traitée et classée par le secrétariat."
        valid_services_emails = [
            "not-repeated-email@liip.ch",
            "test-send-2@geocity.ch",
            "test-send-1@geocity.ch",
        ]
        self.assertIn(
            "a custom signature for email",
            mail.outbox[0].message().as_string(),
        )
        self.assertTrue(mail.outbox[1].to[0] in valid_services_emails)
        self.assertIn(services_message_content, mail.outbox[1].message().as_string())
        self.assertTrue(mail.outbox[2].to[0] in valid_services_emails)
        self.assertIn(services_message_content, mail.outbox[2].message().as_string())
        self.assertTrue(mail.outbox[3].to[0] in valid_services_emails)
        self.assertIn(services_message_content, mail.outbox[3].message().as_string())


class ApprovedSubmissionClassifyTestCase(TestCase):
    def setUp(self):
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permit_department.administrative_entity
        )
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        self.validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            submission__status=submissions_models.Submission.STATUS_PROCESSING,
            validation_status=submissions_models.SubmissionValidation.STATUS_APPROVED,
        )
        self.client.login(username=self.secretariat_user.username, password="password")

    def _get_approval(self):
        response = self.client.get(
            reverse(
                "submissions:submission_approve",
                kwargs={"submission_id": self.validation.submission.pk},
            ),
        )
        self.assertContains(response, "Approbation de la demande")
        self.assertEqual(
            self.validation.submission.status,
            submissions_models.Submission.STATUS_PROCESSING,
        )
        return response

    def test_classify_submission_with_required_validation_doc_shows_file_field(
        self,
    ):
        form = factories.FormFactory(requires_validation_document=True)
        self.validation.submission.forms.set([form])
        response = self._get_approval()
        self.assertContains(response, "validation_pdf")

    def test_classify_submission_without_required_validation_doc_does_not_show_file_field(
        self,
    ):
        form = factories.FormFactory(requires_validation_document=False)
        self.validation.submission.forms.set([form])
        response = self._get_approval()
        self.assertNotContains(response, "validation_pdf")

    def test_classify_submission_with_any_object_requiring_validation_doc_shows_file_field(
        self,
    ):
        form1 = factories.FormFactory(requires_validation_document=True)
        form2 = factories.FormFactory(requires_validation_document=False)
        self.validation.submission.forms.set([form1, form2])
        response = self._get_approval()
        self.assertContains(response, "validation_pdf")
