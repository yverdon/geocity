import re
from datetime import datetime

from django.urls import reverse

from geocity.apps.permits import models

from .. import factories
from ..geocity_test_case import GeocityTestCase


class TestPermitRequestArchiving(GeocityTestCase):
    def setUp(self):
        super(TestPermitRequestArchiving, self).setUp()

        self.login(email="user@test.com")
        self.parent_type = factories.ParentComplementaryDocumentTypeFactory()

        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_RECEIVED,
            administrative_entity=self.administrative_entity,
        )

    def test_permit_request_is_archived(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)

        self.client.post(
            reverse("permits:archived_permit_request_list"),
            data={
                "to_archive[]": self.permit_request.id,
                "action": "archive-requests",
            },
        )
        self.permit_request.refresh_from_db()
        self.assertEquals(
            self.permit_request.status, models.PermitRequest.STATUS_ARCHIVED
        )
        self.assertTrue(
            models.ArchivedPermitRequest.objects.filter(
                permit_request=self.permit_request
            ).exists()
        )

    def test_non_pilot_users_cannot_archive_requests(self):
        self.login(email="validator@test.com", group=self.VALIDATOR)

        response = self.client.post(
            reverse("permits:archived_permit_request_list"),
            data={
                "to_archive[]": self.permit_request.id,
                "action": "archive-requests",
            },
        )
        self.permit_request.refresh_from_db()
        self.assertNotEquals(
            self.permit_request.status, models.PermitRequest.STATUS_ARCHIVED
        )
        self.assertFalse(
            models.ArchivedPermitRequest.objects.filter(
                permit_request=self.permit_request
            ).exists()
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            b"Vous n'avez pas les permissions pour archiver cette demande",
            response.content,
        )

    def test_single_download_archive(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.permit_request.archive(self.user)
        file_response = self.client.get(
            reverse(
                "permits:archived_permit_request_download",
                kwargs={
                    "pk": self.permit_request.pk,
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
        self.permit_request.archive(self.user)
        archive = models.ArchivedPermitRequest.objects.filter(
            permit_request=self.permit_request
        ).first()
        file_response = self.client.get(
            reverse(
                "permits:archived_permit_request_bulk_download",
            ),
            data={"to_download": self.permit_request.pk},
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
        archive = factories.ArchivedPermitRequestFactory(
            permit_request=self.permit_request, archivist=self.user
        )
        self.login(email="validator@test.com", group=self.VALIDATOR)

        response = self.client.get(
            reverse(
                "permits:archived_permit_request_download",
                kwargs={
                    "pk": archive.permit_request.pk,
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
        self.permit_request.archive(self.user)
        archive = models.ArchivedPermitRequest.objects.filter(
            permit_request=self.permit_request
        ).first()
        self.login(email="validator@test.com", group=self.VALIDATOR)
        response = self.client.get(
            reverse(
                "permits:archived_permit_request_bulk_download",
            ),
            data={"to_download": archive.permit_request.pk},
            follow=True,
        )
        self.assertNotEqual(response.get("Content-Type"), "application/zip")
        messages = [str(message) for message in list(response.context["messages"])]
        self.assertIn(
            "Vous n'avez pas les permissions pour télécharger ces archives", messages
        )

    def test_only_archivist_can_delete_archive(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.permit_request.archive(self.user)
        archive = models.ArchivedPermitRequest.objects.filter(
            permit_request=self.permit_request
        ).first()

        self.client.post(
            reverse(
                "permits:archived_permit_request_delete",
                kwargs={"pk": archive.permit_request.pk},
            ),
        )

        self.assertFalse(
            models.ArchivedPermitRequest.objects.filter(
                permit_request=archive.permit_request
            ).exists()
        )
        self.assertFalse(
            models.PermitRequest.objects.filter(pk=self.permit_request.pk).exists()
        )

    def test_user_without_correct_permissions_cannot_delete_archive(self):
        self.login(email="pilot@test.com", group=self.SECRETARIAT)
        self.permit_request.archive(self.user)
        archive = models.ArchivedPermitRequest.objects.filter(
            permit_request=self.permit_request
        ).first()
        self.login(email="validator@test.com", group=self.VALIDATOR)

        response = self.client.post(
            reverse(
                "permits:archived_permit_request_delete",
                kwargs={"pk": archive.permit_request.pk},
            ),
            follow=True,
        )

        messages = [str(message) for message in list(response.context["messages"])]
        self.assertIn(
            "Vous n'avez pas les permissions pour supprimer cette archive", messages
        )
        self.assertTrue(
            models.ArchivedPermitRequest.objects.filter(
                permit_request=archive.permit_request
            ).exists()
        )
        self.assertTrue(
            models.PermitRequest.objects.filter(pk=self.permit_request.pk).exists()
        )
