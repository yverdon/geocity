from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView


def redirect_permit(request):
    response = redirect('/permit-request')
    return response


class CustomPasswordResetView(PasswordResetView):

    extra_email_context = {'custom_host': ''}

    def get_context_data(self, **kwargs):
        context = super(CustomPasswordResetView, self).get_context_data(**kwargs)
        domain = 'https://' + self.request.build_absolute_uri().split('//')[1].split('/')[0]
        self.extra_email_context['custom_host'] = domain
        self.extra_email_context['site_name'] = self.request.build_absolute_uri().split('/')[2]
        return context
