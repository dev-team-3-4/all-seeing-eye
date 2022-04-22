from rest_framework.serializers import *
from .models import *
from bases.tasks import send_mail
from bases.views import get_object_or_none


__all__ = ['UserShortSerializer', 'EmailConfirmSerializer']


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


class EmailConfirmSerializer(Serializer):
    email = CharField(
        label="email",
        write_only=True
    )
    key = CharField(
        label="confirmation key",
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        key = attrs.get('key')

        if email and key:
            confirm_object = get_object_or_none(EmailConfirmObject.objects, email=email, key=key)

            if not confirm_object:
                msg = 'Email confirm request is not found or wrong confirmation key.'
                raise ValidationError(msg, code=403)
        else:
            msg = 'Must include "username" and "password".'
            raise ValidationError(msg)

        attrs['confirm_object'] = confirm_object
        return attrs
