from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponseRedirect, request
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView

from permits import forms, models
import requests


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

class OAuth2TokenView(TemplateView):
    template_name = "oauth2/oauth2_token.html"
    
    def post(self, *args, **kwargs):
        # Values from form
        client_id = self.request.POST.get("client_id")
        client_secret = self.request.POST.get("client_secret")
        code = self.request.POST.get("code")
        refresh_token = self.request.POST.get("refresh_token")

        # Uri used to get token
        absolute_uri = self.request.build_absolute_uri('/')
        suffix_oauth_uri = "oauth/token/"
        suffix_token_uri = "token/"

        # Fix absolute_uri in case we are working on localhost. Docker uses 9095->9000/tcp
        if(absolute_uri == "http://localhost:9095/"):
            absolute_uri_localhost = "http://localhost:9000/"
        else:
            absolute_uri_localhost = absolute_uri

        # Fix endpoint_uri and redirect_uri in case we need a prefix_url
        if settings.PREFIX_URL:
            endpoint_uri = absolute_uri_localhost + settings.PREFIX_URL + suffix_oauth_uri
            redirect_uri = absolute_uri + settings.PREFIX_URL + suffix_token_uri
        else:
            endpoint_uri = absolute_uri_localhost + suffix_oauth_uri
            redirect_uri = absolute_uri + suffix_token_uri

        # Header and data for requests
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

        data_create_token = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        data_refresh_token = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        
        # "code" is used on token creation and "refresh_token" is user on the rfresh token
        if code:
            request = requests.post(endpoint_uri, data=data_create_token, headers=header)
            return HttpResponse(request)
        elif refresh_token:
            request = requests.post(endpoint_uri, data=data_refresh_token, headers=header)
            return HttpResponse(request)
        else:
            return HttpResponseRedirect("../oauth/authorize/?response_type=code&client_id=" + client_id)

    # TODO: "access_token" to "refresh_token" are commented, cause we use "return HttpResponse(request)" on the post. Improve this and return to oauth2_token.html and show the values from the json
    # TODO: Uncomment "<h4>Création du token, étape 3</h4>" in "oauth2_token.html" to show the values when the json will be returned to our route
    # Get the values on the request
    def get_context_data(self, **kwargs):
        context = super(OAuth2TokenView, self).get_context_data(**kwargs)
        context.update({
            "code": self.request.GET.get("code"),
            # "access_token": self.request.GET.get("access_token"),
            # "expires_in": self.request.GET.get("expires_in"),
            # "token_type": self.request.GET.get("token_type"),
            # "scope": self.request.GET.get("scope"),
            # "refresh_token": self.request.GET.get("refresh_token"),
        })
        return context


def permit_author_create(request):
    djangouserform = forms.NewDjangoAuthUserForm(request.POST or None)
    permitauthorform = forms.GenericAuthorForm(request.POST or None)
    is_valid = djangouserform.is_valid() and permitauthorform.is_valid()

    if is_valid:
        new_user = djangouserform.save()
        permitauthorform.instance.user = new_user
        permitauthorform.save()

        login(request, new_user)
        if settings.ENABLE_2FA:
            return HttpResponseRedirect(reverse("two_factor:profile"))
        return HttpResponseRedirect(reverse("permits:permit_requests_list"))

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
    # prvent a crash when admin accesses this page
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
