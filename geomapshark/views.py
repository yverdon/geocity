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
        client_id = self.request.POST.get("client_id")
        client_secret = self.request.POST.get("client_secret")
        code = self.request.POST.get("code")
        absolute_uri = self.request.build_absolute_uri('/')

        # Uri used to get token
        suffix_oauth_uri = "oauth/token/"
        suffix_token_uri = "token/"

        # Fix for localhost, docker users 9095->9000/tcp
        if(absolute_uri == "http://localhost:9095/"):
            absolute_uri_localhost = "http://localhost:9000/"
        else:
            absolute_uri_localhost = absolute_uri

        # Fix for prefix_url
        if settings.PREFIX_URL:
            endpoint_uri = absolute_uri_localhost + settings.PREFIX_URL + suffix_oauth_uri
            redirect_uri = absolute_uri + settings.PREFIX_URL + suffix_token_uri
        else:
            endpoint_uri = absolute_uri_localhost + suffix_oauth_uri
            redirect_uri = absolute_uri + suffix_token_uri

        print(redirect_uri)
        
        if client_secret and code:
            endpoint = endpoint_uri
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
            }

            request = requests.post(endpoint, data=data, headers=headers)
            return HttpResponse(request)

            # url = reverse("oauth2_provider:token", data=data, headers=headers)
            # return HttpResponseRedirect(url)
            # c = {'access_token': 'bar'}
            # return HttpResponse(render(c, "oauth2/oauth2_token.html"), content_type='application/x-www-form-urlencoded')
            # return HttpResponseRedirect(reverse("oauth2_token", args={"access_token": "abcd"}))
            # return render (request, "oauth2/oauth2_token.html")
        else:
            return HttpResponseRedirect("../oauth/authorize/?response_type=code&client_id=" + client_id)

    def get_context_data(self, **kwargs):
        context = super(OAuth2TokenView, self).get_context_data(**kwargs)
        context.update({
            "code": self.request.GET.get("code"),
            "access_token": self.request.GET.get("access_token"),
            "expires_in": self.request.GET.get("expires_in"),
            "token_type": self.request.GET.get("token_type"),
            "scope": self.request.GET.get("scope"),
            "refresh_token": self.request.GET.get("refresh_token"),
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
