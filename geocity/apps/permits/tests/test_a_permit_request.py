# TODO split this file into multiple files
import datetime
import io
import re
import urllib.parse
import uuid
from datetime import date

import tablib
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from geocity.apps.permits import services

# Import models of different apps
from geocity.apps.accounts.models import *
from geocity.apps.forms.models import *
from geocity.apps.reports.models import *
from geocity.apps.submissions.models import *

from geocity.apps.submissions.forms import SubmissionGeoTimeForm
from ..management.commands import create_anonymous_users
from . import factories
from .utils import LoggedInSecretariatMixin, LoggedInUserMixin, get_emails, get_parser


def to_forms_dict(forms):
    return {
        "forms-{}".format(form.form_category.pk): form.pk
        for form in forms
    }


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

        Form.objects.create(
            category=self.form_categories[0],
            is_public=True,
        )
        Form.objects.create(
            category=self.form_categories[1],
            is_public=True,
        )
        self.geotime_step_formset_data = {
            "form-TOTAL_FORMS": ["1"],
            "form-INITIAL_FORMS": ["0"],
            "form-MIN_NUM_FORMS": ["0"],
        }

    def test_categories_step_submit_redirects_to_forms_with_categories_qs(self):
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(
            Form.objects.all()
        )

        response = self.client.post(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            ),
            data={"categories": [self.form_categories[0].pk, self.form_categories[1].pk]},
        )

        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
            + "?categories={}&categories={}".format(
                self.form_categories[0].pk, self.form_categories[1].pk
            ),
        )

    def test_forms_step_without_qs_redirects_to_categories_step(self):
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(
            Form.objects.all()
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
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            ),
        )

    def test_forms_step_submit_saves_multiple_selected_forms(self):
        submission = factories.SubmissionFactory(author=self.user)

        form = Form.objects.first()
        submission.administrative_entity.forms.set(
            Form.objects.all()
        )
        self.client.post(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
            + "?categories={}".format(self.form_categories[0].pk),
            data={
                "forms-{}".format(self.form_categories[0].pk): form.pk
            },
        )

        self.assertEqual(
            Submission.objects.filter(
                forms=form
            ).count(),
            1,
        )

    def test_categories_step_submit_redirects_to_detail_if_logged_as_backoffice(self):

        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )

        submission = factories.SubmissionFactory(
            author=self.user,
            status=Submission.STATUS_APPROVED,
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

    def test_categories_step_submit_redirects_to_detail_if_logged_as_integrator_admin(self):

        integrator_group = factories.GroupFactory(name="Integrator")
        department = factories.PermitDepartmentFactory(
            group=integrator_group, is_integrator_admin=True
        )

        submission = factories.SubmissionFactory(
            author=self.user,
            status=Submission.STATUS_APPROVED,
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
        factories.SelectedFormFactory.create_batch(
            3, submission=submission
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
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
        factories.SelectedFormFactory.create_batch(
            3, submission=submission
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/apps/permits/tests/files/real_jpg.jpg", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        field.forms.last().pk, field.pk
                    ): file
                },
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
        factories.SelectedFormFactory.create_batch(
            3, submission=submission
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/apps/permits/tests/files/real_png.png", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        field.forms.last().pk, field.pk
                    ): file
                },
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
        factories.SelectedFormFactory.create_batch(
            3, submission=submission
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open("geocity/apps/permits/tests/files/real_pdf.pdf", "rb") as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        field.forms.last().pk, field.pk
                    ): file
                },
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
        factories.SelectedFormFactory.create_batch(
            3, submission=submission
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open(
            "geocity/apps/permits/tests/files/unknow_type_for_filetype.txt", "rb"
        ) as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        field.forms.last().pk, field.pk
                    ): file
                },
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="Le type de unknow_type_for_filetype.txt n'est pas supporté, assurez-vous que votre fichier soit du bon type",
        )
        self.assertInHTML(expected, content)

    def test_documents_step_filetype_reject_not_allowed_extension(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(
            3, submission=submission
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open(
            "geocity/apps/permits/tests/files/not_allowed_docx.docx", "rb"
        ) as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        field.forms.last().pk, field.pk
                    ): file
                },
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="not_allowed_docx.docx n'est pas du bon type",
        )
        self.assertInHTML(expected, content)

    def test_documents_step_filetype_reject_fake_jpg_with_not_allowed_extension(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(
            3, submission=submission
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactoryTypeFile()
        field.forms.set(submission.forms.all())

        with open(
            "geocity/apps/permits/tests/files/not_allowed_bmp_as_jpg.jpg", "rb"
        ) as file:
            response = self.client.post(
                reverse(
                    "submissions:submission_appendices",
                    kwargs={"submission_id": submission.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        field.forms.last().pk, field.pk
                    ): file
                },
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="not_allowed_bmp_as_jpg.jpg n'est pas du bon type",
        )
        self.assertInHTML(expected, content)

    def test_user_can_only_see_own_requests(self):
        submission = factories.SubmissionFactory(
            author=factories.UserFactory()
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_non_draft_request(self):
        submission = factories.SubmissionFactory(
            author=self.user,
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
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
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
        )
        form = factories.FormFactory(can_always_update=True)
        factories.SelectedFormFactory(
            submission=submission,
            form=form,
        )
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
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

    def test_secretary_email_is_sent_when_user_treated_requested_complements(self):
        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        factories.SecretariatUserFactory(
            groups=[secretary_group], email="secretary@geocity.ch"
        )
        submission = factories.SubmissionFactory(
            status=Submission.STATUS_AWAITING_SUPPLEMENT,
            author=self.user,
            administrative_entity=department.administrative_entity,
        )
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormWithoutGeometryFactory(
            form_category=form_category,
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
            submission.status, Submission.STATUS_SUBMITTED_FOR_VALIDATION
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["secretary@geocity.ch"])
        self.assertEqual(
            mail.outbox[0].subject,
            "La demande de compléments a été traitée (Foo type)",
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
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user,
                status=Submission.STATUS_DRAFT,
            )
        ).submission
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
        submission.forms.set([form])

        self.client.post(
            reverse(
                "submissions:submission_submit",
                kwargs={"submission_id": submission.pk},
            )
        )
        emails = get_emails("Nouvelle demande (Foo type)")

        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0].to, ["secretariat@yverdon.ch"])

    def test_submit_submission_sends_email_to_services_to_notify_from_field(
        self,
    ):
        submission = factories.SubmissionGeoTimeFactory(
            submission=factories.SubmissionFactory(
                author=self.user,
                status=Submission.STATUS_DRAFT,
            )
        ).submission
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
        selected_form = factories.SelectedFormFactory(
            submission=submission,
            form=form,
        )

        field = factories.FieldFactory(
            services_to_notify="test-send-1@geocity.ch, test-send-2@geocity.ch, test-i-am-not-an-email,  ,\n\n\n",
            input_type=Field.INPUT_TYPE_CHECKBOX,
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
            "Votre service à été mentionné dans une demande (Foo type)",
        )
        self.assertIn(
            "Une nouvelle demande mentionnant votre service vient d'être soumise.",
            mail.outbox[0].message().as_string(),
        )

    def test_missing_mandatory_date_field_gives_invalid_feedback(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_DATE, is_mandatory=True
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
        submission = factories.SubmissionFactory(author=self.user)
        form = factories.FormFactory()
        submission.administrative_entity.forms.set(
            factories.FormFactory.create_batch(2, form=form)
        )
        form_category_id = (
            submission.administrative_entity.forms.values_list(
                "form_category_id", flat=True
            ).first()
        )

        self.client.post(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            ),
            data={"categories": [form_category_id]},
        )

        submission.refresh_from_db()
        forms = submission.forms.all()

        self.assertEqual(
            len(forms),
            1,
            "Submission should have one works object type set",
        )
        self.assertEqual(forms[0].form, form)
        self.assertEqual(forms[0].form_category_id, form_category_id)

    def test_form_category_automatically_set_when_only_one_form(self):
        form_category = factories.FormCategoryFactory()
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set(
            factories.FormFactory.create_batch(2, form_category=form_category)
        )

        response = self.client.post(
            reverse(
                "submissions:submission_select_administrative_entity",
            ),
            data={"administrative_entity": administrative_entity.pk},
        )

        submission = Submission.objects.get()

        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
            + f"?categories={form_category.pk}",
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
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user,
                status=Submission.STATUS_DRAFT,
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
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user,
                status=Submission.STATUS_DRAFT,
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
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user,
                status=Submission.STATUS_DRAFT,
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
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user,
                status=Submission.STATUS_DRAFT,
            )
        ).submission

        submission.forms.set(
            [first_form, second_form]
        )

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

    def test_administrative_entity_is_filtered_by_tag(self):
        administrative_entities = [
            factories.AdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        forms = Form.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.forms.set(forms)

        response = self.client.get(
            reverse("submissions:submission_select_administrative_entity"),
            {"entityfilter": "first"},
            follow=True,
        )

        new_submission = Submission.objects.last()

        content = response.content.decode()
        self.assertInHTML("Sélectionnez le ou les type(s)", content)
        self.assertRedirects(
            response,
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": new_submission.id},
            ),
        )

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
        forms = Form.objects.all()

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
        forms = Form.objects.all()

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
        additional_forms = factories.FormFactory()

        Form.objects.create(
            form_category=additional_form_category,
            form=additional_forms,
            is_public=True,
        )

        self.form_categories[0].tags.add("form_category_a")
        self.form_categories[1].tags.add("form_category_a")
        additional_form_category.tags.add("form_category_b")
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(
            Form.objects.all()
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            )
            + "?categoryfilter=form_category_a"
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        # Check that 2 forms are visibles
        self.assertEqual(2, len(element_parsed))

    def test_form_category_is_not_filtered_by_bad_tag(self):
        additional_form_category = factories.FormCategoryFactory()

        Form.objects.create(
            form_category=additional_form_category,
            is_public=True,
        )

        self.form_categories[0].tags.add("form_category_a")
        self.form_categories[1].tags.add("form_category_a")
        additional_form_category.tags.add("form_category_b")
        submission = factories.SubmissionFactory(author=self.user)
        submission.administrative_entity.forms.set(
            Form.objects.all()
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            )
            + "?categoryfilter=badtag"
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        # Check that 3 forms are visibles
        self.assertEqual(3, len(element_parsed))

    def test_missing_mandatory_list_values_show_error(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        form = submission.forms.first()
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        list_single_field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_LIST_SINGLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        list_multiple_field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_LIST_MULTIPLE,
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
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        list_multiple_field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
        )
        list_multiple_field.forms.set(
            submission.forms.all()
        )

        data = {
            f"fields-{form.pk}_{list_multiple_field.pk}": [
                "foo",
                "bar",
            ],
        }

        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )
        self.assertEqual(
            services.get_property_value(
                FieldValue.objects.first()
            ),
            ["foo", "bar"],
        )

    def test_list_single_value_is_stored_as_list(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        form = submission.forms.first()
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        list_multiple_field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
        )
        list_multiple_field.forms.set(
            submission.forms.all()
        )

        data = {f"fields-{form.pk}_{list_multiple_field.pk}": "foo"}

        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
        )
        self.assertEqual(
            services.get_property_value(
                FieldValue.objects.first()
            ),
            ["foo"],
        )

    def test_input_is_restricted_to_list_values(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        form = submission.forms.first()
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        list_single_field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_LIST_SINGLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        list_multiple_field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_LIST_MULTIPLE,
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
            status=Submission.STATUS_APPROVED,
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
            status=Submission.STATUS_PROCESSING,
            prolongation_status=Submission.PROLONGATION_STATUS_PENDING,
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
            status=Submission.STATUS_AWAITING_SUPPLEMENT,
            prolongation_status=Submission.PROLONGATION_STATUS_REJECTED,
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
            status=Submission.STATUS_AWAITING_SUPPLEMENT,
        )
        submission.forms.set(
            [self.form_prolongable_no_date_with_reminder]
        )
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
            author=self.user, status=Submission.STATUS_APPROVED
        )
        submission.forms.set(
            [self.form_prolongable_with_date_and_reminder]
        )
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
            Submission.PROLONGATION_STATUS_PENDING,
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
            author=self.user, status=Submission.STATUS_APPROVED
        )
        submission.forms.set(
            [self.form_prolongable_with_date_and_reminder]
        )
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
            status=Submission.STATUS_APPROVED,
        )
        submission.forms.set([self.form_prolongable_with_date])
        factories.SubmissionGeoTimeFactory(submission=submission)
        submission.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        # Prolongation form on permit details
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
                "prolongation_status": Submission.PROLONGATION_STATUS_APPROVED,
                "prolongation_comment": "Prolonged! I got the power!",
                "action": ACTION_PROLONG,
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
            Submission.PROLONGATION_STATUS_APPROVED,
            submission.prolongation_status,
        )
        self.assertEqual(prolongation_date, submission.prolongation_date)
        self.assertEqual(
            "Prolonged! I got the power!", submission.prolongation_comment
        )

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
            status=Submission.STATUS_APPROVED,
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
                "prolongation_status": Submission.PROLONGATION_STATUS_REJECTED,
                "prolongation_comment": "Rejected! Because I say so!",
                "action": ACTION_PROLONG,
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
            Submission.PROLONGATION_STATUS_REJECTED,
            submission.prolongation_status,
        )
        self.assertEqual(prolongation_date, submission.prolongation_date)
        self.assertEqual(
            "Rejected! Because I say so!", submission.prolongation_comment
        )

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
            status=Submission.STATUS_RECEIVED,
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
            status=Submission.STATUS_DRAFT,
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
            status=Submission.STATUS_APPROVED,
            author=self.user,
        )
        submission_expired.forms.set(
            [self.form_prolongable_with_date_and_reminder]
        )
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
            status=Submission.STATUS_APPROVED,
            author=self.user,
            prolongation_date=prolongation_date_prolonged,
            prolongation_status=Submission.PROLONGATION_STATUS_APPROVED,
        )
        submission_prolonged.forms.set(
            [self.form_prolongable_with_date_and_reminder]
        )
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
            status=Submission.STATUS_APPROVED,
            author=self.user,
            prolongation_date=prolongation_date_requested,
            prolongation_status=Submission.PROLONGATION_STATUS_PENDING,
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
            status=Submission.STATUS_APPROVED,
            author=self.user,
            prolongation_date=prolongation_date_rejected,
            prolongation_status=Submission.PROLONGATION_STATUS_REJECTED,
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
            status=Submission.STATUS_APPROVED,
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
            status=Submission.STATUS_APPROVED,
        )
        submission.forms.set(
            [self.form_prolongable_with_date, self.form_normal]
        )
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
            status=Submission.STATUS_APPROVED,
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
            "form-0-contact_type": "",
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
        form_category = form.form_category

        contact_required = factories.ContactTypeFactory(
            is_mandatory=True, form_category=form_category
        )

        self.test_formset_data["form-0-contact_type"] = contact_required.type

        submission = factories.SubmissionFactory(
            author=self.user, status=Submission.STATUS_DRAFT
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

        actors = list(submission.actors.all())
        self.assertEqual(len(actors), 1, "Expected 1 actor created")
        self.assertEqual(actors[0].first_name, "John")

    def test_submission_contact_required_cannot_have_empty_field(self):
        form = factories.FormFactory()
        form_category = form.form_category

        contact_required = factories.ContactTypeFactory(
            is_mandatory=True, form_category=form_category
        )

        self.test_formset_data["form-0-contact_type"] = contact_required.type

        submission = factories.SubmissionFactory(
            author=self.user, status=Submission.STATUS_DRAFT
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
        # Check that no actor was saved for this permit
        self.assertEqual(submission.actors.count(), 0)
        # Check that if form not valid, it does not redirect
        self.assertEqual(response.status_code, 200)

    def test_submission_contact_creditor_field_is_hidden_if_form_is_not_paid(self):
        form = factories.FormFactory(requires_payment=False)
        form_category = form.form_category

        factories.ContactTypeFactory(is_mandatory=True, form_category=form_category)

        submission = factories.SubmissionFactory(
            author=self.user, status=Submission.STATUS_DRAFT
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

        free_forms = factories.FormFactory.create_batch(
            2, requires_payment=False
        )
        paid_form = factories.FormFactory(requires_payment=True)
        form_categories = [form.form_category for form in free_forms] + [
            paid_form.form_category
        ]

        for form_category in form_categories:
            factories.ContactTypeFactory(is_mandatory=True, form_category=form_category)

        submission = factories.SubmissionFactory(
            author=self.user, status=Submission.STATUS_DRAFT
        )

        submission.forms.set(
            free_forms + [paid_form]
        )

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


class SubmissionUpdateTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.submission = factories.SubmissionFactory(
            author=self.user
        )
        factories.SelectedFormFactory.create_batch(
            3, submission=self.submission
        )
        self.submission.administrative_entity.forms.set(
            self.submission.forms.all()
        )

    def test_categories_step_submit_shows_new_forms(self):
        new_form = factories.FormFactory()

        new_form.administrative_entities.set(
            [self.submission.administrative_entity]
        )

        response = self.client.post(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": self.submission.pk},
            ),
            follow=True,
            data={
                "categories": get_submission_form_categories_ids(self.submission)
                + [new_form.form_category.pk]
            },
        )

        self.assertContains(response, new_form.form_category)

    def test_categories_step_submit_removes_deselected_categories_from_submission(self):
        form_id = get_submission_form_categories_ids(self.submission)[
            0
        ]

        self.client.post(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": self.submission.pk},
            ),
            data={"categories": form_id},
        )

        self.submission.refresh_from_db()

        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(
            get_submission_form_categories_ids(self.submission),
            [form_id],
        )

    def test_objects_step_submit_updates_submission(self):
        new_form = factories.FormFactory()
        self.submission.administrative_entity.forms.add(
            new_form
        )
        current_forms = list(self.submission.forms.all())
        current_forms_dict = to_forms_dict(
            current_forms
        )
        new_forms_dict = to_forms_dict([new_form])
        form_categories_ids = get_submission_form_categories_ids(self.submission) + [
            new_form.form_category.pk
        ]
        categories_param = urllib.parse.urlencode({"categories": form_categories_ids}, doseq=True)

        self.client.post(
            (
                reverse(
                    "submissions:submission_select_forms",
                    kwargs={"submission_id": self.submission.pk},
                )
                + "?"
                + categories_param
            ),
            data={**current_forms_dict, **new_forms_dict},
        )

        self.submission.refresh_from_db()

        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(
            set(self.submission.forms.all()),
            set(current_forms + [new_form]),
        )

    def test_fields_step_submit_updates_submission(self):
        new_field = factories.FieldFactory()
        new_field.forms.set(self.submission.forms.all())
        data = {
            "fields-{}_{}".format(
                form.pk, new_field.pk
            ): "value-{}".format(form.pk)
            for form in self.submission.forms.all()
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        self.assertEqual(
            set(
                item["val"]
                for item in services.get_fields_values(
                    self.submission
                ).values_list("value", flat=True)
            ),
            set(data.values()),
        )

    def test_missing_mandatory_address_field_gives_invalid_feedback(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        submission.administrative_entity.forms.set(
            submission.forms.all()
        )
        field = factories.FieldFactoryTypeAddress(
            input_type=Field.INPUT_TYPE_ADDRESS, is_mandatory=True
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
        self.assertEqual(1, len(parser.select(".invalid-feedback")))

    def test_fields_step_submit_updates_submission_with_address(self):
        address_field = factories.FieldFactoryTypeAddress(
            input_type=Field.INPUT_TYPE_ADDRESS
        )
        address_field.forms.set(
            self.submission.forms.all()
        )
        form = self.submission.forms.first()
        data = {
            f"fields-{form.pk}_{address_field.pk}": "Hôtel Martinez, Cannes"
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        self.submission.refresh_from_db()
        field_val = services.get_fields_values(self.submission).get(
            property__input_type=Field.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(field_val.value, {"val": "Hôtel Martinez, Cannes"})

    def test_fields_step_submit_updates_geotime_with_address_store_geometry_for_address_field(
        self,
    ):

        address_field = factories.FieldFactoryTypeAddress(
            input_type=Field.INPUT_TYPE_ADDRESS,
            store_geometry_for_address_field=True,
        )
        address_field.forms.set(
            self.submission.forms.all()
        )
        form = self.submission.forms.first()
        data = {
            f"fields-{form.pk}_{address_field.pk}": "Place pestalozzi 2, 1400 Yverdon-les-Bains"
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        self.submission.refresh_from_db()
        field_val = services.get_fields_values(self.submission).get(
            property__input_type=Field.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(
            field_val.value, {"val": "Place pestalozzi 2, 1400 Yverdon-les-Bains"}
        )
        geocoded_geotime_row = SubmissionGeoTime.objects.filter(
            submission=self.submission, comes_from_automatic_geocoding=True
        ).count()
        self.assertEqual(1, geocoded_geotime_row)

    def test_fields_step_submit_updates_submission_with_date(self):

        date_field = factories.FieldFactory(
            input_type=Field.INPUT_TYPE_DATE, name="datum"
        )
        today = date.today()
        form = self.submission.forms.first()
        date_field.forms.set([form])
        data = {
            f"fields-{form.pk}_{date_field.pk}": today.strftime(
                settings.DATE_INPUT_FORMAT
            )
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        field_val = services.get_fields_values(self.submission).get(
            property__name="datum"
        )
        self.assertEqual(
            field_val.value,
            {"val": today.isoformat()},
        )
        self.assertEqual(
            field_val.field.input_type,
            Field.INPUT_TYPE_DATE,
        )


class SubmissionPrefillTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.submission = factories.SubmissionFactory(
            author=self.user
        )
        factories.SelectedFormFactory.create_batch(
            3, submission=self.submission
        )
        self.submission.administrative_entity.forms.set(
            self.submission.forms.all()
        )

    def test_categories_step_preselects_categories_for_existing_submission(self):
        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()

        for i, form_category_id in enumerate(
            get_submission_form_categories_ids(self.submission)
        ):
            expected = (
                '<input checked="" class="form-check-input" id="id_forms_{i}" name="forms" title=""'
                '  type="checkbox" value="{value}"/>'
            ).format(value=form_category_id, i=i)
            self.assertInHTML(expected, content)

    def test_forms_step_preselects_forms_for_existing_submission(self):
        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()

        for form in self.submission.forms.all():
            expected = (
                '<input checked="" class="form-check-input" id="id_forms-{id}_0"'
                ' name="forms-{id}" title="" type="checkbox" value="{value}"/>'
            ).format(id=form.form_category.pk, value=form.pk)
            self.assertInHTML(expected, content)

    def test_fields_step_prefills_fields_for_existing_submission(self):
        selected_form = services.get_selected_forms(
            self.submission
        ).first()
        field = factories.FieldFactory()
        field.forms.add(selected_form.form)
        field_value = factories.FieldValueFactory(
            selected_form=selected_form, field=field
        )
        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()

        expected = '<textarea name="fields-{form_id}_{field_id}" cols="40" rows="1" placeholder="ex: {placeholder}" class="textarea form-control" title="{help_text}" id="id_fields-{form_id}_{field_id}">{value}'.format(
            form_id=selected_form.form.pk,
            field_id=field.pk,
            field_name=field.name,
            value=field_value.value["val"],
            placeholder=field.placeholder,
            help_text=field.help_text,
        )

        expected_help_text = '<small id="hint_id_fields-{form_id}_{field_id}" class="form-text text-muted">{help_text}</small>'.format(
            help_text=field.help_text,
            form_id=selected_form.form.pk,
            field_id=field.pk,
        )

        self.assertInHTML(expected, content)
        self.assertInHTML(expected_help_text, content)

    def test_fields_step_shows_title_and_additional_text(self):
        selected_form = services.get_selected_forms(
            self.submission
        ).first()

        field_title = factories.FieldFactoryTypeTitle()
        field_title.forms.add(selected_form.form)

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()
        expected = "<h5 class='fieldTitle'>{field_name}</h5>".format(
            field_name=field_title.name,
        )

        expected_help_text = "<small>{help_text}</small>".format(
            help_text=field_title.help_text
        )

        self.assertInHTML(expected, content)
        self.assertInHTML(expected_help_text, content)

    def test_fields_step_order_fields_for_existing_submission(self):

        selected_form = services.get_selected_forms(
            self.submission
        ).first()

        field_1 = factories.FieldFactory(order=10, name=str(uuid.uuid4()))
        field_2 = factories.FieldFactory(order=2, name=str(uuid.uuid4()))
        field_1.forms.add(selected_form.form)
        field_2.forms.add(selected_form.form)

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()
        position_1 = content.find(field_1.name)
        position_2 = content.find(field_2.name)
        self.assertGreater(position_1, position_2)

    def test_fields_step_shows_downloadable_file(self):
        selected_form = services.get_selected_forms(
            self.submission
        ).first()

        field_file = factories.FieldFactoryTypeFileDownload()
        field_file.forms.add(selected_form.form)

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )

        expected_href = rf"/permit-requests/form-files/{field_file.file_download.name}"
        parser = get_parser(response.content)
        file_links = parser.find_all("a", href=re.compile(expected_href))
        self.assertEqual(1, len(file_links))
        self.assertIn(expected_href, response.content.decode())

    def test_fields_step_shows_downloadable_files_more_than_once(self):
        selected_forms = services.get_selected_forms(
            self.submission
        )
        selected_form_first = selected_forms.first()
        selected_form_last = selected_forms.last()

        field_file = factories.FieldFactoryTypeFileDownload()
        field_file.forms.add(
            selected_form_first.form
        )
        field_file.forms.add(
            selected_form_last.form
        )

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )

        expected_href = rf"/permit-requests/form-files/{field_file.file_download.name}"
        parser = get_parser(response.content)
        file_links = parser.find_all("a", href=re.compile(expected_href))

        self.assertEqual(2, len(file_links))
        self.assertIn(expected_href, response.content.decode())


class SubmissionAmendmentTestCase(LoggedInSecretariatMixin, TestCase):
    def test_non_secretariat_user_cannot_amend_request(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

        submission = factories.SubmissionFactory(
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user,
        )
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": Submission.STATUS_PROCESSING,
                "action": ACTION_AMEND,
            },
        )

        submission.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            submission.status, Submission.STATUS_SUBMITTED_FOR_VALIDATION
        )

    def test_secretariat_can_amend_request_with_custom_field_and_delete_field_value(
        self,
    ):
        fields_quantity = 3
        submission = factories.SubmissionFactory(
            status=Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        selected_form = factories.SelectedFormFactory(
            submission=submission
        )

        amend_fields = factories.SubmissionAmendFieldFactory.create_batch(fields_quantity)

        data = {
            "action": ACTION_AMEND,
            "status": Submission.STATUS_PROCESSING,
        }

        forms_pk = submission.forms.first().pk
        for amend_field in amend_fields:
            amend_field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=amend_field,
                selected_form=selected_form,
            )
            data[
                f"{forms_pk}_{amend_field.pk}"
            ] = "I am a new field value, I am alive!"

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
            SubmissionAmendFieldValue.objects.values_list(
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
            status=Submission.STATUS_APPROVED,
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
                "action": ACTION_AMEND,
                "status": Submission.STATUS_PROCESSING,
            },
        )

        parser = get_parser(response.content)
        element = "disabled" in str(parser.select('input[id="id_shortname"]'))
        self.assertTrue(element)

    def test_secretariat_can_amend_submission_fields_if_it_can_always_be_updated(
        self,
    ):
        submission = factories.SubmissionFactory(
            status=Submission.STATUS_APPROVED,
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
                "action": models.ACTION_AMEND,
                "status": Submission.STATUS_PROCESSING,
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
            status=Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        selected_form = factories.SelectedFormFactory(
            submission=submission
        )

        fields_public = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, is_visible_by_author=True
        )
        fields_private = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, is_visible_by_author=False
        )
        fields_private_validators = (
            factories.SubmissionAmendFieldFactory.create_batch(
                fields_quantity,
                is_visible_by_author=False,
                is_visible_by_validators=True,
            )
        )

        fields = fields_public + fields_private + fields_private_validators

        self.client.login(
            username=submission.author.username, password="password"
        )
        data = {
            "action": ACTION_AMEND,
            "status": Submission.STATUS_PROCESSING,
        }
        forms_pk = submission.forms.first().pk
        for field in fields:
            field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=field,
                selected_form=selected_form,
            )
            data[
                f"{forms_pk}_{field.pk}"
            ] = "I am a new field value, I am alive!"

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

        parser = get_parser(response.content)
        # check that the 3 fields are visible by author and 6 (3 private + 3 for validators) are hidden
        self.assertEqual(len(parser.select(".amend-field")), 3)

    def test_secretariat_can_see_submitted_requests(self):
        submission = factories.SubmissionFactory(
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        factories.SubmissionGeoTimeFactory(submission=submission)
        response = self.client.get(reverse("submissions:submissions_list"))

        self.assertEqual(list(response.context["submission_list"]), [submission])

    def test_ask_for_supplements_shows_specific_message(self):
        form_1 = factories.FormFactory()
        form_2 = factories.FormFactory()
        submission = factories.SubmissionFactory(
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
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
                "status": Submission.STATUS_AWAITING_SUPPLEMENT,
                "action": ACTION_AMEND,
                "notify_author": "on",
                "reason": "reason",
            },
            follow=True,
        )
        submission.refresh_from_db()
        self.assertEqual(
            submission.status, Submission.STATUS_AWAITING_SUPPLEMENT
        )
        self.assertContains(response, "compléments")

    def test_secretariat_cannot_amend_submission_with_validation_requested(self):
        submission = factories.SubmissionFactory(
            status=Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": Submission.STATUS_AWAITING_SUPPLEMENT,
                "action": ACTION_AMEND,
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
            status=Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )

        submission.forms.set(
            [first_form, second_form]
        )

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
            status=Submission.STATUS_AWAITING_VALIDATION,
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
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user,
        )
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
        submission.forms.set([form])
        factories.SubmissionGeoTimeFactory(submission=submission)
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": Submission.STATUS_RECEIVED,
                "action": ACTION_AMEND,
            },
            follow=True,
        )

        submission.refresh_from_db()
        self.assertEqual(submission.status, Submission.STATUS_RECEIVED)
        self.assertContains(response, "compléments")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )

    def test_email_to_services_is_sent_when_secretariat_acknowledges_reception(self):
        submission = factories.SubmissionFactory(
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
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
                "status": Submission.STATUS_RECEIVED,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )

        submission.refresh_from_db()
        self.assertEqual(submission.status, Submission.STATUS_RECEIVED)

        # 1 email to author + 2 emails to services
        self.assertEqual(len(mail.outbox), 3)

        services_message_subject = (
            "Une annonce a été prise en compte et classée par le secrétariat"
        )
        services_message_content = "Nous vous informons qu'une annonce a été prise en compte et classée par le secrétariat."
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
            status=Submission.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
        )

        form = factories.FormFactory()
        form.administrative_entities.set([submission.administrative_entity])

        selected_form = factories.SelectedFormFactory(
            submission=submission, form=form
        )

        fields = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, can_always_update=True
        )

        data = {
            "action": models.ACTION_AMEND,
            "status": Submission.STATUS_APPROVED,
        }

        forms_pk = submission.forms.first().pk

        for field in fields:
            field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=field,
                selected_form=selected_form,
            )
            data[
                f"{forms_pk}_{field.pk}"
            ] = "I am a new field value, I am alive!"

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data=data,
            follow=True,
        )

        new_fields_values_qs = (
            SubmissionAmendFieldValue.objects.values_list(
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
            status=Submission.STATUS_APPROVED,
            administrative_entity=self.administrative_entity,
        )

        form = factories.FormFactory()
        form.administrative_entities.set([submission.administrative_entity])

        selected_form = factories.SelectedFormFactory(
            submission=submission, form=form
        )

        field_editable = factories.SubmissionAmendFieldFactory(
            name="Editable_prop", can_always_update=True
        )

        field_not_editable = factories.SubmissionAmendFieldFactory(
            name="Not_editable_prop", can_always_update=False
        )

        fields = [field_editable, field_not_editable]

        data = {
            "action": models.ACTION_AMEND,
            "status": Submission.STATUS_APPROVED,
        }

        forms_pk = submission.forms.first().pk

        for field in fields:
            field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=field,
                selected_form=selected_form,
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
            SubmissionAmendFieldValue.objects.values_list(
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
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user,
        )
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
        submission.forms.set([form])
        factories.SubmissionGeoTimeFactory(submission=submission)
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": Submission.STATUS_AWAITING_SUPPLEMENT,
                "notify_author": "1",
                "reason": "Testing email sending",
                "action": ACTION_AMEND,
            },
            follow=True,
        )

        submission.refresh_from_db()
        self.assertEqual(
            submission.status, Submission.STATUS_AWAITING_SUPPLEMENT
        )
        self.assertContains(response, "compléments")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            f"Votre demande a changé de statut (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre demande a changé de statut.",
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
            status=Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "status": Submission.STATUS_AWAITING_SUPPLEMENT,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )
        submission.refresh_from_db()

        self.assertEqual(submission.status, Submission.STATUS_PROCESSING)
        self.assertEqual(
            response.context[0]["forms"]["amend"].errors["notify_author"],
            ["Vous devez notifier l'auteur pour une demande de compléments"],
        )


