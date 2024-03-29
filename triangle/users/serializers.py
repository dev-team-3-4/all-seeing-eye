from django.contrib.auth import password_validation
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.serializers import *

from bases.exceptions import APIException
from .models import *
from bases.tasks import send_mail
from bases.views import get_object_or_none, get_object_or_404


__all__ = ['UserShortSerializer', 'EmailConfirmSerializer',
           'PasswordResetSerializer', 'ChangePasswordSerializer',
           'UserSerializer', 'ContactSerializer', 'UserFullSerializer']


class UserShortSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        try:
            conf_obj = user.email_confirm_objects.first()
            send_mail("Triangle Confirm mail",
                      f"Code is {conf_obj.key}",
                      [conf_obj.email])
        except Exception:
            user.delete()
            raise

        return user

    def update(self, instance, validated_data):
        email = validated_data.pop('email')

        instance = super(UserShortSerializer, self).update(instance, validated_data)

        if email:
            conf_obj = EmailConfirmObject.objects.create(user=instance, email=email)
            try:
                send_mail("Triangle Confirm mail",
                          f"Code is {conf_obj.key}",
                          [conf_obj.email])
            except Exception:
                conf_obj.delete()
                raise

        return instance

    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "password", "profile_photo"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {"write_only": True, "required": True},
            "password": {"write_only": True, "required": True}
        }


class UserSerializer(ModelSerializer):
    in_contacts = BooleanField(read_only=True, allow_null=True, default=False)

    class Meta:
        model = User
        fields = ["id", "username", "profile_photo", "registration_time", "is_online", "in_contacts"]
        read_only_fields = fields

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        request = self.context.get('request')
        if request is None:
            return ret
        if request.user.is_authenticated:
            ret['in_contacts'] = request.user.contain_in_contacts(instance)
        else:
            ret.pop('in_contacts')
        return ret


class UserFullSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "profile_photo", "email", "registration_time",
                  "ban_until", "is_online", "coins"]
        read_only_fields = ["id", "registration_time", "is_online", "coins", "email", "ban_until"]


class EmailConfirmSerializer(Serializer):
    username = CharField(
        label="username",
        write_only=True,
        required=False
    )
    email = CharField(
        label="email",
        write_only=True,
        required=True
    )
    key = CharField(
        label="confirmation key",
        write_only=True,
        required=False
    )

    def validate(self, attrs):
        method = self.context.get('request').method
        username = attrs.get('username')
        email = attrs.get('email')
        key = attrs.get('key')

        if method == "PUT":
            if email and username:
                user = get_object_or_404(User.objects, username=username)
                if self.context.get('request').user != user:
                    raise APIException('Access denied', 403)
                confirm_object, created = EmailConfirmObject.objects.get_or_create(email=email, user=user)
                if not created:
                    confirm_object.update_key()
                    confirm_object.save()

                try:
                    send_mail("Triangle Confirm mail",
                              f"Code is {confirm_object.key}",
                              [confirm_object.email])
                except Exception:
                    confirm_object.delete()
                    raise
                attrs['confirm_object'] = confirm_object
            else:
                raise ValidationError('Must include "email" and "username".', 400)
        elif method == "POST":
            if email and key:
                confirm_object = get_object_or_none(EmailConfirmObject.objects, email=email, key=key)

                if not confirm_object:
                    msg = 'Email confirm request is not found or wrong confirmation key.'
                    raise ValidationError(msg, code=403)
            else:
                raise ValidationError('Must include "email" and "key".', 400)

            attrs['confirm_object'] = confirm_object
        else:
            raise MethodNotAllowed(method)

        return attrs


class PasswordResetSerializer(Serializer):
    username = CharField(
        label="username",
        write_only=True,
        required=True
    )
    key = CharField(
        label="confirmation key",
        write_only=True,
        required=False
    )
    password = CharField(
        label="password",
        write_only=True,
        required=False
    )

    def validate(self, attrs):
        request = self.context.get('request')

        username = attrs.get('username')
        key = attrs.get('key')
        password = attrs.get('password')

        if request.method == 'GET':
            # create reset password request
            if username:
                user = get_object_or_404(User.objects, username=username)
                if user.email is None:
                    raise ValidationError("User must have confirmed mail.", 403)

                reset_obj, created = PasswordResetObject.objects.get_or_create(user=user)
                if not created:
                    reset_obj.update_key()
                    reset_obj.save()

                try:
                    send_mail("Reset Password",
                              f"{request.META['HTTP_HOST']}/web/{username}/reset/{reset_obj.key}",
                              [user.email])
                except Exception:
                    reset_obj.delete()
                    raise

                attrs['reset_obj'] = reset_obj
            else:
                raise ValidationError('Must include "username".', 400)

        elif request.method == 'POST':
            # do reset password
            if username and key and password:
                reset_obj = PasswordResetObject.objects.filter(user__username=username,
                                                               key=key).first()
                if not reset_obj:
                    msg = 'Password reset request is not found or wrong confirmation key.'
                    raise ValidationError(msg, code=403)
                password_validation.validate_password(password)

                attrs['reset_obj'] = reset_obj

            else:
                raise ValidationError('Must include "username", "key" and "password".', 400)

        else:
            raise MethodNotAllowed(request.method)

        return attrs


class ChangePasswordSerializer(Serializer):
    old_password = CharField(
        label="old password",
        write_only=True,
        required=True
    )
    password = CharField(
        label="password",
        write_only=True,
        required=True
    )
    token = CharField(
        label="new auth token",
        read_only=True
    )

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')

        if old_password and password:
            if not self.instance.check_password(old_password):
                raise ValidationError('Wrong old password.', 403)
            password_validation.validate_password(password)
        else:
            raise ValidationError('Must include "old_password" and "password".', 400)

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        token = Token.objects.get_or_create(user=instance)[0]
        self._data = {'token': token.key}

        return instance


class ContactSerializer(ModelSerializer):
    user_subject = UserShortSerializer(many=False, required=False, read_only=True)
    user_subject_id = IntegerField(write_only=True, required=True)

    class Meta:
        model = Contact
        fields = ["user_subject", "user_subject_id", "user_owner"]
        read_only_fields = ["user_subject"]
        extra_kwargs = {
            "user_owner": {"write_only": True, "required": True}
        }

    def to_representation(self, instance):
        return super(ContactSerializer, self).to_representation(instance)['user_subject']
