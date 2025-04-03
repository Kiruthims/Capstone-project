from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsTaskOwner(BasePermission):
    """
    Custom permission to allow only task owners to edit or delete their own tasks.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
