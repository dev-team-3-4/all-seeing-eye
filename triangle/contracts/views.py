from django.http import QueryDict
from rest_framework.response import Response
from django.db.models import Count

from bases.views import *
from .serializers import *
from .models import *
from chats.serializers import MessageSerializer
from chats.models import ChatMember, Chat
from users.models import User

__all__ = ["SmartContractViewSet", "SmartContractView", "InviteModeratorView",
           "AgreeRequest", "InviteModeratorViewSet", "WithdrawalFundsRequestView"]


def get_all_user_contracts(user):
    contracts = user.first_contracts.all()
    contracts.union(user.second_contracts.all())
    contracts.union(user.moderator_contracts.all())

    return contracts


class SmartContractViewSet(BaseViewSet, CreateAPIView):
    serializer_class = SmartContractSerializer

    def get_queryset(self):
        self.check_anonymous(self.request)
        return get_all_user_contracts(self.request.user).order_by("create_time")

    def check_post_perms(self, request):
        self.check_anonymous(request)
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data["first_user_id"] = request.user.id

        if request.data["second_user_id"] == request.data["first_user_id"]:
            raise APIException("Cannot create contract with yourself", 400)
        if request.data.get("chat_id"):
            get_object_or_404(ChatMember.objects,
                              chat_id=request.data["chat_id"],
                              user_id=request.data["first_user_id"])
            get_object_or_404(ChatMember.objects,
                              chat_id=request.data["chat_id"],
                              user_id=request.data["second_user_id"])

    def perform_create(self, serializer):
        flag = 'chat_id' not in self.request.data
        chat = None  # IDE requires
        if flag:
            chat = Chat.objects.create(name="New Smart-contract chat")
            ChatMember.objects.create(chat_id=chat.id, role=ChatMember.ROLES.ADMIN,
                                      user_id=serializer.initial_data["first_user_id"])
            ChatMember.objects.create(chat_id=chat.id, role=ChatMember.ROLES.ADMIN,
                                      user_id=serializer.initial_data["second_user_id"])
            serializer._validated_data["chat_id"] = chat.id
        try:
            serializer.save()
        except Exception:
            if flag:
                chat.delete()
            raise


class SmartContractView(BaseView, RetrieveAPIView, DestroyAPIView):
    serializer_class = SmartContractSerializer

    def get_queryset(self):
        self.check_anonymous(self.request)
        return get_all_user_contracts(self.request.user).order_by("create_time")


