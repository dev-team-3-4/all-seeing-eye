from __future__ import annotations
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException as RestAPIException
from rest_framework.response import Response

__all__ = ['APIException', 'ExceptionCaster']


class APIException(Exception):
    def __init__(self, detail, code=400):
        self.detail = detail
        self.code = code
    
    def serialize(self):
        return self.detail
    
    def to_response(self) -> Response:
        return Response(data=self.serialize(), status=self.code)


def cast_rest_api_exception(exception):
    return APIException(exception.get_full_details(), exception.status_code)


def cast_validation_error(exception):
    return APIException(exception.error_list, exception.code)


def cast_my_exception(exception):
    return exception


class ExceptionCaster:
    EXCEPTION_CAST = {
        ValidationError: cast_validation_error,
        RestAPIException: cast_rest_api_exception,
        APIException: cast_my_exception,
    }

    @classmethod
    def cast_exception(cls, exception):
        for exception_type, caster in cls.EXCEPTION_CAST.items():
            if issubclass(type(exception), exception_type):
                return caster(exception)
        return None

