# products/admin.py
from django.contrib.admin import site


from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.conf import settings
from django.db.models import Q
from tinymce.widgets import TinyMCE
from .models import (
    Department,
    Category,
    Subcategory,
    Product,
    ProductImage,
    ProductComment,
    ProductScrapeJob,
    ScrapeJobBatch,
    Label,
    LabelGroup,
    LabelComboSeoPage,
    CategoryRequest,
)
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
            'price': forms.NumberInput(attrs={
                'type': 'text',  # Use text type to allow formatting
                'class': 'vTextField',
                'placeholder': 'Enter price (e.g., 1,234,567)',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Show existing images count
            existing_count = self.instance.images.count()
            self.fields['multiple_images'].help_text = f"Select additional images to upload (current: {existing_count}/20)"
    
    def clean_price(self):
        """Remove thousand separators before saving"""
        price = self.cleaned_data.get('price')
        if price:
            # If price is a string with commas, remove them
            if isinstance(price, str):
                price = price.replace(',', '').strip()
                if price:
                    try:
                        return int(price)
                    except ValueError:
                        raise forms.ValidationError("Price must be a valid number.")
            # If price is already a number (int/float), convert to int
            elif isinstance(price, (int, float)):
                return int(price)
        return price
    
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

class LabelInline(admin.TabularInline):
    model = Label
    extra = 0
    fields = ['name', 'slug', 'is_active', 'is_promotional', 'is_seo_page']
    readonly_fields = ['slug']
    show_change_link = True
    can_delete = False

class LabelGroupForm(forms.ModelForm):
    subcategories = forms.ModelMultipleChoiceField(
        queryset=Subcategory.objects.filter(is_active=True),
        required=False,
        widget=FilteredSelectMultiple('subcategories', is_stacked=False)
    )

    class Meta:
        model = LabelGroup
        fields = '__all__'

@admin.register(LabelGroup)
class LabelGroupAdmin(admin.ModelAdmin):
    form = LabelGroupForm
    list_display = ['name', 'slug', 'is_active', 'display_order', 'label_count', 'get_subcategories']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'subcategories']
    search_fields = ['name']
    ordering = ['display_order', 'name']
    autocomplete_fields = ['subcategories']
    inlines = [LabelInline]
    actions = ['activate_groups', 'deactivate_groups']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'display_order', 'is_active')
        }),
        ('Subcategory Assignment', {
            'fields': ('subcategories',),
            'description': 'Leave empty for a global group. Assign specific subcategories to show this group when those subcategories are selected.'
        }),
    )

    def label_count(self, obj):
        return obj.labels.filter(is_active=True).count()
    label_count.short_description = 'Active Labels'

    def get_subcategories(self, obj):
        return ", ".join([sc.name for sc in obj.subcategories.all()]) or '-'
    get_subcategories.short_description = 'Subcategories'

    @admin.action(description='Activate selected label groups')
    def activate_groups(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} group(s) activated.')

    @admin.action(description='Deactivate selected label groups')
    def deactivate_groups(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} group(s) deactivated.')

