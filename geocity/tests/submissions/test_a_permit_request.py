# TODO split this file into multiple files
import datetime
import re
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from geocity.apps.accounts import models as accounts_models
from geocity.apps.forms import models as forms_models
from geocity.apps.reports.models import Report
from geocity.apps.submissions import forms as submissions_forms
from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInUserMixin, get_emails, get_parser


def to_forms_dict(forms):
    return {"forms-{}".format(form.form_category.pk): form.pk for form in forms}


def get_submission_form_categories_ids(submission):
    return list(
        submission.forms.order_by("form_category__name")
        .values_list("form_category__pk", flat=True)
        .distinct()
    )


class SubmissionTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.form_categories = factories.FormCategoryFactory.create_batch(2)

        factories.FormFactory(
            category=self.form_categories[0],
            is_public=True,
        )
        factories.FormFactory(
            category=self.form_categories[1],
            is_public=True,
        )

        self.geotime_step_formset_data = {
            "form-TOTAL_FORMS": ["1"],
            "form-INITIAL_FORMS": ["0"],
            "form-MIN_NUM_FORMS": ["0"],
        }

    def test_forms_step_submit_saves_selected_forms(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.FormFactory()

        form = forms_models.Form.objects.first()
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())
        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            ),
            data={"forms-selected_forms": form.pk},
        )

        self.assertEqual(
            submissions_models.Submission.objects.filter(forms=form).count(),
            1,
        )

    def test_forms_step_submit_saves_multiple_selected_forms(self):
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        submission.refresh_from_db()
        self.assertEqual(
            submission.forms.count(),
            forms_models.Form.objects.count(),
        )

    def test_single_form_submission_submit_saves_one_selected_form_only(self):
        submission = factories.SubmissionFactory(
            author=self.user,
            administrative_entity__is_single_form_submissions=True,
        )
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        submission.refresh_from_db()
        self.assertEqual(
            submission.forms.count(),
            1,
        )

    def test_cant_select_exceeded_submissions_single_forms_step(self):
        submission = factories.SubmissionFactory(
            author=self.user,
            administrative_entity__is_single_form_submissions=True,
        )
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        submission.status = submissions_models.Submission.STATUS_APPROVED
        submission.save()

        for form in submission.forms.all():
            form.max_submissions = 1
            form.save()

        new_submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=submission.administrative_entity
        )

        response = self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": new_submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        self.assertIn("Ce formulaire est désactivé", response.content.decode())

    def test_cant_select_exceeded_submissions_single_forms_step_if_bypass_enabled_and_not_pilot(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            administrative_entity__is_single_form_submissions=True,
        )
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        submission.status = submissions_models.Submission.STATUS_APPROVED
        submission.save()

        for form in submission.forms.all():
            form.max_submissions = 1
            form.max_submissions_bypass_enabled = True
            form.save()

        new_submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=submission.administrative_entity
        )

        response = self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": new_submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        self.assertIn("Ce formulaire est désactivé", response.content.decode())

    def test_pilot_can_select_exceeded_submissions_single_forms_step_if_bypass_enabled(
        self,
    ):
        # Create pilot group
        pilot_group = factories.GroupFactory(name="pilot")

        # Create department
        department = factories.PermitDepartmentFactory(
            group=pilot_group, is_backoffice=True
        )

        # Create pilot user
        pilot = factories.SecretariatUserFactory(
            groups=[pilot_group], email="secretary@geocity.ch"
        )
        submission = factories.SubmissionFactory(
            author=self.user,
            administrative_entity=department.administrative_entity,
        )
        submission.save()
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        submission.status = submissions_models.Submission.STATUS_APPROVED
        submission.save()

        for form in submission.forms.all():
            form.max_submissions = 1
            form.max_submissions_bypass_enabled = True
            form.save()

        self.client.login(username=pilot.username, password="password")
        new_submission = factories.SubmissionFactory(
            author=pilot, administrative_entity=submission.administrative_entity
        )

        response = self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": new_submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
            follow=True,
        )

        # We were redirected to the fields step, because we bypassed the max_submissions limit
        assert response.resolver_match.url_name == "submission_fields"

    def test_form_cant_be_submitted_if_exceeded_submissions_in_between(self):
        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
            )
        ).submission
        form = factories.FormFactory()
        selected_form = factories.SelectedFormFactory(
            submission=submission,
            form=form,
        )

        field = factories.FieldFactory(
            services_to_notify="test-send-1@geocity.ch, test-send-2@geocity.ch, test-i-am-not-an-email,  ,\n\n\n",
            input_type=submissions_models.Field.INPUT_TYPE_CHECKBOX,
        )

        field.forms.set(submission.forms.all())
        factories.FieldValueFactory(
            field=field,
            selected_form=selected_form,
            value={"val": True},
        )

        submission.status = submissions_models.Submission.STATUS_APPROVED
        submission.save()

        for sub_form in submission.forms.all():
            sub_form.max_submissions = 1
            sub_form.save()

        new_submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
                administrative_entity=submission.administrative_entity,
            )
        ).submission
        selected_form = factories.SelectedFormFactory(
            submission=new_submission,
            form=form,
        )
        factories.FieldValueFactory(
            field=field,
            selected_form=selected_form,
            value={"val": True},
        )

        response = self.client.get(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": new_submission.pk},
            )
        )

        self.assertIn("Ce formulaire est désactivé", response.content.decode())

    def test_categories_step_submit_redirects_to_detail_if_logged_as_backoffice(self):

        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )

        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_APPROVED,
            administrative_entity=department.administrative_entity,
        )
        secretary_group.user_set.add(self.user)

        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
        )

        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_cant_select_exceeded_submissions_forms_step_submit(self):
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())
        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )
        submission.status = submissions_models.Submission.STATUS_APPROVED
        submission.save()

        for form in submission.forms.all():
            form.max_submissions = 1
            form.save()

        new_submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=submission.administrative_entity
        )

        response = self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": new_submission.pk},
            ),
            data={
                "forms-selected_forms": forms_models.Form.objects.values_list(
                    "pk", flat=True
                )
            },
        )

        self.assertIn("Ce formulaire est désactivé", response.content.decode())

    def test_categories_step_submit_redirects_to_detail_if_logged_as_integrator_admin(
        self,
    ):

        integrator_group = factories.GroupFactory(name="Integrator")
        department = factories.PermitDepartmentFactory(
            group=integrator_group, is_integrator_admin=True
        )

        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_APPROVED,
            administrative_entity=department.administrative_entity,
        )
        integrator_group.user_set.add(self.user)

        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
        )

        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_non_required_fields_can_be_left_blank(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactory()
        field.forms.set(submission.forms.all())

        response = self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_documents_step_filetype_allows_jpg(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/tests/files/real_jpg.jpg", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={"appendices-{}_{}".format(field.forms.last().pk, field.pk): file},
            )

        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_documents_step_filetype_allows_png(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/tests/files/real_png.png", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={"appendices-{}_{}".format(field.forms.last().pk, field.pk): file},
            )

        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_documents_step_filetype_allows_pdf(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/tests/files/real_pdf.pdf", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={"appendices-{}_{}".format(field.forms.last().pk, field.pk): file},
            )

        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_documents_step_filetype_reject_unknow_type_for_filetype(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/tests/files/unknow_type_for_filetype.txt", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={"appendices-{}_{}".format(field.forms.last().pk, field.pk): file},
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="Le type de unknow_type_for_filetype.txt n'est pas supporté, assurez-vous que votre fichier soit du bon type",
        )
        self.assertInHTML(expected, content)

    def test_documents_step_filetype_reject_not_allowed_extension(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/tests/files/not_allowed_docx.docx", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={"appendices-{}_{}".format(field.forms.last().pk, field.pk): file},
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="not_allowed_docx.docx n'est pas du bon type",
        )
        self.assertInHTML(expected, content)

    def test_documents_step_filetype_reject_fake_jpg_with_not_allowed_extension(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/tests/files/not_allowed_bmp_as_jpg.jpg", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={"appendices-{}_{}".format(field.forms.last().pk, field.pk): file},
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="not_allowed_bmp_as_jpg.jpg n'est pas du bon type",
        )
        self.assertInHTML(expected, content)

    def test_user_can_only_see_own_requests(self):
        submission = factories.SubmissionFactory(author=factories.UserFactory())

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_non_draft_request(self):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_user_can_edit_non_draft_request_if_form_can_always_be_updated(self):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        )
        form = factories.FormFactory(can_always_update=True)
        factories.SelectedFormFactory(
            submission=submission,
            form=form,
        )
        submission.administrative_entity.forms.set(submission.forms.all())
        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertNotEqual(
            response,
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_submitted_submission_is_in_correct_status(self):
        submission = factories.SubmissionFactory(
            author=self.user,
        )
        form = factories.FormWithoutGeometryFactory(
            needs_date=False,
        )
        submission.forms.set([form])
        self.client.post(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        submission.refresh_from_db()

        self.assertEqual(
            submission.status,
            submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        )

    def test_submitted_submission_is_in_correct_status_when_validation_is_disabled(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
        )
        form = factories.FormWithoutGeometryFactory(
            needs_date=False, disable_validation_by_validators=True
        )
        submission.forms.set([form])
        self.client.post(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        submission.refresh_from_db()

        self.assertEqual(
            submission.status,
            submissions_models.Submission.STATUS_PROCESSING,
        )

    def test_secretary_email_is_sent_when_user_treated_requested_complements(self):
        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        factories.SecretariatUserFactory(
            groups=[secretary_group], email="secretary@geocity.ch"
        )
        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT,
            author=self.user,
            administrative_entity=department.administrative_entity,
        )
        form = factories.FormWithoutGeometryFactory(
            needs_date=False,
        )
        form_name = form.name
        submission.forms.set([form])
        self.client.post(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        submission.refresh_from_db()
        self.assertEqual(
            submission.status,
            submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["secretary@geocity.ch"])
        self.assertEqual(
            mail.outbox[0].subject,
            "{} ({})".format(
                "La demande de compléments a été traitée",
                form_name,
            ),
        )
        self.assertIn(
            "La demande de compléments a été traitée",
            mail.outbox[0].message().as_string(),
        )

    def test_submit_submission_sends_email_to_secretariat(self):
        # Create a secretariat user Yverdon (the one that will get the notification)
        group = factories.SecretariatGroupFactory()
        factories.SecretariatUserFactory(email="secretariat@yverdon.ch", groups=[group])
        # This one should not receive the notification
        factories.SecretariatUserFactory(email="secretariat@lausanne.ch")

        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                administrative_entity=group.permit_department.administrative_entity,
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
            )
        ).submission
        form = factories.FormFactory()
        form_name = form.name
        submission.forms.set([form])

        self.client.post(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        emails = get_emails(
            "{} ({})".format(
                "Nouvelle demande/annonce",
                form_name,
            )
        )

        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0].to, ["secretariat@yverdon.ch"])

    def test_submit_submission_sends_email_to_services_to_notify_from_field(
        self,
    ):
        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
            )
        ).submission
        form = factories.FormFactory()
        form_name = form.name
        selected_form = factories.SelectedFormFactory(
            submission=submission,
            form=form,
        )

        field = factories.FieldFactory(
            services_to_notify="test-send-1@geocity.ch, test-send-2@geocity.ch, test-i-am-not-an-email,  ,\n\n\n",
            input_type=submissions_models.Field.INPUT_TYPE_CHECKBOX,
        )

        field.forms.set(submission.forms.all())
        factories.FieldValueFactory(
            field=field,
            selected_form=selected_form,
            value={"val": True},
        )
        self.client.post(
            reverse(
                "submissions:submission_submit_confirmed",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(len(mail.outbox), 3)
        self.assertIn(
            mail.outbox[0].to, [["test-send-1@geocity.ch"], ["test-send-2@geocity.ch"]]
        )

        self.assertEqual(
            mail.outbox[0].subject,
            "{} ({})".format(
                "Votre service à été mentionné dans une demande/annonce",
                form_name,
            ),
        )
        self.assertIn(
            "Une nouvelle demande/annonce mentionnant votre service vient d'être soumise.",
            mail.outbox[0].message().as_string(),
        )

    def test_missing_mandatory_date_field_gives_invalid_feedback(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_DATE, is_mandatory=True
        )
        field.forms.set(submission.forms.all())

        data = {
            "fields-{}_{}".format(form.pk, field.pk): ""
            for form in submission.forms.all()
        }

        response = self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )
        parser = get_parser(response.content)
        self.assertEqual(len(parser.select(".invalid-feedback")), 1)

    def test_form_automatically_set_when_only_one_form(self):
        administrative_entity = factories.AdministrativeEntityFactory()
        form_first = factories.FormFactory(
            administrative_entities=[administrative_entity]
        )
        self.client.post(
            reverse(
                "submissions:submission_select_administrative_entity",
            ),
            {"administrative_entity": [administrative_entity]},
        )

        self.assertEqual(submissions_models.Submission.objects.count(), 1)
        self.assertEqual(
            submissions_models.Submission.objects.get().selected_forms.count(),
            1,
            "Submission should have one form set",
        )

    def test_geotime_step_only_date_fields_appear_when_only_date_is_required(self):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormWithoutGeometryFactory(
            needs_date=True,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select('input[name="form-0-starts_at"]')),
            1,
        )
        self.assertEqual(len(parser.select('input[name="form-0-ends_at"]')), 1)

        self.assertEqual(
            len(parser.select('textarea[name="form-0-geom"]')),
            0,
        )

    def test_geotime_step_date_fields_cannot_be_empty_when_date_is_required(self):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormWithoutGeometryFactory(
            needs_date=True,
        )
        submission.forms.set([form])
        self.geotime_step_formset_data.update(
            {"form-0-starts_at": [""], "form-0-ends_at": [""]}
        )
        response = self.client.post(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            ),
            data=self.geotime_step_formset_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormsetError(
            response,
            "formset",
            0,
            "starts_at",
            "Ce champ est obligatoire.",
        )
        self.assertFormsetError(
            response,
            "formset",
            0,
            "ends_at",
            "Ce champ est obligatoire.",
        )

    def test_geotime_step_date_fields_ends_at_must_not_be_before_starts_at(self):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormWithoutGeometryFactory(
            needs_date=True,
        )
        submission.forms.set([form])

        today = date.today()
        starts_at = today + datetime.timedelta(days=(int(settings.MIN_START_DELAY) + 2))
        ends_at = today + datetime.timedelta(days=(int(settings.MIN_START_DELAY) + 1))
        self.geotime_step_formset_data.update(
            {
                "form-0-starts_at": [starts_at.strftime("%Y-%m-%d 14:00:00+02:00")],
                "form-0-ends_at": [ends_at.strftime("%Y-%m-%d 14:00:00+02:00")],
            }
        )

        response = self.client.post(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            ),
            data=self.geotime_step_formset_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormsetError(
            response,
            "formset",
            0,
            None,
            "La date de fin doit être postérieure à la date de début.",
        )

    def test_geotime_step_only_geom_fields_appear_when_only_geom_is_required(self):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=False,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select('textarea[name="form-0-geom"]')),
            1,
        )

        self.assertEqual(
            len(parser.select('input[name="form-0-starts_at"]')),
            0,
        )
        self.assertEqual(len(parser.select('input[name="form-0-ends_at"]')), 0)

    def test_geotime_step_date_and_geom_fields_appear_when_both_required(self):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=True,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select('input[name="form-0-starts_at"]')),
            1,
        )
        self.assertEqual(len(parser.select('input[name="form-0-ends_at"]')), 1)
        self.assertEqual(
            len(parser.select('textarea[name="form-0-geom"]')),
            1,
        )

    def test_geotime_step_only_point_geom_field_appear_when_only_point_geom_type_is_required(
        self,
    ):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory(
            has_geometry_point=True,
            has_geometry_line=False,
            has_geometry_polygon=False,
            needs_date=False,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            0,
        )

    def test_geotime_step_only_line_geom_field_appear_when_only_line_geom_type_is_required(
        self,
    ):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory(
            has_geometry_point=False,
            has_geometry_line=True,
            has_geometry_polygon=False,
            needs_date=False,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            0,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            0,
        )

    def test_geotime_step_only_polygon_geom_field_appear_when_only_polygon_geom_type_is_required(
        self,
    ):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory(
            has_geometry_point=False,
            has_geometry_line=False,
            has_geometry_polygon=True,
            needs_date=False,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            0,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            1,
        )

    def test_geotime_step_help_text_appears_when_defined(self):
        submission = factories.SubmissionFactory(author=self.user)
        help_text = "Mon texte pour aider la saisie"
        form = factories.FormFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            geo_step_help_text=help_text,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, help_text)

    def test_geotime_step_only_two_geom_field_appear_when_only_two_geom_type_are_required(
        self,
    ):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory(
            has_geometry_point=True,
            has_geometry_line=False,
            has_geometry_polygon=True,
            needs_date=False,
        )
        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            1,
        )

    def test_start_date_is_limited_by_forms_with_biggest_start_delay(self):
        group = factories.SecretariatGroupFactory()
        form_1 = factories.FormFactory(
            start_delay=3,
        )
        form_2 = factories.FormFactory(
            start_delay=1,
        )

        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                administrative_entity=group.permit_department.administrative_entity,
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
            )
        ).submission

        submission.forms.set([form_1, form_2])

        resulted_start_at = submission.get_min_starts_at().date()
        expected_start_at = date.today() + datetime.timedelta(days=3)

        self.assertEqual(resulted_start_at, expected_start_at)

    def test_start_date_limit_falls_back_to_setting(self):
        today = date.today()
        group = factories.SecretariatGroupFactory()
        form = factories.FormFactory()

        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                administrative_entity=group.permit_department.administrative_entity,
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
            )
        ).submission

        submission.forms.set([form])

        self.assertEqual(
            submission.get_min_starts_at().date(),
            today + datetime.timedelta(days=int(settings.MIN_START_DELAY)),
        )

    def test_start_date_cant_be_of_limit(self):
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormWithoutGeometryFactory(
            needs_date=True,
            start_delay=3,
        )
        submission.forms.set([form])
        today = date.today()
        start_at = today + datetime.timedelta(days=1)  # Must be >= 3 to be valid
        self.geotime_step_formset_data.update(
            {
                "form-0-starts_at": [start_at.strftime("%Y-%m-%d 14:00:00+02:00")],
                "form-0-ends_at": [start_at.strftime("%Y-%m-%d 16:00:00+02:00")],
            }
        )
        response = self.client.post(
            reverse(
                "submissions:submission_geo_time",
                kwargs={"submission_id": submission.pk},
            ),
            data=self.geotime_step_formset_data,
        )
        self.assertIn("starts_at", response.context["formset"].errors[0])

    def test_start_date_limit_is_set_to_0(self):
        group = factories.SecretariatGroupFactory()
        form = factories.FormFactory(start_delay=0)
        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                administrative_entity=group.permit_department.administrative_entity,
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
            )
        ).submission
        submission.forms.set([form])

        self.assertEqual(submission.get_min_starts_at().date(), date.today())

    def test_summary_and_send_step_has_multiple_directive_fields_when_request_have_multiple_forms(
        self,
    ):
        group = factories.SecretariatGroupFactory()
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

        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                administrative_entity=group.permit_department.administrative_entity,
                author=self.user,
                status=submissions_models.Submission.STATUS_DRAFT,
            )
        ).submission

        submission.forms.set([first_form, second_form])

        response = self.client.get(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )

        parser = get_parser(response.content)

        self.assertEqual(
            len(parser.select("#legal-infos span.directive_description")),
            2,
        )

        self.assertEqual(
            len(parser.select("#legal-infos a.directive_file")),
            2,
        )

        self.assertEqual(
            len(parser.select("#legal-infos span.additional_information")),
            2,
        )

    def test_single_administrative_entity_with_tag_is_automatically_selected(self):
        administrative_entities = [
            factories.AdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        forms = forms_models.Form.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.forms.set(forms)

        response = self.client.get(
            reverse("submissions:submission_select_administrative_entity"),
            {"entityfilter": "first"},
            follow=True,
        )

        self.assertEqual(
            submissions_models.Submission.objects.filter(
                administrative_entity=administrative_entities[0].pk
            ).count(),
            1,
        )

    def test_single_administrative_entity_for_site_is_automatically_selected(self):
        administrative_entities = factories.AdministrativeEntityFactory.create_batch(
            3, sites=[]
        )

        site = get_current_site(self.client.request())
        administrative_entities[0].sites.set([site])
        forms = forms_models.Form.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.forms.set(forms)

        response = self.client.get(
            reverse("submissions:submission_select_administrative_entity"),
            follow=True,
        )

        self.assertEqual(
            submissions_models.Submission.objects.filter(
                administrative_entity=administrative_entities[0].pk
            ).count(),
            1,
        )
        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_select_forms",
                kwargs={
                    "submission_id": submissions_models.Submission.objects.get().pk
                },
            ),
        )

    def test_single_administrative_entity_with_single_form_has_administrative_entity_and_form_automatically_selected(
        self,
    ):
        form = factories.FormFactory()
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set([form])

        response = self.client.get(
            reverse("submissions:submission_select_administrative_entity"),
            follow=True,
        )

        self.assertEqual(
            submissions_models.Submission.objects.filter(
                administrative_entity=administrative_entity,
                forms=form,
            ).count(),
            1,
        )
        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_fields",
                kwargs={
                    "submission_id": submissions_models.Submission.objects.get().pk
                },
            ),
        )

    def test_post_administrative_entity_with_single_form_has_form_automatically_selected(
        self,
    ):
        form = factories.FormFactory()
        administrative_entities = factories.AdministrativeEntityFactory.create_batch(2)

        forms = forms_models.Form.objects.all()
        administrative_entities[0].forms.set([forms[0]])
        administrative_entities[1].forms.set(forms)

        response = self.client.post(
            reverse("submissions:submission_select_administrative_entity"),
            {"administrative_entity": administrative_entities[0].pk},
        )

        self.assertEqual(
            submissions_models.Submission.objects.filter(
                administrative_entity=administrative_entities[0],
                forms=forms[0],
            ).count(),
            1,
        )
        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_fields",
                kwargs={
                    "submission_id": submissions_models.Submission.objects.get().pk
                },
            ),
        )

    def test_post_administrative_entity_with_multiple_forms_shows_form_select_step(
        self,
    ):
        form = factories.FormFactory()
        administrative_entities = factories.AdministrativeEntityFactory.create_batch(2)

        forms = forms_models.Form.objects.all()
        for administrative_entity in administrative_entities:
            administrative_entity.forms.set(forms)

        response = self.client.post(
            reverse("submissions:submission_select_administrative_entity"),
            {"administrative_entity": administrative_entities[0].pk},
        )

        self.assertEqual(
            submissions_models.Submission.objects.filter(
                administrative_entity=administrative_entities[0],
            ).count(),
            1,
        )
        self.assertEqual(
            list(
                submissions_models.Submission.objects.filter(
                    administrative_entity=administrative_entities[0],
                )
                .get()
                .forms.all()
            ),
            [],
        )
        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_select_forms",
                kwargs={
                    "submission_id": submissions_models.Submission.objects.get().pk
                },
            ),
        )

    def test_administrative_entity_is_filtered_by_tag(self):
        administrative_entities = [
            factories.AdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        forms = forms_models.Form.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.forms.set(forms)

        response = self.client.get(
            reverse("submissions:submission_select_administrative_entity"),
            {"entityfilter": "first"},
            follow=True,
        )

        new_submission = submissions_models.Submission.objects.last()

        response2 = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
                kwargs={"submission_id": new_submission.id},
            ),
            {"entityfilter": "first"},
            follow=True,
        )
        parser2 = get_parser(response2.content)
        content2 = response2.content.decode()
        element_parsed = parser2.select(".form-check-label")

        # Check that selected item is there
        self.assertEqual(1, len(element_parsed))
        # Check that filtered items are NOT there
        self.assertNotContains(response, administrative_entities[1].name)
        self.assertNotContains(response, administrative_entities[2].name)
        self.assertInHTML(administrative_entities[0].name, content2)

    def test_wrong_administrative_entity_tag_return_all_administratives_entities(self):
        administrative_entities = [
            factories.AdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        forms = forms_models.Form.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.forms.set(forms)

        response = self.client.get(
            reverse("submissions:submission_select_administrative_entity"),
            {"entityfilter": "wrongtag"},
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        content = response.content.decode()

        self.assertEqual(3, len(element_parsed))
        self.assertInHTML(administrative_entities[0].name, content)
        self.assertInHTML(administrative_entities[1].name, content)
        self.assertInHTML(administrative_entities[2].name, content)

    def test_multiple_administrative_entity_tags_return_multiple_administratives_entities(
        self,
    ):
        administrative_entities = [
            factories.AdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        forms = forms_models.Form.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.forms.set(forms)

        response = self.client.get(
            reverse("submissions:submission_select_administrative_entity"),
            {"entityfilter": ["first", "second"]},
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        content = response.content.decode()

        self.assertEqual(2, len(element_parsed))
        self.assertInHTML(administrative_entities[0].name, content)
        self.assertInHTML(administrative_entities[1].name, content)

    def test_form_category_is_filtered_by_tag(self):
        additional_form_category = factories.FormCategoryFactory()

        factories.FormFactory(
            category=additional_form_category,
            is_public=True,
        )

        self.form_categories[0].tags.add("form_category_a")
        self.form_categories[1].tags.add("form_category_a")
        additional_form_category.tags.add("form_category_b")
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
            + "?typefilter=form_category_a"
        )

        parser = get_parser(response.content)
        element_parsed = parser.select("#id_forms-selected_forms label")

        # Check that 2 forms are visibles
        self.assertEqual(2, len(element_parsed))

    def test_form_category_is_not_filtered_by_bad_tag(self):
        additional_form_category = factories.FormCategoryFactory()

        forms_models.Form.objects.create(
            category=additional_form_category,
            is_public=True,
        )

        self.form_categories[0].tags.add("form_category_a")
        self.form_categories[1].tags.add("form_category_a")
        additional_form_category.tags.add("form_category_b")
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(forms_models.Form.objects.all())

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
            + "?typefilter=badtag"
        )

        parser = get_parser(response.content)
        element_parsed = parser.select("#id_forms-selected_forms label")

        # Check that 3 forms are visibles
        self.assertEqual(3, len(element_parsed))

    def test_missing_mandatory_list_values_show_error(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        form = submission.forms.first()
        submission.administrative_entity.forms.set(submission.forms.all())
        list_single_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_SINGLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        list_multiple_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        for field in [list_single_field, list_multiple_field]:
            field.forms.set(submission.forms.all())

        data = {
            f"fields-{form.pk}_{list_single_field.pk}": "",
        }

        response = self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )
        self.assertFormError(
            response,
            "submission_form",
            f"{form.pk}_{list_single_field.pk}",
            ["Ce champ est obligatoire."],
        )
        self.assertFormError(
            response,
            "submission_form",
            f"{form.pk}_{list_multiple_field.pk}",
            ["Ce champ est obligatoire."],
        )

    def test_list_multiple_value_is_stored_as_list(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        form = submission.forms.first()
        submission.administrative_entity.forms.set(submission.forms.all())
        list_multiple_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
        )
        list_multiple_field.forms.set(submission.forms.all())

        data = {
            f"fields-{form.pk}_{list_multiple_field.pk}": [
                "foo",
                "bar",
            ],
        }
        response = self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )
        self.assertEqual(
            submissions_models.FieldValue.objects.first().get_value(),
            ["foo", "bar"],
        )

    def test_list_single_value_is_stored_as_list(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        form = submission.forms.first()
        submission.administrative_entity.forms.set(submission.forms.all())
        list_multiple_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
        )
        list_multiple_field.forms.set(submission.forms.all())

        data = {f"fields-{form.pk}_{list_multiple_field.pk}": "foo"}

        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )
        self.assertEqual(
            submissions_models.FieldValue.objects.first().get_value(),
            ["foo"],
        )

    def test_input_is_restricted_to_list_values(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        form = submission.forms.first()
        submission.administrative_entity.forms.set(submission.forms.all())
        list_single_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_SINGLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        list_multiple_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        for field in [list_single_field, list_multiple_field]:
            field.forms.set(submission.forms.all())

        data = {
            f"fields-{form.pk}_{list_single_field.pk}": "baz",
            f"fields-{form.pk}_{list_multiple_field.pk}": ["baz"],
        }

        response = self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )

        self.assertFormError(
            response,
            "submission_form",
            f"{form.pk}_{list_single_field.pk}",
            ["Sélectionnez un choix valide. baz n’en fait pas partie."],
        )
        self.assertFormError(
            response,
            "submission_form",
            f"{form.pk}_{list_multiple_field.pk}",
            ["Sélectionnez un choix valide. baz n’en fait pas partie."],
        )

    def test_file_input_extensions_restrictions_sets_accept_correctly_in_template(self):

        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory()
        submission.administrative_entity.forms.set([form])
        submission.forms.set([form])
        field = factories.FieldFactory(
            input_type=forms_models.Field.INPUT_TYPE_FILE,
            allowed_file_types="jpg,png",
        )
        field.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_appendices",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)
        items = parser.select(".form-control-file")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(items[0].has_attr("accept"), True)
        self.assertIn("image/jpeg", items[0]["accept"])
        self.assertIn("image/png", items[0]["accept"])


class SubmissionProlongationTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.form_normal = factories.FormFactory()
        self.form_normal_no_date = factories.FormFactory(needs_date=False)
        self.form_prolongable_no_date = factories.FormFactory(
            needs_date=False,
            permit_duration=30,
        )
        self.form_prolongable_with_date = factories.FormFactory(
            needs_date=True,
            permit_duration=60,
        )
        self.form_prolongable_no_date_with_reminder = factories.FormFactory(
            needs_date=False,
            permit_duration=90,
            expiration_reminder=True,
            days_before_reminder=5,
        )
        self.form_prolongable_with_date_and_reminder = factories.FormFactory(
            needs_date=True,
            permit_duration=120,
            expiration_reminder=True,
            days_before_reminder=10,
        )

        secretary_group = factories.GroupFactory(name="Secrétariat")
        self.department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        self.secretariat = factories.SecretariatUserFactory(
            groups=[secretary_group], email="secretary@geocity.ch"
        )

    def test_user_cannot_request_submission_prolongation_if_submission_is_not_prolongable(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        submission.forms.set([self.form_normal])
        factories.SubmissionGeoTimeFactory(submission=submission)

        # Submission list
        response = self.client.get(
            reverse(
                "submissions:submissions_list",
            )
        )
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Demander une prolongation")

        # Prolongation form
        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
        )
        parser = get_parser(response.content)
        alert = parser.find(
            "div", string="La demande de permis ne peut pas être prolongée."
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_user_cannot_request_submission_prolongation_if_his_prolongation_is_processing(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_PROCESSING,
            prolongation_status=submissions_models.Submission.PROLONGATION_STATUS_PENDING,
            prolongation_date=timezone.now() + datetime.timedelta(days=90),
        )
        submission.forms.set([self.form_prolongable_with_date])
        factories.SubmissionGeoTimeFactory(submission=submission)

        # Prolongation form
        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
        )
        parser = get_parser(response.content)
        regex = re.compile(
            r"^Une demande de prolongation pour le permis #[0-9]* est en attente ou a été refusée."
        )
        alert = parser.find("div", string=regex)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_user_cannot_request_submission_prolongation_if_it_has_been_rejected(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT,
            prolongation_status=submissions_models.Submission.PROLONGATION_STATUS_REJECTED,
            prolongation_date=timezone.now() + datetime.timedelta(days=90),
        )
        submission.forms.set([self.form_prolongable_with_date])
        factories.SubmissionGeoTimeFactory(submission=submission)

        # Prolongation form
        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
        )
        parser = get_parser(response.content)
        regex = re.compile(
            r"^Une demande de prolongation pour le permis #[0-9]* est en attente ou a été refusée."
        )
        alert = parser.find("div", string=regex)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_secretariat_cannot_request_submission_prolongation_via_form_if_it_is_not_the_author(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_AWAITING_SUPPLEMENT,
        )
        submission.forms.set([self.form_prolongable_no_date_with_reminder])
        factories.SubmissionGeoTimeFactory(submission=submission)

        submission.administrative_entity.departments.set([self.department])

        self.client.login(username=self.secretariat, password="password")

        # Prolongation form
        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)
        regex = re.compile(
            r"^Vous ne pouvez pas demander une prolongation pour le permis"
        )
        alert = parser.find("div", string=regex)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_user_can_request_submission_prolongation(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_APPROVED
        )
        submission.forms.set([self.form_prolongable_with_date_and_reminder])
        factories.SubmissionGeoTimeFactory(submission=submission)
        submission.administrative_entity.departments.set([self.department])

        # Prolongation form
        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
        )
        parser = get_parser(response.content)

        title = parser.find("h3", string="Demande de prolongation de permis")
        widget = parser.find(
            "input",
            title="Cliquer sur le champ et sélectionner la nouvelle date de fin planifiée",
        )

        self.assertEqual(1, len(title))
        self.assertEqual("id_prolongation_date", widget.get("id"))

        # Post
        prolongation_date = timezone.now() + datetime.timedelta(days=90)

        response = self.client.post(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
            data={"prolongation_date": prolongation_date},
        )

        parser = get_parser(response.content)
        regex = re.compile(r"^Prolongation en attente")
        icon_prolongation_processing = parser.findAll("i", title=regex)
        icon_submission_expired = parser.findAll("i", title="Demande échue")
        expected_subject_regex = re.compile(
            r"Une demande de prolongation vient d'être soumise"
        )

        submission.refresh_from_db()

        self.assertRedirects(response, reverse("submissions:submissions_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(icon_prolongation_processing))
        self.assertEqual(1, len(icon_submission_expired))
        self.assertEqual(
            submissions_models.Submission.PROLONGATION_STATUS_PENDING,
            submission.prolongation_status,
        )
        self.assertEqual(prolongation_date, submission.prolongation_date)
        # Emails
        self.assertIn("secretary@geocity.ch", mail.outbox[0].to)
        self.assertRegex(mail.outbox[0].subject, expected_subject_regex)
        self.assertRegex(mail.outbox[0].message().as_string(), expected_subject_regex)

    def test_submission_prolongation_request_must_be_after_original_end_date(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_APPROVED
        )
        submission.forms.set([self.form_prolongable_with_date_and_reminder])
        factories.SubmissionGeoTimeFactory(
            submission=submission,
            starts_at=timezone.now() - datetime.timedelta(days=30),
            ends_at=timezone.now(),
        )

        # Post

        response = self.client.post(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
            data={"prolongation_date": timezone.now() - datetime.timedelta(days=1)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "La date de prolongation doit être postérieure à la date originale de fin",
        )

    # TESTS FOR THE SECRETARIAT
    def test_secretariat_can_prolonge_or_submission_without_user_asking(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        submission.forms.set([self.form_prolongable_with_date])
        factories.SubmissionGeoTimeFactory(submission=submission)
        submission.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        # Prolongation form on submission details
        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)

        prolong_form_div = parser.find("div", id="prolong")
        prolong_form = prolong_form_div.find("form")
        no_requested_prolongation_msg = prolong_form.find("small")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(no_requested_prolongation_msg))

        # Post the form
        prolongation_date = timezone.now() + datetime.timedelta(days=90)

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
            data={
                "prolongation_date": prolongation_date,
                "prolongation_status": submissions_models.Submission.PROLONGATION_STATUS_APPROVED,
                "prolongation_comment": "Prolonged! I got the power!",
                "action": submissions_models.ACTION_PROLONG,
            },
        )
        submission.refresh_from_db()

        parser = get_parser(response.content)

        regex = re.compile(r"^Prolongation en attente")
        icon_prolongation_processing = parser.findAll("i", title=regex)
        icon_prolongation_approved = parser.findAll("i", title="Demande renouvelée")
        expected_subject_regex = re.compile(
            r"^La prolongation de votre demande a été acceptée \(.*\)$"
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("submissions:submissions_list"))
        self.assertEqual(0, len(icon_prolongation_processing))
        self.assertEqual(1, len(icon_prolongation_approved))
        self.assertEqual(
            submissions_models.Submission.PROLONGATION_STATUS_APPROVED,
            submission.prolongation_status,
        )
        self.assertEqual(prolongation_date, submission.prolongation_date)
        self.assertEqual("Prolonged! I got the power!", submission.prolongation_comment)

        self.assertIn("user@test.com", mail.outbox[0].to)
        self.assertRegex(mail.outbox[0].subject, expected_subject_regex)
        self.assertIn(
            "Nous vous informons que votre demande de prolongation a été traitée.",
            mail.outbox[0].message().as_string(),
        )

    def test_secretariat_can_reject_submission(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        submission.forms.set([self.form_prolongable_with_date])
        factories.SubmissionGeoTimeFactory(submission=submission)
        submission.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        # Post the form
        prolongation_date = timezone.now() + datetime.timedelta(days=90)

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
            data={
                "prolongation_date": prolongation_date,
                "prolongation_status": submissions_models.Submission.PROLONGATION_STATUS_REJECTED,
                "prolongation_comment": "Rejected! Because I say so!",
                "action": submissions_models.ACTION_PROLONG,
            },
        )
        submission.refresh_from_db()

        parser = get_parser(response.content)

        regex = re.compile(r"^Prolongation en attente")
        icon_prolongation_processing = parser.findAll("i", title=regex)
        icon_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")
        expected_subject_regex = re.compile(
            r"^La prolongation de votre demande a été refusée \(.*\)$"
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("submissions:submissions_list"))
        self.assertEqual(0, len(icon_prolongation_processing))
        self.assertEqual(1, len(icon_prolongation_rejected))
        self.assertEqual(
            submissions_models.Submission.PROLONGATION_STATUS_REJECTED,
            submission.prolongation_status,
        )
        self.assertEqual(prolongation_date, submission.prolongation_date)
        self.assertEqual("Rejected! Because I say so!", submission.prolongation_comment)

        self.assertRegex(mail.outbox[0].subject, expected_subject_regex)
        self.assertIn(
            "Nous vous informons que votre demande de prolongation a été traitée.",
            mail.outbox[0].message().as_string(),
        )

    def test_secretariat_prolonge_form_is_disabled_on_bad_submission_status(
        self,
    ):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=submissions_models.Submission.STATUS_RECEIVED,
        )
        submission.forms.set([self.form_prolongable_with_date])
        factories.SubmissionGeoTimeFactory(submission=submission)
        submission.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        # Prolongation form on submission details
        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

        parser = get_parser(response.content)
        prolong_form_div = parser.find("div", id="prolong")
        prolong_form = prolong_form_div.find("form")
        self.assertTrue("disabled" in str(prolong_form))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_see_prolongation_icons_nor_info_if_expired_submission_is_draft(
        self,
    ):
        # Draft - No action icons - No expired/renew icons

        submission_draft = factories.SubmissionFactory(
            validated_at=timezone.now(),
            status=submissions_models.Submission.STATUS_DRAFT,
            author=self.user,
        )
        submission_draft.forms.set([self.form_normal])
        ends_at_draft = timezone.now()
        factories.SubmissionGeoTimeFactory(
            submission=submission_draft,
            starts_at=timezone.now() - datetime.timedelta(days=30),
            ends_at=ends_at_draft,
        )
        response = self.client.get(
            reverse(
                "submissions:submissions_list",
            )
        )
        parser = get_parser(response.content)

        info_expired_submission = parser.findAll("i", title="Demande échue")
        info_prolonged_submission = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_submission))
        self.assertEqual(0, len(info_prolonged_submission))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_icons_if_submission_is_about_to_expire(
        self,
    ):
        # Expired within delay of reminder  - Action icon - No expired/renew icons
        submission_expired = factories.SubmissionFactory(
            validated_at=timezone.now(),
            status=submissions_models.Submission.STATUS_APPROVED,
            author=self.user,
        )
        submission_expired.forms.set([self.form_prolongable_with_date_and_reminder])
        ends_at_expired = timezone.now() + datetime.timedelta(days=5)
        factories.SubmissionGeoTimeFactory(
            submission=submission_expired,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_expired,
        )

        response = self.client.get(
            reverse(
                "submissions:submissions_list",
            )
        )
        parser = get_parser(response.content)

        info_expired_submission = parser.findAll("i", title="Demande échue")
        info_prolonged_submission = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_submission))
        self.assertEqual(0, len(info_prolonged_submission))
        self.assertEqual(1, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_info_icons_if_submission_is_prolonged(
        self,
    ):
        # Prolonged  - No action icons - Renew icons - Date fin = prolongation_date
        prolongation_date_prolonged = timezone.now() + datetime.timedelta(days=365)
        submission_prolonged = factories.SubmissionFactory(
            validated_at=timezone.now(),
            status=submissions_models.Submission.STATUS_APPROVED,
            author=self.user,
            prolongation_date=prolongation_date_prolonged,
            prolongation_status=submissions_models.Submission.PROLONGATION_STATUS_APPROVED,
        )
        submission_prolonged.forms.set([self.form_prolongable_with_date_and_reminder])
        ends_at_prolonged = timezone.now() + datetime.timedelta(days=5)
        factories.SubmissionGeoTimeFactory(
            submission=submission_prolonged,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_prolonged,
        )

        response = self.client.get(
            reverse(
                "submissions:submissions_list",
            )
        )
        parser = get_parser(response.content)

        info_expired_submission = parser.findAll("i", title="Demande échue")
        info_prolonged_submission = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_submission))
        self.assertEqual(1, len(info_prolonged_submission))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_info_icons_if_submission_prolongation_is_requested(
        self,
    ):

        # Prolongation Requested
        prolongation_date_requested = timezone.now() + datetime.timedelta(days=365)
        submission_prolongation_requested = factories.SubmissionFactory(
            validated_at=timezone.now(),
            status=submissions_models.Submission.STATUS_APPROVED,
            author=self.user,
            prolongation_date=prolongation_date_requested,
            prolongation_status=submissions_models.Submission.PROLONGATION_STATUS_PENDING,
        )
        submission_prolongation_requested.forms.set(
            [self.form_prolongable_no_date_with_reminder]
        )
        ends_at_requested = timezone.now() + datetime.timedelta(days=4)
        factories.SubmissionGeoTimeFactory(
            submission=submission_prolongation_requested,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_requested,
        )

        response = self.client.get(
            reverse(
                "submissions:submissions_list",
            )
        )
        parser = get_parser(response.content)

        info_expired_submission = parser.findAll("i", title="Demande échue")
        info_prolonged_submission = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_submission))
        self.assertEqual(0, len(info_prolonged_submission))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(1, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_info_icons_if_submission_prolongation_is_rejected(
        self,
    ):

        # Prolongation Rejected
        prolongation_date_rejected = timezone.now() + datetime.timedelta(days=300)
        submission_prolongation_rejected = factories.SubmissionFactory(
            validated_at=timezone.now(),
            status=submissions_models.Submission.STATUS_APPROVED,
            author=self.user,
            prolongation_date=prolongation_date_rejected,
            prolongation_status=submissions_models.Submission.PROLONGATION_STATUS_REJECTED,
        )
        submission_prolongation_rejected.forms.set(
            [self.form_prolongable_no_date_with_reminder]
        )
        ends_at_rejected = timezone.now() - datetime.timedelta(days=3)
        factories.SubmissionGeoTimeFactory(
            submission=submission_prolongation_rejected,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_rejected,
        )

        response = self.client.get(
            reverse(
                "submissions:submissions_list",
            )
        )
        parser = get_parser(response.content)

        info_expired_submission = parser.findAll("i", title="Demande échue")
        info_prolonged_submission = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(info_expired_submission))
        self.assertEqual(0, len(info_prolonged_submission))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(1, len(action_prolongation_rejected))

    def test_secretariat_can_see_prolongation_buttons_if_form_has_prolongation_enabled(
        self,
    ):

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        submission.forms.set([self.form_prolongable_with_date])
        submission.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#prolong button")),
            2,
        )

    def test_secretariat_can_see_prolongation_buttons_if_at_least_one_form_has_prolongation_enabled(
        self,
    ):

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        submission.forms.set([self.form_prolongable_with_date, self.form_normal])
        submission.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#prolong button")),
            2,
        )

    def test_secretariat_cannot_see_prolongation_buttons_if_form_has_not_prolongation_enabled(
        self,
    ):

        submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_APPROVED,
        )
        submission.forms.set([self.form_normal])
        submission.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#prolong button")),
            0,
        )


class SubmissionActorsTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.test_formset_data = {
            "form-TOTAL_FORMS": ["1"],
            "form-INITIAL_FORMS": ["0"],
            "form-MIN_NUM_FORMS": ["0"],
            "form-MAX_NUM_FORMS": ["1000"],
            "creditor_type": [""],
            "form-0-contact_form": "",
            "form-0-first_name": ["John"],
            "form-0-last_name": ["Doe"],
            "form-0-phone": ["000 000 00 00"],
            "form-0-email": ["john@doe.com"],
            "form-0-address": ["Main street 1"],
            "form-0-zipcode": ["2000"],
            "form-0-city": ["City"],
            "form-0-company_name": [""],
            "form-0-vat_number": [""],
            "form-0-id": [""],
        }

    def test_submission_contact_creates(self):
        form = factories.FormFactory()
        form_category = form.category

        contact_required = factories.ContactFormFactory(
            is_mandatory=True, form_category=form_category
        )

        self.test_formset_data["form-0-contact_form"] = contact_required.type.id

        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_DRAFT
        )

        submission.administrative_entity.forms.set([form])
        submission.forms.set([form])
        field = factories.FieldFactory()
        field.forms.set([form])

        self.client.post(
            reverse(
                "submissions:submission_contacts",
                kwargs={"submission_id": submission.pk},
            ),
            data=self.test_formset_data,
        )

        contacts = list(submission.contacts.all())
        self.assertEqual(len(contacts), 1, "Expected 1 contact created")
        self.assertEqual(contacts[0].first_name, "John")

    def test_submission_contact_required_cannot_have_empty_field(self):
        form = factories.FormFactory()
        form_category = form.category

        contact_required = factories.ContactFormFactory(
            is_mandatory=True, form_category=form_category
        )

        self.test_formset_data["form-0-contact_form"] = contact_required.type

        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_DRAFT
        )

        submission.administrative_entity.forms.set([form])
        submission.forms.set([form])
        field = factories.FieldFactory()
        field.forms.set([form])

        self.test_formset_data["form-0-last_name"] = ""

        response = self.client.post(
            reverse(
                "submissions:submission_contacts",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
            data=self.test_formset_data,
        )

        submission.refresh_from_db()
        # Check that no userprofile was saved for this submission
        self.assertEqual(submission.contacts.count(), 0)
        # Check that if form not valid, it does not redirect
        self.assertEqual(response.status_code, 200)

    def test_submission_contact_creditor_field_is_hidden_if_form_is_not_paid(self):
        form = factories.FormFactory(requires_payment=False)
        form_category = form.category

        factories.ContactFormFactory(is_mandatory=True, form_category=form_category)

        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_DRAFT
        )

        submission.forms.set([form])

        response = self.client.get(
            reverse(
                "submissions:submission_contacts",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)

        self.assertEqual(
            len(parser.findAll(text=re.compile("Renseignez les contacts"))), 1
        )
        self.assertIsNone(parser.find(id="id_creditor_type"))
        self.assertEqual(
            len(
                parser.findAll(
                    text=re.compile(
                        "Adresse de facturation si différente de celle de l'auteur"
                    )
                )
            ),
            0,
        )

    def test_submission_contact_creditor_field_is_shown_if_at_least_one_form_requires_payment(
        self,
    ):

        free_forms = factories.FormFactory.create_batch(2, requires_payment=False)
        paid_form = factories.FormFactory(requires_payment=True)
        form_categories = [form.category for form in free_forms] + [paid_form.category]

        for form_category in form_categories:
            factories.ContactFormFactory(is_mandatory=True, form_category=form_category)

        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_DRAFT
        )

        submission.forms.set(free_forms + [paid_form])

        response = self.client.get(
            reverse(
                "submissions:submission_contacts",
                kwargs={"submission_id": submission.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)

        self.assertEqual(
            len(parser.findAll(text=re.compile("Renseignez les contacts"))), 1
        )
        self.assertGreaterEqual(len(parser.find(id="id_creditor_type")), 1)
        self.assertEqual(
            len(
                parser.findAll(
                    text=re.compile(
                        "Adresse de facturation si différente de celle de l'auteur"
                    )
                )
            ),
            1,
        )


class OnlinePaymentTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        entity = factories.AdministrativeEntityFactory(is_single_form_submissions=True)

        self.parent_type = factories.ParentComplementaryDocumentTypeFactory()
        self.child_type = factories.ChildComplementaryDocumentTypeFactory(
            parent=self.parent_type
        )

        self.parent_type2 = factories.ParentComplementaryDocumentTypeFactory(
            form=self.parent_type.form
        )
        self.child_type2 = factories.ChildComplementaryDocumentTypeFactory(
            parent=self.parent_type
        )

        prices = factories.PriceFactory.create_batch(4)
        self.payment_settings = factories.PaymentSettingsFactory()

        self.secretariat = factories.SecretariatUserFactory()
        entity.integrator = self.secretariat.groups.first()
        entity.save()

        Report.create_default_report(entity.id)

        report = Report.objects.filter(
            integrator=self.secretariat.groups.first()
        ).first()

        report.document_types.set([self.child_type])
        self.payment_settings.payment_confirmation_report = report
        self.payment_settings.payment_refund_report = report
        self.payment_settings.integrator = self.secretariat.groups.first()
        self.payment_settings.save()

        self.parent_type.form.payment_settings = self.payment_settings
        self.parent_type.form.prices.set(prices)
        self.parent_type.form.save()

        self.parent_type.form.requires_payment = False
        self.parent_type.form.requires_online_payment = True
        self.parent_type.form.has_geometry_point = False
        self.parent_type.form.has_geometry_line = False
        self.parent_type.form.has_geometry_polygon = False
        self.parent_type.form.needs_date = False
        self.parent_type.form.save()

        entity.forms.set([self.parent_type.form])

    def _add_fields_to_form(self):
        list_single_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_SINGLE,
            choices="foo\nbar",
            is_mandatory=False,
        )
        list_multiple_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
            is_mandatory=False,
        )
        for field in [list_single_field, list_multiple_field]:
            field.forms.set([self.parent_type.form])
        return list_single_field, list_multiple_field

    def _add_fields_select_price_and_save(self, submission, override_data=None):
        list_single_field, list_multiple_field = self._add_fields_to_form()

        data = {
            "selected_price": self.parent_type.form.prices.first().pk,
            f"fields-{self.parent_type.form.pk}_{list_single_field.pk}": "foo",
            f"fields-{self.parent_type.form.pk}_{list_multiple_field.pk}": ["bar"],
        }
        if override_data:
            data.update(override_data)

        return self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )

    def test_free_price_and_submit(self):
        free_price = factories.PriceFactory.create(amount=0)
        self.parent_type.form.prices.add(free_price)

        submission = factories.SubmissionFactory(
            author=self.user,
        )
        submission.forms.set([self.parent_type.form])
        response = self._add_fields_select_price_and_save(
            submission, {"selected_price": free_price.pk}
        )
        assert response.status_code == 302

        response = self.client.get(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        content = response.content.decode()
        self.assertIn("/submitconfirmed/", content)
        self.assertNotIn("/submissions/payment/", content)

    def test_price_selection_and_submit_page(self):
        submission = factories.SubmissionFactory(
            author=self.user,
        )
        submission.forms.set([self.parent_type.form])

        response = self._add_fields_select_price_and_save(submission)

        assert response.status_code == 302

        response = self.client.get(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )

        content = response.content.decode()

        self.assertInHTML("Payer maintenant", content)
        self.assertIn("/submissions/payment/", content)

    def test_price_is_required_to_be_selected_in_submit_page(self):
        submission = factories.SubmissionFactory(
            author=self.user,
        )
        submission.forms.set([self.parent_type.form])

        self._add_fields_to_form()

        response = self.client.get(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )

        assert "Vous devez choisir un tarif" in response.content.decode()

    def test_price_selection_in_prolongation_page(self):
        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_APPROVED
        )

        self.parent_type.form.needs_date = True
        self.parent_type.form.permit_duration = 120
        self.parent_type.form.expiration_reminder = True
        self.parent_type.form.days_before_reminder = 10
        self.parent_type.form.save()

        submission.forms.set([self.parent_type.form])

        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            )
        )
        content = response.content.decode()
        self.assertInHTML("Payer", content)

    def test_single_price_is_preselected_in_prolongation_page(self):
        submission = factories.SubmissionFactory(
            author=self.user, status=submissions_models.Submission.STATUS_APPROVED
        )

        price = factories.PriceFactory()
        self.parent_type.form.prices.set([price])
        self.parent_type.form.needs_date = True
        self.parent_type.form.permit_duration = 120
        self.parent_type.form.expiration_reminder = True
        self.parent_type.form.days_before_reminder = 10
        self.parent_type.form.save()

        submission.forms.set([self.parent_type.form])

        response = self.client.get(
            reverse(
                "submissions:submission_prolongation",
                kwargs={"submission_id": submission.pk},
            )
        )
        assert response.context["prices_form"].initial["selected_price"] == price.pk


