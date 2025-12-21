"""
Django admin configuration for SMS Newsletter app
"""
from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.db.models import Q
from django import forms
from .models import SupplierSMSNewsletter

try:
    from .services import KavenegarSMSService
    SMS_SERVICE_AVAILABLE = True
except ImportError:
    SMS_SERVICE_AVAILABLE = False
    KavenegarSMSService = None


class SupplierSMSNewsletterAdminForm(forms.ModelForm):
    """Custom form to ensure proper ManyToMany handling"""
    
    class Meta:
        model = SupplierSMSNewsletter
        fields = '__all__'
    
    def clean_mobile(self):
        """Ensure mobile is unique"""
        mobile = self.cleaned_data.get('mobile')
        if mobile:
            # Check for duplicates excluding current instance
            qs = SupplierSMSNewsletter.objects.filter(mobile=mobile)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return mobile


@admin.register(SupplierSMSNewsletter)
class SupplierSMSNewsletterAdmin(admin.ModelAdmin):
    """
    Admin interface for managing supplier SMS newsletter subscriptions.
    """
    form = SupplierSMSNewsletterAdminForm
    list_display = [
        'supplier_name',
        'company_name',
        'phone',
        'mobile',
        'get_working_fields_display',
        'created_at'
    ]
    list_filter = ['working_fields', 'created_at']
    search_fields = ['supplier_name', 'company_name', 'phone', 'mobile']
    filter_horizontal = ['working_fields']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['send_sms_to_selected', 'delete_selected']
    
    fieldsets = (
        ('اطلاعات تامین‌کننده', {
            'fields': ('supplier_name', 'company_name')
        }),
        ('اطلاعات تماس', {
            'fields': ('phone', 'mobile')
        }),
        ('زمینه‌های کاری', {
            'fields': ('working_fields',),
            'description': 'زمینه‌های کاری تامین‌کننده را انتخاب کنید. می‌توانید چند مورد انتخاب کنید.'
        }),
        ('اطلاعات سیستم', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_working_fields_display(self, obj):
        """Display working fields as comma-separated list"""
        fields = obj.working_fields.all()
        if fields:
            return ', '.join([field.name for field in fields])
        return '-'
    get_working_fields_display.short_description = 'زمینه‌های کاری'
    get_working_fields_display.admin_order_field = 'working_fields'
    
    @admin.action(description='ارسال پیامک به تامین‌کنندگان انتخاب شده')
    def send_sms_to_selected(self, request, queryset):
        """
        Bulk action to send SMS to selected suppliers.
        Sends SMS for each working field (subcategory) of each supplier.
        """
        if not request.user.is_staff:
            self.message_user(
                request,
                'شما مجوز ارسال پیامک ندارید.',
                level=messages.ERROR
            )
            return
        
        if not SMS_SERVICE_AVAILABLE:
            self.message_user(
                request,
                'سرویس پیامک در دسترس نیست. لطفاً پکیج kavenegar را نصب کنید.',
                level=messages.ERROR
            )
            return
        
        try:
            sms_service = KavenegarSMSService()
        except Exception as e:
            self.message_user(
                request,
                f'خطا در راه‌اندازی سرویس پیامک: {str(e)}',
                level=messages.ERROR
            )
            return
        
        suppliers_to_send = []
        total_sms_count = 0
        
        # Prepare suppliers for SMS sending
        for supplier in queryset:
            if not supplier.mobile:
                continue
            
            working_fields = supplier.working_fields.all()
            
            if not working_fields.exists():
                # If no working fields, send one SMS without category
                suppliers_to_send.append({
                    'receptor': supplier.mobile,
                    'name': supplier.supplier_name,
                    'company_name': supplier.company_name,
                    'category_name': 'عمومی'
                })
                total_sms_count += 1
            else:
                # Send SMS for each working field
                for field in working_fields:
                    suppliers_to_send.append({
                        'receptor': supplier.mobile,
                        'name': supplier.supplier_name,
                        'company_name': supplier.company_name,
                        'category_name': field.name
                    })
                    total_sms_count += 1
        
        if not suppliers_to_send:
            self.message_user(
                request,
                'هیچ تامین‌کننده‌ای با شماره موبایل معتبر یافت نشد.',
                level=messages.WARNING
            )
            return
        
        # Send bulk SMS
        results = sms_service.send_bulk_sms(suppliers_to_send)
        
        # Show results
        if results['total_failed'] == 0:
            self.message_user(
                request,
                f'✅ {results["total_sent"]} پیامک با موفقیت ارسال شد.',
                level=messages.SUCCESS
            )
        elif results['total_sent'] > 0:
            self.message_user(
                request,
                f'⚠️ {results["total_sent"]} پیامک ارسال شد، {results["total_failed"]} پیامک ناموفق بود.',
                level=messages.WARNING
            )
        else:
            self.message_user(
                request,
                f'❌ ارسال پیامک ناموفق بود. {results["total_failed"]} خطا رخ داد.',
                level=messages.ERROR
            )
    
    send_sms_to_selected.short_description = 'ارسال پیامک به تامین‌کنندگان انتخاب شده'
    
    def save_model(self, request, obj, form, change):
        """
        Save the supplier instance.
        ManyToMany fields are saved separately in save_related.
        """
        super().save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change):
        """
        Explicitly save ManyToMany relationships.
        This ensures working_fields are saved correctly to a single supplier instance.
        """
        super().save_related(request, form, formsets, change)
    
    def has_add_permission(self, request):
        """Only staff and superusers can add"""
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        """Only staff and superusers can change"""
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        """Only staff and superusers can delete"""
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        """Only staff and superusers can view"""
        return request.user.is_staff

