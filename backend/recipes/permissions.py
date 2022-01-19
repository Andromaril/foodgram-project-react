from rest_framework import permissions

ADMIN_METHODS = ('PATCH', 'DELETE')
SAFE_METHODS = ('GET', 'POST')


class AdminOrReadonly(permissions.BasePermission):

    message = "User not admin"

    def has_permission(self, request, view):

        if (
            request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_staff):
            return True
        return False
