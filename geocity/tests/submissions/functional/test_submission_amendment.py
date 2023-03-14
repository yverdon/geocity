from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInSecretariatMixin, get_parser


class SubmissionAmendmentTestCase(LoggedInSecretariatMixin, TestCase):
    def test_non_secretariat_user_cannot_amend_request(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user,
        )
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_PROCESSING,
                "action": submissions_models.ACTION_AMEND,
            },
        )

        submission.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            submission.status,
            submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        )

    def test_secretariat_can_amend_request_with_custom_field_and_delete_field_value(
        self,
    ):
        fields_quantity = 3
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        selected_form = factories.SelectedFormFactory(submission=submission)

        amend_fields = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity
        )

        data = {
            "action": submissions_models.ACTION_AMEND,
            "status": submissions_models.Submission.STATUS_PROCESSING,
        }

        forms_pk = submission.forms.first().pk
        for amend_field in amend_fields:
            amend_field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=amend_field,
                form=selected_form,
            )
            data[f"{forms_pk}_{amend_field.pk}"] = "I am a new field value, I am alive!"

        # The delete latter field value by setting it to an empty string
        data[f"{forms_pk}_{amend_fields[-1].pk}"] = ""

        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )

        new_fields_values_qs = (
            submissions_models.SubmissionAmendFieldValue.objects.values_list(
                "value", flat=True
            )
        )
        self.assertEqual(len(new_fields_values_qs), fields_quantity - 1)
        self.assertIn(
            "I am a new field value, I am alive!",
            new_fields_values_qs,
        )

    def test_secretariat_cannot_amend_submission_fields_if_can_always_be_updated(
        self,
    ):
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
        )
        form = factories.FormFactory()
        submission.forms.set([form])
        test_shortname_value = "my submission shortname"
        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                f"shortname": test_shortname_value,
                "action": submissions_models.ACTION_AMEND,
                "status": submissions_models.Submission.STATUS_PROCESSING,
            },
        )

        parser = get_parser(response.content)
        element = "disabled" in str(parser.select('input[id="id_shortname"]'))
        self.assertTrue(element)

    def test_secretariat_can_amend_submission_fields_if_it_can_always_be_updated(
        self,
    ):
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
        )
        form = factories.FormFactory(can_always_update=True)
        submission.forms.set([form])
        test_shortname_value = "my submission shortname"
        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                f"shortname": test_shortname_value,
                "action": submissions_models.ACTION_AMEND,
                "status": submissions_models.Submission.STATUS_PROCESSING,
            },
        )

        parser = get_parser(response.content)
        element = "disabled" in str(parser.select('input[id="id_shortname"]'))
        self.assertTrue(element)

    def test_author_cannot_see_private_secretariat_amend_field(
        self,
    ):

        fields_quantity = 3
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        selected_form = factories.SelectedFormFactory(submission=submission)

        fields_public = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, is_visible_by_author=True
        )
        fields_private = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, is_visible_by_author=False
        )
        fields_private_validators = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity,
            is_visible_by_author=False,
            is_visible_by_validators=True,
        )

        fields = fields_public + fields_private + fields_private_validators

        self.client.login(username=submission.author.username, password="password")
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
        # check that the 3 fields are visible by author and 6 (3 private + 3 for validators) are hidden
        self.assertEqual(len(parser.select(".amend-property")), 3)

    def test_secretariat_can_see_submitted_requests(self):
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        factories.SubmissionGeoTimeFactory(submission=submission)
        response = self.client.get(reverse("submissions:submissions_list"))

        self.assertEqual(list(response.context["submission_list"]), [submission])

    def test_ask_for_supplements_shows_specific_message(self):
        form_1 = factories.FormFactory()
        form_2 = factories.FormFactory()
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        submission.forms.set([form_1, form_2])
        factories.SubmissionGeoTimeFactory(submission=submission)
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT,
                "action": submissions_models.ACTION_AMEND,
                "notify_author": "on",
                "reason": "reason",
            },
            follow=True,
        )
        submission.refresh_from_db()
        self.assertEqual(
            submission.status, submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT
        )
        self.assertContains(response, "compléments")

    def test_secretariat_cannot_amend_submission_with_validation_requested(self):
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
                "status": submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT,
                "action": submissions_models.ACTION_AMEND,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_secretariat_can_see_directives(self):
        first_form = factories.FormFactory(
            directive=SimpleUploadedFile("file.pdf", "contents".encode()),
            directive_description="First directive description for a test",
            additional_information="First additional information for a test",
        )
        second_form = factories.FormFactory(
            directive=SimpleUploadedFile("file.pdf", "contents".encode()),
            directive_description="Second directive description for a test",
            additional_information="Second additional information for a test",
        )

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )

        submission.forms.set([first_form, second_form])

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            )
        )

        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#directives span.directive_description")),
            2,
        )

    def test_secretariat_cannot_see_directives_if_not_configured(
        self,
    ):
        forms = factories.FormFactory.create_batch(2)

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )

        submission.forms.set(forms)

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            )
        )

        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#directives span.directive_description")),
            0,
        )

    def test_email_to_author_is_sent_when_secretariat_acknowledges_reception(self):
        user = factories.UserFactory(email="user@geocity.com")
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user,
        )
        form = factories.FormFactory()
        form_name = form.name
        submission.forms.set([form])
        factories.SubmissionGeoTimeFactory(submission=submission)
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_RECEIVED,
                "action": submissions_models.ACTION_AMEND,
            },
            follow=True,
        )

        submission.refresh_from_db()
        self.assertEqual(
            submission.status, submissions_models.Submission.STATUS_RECEIVED
        )
        self.assertContains(response, "compléments")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "{} ({})".format(
                "Votre demande/annonce a été prise en compte et classée",
                form_name,
            ),
        )
        self.assertIn(
            "Nous vous informons que votre demande/annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )

    def test_email_to_services_is_sent_when_secretariat_acknowledges_reception(self):
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        form = factories.FormFactory(
            requires_validation_document=False,
            notify_services=True,
            services_to_notify="service-1@geocity.ch, service-2@geocity.ch, i-am-not-an-email,  ,\n\n\n",
        )
        submission.forms.set([form])
        factories.SubmissionGeoTimeFactory(submission=submission)

        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_RECEIVED,
                "action": submissions_models.ACTION_AMEND,
            },
            follow=True,
        )

        submission.refresh_from_db()
        self.assertEqual(
            submission.status, submissions_models.Submission.STATUS_RECEIVED
        )

        # 1 email to author + 2 emails to services
        self.assertEqual(len(mail.outbox), 3)

        services_message_subject = (
            "Une demande/annonce a été prise en compte et classée par le secrétariat"
        )
        services_message_content = "Nous vous informons qu'une demande/annonce a été prise en compte et classée par le secrétariat."
        valid_services_emails = [
            "service-1@geocity.ch",
            "service-2@geocity.ch",
        ]

        self.assertTrue(mail.outbox[1].to[0] in valid_services_emails)
        self.assertIn(
            services_message_subject,
            mail.outbox[1].subject,
        )
        self.assertIn(services_message_content, mail.outbox[1].message().as_string())
        self.assertTrue(mail.outbox[2].to[0] in valid_services_emails)
        self.assertIn(
            services_message_subject,
            mail.outbox[2].subject,
        )
        self.assertIn(services_message_content, mail.outbox[2].message().as_string())

    def test_secretariat_can_amend_submission_with_status_approved_if_field_is_always_amendable(
        self,
    ):
        fields_quantity = 3
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
        )

        form = factories.FormFactory()
        form.administrative_entities.set([submission.administrative_entity])

        selected_form = factories.SelectedFormFactory(submission=submission, form=form)

        fields = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, can_always_update=True
        )

        data = {
            "action": submissions_models.ACTION_AMEND,
            "status": submissions_models.Submission.STATUS_APPROVED,
        }

        forms_pk = submission.forms.first().pk

        for field in fields:
            field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=field,
                form=selected_form,
            )
            data[f"{forms_pk}_{field.pk}"] = "I am a new field value, I am alive!"

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
            follow=True,
        )

        new_fields_values_qs = (
            submissions_models.SubmissionAmendFieldValue.objects.values_list(
                "value", flat=True
            )
        )

        self.assertIn(
            "I am a new field value, I am alive!",
            new_fields_values_qs,
        )

        self.assertEqual(response.status_code, 200)

    def test_amend_field_are_editable_in_status_approved_if_field_is_always_amendable(
        self,
    ):
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
        )

        form = factories.FormFactory()
        form.administrative_entities.set([submission.administrative_entity])

        selected_form = factories.SelectedFormFactory(submission=submission, form=form)

        field_editable = factories.SubmissionAmendFieldFactory(
            name="Editable_field", can_always_update=True
        )

        field_not_editable = factories.SubmissionAmendFieldFactory(
            name="Not_editable_field", can_always_update=False
        )

        fields = [field_editable, field_not_editable]

        data = {
            "action": submissions_models.ACTION_AMEND,
            "status": submissions_models.Submission.STATUS_APPROVED,
        }

        forms_pk = submission.forms.first().pk

        for field in fields:
            field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=field,
                form=selected_form,
                value=field.name,
            )
            if field.name == "Editable_field":
                data[f"{forms_pk}_{field.pk}"] = "I have been edited!"

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(parser.select("#amend .form-group textarea")),
            3,
        )

        self.assertEqual(
            len(parser.select("#amend .form-group textarea[disabled]")),
            2,
        )

        # Send form edit
        response2 = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
            follow=True,
        )

        new_fields_values_qs = (
            submissions_models.SubmissionAmendFieldValue.objects.values_list(
                "value", flat=True
            )
        )

        self.assertIn(
            "I have been edited!",
            new_fields_values_qs,
        )
        self.assertEqual(response2.status_code, 200)

    def test_email_to_author_is_sent_when_secretariat_checks_notify(self):
        user = factories.UserFactory(email="user@geocity.com")
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user,
        )
        form = factories.FormFactory()
        form_name = form.name
        submission.forms.set([form])
        factories.SubmissionGeoTimeFactory(submission=submission)
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT,
                "notify_author": "1",
                "reason": "Testing email sending",
                "action": submissions_models.ACTION_AMEND,
            },
            follow=True,
        )

        submission.refresh_from_db()
        self.assertEqual(
            submission.status, submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT
        )
        self.assertContains(response, "compléments")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "{} ({})".format(
                "Votre demande/annonce a changé de statut",
                form_name,
            ),
        )
        self.assertIn(
            "Nous vous informons que votre demande/annonce a changé de statut.",
            mail.outbox[0].message().as_string(),
        )
        self.assertIn(
            "Nouveau statut: Demande de compléments",
            mail.outbox[0].message().as_string(),
        )
        self.assertIn(
            "Raison du changement:",
            mail.outbox[0].message().as_string(),
        )

    def test_awaiting_supplement_requires_to_notify_author(
        self,
    ):
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT,
                "action": submissions_models.ACTION_AMEND,
            },
            follow=True,
        )
        submission.refresh_from_db()

        self.assertEqual(
            submission.status, submissions_models.Submission.STATUS_PROCESSING
        )
        self.assertEqual(
            response.context[0]["forms"]["amend"].errors["notify_author"],
            ["Vous devez notifier l'auteur pour une demande de compléments"],
        )
