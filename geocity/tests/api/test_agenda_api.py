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

        self.group = factories.SecretariatGroupFactory()
        self.administrative_entity = self.group.permit_department.administrative_entity

        # Create normal User
        self.normal_user = factories.UserFactory()

        # ////////////////////////////////////#
        # Agenda forms
        # ////////////////////////////////////#

        # Create valid agenda Forms
        self.valid_agenda_form = factories.FormFactory(
            is_public=True,
            agenda_visible=True,
        )
        self.administrative_entity.forms.add(self.valid_agenda_form)

        # Create not valid agenda first iteration Forms
        self.not_valid_agenda_form_1 = factories.FormFactory(
            is_public=False,
            agenda_visible=True,
        )
        self.administrative_entity.forms.add(self.not_valid_agenda_form_1)

        # Create not valid agenda second iteration Forms
        self.not_valid_agenda_form_2 = factories.FormFactory(
            is_public=True,
            agenda_visible=False,
        )
        self.administrative_entity.forms.add(self.not_valid_agenda_form_2)

        # ////////////////////////////////////#
        # Fields
        # ////////////////////////////////////#

        self.title_field = factories.FieldFactory(
            name="title",
            api_name="title",
            api_light=True,
            filter_for_api=False,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_TEXT,
        )

        self.location_field = factories.FieldFactory(
            name="location",
            api_name="location",
            api_light=False,
            filter_for_api=False,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_TEXT,
        )

        self.category_field = factories.FieldFactory(
            name="category",
            api_name="category",
            api_light=True,
            filter_for_api=True,
            public_if_submission_public=True,
            input_type=forms_models.Field.INPUT_TYPE_LIST_MULTIPLE,
            choices="First\nSecond\nThird",
        )

        # ////////////////////////////////////#
        # Submissions
        # ////////////////////////////////////#

        # Submission valid agenda
        self.submission_valid_agenda = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
            is_public_agenda=True,  # TODO: Duplicate with this at false to be sure not visible
            featured_agenda=True,  # TODO: Duplicate with featured_agenda at false, to check if it works correctly
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission_valid_agenda,
            form=self.valid_agenda_form,
        )
        factories.FieldValueFactory(field=self.title_field, selected_form=selected_form)
        factories.FieldValueFactory(
            field=self.location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.category_field, selected_form=selected_form
        )

    def test_test_test_test(self):
        response = self.client.get(reverse("agenda-list"), {})
        response_json = response.json()
        print(response_json)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["detail"],
            "Vous n'avez pas la permission d'effectuer cette action.",
        )


# Test avec tous les status, s'affichent qu'avec les bons status
# Test élément dans light et pas élément pas dans light
# Test configuration, si le moindre élément manque, rien ne s'affiche
# Les filtres apparaissent que s'il y a un domaine
# Check order element (features, dates)
# Check filters work correctly (domaines, types, dates, etc..)
# Check if filters work correctly together, when we put multiple times
# Check if too much filters throw an error
