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

        self.administrative_entity = factories.AdministrativeEntityFactory(tags=["sit"])
        self.group = factories.SecretariatGroupFactory(department=None)
        factories.PermitDepartmentFactory(
            administrative_entity=self.administrative_entity,
            is_backoffice=True,
            group=self.group,
        ),

        # Create normal User
        self.normal_user = factories.UserFactory()

        # ////////////////////////////////////#
        # Agenda forms
        # ////////////////////////////////////#

        # Create valid agenda Forms
        self.valid_agenda_form = factories.FormFactory(
            is_public=True,
            agenda_visible=True,
            administrative_entities=[self.administrative_entity],
        )
        self.valid_agenda_form.administrative_entities.set([self.administrative_entity])
        self.valid_agenda_form.save()

        self.administrative_entity.forms.add(self.valid_agenda_form.pk)

        # Create not valid agenda first iteration Forms
        self.not_valid_agenda_form_1 = factories.FormFactory(
            is_public=False,
            agenda_visible=True,
            administrative_entities=[self.administrative_entity],
        )

        # Create not valid agenda second iteration Forms
        self.not_valid_agenda_form_2 = factories.FormFactory(
            is_public=True,
            agenda_visible=False,
            administrative_entities=[self.administrative_entity],
        )

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
        # Valid submission for agenda, with featured, valid date
        # ////////////////////////////////////#

        self.submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
            is_public_agenda=True,  # TODO: Duplicate with this at false to be sure not visible
            featured_agenda=True,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission,
            form=self.valid_agenda_form,
        )
        factories.FieldValueFactory(field=self.title_field, selected_form=selected_form)
        factories.FieldValueFactory(
            field=self.location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.category_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, valid date
        # ////////////////////////////////////#

        self.submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission,
            form=self.valid_agenda_form,
        )
        factories.FieldValueFactory(field=self.title_field, selected_form=selected_form)
        factories.FieldValueFactory(
            field=self.location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.category_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, valid date but later
        # ////////////////////////////////////#

        self.submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.submission,
            starts_at=start_at_valid_2,
            ends_at=ends_at_valid_2,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission,
            form=self.valid_agenda_form,
        )
        factories.FieldValueFactory(field=self.title_field, selected_form=selected_form)
        factories.FieldValueFactory(
            field=self.location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.category_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, passed date
        # ////////////////////////////////////#

        self.submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.submission,
            starts_at=start_at_passed,
            ends_at=ends_at_passed,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission,
            form=self.valid_agenda_form,
        )
        factories.FieldValueFactory(field=self.title_field, selected_form=selected_form)
        factories.FieldValueFactory(
            field=self.location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.category_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Valid submission for agenda, without featured, passed start but still active
        # ////////////////////////////////////#

        self.submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
            is_public_agenda=True,
            featured_agenda=False,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.submission,
            starts_at=start_at_passed,
            ends_at=ends_at_valid_2,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission,
            form=self.valid_agenda_form,
        )
        factories.FieldValueFactory(field=self.title_field, selected_form=selected_form)
        factories.FieldValueFactory(
            field=self.location_field, selected_form=selected_form
        )
        factories.FieldValueFactory(
            field=self.category_field, selected_form=selected_form
        )

        # ////////////////////////////////////#
        # Invalid submission for agenda, with featured, valid date. Pilot haven't turn public
        # ////////////////////////////////////#

        self.submission = factories.SubmissionFactory(
            status=submissions_models.Submission.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
            author=self.normal_user,
            is_public_agenda=False,
            featured_agenda=True,
        )

        factories.SubmissionGeoTimeFactory(
            submission=self.submission,
            starts_at=start_at_valid_1,
            ends_at=ends_at_valid_1,
        )
        selected_form = factories.SelectedFormFactory(
            submission=self.submission,
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
        response = self.client.get(reverse("agenda-list"), {"domain": "sit"})
        response_json = response.json()
        print(response_json)
        # print(self.title_field)
        # print(self.title_field.api_light)
        # print(self.title_field.public_if_submission_public)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response_json["detail"],
            "Vous n'avez pas la permission d'effectuer cette action.",
        )


# Test avec tous les status, s'affichent qu'avec les bons status # TODO: MAKE DATA OR IGNORE AS IT IS EASY TO KNOW IF IT WORKS
# Test élément dans light et pas élément pas dans light # DATA DISPO
# Test configuration, si le moindre élément manque, rien ne s'affiche # TODO: Make more data, some parts missing, only able to do on submission. Need more selected_form:  form=self.valid_agenda_form,
# Les filtres apparaissent que s'il y a un domaine # DATA DISPO
# Check order element (features, dates) # DATA DISPO
# Check filters work correctly (domaines, types, dates, etc..) # DATA DISPO
# Check if filters work correctly together, when we put multiple times # TODO: make data
# Check if too much filters throw an error # DATA DISPO
# Check le queryset par defaut : date comprises entre aujourd'hui et x # DATA DISPO
# TODO : Make another entity with another tag, and check if data doesn't appear
