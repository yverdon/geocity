from django.core.exceptions import ValidationError
from django.test import TestCase

from geocity.tests.factories import AdministrativeEntityFactory, FormFactory
from geocity.tests.utils import LoggedInUserMixin


class AdministrativeEntityTestCase(LoggedInUserMixin, TestCase):
    def test_administrative_entity_containing_shared_public_forms_is_invalid(self):
        entity1 = AdministrativeEntityFactory()
        entity2 = AdministrativeEntityFactory()
        FormFactory(administrative_entities=[entity1, entity2], is_public=True)
        FormFactory(administrative_entities=[entity1], is_public=True)

        self.assertRaises(ValidationError, entity1.clean)

    def test_administrative_entity_containing_owned_public_forms_is_valid(self):
        entity1 = AdministrativeEntityFactory()
        FormFactory(administrative_entities=[entity1], is_public=True)
        FormFactory(administrative_entities=[entity1], is_public=True)

        entity1.clean()
