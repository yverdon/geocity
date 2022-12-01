import uuid

from django.test import TestCase
from django.urls import reverse

from geocity.tests import factories
from geocity.tests.utils import LoggedInUserMixin, get_parser


class SubmissionPrefillTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(
            3,
            submission=self.submission,
            form__category=factories.FormCategoryFactory(),
        )
        self.submission.administrative_entity.forms.set(self.submission.forms.all())

    def test_forms_step_preselects_forms_for_existing_submission(self):
        response = self.client.get(
            reverse(
                "submissions:submission_select_forms",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()

        for i, form in enumerate(self.submission.forms.order_by("order")):
            expected = (
                f'<input checked="" class="" id="id_forms-selected_forms_0_{i}"'
                f' name="forms-selected_forms" title="" type="checkbox" value="{form.pk}"/>'
            )
            self.assertInHTML(expected, content)

    def test_fields_step_prefills_fields_for_existing_submission(self):
        selected_form = self.submission.get_selected_forms().first()
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
        selected_form = self.submission.get_selected_forms().first()

        field_title = factories.FieldFactoryTypeTitle()
        field_title.forms.add(selected_form.form)

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()
        expected = "<h5 class='propertyTitle'>{field_name}</h5>".format(
            field_name=field_title.name,
        )

        expected_help_text = "<small>{help_text}</small>".format(
            help_text=field_title.help_text
        )

        self.assertInHTML(expected, content)
        self.assertInHTML(expected_help_text, content)

    def test_fields_step_order_fields_for_existing_submission(self):
        selected_form = self.submission.get_selected_forms().first()

        field_1 = factories.FormFieldFactory(
            order=10, field__name=str(uuid.uuid4()), form=selected_form.form
        )
        field_2 = factories.FormFieldFactory(
            order=2, field__name=str(uuid.uuid4()), form=selected_form.form
        )

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )
        content = response.content.decode()
        position_1 = content.find(field_1.field.name)
        position_2 = content.find(field_2.field.name)
        self.assertGreater(position_1, position_2)

    def test_fields_step_shows_downloadable_file(self):
        selected_form = self.submission.get_selected_forms().first()

        field_file = factories.FieldFactoryTypeFileDownload()
        field_file.forms.add(selected_form.form)

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )

        expected_href = f"/submissions/form-files/{field_file.file_download.name}"
        parser = get_parser(response.content)
        file_links = parser.find_all("a", href=expected_href)
        self.assertEqual(1, len(file_links))
        self.assertIn(expected_href, response.content.decode())

    def test_fields_step_shows_downloadable_files_more_than_once(self):
        selected_forms = self.submission.get_selected_forms()
        selected_form_first = selected_forms.first()
        selected_form_last = selected_forms.last()

        field_file = factories.FieldFactoryTypeFileDownload()
        field_file.forms.add(selected_form_first.form)
        field_file.forms.add(selected_form_last.form)

        response = self.client.get(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            )
        )

        expected_href = f"/submissions/form-files/{field_file.file_download.name}"
        parser = get_parser(response.content)
        file_links = parser.find_all("a", href=expected_href)

        self.assertEqual(2, len(file_links))
        self.assertIn(expected_href, response.content.decode())
