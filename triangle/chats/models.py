from django.db.models import *
from django.contrib.postgres.fields import ArrayField

__all__ = ['Chat', 'ChatMember', 'Message']


class Chat(Model):
    name = CharField(max_length=32)
    photo = ImageField(upload_to='chats_photos/', null=True, blank=True)
    members = ManyToManyField('users.User', 'chats', through='ChatMember')
    last_message = ForeignKey("Message", on_delete=SET_NULL, null=True, related_name='chats_in_which_is_last')

    are_private = BooleanField(default=False)


class ChatMember(Model):
    class ROLES:
        USER = 0
        MODERATOR = 1
        ADMIN = 2
        CREATOR = 3

    chat = ForeignKey(Chat, on_delete=CASCADE, related_name="member_objects")
    user = ForeignKey('users.User', on_delete=CASCADE, related_name="chat_objects")
    role = SmallIntegerField(default=ROLES.USER)
    last_checked_message = ForeignKey("Message", on_delete=SET_NULL, null=True, default=None)

    class Meta:
        unique_together = ('chat', 'user')

    def delete(self, using=None, keep_parents=False):
        role = self.role
        chat = self.chat
        super(ChatMember, self).delete(using, keep_parents)
        if not chat.members.exists() or role == self.ROLES.CREATOR:
            chat.delete()


class Message(Model):
    author = ForeignKey('users.User', on_delete=CASCADE, related_name="messages")
    chat = ForeignKey(Chat, on_delete=CASCADE, related_name="messages")
    text = CharField(max_length=512, blank=True, default="")
    attachments = ArrayField(FileField(upload_to="message_attachments/"), 10, default=list, blank=True)
    send_time = DateTimeField(auto_now_add=True)
    edit_time = DateTimeField(auto_now=True)

    def delete(self, using=None, keep_parents=False):
        chat = self.chat
        super(Message, self).delete(using, keep_parents)
        chat.last_message = chat.messages.order_by("-send_time").first()
        chat.save()

