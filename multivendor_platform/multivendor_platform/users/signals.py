# users/signals.py
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, BuyerProfile, VendorProfile


@receiver(post_save, sender=UserProfile)
def create_or_update_role_profiles(sender, instance, created, **kwargs):
    """
    Signal receiver that creates/updates BuyerProfile and VendorProfile
    based on UserProfile role when a UserProfile is saved.
    """
    # Create buyer profile if user is buyer or both
    if instance.role in ['buyer', 'both']:
        BuyerProfile.objects.get_or_create(user=instance.user)
    
    # Create vendor profile if user is seller or both
    if instance.role in ['seller', 'both']:
        vendor_profile, vendor_created = VendorProfile.objects.get_or_create(
            user=instance.user,
            defaults={
                'store_name': _generate_unique_store_name(instance.user.username),
                'description': ''
            }
        )
        
        # If vendor profile already existed but store_name is empty or default, update it
        if not vendor_created and (not vendor_profile.store_name or vendor_profile.store_name.startswith('فروشگاه_')):
            # Only update if it's still the default pattern
            if vendor_profile.store_name == f"فروشگاه_{instance.user.username}":
                vendor_profile.store_name = _generate_unique_store_name(instance.user.username)
                vendor_profile.save(update_fields=['store_name'])


def _generate_unique_store_name(username):
    """
    Generate a unique store name using UUID to avoid database queries.
    This replaces the while loop approach with a more efficient UUID-based method.
    """
    unique_suffix = uuid.uuid4().hex[:6]
    return f"فروشگاه_{username}_{unique_suffix}"

