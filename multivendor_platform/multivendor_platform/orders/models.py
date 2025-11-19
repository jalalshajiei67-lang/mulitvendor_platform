from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category

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
    first_name = models.CharField(max_length=100, blank=True, null=True, help_text="Buyer first name (for RFQ)")
    last_name = models.CharField(max_length=100, blank=True, null=True, help_text="Buyer last name (for RFQ)")
    company_name = models.CharField(max_length=200, blank=True, null=True, help_text="Company name (for RFQ)")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number (for RFQ)")
    unique_needs = models.TextField(blank=True, null=True, help_text="Buyer's unique requirements/needs (for RFQ)")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='rfq_orders', help_text="Category for RFQ (if submitted from category page)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_viewed_at = models.DateTimeField(blank=True, null=True, help_text="When supplier first opened the order")
    first_responded_at = models.DateTimeField(blank=True, null=True, help_text="When supplier first responded")
    response_points_awarded = models.BooleanField(default=False)
    response_speed_bucket = models.CharField(max_length=20, blank=True, null=True, help_text="Speed category (sub_1h, sub_4h, sub_24h)")
    
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
