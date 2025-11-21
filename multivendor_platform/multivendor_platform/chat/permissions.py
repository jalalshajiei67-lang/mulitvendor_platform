from rest_framework import permissions
from .models import GuestSession


class IsChatParticipant(permissions.BasePermission):
    """
    Permission to check if user is a participant of the chat room or has guest session access
    """
    def has_object_permission(self, request, view, obj):
        # Admin can access all rooms
        if request.user.is_authenticated and request.user.is_staff:
            return True
        
        # Check if authenticated user is a participant
        if request.user.is_authenticated:
            if hasattr(obj, 'participants'):
                return obj.participants.filter(id=request.user.id).exists()
        else:
            # Check guest session access
            guest_session_id = request.query_params.get('guest_session')
            if guest_session_id and hasattr(obj, 'guest_session'):
                try:
                    guest_session = GuestSession.objects.get(session_id=guest_session_id)
                    return obj.guest_session == guest_session
                except GuestSession.DoesNotExist:
                    pass
        
        return False


class IsVendorOrAdmin(permissions.BasePermission):
    """
    Permission to check if user is a vendor or admin
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin has access
        if request.user.is_staff:
            return True
        
        # Check if user is a vendor
        return hasattr(request.user, 'vendor_profile')


class IsAdminUser(permissions.BasePermission):
    """
    Permission to check if user is admin
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

