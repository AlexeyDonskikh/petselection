from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.method in SAFE_METHODS or
                request.user.is_superuser or
                request.user == obj.user
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                (request.user.is_staff or request.user.is_admin))


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsMaster(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.master == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated and
                (request.user.is_staff or request.user.is_admin))


class IsStaffOrAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.method in ('PATCH', 'DELETE') and
                request.user.is_authenticated and
                (obj.author == request.user or
                 request.user.is_admin or
                 request.user.is_moderator or
                 request.user.is_staff))

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated
