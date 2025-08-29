from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name="chat_rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="chat_files/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]
    def __str__(self):
        preview = (self.content or ":paperclip: file").strip().replace("\n", " ")
        return f"{self.sender} @ {self.room}: {preview[:30]}"