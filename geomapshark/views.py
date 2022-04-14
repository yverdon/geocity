from urllib.parse import urlparse

from allauth.socialaccount.models import SocialApp
from constance import config

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.views import View

from two_factor.views import LoginView as TwoFactorLoginView
from django.contrib.auth.views import LoginView

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from permits import forms, models
from permits import services as permits_services
from . import services


def logout_view(request):
    templatename = (
        request.session.pop("templatename")
        if "templatename" in request.session
        else None
    )
    logout(request)

    redirect_uri = request.GET.get("next", None)
    # Check if redirect URI is whitelisted
    if redirect_uri and urlparse(
        redirect_uri
    ).hostname in config.LOGOUT_REDIRECT_HOSTNAME_WHITELIST.split(","):
        return redirect(redirect_uri)
    return redirect(
        f'{reverse("account_login")}?template={templatename}'
        if templatename
        else reverse("account_login")
    )


# User has tried to many login attemps
def lockout_view(request):
    return render(request, "account/lockout.html",)


class CustomPasswordResetView(PasswordResetView):

    extra_email_context = {"custom_host": ""}

    def get_context_data(self, **kwargs):
        context = super(CustomPasswordResetView, self).get_context_data(**kwargs)
        domain = (
            "https://" + self.request.build_absolute_uri().split("//")[1].split("/")[0]
        )
        self.extra_email_context["custom_host"] = domain
        self.extra_email_context["site_name"] = self.request.build_absolute_uri().split(
            "/"
        )[2]
        return context


class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"social_apps": SocialApp.objects.all()})

        return services.get_context_data(context, self.request)


class CustomTwoFactorLoginView(TwoFactorLoginView):
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({"social_apps": SocialApp.objects.all()})

        return services.get_context_data(context, self.request)

    def process_step(self, form):
        if self.steps.current == 'token':
            import duo_universal
            from django.contrib.sessions.backends.db import SessionStore
            # TODO: retrieve credentials from environment
            # TODO: callback_url = self.request.build_absolute_uri(reverse('duo_callback'))
            callback_url = "https://geocity.docker.test/account/duo_callback"
            #duo_client = duo_universal.Client(client_id, client_secret, host, callback_url)

            state = duo_client.generate_state()
            s = SessionStore()
            s["state"] = state
            # TODO get username
            prompt_uri = duo_client.create_auth_url("aju", state)
            print(prompt_uri)
            redirect(prompt_uri)


class DuoCallbackView(View):
    def get(self, request, *args, **kwargs):
        state = request.GET.get('state')
        username = request.GET.get('username')
        # TODO:  Check if state and username matches session data
        # TODO: get session and compare state

        # TODO: if state is OK, login, then redirect to URL
        # login(username)
        return redirect(settings.LOGIN_REDIRECT_URL)


def permit_author_create(request):
    djangouserform = forms.NewDjangoAuthUserForm(request.POST or None)
    permitauthorform = forms.GenericAuthorForm(request.POST or None)
    is_valid = djangouserform.is_valid() and permitauthorform.is_valid()

    if is_valid:
        new_user = djangouserform.save()
        permitauthorform.instance.user = new_user
        permitauthorform.save()

        login(request, new_user)
        permits_services.store_tags_in_session(request)
        if settings.ENABLE_2FA:
            return HttpResponseRedirect(
                reverse("two_factor:profile")
                + (
                    "?" + request.META["QUERY_STRING"]
                    if request.META["QUERY_STRING"]
                    else ""
                )
            )
        return HttpResponseRedirect(
            reverse("permits:permit_request_select_administrative_entity")
            + (
                "?" + request.META["QUERY_STRING"]
                if request.META["QUERY_STRING"]
                else ""
            )
        )

    return render(
        request,
        "permits/permit_request_author.html",
        {"permitauthorform": permitauthorform, "djangouserform": djangouserform},
    )


@login_required
def permit_author_edit(request):

    djangouserform = forms.DjangoAuthUserForm(
        request.POST or None, instance=request.user
    )
    # prevent a crash when admin accesses this page
    permitauthorform = None
    if hasattr(request.user, "permitauthor"):
        permit_author_instance = get_object_or_404(
            models.PermitAuthor, pk=request.user.permitauthor.pk
        )
        permitauthorform = forms.GenericAuthorForm(
            request.POST or None, instance=permit_author_instance
        )

    if djangouserform.is_valid() and permitauthorform and permitauthorform.is_valid():
        user = djangouserform.save()
        permitauthorform.instance.user = user
        permitauthorform.save()

        return HttpResponseRedirect(reverse("permits:permit_requests_list"))

    return render(
        request,
        "permits/permit_request_author.html",
        {"permitauthorform": permitauthorform, "djangouserform": djangouserform},
    )
