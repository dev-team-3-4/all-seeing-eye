from bases.exceptions import APIException
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import MethodNotAllowed

__all__ = ['BaseRestPermission']


class BaseRestPermission(BasePermission):
    def __init__(self):
        self.message = None
        self.code = None

    def has_object_permission(self, request, view, obj):
        try:
            if request.method == 'GET':
                view.check_get_perms(request, obj)
            elif request.method == 'PUT':
                view.check_put_perms(request, obj)
            elif request.method == 'DELETE':
                view.check_delete_perms(request, obj)
            else:
                raise MethodNotAllowed(request.method)
        except APIException as e:
            self.message = e.detail
            return False
        else:
            return True

    def has_permission(self, request, view):
        try:
            if request.method == 'POST':
                view.check_post_perms(request)
        except APIException as e:
            self.message = e.detail
            return False
        else:
            return True
