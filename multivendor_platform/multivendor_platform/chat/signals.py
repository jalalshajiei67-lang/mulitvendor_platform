from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import ChatMessage, ChatRoom
from gamification.services import GamificationService

User = get_user_model()


@receiver(post_save, sender=ChatMessage)
def track_vendor_response_time(sender, instance, created, **kwargs):
    """
    Track vendor response time when they reply to a chat message.
    Updates avg_response_minutes in SupplierEngagement.
    """
    if not created:
        return  # Only track new messages
    
    if not instance.sender:
        return  # Skip guest messages
    
    # Check if sender is a vendor
    try:
        vendor_profile = instance.sender.vendor_profile
    except AttributeError:
        return  # User is not a vendor
    
    # Get the room and find the last message from a buyer (non-vendor) before this message
    room = instance.room
    previous_buyer_messages = ChatMessage.objects.filter(
        room=room,
        created_at__lt=instance.created_at
    ).exclude(
        sender=instance.sender  # Exclude vendor's own messages
    ).exclude(
        sender__isnull=True  # Exclude guest messages (we could handle these separately if needed)
    ).order_by('-created_at')
    
    if not previous_buyer_messages.exists():
        return  # No previous buyer message to respond to
    
    # Get the most recent buyer message
    last_buyer_message = previous_buyer_messages.first()
    
    # Check if the last buyer message is from a vendor (could be a conversation between vendors)
    # We only want to track responses to buyers
    if last_buyer_message.sender:
        try:
            # If the sender has a vendor_profile, they're a vendor, skip
            if hasattr(last_buyer_message.sender, 'vendor_profile'):
                return
        except AttributeError:
            pass  # Not a vendor, proceed
    
    # Calculate response time in minutes
    time_diff = instance.created_at - last_buyer_message.created_at
    response_minutes = time_diff.total_seconds() / 60.0
    
    # Update rolling average for vendor's response time
    # Use exponential moving average: new_avg = (old_avg * 0.8) + (new_value * 0.2)
    # This gives more weight to recent responses
    engagement_service = GamificationService(vendor_profile)
    engagement = engagement_service.get_or_create_engagement()
    
    if engagement:
        current_avg = engagement.avg_response_minutes
        if current_avg == 0:
            # First response time, use it directly
            new_avg = response_minutes
        else:
            # Exponential moving average (80% old, 20% new)
            new_avg = (current_avg * 0.8) + (response_minutes * 0.2)
        
        engagement.avg_response_minutes = new_avg
        engagement.save(update_fields=['avg_response_minutes', 'updated_at'])
        
        # Recalculate reputation score since response speed affects it
        engagement_service.compute_reputation_score()
        # Award badges that depend on responsiveness/reputation
        engagement_service.check_and_award_badges()

