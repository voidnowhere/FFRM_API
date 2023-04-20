from rest_framework.permissions import BasePermission

from .models import User


class IsPlayer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == User.PLAYER



class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == User.OWNER
