from django.contrib import admin
from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_private", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "sender", "created_at")
    search_fields = ("content", "sender__username", "room__name")
    list_filter = ("room",) 