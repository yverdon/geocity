from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication
from rest_framework import exceptions

from permits.services_authentication import check_request_ip_is_allowed


class InternalTokenAuthentication(TokenAuthentication):
    """Knox TokenAuthentication, but only usable for requests coming from a whitelisted IP range"""

    def authenticate(self, request):
        # TODO: move check_request_ip_is_allowed implemention here (it shouldn't be useful elsewhere)
        if not check_request_ip_is_allowed(request):
            msg = _("Token authentication is only accepted for internal calls.")
            raise exceptions.AuthenticationFailed(msg)

        return super().authenticate(request)