class AdministrativeEntitySecretaryEmailTestcase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(email="user@geocity.com")
        self.administrative_entity_expeditor = (
            factories.AdministrativeEntityFactory(
                expeditor_email="geocity_rocks@geocity.ch",
                expeditor_name="Geocity Rocks",
            )
        )
        self.group = factories.SecretariatGroupFactory(
            department__administrative_entity=self.administrative_entity_expeditor
        )
        self.secretary = factories.SecretariatUserFactory(groups=[self.group])
        self.client.login(username=self.secretary.username, password="password")

        self.submission = factories.SubmissionFactory(
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity_expeditor,
            author=self.user,
        )

    def test_secretary_email_and_name_are_set_for_the_administrative_entity(self):
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
        self.submission.forms.set([form])

        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": self.submission.pk},
            ),
            data={
                "status": Submission.STATUS_RECEIVED,
                "action": ACTION_AMEND,
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
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )

    def test_just_secretary_email_is_set_for_the_administrative_entity(self):
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
        self.submission.forms.set([form])
        self.administrative_entity_expeditor = (
            AdministrativeEntity.objects.first()
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
                "status": Submission.STATUS_RECEIVED,
                "action": ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "<geocity_rocks@geocity.ch>")
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )

    def test_no_secretary_email_is_set_for_the_administrative_entity(self):
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
        self.submission.forms.set([form])
        self.administrative_entity_expeditor = (
            AdministrativeEntity.objects.first()
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
                "status": Submission.STATUS_RECEIVED,
                "action": ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

        self.assertNotEqual(mail.outbox[0].from_email, "geocity_rocks@geocity.ch")
        self.assertEqual(mail.outbox[0].from_email, "your_noreply_email")
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )


