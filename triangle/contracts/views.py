from rest_framework.response import Response

from bases.views import *
from .serializers import *
from .models import *

__all__ = ["SmartContractViewSet", "SmartContractView"]


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
        if request.data["second_user_id"] == request.user.id:
            raise APIException("Cannot create contract with yourself", 400)


class SmartContractView(BaseView, RetrieveAPIView):
    serializer_class = SmartContractSerializer

    def get_queryset(self):
        self.check_anonymous(self.request)
        return get_all_user_contracts(self.request.user).order_by("create_time")

