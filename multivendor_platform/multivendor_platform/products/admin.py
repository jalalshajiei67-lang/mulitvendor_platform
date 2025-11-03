# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.contrib import messages
from django.utils import timezone
from tinymce.widgets import TinyMCE
from .models import Department, Category, Subcategory, Product, ProductImage, ProductComment, ProductScrapeJob, ScrapeJobBatch
from .scraper import WordPressScraper
from .universal_scraper import UniversalProductScraper, create_product_from_scraped_data
import threading

# Custom widget for multiple file uploads
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    
    def __init__(self, attrs=None):
        default_attrs = {'multiple': True, 'accept': 'image/*'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        return None  # Don't show existing files in multiple file input

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductAdminForm(forms.ModelForm):
    multiple_images = MultipleFileField(
        required=False,
        help_text="📁 Click 'Choose Files' and select multiple images at once (hold Ctrl/Cmd to select multiple files). Maximum 20 images allowed."
    )
    
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Product description with rich text formatting"
    )
    
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Show existing images count
            existing_count = self.instance.images.count()
            self.fields['multiple_images'].help_text = f"Select additional images to upload (current: {existing_count}/20)"
    
    def clean_multiple_images(self):
        # Get files from both cleaned_data and request.FILES
        files = self.cleaned_data.get('multiple_images', [])
        
        # Also check request.FILES for multiple_images
        if hasattr(self, 'data') and hasattr(self.data, 'getlist'):
            request_files = self.data.getlist('multiple_images')
            if request_files:
                files = request_files
        
        if not files:
            return files
            
        if not isinstance(files, list):
            files = [files]
            
        # Filter out empty files
        files = [f for f in files if f and hasattr(f, 'name')]
        
        if not files:
            return []
            
        # Check if adding these files would exceed the limit
        existing_count = 0
        if self.instance and self.instance.pk:
            existing_count = self.instance.images.count()
        
        if existing_count + len(files) > 20:
            raise forms.ValidationError(f"Maximum 20 images allowed. You have {existing_count} existing images and trying to add {len(files)} more.")
        
        # Validate file types
        for file in files:
            if hasattr(file, 'content_type') and not file.content_type.startswith('image/'):
                raise forms.ValidationError(f"File {file.name} is not an image.")
    
        return files
    
    def save(self, commit=True):
        instance = super().save(commit=commit)
        
        if commit:
            # Handle multiple images from form data
            multiple_images = self.cleaned_data.get('multiple_images', [])
            if multiple_images:
                if not isinstance(multiple_images, list):
                    multiple_images = [multiple_images]
                    
                existing_count = instance.images.count()
                has_primary = instance.images.filter(is_primary=True).exists()
                
                for i, file in enumerate(multiple_images):
                    if file:  # Make sure file exists
                        # Only set as primary if no existing images and this is the first new image
                        is_primary = (existing_count == 0 and i == 0 and not has_primary)
                        
                        # Create ProductImage instance
                        product_image = ProductImage(
                            product=instance,
                            image=file,
                            is_primary=is_primary,
                            sort_order=existing_count + i
                        )
                        product_image.save()
        
        return instance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['delete_selected']  # Explicitly include delete action
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image', 'image_alt_text')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Search Engine Optimization fields'
        }),
        ('Settings', {
            'fields': ('is_active', 'sort_order')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/custom_admin.css', 'admin/css/force_action_button.css',)
        }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_departments', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'departments', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['departments', 'subcategories']
    actions = ['delete_selected']  # Explicitly include delete action
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image', 'image_alt_text')
        }),
        ('Relationships', {
            'fields': ('departments', 'subcategories'),
            'description': 'Categories can belong to multiple departments and have multiple subcategories'
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Search Engine Optimization fields'
        }),
        ('Settings', {
            'fields': ('is_active', 'sort_order')
        }),
    )
    
    def get_departments(self, obj):
        """Get departments with error handling"""
        try:
            depts = obj.departments.all()
            if depts.exists():
                return ', '.join([dept.name for dept in depts])
            return 'None'
        except Exception as e:
            return f'Error: {str(e)}'
    get_departments.short_description = 'Departments'
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/custom_admin.css', 'admin/css/force_action_button.css',)
        }

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_departments', 'get_categories', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'categories', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['categories']
    actions = ['delete_selected']  # Explicitly include delete action
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image', 'image_alt_text')
        }),
        ('Relationships', {
            'fields': ('categories',),
            'description': 'Subcategories belong to categories (departments are inferred through categories)'
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Search Engine Optimization fields'
        }),
        ('Settings', {
            'fields': ('is_active', 'sort_order')
        }),
    )
    
    def get_departments(self, obj):
        """Get departments through categories with error handling"""
        try:
            departments = obj.get_departments()
            if departments:
                return ', '.join([dept.name for dept in departments])
            return 'None'
        except Exception as e:
            return f'Error: {str(e)}'
    get_departments.short_description = 'Departments (via Categories)'
    
    def get_categories(self, obj):
        """Get categories with error handling"""
        try:
            cats = obj.categories.all()
            if cats.exists():
                return ', '.join([cat.name for cat in cats])
            return 'None'
        except Exception as e:
            return f'Error: {str(e)}'
    get_categories.short_description = 'Categories'
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/custom_admin.css', 'admin/css/force_action_button.css',)
        }

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 20
    fields = ['image_thumbnail', 'image', 'alt_text', 'is_primary', 'sort_order']
    readonly_fields = ['image_thumbnail', 'created_at', 'updated_at']
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-is_primary', 'sort_order', 'created_at')
    
    class Media:
        js = ('admin/js/product_images.js',)
        css = {
            'all': ('admin/css/product_images.css',)
        }

