from django.test import TestCase

from permits.tests import factories


class GeocityTestCase(TestCase):
    SECRETARIAT = 0
    INTEGRATOR = 1
    SUPER_USER = 2

    def get_user(self, email, password, group):
        if group == self.SECRETARIAT:
            return factories.SecretariatUserFactory(
                email=email,
                password=password,
                groups=[factories.SecretariatGroupFactory()],
            )
        elif group == self.INTEGRATOR:
            return factories.IntegratorUserFactory(
                email=email,
                password=password,
                groups=[factories.IntegratorGroupFactory()],
            )
        elif group == self.SUPER_USER:
            return factories.SuperUserFactory(email=email, password=password)
        else:
            return factories.UserFactory(email=email, password=password,)

    def login(self, email, password="password", group=None):
        self.user = self.get_user(email=email, password=password, group=group)

        self.client.login(username=self.user.username, password=password)
