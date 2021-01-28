# TODO split this file into multiple files
import urllib.parse
from datetime import date

from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from permits import models, services

from . import factories
from .utils import LoggedInSecretariatMixin, LoggedInUserMixin, get_emails, get_parser


def to_works_objects_dict(works_object_types):
    return {
        "works_objects-{}".format(works_object_type.works_type.pk): works_object_type.pk
        for works_object_type in works_object_types
    }


def get_permit_request_works_types_ids(permit_request):
    return list(
        permit_request.works_object_types.order_by("works_type__name")
        .values_list("works_type__pk", flat=True)
        .distinct()
    )


class PermitRequestTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.works_types = factories.WorksTypeFactory.create_batch(2)
        self.works_objects = factories.WorksObjectFactory.create_batch(2)

        models.WorksObjectType.objects.create(
            works_type=self.works_types[0], works_object=self.works_objects[0]
        )
        models.WorksObjectType.objects.create(
            works_type=self.works_types[1], works_object=self.works_objects[1]
        )

    def test_types_step_submit_redirects_to_objects_with_types_qs(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        response = self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={"types": [self.works_types[0].pk, self.works_types[1].pk]},
        )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?types={}&types={}".format(
                self.works_types[0].pk, self.works_types[1].pk
            ),
        )

    def test_objects_step_without_qs_redirects_to_types_step(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_objects_step_submit_saves_selected_object_types(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        # Create another works object type so that the works object step is not skipped
        factories.WorksObjectTypeFactory(works_type=self.works_types[0])

        works_object_type = models.WorksObjectType.objects.first()
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )
        self.client.post(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?types={}".format(self.works_types[0].pk),
            data={
                "works_objects-{}".format(self.works_types[0].pk): works_object_type.pk
            },
        )

        self.assertEqual(
            models.PermitRequest.objects.filter(
                works_object_types=works_object_type
            ).count(),
            1,
        )

    def test_non_required_properties_can_be_left_blank(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.set(permit_request.works_object_types.all())

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_user_can_only_see_own_requests(self):
        permit_request = factories.PermitRequestFactory(
            author=factories.UserFactory().permitauthor
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_non_draft_request(self):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_submit_permit_request_sends_email_to_secretariat(self):
        # Create a secretariat user Yverdon (the one that will get the notification)
        group = factories.SecretariatGroupFactory()
        factories.SecretariatUserFactory(email="secretariat@yverdon.ch", groups=[group])
        # This one should not receive the notification
        factories.SecretariatUserFactory(email="secretariat@lausanne.ch")

        permit_request = factories.PermitRequestGeoTimeFactory(
            permit_request=factories.PermitRequestFactory(
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user.permitauthor,
                status=models.PermitRequest.STATUS_DRAFT,
            )
        ).permit_request
        self.client.post(
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        emails = get_emails("Nouvelle demande de permis")

        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0].to, ["secretariat@yverdon.ch"])

    def test_missing_mandatory_date_property_gives_invalid_feedback(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_DATE, is_mandatory=True
        )
        prop.works_object_types.set(permit_request.works_object_types.all())

        data = {
            "properties-{}_{}".format(works_object_type.pk, prop.pk): ""
            for works_object_type in permit_request.works_object_types.all()
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )
        parser = get_parser(response.content)
        self.assertEqual(len(parser.select(".invalid-feedback")), 1)

    def test_works_object_automatically_set_when_only_one_works_object(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object = factories.WorksObjectFactory()
        permit_request.administrative_entity.works_object_types.set(
            factories.WorksObjectTypeFactory.create_batch(2, works_object=works_object)
        )
        works_type_id = permit_request.administrative_entity.works_object_types.values_list(
            "works_type_id", flat=True
        ).first()

        self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={"types": [works_type_id]},
        )

        permit_request.refresh_from_db()
        works_object_types = permit_request.works_object_types.all()

        self.assertEqual(
            len(works_object_types),
            1,
            "Permit request should have one works object type set",
        )
        self.assertEqual(works_object_types[0].works_object, works_object)
        self.assertEqual(works_object_types[0].works_type_id, works_type_id)

    def test_works_type_automatically_set_when_only_one_works_object(self):
        works_type = factories.WorksTypeFactory()
        administrative_entity = factories.PermitAdministrativeEntityFactory()
        administrative_entity.works_object_types.set(
            factories.WorksObjectTypeFactory.create_batch(2, works_type=works_type)
        )

        response = self.client.post(
            reverse("permits:permit_request_select_administrative_entity",),
            data={"administrative_entity": administrative_entity.pk},
        )

        permit_request = models.PermitRequest.objects.get()

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + f"?types={works_type.pk}",
        )

    def test_geotime_step_only_date_fields_appear_when_only_date_is_required(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            needs_geometry=False, needs_date=True
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(
            len(get_parser(response.content).select('input[name="form-0-starts_at"]')),
            1,
        )
        self.assertGreaterEqual(
            len(get_parser(response.content).select('input[name="form-0-ends_at"]')), 1
        )

        self.assertEqual(
            len(get_parser(response.content).select('textarea[name="form-0-geom"]')), 0,
        )

    def test_geotime_step_only_geom_fields_appear_when_only_geom_is_required(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            needs_geometry=True, needs_date=False
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(
            len(get_parser(response.content).select('textarea[name="form-0-geom"]')), 1,
        )

        self.assertEqual(
            len(get_parser(response.content).select('input[name="form-0-starts_at"]')),
            0,
        )
        self.assertEqual(
            len(get_parser(response.content).select('input[name="form-0-ends_at"]')), 0
        )

    def test_geotime_step_date_and_geom_fields_appear_when_both_required(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            needs_geometry=True, needs_date=True
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(
            len(get_parser(response.content).select('input[name="form-0-starts_at"]')),
            1,
        )
        self.assertGreaterEqual(
            len(get_parser(response.content).select('input[name="form-0-ends_at"]')), 1
        )
        self.assertGreaterEqual(
            len(get_parser(response.content).select('textarea[name="form-0-geom"]')), 1,
        )


class PermitRequestActorsTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.test_formset_data = {
            "form-TOTAL_FORMS": ["1"],
            "form-INITIAL_FORMS": ["0"],
            "form-MIN_NUM_FORMS": ["0"],
            "form-MAX_NUM_FORMS": ["1000"],
            "creditor_type": [""],
            "form-0-actor_type": "",
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

    def test_permitrequestactor_creates(self):
        works_object_type = factories.WorksObjectTypeFactory()
        works_type = works_object_type.works_type

        actor_required = factories.PermitActorTypeFactory(
            is_mandatory=True, works_type=works_type
        )

        self.test_formset_data["form-0-actor_type"] = actor_required.type

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_DRAFT
        )

        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.set([works_object_type])

        self.client.post(
            reverse(
                "permits:permit_request_actors",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=self.test_formset_data,
        )

        actors = list(permit_request.actors.all())
        self.assertEqual(len(actors), 1, "Expected 1 actor created")
        self.assertEqual(actors[0].first_name, "John")

    def test_permitrequestactor_required_cannot_have_empty_field(self):
        works_object_type = factories.WorksObjectTypeFactory()
        works_type = works_object_type.works_type

        actor_required = factories.PermitActorTypeFactory(
            is_mandatory=True, works_type=works_type
        )

        self.test_formset_data["form-0-actor_type"] = actor_required.type

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_DRAFT
        )

        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.set([works_object_type])

        self.test_formset_data["form-0-last_name"] = ""

        response = self.client.post(
            reverse(
                "permits:permit_request_actors",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
            data=self.test_formset_data,
        )

        permit_request.refresh_from_db()
        # Check that no actor was saved for this permit
        self.assertEqual(permit_request.actors.count(), 0)
        # Check that if form not valid, it does not redirect
        self.assertEqual(response.status_code, 200)


class PermitRequestUpdateTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor
        )
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=self.permit_request
        )
        self.permit_request.administrative_entity.works_object_types.set(
            self.permit_request.works_object_types.all()
        )

    def test_types_step_submit_shows_new_objects(self):
        new_works_object_type = factories.WorksObjectTypeFactory()

        new_works_object_type.administrative_entities.set(
            [self.permit_request.administrative_entity]
        )

        response = self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            follow=True,
            data={
                "types": get_permit_request_works_types_ids(self.permit_request)
                + [new_works_object_type.works_type.pk]
            },
        )

        self.assertContains(response, new_works_object_type.works_type)

    def test_types_step_submit_removes_deselected_types_from_permit_request(self):
        works_object_type_id = get_permit_request_works_types_ids(self.permit_request)[
            0
        ]

        self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={"types": works_object_type_id},
        )

        self.permit_request.refresh_from_db()

        self.assertEqual(models.PermitRequest.objects.count(), 1)
        self.assertEqual(
            get_permit_request_works_types_ids(self.permit_request),
            [works_object_type_id],
        )

    def test_objects_step_submit_updates_permit_request(self):
        new_works_object_type = factories.WorksObjectTypeFactory()
        self.permit_request.administrative_entity.works_object_types.add(
            new_works_object_type
        )
        current_works_object_types = list(self.permit_request.works_object_types.all())
        current_works_object_types_dict = to_works_objects_dict(
            current_works_object_types
        )
        new_works_object_types_dict = to_works_objects_dict([new_works_object_type])
        works_types_ids = get_permit_request_works_types_ids(self.permit_request) + [
            new_works_object_type.works_type.pk
        ]
        types_param = urllib.parse.urlencode({"types": works_types_ids}, doseq=True)

        self.client.post(
            (
                reverse(
                    "permits:permit_request_select_objects",
                    kwargs={"permit_request_id": self.permit_request.pk},
                )
                + "?"
                + types_param
            ),
            data={**current_works_object_types_dict, **new_works_object_types_dict},
        )

        self.permit_request.refresh_from_db()

        self.assertEqual(models.PermitRequest.objects.count(), 1)
        self.assertEqual(
            set(self.permit_request.works_object_types.all()),
            set(current_works_object_types + [new_works_object_type]),
        )

    def test_properties_step_submit_updates_permit_request(self):
        new_prop = factories.WorksObjectPropertyFactory()
        new_prop.works_object_types.set(self.permit_request.works_object_types.all())
        data = {
            "properties-{}_{}".format(
                works_object_type.pk, new_prop.pk
            ): "value-{}".format(works_object_type.pk)
            for works_object_type in self.permit_request.works_object_types.all()
        }
        self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data=data,
        )

        self.assertEqual(
            set(
                item["val"]
                for item in services.get_properties_values(
                    self.permit_request
                ).values_list("value", flat=True)
            ),
            set(data.values()),
        )

    def test_missing_mandatory_address_property_gives_invalid_feedback(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeAddress(
            input_type=models.WorksObjectProperty.INPUT_TYPE_ADDRESS, is_mandatory=True
        )
        prop.works_object_types.set(permit_request.works_object_types.all())

        data = {
            "properties-{}_{}".format(works_object_type.pk, prop.pk): ""
            for works_object_type in permit_request.works_object_types.all()
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )
        parser = get_parser(response.content)
        parser.select(".invalid-feedback")
        self.assertEqual(1, len(parser.select(".invalid-feedback")))

    def test_properties_step_submit_updates_permit_request_with_address(self):
        address_prop = factories.WorksObjectPropertyFactoryTypeAddress(
            input_type=models.WorksObjectProperty.INPUT_TYPE_ADDRESS
        )
        address_prop.works_object_types.set(
            self.permit_request.works_object_types.all()
        )
        works_object_type = self.permit_request.works_object_types.first()
        data = {
            f"properties-{works_object_type.pk}_{address_prop.pk}": "Hôtel Martinez, Cannes"
        }
        self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data=data,
        )

        self.permit_request.refresh_from_db()
        prop_val = services.get_properties_values(self.permit_request).get(
            property__input_type=models.WorksObjectProperty.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(prop_val.value, {"val": "Hôtel Martinez, Cannes"})

    def test_properties_step_submit_updates_permit_request_with_date(self):

        date_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_DATE, name="datum"
        )
        today = date.today()
        works_object_type = self.permit_request.works_object_types.first()
        date_prop.works_object_types.set([works_object_type])
        data = {
            f"properties-{works_object_type.pk}_{date_prop.pk}": today.strftime(
                settings.DATE_INPUT_FORMAT
            )
        }
        self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data=data,
        )

        prop_val = services.get_properties_values(self.permit_request).get(
            property__name="datum"
        )
        self.assertEqual(
            prop_val.value, {"val": today.isoformat()},
        )
        self.assertEqual(
            prop_val.property.input_type, models.WorksObjectProperty.INPUT_TYPE_DATE,
        )


class PermitRequestPrefillTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor
        )
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=self.permit_request
        )
        self.permit_request.administrative_entity.works_object_types.set(
            self.permit_request.works_object_types.all()
        )

    def test_types_step_preselects_types_for_existing_permit_request(self):
        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()

        for i, works_type_id in enumerate(
            get_permit_request_works_types_ids(self.permit_request)
        ):
            expected = (
                '<input checked="" class="form-check-input" id="id_types_{i}" name="types" title=""'
                '  type="checkbox" value="{value}"/>'
            ).format(value=works_type_id, i=i)
            self.assertInHTML(expected, content)

    def test_objects_step_preselects_objects_for_existing_permit_request(self):
        response = self.client.get(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()

        for works_object_type in self.permit_request.works_object_types.all():
            expected = (
                '<input checked="" class="form-check-input" id="id_works_objects-{id}_0"'
                ' name="works_objects-{id}" title="" type="checkbox" value="{value}"/>'
            ).format(id=works_object_type.works_type.pk, value=works_object_type.pk)
            self.assertInHTML(expected, content)

    def test_properties_step_prefills_properties_for_existing_permit_request(self):
        works_object_type_choice = services.get_works_object_type_choices(
            self.permit_request
        ).first()
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.add(works_object_type_choice.works_object_type)
        prop_value = factories.WorksObjectPropertyValueFactory(
            works_object_type_choice=works_object_type_choice, property=prop
        )
        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()
        expected = '<textarea name="properties-{obj_type_id}_{prop_id}" cols="40" rows="1" class="form-control" title="" id="id_properties-{obj_type_id}_{prop_id}">{value}</textarea>'.format(
            obj_type_id=works_object_type_choice.works_object_type.pk,
            prop_id=prop.pk,
            prop_name=prop.name,
            value=prop_value.value["val"],
        )

        self.assertInHTML(expected, content)

    def test_properties_step_order_properties_for_existing_permit_request(self):

        works_object_type_choice = services.get_works_object_type_choices(
            self.permit_request
        ).first()

        prop_1 = factories.WorksObjectPropertyFactory(order=10)
        prop_2 = factories.WorksObjectPropertyFactory(order=2)
        prop_1.works_object_types.add(works_object_type_choice.works_object_type)
        prop_2.works_object_types.add(works_object_type_choice.works_object_type)

        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()
        position_1 = content.find(prop_1.name)
        position_2 = content.find(prop_2.name)
        self.assertGreater(position_1, position_2)


class PermitRequestAmendmentTestCase(LoggedInSecretariatMixin, TestCase):
    def test_non_secretariat_user_cannot_amend_request(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user.permitauthor,
        )
        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "price": 300,
                "status": models.PermitRequest.STATUS_PROCESSING,
                "action": models.ACTION_AMEND,
            },
        )

        permit_request.refresh_from_db()

        self.assertIsNone(permit_request.price)

    def test_secretariat_can_amend_request(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "price": 300,
                "status": models.PermitRequest.STATUS_PROCESSING,
                "action": models.ACTION_AMEND,
                "archeology_status": models.PermitRequest.ARCHEOLOGY_STATUS_IRRELEVANT,
            },
        )

        permit_request.refresh_from_db()
        self.assertEqual(permit_request.price, 300)

    def test_secretariat_can_see_submitted_requests(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.get(reverse("permits:permit_requests_list"))

        self.assertEqual(list(response.context["permitrequest_list"]), [permit_request])

    def test_ask_for_supplements_shows_specific_message(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )

        self.assertContains(response, "compléments")

    def test_secretariat_cannot_amend_permit_request_with_validation_requested(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={"price": 200, "action": models.ACTION_AMEND},
        )

        self.assertEqual(response.status_code, 400)


class PermitRequestValidationRequestTestcase(LoggedInSecretariatMixin, TestCase):
    def test_secretariat_can_request_validation(self):
        validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity
        )
        validator_departments = [
            group.permitdepartment.pk for group in validator_groups
        ]

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "departments": validator_departments,
                "action": models.ACTION_REQUEST_VALIDATION,
            },
        )

        permit_request.refresh_from_db()

        self.assertEqual(
            permit_request.status, models.PermitRequest.STATUS_AWAITING_VALIDATION
        )
        self.assertEqual(
            list(permit_request.validations.values_list("department", flat=True)),
            validator_departments,
        )

    def test_secretariat_cannot_request_validation_for_already_validated_permit_request(
        self,
    ):
        validator_group = factories.ValidatorGroupFactory(
            department__administrative_entity=self.administrative_entity
        )

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "departments": [validator_group.permitdepartment.pk],
                "action": models.ACTION_REQUEST_VALIDATION,
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

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
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
        validator_user = factories.ValidatorUserFactory(groups=[validator_groups[0]])
        factories.ValidatorUserFactory(groups=[validator_groups[1]])

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "departments": [validator_groups[0].permitdepartment.pk],
                "action": models.ACTION_REQUEST_VALIDATION,
            },
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator_user.permitauthor.user.email])


