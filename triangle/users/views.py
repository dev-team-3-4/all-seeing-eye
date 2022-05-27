from django.http import QueryDict
from rest_framework.response import Response

from bases.views import *
from .models import User
from .serializers import *

__all__ = ["UserViewSet", "EmailConfirmView",
           "PasswordResetView", "ChangePasswordView", "UserView",
           "UserContactViewSet", "UserContactView"]


class UserViewSet(BaseViewSet, CreateAPIView):
    serializer_class = UserShortSerializer

    def filter_queryset(self, queryset):
        if "username" in self.request.query_params:
            username = self.request.query_params.get("username")
            return queryset.filter(username__iregex=f".*{username}.*")
        return queryset


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

    def put(self, request, *args, **kwargs):
        if hasattr(request.data, 'dict'):
            serializer = self.get_serializer(data=request.data.dict())
        else:
            serializer = self.get_serializer(data=request.data | kwargs)
        serializer.is_valid(raise_exception=True)
        return Response(status=200)

    def post(self, request, *args, **kwargs):
        if hasattr(request.data, 'dict'):
            serializer = self.get_serializer(data=request.data.dict())
        else:
            serializer = self.get_serializer(data=request.data | kwargs)
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

    def get(self, request, *args, **kwargs):
        if hasattr(request.data, 'dict'):
            serializer = self.get_serializer(data=request.data.dict())
        else:
            serializer = self.get_serializer(data=request.data | kwargs)
        serializer.is_valid(raise_exception=True)
        return Response(status=200)

    def post(self, request, *args, **kwargs):
        if hasattr(request.data, 'dict'):
            serializer = self.get_serializer(data=request.data.dict())
        else:
            serializer = self.get_serializer(data=request.data | kwargs)
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

    def check_put_perms(self, request, obj):
        if request.user != obj:
            raise APIException('Access denied', 403)


class UserContactViewSet(BaseViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        self.check_anonymous(self.request)
        return self.request.user.contact_objects.filter(deleted=False)


class UserContactView(BaseView, CreateAPIView, DestroyAPIView):
    lookup_url_kwarg = "username"
    lookup_field = 'user_subject__username'
    serializer_class = ContactSerializer

    def get_queryset(self):
        return self.request.user.contact_objects.filter(deleted=False)

    def check_post_perms(self, request):
        self.check_anonymous(request)
        if request.user.username == self.kwargs["username"]:
            raise APIException("Cannot create contact with myself.")

        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data["user_subject_id"] = get_object_or_404(User.objects, username=self.kwargs["username"]).id
        request.data["user_owner"] = request.user.id

    def check_delete_perms(self, request, obj):
        self.check_anonymous(request)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
