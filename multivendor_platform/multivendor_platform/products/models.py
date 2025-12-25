# products/models.py
import os
from typing import Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='department_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for the image (for SEO and accessibility)")
    og_image = models.ImageField(upload_to='department_og_images/', blank=True, null=True, help_text="Open Graph image for social media sharing")
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    canonical_url = models.URLField(max_length=500, blank=True, null=True, help_text="Canonical URL for SEO")
    schema_markup = models.TextField(blank=True, null=True, help_text="JSON-LD Schema markup for rich snippets")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = "Departments"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for the image (for SEO and accessibility)")
    og_image = models.ImageField(upload_to='category_og_images/', blank=True, null=True, help_text="Open Graph image for social media sharing")
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    canonical_url = models.URLField(max_length=500, blank=True, null=True, help_text="Canonical URL for SEO")
    schema_markup = models.TextField(blank=True, null=True, help_text="JSON-LD Schema markup for rich snippets")
    departments = models.ManyToManyField(Department, related_name='categories', blank=True)
    subcategories = models.ManyToManyField('Subcategory', related_name='parent_categories', blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = "Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for the image (for SEO and accessibility)")
    og_image = models.ImageField(upload_to='subcategory_og_images/', blank=True, null=True, help_text="Open Graph image for social media sharing")
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    canonical_url = models.URLField(max_length=500, blank=True, null=True, help_text="Canonical URL for SEO")
    schema_markup = models.TextField(blank=True, null=True, help_text="JSON-LD Schema markup for rich snippets")
    categories = models.ManyToManyField(Category, related_name='child_subcategories', blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = "Subcategories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_departments(self):
        """Get all departments through categories"""
        departments = set()
        for category in self.categories.all():
            departments.update(category.departments.all())
        return list(departments)

class CategoryRequest(models.Model):
    """
    Model for suppliers to request new subcategories when existing ones don't fit their products.
    Admin manually creates the category structure after approval.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    supplier = models.ForeignKey('users.Supplier', on_delete=models.CASCADE, related_name='category_requests', help_text="Supplier who requested the category")
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='category_request', null=True, blank=True, help_text="Product that triggered this request")
    requested_name = models.CharField(max_length=100, help_text="Name of the subcategory requested by supplier")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin notes or rejection reason")
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_category_requests', help_text="Admin who reviewed this request")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Category Request'
        verbose_name_plural = 'Category Requests'
    
    def __str__(self):
        return f"{self.requested_name} - {self.get_status_display()} ({self.supplier.name})"

class Product(models.Model):
    APPROVAL_STATUS_PENDING = 'pending'
    APPROVAL_STATUS_APPROVED = 'approved'
    APPROVAL_STATUS_REJECTED = 'rejected'
    APPROVAL_STATUS_CHOICES = [
        (APPROVAL_STATUS_PENDING, 'در انتظار تایید'),
        (APPROVAL_STATUS_APPROVED, 'تایید شده'),
        (APPROVAL_STATUS_REJECTED, 'رد شده'),
    ]
    
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')  # Keep for backward compatibility
    supplier = models.ForeignKey('users.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='products', help_text="Company/Supplier")
    subcategories = models.ManyToManyField(Subcategory, related_name='products', blank=True)  # Changed from ForeignKey
    primary_category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True, help_text="Primary category for breadcrumb display")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.PositiveBigIntegerField(help_text="Price in smallest currency unit (no decimals, supports at least 12 digits)")
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Keep for backward compatibility
    image_alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for the main image (for SEO and accessibility)")
    og_image = models.ImageField(upload_to='product_og_images/', blank=True, null=True, help_text="Open Graph image for social media sharing")
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    canonical_url = models.URLField(max_length=500, blank=True, null=True, help_text="Canonical URL for SEO")
    schema_markup = models.TextField(blank=True, null=True, help_text="JSON-LD Schema markup for rich snippets")
    is_active = models.BooleanField(default=True)
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default=APPROVAL_STATUS_PENDING,
        help_text="وضعیت تایید ادمین برای انتشار محصول"
    )
    is_marketplace_hidden = models.BooleanField(
        default=False,
        help_text="اگر فعال باشد، محصول از مارکت‌پلیس اصلی مخفی می‌شود و فقط در مینی‌وبسایت و داشبورد فروشنده دیده می‌شود."
    )
    marketplace_hide_reason = models.TextField(
        blank=True,
        null=True,
        help_text="یادداشت دوستانه ادمین برای توضیح دلیل عدم نمایش (مثلا وجود واترمارک یا اطلاعات فروشنده)."
    )
    
    # Product availability and status fields
    AVAILABILITY_CHOICES = [
        ('in_stock', 'موجود در انبار'),
        ('made_to_order', 'سفارشی'),
    ]
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        blank=True,
        null=True,
        help_text="وضعیت موجودی محصول"
    )
    
    CONDITION_CHOICES = [
        ('new', 'نو'),
        ('used', 'دست دوم'),
    ]
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        blank=True,
        null=True,
        help_text="وضعیت محصول (فقط برای محصولات موجود در انبار)"
    )
    
    ORIGIN_CHOICES = [
        ('iran', 'ساخت ایران'),
        ('imported', 'وارداتی'),
    ]
    origin = models.CharField(
        max_length=20,
        choices=ORIGIN_CHOICES,
        blank=True,
        null=True,
        help_text="مبدا محصول"
    )
    
    lead_time_days = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="زمان تحویل به روز کاری (فقط برای محصولات سفارشی)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # NOTE: labels field is defined after Label model is created (see below)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Enforce admin approval before activation
        if self.approval_status != self.APPROVAL_STATUS_APPROVED:
            # Draft/Pending/Rejected products stay inactive
            self.is_active = False
        else:
            # Products with pending category requests are visible to supplier but not active
            # Products without category and without pending request are inactive
            if not self.primary_category:
                # Check if there's a pending category request
                if hasattr(self, 'category_request') and self.category_request and self.category_request.status == 'pending':
                    # Product is visible to supplier but not active in public listings
                    self.is_active = False
                elif not hasattr(self, 'category_request') or not self.category_request:
                    # No category and no request - inactive
                    self.is_active = False
            else:
                # Has proper category, can be active
                self.is_active = True
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def get_full_category_path(self):
        """Returns the full category path: Department > Category > Subcategory"""
        subcategories = self.subcategories.all()
        if not subcategories.exists():
            return "No Category"
        
        subcategory = subcategories.first()
        categories = subcategory.categories.all()
        departments = subcategory.get_departments()  # Get departments through categories
        
        path_parts = []
        if departments:
            path_parts.append(departments[0].name)
        if categories.exists():
            path_parts.append(categories.first().name)
        path_parts.append(subcategory.name)
        
        return ' > '.join(path_parts)
    
    @property
    def get_breadcrumb_hierarchy(self):
        """Returns structured breadcrumb data: Department > Category > Subcategory > Product"""
        subcategories = self.subcategories.all()
        if not subcategories.exists():
            return []
        
        subcategory = subcategories.first()
        categories = subcategory.categories.all()
        departments = subcategory.get_departments()  # Get departments through categories
        
        breadcrumb = []
        
        # Add department if exists
        if departments:
            dept = departments[0]
            breadcrumb.append({
                'type': 'department',
                'name': dept.name,
                'slug': dept.slug
            })
        
        # Add category if exists
        if categories.exists():
            cat = categories.first()
            breadcrumb.append({
                'type': 'category',
                'name': cat.name,
                'slug': cat.slug
            })
        
        # Add subcategory
        breadcrumb.append({
            'type': 'subcategory',
            'name': subcategory.name,
            'slug': subcategory.slug
        })
        
        return breadcrumb
    
    @property
    def primary_subcategory(self):
        """Returns the primary subcategory for this product"""
        return self.subcategories.first() if self.subcategories.exists() else None
    
    @property
    def primary_image(self):
        """Returns the primary image or the first image if no primary is set"""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return self.image  # Fallback to old image field
    
    @property
    def all_images(self):
        """Returns all images ordered by sort_order and is_primary"""
        return self.images.all().order_by('-is_primary', 'sort_order', 'created_at')

class ProductFeature(models.Model):
    """Key features/specifications for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=200, help_text="نام ویژگی")
    value = models.CharField(max_length=500, help_text="مقدار ویژگی")
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'created_at']
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for this image (for SEO and accessibility)")
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', 'sort_order', 'created_at']
    
    def save(self, *args, **kwargs):
        # Ensure the upload directory exists with proper permissions
        if self.image:
            # Ensure MEDIA_ROOT exists
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT, mode=0o755, exist_ok=True)
            
            # Ensure product_images subdirectory exists
            upload_path = os.path.join(settings.MEDIA_ROOT, 'product_images')
            os.makedirs(upload_path, mode=0o755, exist_ok=True)
        
        # If this image is being set as primary, unset all other primary images for this product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

