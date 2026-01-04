from django import template
from django.db.models import Count
from products.models import Product, ProductUploadRequest

register = template.Library()

@register.simple_tag
def pending_products_count():
    """Return the count of products pending approval"""
    return Product.objects.filter(approval_status=Product.APPROVAL_STATUS_PENDING).count()

@register.simple_tag
def pending_product_upload_requests_count():
    """Return the count of product upload requests pending review"""
    return ProductUploadRequest.objects.filter(status='pending').count()