class SubmissionValidationRequestTestcase(LoggedInSecretariatMixin, TestCase):
    def test_secretariat_can_request_validation(self):
        validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity
        )
        validator_departments = [
            group.permitdepartment.pk for group in validator_groups
        ]

        submission = factories.SubmissionFactory(
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "departments": validator_departments,
                "action": ACTION_REQUEST_VALIDATION,
            },
        )

        submission.refresh_from_db()

        self.assertEqual(
            submission.status, Submission.STATUS_AWAITING_VALIDATION
        )
        self.assertEqual(
            list(submission.validations.values_list("department", flat=True)),
            validator_departments,
        )

    def test_secretariat_cannot_request_validation_for_already_validated_submission(
        self,
    ):
        validator_group = factories.ValidatorGroupFactory(
            department__administrative_entity=self.administrative_entity
        )

        submission = factories.SubmissionFactory(
            status=Submission.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "departments": [validator_group.permitdepartment.pk],
                "action": ACTION_REQUEST_VALIDATION,
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
            status=Submission.STATUS_PROCESSING,
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
                **{group.pk: True for group in default_validator_groups},
                **{non_default_validator_group.pk: False},
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
            status=Submission.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
            data={
                "departments": [validator_groups[0].permitdepartment.pk],
                "action": ACTION_REQUEST_VALIDATION,
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator_user.user.email])


