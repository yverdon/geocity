from django.test import TestCase

from permits.tests import factories


class GeocityTestCase(TestCase):
    SECRETARIAT = 0
    INTEGRATOR = 1
    VALIDATOR = 2
    SUPER_USER = 3

    def setUp(self):
        self.administrative_entity = factories.PermitAdministrativeEntityFactory()
        self.groups = {
            self.SECRETARIAT: factories.SecretariatGroupFactory.create(department=None),
            self.INTEGRATOR: factories.IntegratorGroupFactory.create(department=None),
            self.VALIDATOR: factories.ValidatorGroupFactory.create(department=None),
        }
        self.departments = {
            self.SECRETARIAT: factories.PermitDepartmentFactory(
                administrative_entity=self.administrative_entity,
                is_backoffice=True,
                group=self.groups[self.SECRETARIAT],
            ),
            self.INTEGRATOR: factories.PermitDepartmentFactory(
                administrative_entity=self.administrative_entity,
                is_integrator_admin=True,
                group=self.groups[self.INTEGRATOR],
            ),
            self.VALIDATOR: factories.PermitDepartmentFactory(
                administrative_entity=self.administrative_entity,
                is_validator=True,
                group=self.groups[self.VALIDATOR],
            ),
        }

    def get_user(self, email, password, group):
        if group == self.SECRETARIAT:
            return factories.SecretariatUserFactory.create(
                email=email, password=password, groups=[self.groups[group]],
            )
        elif group == self.INTEGRATOR:
            return factories.IntegratorUserFactory.create(
                email=email, password=password, groups=[self.groups[group]],
            )
        elif group == self.VALIDATOR:
            return factories.ValidatorUserFactory.create(
                email=email, password=password, groups=[self.groups[group]]
            )
        elif group == self.SUPER_USER:
            return factories.SuperUserFactory(email=email, password=password)
        else:
            return factories.UserFactory(email=email, password=password,)

    def login(self, email, password="password", group=None):
        self.user = self.get_user(email=email, password=password, group=group)

        self.client.login(username=self.user.username, password=password)
