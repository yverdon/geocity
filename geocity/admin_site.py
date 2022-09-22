from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.http import is_safe_url
from two_factor.admin import AdminSiteOTPRequired, AdminSiteOTPRequiredMixin

from geocity.apps.permits import models
from geocity.apps.permits.admin import PermitsAdminSite


# https://github.com/Bouke/django-two-factor-auth/issues/219#issuecomment-494382380
# Remove when https://github.com/Bouke/django-two-factor-auth/pull/370 is merged
class AdminSiteOTPRequiredMixinRedirSetup(AdminSiteOTPRequired, PermitsAdminSite):
    def has_permission(self, request):
        if (
            models.PermitDepartment.objects.filter(
                group__in=request.user.groups.all(), mandatory_2fa=True
            )
            .exclude(duo_client_id__exact="")
            .exclude(duo_client_secret__exact="")
            .exclude(duo_host__exact="")
            .exists()
        ):
            return True
        elif not super().has_permission(request):
            return False

        return super().has_permission(request)

    def login(self, request, extra_context=None):
        redirect_to = request.POST.get(
            REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME)
        )

        if request.method == "GET" and super(
            AdminSiteOTPRequiredMixin, self
        ).has_permission(request):
            # Already logged-in and verified by OTP
            if request.user.is_verified():
                # User has permission
                index_path = reverse("admin:index", current_app=self.name)
            else:
                # User has permission but no OTP set:
                index_path = reverse("two_factor:setup", current_app=self.name)
            return HttpResponseRedirect(index_path)

        if not redirect_to or not is_safe_url(
            url=redirect_to, allowed_hosts=[request.get_host()]
        ):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return redirect_to_login(redirect_to)
