from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse
from django_otp import DEVICE_ID_SESSION_KEY
from two_factor.utils import default_device

from geocity.apps.permits.tests.factories import SuperUserFactory

# Make sure we don't patch the admin site by mistake
if not settings.ENABLE_2FA:

    class TestAdminSite(TestCase):
        def test_superuser_get_admin_login_superuser_not_auth(self):
            response = self.client.get(reverse("admin:login"))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "administration Geocity")


if settings.ENABLE_2FA:

    class TestAdminSite2FA(TestCase):

        password = SuperUserFactory.password

        def login_user(self, user=None):
            username = user.get_username()
            assert self.client.login(username=username, password=self.password)
            if default_device(user):
                session = self.client.session
                session[DEVICE_ID_SESSION_KEY] = default_device(user).persistent_id
                session.save()

        def enable_otp(self, user=None):
            return user.totpdevice_set.create(name="default")

        def test_superuser_get_admin_login_superuser_not_auth(self):
            response = self.client.get(reverse("admin:login"), follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertRedirects(
                response,
                "%s?next=%s"
                % (resolve_url("account_login"), reverse(settings.LOGIN_REDIRECT_URL)),
            )

        def test_superuser_get_admin_after_login_but_not_otp_verified(self):
            superuser = SuperUserFactory()
            self.client.login(username=superuser.username, password=self.password)
            response = self.client.get(reverse("admin:login"), follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertRedirects(response, resolve_url("two_factor:setup"))

        def test_superuser_get_admin_after_login_and_otp_verified(self):
            superuser = SuperUserFactory()
            self.enable_otp(user=superuser)
            self.login_user(user=superuser)
            response = self.client.get(reverse("admin:login"), follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertRedirects(response, resolve_url("admin:index"))
            self.assertContains(response, "administration Geocity")
