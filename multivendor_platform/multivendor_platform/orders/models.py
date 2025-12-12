from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category

LEAD_SOURCE_CHOICES = (
    ('phone', 'Phone'),
    ('whatsapp', 'WhatsApp'),
    ('instagram', 'Instagram'),
)

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    )
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True, help_text="User who created the order (null for anonymous RFQ)")
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total amount (null for RFQ, supports large values)")
    shipping_address = models.TextField(blank=True, null=True, help_text="Shipping address (not required for RFQ)")
    shipping_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Shipping phone (not required for RFQ)")
    notes = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    
    # RFQ (Request for Quotation) fields
    is_rfq = models.BooleanField(default=False, help_text="True if this is a Request for Quotation")
    is_free = models.BooleanField(default=False, help_text="True if this RFQ/lead is free and visible to all sellers")
    first_name = models.CharField(max_length=100, blank=True, null=True, help_text="Buyer first name (for RFQ)")
    last_name = models.CharField(max_length=100, blank=True, null=True, help_text="Buyer last name (for RFQ)")
    company_name = models.CharField(max_length=200, blank=True, null=True, help_text="Company name (for RFQ)")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number (for RFQ)")
    email = models.EmailField(blank=True, null=True, help_text="Email address (for RFQ)")
    unique_needs = models.TextField(blank=True, null=True, help_text="Buyer's unique requirements/needs (for RFQ)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='rfq_orders', help_text="Category for RFQ (if submitted from category page)")
    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES, blank=True, null=True, help_text="Source of the lead (phone, whatsapp, instagram)")
    suppliers = models.ManyToManyField('users.Supplier', related_name='rfqs', blank=True, help_text="Suppliers who should receive this RFQ")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_viewed_at = models.DateTimeField(blank=True, null=True, help_text="When supplier first opened the order")
    first_responded_at = models.DateTimeField(blank=True, null=True, help_text="When supplier first responded")
    response_points_awarded = models.BooleanField(default=False)
    response_speed_bucket = models.CharField(max_length=20, blank=True, null=True, help_text="Speed category (sub_1h, sub_4h, sub_24h)")
    
    # Commission tracking
    commission_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, help_text="Commission amount for this order")
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Commission rate applied (%)")
    commission_paid = models.BooleanField(default=False, help_text="Whether commission has been deducted")
    commission_paid_at = models.DateTimeField(blank=True, null=True, help_text="When commission was paid/deducted")
    vendor_payout_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount to be paid to vendor after commission")
    vendor_paid = models.BooleanField(default=False, help_text="Whether vendor has been paid")
    vendor_paid_at = models.DateTimeField(blank=True, null=True, help_text="When vendor was paid")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.is_rfq:
            buyer_name = f"{self.first_name} {self.last_name}".strip() if self.first_name or self.last_name else "Anonymous"
            return f"RFQ {self.order_number} - {buyer_name}"
        buyer_name = self.buyer.username if self.buyer else "Anonymous"
        return f"Order {self.order_number} - {buyer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            import uuid
            prefix = "RFQ" if self.is_rfq else "ORD"
            self.order_number = f"{prefix}-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)
    
    def calculate_commission(self):
        """
        Calculate commission for this order based on vendor's pricing tier.
        Returns (commission_amount, commission_rate, vendor_payout_amount)
        """
        if not self.total_amount or self.total_amount <= 0:
            return 0, 0, 0
        
        # Get the vendor from order items (assumes single vendor per order)
        first_item = self.items.first()
        if not first_item or not first_item.seller:
            return 0, 0, 0
        
        vendor = first_item.seller
        
        try:
            from users.models import VendorSubscription
            subscription = VendorSubscription.objects.get(user=vendor)
            
            if not subscription.tier.is_commission_based:
                return 0, 0, self.total_amount
            
            # Calculate commission based on order amount
            commission_amount = subscription.tier.calculate_commission(self.total_amount)
            commission_rate = (
                subscription.tier.commission_rate_high 
                if self.total_amount >= (subscription.tier.commission_threshold or 0) 
                else subscription.tier.commission_rate_low
            )
            vendor_payout = self.total_amount - commission_amount
            
            return commission_amount, commission_rate, vendor_payout
        except:
            return 0, 0, self.total_amount
    
    def apply_commission(self):
        """Apply commission calculation to order fields."""
        commission_amount, commission_rate, vendor_payout = self.calculate_commission()
        self.commission_amount = commission_amount
        self.commission_rate = commission_rate
        self.vendor_payout_amount = vendor_payout
        self.save(update_fields=['commission_amount', 'commission_rate', 'vendor_payout_amount'])
    
    def mark_vendor_paid(self):
        """Mark vendor as paid and record commission."""
        from django.utils import timezone
        from users.models import VendorSubscription
        
        if self.vendor_paid:
            return  # Already paid
        
        # Get vendor
        first_item = self.items.first()
        if not first_item or not first_item.seller:
            return
        
        vendor = first_item.seller
        
        try:
            subscription = VendorSubscription.objects.get(user=vendor)
            if subscription.tier.is_commission_based and self.commission_amount > 0:
                # Record commission in subscription
                subscription.record_commission_sale(
                    self.total_amount,
                    self.commission_amount
                )
                self.commission_paid = True
                self.commission_paid_at = timezone.now()
        except:
            pass
        
        self.vendor_paid = True
        self.vendor_paid_at = timezone.now()
        self.save(update_fields=['vendor_paid', 'vendor_paid_at', 'commission_paid', 'commission_paid_at'])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sold_items')
    product_name = models.CharField(max_length=200)  # Store name in case product is deleted
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2, help_text="Price in smallest currency unit (supports large values for RFQ)")
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        if self.product:
            self.product_name = self.product.name
            self.seller = self.product.vendor
        super().save(*args, **kwargs)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id} for {self.order.order_number}"

class OrderImage(models.Model):
    """Images attached to RFQ orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='order_images/')
    alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for this image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Order Image"
        verbose_name_plural = "Order Images"
    
    def __str__(self):
        return f"Image for Order {self.order.order_number}"


class OrderVendorView(models.Model):
    """Tracks which vendor has revealed/seen an RFQ lead."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='vendor_views')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_rfqs')
    revealed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('order', 'vendor')
        indexes = [
            models.Index(fields=['vendor', 'order']),
        ]

    def __str__(self):
        return f"{self.vendor} viewed {self.order}"
