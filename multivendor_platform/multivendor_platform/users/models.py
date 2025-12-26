from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

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
    contact_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Mobile phone number")
    contact_phone_landline = models.CharField(max_length=20, blank=True, null=True, help_text="Landline/office phone number")
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True, help_text="Physical address of the supplier")
    
    # New fields for supplier page
    work_resume = models.TextField(blank=True, null=True, help_text="Work experience and resume")
    successful_projects = models.TextField(blank=True, null=True, help_text="List of successful projects")
    history = models.TextField(blank=True, null=True, help_text="Company history and background")
    about = models.TextField(blank=True, null=True, help_text="About the supplier/company")
    
    # Mini website branding fields
    banner_image = models.ImageField(upload_to='vendor_banners/', blank=True, null=True, help_text="Hero banner for supplier page")
    brand_color_primary = models.CharField(max_length=7, blank=True, null=True, help_text="Primary brand color (hex)")
    brand_color_secondary = models.CharField(max_length=7, blank=True, null=True, help_text="Secondary brand color (hex)")
    slogan = models.CharField(max_length=200, blank=True, null=True, help_text="Company slogan/tagline")
    year_established = models.PositiveIntegerField(blank=True, null=True, help_text="Year company was founded")
    employee_count = models.PositiveIntegerField(blank=True, null=True, help_text="Number of employees")
    certifications = models.JSONField(blank=True, null=True, help_text="List of certifications")
    awards = models.JSONField(blank=True, null=True, help_text="List of awards/achievements")
    social_media = models.JSONField(blank=True, null=True, help_text="Social media links")
    video_url = models.URLField(blank=True, null=True, help_text="Company introduction video URL")
    meta_title = models.CharField(max_length=200, blank=True, null=True, help_text="SEO meta title")
    meta_description = models.TextField(blank=True, null=True, help_text="SEO meta description")
    
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


