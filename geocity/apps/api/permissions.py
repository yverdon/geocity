from rest_framework.permissions import BasePermission

from geocity.apps.accounts.users import is_user_trusted


class AllowAllRequesters(BasePermission):
    """
    Allow access to Permit Requesters
    """

    def has_permission(self, request, view):
        return True


class BlockRequesterUserPermission(BasePermission):
    """
    Block access to Permit Requesters (General Public)
    Only superuser or integrators can use these endpoints
    """

    def has_permission(self, request, view):
        is_integrator_admin = request.user.groups.filter(
            permit_department__is_integrator_admin=True
        ).exists()
        return is_integrator_admin or request.user.is_superuser


class BlockRequesterUserWithoutGroup(BasePermission):
    """
    Block untrusted user. User must belong to a group in order to access this endpoint
    """

    def has_permission(self, request, view):
        return is_user_trusted(request.user)