class AdministrativeEntitySecretaryEmailTestcase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(email="user@geocity.com")
        self.administrative_entity_expeditor = factories.AdministrativeEntityFactory(
            expeditor_email="geocity_rocks@geocity.ch",
            expeditor_name="Geocity Rocks",
        )
        self.group = factories.SecretariatGroupFactory(
            department__administrative_entity=self.administrative_entity_expeditor
        )
        self.secretary = factories.SecretariatUserFactory(groups=[self.group])
        self.client.login(username=self.secretary.username, password="password")

        self.submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity_expeditor,
            author=self.user,
        )

    def test_secretary_email_and_name_are_set_for_the_administrative_entity(self):
        form = factories.FormFactory()
        form_name = form.name
        self.submission.forms.set([form])

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_RECEIVED,
                "action": submissions_models.ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].from_email, "Geocity Rocks <geocity_rocks@geocity.ch>"
        )
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

    def test_just_secretary_email_is_set_for_the_administrative_entity(self):
        form = factories.FormFactory()
        form_name = form.name
        self.submission.forms.set([form])
        self.administrative_entity_expeditor = (
            submissions_models.AdministrativeEntity.objects.first()
        )
        self.administrative_entity_expeditor.expeditor_email = (
            "geocity_rocks@geocity.ch"
        )
        self.administrative_entity_expeditor.expeditor_name = ""
        self.administrative_entity_expeditor.save()
        self.administrative_entity_expeditor.refresh_from_db()

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_RECEIVED,
                "action": submissions_models.ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "<geocity_rocks@geocity.ch>")
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

    def test_no_secretary_email_is_set_for_the_administrative_entity(self):
        form = factories.FormFactory()
        form_name = form.name
        self.submission.forms.set([form])
        self.administrative_entity_expeditor = (
            submissions_models.AdministrativeEntity.objects.first()
        )
        self.administrative_entity_expeditor.expeditor_email = ""
        self.administrative_entity_expeditor.expeditor_name = "Geocity Rocks"
        self.administrative_entity_expeditor.save()
        self.administrative_entity_expeditor.refresh_from_db()

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
            data={
                "status": submissions_models.Submission.STATUS_RECEIVED,
                "action": submissions_models.ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

        self.assertNotEqual(mail.outbox[0].from_email, "geocity_rocks@geocity.ch")
        self.assertEqual(mail.outbox[0].from_email, "your_noreply_email")
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


class SubmissionAnonymousTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def test_anonymous_request_on_non_anonymous_entity_returns_404(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        category = factories.FormCategoryFactory(tags=["a"])

        response = self.client.get(
            reverse("submissions:anonymous_submission"),
            data={
                "entityfilter": entity.tags.get().slug,
                "typefilter": category.tags.get().slug,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_request_on_anonymous_entity_displays_captcha_form(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        entity.create_anonymous_user()

        category = factories.FormCategoryFactory(tags=["a"])

        response = self.client.get(
            reverse("submissions:anonymous_submission"),
            data={
                "entityfilter": entity.tags.get().slug,
                "typefilter": category.tags.get().slug,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("anonymous_request_form", response.context)

    def test_anonymous_request_temporary_logged_in_no_form_displays_request_form(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        entity.create_anonymous_user()

        temp_author = accounts_models.UserProfile.objects.create_temporary_user(entity)
        self.client.force_login(temp_author.user)
        session = self.client.session
        session["anonymous_request_token"] = hash((temp_author, entity))
        session.save()

        category = factories.FormCategoryFactory(tags=["a"])

        response = self.client.get(
            reverse("submissions:anonymous_submission"),
            data={
                "entityfilter": entity.tags.get().slug,
                "typefilter": category.tags.get().slug,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_request_temporary_logged_in_displays_request_form(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        entity.create_anonymous_user()

        temp_author = accounts_models.UserProfile.objects.create_temporary_user(entity)
        self.client.force_login(temp_author.user)
        session = self.client.session
        session["anonymous_request_token"] = hash((temp_author, entity))
        session.save()

        category = factories.FormCategoryFactory(tags=["a"])
        factories.FormFactory(
            is_anonymous=True,
            category=category,
            administrative_entities=[entity],
        )

        response = self.client.get(
            reverse("submissions:anonymous_submission"),
            data={
                "entityfilter": entity.tags.get().slug,
                "typefilter": category.tags.get().slug,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        # As the form has to fields, going directly to next step
        self.assertTrue(
            isinstance(
                response.context["formset"].forms[0],
                submissions_forms.SubmissionGeoTimeForm,
            )
        )

    def test_anonymous_request_submission_deletes_temporary_user(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        entity.create_anonymous_user()

        temp_author = accounts_models.UserProfile.objects.create_temporary_user(entity)
        self.client.force_login(temp_author.user)
        session = self.client.session
        session["anonymous_request_token"] = hash((temp_author, entity))
        session.save()

        category = factories.FormCategoryFactory(tags=["a"])
        form = factories.FormWithoutGeometryFactory(
            is_anonymous=True,
            category=category,
            administrative_entities=[entity],
            needs_date=False,
        )

        # Filled submission
        submission = factories.SubmissionFactory(
            author=temp_author.user,
            status=submissions_models.Submission.STATUS_DRAFT,
            administrative_entity=entity,
        )
        selected_form = factories.SelectedFormFactory(
            submission=submission,
            form=form,
        )
        field = factories.FieldFactory()
        field.forms.set([form])
        factories.FieldValueFactory(
            field=field,
            selected_form=selected_form,
            value={"val": True},
        )

        response = self.client.post(
            reverse(
                "submissions:submission_submit_confirmed",
                kwargs={"submission_id": submission.pk},
            )
        )

        submission.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("submissions:anonymous_submission_sent"))
        self.assertEqual(submission.author, entity.anonymous_user.user)

        self.assertEqual(
            get_user_model().objects.get().pk,
            submission.author.id,
        )
