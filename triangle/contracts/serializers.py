from rest_framework.serializers import *
from .models import *
from users.serializers import UserShortSerializer

__all__ = ["SmartContractSerializer", "ModeratorInviteSerializer",
           "SmartContractSerializerFromModeratorInvite",
           "WithdrawalFundsRequestSerializer"]


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


class SmartContractSerializerFromModeratorInvite(ModelSerializer):
    smart_contract = SmartContractSerializer(read_only=True)

    class Meta:
        model = ModeratorInvite
        fields = ["smart_contract"]

    def to_representation(self, instance):
        ret = super(SmartContractSerializerFromModeratorInvite, self).to_representation(instance)
        return ret['smart_contract']


class ModeratorInviteSerializer(ModelSerializer):
    moderator = UserShortSerializer(read_only=True, many=False)

    class Meta:
        model = ModeratorInvite
        fields = ["first_user_agree", "second_user_agree", "moderator", "refused"]
        read_only_field = fields


class WithdrawalFundsRequestSerializer(ModelSerializer):
    author_id = IntegerField(write_only=True)
    chat_id = IntegerField(write_only=True)

    class Meta:
        model = WithdrawalFundsRequest
        fields = ['first_user_agree', 'second_user_agree', 'moderator_agree',
                  'first_user_funds', 'second_user_funds', 'moderator_funds',
                  'close_contract', 'author_id', 'chat_id']
        read_only_fields = ['first_user_agree', 'second_user_agree', 'moderator_agree']
