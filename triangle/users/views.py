from bases.views import *
from .serializers import *

__all__ = ["UserViewSet"]


class UserViewSet(BaseViewSet, CreateAPIView):
    serializer_class = UserShortSerializer

