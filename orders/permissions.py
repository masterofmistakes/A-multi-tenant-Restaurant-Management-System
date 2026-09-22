from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import UserRole

class IsWaiterOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user.is_authenticated and 
            request.user.role == UserRole.WAITER
        )

class IsChefPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == UserRole.CHEF
        