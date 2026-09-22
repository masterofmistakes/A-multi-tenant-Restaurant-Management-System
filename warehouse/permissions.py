from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import UserRole

class CanManageWH(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == UserRole.SKLADCHIK
        )