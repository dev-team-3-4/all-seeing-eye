from django.http import QueryDict
from rest_framework.response import Response
from django.db.models import Count

from bases.views import *
from .serializers import *
from .models import *
from chats.models import ChatMember, Chat
from users.models import User

__all__ = ["SmartContractViewSet", "SmartContractView", "InviteModeratorView"]


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


class InviteModeratorView(BaseView, CreateAPIView, UpdateAPIView):
    serializer_class = SmartContractSerializer

    def check_post_perms(self, request):
        self.check_anonymous(request)
        contract = get_object_or_404(SmartContract.objects, id=self.kwargs["contract_id"])
        if request.user.id not in (contract.first_user.id,
                                   contract.second_user.id):
            raise APIException("This is not your smart-contract.", 403)
        if contract.moderator is not None:
            raise APIException("Moderator already invited.", 403)

        for invite in contract.moderator_invites.filter(refused=False).all():
            v = invite.is_agreed()
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
        if not invite.is_agreed():
            raise APIException("Invite are not agreed", 403)

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
        contract = get_object_or_404(SmartContract.objects, id=self.kwargs["contract_id"])
        contract.moderator = request.user
        contract.save()

        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        invite = ModeratorInvite.objects.filter(smart_contract_id=self.kwargs["contract_id"],
                                                moderator_id=request.user.id).order_by("send_time").first()
        invite.refused = True
        invite.save()
        return Response(status=201)
