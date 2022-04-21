from rest_framework.serializers import *
from .models import *
from bases.tasks import send_mail


__all__ = ['UserShortSerializer']


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

    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "password", "profile_photo"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {"write_only": True, "required": True},
            "password": {"write_only": True, "required": True}
        }
