from django.test import TestCase
from django.urls import reverse

from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories


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
