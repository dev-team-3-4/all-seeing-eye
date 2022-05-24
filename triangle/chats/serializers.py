from rest_framework.serializers import *
from users.serializers import UserShortSerializer
from .models import *

__all__ = ["ChatSerializer", "FullChatSerializer", "ChatMemberSerializer",
           "MessageSerializer", "ChatInviteSerializer"]


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "name", "photo"]
        read_only_fields = ["id"]


class ChatMemberSerializer(ModelSerializer):
    user = UserShortSerializer(many=False)

    class Meta:
        model = ChatMember
        fields = ["user", "role"]
        read_only_fields = ["user"]


class FullChatSerializer(ModelSerializer):
    members = ChatMemberSerializer(many=True)

    class Meta:
        model = Chat
        fields = ["id", "name", "photo", "members"]
        read_only_fields = ["id", "members"]


class MessageSerializer(ModelSerializer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.instance:
            if self.instance.is_banned:
                self.Meta.fields = ["id", "author", "chat_id", "is_banned",
                                    "send_time", "edit_time"]

    author = UserShortSerializer(many=False)

    class Meta:
        model = Message
        fields = ["id", "author", "chat", "is_banned",
                  "text", "attachments", "send_time", "edit_time"]
        read_only_fields = ["id", "send_time", "edit_time"]
        extra_kwargs = {
            "chat": {"write_only": True, "required": True}
        }


class ChatInviteSerializer(Serializer):
    chat_id = IntegerField(write_only=True)
    user_id = IntegerField(write_only=True)
    role = IntegerField(write_only=True, default=ChatMember.ROLES.USER)

    def create(self, validated_data):
        return ChatMember.objects.create(chat_id=validated_data['chat_id'],
                                         user_id=validated_data['user_id'])

    def update(self, instance, validated_data):
        instance.role = validated_data["role"]
        instance.save()
        return instance

