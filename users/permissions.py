from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class NotModerator(permissions.BasePermission):
    """Проверяет, не является ли пользователь модератором."""

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    """Доступ разрешён только владельцу объекта."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
