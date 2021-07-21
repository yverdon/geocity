from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import logout


def get_user_data():
    return {
        "username": "joe",
        "password1": "4512carlos",
        "password2": "4512carlos",
        "first_name": "Joe",
        "last_name": "Blow",
        "email": "foo@bar.com",
        "address": "an address",
        "zipcode": 1007,
        "city": "Lausanne",
        "phone_first": "0789124692",
    }


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
    def test_user_cannot_register_if_email_is_used(self):
        data = get_user_data()
        self.client.post(reverse("permit_author_create"), data, follow=True)
        self.client.post(reverse("logout"))
        response = self.client.post(reverse("permit_author_create"), data, follow=True)
        self.assertContains(response, "Cet email est déjà utilisé.")
        self.assertFalse(response.context["user"].is_authenticated)

    if settings.ENABLE_2FA:

        def test_post_register_view(self):
            data = get_user_data()
            response = self.client.post(
                reverse("permit_author_create"), data, follow=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(response, resolve_url("two_factor:profile"))

    else:

        def test_post_register_view(self):
            data = get_user_data()
            response = self.client.post(
                reverse("permit_author_create"), data, follow=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["user"].is_authenticated)
            self.assertRedirects(
                response,
                resolve_url("permits:permit_request_select_administrative_entity"),
            )
