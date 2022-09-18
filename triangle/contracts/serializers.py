from rest_framework.serializers import *
from .models import *
from users.serializers import UserShortSerializer

__all__ = ["SmartContractSerializer", "ModeratorInviteSerializer",
           "SmartContractSerializerFromModeratorInvite",
           "WithdrawalFundsRequestSerializer", "BankInputSerializer"]


class SmartContractSerializer(ModelSerializer):
    first_user = UserShortSerializer(read_only=True, many=False)
    second_user = UserShortSerializer(read_only=True, many=False)
    second_user_id = IntegerField(write_only=True)
    moderator = UserShortSerializer(read_only=True, many=False)

    chat_id = IntegerField(read_only=True)

    class Meta:
        model = SmartContract
        fields = ["id", "first_user", "second_user", "second_user_id",
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
        fields = ["first_user_agree", "second_user_agree", "moderator", "checked"]
        read_only_fields = fields


class WithdrawalFundsRequestSerializer(ModelSerializer):
    class Meta:
        model = WithdrawalFundsRequest
        fields = ['first_user_agree', 'second_user_agree', 'moderator_agree',
                  'first_user_funds', 'second_user_funds', 'moderator_funds',
                  'close_contract']
        read_only_fields = ['first_user_agree', 'second_user_agree', 'moderator_agree']


class BankInputSerializer(Serializer):
    input_coins = IntegerField(write_only=True)

    def save(self, **kwargs):
        user = self.context['request'].user
        contract_id = self.context['view'].kwargs['id']

        contract = SmartContract.objects.get(id=contract_id)

        user.coins -= self.validated_data['input_coins']
        contract.bank += self.validated_data['input_coins']

        user.save()
        contract.save()
