from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Room, Message

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "avatar", "status"]


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )
    class Meta:
        model = Room
        fields = ["id", "name", "is_private", "participants", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ["id", "room", "sender", "content", "file", "created_at"]
        read_only_fields = ["sender", "created_at"]
    def validate(self, attrs):
        if not attrs.get("content") and not attrs.get("file"):
            raise serializers.ValidationError("Either content or file is required.")
        return attrs
    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data) 