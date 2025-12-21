from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class PremiumSubscriptionPayment(models.Model):
    """Model to track premium subscription payments"""
    
    BILLING_PERIOD_CHOICES = (
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semiannual', 'Semiannual'),
        ('yearly', 'Yearly'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    # User and subscription info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='premium_payments')
    billing_period = models.CharField(max_length=20, choices=BILLING_PERIOD_CHOICES, default='monthly')
    amount = models.DecimalField(max_digits=12, decimal_places=0, help_text="Amount in Rials")
    
    # Zibal tracking
    track_id = models.CharField(max_length=100, unique=True, db_index=True, help_text="Zibal track ID")
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, help_text="Internal order ID")
    ref_number = models.CharField(max_length=100, blank=True, null=True, help_text="Zibal reference number")
    card_number = models.CharField(max_length=20, blank=True, null=True, help_text="Masked card number")
    
    # Payment status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='zibal', help_text="Payment gateway used")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True, help_text="When payment was made")
    verified_at = models.DateTimeField(blank=True, null=True, help_text="When payment was verified")
    
    # Additional info
    description = models.TextField(blank=True, null=True)
    zibal_response = models.JSONField(blank=True, null=True, help_text="Full response from Zibal")
    
    # Discount info
    discount_campaign = models.ForeignKey(
        'DiscountCampaign',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        help_text="Discount campaign used for this payment"
    )
    discount_amount_toman = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        help_text="Discount amount applied in Toman"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Premium Subscription Payment"
        verbose_name_plural = "Premium Subscription Payments"
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_billing_period_display()} - {self.status}"
    
    def get_amount_toman(self):
        """Convert Rial to Toman for display"""
        return self.amount / 10
    
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
    
    def mark_as_failed(self):
        """Mark payment as failed"""
        self.status = 'failed'
        self.save(update_fields=['status'])
    
    def get_subscription_duration_days(self):
        """Get subscription duration in days based on billing period"""
        duration_map = {
            'monthly': 30,
            'quarterly': 90,
            'semiannual': 180,
            'yearly': 365,
        }
        return duration_map.get(self.billing_period, 30)


