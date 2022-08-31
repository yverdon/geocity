from unittest import mock

from bs4 import BeautifulSoup
from constance import config
from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse
from django_otp.util import random_hex

from permits.tests import factories


def get_parser(content):
    return BeautifulSoup(content, features="html5lib")


class TestLoginMixin:
    def test_get_login_view(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion")

    def enable_otp(self, user):
        return user.totpdevice_set.create(name="default")


if not settings.ENABLE_2FA:

    class TestLoginView(TestCase, TestLoginMixin):
        def test_post_login_view(self):
            user = factories.UserFactory()
            response = self.client.post(
                reverse("account_login"),
                {"username": user.username, "password": "password"},
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(
                response,
                resolve_url("permits:permit_request_select_administrative_entity"),
            )

        def test_post_login_view_fail(self):
            response = self.client.post(reverse("account_login"), {}, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                "Votre mot de passe et votre nom d'utilisateur ne correspondent pas",
            )


if settings.ENABLE_2FA:

    class TestLoginView2FA(TestCase, TestLoginMixin):
        def login(self, data):
            return self.client.post(
                reverse("account_login"),
                data,
                follow=True,
            )

        def test_post_login_view_2FA_inactive(self):
            user = factories.UserFactory()
            response = self.login(
                data={
                    "auth-username": user.username,
                    "auth-password": "password",
                    "custom_login_view-current_step": "auth",
                }
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(response, resolve_url("two_factor:profile"))

        @mock.patch("two_factor.views.core.time")
        def test_post_login_view_2FA_active(self, mock_time):
            mock_time.time.return_value = 12345.12
            user = factories.UserFactory()
            user.totpdevice_set.create(name="default", key=random_hex())
            response = self.login(
                data={
                    "auth-username": user.username,
                    "auth-password": "password",
                    "custom_login_view-current_step": "auth",
                }
            )

            self.assertContains(response, "Jeton")
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context["user"].is_authenticated)

        def test_post_login_view_fail(self):
            response = self.client.post(reverse("account_login"), {}, follow=True)
            self.assertEqual(response.status_code, 400)

        def test_post_login_view_with_step_fail(self):
            response = self.client.post(
                reverse("account_login"),
                {"custom_login_view-current_step": "auth"},
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                "Votre mot de passe et votre nom d'utilisateur ne correspondent pas",
            )


class TestLoginPage(TestCase):
    def test_get_customized_login_view(self):
        customization = factories.TemplateCustomizationFactory()
        response = self.client.get(
            reverse("account_login"), data={"template": customization.templatename}
        )

        expected_title = "<h3>" + customization.application_title + "</h3>"
        expected_subtitle = "<h5>" + customization.application_subtitle + "</h5>"
        expected_description = (
            '<div class="login-description">'
            + customization.application_description
            + "</div>"
        )

        parser = get_parser(response.content)
        title = str(parser.select(".login-welcome-text h3")[0])
        subtitle = str(parser.select(".login-welcome-text h5")[0])
        description = str(parser.select(".login-description")[0])

        self.assertEqual(response.status_code, 200)
        self.assertHTMLEqual(title, expected_title)
        self.assertHTMLEqual(subtitle, expected_subtitle)
        self.assertHTMLEqual(description, expected_description)

    def test_get_standard_login_view(self):

        response = self.client.get(
            reverse("account_login"),
        )
        content = response.content.decode()

        expected_title = "<h3>" + config.APPLICATION_TITLE + "</h3>"
        expected_subtitle = "<h5>" + config.APPLICATION_SUBTITLE + "</h5>"
        expected_description = (
            '<div class="login-description">'
            + config.APPLICATION_DESCRIPTION
            + "</div>"
        )

        parser = get_parser(response.content)
        title = str(parser.select(".login-welcome-text h3")[0])
        subtitle = str(parser.select(".login-welcome-text h5")[0])
        description = str(parser.select(".login-description")[0])

        self.assertEqual(response.status_code, 200)
        self.assertHTMLEqual(title, expected_title)
        self.assertHTMLEqual(subtitle, expected_subtitle)
        self.assertHTMLEqual(description, expected_description)


class TestRemoteUserLogin(TestCase):
    def setUp(self):
        super().setUp()
        if (
            "django.contrib.auth.backends.RemoteUserBackend"
            not in settings.AUTHENTICATION_BACKENDS
        ):
            settings.AUTHENTICATION_BACKENDS.append(
                "django.contrib.auth.backends.RemoteUserBackend"
            )
        if (
            "django.contrib.auth.middleware.RemoteUserMiddleware"
            not in settings.MIDDLEWARE
        ):
            settings.MIDDLEWARE.append(
                "django.contrib.auth.middleware.RemoteUserMiddleware"
            )

    def test_automatic_login_of_remote_user(self):
        user = factories.UserFactory()
        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            follow=True,
            REMOTE_USER=user.username,
        )

        self.assertTrue(response.context["user"].is_authenticated)
        self.assertNotContains(response, "Connexion")
        self.assertContains(response, "Entité administrative")

    def test_automatic_login_of_remote_user_refuses_inactive_users(self):
        user = factories.UserFactory(is_active=False)
        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            follow=True,
            REMOTE_USER=user.username,
        )

        self.assertFalse(response.context["user"].is_authenticated)
        self.assertContains(response, "Connexion")
        self.assertNotContains(response, "Entité administrative")

    def test_automatic_login_of_remote_user_refuses_when_user_is_empty(self):
        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            follow=True,
            REMOTE_USER="",
        )

        self.assertFalse(response.context["user"].is_authenticated)
        self.assertContains(response, "Connexion")
        self.assertNotContains(response, "Entité administrative")

    def test_login_with_credentials_works_when_remote_user_is_empty(self):
        user = factories.UserFactory()
        response1 = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            follow=True,
            REMOTE_USER="",
        )

        self.assertEqual(response1.status_code, 200)
        self.assertRedirects(
            response1,
            f"{resolve_url('account_login')}?next=/permit-requests/administrative-entity/",
        )
        self.assertFalse(response1.context["user"].is_authenticated)
        self.assertContains(response1, "Connexion")
        self.assertNotContains(response1, "Entité administrative")

        self.client.login(username=user.username, password="password")
        response2 = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            follow=True,
            REMOTE_USER="",
        )

        self.assertTrue(response2.context["user"].is_authenticated)
        self.assertNotContains(response2, "Connexion")
        self.assertContains(response2, "Entité administrative")


# Disabling the REMOTE_USER
class TestRemoteUserLoginNotAllowed(TestCase):
    def setUp(self):
        super().setUp()
        # Tests run twice! Second time, setting will be already gone.
        try:
            settings.AUTHENTICATION_BACKENDS.remove(
                "django.contrib.auth.backends.RemoteUserBackend"
            )
            settings.MIDDLEWARE.remove(
                "django.contrib.auth.middleware.RemoteUserMiddleware"
            )
        except ValueError:
            pass

    def test_automatic_login_of_remote_user_is_denied(self):
        user = factories.UserFactory()
        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            follow=True,
            REMOTE_USER=user.username,
        )

        self.assertFalse(response.context["user"].is_authenticated)
        self.assertContains(response, "Connexion")
        self.assertNotContains(response, "Entité administrative")