class PermitRequestValidationTestcase(TestCase):
    def test_validator_can_see_assigned_permit_requests(self):
        validation = factories.PermitRequestValidationFactory()
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=validator.username, password="password")

        response = self.client.get(reverse("permits:permit_requests_list"))

        self.assertEqual(
            list(response.context["permitrequest_list"]), [validation.permit_request]
        )

    def test_validator_can_validate_assigned_permit_requests(self):
        validation = factories.PermitRequestValidationFactory()
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=validator.username, password="password")

        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "action": models.ACTION_VALIDATE,
                "validation_status": models.PermitRequestValidation.STATUS_APPROVED,
            },
        )

        validation.refresh_from_db()

        self.assertEqual(
            validation.validation_status, models.PermitRequestValidation.STATUS_APPROVED
        )

    def test_validator_cannot_validate_non_assigned_permit_requests(self):
        validation = factories.PermitRequestValidationFactory()
        factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )
        validator = factories.ValidatorUserFactory()

        self.client.login(username=validator.username, password="password")

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "action": models.ACTION_VALIDATE,
                "validation_status": models.PermitRequestValidation.STATUS_APPROVED,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_secretariat_can_send_validation_reminders(self):
        group = factories.SecretariatGroupFactory()
        administrative_entity = group.permitdepartment.administrative_entity
        secretariat = factories.SecretariatUserFactory(groups=[group])

        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=administrative_entity
        )
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=secretariat.username, password="password")

        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={"action": models.ACTION_POKE,},
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator.permitauthor.user.email])


