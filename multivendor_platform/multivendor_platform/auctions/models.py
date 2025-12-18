from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from products.models import Product, Subcategory
import uuid

User = get_user_model()


class AuctionRequest(models.Model):
    """Main auction request model"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('abandoned', 'Abandoned'),
    ]
    
    REQUEST_TYPE_CHOICES = [
        ('free', 'Free Request'),
        ('verified', 'Verified Request (Paid Deposit)'),
    ]
    
    DEPOSIT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('held_in_escrow', 'Held in Escrow'),
        ('forfeited', 'Forfeited'),
        ('refunded', 'Refunded'),
    ]
    
    AUCTION_STYLE_CHOICES = [
        ('sealed', 'Sealed Bid'),
        ('live_reverse', 'Live Reverse Auction'),
    ]
    
    # Basic Information
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_requests')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='auction_requests', help_text="Starting point product")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, 
                                    related_name='auction_requests', help_text="For feature templates")
    
    # Status and Type
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, default='free')
    
    # Deposit Information
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=0, default=5000000, 
                                        help_text="Deposit amount in Toman")
    deposit_status = models.CharField(max_length=20, choices=DEPOSIT_STATUS_CHOICES, default='unpaid')
    deposit_payment = models.ForeignKey('AuctionDepositPayment', on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='auction_request')
    
    # Auction Configuration
    auction_style = models.CharField(max_length=20, choices=AUCTION_STYLE_CHOICES, default='sealed')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Content
    description = models.TextField(help_text="Buyer's need explanation")
    technical_specs = models.JSONField(default=dict, blank=True, 
                                       help_text="Filled from SubcategoryFeatureTemplate")
    
    # Admin Fields
    admin_notes = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='reviewed_auctions')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Winner
    winner = models.ForeignKey('Bid', on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='won_auctions')
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Auction Request'
        verbose_name_plural = 'Auction Requests'
        indexes = [
            models.Index(fields=['buyer', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['subcategory', 'status']),
        ]
    
    def __str__(self):
        return f"Auction #{self.id} - {self.buyer.username} - {self.get_status_display()}"
    
    def is_verified(self):
        """Check if this is a verified request with deposit"""
        return self.request_type == 'verified' and self.deposit_status in ['paid', 'held_in_escrow']
    
    def can_close_early(self):
        """Check if buyer can close auction early"""
        if self.auction_style == 'sealed':
            return True
        elif self.auction_style == 'live_reverse':
            if self.end_time:
                time_remaining = self.end_time - timezone.now()
                return time_remaining.total_seconds() > 3600  # More than 1 hour remaining
        return False


class AuctionPhoto(models.Model):
    """Photos attached to auction requests"""
    
    auction = models.ForeignKey(AuctionRequest, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='auction_photos/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Auction Photo'
        verbose_name_plural = 'Auction Photos'
    
    def __str__(self):
        return f"Photo for Auction #{self.auction.id}"


class AuctionDocument(models.Model):
    """Documents attached to verified auction requests"""
    
    auction = models.ForeignKey(AuctionRequest, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='auction_documents/%Y/%m/')
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Auction Document'
        verbose_name_plural = 'Auction Documents'
    
    def __str__(self):
        return f"{self.file_name} - Auction #{self.auction.id}"


class Bid(models.Model):
    """Bids submitted by sellers"""
    
    auction = models.ForeignKey(AuctionRequest, on_delete=models.CASCADE, related_name='bids')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    technical_compliance = models.JSONField(default=dict, 
                                           help_text="Filled from SubcategoryFeatureTemplate")
    additional_notes = models.TextField(blank=True, null=True)
    is_winner = models.BooleanField(default=False)
    rank = models.IntegerField(null=True, blank=True, help_text="Final ranking in auction")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price', 'created_at']
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'
        indexes = [
            models.Index(fields=['auction', 'price']),
            models.Index(fields=['seller', '-created_at']),
        ]
        unique_together = [['auction', 'seller']]  # One bid per seller per auction
    
    def __str__(self):
        return f"Bid #{self.id} - {self.seller.username} - {self.price} for Auction #{self.auction.id}"


class AuctionDepositPayment(models.Model):
    """Payment model for auction deposits via Zibal"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('forfeited', 'Forfeited'),
    ]
    
    auction = models.OneToOneField(AuctionRequest, on_delete=models.CASCADE, related_name='deposit_payment_detail')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_deposit_payments')
    amount = models.DecimalField(max_digits=12, decimal_places=0, default=5000000, 
                                help_text="Amount in Toman")
    
    # Zibal tracking
    track_id = models.CharField(max_length=100, unique=True, db_index=True, 
                               help_text="Zibal track ID")
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, 
                               help_text="Internal order ID")
    ref_number = models.CharField(max_length=100, blank=True, null=True, 
                                 help_text="Zibal reference number")
    card_number = models.CharField(max_length=20, blank=True, null=True, 
                                   help_text="Masked card number")
    
    # Payment status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='zibal', 
                                      help_text="Payment gateway used")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    description = models.TextField(blank=True, null=True)
    zibal_response = models.JSONField(blank=True, null=True, help_text="Full response from Zibal")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Auction Deposit Payment'
        verbose_name_plural = 'Auction Deposit Payments'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"Deposit Payment - Auction #{self.auction.id} - {self.status}"
    
    def mark_as_paid(self, ref_number=None, card_number=None):
        """Mark payment as paid"""
        self.status = 'paid'
        self.paid_at = timezone.now()
        if ref_number:
            self.ref_number = ref_number
        if card_number:
            self.card_number = card_number
        self.save(update_fields=['status', 'paid_at', 'ref_number', 'card_number'])
    
    def mark_as_verified(self):
        """Mark payment as verified"""
        self.status = 'verified'
        self.verified_at = timezone.now()
        self.save(update_fields=['status', 'verified_at'])
        
        # Update auction deposit status
        self.auction.deposit_status = 'held_in_escrow'
        self.auction.deposit_payment = self
        self.auction.save(update_fields=['deposit_status', 'deposit_payment'])
    
    def mark_as_failed(self):
        """Mark payment as failed"""
        self.status = 'failed'
        self.save(update_fields=['status'])


class AuctionReport(models.Model):
    """Admin-written report for completed auctions"""
    
    auction = models.OneToOneField(AuctionRequest, on_delete=models.CASCADE, related_name='report')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auction_reports')
    report_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Auction Report'
        verbose_name_plural = 'Auction Reports'
    
    def __str__(self):
        return f"Report for Auction #{self.auction.id}"


class AuctionNotification(models.Model):
    """Notifications for auction events"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('auction_published', 'Auction Published'),
        ('bid_received', 'Bid Received'),
        ('auction_closed', 'Auction Closed'),
        ('deposit_forfeiture_warning', 'Deposit Forfeiture Warning'),
        ('deposit_forfeited', 'Deposit Forfeited'),
        ('auction_approved', 'Auction Approved'),
        ('auction_rejected', 'Auction Rejected'),
    ]
    
    auction = models.ForeignKey(AuctionRequest, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Auction Notification'
        verbose_name_plural = 'Auction Notifications'
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
            models.Index(fields=['auction', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"
