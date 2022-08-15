from django.http import QueryDict
from rest_framework.response import Response

from bases.views import *
from users.models import User, Contact
from .serializers import *
from .models import *

__all__ = ['ChatViewset', 'ChatView', 'MemberView',
           'MessageViewSet', 'MessageView', 'PerformPrivateChatView',
           'ReadMessageView']


class ReadMessageView(BaseView, UpdateAPIView):
    serializer_class = MessageReadSerializer
    queryset = Message.objects.all()

    def check_put_perms(self, request, obj):
        self.check_anonymous(request)
        if not ChatMember.objects.filter(user=request.user, chat=obj.chat):
            raise APIException("You cannot read this message.", 403)


class ChatViewset(BaseViewSet, CreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        self.check_anonymous(self.request)
        return self.request.user.chats.all()

    def check_post_perms(self, request):
        self.check_anonymous(request)
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data["are_private"] = False

    def post(self, request, *args, **kwargs):
        resp = super(ChatViewset, self).post(request, *args, **kwargs)
        ChatMember.objects.create(user=request.user,
                                  chat_id=resp.data["id"],
                                  role=ChatMember.ROLES.CREATOR)
        return resp


class ChatView(BaseView, RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = FullChatSerializer

    def check_put_perms(self, request, obj):
        chat_member = get_object_or_404(obj.member_objects, user=request.user)
        if obj.are_private:
            raise APIException("Cannot edit a private chat.", 403)
        if chat_member.role not in (ChatMember.ROLES.CREATOR,
                                    ChatMember.ROLES.ADMIN):
            raise APIException("No access to edit the chat.", 403)

    check_delete_perms = check_put_perms


class MemberView(BaseView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = ChatInviteSerializer

    def get_object(self):
        chat = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"])
        obj = get_object_or_404(chat.member_objects, user_id=self.kwargs["user_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def check_post_perms(self, request):
        self.check_anonymous(request)
        chat = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"])
        if chat.are_private:
            APIException("Cannot invite in a private chat.", 403)
        chat_members = chat.members
        if chat_members.filter(id=self.kwargs["user_id"]).first():
            raise APIException("The user already in the chat.")
        if not chat_members.contains(request.user) and request.user.id != self.kwargs["user_id"]:
            raise APIException("You cannot invite user in the chat without you.", 403)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['user_id'] = self.kwargs["user_id"]
        request.data['chat_id'] = self.kwargs["chat_id"]

    def check_put_perms(self, request, obj):
        self.check_anonymous(request)
        chat = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"])
        if chat.are_private:
            APIException("Cannot do this in a private chat.", 403)
        chat_members = chat.member_objects
        user_member = get_object_or_404(chat_members, user=request.user)

        if user_member.role <= obj.role or request.data["role"] >= user_member.role:
            raise APIException("No access.", 403)

    def check_delete_perms(self, request, obj):
        self.check_anonymous(request)
        chat = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"])
        chat_members = chat.member_objects
        user_member = get_object_or_404(chat_members, user=request.user)
        if chat.are_private:
            APIException("Cannot do this in a private chat.", 403)

        if user_member.role <= obj.role and user_member != obj:
            raise APIException("No access.", 403)


class MessageViewSet(BaseViewSet, CreateAPIView):
    serializer_class = MessageSerializer

    def get_chat(self):
        return get_object_or_404(self.request.user.chats, id=self.kwargs["chat_id"])

    def get_queryset(self):
        self.check_anonymous(self.request)
        return self.get_chat().messages.order_by("send_time")

    def check_post_perms(self, request):
        self.check_anonymous(request)
        chat = self.get_chat()
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['author_id'] = request.user.id
        request.data['chat'] = chat.id

    def perform_create(self, serializer):
        serializer.save()
        serializer.instance.chat.last_message = serializer.instance
        serializer.instance.chat.save()


class MessageView(BaseView, UpdateAPIView, DestroyAPIView):
    serializer_class = MessageSerializer

    def check_put_perms(self, request, obj):
        self.check_anonymous(request)
        chat_member = ChatMember.objects.filter(chat=obj.chat, user=request.user).first()
        if chat_member is None:
            raise APIException("You not in the chat.", 403)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data.pop('author_id', None)
        request.data.pop('chat', None)

        if obj.author != request.user:
            for field in ("text", "attachments"):
                if field in request.data:
                    raise APIException("Cannot edit not your messages.", 403)

    def check_delete_perms(self, request, obj):
        self.check_anonymous(request)
        chat_member = ChatMember.objects.filter(chat=obj.chat, user=request.user).first()
        if chat_member is None:
            raise APIException("You not in the chat.", 403)

        if obj.author != request.user:
            raise APIException("Cannot remove not your messages.", 403)

    def perform_destroy(self, instance):
        chat = instance.chat
        instance.delete()
        chat.last_message = chat.messages.ordering("-send_time").first()
        chat.save()


class PerformPrivateChatView(BaseView, CreateAPIView):
    serializer_class = ChatSerializer

    def check_post_perms(self, request):
        self.check_anonymous(request)
        if request.user == self.kwargs["username"]:
            raise APIException("Cannot perform chat with myself.")

    def post(self, request, *args, **kwargs):
        user_first = request.user
        user_second = get_object_or_404(User.objects, username=self.kwargs["username"])

        contact_f_s = Contact.objects.get_or_create(user_owner=user_first, user_subject=user_second)[0]
        contact_s_f = Contact.objects.get_or_create(user_owner=user_second, user_subject=user_first)[0]

        chat = contact_f_s.private_chat or contact_s_f.private_chat
        if chat is None:
            chat = Chat.objects.create(name="Private chat", are_private=True)

        contact_f_s.private_chat_id = chat
        contact_s_f.private_chat_id = chat
        contact_f_s.save()
        contact_s_f.save()

        ChatMember.objects.get_or_create(user=user_first, chat=chat)
        ChatMember.objects.get_or_create(user=user_second, chat=chat)

        return Response(self.get_serializer(instance=chat).data, 200)
