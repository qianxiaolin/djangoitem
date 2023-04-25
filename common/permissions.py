from rest_framework import permissions

class MyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        else:
            return False
