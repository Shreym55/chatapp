from django.db.models import Q
from rest_framework import viewsets, mixins, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from .permissions import IsAdminOrReadOnly, IsRoomParticipant


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().prefetch_related("participants")
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["is_private"]
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        room = self.get_object()
        room.participants.add(request.user)
        return Response({"detail": "Joined room."})
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def leave(self, request, pk=None):
        room = self.get_object()
        room.participants.remove(request.user)
        return Response({"detail": "Left room."})


class MessageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated & IsRoomParticipant]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["content", "sender__username"]
    filterset_fields = ["room"]
    def get_queryset(self):
        qs = Message.objects.select_related("room", "sender")
        room_id = self.request.query_params.get("room")
        if room_id:
            qs = qs.filter(room_id=room_id)
        return qs
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        q = request.query_params.get("q", "")
        room_id = request.query_params.get("room")
        qs = self.get_queryset()
        if q:
            qs = qs.filter(Q(content__icontains=q) | Q(sender__username__icontains=q))
        if room_id:
            qs = qs.filter(room_id=room_id)
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)