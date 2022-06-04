from rest_framework.serializers import *
from .models import *
from users.serializers import UserShortSerializer

__all__ = ["SmartContractSerializer"]


class SmartContractSerializer(ModelSerializer):
    first_user = UserShortSerializer(read_only=True, many=False)
    first_user_id = IntegerField(write_only=True)

    second_user = UserShortSerializer(read_only=True, many=False)
    second_user_id = IntegerField(write_only=True)

    moderator = UserShortSerializer(read_only=True, many=False)

    chat_id = IntegerField(required=False)

    class Meta:
        model = SmartContract
        fields = ["id", "first_user", "first_user_id", "second_user", "second_user_id",
                  "moderator", "create_time", "chat_id", "is_closed", "bank"]
        read_only_fields = ["id", "create_time", "is_closed", "bank"]
