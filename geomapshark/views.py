from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import View

if settings.ENABLE_2FA:
    from two_factor.views import LoginView
else:
    from django.contrib.auth.views import LoginView

from django.http import HttpResponseRedirect, HttpResponse
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
                "domain": "geocity.docker.test",  # get_current_site(request).domain,
                "url": reverse("activate_account", kwargs={
                    # we need the user id to validate the token
                    "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                    "token": PasswordResetTokenGenerator().make_token(new_user),
                }),
                "signature": _("L'équipe de Geocity"),
            },
        )

        email = EmailMessage(mail_subject, message, to=[new_user.email])
        email.send()
        return HttpResponse(
            "Please confirm your email address to complete the registration"
        )

        # permits_services.store_tags_in_session(request)
        # if settings.ENABLE_2FA:
        #     return HttpResponseRedirect(
        #         reverse("two_factor:profile")
        #         + (
        #             "?" + request.META["QUERY_STRING"]
        #             if request.META["QUERY_STRING"]
        #             else ""
        #         )
        #     )
        # return HttpResponseRedirect(
        #     reverse("permits:permit_request_select_administrative_entity")
        #     + (
        #         "?" + request.META["QUERY_STRING"]
        #         if request.META["QUERY_STRING"]
        #         else ""
        #     )
        # )

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