class LabelAdminForm(forms.ModelForm):
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        widget=FilteredSelectMultiple('departments', is_stacked=False),
        help_text='اختیاری: این لیبل را به دپارتمان‌های مشخص محدود کنید.'
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        widget=FilteredSelectMultiple('categories', is_stacked=False),
        help_text='اختیاری: این لیبل را به دسته‌بندی‌های مشخص محدود کنید.'
    )
    subcategories = forms.ModelMultipleChoiceField(
        queryset=Subcategory.objects.filter(is_active=True),
        required=False,
        widget=FilteredSelectMultiple('subcategories', is_stacked=False),
        help_text='اختیاری: این لیبل را به زیرشاخه‌های مشخص محدود کنید.'
    )
    seo_faq = forms.JSONField(required=False, widget=forms.Textarea(attrs={'rows': 4}), help_text='JSON array of FAQ objects')

    class Meta:
        model = Label
        fields = '__all__'

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    form = LabelAdminForm
    list_display = ['name', 'slug', 'label_group', 'type_badges', 'get_departments', 'get_categories', 'get_subcategories', 'product_count', 'is_active']
    list_filter = ['label_group', 'is_promotional', 'is_filterable', 'is_seo_page', 'is_active', 'departments', 'categories', 'subcategories']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']
    readonly_fields = ['product_count']
    autocomplete_fields = ['departments', 'categories', 'subcategories']
    actions = ['refresh_counts', 'mark_as_seo', 'unmark_seo']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'label_group', 'description', 'color')
        }),
        ('Type & Behavior', {
            'fields': ('is_promotional', 'is_filterable', 'is_seo_page', 'display_order', 'is_active')
        }),
        ('Scope in Catalog', {
            'fields': ('departments', 'categories', 'subcategories'),
            'description': 'اگر هیچ گزینه‌ای انتخاب نشود، این لیبل برای تمام سایت در دسترس است. در غیر این صورت فقط در بخش‌های انتخاب شده نمایش داده می‌شود.'
        }),
        ('Product Data', {
            'fields': ('product_count',),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('seo_title', 'seo_description', 'seo_h1', 'seo_intro_text', 'seo_faq', 'og_image', 'canonical_url', 'image_alt_text', 'schema_markup'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Types')
    def type_badges(self, obj):
        badges = []
        if obj.is_promotional:
            badges.append('<span style="color: #1e88e5;">Promotional</span>')
        if obj.is_filterable:
            badges.append('<span style="color: #43a047;">Filterable</span>')
        if obj.is_seo_page:
            badges.append('<span style="color: #fb8c00;">SEO</span>')
        return format_html(' | '.join(badges)) if badges else '-'

    def get_departments(self, obj):
        names = [dept.name for dept in obj.departments.all()]
        return ", ".join(names) or '-'
    get_departments.short_description = 'Departments'

    def get_categories(self, obj):
        names = [cat.name for cat in obj.categories.all()]
        return ", ".join(names) or '-'
    get_categories.short_description = 'Categories'

    def get_subcategories(self, obj):
        return ", ".join([sc.name for sc in obj.subcategories.all()]) or '-'
    get_subcategories.short_description = 'Subcategories'

    @admin.action(description='Refresh product counts for selected labels')
    def refresh_counts(self, request, queryset):
        for label in queryset:
            label.update_product_count()
        self.message_user(request, f'Refreshed counts for {queryset.count()} label(s).')

    @admin.action(description='Mark selected labels as SEO pages')
    def mark_as_seo(self, request, queryset):
        updated = queryset.update(is_seo_page=True)
        self.message_user(request, f'{updated} label(s) marked as SEO pages.')

    @admin.action(description='Unmark selected labels as SEO pages')
    def unmark_seo(self, request, queryset):
        updated = queryset.update(is_seo_page=False)
        self.message_user(request, f'{updated} label(s) removed from SEO pages.')

class LabelComboSeoPageForm(forms.ModelForm):
    seo_faq = forms.JSONField(required=False, widget=forms.Textarea(attrs={'rows': 4}), help_text='FAQ JSON array')

    class Meta:
        model = LabelComboSeoPage
        fields = '__all__'

@admin.register(LabelComboSeoPage)
class LabelComboSeoPageAdmin(admin.ModelAdmin):
    form = LabelComboSeoPageForm
    list_display = ['name', 'slug', 'is_indexable', 'labels_list']
    list_filter = ['is_indexable']
    search_fields = ['name', 'slug']
    filter_horizontal = ['labels']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['mark_indexable', 'unmark_indexable']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'labels', 'display_order')
        }),
        ('SEO Settings', {
            'fields': ('seo_title', 'seo_description', 'seo_h1', 'seo_intro_text', 'seo_faq', 'og_image', 'schema_markup'),
            'classes': ('collapse',),
        }),
        ('Indexing', {
            'fields': ('is_indexable',),
        }),
    )

    def labels_list(self, obj):
        return ", ".join([label.name for label in obj.labels.all()])
    labels_list.short_description = 'Labels'

    @admin.action(description='Mark selected combos as indexable')
    def mark_indexable(self, request, queryset):
        updated = queryset.update(is_indexable=True)
        self.message_user(request, f'{updated} combo page(s) marked indexable.')

    @admin.action(description='Unmark selected combos as indexable')
    def unmark_indexable(self, request, queryset):
        updated = queryset.update(is_indexable=False)
        self.message_user(request, f'{updated} combo page(s) marked non-indexable.')


