from django.test import TestCase
from django.urls import reverse

from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInReadonlyTrustedMixin, get_parser


class ReadonlySubmissionTestCase(LoggedInReadonlyTrustedMixin, TestCase):
    def test_trusted_user_with_read_permission_can_read_submission_detail_but_not_secretariat_infos(
        self,
    ):

        user = factories.UserFactory()

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Auteur-e", response.content.decode())
        # Ensure processing tabs are not visible to this role
        parser = get_parser(response.content)
        self.assertEqual(len(parser.select("#amend-tab")), 0)
        self.assertEqual(len(parser.select("#request-validation")), 0)
        self.assertEqual(len(parser.select("#classify")), 0)
        self.assertEqual(len(parser.select("#documents")), 0)
