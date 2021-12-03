from rest_framework import permissions

from .models import ChatRoom


class CanUpdateChat(permissions.BasePermission):
    def has_object_permission(self, request, _, obj: ChatRoom):
        if request.method in ['PATCH', 'PUT']:
            return obj.users.filter(id=request.user.id).exists()
        return True
