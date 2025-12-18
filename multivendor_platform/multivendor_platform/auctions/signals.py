"""
Signals for automatic auction notifications
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AuctionRequest, Bid, AuctionNotification
from products.models import Subcategory


@receiver(post_save, sender=AuctionRequest)
def notify_auction_published(sender, instance, created, **kwargs):
    """Notify sellers when auction is published"""
    # Only notify when status changes to 'active' (not on creation)
    # Check if this is a status change to 'active'
    if instance.status == 'active' and not created:
        # Check if we should notify (avoid duplicate notifications)
        # by checking if notification already exists
        from .models import AuctionNotification
        if AuctionNotification.objects.filter(
            auction=instance,
            notification_type='auction_published'
        ).exists():
            return  # Already notified
        # Get all sellers who have products in this subcategory
        if instance.subcategory:
            from products.models import Product
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # Get sellers with products in this subcategory
            products = Product.objects.filter(
                subcategories=instance.subcategory,
                is_active=True
            ).select_related('vendor')
            
            seller_ids = set(products.values_list('vendor_id', flat=True))
            
            # Create notifications for each seller
            for seller_id in seller_ids:
                try:
                    seller = User.objects.get(id=seller_id)
                    if hasattr(seller, 'profile') and seller.profile.is_seller():
                        AuctionNotification.objects.create(
                            auction=instance,
                            user=seller,
                            notification_type='auction_published',
                            message=f'مناقصه جدید در دسته‌بندی "{instance.subcategory.name}"'
                        )
                except User.DoesNotExist:
                    pass


@receiver(post_save, sender=Bid)
def notify_bid_received(sender, instance, created, **kwargs):
    """Notify buyer when a new bid is received"""
    if created:
        auction = instance.auction
        AuctionNotification.objects.create(
            auction=auction,
            user=auction.buyer,
            notification_type='bid_received',
            message=f'پیشنهاد جدید برای مناقصه #{auction.id}'
        )

