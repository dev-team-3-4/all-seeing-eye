from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema

from bases.views import *
from .serializers import *

__all__ = ["UserViewSet", "EmailConfirmView"]


class UserViewSet(BaseViewSet, CreateAPIView):
    serializer_class = UserShortSerializer


class EmailConfirmView(BaseView):
    serializer_class = EmailConfirmSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Email address for confirmation",
                    ),
                ),
                coreapi.Field(
                    name="key",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Confirmation Key",
                        description="Confirmation key from received mail",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirm_object = serializer.validated_data['confirm_object']

        user = confirm_object.user
        user.email = confirm_object.email
        for co in user.email_confirm_objects:
            co.delete()
        # TODO serialize user
        return Response(status=200)
