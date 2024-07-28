
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with role 'admin'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'