class LabelManagementAdmin(admin.ModelAdmin):
    """
    Unified admin view for managing SEO label pages.
    Shows both Labels (with is_seo_page=True) and LabelComboSeoPage in one table.
    """
    change_list_template = 'admin/products/label_management.html'
    
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.model = model
    
    def has_add_permission(self, request):
        """Disable add permission - use individual model admins"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Allow viewing - redirects to individual model admin for editing"""
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        """Disable delete permission - use individual model admins"""
        return False
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist to show our custom label management view"""
        return self.label_management_view(request)
    
    def label_management_view(self, request):
        """
        Custom view that displays unified table of SEO labels and combos
        """
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        
        # Get frontend URL from settings
        # SITE_URL should point to the frontend (Nuxt), not the Django backend
        site_url = getattr(settings, 'SITE_URL', '').strip().rstrip('/')
        
        # If SITE_URL is not set, try to detect frontend URL
        if not site_url:
            # Check for FRONTEND_URL environment variable
            import os
            site_url = os.environ.get('FRONTEND_URL', '').strip().rstrip('/')
        
        # If still not set, use intelligent defaults
        if not site_url:
            scheme = 'https' if request.is_secure() else 'http'
            host = request.get_host().split(':')[0]  # Get hostname without port
            
            if settings.DEBUG:
                # In development, Nuxt typically runs on port 3000
                if host in ['localhost', '127.0.0.1']:
                    site_url = "http://localhost:3000"
                else:
                    # For other dev setups, try to use same host
                    site_url = f"{scheme}://{host}:3000"
            else:
                # Production: detect if we're on API domain and convert to frontend domain
                # Common patterns: api-staging.indexo.ir -> staging.indexo.ir
                #                  api.indexo.ir -> indexo.ir
                #                  api-staging -> staging (if subdomain pattern)
                if host.startswith('api-'):
                    # Remove 'api-' prefix to get frontend domain
                    frontend_host = host.replace('api-', '', 1)
                    site_url = f"{scheme}://{frontend_host}"
                elif host.startswith('api.'):
                    # Remove 'api.' prefix to get frontend domain
                    frontend_host = host.replace('api.', '', 1)
                    site_url = f"{scheme}://{frontend_host}"
                elif '.api.' in host:
                    # Handle cases like staging.api.indexo.ir -> staging.indexo.ir
                    frontend_host = host.replace('.api.', '.', 1)
                    site_url = f"{scheme}://{frontend_host}"
                else:
                    # Fallback: assume frontend is on same domain (for same-domain setups)
                    site_url = f"{scheme}://{host}"
        
        # Get filter parameters
        department_filter = request.GET.get('department', '')
        category_filter = request.GET.get('category', '')
        search_query = request.GET.get('q', '')
        type_filter = request.GET.get('type', '')  # 'label', 'combo', or ''
        
        # Build queryset for Labels
        labels_qs = Label.objects.filter(is_seo_page=True, is_active=True)
        
        # Build queryset for LabelComboSeoPage
        combos_qs = LabelComboSeoPage.objects.all()
        
        # Apply filters
        if department_filter:
            labels_qs = labels_qs.filter(
                Q(departments__id=department_filter) | Q(departments__isnull=True)
            ).distinct()
            # For combos, filter by labels' departments
            combos_qs = combos_qs.filter(
                labels__departments__id=department_filter
            ).distinct()
        
        if category_filter:
            labels_qs = labels_qs.filter(
                Q(categories__id=category_filter) | Q(categories__isnull=True)
            ).distinct()
            combos_qs = combos_qs.filter(
                labels__categories__id=category_filter
            ).distinct()
        
        if search_query:
            labels_qs = labels_qs.filter(
                Q(name__icontains=search_query) | Q(slug__icontains=search_query)
            )
            combos_qs = combos_qs.filter(
                Q(name__icontains=search_query) | Q(slug__icontains=search_query)
            )
        
        if type_filter == 'label':
            combos_qs = combos_qs.none()
        elif type_filter == 'combo':
            labels_qs = labels_qs.none()
        
        # Prepare data for display
        label_items = []
        for label in labels_qs:
            # Get product count
            product_count = label.product_count or label.products.filter(is_active=True).count()
            
            # Build URL
            url = f"{site_url}/machinery/{label.slug}/"
            
            # Get departments/categories
            departments = ", ".join([d.name for d in label.departments.all()[:3]])
            if label.departments.count() > 3:
                departments += f" (+{label.departments.count() - 3})"
            if not departments:
                departments = "همه دپارتمان‌ها"
            
            categories = ", ".join([c.name for c in label.categories.all()[:3]])
            if label.categories.count() > 3:
                categories += f" (+{label.categories.count() - 3})"
            if not categories:
                categories = "همه دسته‌بندی‌ها"
            
            label_items.append({
                'id': f"label-{label.id}",
                'name': label.name,
                'type': 'Label',
                'url': url,
                'product_count': product_count,
                'departments': departments,
                'categories': categories,
                'slug': label.slug,
                'edit_url': reverse('admin:products_label_change', args=[label.id]),
            })
        
        combo_items = []
        for combo in combos_qs:
            # Get product count (products that have ALL labels in combo)
            label_ids = list(combo.labels.values_list('id', flat=True))
            if label_ids:
                products = Product.objects.filter(is_active=True, is_marketplace_hidden=False)
                for label_id in label_ids:
                    products = products.filter(labels__id=label_id)
                product_count = products.distinct().count()
            else:
                product_count = 0
            
            # Build URL
            url = f"{site_url}/machinery/{combo.slug}/"
            
            # Get departments/categories from labels
            all_departments = set()
            all_categories = set()
            for label in combo.labels.all():
                all_departments.update(label.departments.all())
                all_categories.update(label.categories.all())
            
            departments = ", ".join([d.name for d in list(all_departments)[:3]])
            if len(all_departments) > 3:
                departments += f" (+{len(all_departments) - 3})"
            if not departments:
                departments = "همه دپارتمان‌ها"
            
            categories = ", ".join([c.name for c in list(all_categories)[:3]])
            if len(all_categories) > 3:
                categories += f" (+{len(all_categories) - 3})"
            if not categories:
                categories = "همه دسته‌بندی‌ها"
            
            combo_items.append({
                'id': f"combo-{combo.id}",
                'name': combo.name,
                'type': 'Combo',
                'url': url,
                'product_count': product_count,
                'departments': departments,
                'categories': categories,
                'slug': combo.slug,
                'edit_url': reverse('admin:products_labelcomboseopage_change', args=[combo.id]),
            })
        
        # Combine and sort
        all_items = label_items + combo_items
        all_items.sort(key=lambda x: x['name'])
        
        # Pagination
        paginator = Paginator(all_items, 50)  # 50 items per page
        page = request.GET.get('page', 1)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        
        # Get filter options
        departments = Department.objects.all().order_by('name')
        categories = Category.objects.all().order_by('name')
        
        context = {
            **self.admin_site.each_context(request),
            'title': 'مدیریت لیبل‌های SEO',
            'items': items,
            'total_count': len(all_items),
            'departments': departments,
            'categories': categories,
            'current_department': department_filter,
            'current_category': category_filter,
            'current_search': search_query,
            'current_type': type_filter,
            'site_url': site_url,
            'opts': self.model._meta,
            'has_add_permission': False,
            'has_change_permission': True,
            'has_delete_permission': False,
        }
        
        return render(request, self.change_list_template, context)


# Create a proxy model for Label Management
from django.db import models as db_models

class LabelManagementProxy(Label):
    """Proxy model for Label Management admin view - uses Label as base but shows custom view"""
    class Meta:
        proxy = True
        verbose_name = 'مدیریت لیبل‌های SEO'
        verbose_name_plural = 'مدیریت لیبل‌های SEO'
        app_label = 'products'


# Register the admin
admin.site.register(LabelManagementProxy, LabelManagementAdmin)


class DepartmentAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Department description with rich text formatting (supports HTML, images, links, etc.)",
        required=False
    )
    
    class Meta:
        model = Department
        fields = '__all__'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentAdminForm
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
        js = ('admin/js/fix_action_button.js', 'admin/js/tinymce_image_picker.js',)
        css = {
            'all': ('admin/css/custom_admin.css', 'admin/css/force_action_button.css',)
        }

class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Category description with rich text formatting (supports HTML, images, links, etc.)",
        required=False
    )
    
    class Meta:
        model = Category
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
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
        js = ('admin/js/fix_action_button.js', 'admin/js/tinymce_image_picker.js',)
        css = {
            'all': ('admin/css/custom_admin.css', 'admin/css/force_action_button.css',)
        }

class SubcategoryAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Subcategory description with rich text formatting (supports HTML, images, links, etc.)",
        required=False
    )
    
    class Meta:
        model = Subcategory
        fields = '__all__'

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    form = SubcategoryAdminForm
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
        js = ('admin/js/fix_action_button.js', 'admin/js/tinymce_image_picker.js',)
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
            delete_button = format_html(
                '<button type="button" class="delete-image-btn" data-row-id="{}" '
                'style="margin-left: 10px; background: #dc3545; color: white; border: none; '
                'padding: 2px 8px; border-radius: 3px; cursor: pointer; font-size: 11px;">🗑️ Delete</button>',
                obj.pk
            ) if obj.pk else ''
            return format_html(
                '<div style="display: flex; align-items: center;">'
                '<img src="{}" style="max-width: 100px; max-height: 100px; border-radius: 4px;" />'
                '{}'
                '</div>',
                obj.image.url, delete_button
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
    list_display = ['name', 'slug', 'vendor', 'supplier', 'primary_category', 'get_subcategories', 'get_labels', 'price', 'stock', 'image_count', 'comment_count', 'approval_status', 'is_active', 'created_at']
    list_filter = ['approval_status', 'is_active', 'primary_category', 'subcategories', 'labels', 'created_at']
    search_fields = ['name', 'description', 'vendor__username', 'vendor__email']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['subcategories', 'labels']
    inlines = [ProductImageInline, ProductCommentInline]
    actions = ['make_active', 'make_inactive', 'approve_products', 'reject_products', 'delete_selected']  # Enable bulk actions with delete
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
        ('Labels & Tags', {
            'fields': ('labels',),
            'description': 'Add labels for filtering, promotional badges, and SEO. Select multiple labels using the selection widget below.'
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
            'fields': ('approval_status', 'is_active',)
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
    
    def get_labels(self, obj):
        """Display labels as colored badges"""
        try:
            labels = obj.labels.filter(is_active=True)[:5]  # Show max 5 labels
            if labels.exists():
                badges = []
                for label in labels:
                    color = label.color if label.color else '#1976d2'
                    badges.append(
                        f'<span style="background-color: {color}1a; color: {color}; '
                        f'padding: 2px 8px; border-radius: 12px; margin: 2px; '
                        f'display: inline-block; font-size: 11px; font-weight: 500;">'
                        f'{label.name}</span>'
                    )
                return format_html(' '.join(badges))
            return '-'
        except Exception as e:
            return format_html('<span style="color: orange;">Error</span>')
    get_labels.short_description = 'Labels'
    
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
    
    def approve_products(self, request, queryset):
        """Approve selected products"""
        updated = queryset.update(approval_status=Product.APPROVAL_STATUS_APPROVED)
        # Trigger save() to update is_active based on approval_status and primary_category
        for product in queryset:
            product.save()
        self.message_user(request, f'{updated} product(s) approved.')
    approve_products.short_description = "✅ Approve Products"
    
    def reject_products(self, request, queryset):
        """Reject selected products"""
        updated = queryset.update(approval_status=Product.APPROVAL_STATUS_REJECTED)
        # Trigger save() to update is_active based on approval_status
        for product in queryset:
            product.save()
        self.message_user(request, f'{updated} product(s) rejected.')
    reject_products.short_description = "❌ Reject Products"
    
    def has_delete_permission(self, request, obj=None):
        """Explicitly allow delete permission"""
        return True
    
    def save_model(self, request, obj, form, change):
        """Override save_model to handle multiple images and is_active/approval_status"""
        # If admin explicitly sets is_active=True, automatically approve the product
        if form.cleaned_data.get('is_active', False):
            obj.approval_status = Product.APPROVAL_STATUS_APPROVED
        
        super().save_model(request, obj, form, change)
        
        # Handle multiple images upload
        if hasattr(request, 'FILES'):
            files = request.FILES.getlist('multiple_images')
            if files:
                existing_count = obj.images.count()
                has_primary = obj.images.filter(is_primary=True).exists()
                
                for i, file in enumerate(files):
                    if file and file.size > 0:  # Make sure file exists and has content
                        try:
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
                        except (OSError, IOError, PermissionError) as e:
                            error_msg = f"خطا در ذخیره تصویر: {str(e)}. لطفاً از وجود پوشه media و دسترسی‌های نوشتن اطمینان حاصل کنید."
                            messages.error(request, error_msg)
                            raise
                        except Exception as e:
                            error_msg = f"خطا در ذخیره تصویر: {str(e)}"
                            messages.error(request, error_msg)
                            raise
    
    class Media:
        js = ('admin/js/fix_action_button.js', 'admin/js/price_formatter.js', 'admin/js/tinymce_image_picker.js',)
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
    Background function to process a scrape job
    """
    
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
        job.save()
        
        # Create product from scraped data
        product, error = create_product_from_scraped_data(
            scraped_data,
            vendor=job.vendor,
            supplier=job.supplier
        )
        
        if product:
            job.created_product = product
            job.status = 'completed'
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
    
    actions = ['retry_failed_in_batch']
    
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
    
    def retry_failed_in_batch(self, request, queryset):
        """Retry only failed jobs in selected batches"""
        total_retried = 0
        for batch in queryset:
            failed_jobs = batch.jobs.filter(status='failed')
            for job in failed_jobs:
                job.status = 'pending'
                job.error_message = None
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
    
    
    def get_urls(self):
        """Add custom URLs"""
        from django.urls import re_path
        urls = super().get_urls()
        custom_urls = [
            re_path(r'^(?P<object_id>\d+)/errors/$', self.admin_site.admin_view(self.errors_view), name='products_scrapejobatch_errors'),
        ]
        return custom_urls + urls
    
    def errors_view(self, request, object_id):
        """View HTTP errors for a batch"""
        from django.core.exceptions import PermissionDenied
        
        # Check permissions
        if not request.user.is_staff:
            raise PermissionDenied
        
        try:
            batch_id = int(object_id)
            batch = get_object_or_404(ScrapeJobBatch, id=batch_id)
            
            # Get failed jobs with HTTP errors
            failed_jobs = batch.jobs.filter(status='failed').exclude(error_message__isnull=True)
            
            # Extract HTTP status codes from error messages
            http_errors = []
            for job in failed_jobs:
                error_msg = job.error_message or ''
                # Try to extract HTTP status code
                import re
                status_match = re.search(r'(\d{3})', error_msg)
                status_code = int(status_match.group(1)) if status_match else None
                
                if status_code and 400 <= status_code < 600:
                    http_errors.append({
                        'job_id': job.id,
                        'url': job.url,
                        'status_code': status_code,
                        'error_message': error_msg,
                        'created_at': job.created_at,
                    })
            
            context = {
                'title': f'HTTP Errors - {batch.name or f"Batch #{batch_id}"}',
                'batch': batch,
                'http_errors': http_errors,
                'total_errors': len(http_errors),
                'opts': self.model._meta,
                'has_permission': True,
            }
            return render(request, 'admin/products/http_errors.html', context)
        except (ValueError, TypeError):
            messages.error(request, f"Invalid batch ID: {object_id}")
            return redirect('/admin/products/scrapejobatch/')
        except ScrapeJobBatch.DoesNotExist:
            messages.error(request, f"Batch #{object_id} not found.")
            return redirect('/admin/products/scrapejobatch/')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('/admin/products/scrapejobatch/')


