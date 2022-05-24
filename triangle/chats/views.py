from django.http import QueryDict

from bases.views import *
from .serializers import *
from .models import *

__all__ = ['ChatViewset', 'ChatView', 'MemberView',
           'MessageViewSet', 'MessageView']


class ChatViewset(BaseViewSet, CreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        self.check_anonymous(self.request)
        return self.request.user.chats

    def check_post_perms(self, request):
        self.check_anonymous(request)

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
        if chat_member.role not in (ChatMember.ROLES.CREATOR,
                                    ChatMember.ROLES.ADMIN):
            raise APIException("No access to edit the chat.", 403)

    check_delete_perms = check_put_perms


class MemberView(BaseView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = ChatInviteSerializer

    def get_object(self):
        chat = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"])
        return get_object_or_404(chat.member_objects, user_id=self.kwargs["user_id"])

    def check_post_perms(self, request):
        self.check_anonymous(request)
        chat_members = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"]).members
        if chat_members.filter(id=self.kwargs["user_id"]).first():
            raise APIException("The user already in the chat.")
        if request.user not in chat_members and request.user.id != self.kwargs["user_id"]:
            raise APIException("You cannot invite user in the chat without you.", 403)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['user_id'] = self.kwargs["user_id"]
        request.data['chat_id'] = self.kwargs["chat_id"]

    def check_put_perms(self, request, obj):
        self.check_anonymous(request)
        chat_members = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"]).member_objects
        user_member = get_object_or_404(chat_members, user=request.user)

        if user_member.role <= obj.role or request.data["role"] >= user_member.role:
            raise APIException("No access.", 403)

    def check_delete_perms(self, request, obj):
        self.check_anonymous(request)
        chat_members = get_object_or_404(Chat.objects, id=self.kwargs["chat_id"]).member_objects
        user_member = get_object_or_404(chat_members, user=request.user)

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
        request.data['author'] = request.user
        request.data['chat'] = chat
        request.data['is_banned'] = False


class MessageView(BaseView, UpdateAPIView, DestroyAPIView):
    serializer_class = MessageSerializer

    def check_put_perms(self, request, obj):
        self.check_anonymous(request)
        chat_member = ChatMember.objects.filter(chat=obj.chat, user=request.user).first()
        if chat_member is None:
            raise APIException("You not in the chat.", 403)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data.pop('author', None)
        request.data.pop('chat', None)

        if 'is_banned' in request.data and chat_member.role < ChatMember.ROLES.MODERATOR:
            raise APIException("Cannot ban messages in this chat.", 403)

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
