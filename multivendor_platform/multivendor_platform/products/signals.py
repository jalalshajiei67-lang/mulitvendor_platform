# products/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import ProductUploadRequest
from users.models import UserActivity


@receiver(post_save, sender=ProductUploadRequest)
def log_product_upload_request(sender, instance, created, **kwargs):
    """
    Log product upload request creation to UserActivity for admin monitoring
    """
    if created:
        # Get the supplier's user
        supplier_user = instance.supplier.vendor
        
        # Get ContentType for ProductUploadRequest
        content_type = ContentType.objects.get_for_model(ProductUploadRequest)
        
        # Create UserActivity entry
        UserActivity.objects.create(
            user=supplier_user,
            action='other',  # Using 'other' since we don't have a specific action for this
            description=f'درخواست بارگذاری محصول - وب‌سایت: {instance.website}',
            content_type=content_type,
            object_id=instance.id
        )