class PermitRequestClassifyTestCase(TestCase):
    def setUp(self):
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permitdepartment.administrative_entity
        )
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity
        )
        self.validator_user = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

    def test_secretariat_can_classify_permit_request(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "validation_pdf": SimpleUploadedFile("file.pdf", "contents".encode())
            },
        )

        self.assertRedirects(response, reverse("permits:permit_requests_list"))
        validation.permit_request.refresh_from_db()
        self.assertEqual(
            validation.permit_request.status, models.PermitRequest.STATUS_APPROVED
        )

    def test_secretariat_cannot_classify_permit_request_with_pending_validations(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={"validation_pdf": SimpleUploadedFile("file.pdf", "")},
        )

        self.assertEqual(response.status_code, 404)

    def test_secretariat_does_not_see_classify_form_when_pending_validations(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            )
        )

        self.assertNotContains(
            response,
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
        )

    def test_user_without_permission_cannot_classify_permit_request(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
        )
        user = factories.UserFactory(actor=validation.permit_request.author)
        self.client.login(username=user.username, password="password")

        approve_url = reverse(
            "permits:permit_request_approve",
            kwargs={"permit_request_id": validation.permit_request.pk},
        )

        response = self.client.post(
            approve_url, data={"validation_pdf": SimpleUploadedFile("file.pdf", "")}
        )

        self.assertRedirects(
            response, "%s?next=%s" % (reverse(settings.LOGIN_URL), approve_url)
        )

    def test_permit_request_validation_file_accessible_to_permit_request_author(self):
        author_user = factories.UserFactory()
        permit_request = factories.PermitRequestFactory(
            validated_at=timezone.now(),
            status=models.PermitRequest.STATUS_APPROVED,
            author=author_user.permitauthor,
        )
        # This cannot be performed in the factory because we need the permit request to have an id to upload a file
        permit_request.validation_pdf = SimpleUploadedFile("file.pdf", b"contents")
        permit_request.save()

        self.client.login(username=author_user, password="password")
        response = self.client.get(permit_request.validation_pdf.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"contents")

    def test_permit_request_validation_file_not_accessible_to_other_users(self):
        non_author_user = factories.UserFactory()
        permit_request = factories.PermitRequestFactory(
            validated_at=timezone.now(), status=models.PermitRequest.STATUS_APPROVED
        )
        # This cannot be performed in the factory because we need the permit request to have an id to upload a file
        permit_request.validation_pdf = SimpleUploadedFile("file.pdf", b"contents")
        permit_request.save()

        self.client.login(username=non_author_user, password="password")
        response = self.client.get(permit_request.validation_pdf.url)
        self.assertEqual(response.status_code, 404)

    def test_classify_sets_validation_date(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={"validation_pdf": SimpleUploadedFile("file.pdf", b"contents")},
        )

        validation.permit_request.refresh_from_db()
        self.assertIsNotNone(validation.permit_request.validated_at)
