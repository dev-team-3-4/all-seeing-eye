from django.core.files.storage import default_storage
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import *
from users.serializers import UserShortSerializer
from .models import *
from contracts.serializers import ModeratorInviteSerializer, WithdrawalFundsRequestSerializer

__all__ = ["ChatSerializer", "FullChatSerializer", "ChatMemberSerializer",
           "MessageSerializer", "ChatInviteSerializer", "MessageReadSerializer"]


class MessageReadSerializer(Serializer):
    new_messages = BooleanField(read_only=True)

    def save(self, **kwargs):
        request = self.context.get('request')
        chat = self.instance
        message = chat.last_message
        if message is None:
            self._data = {'new_messages': False}
            return

        chat_member = ChatMember.objects.filter(user=request.user, chat=chat).first()
        if not chat_member.last_checked_message or message.send_time > chat_member.last_checked_message.send_time:
            chat_member.last_checked_message = message
            chat_member.save()
        self._data = {'new_messages': chat_member.last_checked_message == chat_member.chat.last_message}


class MessageSerializer(ModelSerializer):
    author = UserShortSerializer(many=False, read_only=True)

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

        if hasattr(instance, 'moderatorinvite'):
            ret.pop('text', None)
            ret.pop('attachments', None)
            ret['moderator_invite'] = ModeratorInviteSerializer(instance=instance.moderatorinvite).data
        elif hasattr(instance, 'withdrawalfundsrequest'):
            ret.pop('text', None)
            ret.pop('attachments', None)
            ret['withdrawal_request'] = WithdrawalFundsRequestSerializer(instance=instance.withdrawalfundsrequest).data
        return ret

    class Meta:
        model = Message
        fields = ["id", "author",
                  "text", "attachments", "send_time", "edit_time"]
        read_only_fields = ["id", "send_time", "edit_time", "author"]


class ChatSerializer(ModelSerializer):
    last_message = MessageSerializer(read_only=True, required=False)

    class Meta:
        model = Chat
        fields = ["id", "name", "photo", "are_private", "last_message"]
        read_only_fields = ["id", "are_private", "last_message"]

    def to_representation(self, instance: Chat):
        ret = super(ChatSerializer, self).to_representation(instance)
        request = self.context.get('request')
        if instance.are_private:
            other_user = instance.members.exclude(id=request.user.id).first()
            ret['name'] = other_user.username
            if other_user.profile_photo:
                ret['photo'] = request.build_absolute_uri(other_user.profile_photo.url)
            else:
                ret['photo'] = None
        member = request.user.chat_objects.filter(chat_id=instance.id).first()
        ret['new_messages'] = instance.last_message is not None and member.last_checked_message != instance.last_message
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
        fields = ["id", "name", "photo", "member_objects", "are_private", "last_message"]
        read_only_fields = ["id", "member_objects", "are_private", "last_message"]


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
