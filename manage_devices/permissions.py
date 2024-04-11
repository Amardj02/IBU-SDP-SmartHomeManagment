from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class IsOwnerOfDeviceInRoom(permissions.BasePermission):
    message = "You cannot access this device, because it is not in your room"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        if request.user == obj.room.owner:
            return True
        return False
