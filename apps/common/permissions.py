
from rest_framework.exceptions import PermissionDenied

from apps.common.models import OrganizationMembership


WRITE_ROLES = {
    OrganizationMembership.Role.ADMIN,
    OrganizationMembership.Role.HR,
}


def get_user_membership(user):
    """Return the user's active organization membership."""
    if not user or not user.is_authenticated:
        raise PermissionDenied("Authentication is required.")

    try:
        membership = user.organization_membership
    except OrganizationMembership.DoesNotExist:
        raise PermissionDenied(
            "You do not belong to an organization."
        )

    if not membership.organization.status:
        raise PermissionDenied(
            "Your organization is inactive."
        )

    return membership


def get_user_organization(user):
    """Return the organization the authenticated user belongs to."""
    return get_user_membership(user).organization


def require_write_role(user):
    """Allow only administrators and HR staff to modify records."""
    membership = get_user_membership(user)

    if membership.role not in WRITE_ROLES:
        raise PermissionDenied(
            "You do not have permission to modify these records."
        )

    return membership
