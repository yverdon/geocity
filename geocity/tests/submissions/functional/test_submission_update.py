from datetime import date

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from geocity.apps.forms import models as forms_models
from geocity.apps.submissions import models as submissions_models
from geocity.tests import factories
from geocity.tests.utils import LoggedInUserMixin, get_parser


class SubmissionUpdateTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory.create_batch(3, submission=self.submission)
        self.submission.administrative_entity.forms.set(self.submission.forms.all())

    def test_form_step_submit_updates_submission(self):
        new_form = factories.FormFactory()
        self.submission.administrative_entity.forms.add(new_form)
        current_forms = list(self.submission.forms.all())

        self.client.post(
            (
                reverse(
                    "submissions:submission_select_forms",
                    kwargs={"submission_id": self.submission.pk},
                )
            ),
            data={
                "forms-selected_forms": [form.pk for form in current_forms + [new_form]]
            },
        )

        self.submission.refresh_from_db()

        self.assertEqual(submissions_models.Submission.objects.count(), 1)
        self.assertEqual(
            set(self.submission.forms.all()),
            set(current_forms + [new_form]),
        )

    def test_fields_step_submit_updates_submission(self):
        new_field = factories.FieldFactory()
        new_field.forms.set(self.submission.forms.all())
        data = {
            "fields-{}_{}".format(form.pk, new_field.pk): "value-{}".format(form.pk)
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
                for item in self.submission.get_fields_values().values_list(
                    "value", flat=True
                )
            ),
            set(data.values()),
        )

    def test_missing_mandatory_address_field_gives_invalid_feedback(self):
        submission = factories.SubmissionFactory(author=self.user)
        factories.SelectedFormFactory(submission=submission)
        submission.administrative_entity.forms.set(submission.forms.all())
        field = factories.FieldFactoryTypeAddress(
            input_type=submissions_models.Field.INPUT_TYPE_ADDRESS, is_mandatory=True
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
            input_type=submissions_models.Field.INPUT_TYPE_ADDRESS
        )
        address_field.forms.set(self.submission.forms.all())
        form = self.submission.forms.first()
        data = {f"fields-{form.pk}_{address_field.pk}": "Hôtel Martinez, Cannes"}
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        self.submission.refresh_from_db()
        field_val = self.submission.get_fields_values().get(
            field__input_type=submissions_models.Field.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(field_val.value, {"val": "Hôtel Martinez, Cannes"})

    def test_fields_step_submit_updates_geotime_with_address_store_geometry_for_address_field(
        self,
    ):
        address_field = factories.FieldFactoryTypeAddress(
            input_type=submissions_models.Field.INPUT_TYPE_ADDRESS,
            store_geometry_for_address_field=True,
        )
        address_field.forms.set(self.submission.forms.all())
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
        field_val = self.submission.get_fields_values().get(
            field__input_type=submissions_models.Field.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(
            field_val.value, {"val": "Place pestalozzi 2, 1400 Yverdon-les-Bains"}
        )
        geocoded_geotime_row = submissions_models.SubmissionGeoTime.objects.filter(
            submission=self.submission, comes_from_automatic_geocoding=True
        ).count()
        self.assertEqual(1, geocoded_geotime_row)

    def test_fields_step_submit_updates_submission_with_date(self):
        date_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_DATE, name="datum"
        )
        today = date.today()
        form = self.submission.forms.first()
        date_field.forms.set([form])
        data = {
            f"fields-{form.pk}_{date_field.pk}": today.strftime(
                settings.DATE_INPUT_FORMATS[0]
            )
        }
        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        field_val = self.submission.get_fields_values().get(field__name="datum")
        self.assertEqual(
            field_val.value,
            {"val": today.isoformat()},
        )
        self.assertEqual(
            field_val.field.input_type,
            submissions_models.Field.INPUT_TYPE_DATE,
        )

    def test_fields_step_submit_saves_geometry_field(self):

        test_geometry_value = '{ "type": "GeometryCollection", "geometries": [ { "type": "MultiPoint", "coordinates": [ [ 2539123.31, 1181095.01 ] ] } ] }'
        test_map_config = '{"wfs": {"url": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=ELE_tragwerk_gesco"}, "mode": {"type": "select"}, "wmts": [], "zoom": 15, "border": {"url": "", "notification": "Veuillez placer votre élément dans les limites autorisées"}, "search": {"displaySearch": true, "bboxRestiction": "", "requestWithoutCustomValue": "https://api3.geo.admin.ch/rest/services/api/SearchServer?limit=5&&type=locations&sr=2056&lang=fr&origins=address%2Cparcel"}, "cluster": {"distance": 40, "minDistance": 35}, "maxZoom": 20, "minZoom": 1, "information": {"title": "Signaler ...", "content": "", "duration": 5000}, "interaction": {"fullscreen": true, "displayZoom": true, "enableRotation": true, "displayScaleLine": false, "enableGeolocation": true, "enableCenterButton": true}, "outputFormat": "GeometryCollection", "defaultCenter": [2539057, 1181111], "inclusionArea": {"url": "", "filter": ""}, "notifications": [{"rule": {"type": "ZOOM_CONSTRAINT", "minZoom": 16, "maxElement": null, "couldBypass": null}, "type": "warning", "message": "Veuillez zoomer davantage avant de pouvoir sélectionner un emplacement."}, {"rule": {"type": "MAX_SELECTION", "minZoom": null, "maxElement": 1, "couldBypass": null}, "type": "warning", "message": "Le maximum de sélection est limité à {x}."}, {"rule": {"type": "INFORMATION", "minZoom": null, "maxElement": null, "couldBypass": null}, "type": "info", "message": "Sélectionnez un marqueur sur la carte."}], "geolocationInformation": {"displayBox": true, "currentLocation": false, "reverseLocation": true}, "selectionTargetBoxMessage": ""}'

        # Define the map widget for advanced geometry
        map_widget_configuration = forms_models.MapWidgetConfiguration.objects.create(
            name="Sélection d'objets",
            configuration=test_map_config,
        )

        # Create the field and assign the widget
        geom_field = factories.FieldFactory(
            input_type=submissions_models.Field.INPUT_TYPE_GEOM, name="geom"
        )
        geom_field.map_widget_configuration = map_widget_configuration
        geom_field.save()

        # Assign new field to the form
        form = self.submission.forms.first()
        geom_field.forms.set([form])

        # Fill the widget
        data = {f"fields-{form.pk}_{geom_field.pk}": test_geometry_value}

        self.client.post(
            reverse(
                "submissions:submission_fields",
                kwargs={"submission_id": self.submission.pk},
            ),
            data=data,
        )

        # Check that the field value is saved into SubmissionGeoTime model
        geotime_count_after = submissions_models.SubmissionGeoTime.objects.all().count()
        self.assertEqual(
            geotime_count_after,
            1,
        )

        # Check that geometry is saved correctly
        item = submissions_models.SubmissionGeoTime.objects.first()
        self.assertEqual(
            test_geometry_value,
            item.geom.geojson,
        )
