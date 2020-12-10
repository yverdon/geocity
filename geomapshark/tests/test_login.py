from django.conf import settings
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse

from permits import factories

if not settings.ENABLE_2FA:
    class TestLoginView(TestCase):

        def test_get_login_view_classic(self):
            response = self.client.get(reverse('login'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Connexion')

        def test_post_login_view_classic(self):
            user = factories.UserFactory()
            response = self.client.post(reverse('login'), {
                'username': user.username,
                'password': 'password'
            }, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['user'].is_authenticated)
            self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))


if settings.ENABLE_2FA:
    class TestLoginView2FA(TestCase):

        def test_post_login_view_2fa(self):
            user = factories.UserFactory()
            response = self.client.post(reverse('login'), {
                'auth-username': user.username,
                'auth-password': 'password',
                'login_view-current_step': 'auth'
            }, follow=True)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['user'].is_authenticated)
            self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))
