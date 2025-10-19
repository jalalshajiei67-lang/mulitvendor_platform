# products/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='department_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for the image (for SEO and accessibility)")
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

class Product(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')  # Keep for backward compatibility
    supplier = models.ForeignKey('users.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='products', help_text="Company/Supplier")
    subcategories = models.ManyToManyField(Subcategory, related_name='products', blank=True)  # Changed from ForeignKey
    primary_category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True, help_text="Primary category for breadcrumb display")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Keep for backward compatibility
    image_alt_text = models.CharField(max_length=125, blank=True, null=True, help_text="Alt text for the main image (for SEO and accessibility)")
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    canonical_url = models.URLField(max_length=500, blank=True, null=True, help_text="Canonical URL for SEO")
    schema_markup = models.TextField(blank=True, null=True, help_text="JSON-LD Schema markup for rich snippets")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Auto-draft products without a primary category
        if not self.primary_category:
            self.is_active = False
        
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

class ScrapeJobBatch(models.Model):
    """
    Represents a batch scraping session (multiple URLs submitted together)
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('completed_with_errors', 'Completed with Errors'),
    ]
    
    name = models.CharField(max_length=200, blank=True, null=True, help_text="Optional name for this batch")
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scrape_batches')
    supplier = models.ForeignKey('users.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='scrape_batches')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    
    # Statistics
    total_urls = models.PositiveIntegerField(default=0)
    completed_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Report data
    report_data = models.JSONField(blank=True, null=True, help_text="Complete batch report in JSON")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Scrape Job Batch'
        verbose_name_plural = 'Scrape Job Batches'
    
    def __str__(self):
        name = self.name or f"Batch #{self.id}"
        return f"{name} - {self.total_urls} URLs ({self.status})"
    
    @property
    def success_rate(self):
        """Calculate success rate percentage"""
        if self.total_urls == 0:
            return 0
        return round((self.completed_count / self.total_urls) * 100, 1)
    
    @property
    def duration(self):
        """Calculate how long the batch took"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds()
        return None
    
    @property
    def is_complete(self):
        """Check if batch is complete"""
        return self.status in ['completed', 'completed_with_errors']
    
    def update_statistics(self):
        """Update statistics from related scrape jobs"""
        jobs = self.jobs.all()
        self.total_urls = jobs.count()
        self.completed_count = jobs.filter(status__in=['completed', 'completed_with_warnings']).count()
        self.failed_count = jobs.filter(status='failed').count()
        
        # Update status
        processing = jobs.filter(status__in=['pending', 'processing']).count()
        if processing == 0:
            self.status = 'completed_with_errors' if self.failed_count > 0 else 'completed'
            if not self.completed_at:
                self.completed_at = timezone.now()
        else:
            self.status = 'processing'
        
        self.save()
    
    def generate_report(self):
        """Generate comprehensive batch report"""
        jobs = self.jobs.all().order_by('created_at')
        
        successful_jobs = []
        failed_jobs = []
        warning_jobs = []
        
        for job in jobs:
            job_data = {
                'id': job.id,
                'url': job.url,
                'status': job.status,
                'created_at': job.created_at.isoformat(),
                'processed_at': job.processed_at.isoformat() if job.processed_at else None,
            }
            
            if job.status in ['completed', 'completed_with_warnings']:
                job_data['product_id'] = job.created_product.id if job.created_product else None
                job_data['product_name'] = job.created_product.name if job.created_product else None
                
                if job.status == 'completed_with_warnings':
                    job_data['warnings'] = job.warning_count
                    warning_jobs.append(job_data)
                else:
                    successful_jobs.append(job_data)
            else:
                job_data['error'] = job.error_message
                failed_jobs.append(job_data)
        
        report = {
            'batch_id': self.id,
            'batch_name': self.name or f"Batch #{self.id}",
            'summary': {
                'total_urls': self.total_urls,
                'completed': self.completed_count,
                'failed': self.failed_count,
                'success_rate': self.success_rate,
                'duration_seconds': self.duration,
            },
            'timing': {
                'created_at': self.created_at.isoformat(),
                'started_at': self.started_at.isoformat() if self.started_at else None,
                'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            },
            'successful_jobs': successful_jobs,
            'warning_jobs': warning_jobs,
            'failed_jobs': failed_jobs,
        }
        
        self.report_data = report
        self.save()
        
        return report


class ProductScrapeJob(models.Model):
    """
    Model to manage individual product scraping jobs with robust error tracking
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('completed_with_warnings', 'Completed with Warnings'),
        ('failed', 'Failed'),
    ]
    
    batch = models.ForeignKey(ScrapeJobBatch, on_delete=models.CASCADE, null=True, blank=True, related_name='jobs', help_text="Batch this job belongs to")
    url = models.URLField(max_length=500, help_text="URL of the product page to scrape")
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scrape_jobs', help_text="Vendor who requested the scrape")
    supplier = models.ForeignKey('users.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='scrape_jobs', help_text="Supplier/Company for this product")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True, help_text="Primary error message if scraping failed")
    error_details = models.JSONField(blank=True, null=True, help_text="Detailed error information from error handler")
    created_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='scrape_job', help_text="Product created from this scrape job")
    
    # Scraped data (stored before creating product)
    scraped_data = models.JSONField(blank=True, null=True, help_text="Raw scraped data in JSON format")
    
    # Retry tracking
    retry_count = models.PositiveIntegerField(default=0, help_text="Number of times this job has been retried")
    last_retry_at = models.DateTimeField(null=True, blank=True, help_text="When the last retry occurred")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True, help_text="When the scraping was processed")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product Scrape Job'
        verbose_name_plural = 'Product Scrape Jobs'
    
    def __str__(self):
        return f"Scrape Job #{self.id} - {self.url[:50]} ({self.status})"
    
    @property
    def has_warnings(self):
        """Check if job has warnings"""
        if self.scraped_data and 'scraping_metadata' in self.scraped_data:
            return self.scraped_data['scraping_metadata'].get('warnings_count', 0) > 0
        return False
    
    @property
    def warning_count(self):
        """Get number of warnings"""
        if self.scraped_data and 'scraping_metadata' in self.scraped_data:
            return self.scraped_data['scraping_metadata'].get('warnings_count', 0)
        return 0