class PricingTier(models.Model):
    """Subscription tier definition for suppliers"""
    PRICING_TYPE_CHOICES = (
        ('subscription', 'Subscription-based'),
        ('commission', 'Commission-based'),
    )
    
    slug = models.SlugField(max_length=50, unique=True, help_text="Unique machine-readable identifier")
    name = models.CharField(max_length=100, help_text="Display name for the tier")
    pricing_type = models.CharField(
        max_length=20,
        choices=PRICING_TYPE_CHOICES,
        default='subscription',
        help_text="Type of pricing model"
    )
    
    # Commission-based fields
    is_commission_based = models.BooleanField(
        default=False,
        help_text="True if this tier uses commission-based pricing"
    )
    commission_rate_low = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Commission rate (%) for orders under threshold (e.g., 5.00 for 5%)"
    )
    commission_rate_high = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Commission rate (%) for orders above threshold (e.g., 3.00 for 3%)"
    )
    commission_threshold = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Threshold amount for commission rate change (e.g., 1000000000 for 1 billion Toman)"
    )
    
    # Subscription-based fields
    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monthly subscription price in Toman (if applicable)"
    )
    monthly_price_rial = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        help_text="Monthly subscription price in Rial for Zibal payment gateway"
    )
    
    daily_customer_unlock_limit = models.PositiveIntegerField(
        default=1,
        help_text="How many new customers can be unlocked in a rolling 24h window (0 for unlimited)."
    )
    allow_marketplace_visibility = models.BooleanField(
        default=True,
        help_text="If false, products stay hidden from marketplace regardless of other flags."
    )
    lead_exclusivity = models.CharField(
        max_length=20,
        default='shared',
        choices=(
            ('shared', 'Shared lead (non-exclusive)'),
            ('exclusive', 'Exclusive after claim'),
        ),
        help_text="Defines whether leads become exclusive when revealed at this tier."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['slug']
        verbose_name = "Pricing Tier"
        verbose_name_plural = "Pricing Tiers"

    def __str__(self):
        return self.name

    def calculate_commission(self, order_amount):
        """Calculate commission amount for a given order amount."""
        if not self.is_commission_based:
            return 0
        
        if order_amount >= (self.commission_threshold or 0):
            rate = self.commission_rate_high or 0
        else:
            rate = self.commission_rate_low or 0
        
        return (order_amount * rate) / 100
    
    @classmethod
    def get_default_free(cls):
        """Return the default free tier, creating it if missing."""
        # #region agent log
        import json
        try:
            with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'post-fix',
                    'hypothesisId': 'A',
                    'location': 'users/models.py:209',
                    'message': 'get_default_free entry',
                    'data': {'method': 'get_default_free', 'cls': str(cls)},
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except: pass
        # #endregion
        from django.db import OperationalError
        try:
            # Try normal get_or_create first
            tier, _ = cls.objects.get_or_create(
                slug='free',
                defaults={
                    'name': 'Free',
                    'pricing_type': 'subscription',
                    'is_commission_based': False,
                    'daily_customer_unlock_limit': 1,
                    'lead_exclusivity': 'shared',
                    'allow_marketplace_visibility': True,
                },
            )
            # #region agent log
            try:
                with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'post-fix',
                        'hypothesisId': 'A',
                        'location': 'users/models.py:222',
                        'message': 'get_or_create success',
                        'data': {'tier_id': tier.id if tier else None, 'created': _},
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except: pass
            # #endregion
            return tier
        except OperationalError as e:
            # Handle case where monthly_price_rial column doesn't exist yet (migration not applied)
            if 'monthly_price_rial' in str(e):
                # #region agent log
                try:
                    with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                        f.write(json.dumps({
                            'sessionId': 'debug-session',
                            'runId': 'post-fix',
                            'hypothesisId': 'A',
                            'location': 'users/models.py:230',
                            'message': 'Migration workaround - using only() to exclude monthly_price_rial',
                            'data': {'error': str(e)},
                            'timestamp': int(__import__('time').time() * 1000)
                        }) + '\n')
                except: pass
                # #endregion
                # Use only() to query without the problematic field
                try:
                    tier = cls.objects.only('id', 'slug', 'name', 'pricing_type', 'is_commission_based', 
                                            'daily_customer_unlock_limit', 'lead_exclusivity', 
                                            'allow_marketplace_visibility', 'created_at', 'updated_at').get(slug='free')
                    # #region agent log
                    try:
                        with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                            f.write(json.dumps({
                                'sessionId': 'debug-session',
                                'runId': 'post-fix',
                                'hypothesisId': 'A',
                                'location': 'users/models.py:240',
                                'message': 'Found existing tier using only()',
                                'data': {'tier_id': tier.id},
                                'timestamp': int(__import__('time').time() * 1000)
                            }) + '\n')
                    except: pass
                    # #endregion
                    return tier
                except cls.DoesNotExist:
                    # Create without monthly_price_rial field
                    tier = cls.objects.create(
                        slug='free',
                        name='Free',
                        pricing_type='subscription',
                        is_commission_based=False,
                        daily_customer_unlock_limit=1,
                        lead_exclusivity='shared',
                        allow_marketplace_visibility=True,
                    )
                    # #region agent log
                    try:
                        with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                            f.write(json.dumps({
                                'sessionId': 'debug-session',
                                'runId': 'post-fix',
                                'hypothesisId': 'A',
                                'location': 'users/models.py:255',
                                'message': 'Created tier without monthly_price_rial',
                                'data': {'tier_id': tier.id},
                                'timestamp': int(__import__('time').time() * 1000)
                            }) + '\n')
                    except: pass
                    # #endregion
                    return tier
            else:
                # Re-raise if it's a different OperationalError
                raise
    
    @classmethod
    def get_commission_tier(cls):
        """Return the commission-based tier, creating it if missing."""
        from django.db import OperationalError
        try:
            # Try normal get_or_create first
            tier, _ = cls.objects.get_or_create(
                slug='commission',
                defaults={
                    'name': 'Commission',
                    'pricing_type': 'commission',
                    'is_commission_based': True,
                    'commission_rate_low': 5.00,  # 5% for under 1 billion
                    'commission_rate_high': 3.00,  # 3% for over 1 billion
                    'commission_threshold': 1000000000,  # 1 billion Toman
                    'daily_customer_unlock_limit': 0,  # Unlimited
                    'lead_exclusivity': 'shared',
                    'allow_marketplace_visibility': True,
                },
            )
            return tier
        except OperationalError as e:
            # Handle case where monthly_price_rial column doesn't exist yet (migration not applied)
            if 'monthly_price_rial' in str(e):
                # Use only() to query without the problematic field
                try:
                    tier = cls.objects.only('id', 'slug', 'name', 'pricing_type', 'is_commission_based',
                                            'commission_rate_low', 'commission_rate_high', 'commission_threshold',
                                            'daily_customer_unlock_limit', 'lead_exclusivity',
                                            'allow_marketplace_visibility', 'created_at', 'updated_at').get(slug='commission')
                    return tier
                except cls.DoesNotExist:
                    # Create without monthly_price_rial field
                    tier = cls.objects.create(
                        slug='commission',
                        name='Commission',
                        pricing_type='commission',
                        is_commission_based=True,
                        commission_rate_low=5.00,
                        commission_rate_high=3.00,
                        commission_threshold=1000000000,
                        daily_customer_unlock_limit=0,
                        lead_exclusivity='shared',
                        allow_marketplace_visibility=True,
                    )
                    return tier
            else:
                # Re-raise if it's a different OperationalError
                raise


class VendorSubscription(models.Model):
    """Active subscription for a vendor/user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_subscription')
    tier = models.ForeignKey(PricingTier, on_delete=models.PROTECT, related_name='subscriptions')
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True, help_text="Optional expiration for paid plans")
    auto_renew = models.BooleanField(default=False, help_text="Auto-renew subscription on expiry")
    expiry_reminder_sent = models.DateTimeField(blank=True, null=True, help_text="When expiry reminder was sent")
    last_customer_unlock_at = models.DateTimeField(blank=True, null=True, help_text="Last time a new customer was unlocked")
    total_customer_unlocks = models.PositiveIntegerField(default=0, help_text="Total unlocks ever made by this vendor")
    is_active = models.BooleanField(default=True)
    
    # Commission-based plan fields
    contract_signed = models.BooleanField(default=False, help_text="Whether vendor has signed the commission contract")
    contract_signed_at = models.DateTimeField(blank=True, null=True, help_text="When contract was signed")
    contract_document = models.FileField(upload_to='vendor_contracts/', blank=True, null=True, help_text="Signed contract document")
    bank_guarantee_submitted = models.BooleanField(default=False, help_text="Whether bank guarantee has been submitted")
    bank_guarantee_document = models.FileField(upload_to='bank_guarantees/', blank=True, null=True, help_text="Bank guarantee document")
    bank_guarantee_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of bank guarantee")
    bank_guarantee_expiry = models.DateField(blank=True, null=True, help_text="Bank guarantee expiry date")
    terms_accepted = models.BooleanField(default=False, help_text="Whether vendor accepted terms and conditions")
    terms_accepted_at = models.DateTimeField(blank=True, null=True, help_text="When terms were accepted")
    admin_approved = models.BooleanField(default=False, help_text="Whether admin has approved commission plan activation")
    admin_approved_at = models.DateTimeField(blank=True, null=True, help_text="When admin approved")
    admin_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_subscriptions', help_text="Admin who approved")
    rejection_reason = models.TextField(blank=True, null=True, help_text="Reason for rejection if not approved")
    
    # Commission tracking
    total_commission_charged = models.DecimalField(max_digits=20, decimal_places=2, default=0, help_text="Total commission charged to vendor")
    total_sales_volume = models.DecimalField(max_digits=20, decimal_places=2, default=0, help_text="Total sales volume for commission calculation")

    class Meta:
        verbose_name = "Vendor Subscription"
        verbose_name_plural = "Vendor Subscriptions"

    def __str__(self):
        return f"{self.user.username} - {self.tier.slug}"

    @classmethod
    def for_user(cls, user: User) -> "VendorSubscription":
        """
        Return the subscription for the given user, creating a free subscription
        if none exists.
        """
        # #region agent log
        import json
        try:
            with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A',
                    'location': 'users/models.py:343',
                    'message': 'for_user entry',
                    'data': {'user_id': user.id if user else None, 'username': user.username if user else None},
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except: pass
        # #endregion
        tier = PricingTier.get_default_free()
        # #region agent log
        try:
            with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A',
                    'location': 'users/models.py:349',
                    'message': 'After get_default_free',
                    'data': {'tier_id': tier.id if tier else None, 'tier_slug': tier.slug if tier else None},
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except: pass
        # #endregion
        subscription, _ = cls.objects.get_or_create(
            user=user,
            defaults={'tier': tier, 'is_active': True},
        )
        # #region agent log
        try:
            with open('/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log', 'a') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'A',
                    'location': 'users/models.py:353',
                    'message': 'for_user exit',
                    'data': {'subscription_id': subscription.id if subscription else None, 'created': _},
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except: pass
        # #endregion
        return subscription

    def can_unlock_customer(self):
        """
        Check whether vendor can unlock a new customer in the current rolling 24h window.
        Returns (can_unlock: bool, next_time: datetime|None).
        """
        limit = self.tier.daily_customer_unlock_limit or 0
        if limit == 0:
            return True, None

        if not self.last_customer_unlock_at:
            return True, None

        next_time = self.last_customer_unlock_at + timedelta(hours=24)
        return timezone.now() >= next_time, next_time

    def register_customer_unlock(self):
        """Record a successful customer unlock."""
        self.last_customer_unlock_at = timezone.now()
        self.total_customer_unlocks += 1
        self.save(update_fields=['last_customer_unlock_at', 'total_customer_unlocks'])
    
    def can_activate_commission_plan(self):
        """
        Check if vendor can activate commission-based plan.
        Requires: complete profile data AND gold tier (or higher) achievement.
        Returns (can_activate: bool, missing_requirements: list)
        """
        missing = []
        
        # Check if vendor profile is complete
        try:
            vendor_profile = self.user.vendor_profile
            if not vendor_profile.store_name:
                missing.append('store_name')
            if not vendor_profile.contact_email:
                missing.append('contact_email')
            if not vendor_profile.contact_phone:
                missing.append('contact_phone')
            if not vendor_profile.address:
                missing.append('address')
        except:
            missing.append('vendor_profile')
        
        # Check if user profile exists
        try:
            user_profile = self.user.profile
            if not user_profile.phone:
                missing.append('phone')
        except:
            missing.append('user_profile')
        
        # Check if seller has achieved gold tier (or higher)
        try:
            from gamification.services import GamificationService
            service = GamificationService.for_user(self.user)
            current_tier = service.calculate_tier()
            
            # Gold tier requires: 500+ points AND 60+ reputation
            # Diamond tier is also acceptable (higher than gold)
            tier_order = ['inactive', 'bronze', 'silver', 'gold', 'diamond']
            current_tier_index = tier_order.index(current_tier) if current_tier in tier_order else 0
            gold_tier_index = tier_order.index('gold')
            
            if current_tier_index < gold_tier_index:
                missing.append('gold_tier')
        except Exception as e:
            # If gamification service fails, treat as missing gold tier
            missing.append('gold_tier')
        
        return len(missing) == 0, missing
    
    def is_commission_plan_ready(self):
        """Check if commission plan is fully activated and ready to use."""
        if not self.tier.is_commission_based:
            return False
        return (
            self.contract_signed and 
            self.bank_guarantee_submitted and 
            self.terms_accepted and 
            self.admin_approved and 
            self.is_active
        )
    
    def record_commission_sale(self, sale_amount, commission_amount):
        """Record a sale and commission charge."""
        self.total_sales_volume += sale_amount
        self.total_commission_charged += commission_amount
        self.save(update_fields=['total_sales_volume', 'total_commission_charged'])

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
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True, null=True)
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
    is_flagged = models.BooleanField(default=False, help_text="Flagged for moderation")
    flag_reason = models.CharField(max_length=255, blank=True, null=True)
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

class SupplierPortfolioItem(models.Model):
    """Portfolio items/projects for supplier mini websites"""
    vendor_profile = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200, help_text="Project/portfolio title")
    description = models.TextField(help_text="Project description")
    image = models.ImageField(upload_to='portfolio_images/', help_text="Project image")
    project_date = models.DateField(blank=True, null=True, help_text="Date of project")
    client_name = models.CharField(max_length=200, blank=True, null=True, help_text="Client name (optional)")
    category = models.CharField(max_length=100, blank=True, null=True, help_text="Portfolio category")
    sort_order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_featured = models.BooleanField(default=False, help_text="Featured project flag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-project_date', '-created_at']
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"
    
    def __str__(self):
        return f"{self.vendor_profile.store_name} - {self.title}"

class SupplierTeamMember(models.Model):
    """Team members for supplier mini websites"""
    vendor_profile = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=200, help_text="Member name")
    position = models.CharField(max_length=200, help_text="Job title")
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True, help_text="Member photo")
    bio = models.TextField(blank=True, null=True, help_text="Short bio")
    sort_order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return f"{self.name} - {self.position} at {self.vendor_profile.store_name}"

class SupplierContactMessage(models.Model):
    """Contact messages sent to suppliers through their mini websites"""
    vendor_profile = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='contact_messages')
    sender_name = models.CharField(max_length=200, help_text="Sender's name")
    sender_email = models.EmailField(help_text="Sender's email")
    sender_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Sender's phone")
    subject = models.CharField(max_length=200, help_text="Message subject")
    message = models.TextField(help_text="Message content")
    is_read = models.BooleanField(default=False, help_text="Read status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"Message from {self.sender_name} to {self.vendor_profile.store_name}"

class OTP(models.Model):
    """One-Time Password for authentication and verification"""
    PURPOSE_CHOICES = (
        ('login', 'Login'),
        ('password_reset', 'Password Reset'),
        ('phone_verification', 'Phone Verification'),
        ('transaction', 'Transaction'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps', null=True, blank=True, help_text="User (nullable for phone-based OTP)")
    phone = models.CharField(max_length=20, help_text="Phone number (when user is not authenticated)")
    code = models.CharField(max_length=6, help_text="6-digit OTP code")
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, help_text="Purpose of the OTP")
    is_used = models.BooleanField(default=False, help_text="Whether the OTP has been used")
    expires_at = models.DateTimeField(help_text="Expiration time of the OTP")
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0, help_text="Number of verification attempts")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        indexes = [
            models.Index(fields=['phone', 'purpose', 'is_used']),
            models.Index(fields=['user', 'purpose', 'is_used']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else self.phone
        return f"OTP for {user_str} - {self.get_purpose_display()} ({'used' if self.is_used else 'active'})"
    
    def is_expired(self):
        """Check if OTP has expired"""
        from django.utils import timezone
        return timezone.now() > self.expires_at


class SellerContact(models.Model):
    """CRM Contact management for sellers"""
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crm_contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="General notes about the contact")
    source_order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_contacts', help_text="Order/RFQ that created this contact")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Seller Contact"
        verbose_name_plural = "Seller Contacts"
        indexes = [
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip()
        if self.company_name:
            return f"{name} ({self.company_name})"
        return name or self.phone


class ContactNote(models.Model):
    """Notes linked to CRM contacts"""
    contact = models.ForeignKey(SellerContact, on_delete=models.CASCADE, related_name='contact_notes')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crm_notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Note"
        verbose_name_plural = "Contact Notes"
        indexes = [
            models.Index(fields=['contact', '-created_at']),
            models.Index(fields=['seller', '-created_at']),
        ]
    
    def __str__(self):
        return f"Note for {self.contact} - {self.created_at.strftime('%Y-%m-%d')}"


class ContactTask(models.Model):
    """Tasks/Reminders for CRM"""
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    contact = models.ForeignKey(SellerContact, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True, help_text="Optional: link task to a contact")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crm_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', '-priority']
        verbose_name = "Contact Task"
        verbose_name_plural = "Contact Tasks"
        indexes = [
            models.Index(fields=['seller', 'status', 'due_date']),
            models.Index(fields=['contact', 'status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        contact_str = f" for {self.contact}" if self.contact else ""
        return f"{self.title}{contact_str} - {self.get_status_display()}"