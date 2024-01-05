import ipaddress

from constance import config
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication
from rest_framework import exceptions

# Todo: Use name to get route path instead of hardcoding
api_public_routes = ["events", "current_user", "agenda"]


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def check_request_ip_is_allowed(request):
    """
    Check that the request is coming from allowed ip
    """
    # Check for exact ip
    client_ip = get_client_ip(request)
    if config.IP_WHITELIST != "":
        for whitelisted_ip in config.IP_WHITELIST.split(","):
            if client_ip in whitelisted_ip:
                return True
    # Check for network
    if config.NETWORK_WHITELIST != "":
        for whitelisted_network in config.NETWORK_WHITELIST.split(","):
            ip_address = ipaddress.ip_address(client_ip)
            ip_network = ipaddress.ip_network(whitelisted_network)
            if ip_address in ip_network:
                return True

    return False


def check_is_public_route(request):
    # Resolve request
    resolved_match = resolve(request.path)

    # Url_name correspond to route_name
    url_name = resolved_match.url_name

    # If route should be public and is in the request, return true.
    # Example : api_public_routes = ["events", "current_user", "agenda"]
    # url_name = agenda # Will return True
    # url_name = submission # Will return False
    return any(route in url_name for route in api_public_routes)


class InternalTokenAuthentication(TokenAuthentication):
    """Knox TokenAuthentication, but only usable for requests coming from a whitelisted IP range"""

    def authenticate(self, request):
        if not (check_request_ip_is_allowed(request) or check_is_public_route(request)):
            msg = _("Token authentication is only accepted for internal calls.")
            raise exceptions.AuthenticationFailed(msg)

        return super().authenticate(request)
