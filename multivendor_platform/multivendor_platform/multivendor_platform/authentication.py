"""
Custom authentication classes for Django REST Framework
"""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication that doesn't enforce CSRF validation.
    Use this for API endpoints that should work without CSRF tokens.
    """
    def enforce_csrf(self, request):
        return  # Do not enforce CSRF for this authentication class







