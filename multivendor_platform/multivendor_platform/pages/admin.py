from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django import forms
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from .models import AboutPage, ContactPage, Redirect


class AboutPageAdminForm(forms.ModelForm):
    content_fa = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="محتوای کامل صفحه درباره ما به فارسی با قابلیت فرمت‌دهی"
    )
    content_en = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Full About Us page content in English with rich text formatting",
        required=False
    )
    
    class Meta:
        model = AboutPage
        fields = '__all__'
        widgets = {
            'content_fa': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'content_en': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """
    Admin interface for About Us page
    """
    form = AboutPageAdminForm
    
    class Media:
        js = ('admin/js/tinymce_image_picker.js',)
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


class ContactPageAdminForm(forms.ModelForm):
    content_fa = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="محتوای کامل صفحه تماس با ما به فارسی با قابلیت فرمت‌دهی"
    )
    content_en = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        help_text="Full Contact Us page content in English with rich text formatting",
        required=False
    )
    
    class Meta:
        model = ContactPage
        fields = '__all__'
        widgets = {
            'content_fa': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'content_en': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    """
    Admin interface for Contact Us page
    """
    form = ContactPageAdminForm
    
    class Media:
        js = ('admin/js/tinymce_image_picker.js',)
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


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    """
    Admin interface for URL redirects management
    """
    list_display = ('from_path', 'to_path_display', 'redirect_type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'redirect_type', 'created_at')
    search_fields = ('from_path', 'to_path', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    
    fieldsets = (
        ('اطلاعات هدایت (Redirect Information)', {
            'fields': ('from_path', 'to_path', 'redirect_type', 'is_active'),
            'description': 'مسیر قدیمی و جدید را وارد کنید. نوع هدایت را انتخاب کنید (301 برای دائمی، 302 برای موقت).'
        }),
        ('یادداشت‌ها (Notes)', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('اطلاعات (Information)', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def to_path_display(self, obj):
        """Display to_path with styling"""
        if obj.to_path.startswith('http'):
            return format_html('<a href="{}" target="_blank">{}</a>', obj.to_path, obj.to_path)
        return obj.to_path
    to_path_display.short_description = 'به مسیر'
    
    def save_model(self, request, obj, form, change):
        """Set created_by when creating new redirect"""
        if not change:  # Only set on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['activate_redirects', 'deactivate_redirects']
    
    @admin.action(description='فعال کردن هدایت‌های انتخاب شده')
    def activate_redirects(self, request, queryset):
        """Activate selected redirects"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} هدایت فعال شد.')
    activate_redirects.short_description = 'فعال کردن هدایت‌های انتخاب شده'
    
    @admin.action(description='غیرفعال کردن هدایت‌های انتخاب شده')
    def deactivate_redirects(self, request, queryset):
        """Deactivate selected redirects"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} هدایت غیرفعال شد.')
    deactivate_redirects.short_description = 'غیرفعال کردن هدایت‌های انتخاب شده'