class ProductCommentInline(admin.TabularInline):
    model = ProductComment
    extra = 0
    fields = ['author', 'content', 'rating', 'is_approved', 'parent', 'created_at']
    readonly_fields = ['author', 'created_at']
    can_delete = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'slug', 'vendor', 'supplier', 'primary_category', 'get_subcategories', 'get_category_path', 'price', 'stock', 'image_count', 'comment_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'primary_category', 'subcategories', 'created_at']
    search_fields = ['name', 'description', 'vendor__username', 'vendor__email']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['subcategories']
    inlines = [ProductImageInline, ProductCommentInline]
    actions = ['make_active', 'make_inactive', 'delete_selected']  # Enable bulk actions with delete
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image', 'image_alt_text')
        }),
        ('Multiple Images Upload', {
            'fields': ('multiple_images',),
            'description': '🚀 Upload multiple images at once! Click "Choose Files" and select multiple images (hold Ctrl/Cmd to select multiple). Maximum 20 images total. Alt text can be added to each image in the "Product images" section below.'
        }),
        ('Category, Supplier & Vendor', {
            'fields': ('supplier', 'subcategories', 'primary_category', 'vendor')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Search Engine Optimization fields'
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )
    
    def get_subcategories(self, obj):
        """Get subcategories as comma-separated string with error handling"""
        try:
            subcats = obj.subcategories.all()
            if subcats.exists():
                return ', '.join([subcat.name for subcat in subcats])
            return 'None'
        except Exception as e:
            return f'Error: {str(e)}'
    get_subcategories.short_description = 'Subcategories'
    
    def get_category_path(self, obj):
        """Get full category path with error handling"""
        try:
            if hasattr(obj, 'get_full_category_path'):
                # It's a property, not a method
                return obj.get_full_category_path or 'N/A'
            return 'N/A'
        except Exception as e:
            return f'Error: {str(e)}'
    get_category_path.short_description = 'Category Path'
    
    def image_count(self, obj):
        """Count images with error handling"""
        try:
            count = obj.images.count()
            if count > 0:
                primary_img = obj.primary_image
                if primary_img:
                    try:
                        return format_html(
                            '<span style="color: green;">{}/20</span> <br>'
                            '<img src="{}" style="max-width: 50px; max-height: 50px; border-radius: 4px;" />',
                            count, primary_img.url
                        )
                    except:
                        # If image URL fails, just show count
                        return format_html('<span style="color: green;">{}/20</span>', count)
            return format_html('<span style="color: red;">{}/20</span>', count)
        except Exception as e:
            return format_html('<span style="color: orange;">Error</span>')
    image_count.short_description = 'Images'
    
    def comment_count(self, obj):
        """Count comments with error handling"""
        try:
            count = obj.comments.count()
            approved = obj.comments.filter(is_approved=True).count()
            return format_html(
                '<span style="color: {};">{} ({} approved)</span>',
                'green' if approved > 0 else 'gray',
                count, approved
            )
        except Exception as e:
            return format_html('<span style="color: orange;">Error</span>')
    comment_count.short_description = 'Comments'
    
    # Bulk actions
    def make_active(self, request, queryset):
        """Mark selected products as active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} product(s) marked as active.')
    make_active.short_description = "✅ Mark as Active"
    
    def make_inactive(self, request, queryset):
        """Mark selected products as inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} product(s) marked as inactive.')
    make_inactive.short_description = "❌ Mark as Inactive"
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    def save_model(self, request, obj, form, change):
        """Override save_model to handle multiple images"""
        super().save_model(request, obj, form, change)
        
        # Handle multiple images upload
        if hasattr(request, 'FILES'):
            files = request.FILES.getlist('multiple_images')
            if files:
                existing_count = obj.images.count()
                has_primary = obj.images.filter(is_primary=True).exists()
                
                for i, file in enumerate(files):
                    if file and file.size > 0:  # Make sure file exists and has content
                        # Only set as primary if no existing images and this is the first new image
                        is_primary = (existing_count == 0 and i == 0 and not has_primary)
                        
                        # Create ProductImage instance
                        product_image = ProductImage(
                            product=obj,
                            image=file,
                            is_primary=is_primary,
                            sort_order=existing_count + i
                        )
                        product_image.save()
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/custom_admin.css', 'admin/css/force_action_button.css',)
        }

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'author', 'content_preview', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['content', 'author__username', 'product__name']
    readonly_fields = ['author', 'product', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('product', 'author', 'content', 'rating')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'parent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} comments disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'


# Scraper Forms and Admin
class BulkScrapeForm(forms.Form):
    """
    Form for bulk URL scraping
    """
    urls = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 80,
            'placeholder': 'Enter product URLs (one per line)\nExample:\nhttps://example.com/product/item-1\nhttps://example.com/product/item-2'
        }),
        label='Product URLs',
        help_text='Enter one URL per line. Each URL will be scraped and queued for product creation.'
    )
    supplier = forms.ModelChoiceField(
        queryset=None,
        required=False,
        help_text='Optional: Select a supplier/company for all scraped products'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from users.models import Supplier
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True)
    
    def clean_urls(self):
        urls_text = self.cleaned_data['urls']
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        if not urls:
            raise forms.ValidationError("Please enter at least one URL")
        
        # Validate URLs
        from django.core.validators import URLValidator
        validator = URLValidator()
        
        valid_urls = []
        for url in urls:
            try:
                validator(url)
                valid_urls.append(url)
            except forms.ValidationError:
                raise forms.ValidationError(f"Invalid URL: {url}")
        
        return valid_urls


