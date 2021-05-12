from bs4 import BeautifulSoup

from django.core import mail

from . import factories


def get_parser(content):
    return BeautifulSoup(content, features="html5lib")


def get_emails(subject):
    return [email for email in mail.outbox if email.subject == subject]


class LoggedInUserMixin:
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")


class LoggedInSecretariatMixin:
    def setUp(self):
        self.group = factories.SecretariatGroupFactory()
        self.administrative_entity = self.group.permitdepartment.administrative_entity
        self.user = factories.SecretariatUserFactory(groups=[self.group])
        self.client.login(username=self.user.username, password="password")


class LoggedInIntegrator:
    def setUp(self):
        self.group = factories.IntegratorGroupFactory()
        self.user = factories.IntegratorUserFactory(groups=[self.group])
        self.client.login(username=self.user.username, password="password")
