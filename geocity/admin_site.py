from django.conf import settings
from django.contrib import messages
from django.contrib.admin import AdminSite, site
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.management import CommandError, call_command
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.urls import re_path, reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from two_factor.admin import AdminSiteOTPRequired, AdminSiteOTPRequiredMixin

from geocity.apps.permits.admin import PermitsAdminSite


class PermitsAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(site._registry)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r"^create-anonymous-user/$",
                self.create_anonymous_user,
                name="create_anonymous_user",
            ),
            re_path(
                r"^create-knox-token/$",
                self.create_knox_token,
                name="create_knox_token",
            ),
        ]
        return custom_urls + urls

    @method_decorator(staff_member_required)
    @method_decorator(require_POST)
    def create_anonymous_user(self, request):
        """
        Admin custom view to create the anonymous user for the given Administrative
        entity.
        FIXME: Special permission required to do that ?
         Like being an integrator of the given entity ?
        """
        try:
            entity_id = int(request.POST.get("entity_id"))
        except ValueError:
            raise Http404

        try:
            call_command("create_anonymous_users", entity_id)
        except CommandError:
            # Display error
            messages.add_message(
                request,
                messages.ERROR,
                _("Echec de la création de l'utilisateur anonyme."),
            )
        else:
            messages.add_message(
                request, messages.SUCCESS, _("Utilisateur anonyme créé avec succès.")
            )

        return redirect(
            reverse(
                "admin:permits_permitadministrativeentity_change",
                kwargs={"object_id": entity_id},
            )
        )

    @method_decorator(staff_member_required)
    @method_decorator(require_POST)
    def create_knox_token(self, request):
        """
        Admin custom view to create the knox token for the given User
        """
        user_id = int(request.POST.get("user"))
        request_user_id = request.user.id
        try:
            token = call_command("create_knox_token", user_id, request_user_id)
        except CommandError:
            # Display error
            messages.add_message(
                request,
                messages.ERROR,
                _("Echec de la création du knox token."),
            )
        else:
            messages.add_message(
                request,
                messages.SUCCESS,
                _(
                    "Knox token créé avec succès. Veuillez le copier, il ne sera visible qu'une seule fois."
                ),
            )
            messages.add_message(request, messages.INFO, token)

        return redirect(
            reverse(
                "admin:auth_user_change",
                kwargs={"object_id": user_id},
            )
        )


# https://github.com/Bouke/django-two-factor-auth/issues/219#issuecomment-494382380
# Remove when https://github.com/Bouke/django-two-factor-auth/pull/370 is merged
class AdminSiteOTPRequiredMixinRedirSetup(AdminSiteOTPRequired, PermitsAdminSite):
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