class SubmissionValidationTestcase(TestCase):
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
                "action": ACTION_VALIDATE,
                "validation_status": SubmissionValidation.STATUS_APPROVED,
            },
        )

        validation.refresh_from_db()

        self.assertEqual(
            validation.validation_status, SubmissionValidation.STATUS_APPROVED
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
                "action": ACTION_VALIDATE,
                "validation_status": SubmissionValidation.STATUS_APPROVED,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_validator_can_see_for_validators_amend_property(
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
        selected_form = factories.SelectedFormFactory(
            submission=submission
        )
        fields_private = factories.SubmissionAmendFieldFactory.create_batch(
            fields_quantity, is_visible_by_author=False, is_visible_by_validators=False
        )
        fields_private_validators = (
            factories.SubmissionAmendFieldFactory.create_batch(
                fields_quantity,
                is_visible_by_author=False,
                is_visible_by_validators=True,
            )
        )

        fields = fields_private + fields_private_validators

        data = {
            "action": models.ACTION_AMEND,
            "status": Submission.STATUS_PROCESSING,
        }
        forms_pk = submission.forms.first().pk
        for field in fields:
            field.forms.set(submission.forms.all())
            factories.SubmissionAmendFieldValueFactory(
                field=field,
                selected_form=selected_form,
            )
            data[
                f"{forms_pk}_{field.pk}"
            ] = "I am a new field value, I am alive!"

        response = self.client.get(
            reverse(
                "submissions:submission_detail",
                kwargs={"submission_id": submission.pk},
            ),
        )

        parser = get_parser(response.content)
        # check that the 3 fields are visible by validator and 3 are hidden
        self.assertEqual(len(parser.select(".amend-field")), 3)

    def test_secretariat_can_send_validation_reminders(self):
        group = factories.SecretariatGroupFactory()
        administrative_entity = group.permitdepartment.administrative_entity
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
                "action": ACTION_POKE,
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator.user.email])

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
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
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
                "action": ACTION_VALIDATE,
                "validation_status": SubmissionValidation.STATUS_APPROVED,
            },
        )

        validation.refresh_from_db()

        self.assertEqual(
            validation.validation_status, SubmissionValidation.STATUS_APPROVED
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["secretary@geocity.ch"])
        self.assertEqual(
            mail.outbox[0].subject,
            "Les services chargés de la validation d'une demande ont donné leur préavis (Foo type)",
        )
        self.assertIn(
            "Les services chargés de la validation d'une demande ont donné leur préavis",
            mail.outbox[0].message().as_string(),
        )


