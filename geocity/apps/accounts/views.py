import mimetypes
from urllib import parse
from urllib.parse import urlparse

from allauth.socialaccount.models import SocialApp
from constance import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404, StreamingHttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
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

from geocity.apps.accounts.decorators import (
    check_mandatory_2FA,
    permanent_user_required,
)
from geocity.fields import PrivateFileSystemStorage

from . import forms, models


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
        f'{reverse("accounts:account_login")}?template={templatename}'
        if templatename
        else reverse("accounts:account_login")
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
        context = super().get_context_data(**kwargs)
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
            messages.success(
                request,
                _(
                    "Votre compte a été activé avec succès! Vous pouvez maintenant vous connecter à l'aide de vos identifiants."
                ),
            )
        else:
            messages.error(request, _("Une erreur est survenue lors de l'activation"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"social_apps": SocialApp.objects.all()})

        customization = {
            "application_title": config.APPLICATION_TITLE,
            "application_subtitle": config.APPLICATION_SUBTITLE,
            "application_description": config.APPLICATION_DESCRIPTION,
            "general_conditions_url": config.GENERAL_CONDITIONS_URL,
            "privacy_policy_url": config.PRIVACY_POLICY_URL,
            "background_image": None,
        }
        uri = parse.unquote(self.request.build_absolute_uri()).replace("next=/", "")

        params_str = (
            parse.urlsplit(uri).query.replace("?", "").replace(settings.PREFIX_URL, "")
        )

        self.request.session["templatename"] = None
        url_qs = ""

        if "template" in parse.parse_qs(params_str).keys():
            template_value = parse.parse_qs(params_str)["template"][0]
            template = models.TemplateCustomization.objects.filter(
                templatename=template_value
            ).first()
            if template:
                customization = {
                    "application_title": template.application_title
                    if template.application_title
                    else config.APPLICATION_TITLE,
                    "application_subtitle": template.application_subtitle
                    if template.application_subtitle
                    else config.APPLICATION_SUBTITLE,
                    "application_description": template.application_description
                    if template.application_description
                    else config.APPLICATION_DESCRIPTION,
                    "background_image": template.background_image
                    if template.background_image
                    else None,
                }
                self.request.session["templatename"] = template.templatename
                url_qs = "&template=" + template.templatename
            # use anonymous session
            self.request.session["template"] = template_value
        context.update({"customization": customization})
        if "entityfilter" in parse.parse_qs(params_str).keys():
            for value in parse.parse_qs(params_str)["entityfilter"]:
                url_qs += "&entityfilter=" + value

        if "typefilter" in parse.parse_qs(params_str).keys():
            for value in parse.parse_qs(params_str)["typefilter"]:
                url_qs += "&typefilter=" + value
        if url_qs:
            context.update({"query_string": url_qs[1:]})

        return context

    def get_success_url(self):

        qs_dict = parse.parse_qs(self.request.META["QUERY_STRING"])

        url_value = (
            qs_dict["next"][0]
            if "next" in qs_dict
            else reverse("submissions:submission_select_administrative_entity")
        )

        if "next" in qs_dict:
            qs_dict.pop("next")

        return (
            reverse("accounts:profile")
            if settings.ENABLE_2FA and not self.request.user.totpdevice_set.exists()
            else url_value
        )


class ActivateAccountView(View):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = models.User.objects.get(pk=uid)
        except models.User.DoesNotExist:
            user = None

        successful = user and default_token_generator.check_token(user, token)
        if successful:
            user.is_active = True
            user.save()

        return redirect(reverse("accounts:account_login") + f"?success={successful}")


@login_required
def user_profile_edit(request):
    django_user_form = forms.DjangoAuthUserForm(
        request.POST or None, instance=request.user
    )
    # prevent a crash when admin accesses this page
    user_profile_form = None
    if hasattr(request.user, "userprofile"):
        permit_author_instance = get_object_or_404(
            models.UserProfile, pk=request.user.userprofile.pk
        )
        user_profile_form = forms.GenericUserProfileForm(
            request.POST or None, instance=permit_author_instance
        )

    if (
        django_user_form.is_valid()
        and user_profile_form
        and user_profile_form.is_valid()
    ):
        user = django_user_form.save()
        user_profile_form.instance.user = user
        user_profile_form.save()

        return HttpResponseRedirect(reverse("submissions:submissions_list"))

    return render(
        request,
        "accounts/user_profile_edit.html",
        {"user_profile_form": user_profile_form, "django_user_form": django_user_form},
    )


def user_profile_create(request):
    django_user_form = forms.NewDjangoAuthUserForm(request.POST or None)
    user_profile_form = forms.GenericUserProfileForm(request.POST or None)
    is_valid = django_user_form.is_valid() and user_profile_form.is_valid()

    if is_valid:
        new_user = django_user_form.save()
        # email wasn't verified yet, so account isn't active just yet
        new_user.is_active = False
        new_user.save()
        user_profile_form.instance.user = new_user
        user_profile_form.save()

        mail_subject = _("Activer votre compte")
        message = render_to_string(
            "registration/emails/email_confirmation.txt",
            {
                "user": new_user,
                "domain": get_current_site(request).domain,
                "url": reverse(
                    "accounts:activate_account",
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
        return redirect(reverse("accounts:account_login"))

    return render(
        request,
        "accounts/user_profile_edit.html",
        {
            "user_profile_form": user_profile_form,
            "django_user_form": django_user_form,
        },
    )


@login_required
@permanent_user_required
@check_mandatory_2FA
def administrative_entity_file_download(request, path):
    """
    Only allows logged user to download administrative entity files
    """

    mime_type, encoding = mimetypes.guess_type(path)
    storage = PrivateFileSystemStorage()

    try:
        return StreamingHttpResponse(storage.open(path), content_type=mime_type)
    except IOError:
        raise Http404
