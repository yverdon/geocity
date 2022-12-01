from django.core.exceptions import ValidationError
from django.test import TestCase

from geocity.tests.factories import AdministrativeEntityFactory, FormFactory
from geocity.tests.utils import LoggedInUserMixin


class AdministrativeEntityTestCase(LoggedInUserMixin, TestCase):
    def test_cant_save_single_demands_by_form_if_multi_forms_exist(self):
        entity1 = AdministrativeEntityFactory()
        entity2 = AdministrativeEntityFactory()
        FormFactory(administrative_entities=[entity1, entity2], is_public=True)

        entity1.is_single_form_submissions = True
        self.assertRaises(ValidationError, entity1.clean)

    def test_can_save_single_demands_by_form(self):
        entity1 = AdministrativeEntityFactory()
        FormFactory(administrative_entities=[entity1], is_public=True)

        entity1.is_single_form_submissions = True
        entity1.clean()
