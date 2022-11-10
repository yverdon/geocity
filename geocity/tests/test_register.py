from captcha.models import CaptchaStore
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from geocity.apps.permits.tests import factories


class TestRegisterMixin:
    def test_get_register_view(self):
        response = self.client.get(reverse("accounts:user_profile_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mon compte")

    def test_post_register_view_fail(self):
        response = self.client.post(reverse("accounts:user_profile_create"), {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


class TestRegisterView(TestCase, TestRegisterMixin):
    def generate_captcha(self):
        return CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())

    def get_user_data(self):
        return {
            "username": "joe",
            "password1": "yCKntcz@#3&U%8",
            "password2": "yCKntcz@#3&U%8",
            "first_name": "Joe",
            "last_name": "Blow",
            "email": "foo@bar.com",
            "address": "an address",
            "zipcode": 1007,
            "city": "Lausanne",
            "phone_first": "0789124692",
        }

    def test_user_cannot_register_if_email_is_used(self):
        data = self.get_user_data()
        captcha = self.generate_captcha()
        self.client.post(
            reverse("accounts:user_profile_create"),
            {**data, **{"captcha_0": captcha.hashkey, "captcha_1": captcha.response}},
            follow=True,
        )
        self.client.post(reverse("logout"))
        response = self.client.post(
            reverse("accounts:user_profile_create"), data, follow=True
        )
        self.assertContains(response, "Cet email est déjà utilisé.")
        self.assertFalse(response.context["user"].is_authenticated)

    def execute_post_register(self):
        data = self.get_user_data()
        captcha = self.generate_captcha()
        return self.client.post(
            reverse("accounts:user_profile_create"),
            {
                **data,
                **{"captcha_0": captcha.hashkey, "captcha_1": captcha.response},
            },
            follow=True,
        )

    def test_account_activation_success(self):
        self.execute_post_register()
        user = User.objects.get(email=self.get_user_data()["email"])

        response = self.client.get(
            reverse(
                "activate_account",
                kwargs={
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            ),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["QUERY_STRING"], "success=True")
        self.assertContains(response, "Votre compte a été activé avec succès!")

    def test_account_activation_fail(self):
        self.execute_post_register()
        user = User.objects.get(email=self.get_user_data()["email"])
        user2 = factories.UserFactory()

        response = self.client.get(
            reverse(
                "activate_account",
                kwargs={
                    "uid": urlsafe_base64_encode(force_bytes(user2.pk)),
                    "token": default_token_generator.make_token(user),
                },
            ),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["QUERY_STRING"], "success=False")
        self.assertContains(response, "Une erreur est survenu")

    def test_user_cannot_register_if_captcha_isnot_filled(self):
        data = self.get_user_data()
        response = self.client.post(
            reverse("accounts:user_profile_create"), data, follow=True
        )
        self.assertEquals(
            response.context[0]["permitauthorform"].errors["captcha"],
            ["Ce champ est obligatoire."],
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_post_register_view(self):
        response = self.execute_post_register()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)
        self.assertRedirects(response, resolve_url("account_login"))
        self.assertContains(
            response,
            "Votre compte a été créé avec succès! Vous allez recevoir un email pour valider et activer votre compte.",
        )
        self.assertEqual(len(mail.outbox), 1)
