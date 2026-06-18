from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Разрешение только для модераторов"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()


class IsNotModer(permissions.BasePermission):
    """Разрешение для всех, кроме модераторов"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """Разрешение для владельца объекта"""

    def has_object_permission(self, request, view, obj):
        # Проверяем, что пользователь является владельцем объекта
        return obj.owner == request.user


class IsOwnerOrModer(permissions.BasePermission):
    """Разрешение для владельца объекта или модератора"""

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True
        return obj.owner == request.user
