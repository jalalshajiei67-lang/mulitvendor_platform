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

