from rest_framework import permissions

from accounts.models import UserAPIKey


class HasValidAPIKey(permissions.BasePermission):
    """
    Allows access only to users with valid API key.
    """
    def has_permission(self, request, view):
        api_key_header = request.headers.get('Api-Key')
        if api_key_header:
            try:
                UserAPIKey.objects.get(hashed_key=api_key_header)
                return True
            except UserAPIKey.DoesNotExist:
                return False
        return False