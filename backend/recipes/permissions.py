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


class IsAuthorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )
 
    def has_object_permission(self, request, view, obj):

        if request.method == 'GET':
            return True
        if request.method == 'DELETE' or request.method == 'PATCH' or request.method == 'POST':
            if (request.user.is_staff
               or obj.author == request.user):
                return True
            return False
        return True
 