class SubmissionClassifyTestCase(TestCase):
    def setUp(self):
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permitdepartment.administrative_entity
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
            submission__status=Submission.STATUS_PROCESSING,
            validation_status=SubmissionValidation.STATUS_APPROVED,
            submission__author__user__email="user@geocity.com",
        )
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
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
            validation.submission.status, Submission.STATUS_APPROVED
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre demande a été traitée et classée (Foo type)",
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
            submission__status=Submission.STATUS_PROCESSING,
            validation_status=SubmissionValidation.STATUS_REJECTED,
            submission__author__user__email="user@geocity.com",
        )
        form_category = factories.FormCategoryFactory(name="Foo type")
        form = factories.FormFactory(
            form_category=form_category,
        )
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
            validation.submission.status, Submission.STATUS_REJECTED
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre demande a été traitée et classée (Foo type)",
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
            validation_status=SubmissionValidation.STATUS_APPROVED,
        )
        user = factories.UserFactory(actor=validation.submission.author)
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
            status=Submission.STATUS_APPROVED,
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
            validated_at=timezone.now(), status=Submission.STATUS_APPROVED
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
            submission__status=Submission.STATUS_PROCESSING,
            validation_status=SubmissionValidation.STATUS_APPROVED,
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
        form_category_1 = factories.FormCategoryFactory(name="Foo type")
        form_category_2 = factories.FormCategoryFactory(name="Bar type")
        form = factories.FormFactory(
            requires_validation_document=False,
            notify_services=True,
            services_to_notify="test-send-1@geocity.ch, test-send-2@geocity.ch, test-i-am-not-an-email,  ,\n\n\n",
            form_category=form_category_1,
        )
        form2 = factories.FormFactory(
            requires_validation_document=False,
            notify_services=True,
            services_to_notify="not-repeated-email@liip.ch, test-send-1@geocity.ch, \n, test-send-2@geocity.ch, test-i-am-not-an-email,  ,",
            form_category=form_category_2,
        )
        validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            submission__status=Submission.STATUS_PROCESSING,
            validation_status=SubmissionValidation.STATUS_APPROVED,
            submission__author__user__email="user@geocity.com",
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
            validation.submission.status, Submission.STATUS_APPROVED
        )
        # Only valid emails are sent, not repeated emails.
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])

        self.assertIn(
            "Votre demande a été traitée et classée",
            mail.outbox[0].subject,
        )

        self.assertIn(
            "Bar type",
            mail.outbox[0].subject,
        )

        self.assertIn(
            "Foo type",
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
            self.secretariat_group.permitdepartment.administrative_entity
        )
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        self.validation = factories.SubmissionValidationFactory(
            submission__administrative_entity=self.administrative_entity,
            submission__status=Submission.STATUS_PROCESSING,
            validation_status=SubmissionValidation.STATUS_APPROVED,
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
            Submission.STATUS_PROCESSING,
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


class PrivateDemandsTestCase(LoggedInUserMixin, TestCase):
    def test_administrative_entity_step_without_public_requests_is_empty_to_standard_user(
        self,
    ):

        form_category = factories.FormCategoryFactory()
        private_form = factories.FormFactory(
            form_category=form_category,
            is_public=False,
        )

        administrative_entity = factories.AdministrativeEntityFactory(
            name="privateEntity"
        )
        private_form.administrative_entities.set([administrative_entity])
        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
            ),
        )
        self.assertNotContains(response, "privateEntity")

    def test_administrative_entity_step_without_public_requests_is_visible_to_user_with_specific_permission(
        self,
    ):

        see_private_requests_permission = Permission.objects.get(
            codename="see_private_requests"
        )
        self.user.user_permissions.add(see_private_requests_permission)
        form_category = factories.FormCategoryFactory()
        private_form = factories.FormFactory(
            form_category=form_category,
            is_public=True,
        )

        administrative_entity_1 = factories.AdministrativeEntityFactory(
            name="privateEntity1"
        )
        administrative_entity_2 = factories.AdministrativeEntityFactory(
            name="privateEntity2"
        )
        private_form.administrative_entities.set(
            [administrative_entity_1, administrative_entity_2]
        )
        response = self.client.get(
            reverse(
                "submissions:submission_select_administrative_entity",
            ),
        )

        self.assertContains(response, "privateEntity1")
        self.assertContains(response, "privateEntity2")

    def test_form_category_step_only_show_public_requests_to_standard_user(
        self,
    ):

        public_forms = factories.FormFactory.create_batch(
            2, is_public=True
        )
        private_form = factories.FormFactory(is_public=False)
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set(
            public_forms + [private_form]
        )

        submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=administrative_entity
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 2
        )

    def test_form_category_step_show_private_requests_with_choices_to_user_with_specific_permission(
        self,
    ):

        see_private_requests_permission = Permission.objects.get(
            codename="see_private_requests"
        )
        self.user.user_permissions.add(see_private_requests_permission)

        public_forms = factories.FormFactory.create_batch(
            2, is_public=True
        )
        private_form = factories.FormFactory(is_public=False)
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set(
            public_forms + [private_form]
        )

        submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=administrative_entity
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_categories",
                kwargs={"submission_id": submission.pk},
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 3
        )

    def test_form_category_step_show_public_requests_to_standard_user(
        self,
    ):
        public_forms = factories.FormFactory.create_batch(
            2, is_public=True
        )
        private_form = factories.FormFactory(is_public=False)
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set(
            public_forms + [private_form]
        )

        submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=administrative_entity
        )

        submission.administrative_entity.forms.set(
            Form.objects.all()
        )

        Form.objects.create(
            submission=submission,
            form=public_forms[0],
        )

        Form.objects.create(
            submission=submission,
            form=public_forms[1],
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
            + "?categories={}&forms={}".format(
                public_forms[0].form_category.pk,
                public_forms[1].form_category.pk,
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 2
        )

    def test_form_category_step_show_private_requests_to_user_with_specific_permission(
        self,
    ):

        see_private_requests_permission = Permission.objects.get(
            codename="see_private_requests"
        )
        self.user.user_permissions.add(see_private_requests_permission)

        public_forms = factories.FormFactory.create_batch(
            2, is_public=True
        )
        private_form = factories.FormFactory(is_public=False)
        administrative_entity = factories.AdministrativeEntityFactory()
        administrative_entity.forms.set(
            public_forms + [private_form]
        )

        submission = factories.SubmissionFactory(
            author=self.user, administrative_entity=administrative_entity
        )

        submission.administrative_entity.forms.set(
            Form.objects.all()
        )

        Form.objects.create(
            submission=submission,
            form=public_forms[0],
        )

        Form.objects.create(
            submission=submission,
            form=public_forms[1],
        )

        Form.objects.create(
            submission=submission, form=private_form
        )

        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": submission.pk},
            )
            + "?categories={}&forms={}&forms={}".format(
                public_forms[0].form_category.pk,
                public_forms[1].form_category.pk,
                private_form.form_category.pk,
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 3
        )


