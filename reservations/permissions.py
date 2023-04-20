from rest_framework.permissions import BasePermission

from users.models import User


class IsReservationOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
