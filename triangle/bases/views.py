from django.conf import settings
from django.http import Http404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import (GenericAPIView, ListAPIView, CreateAPIView,
                                     DestroyAPIView, RetrieveAPIView, get_object_or_404)
from rest_framework.views import set_rollback
from rest_framework.serializers import ModelSerializer
from bases.exceptions import *
from bases.pagination import BasePagination
from .permissions import BaseRestPermission

__all__ = ["BaseViewSet", "BaseView", "CreateAPIView", "UpdateAPIView", "RetrieveAPIView",
           "DestroyAPIView", "get_object_or_404", "get_object_or_none", "APIException"]


def get_object_or_none(queryset, *filter_args, **filter_kwargs):
    try:
        return get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except Http404:
        return None


def _exception_handler(exception: Exception):
    set_rollback()
    error = ExceptionCaster.cast_exception(exception)

    if error is None:
        error = APIException(detail=exception.__class__.__name__)

    return error.to_response()


class BaseView(GenericAPIView):
    lookup_field = 'id'
    permission_classes = [BaseRestPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if issubclass(self.serializer_class, ModelSerializer):
            self.queryset = self.serializer_class.Meta.model.objects.all()

    def handle_exception(self, exception):
        if not settings.DEBUG:
            return _exception_handler(exception)
        raise exception

    @staticmethod
    def check_anonymous(request):
        if request.user.is_anonymous:
            raise APIException("Anonymous cannot do this")

    def check_get_perms(self, request, obj):
        pass

    def check_post_perms(self, request):
        pass

    def check_put_perms(self, request, obj):
        pass

    def check_delete_perms(self, request, obj):
        pass


class BaseViewSet(ListAPIView, BaseView):
    pagination_class = BasePagination


class UpdateAPIView(UpdateModelMixin, GenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, partial=True, **kwargs)
