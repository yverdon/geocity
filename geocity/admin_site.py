from django.contrib import messages
from django.contrib.admin import AdminSite, site
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import CommandError, call_command
from django.http import Http404
from django.shortcuts import redirect
from django.urls import re_path, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST


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
                "admin:forms_administrativeentityforadminsite_change",
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
