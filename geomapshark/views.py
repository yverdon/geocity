from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from permits import forms, models
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def redirect_permit(request):
    response = redirect(reverse('permits:permit_requests_list'))
    return response


class CustomPasswordResetView(PasswordResetView):

    extra_email_context = {'custom_host': ''}

    def get_context_data(self, **kwargs):
        context = super(CustomPasswordResetView, self).get_context_data(**kwargs)
        domain = 'https://' + self.request.build_absolute_uri().split('//')[1].split('/')[0]
        self.extra_email_context['custom_host'] = domain
        self.extra_email_context['site_name'] = self.request.build_absolute_uri().split('/')[2]
        return context


def permit_author_create(request):

    djangouserform = forms.NewDjangoAuthUserForm(request.POST or None)
    permitauthorform = forms.GenericAuthorForm(request.POST or None)

    if djangouserform.is_valid() and permitauthorform.is_valid():

        new_user = djangouserform.save()
        permitauthorform.instance.user = new_user
        permitauthorform.save()

        login(request, new_user)

        return HttpResponseRedirect(
            reverse('permits:permit_requests_list'))

    return render(request, "permits/permit_request_author.html", {'permitauthorform': permitauthorform, 'djangouserform': djangouserform})


@login_required
def permit_author_edit(request):

    djangouserform = forms.DjangoAuthUserForm(request.POST or None, instance=request.user)
    permit_author_instance = get_object_or_404(models.PermitAuthor, pk=request.user.permitauthor.pk)
    permitauthorform = forms.GenericAuthorForm(request.POST or None, instance=permit_author_instance)

    if djangouserform.is_valid() and permitauthorform.is_valid():

        user = djangouserform.save()
        permitauthorform.instance.user = user
        permitauthorform.save()

        return HttpResponseRedirect(
            reverse('permits:permit_requests_list'))

    return render(request, "permits/permit_request_author.html", {'permitauthorform': permitauthorform, 'djangouserform': djangouserform})
