from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Category


class ReverseAuction(models.Model):
    """Main reverse auction entity"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('awarded', 'Awarded'),
        ('cancelled', 'Cancelled'),
    )
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_auctions')
    title = models.CharField(max_length=200, help_text="Auction title/name")
    description = models.TextField(help_text="Detailed description of what is being requested")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='auctions')
    starting_price = models.DecimalField(max_digits=20, decimal_places=2, help_text="Maximum price (ceiling)")
    reserve_price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Hidden minimum price below which contract is guaranteed"
    )
    deadline = models.DateTimeField(help_text="When the auction closes")
    minimum_decrement = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=0,
        help_text="Minimum amount by which a bid must be lower than previous"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    winner = models.ForeignKey('Bid', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')
    extended_count = models.PositiveIntegerField(default=0, help_text="Number of times deadline was extended")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Reverse Auction"
        verbose_name_plural = "Reverse Auctions"
        indexes = [
            models.Index(fields=['status', 'deadline']),
            models.Index(fields=['buyer', '-created_at']),
            models.Index(fields=['category', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def is_active(self):
        """Check if auction is currently active"""
        if self.status != 'active':
            return False
        return timezone.now() < self.deadline
    
    def time_remaining(self):
        """Calculate time remaining until deadline"""
        if not self.is_active():
            return None
        return self.deadline - timezone.now()
    
    def should_extend(self):
        """Check if auction should be extended (bid in last 5 minutes)"""
        if not self.is_active():
            return False
        if self.extended_count >= 3:  # Max 3 extensions to prevent infinite loops
            return False
        time_remaining = self.time_remaining()
        if time_remaining and time_remaining.total_seconds() <= 300:  # 5 minutes
            return True
        return False
    
    def extend_deadline(self):
        """Extend deadline by 5 minutes"""
        if self.should_extend():
            self.deadline = self.deadline + timedelta(minutes=5)
            self.extended_count += 1
            self.save(update_fields=['deadline', 'extended_count'])
            return True
        return False


class AuctionInvitation(models.Model):
    """Track invited suppliers for an auction"""
    auction = models.ForeignKey(ReverseAuction, on_delete=models.CASCADE, related_name='invitations')
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_invitations')
    invited_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('auction', 'supplier')
        verbose_name = "Auction Invitation"
        verbose_name_plural = "Auction Invitations"
        indexes = [
            models.Index(fields=['supplier', '-invited_at']),
            models.Index(fields=['auction', 'supplier']),
        ]
    
    def __str__(self):
        return f"{self.supplier.username} invited to {self.auction.title}"
    
    def mark_viewed(self):
        """Mark invitation as viewed"""
        if not self.viewed_at:
            self.viewed_at = timezone.now()
            self.save(update_fields=['viewed_at'])


class Bid(models.Model):
    """Supplier bid on an auction"""
    auction = models.ForeignKey(ReverseAuction, on_delete=models.CASCADE, related_name='bids')
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_bids')
    amount = models.DecimalField(max_digits=20, decimal_places=2, help_text="Bid amount")
    rank = models.PositiveIntegerField(null=True, blank=True, help_text="Current rank (1st, 2nd, 3rd, etc.)")
    is_winning = models.BooleanField(default=False, help_text="True if this is currently the lowest bid")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['amount', 'created_at']  # Lowest amount first
        verbose_name = "Bid"
        verbose_name_plural = "Bids"
        indexes = [
            models.Index(fields=['auction', 'amount']),
            models.Index(fields=['supplier', '-created_at']),
            models.Index(fields=['auction', 'supplier']),
        ]
        # One active bid per supplier per auction (suppliers can update their bid)
        unique_together = ('auction', 'supplier')
    
    def __str__(self):
        return f"{self.supplier.username} - {self.amount} on {self.auction.title}"
    
    def calculate_rank(self):
        """Calculate this bid's rank among all bids for the auction"""
        # Get all bids for this auction, ordered by amount (lowest first)
        all_bids = Bid.objects.filter(auction=self.auction).order_by('amount', 'created_at')
        rank = 1
        for bid in all_bids:
            if bid.id == self.id:
                return rank
            rank += 1
        return None
    
    def is_better_than_previous(self):
        """Check if this bid is better (lower) than supplier's previous bid"""
        previous_bid = Bid.objects.filter(
            auction=self.auction,
            supplier=self.supplier
        ).exclude(id=self.id).order_by('-created_at').first()
        
        if not previous_bid:
            # First bid - must be less than starting price
            return self.amount < self.auction.starting_price
        
        # Must be lower than previous bid
        return self.amount < previous_bid.amount

