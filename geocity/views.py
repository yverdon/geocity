from urllib import parse
from urllib.parse import urlparse

import duo_universal
from allauth.socialaccount.models import SocialApp
from constance import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import View
from two_factor.views import LoginView as TwoFactorLoginView

from geocity.apps.permits import forms, models
from geocity.apps.permits import services as permits_services

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


# User has tried to many login attempts
def lockout_view(request):
    return render(
        request,
        "account/lockout.html",
    )


class SetCurrentSiteMixin:
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        current_site = get_current_site(self.request)
        settings.SITE_ID = current_site.id
        settings.SITE_DOMAIN = current_site.domain


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


def get_redirect_url_after_login(qs_dict):
    url_value = (
        qs_dict["next"][0]
        if "next" in qs_dict
        else reverse("permits:permit_request_select_administrative_entity")
    )
    return url_value


def create_duo_client(username, request):
    # Initial value of duo_client
    duo_client = None

    # Get user corresponding to the user name
    user = User.objects.get(username=username)

    # Get PermitDepartments using duo. Need to retrieve data for duo_universal.Client() or call exchange_authorization_code_for_2fa_result()
    permitdepartement = (
        models.PermitDepartment.objects.filter(
            group__in=user.groups.all(), mandatory_2fa=True
        )
        .exclude(duo_client_id__exact="")
        .exclude(duo_client_secret__exact="")
        .exclude(duo_host__exact="")
    )

    # Tells if duo multi factor authentication is activated
    duo_mfa = permitdepartement.exists()
    if duo_mfa:
        # Retrieve information for duo_universal.Client from first PermitDepartment
        client_id = permitdepartement[0].duo_client_id
        client_secret = permitdepartement[0].duo_client_secret
        host = permitdepartement[0].duo_host

        # Define the callback
        callback_url = request.build_absolute_uri(reverse("duo_callback"))

        # Create the duo_universal.Client
        duo_client = duo_universal.Client(client_id, client_secret, host, callback_url)
    return user, duo_mfa, duo_client


class CustomTwoFactorLoginView(TwoFactorLoginView):
    # Add default value to duo_mfa to prevent a throw error on "self.steps.current != 'auth'"
    def __init__(self, **kwargs):
        self.duo_mfa = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        successful = request.GET.get("success")
        # check if we need to display an activation message
        # if the value is None, we didn't come from the activation view
        if successful is None:
            pass
        elif successful == "True":
            messages.success(
                request,
                _(
                    "Votre compte a été activé avec succès! Vous pouvez maintenant vous connecter à l'aide de vos identifiants."
                ),
            )
        else:
            messages.error(request, _("Une erreur est survenu lors de l'activation"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"social_apps": SocialApp.objects.all()})

        return services.get_context_data(context, self.request)

    def done(self, form_list, **kwargs):
        permits_services.store_tags_in_session(self.request)

        # Redirect to the duo authentication page
        if self.duo_mfa:
            return redirect(self.prompt_uri)
        return super(CustomTwoFactorLoginView, self).done(form_list, **kwargs)

    def get_success_url(self):
        qs_dict = parse.parse_qs(self.request.META["QUERY_STRING"])

        url_value = get_redirect_url_after_login(qs_dict)

        return (
            reverse("two_factor:profile")
            if settings.ENABLE_2FA and not self.request.user.totpdevice_set.exists()
            else url_value
        )

    def process_step(self, form):
        # Override only this step
        if self.steps.current == "auth":
            # Get username
            username = form.is_valid() and form.user_cache

            # Get user, duo_mfa and duo_client
            user, self.duo_mfa, duo_client = create_duo_client(username, self.request)

            if self.duo_mfa:
                # Health check
                try:
                    duo_client.health_check()
                except:
                    raise Exception("Duo n'est pas disponible pour le moment.")

                # Generate the actual state
                state = duo_client.generate_state()

                # Get query_string. Used to know if there is a "next" in the request
                qs_dict = parse.parse_qs(self.request.META["QUERY_STRING"])

                # Store state, username and qs_disct in session
                self.request.session["state"] = state
                self.request.session["username"] = user.username
                self.request.session["qs_dict"] = qs_dict

                # Create url to duo authentication page. Used in self.done()
                self.prompt_uri = duo_client.create_auth_url(user.username, state)
            else:
                # When duo isn't activated, use django 2fa
                return super().process_step(form)
        else:
            return super().process_step(form)


class DuoCallbackView(View):
    def get(self, request, *args, **kwargs):
        # Get informations from duo
        state = request.GET.get("state")
        duo_code = request.GET.get("duo_code")

        # Get stored sessions
        session_state = request.session["state"]
        session_username = request.session["username"]
        session_qs_dict = request.session["qs_dict"]

        # Get user, duo_mfa and duo_client
        user, duo_mfa, duo_client = create_duo_client(session_username, request)

        # Check if state didn't change
        if state != session_state:
            raise Exception("Un problème de sécurité est survenu.")

        # Ask to duo if the connection was made correctly
        try:
            decoded_token = duo_client.exchange_authorization_code_for_2fa_result(
                duo_code, user.username
            )
        except:
            raise Exception("Un problème de connection est survenu.")

        # Log the user
        login(request, user, "django.contrib.auth.backends.ModelBackend")

        url_value = get_redirect_url_after_login(session_qs_dict)
        return redirect(url_value)


def permit_author_create(request):
    djangouserform = forms.NewDjangoAuthUserForm(request.POST or None)
    permitauthorform = forms.GenericAuthorForm(request.POST or None)
    is_valid = djangouserform.is_valid() and permitauthorform.is_valid()

    if is_valid:
        new_user = djangouserform.save()
        # email wasn't verified yet, so account isn't active just yet
        new_user.is_active = False
        new_user.save()
        permitauthorform.instance.user = new_user
        permitauthorform.save()

        mail_subject = _("Activer votre compte")
        message = render_to_string(
            "registration/emails/email_confirmation.txt",
            {
                "user": new_user,
                "domain": get_current_site(request).domain,
                "url": reverse(
                    "activate_account",
                    kwargs={
                        # we need the user id to validate the token
                        "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                        "token": default_token_generator.make_token(new_user),
                    },
                ),
                "signature": _("L'équipe de Geocity"),
            },
        )

        email = EmailMessage(mail_subject, message, to=[new_user.email])
        email.send()
        messages.success(
            request,
            _(
                "Votre compte a été créé avec succès! Vous allez recevoir un email pour valider et activer votre compte."
            ),
        )
        return redirect(reverse("account_login"))

    return render(
        request,
        "permits/permit_request_author.html",
        {"permitauthorform": permitauthorform, "djangouserform": djangouserform},
    )


class ActivateAccountView(View):
    def get(self, request, uid, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        successful = user and default_token_generator.check_token(user, token)
        if successful:
            user.is_active = True
            user.save()

        return redirect(reverse("account_login") + f"?success={successful}")


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
