import socket
import ipaddress

from constance import config


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


def check_request_comes_from_internal_qgisserver(request):
    """
    Check that the request is coming from inside the docker composition AND that it is an allowed ip
    """
    # TODO: deduplicate with services.check_request_comes_from_internal_qgisserver
    if (
        check_request_ip_is_allowed(request)
        and socket.gethostbyname("qgis") == request.META["REMOTE_ADDR"]
    ):
        return True
    return False
