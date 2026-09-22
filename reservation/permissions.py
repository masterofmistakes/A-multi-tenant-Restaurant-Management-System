from rest_framework.permissions import BasePermission
from accounts.models import UserRole

class WhoAreYou(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in {UserRole.ADMIN, UserRole.WAITER, UserRole.CLIENT})