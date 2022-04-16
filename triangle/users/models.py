from random import sample
import string
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.timezone import now
from django.db.models import *


__all__ = ["User", "EmailConfirmObject"]


CHARS_POOL = string.ascii_lowercase + string.ascii_uppercase + string.digits


def generate_key(length: int, chars_pool=CHARS_POOL):
    return ''.join(sample(chars_pool, length))


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password):
        u = self.create_user(username, email, password)
        u.role = User.ROLES.USER
        u.save()
        return u

    def create_user(self, username, email, password):
        password_validation.validate_password(password)

        u = User(username=username, last_login=now())
        u.set_password(password)
        u.save()
        try:
            EmailConfirmObject(user=u, email=email).save()
        except Exception:
            u.delete()
            raise
        return u


class User(AbstractBaseUser, PermissionsMixin):
    class ROLES:
        USER = 0
        MODERATOR = 1
        ADMIN = 2

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    ONLINE_REQUEST_TIMEOUT = timedelta(minutes=1)

    username = CharField(max_length=20, unique=True)
    email = EmailField(unique=True, null=True)
    created_at = DateTimeField(auto_now_add=True, editable=False)
    profile_photo = ImageField(upload_to='accounts_photos/', null=True, blank=True)
    role = SmallIntegerField(default=ROLES.USER)
    ban_until = DateTimeField(default=now)
    registration_time = DateTimeField(auto_now_add=True)
    bank_card_number = CharField(max_length=16, null=True, blank=True)

    @property
    def is_active(self):
        return self.ban_until <= now() and self.email

    @property
    def is_online(self):
        if self.last_login is None:
            return False
        return now() - self.last_login < self.ONLINE_REQUEST_TIMEOUT

    @property
    def is_staff(self):
        return self.role in (self.ROLES.MODERATOR, self.ROLES.ADMIN)

    @property
    def is_superuser(self):
        return self.role == self.ROLES.ADMIN

    def set_password(self, raw_password):
        if hasattr(self, 'auth_token'):
            self.auth_token.delete()
        super(User, self).set_password(raw_password)

    def __str__(self):
        return self.username

    objects = UserManager()


def generate_key_for_email():
    return generate_key(6, '0123456789')


class EmailConfirmObject(Model):
    LIVE_TIME = timedelta(minutes=5)

    user = ForeignKey('User', on_delete=CASCADE, related_name='email_confirm_objects')
    email = EmailField(unique=True)
    key = CharField(max_length=6, default=generate_key_for_email)
    created_time = DateTimeField(default=now)

    def clean(self):
        if User.objects.filter(email=self.email).exclude(username=self.user.username).exists():
            raise ValidationError("User with this mail already exists.", 403)
        return super(EmailConfirmObject, self).clean()

    def update_key(self):
        self.key = generate_key_for_email()
        self.created_time = now

    def save(self, **kwargs):
        self.full_clean()
        return super(EmailConfirmObject, self).save(**kwargs)


def generate_key_for_password():
    return generate_key(16)


class PasswordResetObject(Model):
    LIVE_TIME = timedelta(minutes=5)

    user = OneToOneField('User', on_delete=CASCADE, related_name='password_reset_obj')
    key = CharField(max_length=6, default=generate_key_for_password)
    created_time = DateTimeField(default=now)

    def update_key(self):
        self.key = generate_key_for_password()
        self.created_time = now


class Contact(Model):
    user_owner = ForeignKey('User', on_delete=CASCADE, related_name='contacts')
    user_subject = ForeignKey('User', on_delete=CASCADE)

    class Meta:
        unique_together = ('user_owner', 'user_subject')
