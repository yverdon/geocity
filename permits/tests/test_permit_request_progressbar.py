import re

from django.test import TestCase
from django.urls import reverse

from . import factories
from .utils import LoggedInUserMixin, get_parser


def extract_nav_items(content):
    nav_items = get_parser(content).select(".progress-nav-item")
    nav_items_text = [
        re.sub(r"\s+", " ", nav_item.get_text()).strip() for nav_item in nav_items
    ]
    return [
        tuple(nav_item_text.split(" ", maxsplit=1)) for nav_item_text in nav_items_text
    ]


class PermitRequestProgressBarTestCase(LoggedInUserMixin, TestCase):
    def create_permit_request(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        return permit_request

    def test_works_objects_step_does_not_appear_when_only_one_object(self):
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
        self.assertIn(("2", "Type"), nav_items)
        self.assertIn(("3", "Détails"), nav_items)
        self.assertNotIn("Objets", [nav_item_text[1] for nav_item_text in nav_items])

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
        self.assertIn(("2", "Objets"), nav_items)
        self.assertIn(("3", "Détails"), nav_items)
        self.assertNotIn("Type", [nav_item_text[1] for nav_item_text in nav_items])
