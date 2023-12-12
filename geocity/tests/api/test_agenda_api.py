import datetime

from django.conf import settings
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from geocity.apps.forms import models as forms_models
from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories


class AgendaAPITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()

        # ////////////////////////////////////#
        # Dates for agenda
        # ////////////////////////////////////#

        start_at_valid_1 = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=settings.LOCAL_TIME_ZONE_UTC + 1)
        ends_at_valid_1 = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(days=5)

        start_at_valid_2 = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=settings.LOCAL_TIME_ZONE_UTC + 5)
        ends_at_valid_2 = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(days=3)

        start_at_passed = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(days=-10)
        ends_at_passed = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(days=-5)

        # ////////////////////////////////////#
        # First administrative entity (sit)
        # ////////////////////////////////////#

        # ////////////////////////////////////#
        # Users, groups and administrative entity
        # ////////////////////////////////////#

        self.sit_integrator_group = factories.IntegratorGroupFactory(department=None)
        self.sit_pilot_group = factories.SecretariatGroupFactory(department=None)
        self.sit_administrative_entity = factories.AdministrativeEntityFactory(
            tags=["sit"], integrator=self.sit_integrator_group
        )

        factories.IntegratorPermitDepartmentFactory(
            administrative_entity=self.sit_administrative_entity,
            group=self.sit_integrator_group,
        ),

        factories.PermitDepartmentFactory(
            administrative_entity=self.sit_administrative_entity,
            is_backoffice=True,
            group=self.sit_pilot_group,
        ),

        # Create normal User
        self.sit_normal_user = factories.UserFactory()

        # ////////////////////////////////////#
        # Agenda forms
        # ////////////////////////////////////#

        # Create valid agenda Forms
        self.sit_valid_agenda_form = factories.FormFactory(
            is_public=True,
            agenda_visible=True,
            administrative_entities=[self.sit_administrative_entity],
        )

        # Create valid agenda second iteration Forms
        self.sit_valid_agenda_form_2 = factories.FormFactory(
            is_public=False,
            agenda_visible=True,
            administrative_entities=[self.sit_administrative_entity],
        )

        # Create not valid agenda first iteration Forms
        self.sit_not_valid_agenda_form_1 = factories.FormFactory(
            is_public=True,
            agenda_visible=False,
            administrative_entities=[self.sit_administrative_entity],
        )

        # ////////////////////////////////////#
        # Fields
        # ////////////////////////////////////#

        self.sit_title_field = factories.FieldFactory(
            name="title",
            api_name="title",
            api_light=True,
            filter_for_api=False,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_TEXT,
        )

        self.sit_location_field = factories.FieldFactory(
            name="location",
            api_name="location",
            api_light=False,
            filter_for_api=False,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_TEXT,
        )

        self.sit_category_field = factories.FieldFactory(
            name="category",
            api_name="category",
            api_light=True,
            filter_for_api=True,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="First\nSecond\nThird",
        )

        self.sit_private_field = factories.FieldFactory(
            name="private_field",
            api_name="private_field",
            api_light=True,
            filter_for_api=False,
            public_if_submission_public=False,
            input_type=forms_models.Field.INPUT_TYPE_TEXT,
        )

        # ////////////////////////////////////#
        # Form fields
        # ////////////////////////////////////#

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form,
            field=self.sit_title_field,
        )

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form,
            field=self.sit_location_field,
        )

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form,
            field=self.sit_category_field,
        )

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form,
            field=self.sit_private_field,
        )

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form_2,
            field=self.sit_title_field,
        )

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form_2,
            field=self.sit_location_field,
        )

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form_2,
            field=self.sit_category_field,
        )

        factories.FormFieldFactory(
            form=self.sit_valid_agenda_form_2,
            field=self.sit_private_field,
        )

        factories.FormFieldFactory(
            form=self.sit_not_valid_agenda_form_1,
            field=self.sit_title_field,
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, with featured, valid date
        # ////////////////////////////////////#

        self.sit_first_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.sit_administrative_entity,
            author=self.sit_normal_user,
            is_public_agenda=True,
            featured_agenda=True,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.sit_first_submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.sit_first_submission,
            form=self.sit_valid_agenda_form,
        )
        factories.FieldValueFactory(
            field=self.sit_title_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_category_field,
            selected_form=selected_form,
            value={"val": "First"},
        )
        factories.FieldValueFactory(
            field=self.sit_private_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, valid date
        # ////////////////////////////////////#

        self.sit_second_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.sit_administrative_entity,
            author=self.sit_normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.sit_second_submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.sit_second_submission,
            form=self.sit_valid_agenda_form,
        )
        factories.FieldValueFactory(
            field=self.sit_title_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_category_field,
            selected_form=selected_form,
            value={"val": "Second"},
        )
        factories.FieldValueFactory(
            field=self.sit_private_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, valid date but later
        # ////////////////////////////////////#

        self.sit_third_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.sit_administrative_entity,
            author=self.sit_normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.sit_third_submission,
            starts_at=start_at_valid_2,
            ends_at=ends_at_valid_2,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.sit_third_submission,
            form=self.sit_valid_agenda_form_2,
        )
        factories.FieldValueFactory(
            field=self.sit_title_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_category_field,
            selected_form=selected_form,
            value={"val": "Third"},
        )
        factories.FieldValueFactory(
            field=self.sit_private_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, passed date
        # ////////////////////////////////////#

        self.sit_fourth_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.sit_administrative_entity,
            author=self.sit_normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.sit_fourth_submission,
            starts_at=start_at_passed,
            ends_at=ends_at_passed,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.sit_fourth_submission,
            form=self.sit_valid_agenda_form_2,
        )
        factories.FieldValueFactory(
            field=self.sit_title_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_category_field,
            selected_form=selected_form,
            value={"val": "First"},
        )
        factories.FieldValueFactory(
            field=self.sit_private_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, passed start but still active
        # ////////////////////////////////////#

        self.sit_fifth_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.sit_administrative_entity,
            author=self.sit_normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.sit_fifth_submission,
            starts_at=start_at_passed,
            ends_at=ends_at_valid_2,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.sit_fifth_submission,
            form=self.sit_valid_agenda_form_2,
        )
        factories.FieldValueFactory(
            field=self.sit_title_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_category_field,
            selected_form=selected_form,
            value={"val": "Second"},
        )
        factories.FieldValueFactory(
            field=self.sit_private_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Invalid submission for agenda, with featured, valid date. Pilot haven't turn public
        # ////////////////////////////////////#

        self.sit_sixth_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.sit_administrative_entity,
            author=self.sit_normal_user,
            is_public_agenda=False,
            featured_agenda=True,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.sit_sixth_submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.sit_sixth_submission,
            form=self.sit_valid_agenda_form_2,
        )
        factories.FieldValueFactory(
            field=self.sit_title_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.sit_category_field,
            selected_form=selected_form,
            value={"val": "Third"},
        )
        factories.FieldValueFactory(
            field=self.sit_private_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, with featured, valid date but invalid form
        # ////////////////////////////////////#

        self.sit_seventh_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.sit_administrative_entity,
            author=self.sit_normal_user,
            is_public_agenda=True,
            featured_agenda=True,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.sit_seventh_submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.sit_seventh_submission,
            form=self.sit_not_valid_agenda_form_1,
        )
        factories.FieldValueFactory(
            field=self.sit_title_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Second administrative entity (fin)
        # ////////////////////////////////////#

        # ////////////////////////////////////#
        # Users, groups and administrative entity
        # ////////////////////////////////////#

        self.fin_integrator_group = factories.IntegratorGroupFactory(department=None)
        self.fin_group = factories.SecretariatGroupFactory(department=None)
        self.fin_administrative_entity = factories.AdministrativeEntityFactory(
            tags=["fin"], integrator=self.fin_integrator_group
        )

        factories.IntegratorPermitDepartmentFactory(
            administrative_entity=self.fin_administrative_entity,
            group=self.fin_integrator_group,
        ),

        factories.PermitDepartmentFactory(
            administrative_entity=self.fin_administrative_entity,
            is_backoffice=True,
            group=self.fin_group,
        ),

        # Create normal User
        self.fin_normal_user = factories.UserFactory()

        # ////////////////////////////////////#
        # Agenda form
        # ////////////////////////////////////#

        # Create valid agenda Form
        self.fin_valid_agenda_form = factories.FormFactory(
            is_public=True,
            agenda_visible=True,
            administrative_entities=[self.fin_administrative_entity],
        )

        # ////////////////////////////////////#
        # Fields
        # ////////////////////////////////////#

        self.fin_title_field = factories.FieldFactory(
            name="title",
            api_name="title",
            api_light=True,
            filter_for_api=False,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_TEXT,
        )

        self.fin_location_field = factories.FieldFactory(
            name="location",
            api_name="location",
            api_light=False,
            filter_for_api=False,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_TEXT,
        )

        self.fin_category_field = factories.FieldFactory(
            name="category",
            api_name="category",
            api_light=True,
            filter_for_api=True,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="One\nTwo\nThree",
        )

        # ////////////////////////////////////#
        # Form fields
        # ////////////////////////////////////#

        factories.FormFieldFactory(
            form=self.fin_valid_agenda_form,
            field=self.fin_title_field,
        )

        factories.FormFieldFactory(
            form=self.fin_valid_agenda_form,
            field=self.fin_location_field,
        )

        factories.FormFieldFactory(
            form=self.fin_valid_agenda_form,
            field=self.fin_category_field,
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, with featured, valid date
        # ////////////////////////////////////#

        self.fin_first_submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.fin_administrative_entity,
            author=self.fin_normal_user,
            is_public_agenda=True,
            featured_agenda=True,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.fin_first_submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.fin_first_submission,
            form=self.fin_valid_agenda_form,
        )
        factories.FieldValueFactory(
            field=self.fin_title_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.fin_location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.fin_category_field,
            selected_form=selected_form,
            value={"val": "Premier"},
        )

    def test_light_and_detailed_works_correctly(self):
        """
        Light api should show multiple objects, have a next, previous, count, features.
        Detailed should show infos that are api_light=False.
        Field not public should not appear.
        Invalid configuration should not appear.
        """

        # ////////////////////////////////////#
        # Light API
        # ////////////////////////////////////#

        # Request to agenda-list (light API)
        response = self.client.get(reverse("agenda-list"), {})
        response_json = response.json()

        # Check if request is ok
        self.assertEqual(response.status_code, 200)

        # Check if there's a next
        self.assertContains(response, "next")

        # Check if there's a previous
        self.assertContains(response, "previous")

        # Check if there's a count (multiple objects)
        self.assertContains(response, "count")

        # Check if there's features (same number as count)
        self.assertEqual(len(response_json["features"]), response_json["count"])

        # Check private field doesn't appear
        self.assertNotContains(response, "private_field")

        # Check api_light=False field doesn't appear
        self.assertNotContains(response, "location")

        # ////////////////////////////////////#
        # Detailed API
        # ////////////////////////////////////#

        # Request to agenda_detail (detailed API)
        response = self.client.get(
            reverse("agenda-detail", kwargs={"pk": self.sit_first_submission.pk}), {}
        )
        response_json = response.json()

        # Check if request is ok
        self.assertEqual(response.status_code, 200)

        # Check there's not a next
        self.assertNotContains(response, "next")

        # Check there's not a previous
        self.assertNotContains(response, "previous")

        # Check there's not a count (multiple objects)
        self.assertNotContains(response, "count")

        # Check private field doesn't appear
        self.assertNotContains(response, "private_field")

        # Check api_light=False field appears in detailed
        self.assertContains(response, "location")

    def test_filters_only_appears_with_domain(self):
        """
        A domain is required to show filters.
        """

        # ////////////////////////////////////#
        # Without domain
        # ////////////////////////////////////#

        # Request to agenda-list (light API)
        response = self.client.get(reverse("agenda-list"), {})
        response_json = response.json()

        # Check if request is ok
        self.assertEqual(response.status_code, 200)

        # Check if filters is None
        self.assertEqual(response_json["filters"], None)

        # ////////////////////////////////////#
        # With domain
        # ////////////////////////////////////#

        # Request to agenda-list (light API) on ?domain=sit
        response = self.client.get(reverse("agenda-list"), {"domain": "sit"})
        response_json = response.json()

        # Check if request is ok
        self.assertEqual(response.status_code, 200)

        # Check if filters is not None
        self.assertNotEqual(response_json["filters"], None)

    # TODO: Count number of elements
    def test_elements_are_ordered_by_featured_and_dates(self):
        """
        Order of elements logic is in the backend.
        Featured should appear first and everything should be sorted by date.
        By default only return events that are in progress or still to come.
        """

        # Request to agenda-list (light API) on ?domain=sit
        response = self.client.get(reverse("agenda-list"), {"domain": "sit"})
        response_json = response.json()

        # Check if request is ok
        self.assertEqual(response.status_code, 200)

        # Check first element is first_submission
        self.assertEqual(
            response_json["features"][0]["properties"]["id"],
            self.sit_first_submission.pk,
        )

        # Check second element is fifth_submission
        self.assertEqual(
            response_json["features"][1]["properties"]["id"],
            self.sit_fifth_submission.pk,
        )

        # Check third element is second_submission
        self.assertEqual(
            response_json["features"][2]["properties"]["id"],
            self.sit_second_submission.pk,
        )

        # Check fourth element is third_submission
        self.assertEqual(
            response_json["features"][3]["properties"]["id"],
            self.sit_third_submission.pk,
        )

    def test_filters_work_correctly(self):
        """
        Filters by domain, date and custom filters does return the expected result.
        """

        # ////////////////////////////////////#
        # Filter by domain
        # ////////////////////////////////////#

        # Request to agenda-list (light API) on ?domain=sit
        response_sit = self.client.get(reverse("agenda-list"), {"domain": "sit"})
        response_json_sit = response_sit.json()

        # Request to agenda-list (light API) on ?domain=fin
        response_fin = self.client.get(reverse("agenda-list"), {"domain": "fin"})
        response_json_fin = response_fin.json()

        # Check if request is ok for sit
        self.assertEqual(response_sit.status_code, 200)

        # Check if request is ok for fin
        self.assertEqual(response_fin.status_code, 200)

        # Check number of submissions is different in two entities
        self.assertNotEqual(response_json_sit["count"], response_json_fin["count"])

        # Check filters are not empty
        self.assertNotEqual(response_json_sit["filters"], None)
        self.assertNotEqual(response_json_fin["filters"], None)

        # Check filters are different
        self.assertNotEqual(response_json_sit["filters"], response_json_fin["filters"])

        # Check if valid elements of sit doesn't appear in fin, as there's only 1 element valid in fin
        self.assertEqual(response_json_fin["count"], 1)

        # ////////////////////////////////////#
        # Filter by custom filter
        # ////////////////////////////////////#

        # Request to agenda-list (light API) on ?domain=sit
        response = self.client.get(
            reverse("agenda-list"), {"domain": "sit", "category": 0}
        )
        response_json = response.json()

        # Check if request is ok
        self.assertEqual(response.status_code, 200)

        # Check if there's only 1 feature
        self.assertEqual(response_json["count"], 1)

        # Check if this is the first_submission
        self.assertEqual(
            response_json["features"][0]["properties"]["id"],
            self.sit_first_submission.pk,
        )
