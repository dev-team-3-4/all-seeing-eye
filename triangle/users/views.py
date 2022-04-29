from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema

from bases.views import *
from .models import User
from .serializers import *

__all__ = ["UserViewSet", "EmailConfirmView",
           "PasswordResetView", "ChangePasswordView", "UserView"]


class UserViewSet(BaseViewSet, CreateAPIView):
    serializer_class = UserShortSerializer


class UserView(BaseView, RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    lookup_field = 'username'
    serializer_class = UserSerializer

    def check_put_perms(self, request, obj):
        if request.user != obj:
            raise APIException('Access denied', 403)

    def check_delete_perms(self, request, obj):
        if request.user != obj:
            raise APIException('Access denied', 403)
        # TODO check haven't active smart contracts


class EmailConfirmView(BaseView):
    serializer_class = EmailConfirmSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=False,
                    location='form',
                    schema=coreschema.String(
                        title="Username"
                    ),
                ),
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
                    required=False,
                    location='form',
                    schema=coreschema.String(
                        title="Confirmation Key",
                        description="Confirmation key from received mail",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.dict())
        serializer.is_valid(raise_exception=True)
        return Response(status=200)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.dict())
        serializer.is_valid(raise_exception=True)
        confirm_object = serializer.validated_data['confirm_object']

        user = confirm_object.user
        user.email = confirm_object.email
        for co in user.email_confirm_objects.all():
            co.delete()
        user.save()
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=200)


class PasswordResetView(BaseView):
    serializer_class = PasswordResetSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="key",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Confirmation Key",
                        description="Confirmation key from received mail",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="New password",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.dict() | kwargs)
        serializer.is_valid(raise_exception=True)
        return Response(status=200)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.dict() | kwargs)
        serializer.is_valid(raise_exception=True)
        reset_obj = serializer.validated_data['reset_obj']

        user = reset_obj.user
        user.set_password(serializer.validated_data['password'])
        user.save()
        reset_obj.delete()
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=200)


class ChangePasswordView(BaseView, UpdateAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="old_password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Old password",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="New password",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def check_put_perms(self, request, obj):
        if request.user != obj:
            raise APIException('Access denied', 403)
