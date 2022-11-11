import re
from datetime import datetime

from django.urls import reverse

from geocity.apps.submissions import models as submissions_models

from geocity.tests import factories
from geocity.tests.geocity_test_case import GeocityTestCase


class TestSubmissionArchiving(GeocityTestCase):
    def setUp(self):
        super(TestSubmissionArchiving, self).setUp()

        self.login(email="user@test.com")
        self.parent_type = factories.ParentComplementaryDocumentTypeFactory()

        self.submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_RECEIVED,
            administrative_entity=self.administrative_entity,
        )

    def test_submission_is_archived(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)

        self.client.post(
            reverse("submissions:archived_submission_list"),
            data={
                "to_archive[]": self.submission.id,
                "action": "archive-requests",
            },
        )
        self.submission.refresh_from_db()
        self.assertEquals(
            self.submission.status, submissions_models.Submission.STATUS_ARCHIVED
        )
        self.assertTrue(
            submissions_models.ArchivedSubmission.objects.filter(
                submission=self.submission
            ).exists()
        )

    def test_non_pilot_users_cannot_archive_requests(self):
        self.login(email="validator@test.com", group=self.VALIDATOR)

        response = self.client.post(
            reverse("submissions:archived_submission_list"),
            data={
                "to_archive[]": self.submission.id,
                "action": "archive-requests",
            },
        )
        self.submission.refresh_from_db()
        self.assertNotEquals(
            self.submission.status, submissions_models.Submission.STATUS_ARCHIVED
        )
        self.assertFalse(
            submissions_models.ArchivedSubmission.objects.filter(
                submission=self.submission
            ).exists()
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            b"Vous n'avez pas les permissions pour archiver cette demande",
            response.content,
        )

    def test_single_download_archive(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.submission.archive(self.user)
        file_response = self.client.get(
            reverse(
                "submissions:archived_submission_download",
                kwargs={
                    "pk": self.submission.pk,
                },
            ),
        )

        # Do not compare seconds as they can have a small delta and sometimes make the tests fail
        expected_filename_regex = (
            f"Archive_{datetime.today().strftime('%d.%m.%Y.%H.%M')}.[0-9][0-9]"
        )

        self.assertEqual(file_response.get("Content-Type"), "application/zip")
        self.assertRegex(
            file_response.get("Content-Disposition"),
            re.compile(rf'inline; filename="{expected_filename_regex}.zip"'),
        )

    def test_bulk_download(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.submission.archive(self.user)
        archive = submissions_models.ArchivedSubmission.objects.filter(
            submission=self.submission
        ).first()
        file_response = self.client.get(
            reverse(
                "submissions:archived_submission_bulk_download",
            ),
            data={"to_download": self.submission.pk},
        )

        # Do not compare seconds as they can have a small delta and sometimes make the tests fail
        expected_filename_regex = (
            f"Archive_{datetime.today().strftime('%d.%m.%Y.%H.%M')}.[0-9][0-9]"
        )

        self.assertEqual(file_response.get("Content-Type"), "application/zip")
        self.assertRegex(
            file_response.get("Content-Disposition"),
            re.compile(rf'inline; filename="{expected_filename_regex}.zip"'),
        )

    def test_users_not_in_archivist_group_cannot_single_download(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        archive = factories.ArchivedSubmissionFactory(
            submission=self.submission, archivist=self.user
        )
        self.login(email="validator@test.com", group=self.VALIDATOR)

        response = self.client.get(
            reverse(
                "submissions:archived_submission_download",
                kwargs={
                    "pk": archive.submission.pk,
                },
            ),
            follow=True,
        )
        self.assertNotEqual(response.get("Content-Type"), "application/zip")
        messages = [str(message) for message in list(response.context["messages"])]
        self.assertIn(
            "Vous n'avez pas les permissions pour télécharger cette archive", messages
        )

    def test_users_not_in_archivist_group_cannot_bulk_download(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.submission.archive(self.user)
        archive = submissions_models.ArchivedSubmission.objects.filter(
            submission=self.submission
        ).first()
        self.login(email="validator@test.com", group=self.VALIDATOR)
        response = self.client.get(
            reverse(
                "submissions:archived_submission_bulk_download",
            ),
            data={"to_download": archive.submission.pk},
            follow=True,
        )
        self.assertNotEqual(response.get("Content-Type"), "application/zip")
        messages = [str(message) for message in list(response.context["messages"])]
        self.assertIn(
            "Vous n'avez pas les permissions pour télécharger ces archives", messages
        )

    def test_only_archivist_can_delete_archive(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.submission.archive(self.user)
        archive = submissions_models.ArchivedSubmission.objects.filter(
            submission=self.submission
        ).first()

        self.client.post(
            reverse(
                "submissions:archived_submission_delete",
                kwargs={"pk": archive.submission.pk},
            ),
        )

        self.assertFalse(
            submissions_models.ArchivedSubmission.objects.filter(
                submission=archive.submission
            ).exists()
        )
        self.assertFalse(
            submissions_models.Submission.objects.filter(pk=self.submission.pk).exists()
        )

    def test_user_without_correct_permissions_cannot_delete_archive(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.submission.archive(self.user)
        archive = submissions_models.ArchivedSubmission.objects.filter(
            submission=self.submission
        ).first()
        self.login(email="validator@test.com", group=self.VALIDATOR)

        response = self.client.post(
            reverse(
                "submissions:archived_submission_delete",
                kwargs={"pk": archive.submission.pk},
            ),
            follow=True,
        )

        messages = [str(message) for message in list(response.context["messages"])]
        self.assertIn(
            "Vous n'avez pas les permissions pour supprimer cette archive", messages
        )
        self.assertTrue(
            submissions_models.ArchivedSubmission.objects.filter(
                submission=archive.submission
            ).exists()
        )
        self.assertTrue(
            submissions_models.Submission.objects.filter(pk=self.submission.pk).exists()
        )