def process_scrape_job(job_id):
    """
    Background function to process a scrape job with robust error handling
    IMPORTANT: Continues processing even if one job fails (for batch processing)
    """
    import json
    from .scraper_error_handler import ErrorHandler
    
    job = None
    try:
        job = ProductScrapeJob.objects.get(id=job_id)
        job.status = 'processing'
        job.save()
        
        scraped_data = None
        scraper = None
        
        # Try scraping with multiple fallback strategies
        scraped_data = None
        attempts = [
            {'verify_ssl': True, 'use_proxy': False, 'desc': 'SSL verified, no proxy'},
            {'verify_ssl': False, 'use_proxy': False, 'desc': 'SSL disabled, no proxy'},
            {'verify_ssl': True, 'use_proxy': True, 'desc': 'SSL verified, with proxy'},
            {'verify_ssl': False, 'use_proxy': True, 'desc': 'SSL disabled, with proxy'},
        ]
        
        last_error = None
        for attempt in attempts:
            try:
                # Use Universal Scraper - works with ALL e-commerce platforms
                scraper = UniversalProductScraper(
                    job.url, 
                    verify_ssl=attempt['verify_ssl'],
                    use_proxy=attempt['use_proxy']
                )
                scraped_data = scraper.scrape()
                
                # If successful, log which method worked
                if not attempt['verify_ssl'] or not attempt['use_proxy']:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.info(f"Scraping succeeded with: {attempt['desc']}")
                
                break  # Success! Exit the loop
            except Exception as e:
                last_error = e
                # Check if it's a proxy error
                if 'PROXY' in str(e).upper() or 'proxy' in str(e).lower():
                    # Skip to non-proxy attempts
                    continue
                # Check if it's SSL error  
                elif 'SSL' in str(e) or 'CERTIFICATE' in str(e).upper():
                    # Try next attempt
                    continue
                else:
                    # For other errors, continue trying
                    continue
        
        # If all attempts failed, raise the last error
        if scraped_data is None:
            raise last_error if last_error else Exception("All scraping attempts failed")
        
        # Store scraped data
        job.scraped_data = scraped_data
        
        # Check if there were warnings during scraping
        has_warnings = False
        if scraped_data and 'scraping_metadata' in scraped_data:
            metadata = scraped_data['scraping_metadata']
            has_warnings = metadata.get('warnings_count', 0) > 0
            
            # Store detailed error information
            if metadata.get('errors'):
                job.error_details = metadata['errors']
        
        job.save()
        
        # Create product from scraped data
        product, error = create_product_from_scraped_data(
            scraped_data,
            vendor=job.vendor,
            supplier=job.supplier
        )
        
        if product:
            job.created_product = product
            # Set status based on whether there were warnings
            job.status = 'completed_with_warnings' if has_warnings else 'completed'
            job.processed_at = timezone.now()
            job.save()
        else:
            job.status = 'failed'
            job.error_message = error or "Unknown error occurred while creating product"
            job.save()
    
    except Exception as e:
        try:
            if not job:
                job = ProductScrapeJob.objects.get(id=job_id)
            job.status = 'failed'
            job.error_message = str(e)
            
            # Try to get error details from scraper if available
            if 'scraper' in locals() and scraper and hasattr(scraper, 'error_handler'):
                job.error_details = scraper.error_handler.get_error_report()
            
            job.save()
        except Exception as save_error:
            # Log the error but don't raise - continue processing other jobs
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to save error state for job {job_id}: {str(save_error)}")
    
    finally:
        # Update batch statistics if this job belongs to a batch
        try:
            if job and job.batch:
                job.batch.update_statistics()
                # Generate report if batch is complete
                if job.batch.is_complete:
                    job.batch.generate_report()
        except Exception as batch_error:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to update batch statistics: {str(batch_error)}")


