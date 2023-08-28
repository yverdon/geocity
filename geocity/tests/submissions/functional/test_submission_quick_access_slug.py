from django.test import TestCase

from geocity.tests import factories


class SubmissionQuickAccessSlugTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        entity = factories.AdministrativeEntityFactory()
        self.user = factories.UserFactory()
        self.form = factories.FormFactory()

        # Use one admin entity and add a field so that we don't skip the screen.
        self.form.administrative_entities.set([entity])
        factories.FormFieldFactory(form=self.form)

    def test_quick_access_slug_redirects(self):
        self.client.login(username=self.user, password="password")

        response = self.client.get(f"/?q={self.form.quick_access_slug}", follow=True)

        content = response.content.decode()
        self.assertIn(self.form.name, content)
