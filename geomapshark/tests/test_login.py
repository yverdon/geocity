from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse

from permits.tests import factories
from permits.models import TemplateCustomization
from constance import config
from bs4 import BeautifulSoup


def get_parser(content):
    return BeautifulSoup(content, features="html5lib")


class TestLoginMixin:
    def test_get_login_view(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion")


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
            self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

        def test_post_login_view_fail(self):
            response = self.client.post(reverse("account_login"), {}, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                "Votre mot de passe et votre nom d'utilisateur ne correspondent pas",
            )


if settings.ENABLE_2FA:

    class TestLoginView2FA(TestCase, TestLoginMixin):
        def test_post_login_view(self):
            user = factories.UserFactory()
            response = self.client.post(
                reverse("account_login"),
                {
                    "auth-username": user.username,
                    "auth-password": "password",
                    "custom_login_view-current_step": "auth",
                },
                follow=True,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

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
            "<div>" + customization.application_description + "</div>"
        )

        parser = get_parser(response.content)
        title = str(parser.select("#login-welcome-text h3")[0])
        subtitle = str(parser.select("#login-welcome-text h5")[0])
        description = str(parser.select("#login-welcome-text div")[0])

        self.assertEqual(response.status_code, 200)
        self.assertHTMLEqual(title, expected_title)
        self.assertHTMLEqual(subtitle, expected_subtitle)
        self.assertHTMLEqual(description, expected_description)

    def test_get_standard_login_view(self):

        response = self.client.get(reverse("account_login"),)
        content = response.content.decode()

        expected_title = "<h3>" + config.APPLICATION_TITLE + "</h3>"
        expected_subtitle = "<h5>" + config.APPLICATION_SUBTITLE + "</h5>"
        expected_description = "<div>" + config.APPLICATION_DESCRIPTION + "</div>"

        parser = get_parser(response.content)
        title = str(parser.select("#login-welcome-text h3")[0])
        subtitle = str(parser.select("#login-welcome-text h5")[0])
        description = str(parser.select("#login-welcome-text div")[0])

        self.assertEqual(response.status_code, 200)
        self.assertHTMLEqual(title, expected_title)
        self.assertHTMLEqual(subtitle, expected_subtitle)
        self.assertHTMLEqual(description, expected_description)
