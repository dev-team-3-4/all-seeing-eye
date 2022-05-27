from rest_framework.serializers import *
from users.serializers import UserShortSerializer
from .models import *
from django.core.files.storage import default_storage

__all__ = ["ChatSerializer", "FullChatSerializer", "ChatMemberSerializer",
           "MessageSerializer", "ChatInviteSerializer"]


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "name", "photo"]
        read_only_fields = ["id"]

    def to_representation(self, instance: Chat):
        ret = super(ChatSerializer, self).to_representation(instance)
        if instance.are_private:
            request = self.context.get('request')
            other_user = instance.members.exclude(id=request.user.id).first()
            ret['name'] = other_user.username
            if other_user.profile_photo:
                ret['photo'] = other_user.profile_photo.url
            else:
                ret['photo'] = None
        return ret


class ChatMemberSerializer(ModelSerializer):
    user = UserShortSerializer(many=False)

    class Meta:
        model = ChatMember
        fields = ["user", "role"]
        read_only_fields = ["user"]


class FullChatSerializer(ChatSerializer):
    member_objects = ChatMemberSerializer(many=True)

    class Meta:
        model = Chat
        fields = ["id", "name", "photo", "member_objects"]
        read_only_fields = ["id", "member_objects"]


class MessageSerializer(ModelSerializer):
    author = UserShortSerializer(many=False, required=False)
    author_id = IntegerField(write_only=True, required=True)

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        attachments = validated_data.get('attachments', None)
        if attachments:
            for file in attachments:
                file._name = default_storage.save("message_attachments/" + file.name, file)
        return super(MessageSerializer, self).save(**validated_data)

    def to_representation(self, instance):
        new_attachments = list()
        for file in instance.attachments:
            if not hasattr(file, 'name'):
                file_name = file
                file = default_storage.open(file)
                file.name = file_name

            file.url = default_storage.url(file.name)
            new_attachments.append(file)
        if new_attachments:
            instance.attachments = new_attachments

        ret = super(MessageSerializer, self).to_representation(instance)
        if instance.is_banned:
            ret.pop('text', None)
            ret.pop('attachments', None)
        return ret

    class Meta:
        model = Message
        fields = ["id", "author", "author_id", "chat", "is_banned",
                  "text", "attachments", "send_time", "edit_time"]
        read_only_fields = ["id", "send_time", "edit_time", "author"]
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
        if validated_data["role"] not in ChatMember.ROLES:
            raise ValidationError("Unknown role id.", 400)

        instance.role = validated_data["role"]
        instance.save()
        return instance
