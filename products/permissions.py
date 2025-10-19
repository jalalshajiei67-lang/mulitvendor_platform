# multivendor_platform/products/permissions.py

from rest_framework import permissions

class IsVendorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow vendors to edit their own products.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the vendor of the product.
        # obj.vendor is the user who created the product.
        # request.user is the user making the current request.
        return obj.vendor == request.user