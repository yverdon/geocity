from django.test import TestCase

from permits.tests import factories


class GeocityTestCase(TestCase):
    SECRETARIAT = 0
    INTEGRATOR = 1
    SUPER_USER = 2

    def setUp(self):
        self.groups = {
            self.SECRETARIAT: factories.SecretariatGroupFactory(),
            self.INTEGRATOR: factories.IntegratorGroupFactory(),
        }

    def get_user(self, email, password, group):
        if group == self.SECRETARIAT:
            return factories.SecretariatUserFactory(
                email=email,
                password=password,
                groups=[self.groups[group]],
            )
        elif group == self.INTEGRATOR:
            return factories.IntegratorUserFactory(
                email=email,
                password=password,
                groups=[self.groups[group]],
            )
        elif group == self.SUPER_USER:
            return factories.SuperUserFactory(email=email, password=password)
        else:
            return factories.UserFactory(
                email=email,
                password=password,
            )

    def login(self, email, password="password", group=None):
        self.user = self.get_user(email=email, password=password, group=group)

        self.client.login(username=self.user.username, password=password)