@admin.register(ScrapeJobBatch)
class ScrapeJobBatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'batch_name_display', 'vendor', 'supplier', 'total_urls', 'progress_display', 'success_rate_display', 'status_display_batch', 'created_at', 'duration_display']
    list_filter = ['status', 'created_at', 'supplier']
    search_fields = ['name', 'vendor__username']
    readonly_fields = ['total_urls', 'completed_count', 'failed_count', 'created_at', 'started_at', 'completed_at', 'report_data']
    
    fieldsets = (
        ('Batch Information', {
            'fields': ('name', 'vendor', 'supplier', 'status')
        }),
        ('Statistics', {
            'fields': ('total_urls', 'completed_count', 'failed_count')
        }),
        ('Timing', {
            'fields': ('created_at', 'started_at', 'completed_at')
        }),
        ('Report', {
            'fields': ('report_data',),
            'classes': ('collapse',),
            'description': 'Detailed batch report in JSON format'
        }),
    )
    
    actions = ['generate_reports', 'retry_failed_in_batch', 'export_report_csv']
    
    def batch_name_display(self, obj):
        name = obj.name or f"Batch #{obj.id}"
        return format_html('<strong>{}</strong>', name)
    batch_name_display.short_description = 'Batch Name'
    
    def progress_display(self, obj):
        completed = obj.completed_count
        failed = obj.failed_count
        total = obj.total_urls
        
        return format_html(
            '<span style="color: #28a745;">✓ {}</span> / '
            '<span style="color: #dc3545;">✗ {}</span> / '
            '<span style="color: #666;">Total: {}</span>',
            completed, failed, total
        )
    progress_display.short_description = 'Progress'
    
    def success_rate_display(self, obj):
        rate = obj.success_rate
        color = '#28a745' if rate >= 80 else '#ffc107' if rate >= 50 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, rate
        )
    success_rate_display.short_description = 'Success Rate'
    
    def status_display_batch(self, obj):
        status_colors = {
            'pending': '#FFA500',
            'processing': '#0066CC',
            'completed': '#28a745',
            'completed_with_errors': '#FFC107',
        }
        color = status_colors.get(obj.status, '#999')
        icon = {
            'completed': '✓',
            'completed_with_errors': '⚠️',
            'processing': '⏳',
            'pending': '⏱️'
        }.get(obj.status, '')
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, obj.status.replace('_', ' ').upper()
        )
    status_display_batch.short_description = 'Status'
    
    def duration_display(self, obj):
        if obj.duration:
            minutes = int(obj.duration // 60)
            seconds = int(obj.duration % 60)
            return f"{minutes}m {seconds}s"
        return "-"
    duration_display.short_description = 'Duration'
    
    def generate_reports(self, request, queryset):
        """Generate reports for selected batches"""
        count = 0
        for batch in queryset:
            batch.update_statistics()
            batch.generate_report()
            count += 1
        self.message_user(request, f'✅ Generated reports for {count} batch(es).', level=messages.SUCCESS)
    generate_reports.short_description = '📊 Generate Reports'
    
    def retry_failed_in_batch(self, request, queryset):
        """Retry only failed jobs in selected batches"""
        total_retried = 0
        for batch in queryset:
            failed_jobs = batch.jobs.filter(status='failed')
            for job in failed_jobs:
                job.status = 'pending'
                job.error_message = None
                job.error_details = None
                job.retry_count += 1
                job.last_retry_at = timezone.now()
                job.save()
                
                # Process in background
                thread = threading.Thread(target=process_scrape_job, args=(job.id,))
                thread.daemon = True
                thread.start()
                total_retried += 1
            
            # Reset batch status
            if failed_jobs.exists():
                batch.status = 'processing'
                batch.save()
        
        self.message_user(request, f'🔄 {total_retried} failed job(s) queued for retry.', level=messages.SUCCESS)
    retry_failed_in_batch.short_description = '🔄 Retry Failed Jobs Only'
    
    def export_report_csv(self, request, queryset):
        """Export batch reports as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scrape_reports_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Batch ID', 'Batch Name', 'Total URLs', 'Completed', 'Failed', 'Success Rate', 'Duration', 'Created At', 'Completed At'])
        
        for batch in queryset:
            batch.update_statistics()
            writer.writerow([
                batch.id,
                batch.name or f"Batch #{batch.id}",
                batch.total_urls,
                batch.completed_count,
                batch.failed_count,
                f"{batch.success_rate}%",
                f"{batch.duration}s" if batch.duration else "N/A",
                batch.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                batch.completed_at.strftime('%Y-%m-%d %H:%M:%S') if batch.completed_at else "N/A",
            ])
        
        return response
    export_report_csv.short_description = '📥 Export Reports as CSV'
    
    def get_urls(self):
        """Add custom URLs for batch reporting"""
        from django.urls import path
        urls = super().get_urls()
        # Custom URLs must come BEFORE default URLs to be matched first
        custom_urls = [
            path('<int:batch_id>/report/', self.admin_site.admin_view(self.batch_report_view), name='products_scrapejobatch_report'),
            path('<int:batch_id>/retry-failed/', self.admin_site.admin_view(self.retry_failed_view), name='products_scrapejobatch_retry_failed'),
        ]
        return custom_urls + urls
    
    def batch_report_view(self, request, batch_id):
        """View detailed batch report"""
        from django.shortcuts import get_object_or_404
        from django.core.exceptions import PermissionDenied
        from django.http import Http404
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Check permissions
        if not request.user.is_staff:
            raise PermissionDenied
        
        try:
            batch = get_object_or_404(ScrapeJobBatch, id=batch_id)
            batch.update_statistics()
            report = batch.generate_report()
            
            context = {
                'title': f'Batch Report: {batch.name or f"Batch #{batch_id}"}',
                'batch': batch,
                'report': report,
                'opts': self.model._meta,
                'has_permission': True,
            }
            return render(request, 'admin/products/batch_report.html', context)
        except ScrapeJobBatch.DoesNotExist:
            logger.error(f"Batch #{batch_id} not found")
            messages.error(request, f"Batch #{batch_id} not found.")
            return redirect(reverse('admin:products_scrapejobbatch_changelist'))
        except Exception as e:
            logger.error(f"Error generating batch report for batch {batch_id}: {str(e)}")
            messages.error(request, f"Error generating report: {str(e)}")
            return redirect(reverse('admin:products_scrapejobbatch_changelist'))
    
    def retry_failed_view(self, request, batch_id):
        """Retry only failed jobs in a specific batch"""
        batch = ScrapeJobBatch.objects.get(id=batch_id)
        failed_jobs = batch.jobs.filter(status='failed')
        
        count = 0
        for job in failed_jobs:
            job.status = 'pending'
            job.error_message = None
            job.error_details = None
            job.retry_count += 1
            job.last_retry_at = timezone.now()
            job.save()
            
            # Process in background
            thread = threading.Thread(target=process_scrape_job, args=(job.id,))
            thread.daemon = True
            thread.start()
            count += 1
        
        batch.status = 'processing'
        batch.save()
        
        messages.success(request, f'🔄 {count} failed job(s) queued for retry.')
        return redirect(reverse('admin:products_scrapejobbatch_changelist'))


@admin.register(ProductScrapeJob)
class ProductScrapeJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'batch_link', 'url_preview', 'vendor', 'supplier', 'status_display', 'retry_info', 'created_product_link', 'created_at', 'processed_at']
    list_filter = ['status', 'batch', 'created_at', 'supplier']
    search_fields = ['url', 'vendor__username', 'error_message']
    readonly_fields = ['batch', 'scraped_data', 'created_product', 'processed_at', 'created_at', 'updated_at', 'display_errors_formatted', 'retry_count', 'last_retry_at']
    
    fieldsets = (
        ('Job Information', {
            'fields': ('url', 'batch', 'vendor', 'supplier', 'status')
        }),
        ('Results', {
            'fields': ('created_product', 'error_message', 'processed_at'),
            'description': 'Product creation results and primary error message'
        }),
        ('Error Details & Warnings', {
            'fields': ('display_errors_formatted',),
            'description': 'Detailed error and warning information from the scraper with suggestions'
        }),
        ('Retry Information', {
            'fields': ('retry_count', 'last_retry_at'),
            'classes': ('collapse',),
        }),
        ('Scraped Data', {
            'fields': ('scraped_data',),
            'classes': ('collapse',),
            'description': 'Raw scraped data in JSON format including metadata'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['retry_failed_jobs', 'process_pending_jobs']
    
    def batch_link(self, obj):
        """Display link to batch if job belongs to one"""
        if obj.batch:
            url = reverse('admin:products_scrapejobatch_report', args=[obj.batch.id])
            return format_html(
                '<a href="{}" style="color: #667eea; font-weight: 500;">📊 Batch #{}</a>',
                url, obj.batch.id
            )
        return format_html('<span style="color: #999;">-</span>')
    batch_link.short_description = 'Batch'
    
    def url_preview(self, obj):
        max_length = 60
        url = obj.url if len(obj.url) <= max_length else obj.url[:max_length] + '...'
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, url)
    url_preview.short_description = 'URL'
    
    def status_display(self, obj):
        """Display status with error message and warnings"""
        status_colors = {
            'pending': '#FFA500',
            'processing': '#0066CC',
            'completed': '#28a745',
            'completed_with_warnings': '#FFC107',
            'failed': '#dc3545',
        }
        color = status_colors.get(obj.status, '#999')
        
        # Build status display
        status_text = obj.status.replace('_', ' ').upper()
        
        if obj.status == 'failed' and obj.error_message:
            # Truncate long error messages
            error_preview = obj.error_message[:150] + '...' if len(obj.error_message) > 150 else obj.error_message
            return format_html(
                '<span style="color: {}; font-weight: bold;" title="{}">{}</span><br>'
                '<small style="color: #dc3545; display: block; margin-top: 4px;">❌ {}</small>',
                color, obj.error_message, status_text, error_preview
            )
        elif obj.status == 'completed_with_warnings':
            warning_count = obj.warning_count
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span><br>'
                '<small style="color: #856404;">⚠️ {} warning(s)</small>',
                color, status_text, warning_count
            )
        else:
            icon = {
                'completed': '✓',
                'processing': '⏳',
                'pending': '⏱️'
            }.get(obj.status, '')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} {}</span>',
                color, icon, status_text
            )
    status_display.short_description = 'Status'
    
    def retry_info(self, obj):
        """Display retry information"""
        if obj.retry_count > 0:
            return format_html(
                '<span style="color: #666;">🔄 {} time(s)</span>',
                obj.retry_count
            )
        return format_html('<span style="color: #999;">-</span>')
    retry_info.short_description = 'Retries'
    
    def created_product_link(self, obj):
        if obj.created_product:
            url = f'/admin/products/product/{obj.created_product.id}/change/'
            return format_html(
                '<a href="{}" style="color: green;">✓ Product #{}</a>',
                url, obj.created_product.id
            )
        return format_html('<span style="color: gray;">-</span>')
    created_product_link.short_description = 'Created Product'
    
    def display_errors_formatted(self, obj):
        """Display errors and warnings in a nicely formatted HTML view"""
        import json
        
        if not obj.error_details:
            return format_html(
                '<div style="padding: 15px; background: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px;">'
                '<strong style="color: #2e7d32;">✓ No errors recorded</strong>'
                '</div>'
            )
        
        try:
            # Parse error_details - it could be from scraping_metadata or direct error list
            if isinstance(obj.error_details, str):
                error_data = json.loads(obj.error_details)
            else:
                error_data = obj.error_details
            
            # Extract errors and warnings
            errors = []
            warnings = []
            summary = ""
            platform = "Unknown"
            should_retry = False
            
            # Handle different error_details structures
            if isinstance(error_data, dict):
                # From scraping_metadata structure
                errors = error_data.get('errors', [])
                warnings = error_data.get('warnings', [])
                summary = error_data.get('summary', '')
                should_retry = error_data.get('should_retry', False)
                platform = error_data.get('platform_detected', 'Unknown')
            elif isinstance(error_data, list):
                # Direct error list
                errors = error_data
            
            html_parts = []
            
            # Header with summary
            html_parts.append(
                '<div style="padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px; margin-bottom: 15px;">'
                f'<strong>Platform Detected:</strong> <span style="color: #667eea;">{platform}</span><br>'
                f'<strong>Should Retry:</strong> <span style="color: {"#28a745" if should_retry else "#dc3545"};">{"Yes" if should_retry else "No"}</span>'
                '</div>'
            )
            
            # Display errors
            if errors:
                html_parts.append('<h3 style="color: #dc3545; margin-top: 20px;">Errors ({0})</h3>'.format(len(errors)))
                
                severity_colors = {
                    'critical': '#dc3545',
                    'high': '#fd7e14',
                    'medium': '#ffc107',
                    'low': '#17a2b8'
                }
                
                severity_icons = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🔵'
                }
                
                for i, error in enumerate(errors):
                    severity = error.get('severity', 'medium')
                    color = severity_colors.get(severity, '#999')
                    icon = severity_icons.get(severity, '⚠️')
                    category = error.get('category', 'unknown')
                    message = error.get('message', 'No message')
                    details = error.get('details', '')
                    suggested_action = error.get('suggested_action', '')
                    
                    html_parts.append(
                        f'<div style="margin: 10px 0; padding: 12px; background: #fff; border-left: 4px solid {color}; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">'
                        f'<div style="margin-bottom: 8px;">'
                        f'<span style="background: {color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{icon} {severity.upper()}</span> '
                        f'<span style="background: #e9ecef; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{category}</span>'
                        f'</div>'
                        f'<strong style="color: #333;">{message}</strong>'
                    )
                    
                    if details:
                        # Truncate very long details
                        display_details = details[:300] + '...' if len(details) > 300 else details
                        html_parts.append(
                            f'<div style="margin-top: 8px; padding: 8px; background: #f8f9fa; border-radius: 3px; font-size: 12px; color: #666;">'
                            f'{display_details}'
                            f'</div>'
                        )
                    
                    if suggested_action:
                        html_parts.append(
                            f'<div style="margin-top: 8px; padding: 8px; background: #d4edda; border-left: 3px solid #28a745; border-radius: 3px;">'
                            f'<strong style="color: #155724;">💡 Suggestion:</strong> {suggested_action}'
                            f'</div>'
                        )
                    
                    html_parts.append('</div>')
            
            # Display warnings
            if warnings:
                html_parts.append('<h3 style="color: #856404; margin-top: 20px;">Warnings ({0})</h3>'.format(len(warnings)))
                
                for warning in warnings[:10]:  # Limit to 10 warnings
                    message = warning.get('message', 'No message')
                    details = warning.get('details', '')
                    
                    html_parts.append(
                        '<div style="margin: 10px 0; padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">'
                        f'<strong style="color: #856404;">⚠️ {message}</strong>'
                    )
                    
                    if details:
                        html_parts.append(
                            f'<div style="margin-top: 5px; font-size: 12px; color: #856404;">{details}</div>'
                        )
                    
                    html_parts.append('</div>')
                
                if len(warnings) > 10:
                    html_parts.append(
                        f'<div style="padding: 8px; color: #856404; font-style: italic;">... and {len(warnings) - 10} more warnings</div>'
                    )
            
            # If we have a summary, display it at the end
            if summary and not errors and not warnings:
                html_parts.append(
                    f'<div style="padding: 12px; background: #f8f9fa; border-radius: 4px; margin-top: 15px;">'
                    f'<strong>Summary:</strong><br>{summary}'
                    f'</div>'
                )
            
            return format_html(''.join(html_parts))
            
        except Exception as e:
            return format_html(
                '<div style="padding: 15px; background: #f8d7da; border-left: 4px solid #dc3545; border-radius: 4px;">'
                f'<strong style="color: #721c24;">Error parsing error details:</strong> {str(e)}<br><br>'
                f'<pre style="background: #fff; padding: 10px; border-radius: 3px; overflow: auto;">{obj.error_details}</pre>'
                '</div>'
            )
    
    display_errors_formatted.short_description = 'Error Details & Warnings'
    
    def retry_failed_jobs(self, request, queryset):
        """Retry failed scrape jobs with tracking"""
        jobs = queryset.filter(status='failed')
        count = 0
        for job in jobs:
            job.status = 'pending'
            job.error_message = None
            job.error_details = None
            job.retry_count += 1
            job.last_retry_at = timezone.now()
            job.save()
            # Process in background
            thread = threading.Thread(target=process_scrape_job, args=(job.id,))
            thread.daemon = True
            thread.start()
            count += 1
        
        self.message_user(request, f'✅ {count} job(s) queued for retry.', level=messages.SUCCESS)
    retry_failed_jobs.short_description = '🔄 Retry failed jobs'
    
    def process_pending_jobs(self, request, queryset):
        """Process pending scrape jobs"""
        jobs = queryset.filter(status='pending')
        count = 0
        for job in jobs:
            # Process in background
            thread = threading.Thread(target=process_scrape_job, args=(job.id,))
            thread.daemon = True
            thread.start()
            count += 1
        
        self.message_user(request, f'{count} jobs queued for processing.')
    process_pending_jobs.short_description = 'Process pending jobs'
    
    def get_urls(self):
        """Add custom URLs for scraping features"""
        urls = super().get_urls()
        custom_urls = [
            path('bulk-scrape/', self.admin_site.admin_view(self.bulk_scrape_view), name='products_bulk_scrape'),
            path('add-scrape-jobs/', self.admin_site.admin_view(self.add_scrape_jobs_view), name='products_add_scrape_jobs'),
            path('batch-scrape/', self.admin_site.admin_view(self.batch_scrape_api), name='products_batch_scrape'),
            path('scrape-status/', self.admin_site.admin_view(self.scrape_status_api), name='products_scrape_status'),
        ]
        return custom_urls + urls
    
    def bulk_scrape_view(self, request):
        """View for bulk URL scraping"""
        if request.method == 'POST':
            form = BulkScrapeForm(request.POST)
            if form.is_valid():
                urls = form.cleaned_data['urls']
                supplier = form.cleaned_data.get('supplier')
                
                # Create scrape jobs
                jobs_created = 0
                for url in urls:
                    job = ProductScrapeJob.objects.create(
                        url=url,
                        vendor=request.user,
                        supplier=supplier,
                        status='pending'
                    )
                    
                    # Process in background thread
                    thread = threading.Thread(target=process_scrape_job, args=(job.id,))
                    thread.daemon = True
                    thread.start()
                    
                    jobs_created += 1
                
                messages.success(request, f'{jobs_created} scrape jobs created and queued for processing!')
                return redirect('admin:products_productscrapejob_changelist')
        else:
            form = BulkScrapeForm()
        
        context = {
            'form': form,
            'title': 'Bulk Product Scraper',
            'site_header': 'Product Scraper',
            'has_permission': True,
            'opts': self.model._meta,
        }
        return render(request, 'admin/products/bulk_scrape.html', context)
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist to add bulk scrape button"""
        extra_context = extra_context or {}
        extra_context['show_bulk_scrape_button'] = True
        return super().changelist_view(request, extra_context=extra_context)
    
    def add_scrape_jobs_view(self, request):
        """Enhanced batch scraping view with progress tracking"""
        from users.models import Supplier
        
        context = {
            'title': 'Add Product Scrape Jobs - Batch Processing',
            'suppliers': Supplier.objects.filter(is_active=True),
            'opts': self.model._meta,
            'has_permission': True,
        }
        return render(request, 'admin/products/add_scrape_jobs.html', context)
    
    def batch_scrape_api(self, request):
        """API endpoint for batch scraping with batch tracking and reporting"""
        import json
        from django.http import JsonResponse
        
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                urls = data.get('urls', [])
                supplier_id = data.get('supplier')
                batch_name = data.get('batch_name', '')
                
                if not urls:
                    return JsonResponse({'success': False, 'error': 'No URLs provided'})
                
                # Get supplier if provided
                supplier = None
                if supplier_id:
                    from users.models import Supplier
                    try:
                        supplier = Supplier.objects.get(id=supplier_id)
                    except Supplier.DoesNotExist:
                        pass
                
                # Create batch
                batch = ScrapeJobBatch.objects.create(
                    name=batch_name or f"Batch {timezone.now().strftime('%Y-%m-%d %H:%M')}",
                    vendor=request.user,
                    supplier=supplier,
                    total_urls=len(urls),
                    started_at=timezone.now()
                )
                
                # Create jobs linked to batch
                job_ids = []
                for url in urls:
                    job = ProductScrapeJob.objects.create(
                        batch=batch,
                        url=url,
                        vendor=request.user,
                        supplier=supplier,
                        status='pending'
                    )
                    job_ids.append(job.id)
                    
                    # Process in background - each job is independent
                    thread = threading.Thread(target=process_scrape_job, args=(job.id,))
                    thread.daemon = True
                    thread.start()
                
                return JsonResponse({
                    'success': True,
                    'batch_id': batch.id,
                    'jobs_created': len(job_ids),
                    'job_ids': job_ids
                })
                
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    def scrape_status_api(self, request):
        """API endpoint to check scraping progress with batch information"""
        from django.http import JsonResponse
        
        job_ids_str = request.GET.get('job_ids', '')
        if not job_ids_str:
            return JsonResponse({'error': 'No job IDs provided'})
        
        try:
            job_ids = [int(id) for id in job_ids_str.split(',')]
            jobs = ProductScrapeJob.objects.filter(id__in=job_ids)
            
            total = jobs.count()
            completed = jobs.filter(status__in=['completed', 'completed_with_warnings']).count()
            failed = jobs.filter(status='failed').count()
            processing = jobs.filter(status='processing').count()
            pending = jobs.filter(status='pending').count()
            
            # Get batch info if available
            batch_id = None
            batch_status = None
            first_job = jobs.first()
            if first_job and first_job.batch:
                first_job.batch.update_statistics()
                batch_id = first_job.batch.id
                batch_status = first_job.batch.status
            
            return JsonResponse({
                'total': total,
                'completed': completed,
                'failed': failed,
                'processing': processing,
                'pending': pending,
                'batch_id': batch_id,
                'batch_status': batch_status
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)})