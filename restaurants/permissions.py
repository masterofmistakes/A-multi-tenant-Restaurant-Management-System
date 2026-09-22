from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import UserRole
class IsSuperAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)        

class IsAdminOrStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not (request.user and request.user.is_authenticated):
            return False

        return bool(
            request.user.role == UserRole.ADMIN or 
            (request.user.role == UserRole.WAITER and request.method == 'PATCH')
        )