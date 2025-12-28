from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django import forms
from django.utils.html import format_html
from django.db.models import Count
from tinymce.widgets import TinyMCE
from .models import AboutPage, ContactPage, Redirect, ShortLink, ShortLinkClick


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



class ShortLinkClickInline(admin.TabularInline):
    model = ShortLinkClick
    extra = 0
    can_delete = False
    readonly_fields = ('ip_address', 'device_type', 'clicked_at')
    fields = ('ip_address', 'device_type', 'clicked_at')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ('short_code_display', 'campaign_name', 'target_url_display', 'click_stats', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('short_code', 'campaign_name', 'target_url')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'full_url', 'stats_summary')
    inlines = [ShortLinkClickInline]
    list_display_links = ('short_code_display', 'campaign_name')
    
    fieldsets = (
        ('اطلاعات لینک (Link Information)', {
            'fields': ('short_code', 'target_url', 'campaign_name', 'is_active', 'full_url'),
        }),
        ('آمار (Statistics)', {
            'fields': ('stats_summary',),
        }),
        ('اطلاعات (Information)', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def short_code_display(self, obj):
        return format_html('<code>/s/{}</code>', obj.short_code)
    short_code_display.short_description = 'کد کوتاه'
    
    def target_url_display(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.target_url, obj.target_url)
    target_url_display.short_description = 'آدرس هدف'
    
    def full_url(self, obj):
        if obj.pk:
            return format_html('<code>indexo.ir/s/{}</code>', obj.short_code)
        return '-'
    full_url.short_description = 'لینک کامل'
    
    def stats_summary(self, obj):
        if not obj.pk:
            return '-'
        clicks = obj.get_click_count()
        unique = obj.get_unique_visitors()
        mobile = obj.clicks.filter(device_type='mobile').count()
        desktop = obj.clicks.filter(device_type='desktop').count()
        tablet = obj.clicks.filter(device_type='tablet').count()
        
        return format_html(
            '<div style="line-height: 1.8;">' 
            '<strong>کل کلیک‌ها:</strong> {}<br>'
            '<strong>بازدیدکننده یکتا:</strong> {}<br>'
            '<strong>موبایل:</strong> {} | <strong>دسکتاپ:</strong> {} | <strong>تبلت:</strong> {}'
            '</div>',
            clicks, unique, mobile, desktop, tablet
        )
    stats_summary.short_description = 'خلاصه آمار'
    
    def click_stats(self, obj):
        clicks = obj.get_click_count()
        unique = obj.get_unique_visitors()
        return format_html('<strong>{}</strong> کلیک | <strong>{}</strong> بازدیدکننده', clicks, unique)
    click_stats.short_description = 'آمار'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            click_count=Count('clicks'),
            unique_visitors=Count('clicks__ip_address', distinct=True)
        )


@admin.register(ShortLinkClick)
class ShortLinkClickAdmin(admin.ModelAdmin):
    list_display = ('short_link', 'ip_address', 'device_type', 'clicked_at')
    list_filter = ('device_type', 'clicked_at', 'short_link')
    search_fields = ('ip_address', 'short_link__short_code')
    readonly_fields = ('short_link', 'ip_address', 'device_type', 'clicked_at')
    date_hierarchy = 'clicked_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
