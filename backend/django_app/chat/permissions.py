from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Room


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsRoomParticipant(BasePermission):
    
    def has_permission(self, request, view):
        room_id = request.query_params.get("room") or request.data.get("room")
        if request.user and request.user.is_staff:
            return True
        if not room_id:
            return False
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return False
        return room.participants.filter(pk=request.user.pk).exists() 