from rest_framework.permissions import BasePermission


class IsFieldOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.type.owner == request.user
