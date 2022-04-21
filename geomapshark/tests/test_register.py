from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse
from captcha.models import CaptchaStore
from django.contrib.auth import logout
from django.core import mail


class TestRegisterMixin:
    def test_get_register_view(self):
        response = self.client.get(reverse("permit_author_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mon compte")

    def test_post_register_view_fail(self):
        response = self.client.post(reverse("permit_author_create"), {})
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
            reverse("permit_author_create"),
            {**data, **{"captcha_0": captcha.hashkey, "captcha_1": captcha.response}},
            follow=True,
        )
        self.client.post(reverse("logout"))
        response = self.client.post(reverse("permit_author_create"), data, follow=True)
        self.assertContains(response, "Cet email est déjà utilisé.")
        self.assertFalse(response.context["user"].is_authenticated)

    def test_user_cannot_register_if_captcha_isnot_filled(self):
        data = self.get_user_data()
        response = self.client.post(reverse("permit_author_create"), data, follow=True)
        self.assertEquals(
            response.context[0]["permitauthorform"].errors["captcha"],
            ["Ce champ est obligatoire."],
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def execute_post_register(self):
        data = self.get_user_data()
        captcha = self.generate_captcha()
        return self.client.post(
            reverse("permit_author_create"),
            {**data, **{"captcha_0": captcha.hashkey, "captcha_1": captcha.response},},
            follow=True,
        )

    if settings.ENABLE_2FA:

        def test_post_register_view(self):
            response = self.execute_post_register()
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(response, resolve_url("two_factor:profile"))

    else:

        def test_post_register_view(self):
            response = self.execute_post_register()
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context["user"].is_authenticated)
            self.assertRedirects(response, resolve_url("account_login"))
            self.assertContains(
                response,
                "Votre compte a été créé avec succès! Vous allez recevoir un email pour valider votre email",
            )
            self.assertEqual(len(mail.outbox), 1)
