from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from .models import Seller
from .services import send_sms_via_kavenegar
from products.models import Subcategory


@admin.action(description='ارسال پیامک به فروشندگان انتخاب شده')
def send_sms_to_sellers(modeladmin, request, queryset):
    """
    Admin action to send SMS to selected sellers.
    Uses their own working fields for the SMS content.
    """
    if not queryset.exists():
        modeladmin.message_user(request, 'هیچ فروشنده‌ای انتخاب نشده است.', messages.WARNING)
        return
    
    results = []
    for seller in queryset:
        result = send_sms_via_kavenegar(seller, working_fields=None)
        results.append({
            'seller': seller.name,
            'success': result['success'],
            'message': result['message']
        })
    
    # Count successes and failures
    success_count = sum(1 for r in results if r['success'])
    failure_count = len(results) - success_count
    
    if failure_count == 0:
        modeladmin.message_user(
            request,
            f'پیامک با موفقیت به {success_count} فروشنده ارسال شد.',
            messages.SUCCESS
        )
    else:
        failed_sellers = [r['seller'] for r in results if not r['success']]
        modeladmin.message_user(
            request,
            f'{success_count} پیامک ارسال شد، {failure_count} مورد ناموفق. ناموفق: {", ".join(failed_sellers[:5])}',
            messages.WARNING
        )


class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'mobile_number', 'phone', 'get_working_fields_count', 'created_at', 'send_sms_button']
    list_filter = ['working_fields', 'created_at']
    search_fields = ['name', 'company_name', 'mobile_number', 'phone']
    filter_horizontal = ['working_fields']
    actions = [send_sms_to_sellers]
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'company_name', 'mobile_number', 'phone')
        }),
        ('حوزه‌های کاری', {
            'fields': ('working_fields',),
            'description': 'زیردسته‌بندی‌های مرتبط با این فروشنده را انتخاب کنید'
        }),
    )

    def get_working_fields_count(self, obj):
        """Display count of working fields"""
        count = obj.working_fields.count()
        return f'{count} حوزه کاری'
    get_working_fields_count.short_description = 'تعداد حوزه‌های کاری'
    
    def send_sms_button(self, obj):
        """Display a button to send SMS to this seller"""
        url = reverse('admin:sms_newsletter_seller_send_single_sms', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="padding: 5px 10px; background-color: #417690; color: white; text-decoration: none; border-radius: 3px;">ارسال پیامک</a>',
            url
        )
    send_sms_button.short_description = 'ارسال پیامک'
    
    def get_urls(self):
        """Add custom URL for sending SMS to a single seller"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:seller_id>/send-sms/',
                self.admin_site.admin_view(self.send_single_sms),
                name='sms_newsletter_seller_send_single_sms',
            ),
        ]
        return custom_urls + urls
    
    def send_single_sms(self, request, seller_id):
        """Send SMS to a single seller"""
        try:
            seller = Seller.objects.get(pk=seller_id)
        except Seller.DoesNotExist:
            self.message_user(request, 'فروشنده یافت نشد.', messages.ERROR)
            return HttpResponseRedirect(reverse('admin:sms_newsletter_seller_changelist'))
        
        result = send_sms_via_kavenegar(seller, working_fields=None)
        
        if result['success']:
            self.message_user(
                request,
                f'پیامک با موفقیت به {seller.name} ارسال شد.',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f'خطا در ارسال پیامک به {seller.name}: {result["message"]}',
                messages.ERROR
            )
        
        return HttpResponseRedirect(reverse('admin:sms_newsletter_seller_change', args=[seller_id]))


# Register the model
admin.site.register(Seller, SellerAdmin)