class InviteModeratorView(BaseView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = ModeratorInviteSerializer

    def check_post_perms(self, request):
        self.check_anonymous(request)
        contract = get_object_or_404(SmartContract.objects, id=self.kwargs["contract_id"])
        if request.user.id not in (contract.first_user.id,
                                   contract.second_user.id):
            raise APIException("This is not your smart-contract.", 403)
        if contract.is_closed:
            raise APIException("Contract are closed.", 403)
        if contract.moderator is not None:
            raise APIException("Moderator already invited.", 403)

        for invite in contract.moderator_invites.filter(refused=False).all():
            v = invite.is_agreed
            if v is None or v:
                raise APIException("There are an active invite.", 403)

        if "user_id" in self.kwargs:
            if self.kwargs["user_id"] in (contract.first_user.id,
                                          contract.second_user.id):
                raise APIException("This user already in smart-contract.", 403)
        else:
            user = User.objects.filter(role=User.ROLES.MODERATOR).\
                exclude(id__in=(contract.first_user.id, contract.second_user.id)).\
                annotate(smc=Count('moderator_contracts')).order_by('smc').first()
            if user is None:
                raise APIException("Sorry, now there are no moderators for your smart-contract. Try again later.", 500)

            self.kwargs["user_id"] = user.id

    def check_put_perms(self, request, obj):
        self.check_anonymous(request)
        invite = ModeratorInvite.objects.filter(smart_contract_id=self.kwargs["contract_id"],
                                                moderator_id=request.user.id).order_by("send_time").first()
        if invite is None:
            raise APIException("You are not invited.", 404)
        if not invite.is_agreed:
            raise APIException("Invite are not agreed", 403)
        if invite.smart_contract.is_closed:
            raise APIException("Contract are closed.", 403)
        invite.checked = True
        invite.save()

    check_delete_perms = check_put_perms

    def post(self, request, *args, **kwargs):
        contract = get_object_or_404(SmartContract.objects, id=self.kwargs["contract_id"])
        ModeratorInvite.objects.create(
            chat_id=contract.chat_id,
            text='Moderator invite.',
            author_id=request.user.id,

            smart_contract=contract,
            moderator_id=self.kwargs["user_id"]
        )
        return Response(status=201)

    def put(self, request, *args, **kwargs):
        self.check_put_perms(request, None)
        contract = get_object_or_404(SmartContract.objects, id=self.kwargs["contract_id"])
        contract.moderator = request.user
        contract.save()

        ChatMember.objects.get_or_create(chat_id=contract.chat_id, user_id=request.user.id)

        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        self.check_delete_perms(request, None)
        return Response(status=201)


class AgreeRequest(BaseView, UpdateAPIView, DestroyAPIView):
    serializer_class = MessageSerializer

    def check_put_perms(self, request, obj):
        self.check_anonymous(request)
        if not obj.chat.members.contains(request.user):
            raise APIException("You is not member of this chat.", 403)
        if hasattr(obj, 'moderatorinvite'):
            proposal = obj.moderatorinvite
        elif hasattr(obj, 'withdrawalfundsrequest'):
            proposal = obj.withdrawalfundsrequest
        else:
            raise APIException("Message is not contains proposal.", 400)

        if request.user not in (proposal.smart_contract.first_user,
                                proposal.smart_contract.second_user,
                                proposal.smart_contract.moderator):
            raise APIException("You is not member of this contract.", 403)

        if proposal.smart_contract.is_closed:
            raise APIException("Contract are closed.", 403)

        if proposal.is_agreed is not None:
            raise APIException("Decision has been made.", 403)

    check_delete_perms = check_put_perms

    def solve_proposal(self, instance, decision):
        if hasattr(instance, 'moderatorinvite'):
            instance = instance.moderatorinvite
        elif hasattr(instance, 'withdrawalfundsrequest'):
            instance = instance.withdrawalfundsrequest

        if self.request.user.id == instance.smart_contract.first_user_id:
            instance.first_user_agree = decision
        elif self.request.user.id == instance.smart_contract.second_user_id:
            instance.second_user_agree = decision
        elif hasattr(instance, 'moderator_agree') and self.request.user.id == instance.smart_contract.moderator_id:
            instance.moderator_agree = decision
        instance.save()

    def perform_destroy(self, instance):
        self.solve_proposal(instance, False)

    def perform_update(self, serializer):
        instance = serializer.instance
        self.solve_proposal(instance, True)


class InviteModeratorViewSet(BaseViewSet):
    serializer_class = SmartContractSerializerFromModeratorInvite

    def get_queryset(self):
        self.check_anonymous(self.request)
        return self.request.user.moderator_invites.filter(checked=False,
                                                          first_user_agree=True,
                                                          second_user_agree=True,
                                                          smart_contract__is_closed=False)


class WithdrawalFundsRequestView(BaseView, CreateAPIView):
    def check_post_perms(self, request):
        self.check_anonymous(request)
        contract = get_object_or_404(SmartContract.objects, id=self.kwargs["contract_id"])

        if request.user not in (contract.first_user, contract.second_user,
                                contract.moderator):
            raise APIException("You is not member of this contract.", 403)

        if contract.is_closed:
            raise APIException("Contract are closed.", 403)

        if contract.moderator is None and request.data.get('moderator_funds', 0):
            raise APIException("There are moderator's fund, but the contract haven't a moderator", 400)
        if request.data.get('first_user_funds', 0) < 0 or \
           request.data.get('second_user_funds', 0) < 0 or \
           request.data.get('moderator_funds', 0) < 0:
            raise APIException("Invalid funds.", 400)

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data["author_id"] = request.user.id
        request.data["chat_id"] = contract.chat_id
