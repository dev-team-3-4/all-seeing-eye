from rest_framework.authentication import TokenAuthentication as parentToken
from django.utils.timezone import now

__all__ = ['TokenAuthentication']


class TokenAuthentication (parentToken):
    def authenticate_credentials(self, key):
        user, token = super(TokenAuthentication, self).authenticate_credentials(key)
        if user and user.is_authenticated:
            user.last_login = now()
            user.save()

        return user, token
