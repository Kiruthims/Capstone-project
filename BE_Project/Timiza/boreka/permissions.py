from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """Allow full access to superusers."""
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsTaskOwner(BasePermission):
    """Allow users to modify only their own tasks."""

    def has_permission(self, request, view):
        # Prevent users who are not staff from performing PUT/DELETE actions
        if request.method in ['PUT', 'DELETE']:
            if not request.user.is_staff:  # Check for staff status
                return False
        return True

    def has_object_permission(self, request, view, obj):
        # Ensure users can only modify their own tasks (GET/POST allowed)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.user != request.user:
                return False
        return obj.user == request.user



class IsAdminUser(BasePermission):
    """Allow admin users to view and modify their tasks."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Checks if user is an admin
