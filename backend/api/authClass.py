from rest_framework.permissions import BasePermission

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.get('id') and request.user.get('is_authenticated'))