class PaymentInvoice(models.Model):
    """Model to store payment invoices"""
    
    payment = models.OneToOneField(
        PremiumSubscriptionPayment,
        on_delete=models.CASCADE,
        related_name='invoice'
    )
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique invoice number"
    )
    
    # Invoice details
    issue_date = models.DateTimeField(auto_now_add=True, help_text="Invoice issue date")
    due_date = models.DateField(help_text="Payment due date (for records)")
    
    # Financial details
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, help_text="Subtotal in Rials")
    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        help_text="Tax amount (9% VAT)"
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, help_text="Total amount in Rials")
    
    # PDF storage
    invoice_pdf = models.FileField(
        upload_to='invoices/%Y/%m/',
        blank=True,
        null=True,
        help_text="Generated PDF invoice"
    )
    
    # Additional info
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment Invoice"
        verbose_name_plural = "Payment Invoices"
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.payment.user.username}"
    
    def generate_invoice_number(self):
        """Generate unique invoice number"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"INV-{timestamp}-{self.payment.user.id}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        if not self.due_date:
            self.due_date = timezone.now().date()
        super().save(*args, **kwargs)


class DiscountCampaign(models.Model):
    """Model for promotional discount campaigns"""
    
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount (Toman)'),
    )
    
    BILLING_PERIOD_CHOICES = (
        ('all', 'All Periods'),
        ('monthly', 'Monthly Only'),
        ('quarterly', 'Quarterly Only'),
        ('semiannual', 'Semiannual Only'),
        ('yearly', 'Yearly Only'),
    )
    
    # Campaign info
    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique discount code (e.g., SUMMER2024). Will be stored in uppercase."
    )
    
    def save(self, *args, **kwargs):
        """Normalize code to uppercase before saving"""
        if self.code:
            self.code = self.code.strip().upper()
        super().save(*args, **kwargs)
    name = models.CharField(
        max_length=200,
        help_text="Campaign name for admin reference"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Campaign description"
    )
    
    # Discount settings
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage',
        help_text="Type of discount"
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Discount amount (percentage or fixed Toman)"
    )
    
    # Applicability
    billing_period = models.CharField(
        max_length=20,
        choices=BILLING_PERIOD_CHOICES,
        default='all',
        help_text="Which billing periods this discount applies to"
    )
    min_amount_toman = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        help_text="Minimum purchase amount in Toman (0 = no minimum)"
    )
    max_discount_toman = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        blank=True,
        null=True,
        help_text="Maximum discount amount in Toman (null = no limit)"
    )
    
    # Usage limits
    max_uses = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Maximum number of times this code can be used (null = unlimited)"
    )
    max_uses_per_user = models.PositiveIntegerField(
        default=1,
        help_text="Maximum times a single user can use this code"
    )
    used_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this code has been used"
    )
    
    # Validity period
    valid_from = models.DateTimeField(
        help_text="Campaign start date and time"
    )
    valid_until = models.DateTimeField(
        help_text="Campaign end date and time"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this campaign is currently active"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_discount_campaigns',
        help_text="Admin user who created this campaign"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Discount Campaign"
        verbose_name_plural = "Discount Campaigns"
        indexes = [
            models.Index(fields=['code', 'is_active']),
            models.Index(fields=['valid_from', 'valid_until']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def is_valid(self, user=None, billing_period=None, amount_toman=None):
        """
        Check if discount code is valid for given conditions
        """
        from django.utils import timezone
        
        # Check if active
        if not self.is_active:
            return False, "این کد تخفیف غیرفعال است"
        
        # Check validity period
        now = timezone.now()
        if now < self.valid_from:
            return False, "این کد تخفیف هنوز فعال نشده است"
        if now > self.valid_until:
            return False, "این کد تخفیف منقضی شده است"
        
        # Check usage limits
        if self.max_uses and self.used_count >= self.max_uses:
            return False, "این کد تخفیف به حداکثر استفاده رسیده است"
        
        # Check user usage limit
        if user:
            user_usage = DiscountUsage.objects.filter(
                campaign=self,
                user=user
            ).count()
            if user_usage >= self.max_uses_per_user:
                return False, "شما قبلاً از این کد تخفیف استفاده کرده‌اید"
        
        # Check billing period
        if billing_period and self.billing_period != 'all':
            if self.billing_period != billing_period:
                return False, f"این کد تخفیف فقط برای پرداخت {self.get_billing_period_display()} معتبر است"
        
        # Check minimum amount
        if amount_toman and self.min_amount_toman > 0:
            if amount_toman < self.min_amount_toman:
                return False, f"حداقل مبلغ خرید برای استفاده از این کد {int(self.min_amount_toman):,} تومان است"
        
        return True, None
    
    def calculate_discount(self, amount_toman):
        """
        Calculate discount amount in Toman
        Returns: (discount_amount_toman, final_amount_toman)
        """
        from decimal import Decimal
        
        # Convert inputs to Decimal for precise calculations
        amount_decimal = Decimal(str(amount_toman))
        discount_value_decimal = Decimal(str(self.discount_value))
        
        if self.discount_type == 'percentage':
            discount = (amount_decimal * discount_value_decimal) / Decimal('100')
        else:  # fixed
            discount = discount_value_decimal
        
        # Apply max discount limit if set
        if self.max_discount_toman:
            max_discount_decimal = Decimal(str(self.max_discount_toman))
            if discount > max_discount_decimal:
                discount = max_discount_decimal
        
        final_amount = max(Decimal('0'), amount_decimal - discount)
        
        # Return as floats for API response
        return float(discount), float(final_amount)
    
    def record_usage(self, user, payment):
        """Record that this discount code was used"""
        DiscountUsage.objects.create(
            campaign=self,
            user=user,
            payment=payment
        )
        self.used_count += 1
        self.save(update_fields=['used_count'])


class DiscountUsage(models.Model):
    """Track usage of discount codes by users"""
    
    campaign = models.ForeignKey(
        DiscountCampaign,
        on_delete=models.CASCADE,
        related_name='usages'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discount_usages'
    )
    payment = models.ForeignKey(
        PremiumSubscriptionPayment,
        on_delete=models.CASCADE,
        related_name='discount_usage',
        null=True,
        blank=True
    )
    discount_amount_toman = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        help_text="Discount amount applied in Toman"
    )
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-used_at']
        verbose_name = "Discount Usage"
        verbose_name_plural = "Discount Usages"
        indexes = [
            models.Index(fields=['campaign', 'user']),
            models.Index(fields=['user', '-used_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.campaign.code} - {self.used_at}"