class SubmissionFilteredFormListTestCase(LoggedInSecretariatMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.form_normal = factories.FormFactory()
        self.submission = factories.SubmissionFactory(
            author=self.user,
            status=Submission.STATUS_APPROVED,
        )
        self.submission.forms.set([self.form_normal])
        factories.SubmissionGeoTimeFactory(submission=self.submission)

        selected_form = self.submission.selectedform_set.first()
        field = factories.FieldFactory()
        field.forms.add(selected_form.form)
        self.field_value = factories.FieldValueFactory(
            selected_form=selected_form, field=field
        )

    def test_secretariat_user_can_see_filtered_submission_details(
        self,
    ):
        response = self.client.get(
            "{}?forms__form={}".format(
                reverse(
                    "submissions:submissions_list",
                ),
                self.submission.forms.first().form.id,
            )
        )

        self.assertInHTML(self.field_value.value["val"], response.content.decode())

    def test_secretariat_user_can_see_filtered_submission_details_in_xlsx(
        self,
    ):
        response = self.client.get(
            "{}?forms__form={}&_export=xlsx".format(
                reverse(
                    "submissions:submissions_list",
                ),
                self.submission.forms.first().form.id,
            )
        )

        content = io.BytesIO(response.content)

        # Replace content in bytes with the readable one
        response.content = tablib.import_set(content.read(), format="xlsx")

        self.assertContains(response, self.field_value.value["val"])
        self.assertContains(response, self.field_value.field)


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
                "categoryfilter": category.tags.get().slug,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_request_on_anonymous_entity_displays_captcha_form(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        create_anonymous_users._create_anonymous_user_for_entity(entity)

        category = factories.FormCategoryFactory(tags=["a"])

        response = self.client.get(
            reverse("submissions:anonymous_submission"),
            data={
                "entityfilter": entity.tags.get().slug,
                "categoryfilter": category.tags.get().slug,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("anonymous_request_form", response.context)

    def test_anonymous_request_temporary_logged_in_no_form_displays_request_form(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        create_anonymous_users._create_anonymous_user_for_entity(entity)

        temp_author = UserProfile.objects.create_temporary_user(entity)
        self.client.force_login(temp_author.user)
        session = self.client.session
        session["anonymous_request_token"] = hash((temp_author, entity))
        session.save()

        category = factories.FormCategoryFactory(tags=["a"])

        response = self.client.get(
            reverse("submissions:anonymous_submission"),
            data={
                "entityfilter": entity.tags.get().slug,
                "categoryfilter": category.tags.get().slug,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_request_temporary_logged_in_displays_request_form(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        create_anonymous_users._create_anonymous_user_for_entity(entity)

        temp_author = UserProfile.objects.create_temporary_user(entity)
        self.client.force_login(temp_author.user)
        session = self.client.session
        session["anonymous_request_token"] = hash((temp_author, entity))
        session.save()

        category = factories.FormCategoryFactory(tags=["a"])
        factories.FormFactory(
            is_anonymous=True,
            form_category=category,
            administrative_entities=[entity],
        )

        response = self.client.get(
            reverse("submissions:anonymous_submission"),
            data={
                "entityfilter": entity.tags.get().slug,
                "categoryfilter": category.tags.get().slug,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        # As the form has to fields, going directly to next step
        self.assertTrue(
            isinstance(response.context["formset"].forms[0], SubmissionGeoTimeForm)
        )

    def test_anonymous_request_submission_deletes_temporary_user(self):
        entity = factories.AdministrativeEntityFactory(tags=["a"])
        create_anonymous_users._create_anonymous_user_for_entity(entity)

        temp_author = UserProfile.objects.create_temporary_user(entity)
        self.client.force_login(temp_author.user)
        session = self.client.session
        session["anonymous_request_token"] = hash((temp_author, entity))
        session.save()

        category = factories.FormCategoryFactory(tags=["a"])
        form = factories.FormWithoutGeometryFactory(
            is_anonymous=True,
            form_category=category,
            administrative_entities=[entity],
            needs_date=False,
        )

        # Filled submission
        submission = factories.SubmissionFactory(
            author=temp_author,
            status=Submission.STATUS_DRAFT,
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

        self.assertEqual(submission.author, entity.anonymous_user)

        self.assertEqual(
            get_user_model().objects.get().pk,
            submission.author.user_id,
        )
