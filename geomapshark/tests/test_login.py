from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse

from permits.tests import factories


class TestLoginMixin:
    def test_get_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion")


if not settings.ENABLE_2FA:

    class TestLoginView(TestCase, TestLoginMixin):
        def test_post_login_view(self):
            user = factories.UserFactory()
            response = self.client.post(
                reverse("login"),
                {"username": user.username, "password": "password"},
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

        def test_post_login_view_fail(self):
            response = self.client.post(reverse("login"), {}, follow=True)
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
                reverse("login"),
                {
                    "auth-username": user.username,
                    "auth-password": "password",
                    "login_view-current_step": "auth",
                },
                follow=True,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

        def test_post_login_view_fail(self):
            response = self.client.post(reverse("login"), {}, follow=True)
            self.assertEqual(response.status_code, 400)

        def test_post_login_view_with_step_fail(self):
            response = self.client.post(
                reverse("login"), {"login_view-current_step": "auth"}, follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                "Votre mot de passe et votre nom d'utilisateur ne correspondent pas",
            )
