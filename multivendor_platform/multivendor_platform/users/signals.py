# users/signals.py
import uuid
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError, transaction
from .models import UserProfile, BuyerProfile, VendorProfile, VendorSubscription

logger = logging.getLogger(__name__)


@receiver(post_save, sender=UserProfile)
def create_or_update_role_profiles(sender, instance, created, **kwargs):
    """
    Signal receiver that creates/updates BuyerProfile and VendorProfile
    based on UserProfile role when a UserProfile is saved.
    This ensures profiles are automatically created when a user signs up as a seller.
    """
    # Create buyer profile if user is buyer or both
    if instance.role in ['buyer', 'both']:
        try:
            buyer_profile, buyer_created = BuyerProfile.objects.get_or_create(user=instance.user)
            if buyer_created:
                logger.info(f"Created BuyerProfile for user {instance.user.id} ({instance.user.username})")
        except Exception as e:
            logger.error(f"Failed to create BuyerProfile for user {instance.user.id} ({instance.user.username}): {e}", exc_info=True)
            # Re-raise to ensure the error is not silently ignored
            raise
    
    # Create vendor profile if user is seller or both
    # This is critical - ensures VendorProfile exists for all sellers
    # Business rule: Each user can only have one vendor profile
    if instance.role in ['seller', 'both']:
        try:
            # Use transaction to ensure atomicity
            with transaction.atomic():
                # Check if vendor profile already exists first (enforce one-per-user rule)
                try:
                    vendor_profile = VendorProfile.objects.get(user=instance.user)
                    vendor_created = False
                except VendorProfile.DoesNotExist:
                    # Create new vendor profile only if it doesn't exist
                    vendor_profile = VendorProfile.objects.create(
                        user=instance.user,
                        store_name=_generate_unique_store_name(instance.user.username),
                        description=''
                    )
                    vendor_created = True
                
                # If vendor profile already existed but store_name is empty or default, update it
                if not vendor_created and (not vendor_profile.store_name or vendor_profile.store_name.startswith('فروشگاه_')):
                    # Only update if it's still the default pattern (without UUID)
                    if not vendor_profile.store_name or len(vendor_profile.store_name.split('_')) < 3:
                        # Generate unique store name and handle conflicts
                        new_store_name = _generate_unique_store_name(instance.user.username)
                        max_attempts = 10
                        attempts = 0
                        while VendorProfile.objects.filter(store_name=new_store_name).exclude(user=instance.user).exists() and attempts < max_attempts:
                            new_store_name = _generate_unique_store_name(instance.user.username)
                            attempts += 1
                        
                        if attempts >= max_attempts:
                            logger.warning(f"Could not generate unique store_name for user {instance.user.id} after {max_attempts} attempts")
                        else:
                            vendor_profile.store_name = new_store_name
                            vendor_profile.save(update_fields=['store_name'])

                # Ensure the vendor has a subscription (defaults to free)
                VendorSubscription.for_user(instance.user)
                
                if vendor_created:
                    logger.info(f"Created VendorProfile for user {instance.user.id} ({instance.user.username}) with store_name: {vendor_profile.store_name}")
                    
        except IntegrityError as e:
            # Handle unique constraint violations (e.g., store_name conflict)
            logger.error(f"IntegrityError creating VendorProfile for user {instance.user.id} ({instance.user.username}): {e}", exc_info=True)
            # Try to get existing profile
            try:
                vendor_profile = VendorProfile.objects.get(user=instance.user)
                logger.info(f"VendorProfile already exists for user {instance.user.id}, using existing profile")
            except VendorProfile.DoesNotExist:
                logger.error(f"VendorProfile does not exist and could not be created for user {instance.user.id}")
                raise
        except Exception as e:
            # Log error and re-raise - this is critical for seller functionality
            logger.error(f"Failed to create VendorProfile for user {instance.user.id} ({instance.user.username}): {e}", exc_info=True)
            raise


def _generate_unique_store_name(username):
    """
    Generate a unique store name using UUID to avoid database queries.
    This replaces the while loop approach with a more efficient UUID-based method.
    """
    unique_suffix = uuid.uuid4().hex[:6]
    return f"فروشگاه_{username}_{unique_suffix}"


# Export the function so it can be used in serializers
__all__ = ['create_or_update_role_profiles', '_generate_unique_store_name']