class ProductComment(models.Model):
    """
    Comments on products
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_comments')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating from 1 to 5 stars")
    is_approved = models.BooleanField(default=False, help_text="Comment must be approved by admin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For nested comments (replies)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.product.name}'

class LabelGroup(models.Model):
    """Group for organizing labels (e.g., Industry, Size, Status)"""
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    subcategories = models.ManyToManyField(
        Subcategory,
        related_name='label_groups',
        blank=True,
        help_text='Assign this group to subcategories; leave empty to keep it global.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Label Group'
        verbose_name_plural = 'Label Groups'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def is_global(self):
        return not self.subcategories.exists()

    def applies_to_subcategory(self, subcategory_id: Optional[int]):
        if not subcategory_id:
            return True
        if self.is_global():
            return True
        return self.subcategories.filter(id=subcategory_id).exists()

    def get_labels_for_subcategory(self, subcategory_id: Optional[int]):
        """
        Return labels that should be displayed for `subcategory_id`.
        Global labels always show; others must explicitly attach to the subcategory.
        """
        labels = self.labels.filter(is_active=True)
        if not subcategory_id:
            return labels
        return labels.filter(
            models.Q(subcategories__id=subcategory_id) | models.Q(subcategories__isnull=True)
        ).distinct()


class Label(models.Model):
    """Product label for filtering, badges, and SEO landing pages"""
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    # Optional scoping by catalog hierarchy
    departments = models.ManyToManyField(
        Department,
        related_name='labels',
        blank=True,
        help_text='Limit this label to specific departments (leave empty for all departments).'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='labels',
        blank=True,
        help_text='Limit this label to specific categories (leave empty for all categories).'
    )
    label_group = models.ForeignKey(
        LabelGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='labels'
    )
    subcategories = models.ManyToManyField(Subcategory, related_name='labels', blank=True)
    color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text='Hex color code for badge (include #)'
    )
    
    # Type flags
    is_promotional = models.BooleanField(default=False)
    is_filterable = models.BooleanField(default=True)
    is_seo_page = models.BooleanField(
        default=False,
        help_text='Controls whether this label gets a dedicated landing page'
    )
    
    # SEO fields
    seo_title = models.CharField(max_length=70, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)
    seo_h1 = models.CharField(max_length=140, blank=True, null=True)
    seo_intro_text = models.TextField(blank=True, null=True)
    seo_faq = models.JSONField(
        blank=True,
        null=True,
        help_text='Optional FAQ JSON array (list of {"question": "", "answer": ""})'
    )
    og_image = models.ImageField(
        upload_to='label_og_images/',
        blank=True,
        null=True,
        help_text='OpenGraph image for SEO pages'
    )
    canonical_url = models.URLField(max_length=500, blank=True, null=True, help_text="Canonical URL for SEO")
    schema_markup = models.TextField(
        blank=True,
        null=True,
        help_text='Optional JSON-LD markup'
    )
    image_alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for the image (for SEO and accessibility)")
    
    # Meta
    product_count = models.PositiveIntegerField(default=0)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def update_product_count(self):
        """Update the cached product count"""
        self.product_count = self.products.filter(is_active=True).count()
        self.save(update_fields=['product_count'])

    def applies_to_subcategory(self, subcategory_id: Optional[int]):
        if not subcategory_id:
            return True
        if not self.subcategories.exists():
            return True
        return self.subcategories.filter(id=subcategory_id).exists()

    def is_global(self) -> bool:
        """Return True when the label applies to every subcategory."""
        return not self.subcategories.exists()

    def is_relevant_for_subcategory(self, subcategory_id: Optional[int]) -> bool:
        if not subcategory_id:
            return True
        if self.is_global():
            return True
        return self.subcategories.filter(id=subcategory_id).exists()

    def get_breadcrumb_hierarchy(self):
        """Return breadcrumb data for SEO pages"""
        breadcrumbs = [
            {'type': 'home', 'name': 'Home', 'slug': '/'},
            {'type': 'products', 'name': 'Products', 'slug': '/products'},
        ]
        if self.label_group:
            breadcrumbs.append({
                'type': 'label_group',
                'name': self.label_group.name,
                'slug': self.label_group.slug
            })
        breadcrumbs.append({
            'type': 'label',
            'name': self.name,
            'slug': self.slug
        })
        return breadcrumbs


class LabelComboSeoPage(models.Model):
    """SEO page for combination of multiple labels"""
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=180, unique=True)
    labels = models.ManyToManyField(Label, related_name='combo_pages')
    
    # SEO fields
    seo_title = models.CharField(max_length=70, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)
    seo_h1 = models.CharField(max_length=140, blank=True, null=True)
    seo_intro_text = models.TextField(blank=True, null=True)
    seo_faq = models.JSONField(
        blank=True,
        null=True,
        help_text='FAQ entries for combo page'
    )
    og_image = models.ImageField(
        upload_to='label_combo_og_images/',
        blank=True,
        null=True
    )
    schema_markup = models.TextField(blank=True, null=True)
    
    # Meta
    is_indexable = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Label Combo SEO Page'
        verbose_name_plural = 'Label Combo SEO Pages'

    def __str__(self):
        return self.name

    def get_filtered_products(self):
        """Return products that match ALL labels in this combo"""
        label_ids = list(self.labels.values_list('id', flat=True))
        if not label_ids:
            return Product.objects.none()
        
        # Get products that have ALL the labels
        products = Product.objects.filter(is_active=True, is_marketplace_hidden=False)
        for label_id in label_ids:
            products = products.filter(labels__id=label_id)
        
        return products.distinct()


# Add labels field to Product model after Label is defined
Product.add_to_class(
    'labels',
    models.ManyToManyField(Label, related_name='products', blank=True)
)

def get_promotional_labels(self):
    """Get promotional labels for badge display (limit 2)"""
    return self.labels.filter(
        is_promotional=True,
        is_active=True
    ).order_by('display_order')[:2]

# Add method to Product class
Product.add_to_class('get_promotional_labels', get_promotional_labels)