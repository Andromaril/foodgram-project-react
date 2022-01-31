from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_staff)

class IsAuthorAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )
 
    def has_object_permission(self, request, view, obj):

        if request.method == 'GET':
            return True
        if request.method == 'DELETE' or request.method == 'POST':
            if (request.user.is_staff
               or obj.author == request.user):
                return True
            return False
        return True