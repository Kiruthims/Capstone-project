from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:  # Hugo and allow others since their perm allow
            return False
        return obj.user == request.user  
