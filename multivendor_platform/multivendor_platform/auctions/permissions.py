from rest_framework import permissions
from .models import ReverseAuction, AuctionInvitation


class IsBuyerOrReadOnly(permissions.BasePermission):
    """
    Only buyers can create auctions.
    Others can only read.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions require authentication
        if not request.user.is_authenticated:
            return False
        
        # Check if user is a buyer
        try:
            profile = request.user.profile
            is_buyer = profile.is_buyer()
            return is_buyer
        except Exception as e:
            return False


class IsInvitedSupplier(permissions.BasePermission):
    """
    Only invited suppliers can place bids.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user is a supplier
        try:
            profile = request.user.profile
            if not profile.is_seller():
                return False
        except:
            return False
        
        # For bid placement, check invitation in has_object_permission
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Check if supplier is invited to this auction.
        """
        if not request.user.is_authenticated:
            return False
        
        # Check if user is invited
        return AuctionInvitation.objects.filter(
            auction=obj,
            supplier=request.user
        ).exists()


class IsAuctionOwner(permissions.BasePermission):
    """
    Only auction creator (buyer) can award or cancel auction.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Only buyer (owner) can perform these actions
        return obj.buyer == request.user


class IsAuctionOwnerOrInvitedSupplier(permissions.BasePermission):
    """
    Auction owner (buyer) or invited supplier can view auction details.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Owner can always view
        if obj.buyer == request.user:
            return True
        
        # Check if user is invited supplier
        return AuctionInvitation.objects.filter(
            auction=obj,
            supplier=request.user
        ).exists()

