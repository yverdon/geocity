from urllib import parse
from urllib.parse import urlparse

from allauth.socialaccount.models import SocialApp
from constance import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import View

if settings.ENABLE_2FA:
    from two_factor.views import LoginView
else:
    from django.contrib.auth.views import LoginView

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

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


class CustomLoginView(LoginView, SetCurrentSiteMixin):
    def get(self, request, *args, **kwargs):
        successful = request.GET.get("success")
        # check if we need to display an activation message
        # if the value is None, we didn't come from the activation view
        if successful is None:
            pass
        elif successful == "True":
            messages.success(request, _("Votre compte a été activé avec succès!"))
        else:
            messages.error(request, _("Une erreur est survenu lors de l'activation"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"social_apps": SocialApp.objects.all()})

        return services.get_context_data(context, self.request)

    def done(self, form_list, **kwargs):
        permits_services.store_tags_in_session(self.request)
        return super(CustomLoginView, self).done(form_list, **kwargs)

    def get_success_url(self):

        qs_dict = parse.parse_qs(self.request.META["QUERY_STRING"])

        url_value = (
            qs_dict["next"][0]
            if "next" in qs_dict
            else reverse("permits:permit_request_select_administrative_entity")
        )

        if "next" in qs_dict:
            qs_dict.pop("next")

        return (
            reverse("two_factor:profile")
            if settings.ENABLE_2FA and not self.request.user.totpdevice_set.exists()
            else url_value
        )


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
