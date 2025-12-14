# users/signals.py
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, BuyerProfile, VendorProfile, VendorSubscription


@receiver(post_save, sender=UserProfile)
def create_or_update_role_profiles(sender, instance, created, **kwargs):
    """
    Signal receiver that creates/updates BuyerProfile and VendorProfile
    based on UserProfile role when a UserProfile is saved.
    This ensures profiles are automatically created when a user signs up as a seller.
    """
    # Create buyer profile if user is buyer or both
    if instance.role in ['buyer', 'both']:
        BuyerProfile.objects.get_or_create(user=instance.user)
    
    # Create vendor profile if user is seller or both
    # This is critical - ensures VendorProfile exists for all sellers
    if instance.role in ['seller', 'both']:
        try:
            vendor_profile, vendor_created = VendorProfile.objects.get_or_create(
                user=instance.user,
                defaults={
                    'store_name': _generate_unique_store_name(instance.user.username),
                    'description': ''
                }
            )
            
            # If vendor profile already existed but store_name is empty or default, update it
            if not vendor_created and (not vendor_profile.store_name or vendor_profile.store_name.startswith('فروشگاه_')):
                # Only update if it's still the default pattern (without UUID)
                if not vendor_profile.store_name or len(vendor_profile.store_name.split('_')) < 3:
                    vendor_profile.store_name = _generate_unique_store_name(instance.user.username)
                    vendor_profile.save(update_fields=['store_name'])

            # Ensure the vendor has a subscription (defaults to free)
            VendorSubscription.for_user(instance.user)
        except Exception as e:
            # Log error but don't fail silently - this is critical for seller functionality
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create VendorProfile for user {instance.user.id}: {e}")


def _generate_unique_store_name(username):
    """
    Generate a unique store name using UUID to avoid database queries.
    This replaces the while loop approach with a more efficient UUID-based method.
    """
    unique_suffix = uuid.uuid4().hex[:6]
    return f"فروشگاه_{username}_{unique_suffix}"