@admin.register(ProductScrapeJob)
class ProductScrapeJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'batch_link', 'url_preview', 'vendor', 'supplier', 'status_display', 'retry_info', 'created_product_link', 'created_at', 'processed_at']
    list_filter = ['status', 'batch', 'created_at', 'supplier']
    search_fields = ['url', 'vendor__username', 'error_message']
    readonly_fields = ['batch', 'scraped_data', 'created_product', 'processed_at', 'created_at', 'updated_at', 'retry_count', 'last_retry_at']
    
    fieldsets = (
        ('Job Information', {
            'fields': ('url', 'batch', 'vendor', 'supplier', 'status')
        }),
        ('Results', {
            'fields': ('created_product', 'error_message', 'processed_at'),
            'description': 'Product creation results and error message'
        }),
        ('Retry Information', {
            'fields': ('retry_count', 'last_retry_at'),
            'classes': ('collapse',),
        }),
        ('Scraped Data', {
            'fields': ('scraped_data',),
            'classes': ('collapse',),
            'description': 'Raw scraped data in JSON format'
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
            url = f'/admin/products/scrapejobatch/{obj.batch.id}/errors/'
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
        """Display status with error message"""
        status_colors = {
            'pending': '#FFA500',
            'processing': '#0066CC',
            'completed': '#28a745',
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
    
    def retry_failed_jobs(self, request, queryset):
        """Retry failed scrape jobs with tracking"""
        jobs = queryset.filter(status='failed')
        count = 0
        for job in jobs:
            job.status = 'pending'
            job.error_message = None
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


@admin.register(CategoryRequest)
class CategoryRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'requested_name', 'supplier', 'product_link', 'status_display', 'reviewed_by', 'created_at', 'reviewed_at']
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = ['requested_name', 'supplier__name', 'product__name']
    readonly_fields = ['created_at', 'updated_at', 'reviewed_at']
    actions = ['approve_requests', 'reject_requests']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('supplier', 'product', 'requested_name', 'status')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'reviewed_at', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def product_link(self, obj):
        if obj.product:
            url = f'/admin/products/product/{obj.product.id}/change/'
            return format_html(
                '<a href="{}" style="color: #667eea;">{}</a>',
                url, obj.product.name[:50]
            )
        return '-'
    product_link.short_description = 'Product'
    
    def status_display(self, obj):
        status_colors = {
            'pending': '#FFA500',
            'approved': '#28a745',
            'rejected': '#dc3545',
        }
        color = status_colors.get(obj.status, '#999')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    @admin.action(description='Approve selected requests')
    def approve_requests(self, request, queryset):
        """Approve category requests"""
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='approved',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} request(s) approved.')
    
    @admin.action(description='Reject selected requests')
    def reject_requests(self, request, queryset):
        """Reject category requests"""
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{updated} request(s) rejected.')

        ordered_models = [
            (Product, ProductAdmin),
            (Department, DepartmentAdmin),
            (Category, CategoryAdmin),
            (Subcategory, SubcategoryAdmin),
            (ProductComment, ProductCommentAdmin),
            (CategoryRequest, CategoryRequestAdmin),
            (ProductScrapeJob, ProductScrapeJobAdmin),
            (ScrapeJobBatch, ScrapeJobBatchAdmin),
        ]

        # Unregister each model if it's already registered.
        for model, _ in ordered_models:
            if site.is_registered(model):
                site.unregister(model)

       # Re-register all models in the new, defined order.
        for model, admin_class in ordered_models:
            site.register(model, admin_class)