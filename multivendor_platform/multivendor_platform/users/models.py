from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class UserProfile(models.Model):
    """Extended user profile with roles"""
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Supplier'),
        ('both', 'Both'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False, help_text="User verified by admin")
    is_blocked = models.BooleanField(default=False, help_text="User blocked by admin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def is_seller(self):
        return self.role in ['seller', 'both']
    
    def is_buyer(self):
        return self.role in ['buyer', 'both']

class BuyerProfile(models.Model):
    """Buyer specific information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    default_payment_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Buyer Profile"
        verbose_name_plural = "Buyer Profiles"
    
    def __str__(self):
        return f"Buyer: {self.user.username}"

class VendorProfile(models.Model):
    """Supplier/Vendor specific information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    store_name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True, help_text="Physical address of the supplier")
    
    # New fields for supplier page
    work_resume = models.TextField(blank=True, null=True, help_text="Work experience and resume")
    successful_projects = models.TextField(blank=True, null=True, help_text="List of successful projects")
    history = models.TextField(blank=True, null=True, help_text="Company history and background")
    about = models.TextField(blank=True, null=True, help_text="About the supplier/company")
    
    is_approved = models.BooleanField(default=False, help_text="Approved by admin as supplier")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Supplier Profile"
        verbose_name_plural = "Supplier Profiles"
    
    def __str__(self):
        return self.store_name
    
    def get_product_count(self):
        """Get total number of products from this supplier"""
        return self.user.products.filter(is_active=True).count()
    
    def get_rating_average(self):
        """Get average rating from supplier comments"""
        from django.db.models import Avg
        avg = self.comments.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

class Supplier(models.Model):
    """Company/Supplier model - scraped or manually created"""
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suppliers', help_text="The user/admin who manages this supplier")
    name = models.CharField(max_length=200, help_text="Company name")
    website = models.URLField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text="About the company")
    logo = models.ImageField(upload_to='supplier_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Supplier/Company"
        verbose_name_plural = "Suppliers/Companies"
        unique_together = [['name', 'website']]  # Unique by name AND website
    
    def __str__(self):
        return self.name
    
    def get_product_count(self):
        """Get total number of products from this supplier"""
        return self.products.filter(is_active=True).count()


class SellerAd(models.Model):
    """Advertisement created by suppliers"""
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    description = models.TextField()
    contact_info = models.TextField(help_text="Contact information for this ad")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Supplier Advertisement"
        verbose_name_plural = "Supplier Advertisements"
    
    def __str__(self):
        return self.title

class SellerAdImage(models.Model):
    """Images for supplier advertisements"""
    ad = models.ForeignKey(SellerAd, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ad_images/')
    alt_text = models.CharField(max_length=125, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sort_order', 'created_at']
        verbose_name = "Supplier Ad Image"
        verbose_name_plural = "Supplier Ad Images"
    
    def __str__(self):
        return f"Image for {self.ad.title}"

class ProductReview(models.Model):
    """Product reviews and comments by buyers"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='product_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    seller_reply = models.TextField(blank=True, null=True)
    seller_replied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.buyer.username} - {self.product.name} ({self.rating}★)"

class SupplierComment(models.Model):
    """Comments and reviews for suppliers/vendors"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    supplier = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplier_comments')
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True, help_text="Approved by admin")
    supplier_reply = models.TextField(blank=True, null=True)
    supplier_replied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Supplier Comment"
        verbose_name_plural = "Supplier Comments"
    
    def __str__(self):
        return f"{self.user.username} - {self.supplier.store_name} ({self.rating}★)"

class UserActivity(models.Model):
    """Track user activities for admin monitoring"""
    ACTION_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Register'),
        ('create_product', 'Create Product'),
        ('update_product', 'Update Product'),
        ('delete_product', 'Delete Product'),
        ('create_order', 'Create Order'),
        ('update_order', 'Update Order'),
        ('create_ad', 'Create Ad'),
        ('update_ad', 'Update Ad'),
        ('delete_ad', 'Delete Ad'),
        ('create_review', 'Create Review'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('password_reset', 'Password Reset'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Generic relation to track what object was affected
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Activities"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} at {self.created_at}"