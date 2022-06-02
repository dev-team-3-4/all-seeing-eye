from django.db.models import *
from django.contrib.postgres.fields import ArrayField

__all__ = ['Chat', 'ChatMember', 'Message']


class Chat(Model):
    name = CharField(max_length=32)
    photo = ImageField(upload_to='chats_photos/', null=True, blank=True)
    members = ManyToManyField('users.User', 'chats', through='ChatMember')

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
    is_banned = BooleanField(default=False)
    text = CharField(max_length=512, blank=True, default="")
    attachments = ArrayField(FileField(upload_to="message_attachments/"), 10, default=list, blank=True)
    send_time = DateTimeField(auto_now_add=True)
    edit_time = DateTimeField(auto_now=True)

