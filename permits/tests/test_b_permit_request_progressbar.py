from django.test import TestCase
from django.urls import reverse

from permits import models

from . import factories
from .utils import LoggedInUserMixin, get_parser


def extract_nav_items(content):
    nav_items = get_parser(content).select(".progress-nav-item .step-name")
    return [nav_item.text.strip() for nav_item in nav_items]


class PermitRequestProgressBarTestCase(LoggedInUserMixin, TestCase):
    def create_permit_request(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        return permit_request

    def test_works_objects_step_does_not_appear_when_only_one_object_on_administrative_entity(
        self,
    ):
        """
        Test that the works objects step doesn’t appear for an administrative entity
        with 2 works types that both have the same only works object.
        """
        permit_request = self.create_permit_request()
        works_object = factories.WorksObjectFactory()
        permit_request.administrative_entity.works_object_types.set(
            factories.WorksObjectTypeFactory.create_batch(2, works_object=works_object)
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)

        nav_items = extract_nav_items(response.content)
        self.assertIn("Type", nav_items)
        self.assertIn("Détails", nav_items)
        self.assertNotIn("Objets", nav_items)

    def test_works_objects_step_does_not_appear_when_only_one_object_on_permit_request(
        self,
    ):
        """
        Test that the works objects step doesn’t appear for a permit request with works
        types that have the same only works object.
        """
        permit_request = self.create_permit_request()
        works_object = factories.WorksObjectFactory()
        works_object_types = factories.WorksObjectTypeFactory.create_batch(
            2, works_object=works_object
        )
        permit_request.administrative_entity.works_object_types.set(works_object_types)
        permit_request.works_object_types.set(works_object_types)

        response = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)

        nav_items = extract_nav_items(response.content)
        self.assertIn("Type", nav_items)
        self.assertIn("Détails", nav_items)
        self.assertNotIn("Objets", nav_items)

    def test_works_object_step_appears_when_multiple_objects_on_selected_types(self):
        """
        Test that the works objects step appears after selecting works types that have
        more than 1 works object.
        """
        permit_request = self.create_permit_request()
        works_object_types = factories.WorksObjectTypeFactory.create_batch(2)
        permit_request.administrative_entity.works_object_types.set(works_object_types)

        response = self.client.get(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + f"?types={works_object_types[0].works_type_id}&types={works_object_types[1].works_type_id}"
        )

        self.assertEqual(response.status_code, 200)

        nav_items = extract_nav_items(response.content)
        self.assertIn("Type", nav_items)
        self.assertIn("Objets", nav_items)

    def test_works_types_step_does_not_appear_when_only_one_type(self):
        permit_request = self.create_permit_request()
        works_type = factories.WorksTypeFactory()
        permit_request.administrative_entity.works_object_types.set(
            factories.WorksObjectTypeFactory.create_batch(2, works_type=works_type)
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)

        nav_items = extract_nav_items(response.content)
        self.assertIn("Objets", nav_items)
        self.assertIn("Détails", nav_items)
        self.assertNotIn("Type", nav_items)

    def test_contacts_step_does_not_appear_when_no_contacts_required(self):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeFactory()
        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertNotIn("Contacts", nav_items)

    def test_contacts_step_appears_when_contacts_required(self):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeFactory()
        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])
        factories.PermitActorTypeFactory(works_type=works_object_type.works_type)

        response = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Contacts", nav_items)

    def test_appendices_step_does_not_appear_when_no_appendices_required(self):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeFactory()
        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertNotIn("Documents", nav_items)

    def test_appendices_step_appears_when_appendices_required(self):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeFactory()
        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])
        works_object_property = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_FILE,
        )
        works_object_property.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Documents", nav_items)

    def test_geotime_step_does_not_appear_when_no_date_nor_geometry_types_are_required(
        self,
    ):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeWithoutGeometryFactory(
            needs_date=False,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertNotIn("Planning et localisation", nav_items)
        self.assertNotIn("Planning", nav_items)
        self.assertNotIn("Localisation", nav_items)

    def test_geotime_step_appears_when_date_and_geometry_types_are_required(self):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=True,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Planning et localisation", nav_items)

    def test_geotime_step_appears_when_only_date_is_required(self):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeWithoutGeometryFactory(
            needs_date=True,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Planning", nav_items)
        self.assertNotIn("Planning et localisation", nav_items)
        self.assertNotIn("Localisation", nav_items)

    def test_geotime_step_appears_when_only_geometry_types_are_required(self):
        permit_request = self.create_permit_request()
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=False,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        nav_items = extract_nav_items(response.content)
        self.assertIn("Localisation", nav_items)
        self.assertNotIn("Planning et localisation", nav_items)
        self.assertNotIn("Planning", nav_items)
