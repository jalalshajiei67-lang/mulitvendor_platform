from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import AboutPage, ContactPage


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """
    Admin interface for About Us page
    """
    fieldsets = (
        ('محتوای فارسی (Persian Content)', {
            'fields': ('title_fa', 'content_fa'),
            'classes': ('wide',),
        }),
        ('محتوای انگلیسی (English Content)', {
            'fields': ('title_en', 'content_en'),
            'classes': ('collapse',),
        }),
        ('سئو فارسی (Persian SEO)', {
            'fields': ('meta_title_fa', 'meta_description_fa', 'meta_keywords_fa'),
            'classes': ('collapse',),
            'description': 'تنظیمات SEO برای بهبود رتبه در موتورهای جستجو'
        }),
        ('سئو انگلیسی (English SEO)', {
            'fields': ('meta_title_en', 'meta_description_en', 'meta_keywords_en'),
            'classes': ('collapse',),
            'description': 'SEO settings to improve search engine ranking'
        }),
        ('اطلاعات (Information)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    list_display = ('title_fa', 'updated_at')
    
    def changelist_view(self, request, extra_context=None):
        """
        Redirect to edit page if instance(s) exist
        """
        if AboutPage.objects.exists():
            # Get the most recently updated instance (in case of duplicates)
            obj = AboutPage.objects.order_by('-updated_at').first()
            return redirect(reverse('admin:pages_aboutpage_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        """
        Only allow adding if no instance exists
        """
        if AboutPage.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of the page
        """
        return False


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    """
    Admin interface for Contact Us page
    """
    fieldsets = (
        ('محتوای فارسی (Persian Content)', {
            'fields': ('title_fa', 'content_fa'),
            'classes': ('wide',),
        }),
        ('اطلاعات تماس (Contact Information)', {
            'fields': ('address_fa', 'phone', 'email', 'working_hours_fa'),
            'classes': ('wide',),
        }),
        ('محتوای انگلیسی (English Content)', {
            'fields': ('title_en', 'content_en', 'address_en', 'working_hours_en'),
            'classes': ('collapse',),
        }),
        ('سئو فارسی (Persian SEO)', {
            'fields': ('meta_title_fa', 'meta_description_fa', 'meta_keywords_fa'),
            'classes': ('collapse',),
            'description': 'تنظیمات SEO برای بهبود رتبه در موتورهای جستجو'
        }),
        ('سئو انگلیسی (English SEO)', {
            'fields': ('meta_title_en', 'meta_description_en', 'meta_keywords_en'),
            'classes': ('collapse',),
            'description': 'SEO settings to improve search engine ranking'
        }),
        ('اطلاعات (Information)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    list_display = ('title_fa', 'phone', 'email', 'updated_at')
    
    def changelist_view(self, request, extra_context=None):
        """
        Redirect to edit page if instance(s) exist
        """
        if ContactPage.objects.exists():
            # Get the most recently updated instance (in case of duplicates)
            obj = ContactPage.objects.order_by('-updated_at').first()
            return redirect(reverse('admin:pages_contactpage_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        """
        Only allow adding if no instance exists
        """
        if ContactPage.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of the page
        """
        return False

