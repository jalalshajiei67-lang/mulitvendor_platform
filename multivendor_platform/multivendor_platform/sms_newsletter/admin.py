from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Seller
from .services import send_sms_via_kavenegar
from products.models import Subcategory


@admin.action(description='ارسال پیامک به فروشندگان انتخاب شده')
def send_sms_to_selected_sellers(modeladmin, request, queryset):
    """
    Admin action to send SMS to selected sellers.
    Only works when a filter is applied.
    Uses the applied filter name as token2.
    """
    if not queryset.exists():
        modeladmin.message_user(request, 'هیچ فروشنده‌ای انتخاب نشده است.', messages.WARNING)
        return
    
    # Get applied filter name
    filter_name = modeladmin._get_applied_filter_name(request)
    if not filter_name:
        modeladmin.message_user(
            request,
            'لطفاً ابتدا فیلتر را اعمال کنید. ارسال پیامک نیاز به فیلتر دارد.',
            messages.ERROR
        )
        return
    
    # Send SMS to each selected seller
    results = []
    for seller in queryset:
        result = send_sms_via_kavenegar(seller, filter_name=filter_name)
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
            f'پیامک با موفقیت به {success_count} فروشنده ارسال شد. (فیلتر: {filter_name})',
            messages.SUCCESS
        )
    else:
        failed_sellers = [r['seller'] for r in results if not r['success']]
        modeladmin.message_user(
            request,
            f'{success_count} پیامک ارسال شد، {failure_count} مورد ناموفق. ناموفق: {", ".join(failed_sellers[:5])} (فیلتر: {filter_name})',
            messages.WARNING
        )


class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'mobile_number', 'phone', 'get_working_fields_count', 'created_at', 'send_sms_button']
    list_filter = ['working_fields', 'created_at']
    search_fields = ['name', 'company_name', 'mobile_number', 'phone']
    filter_horizontal = ['working_fields']
    # Actions will be conditionally shown based on filter
    
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
        """Display a button to send SMS to this seller - only if filter is applied"""
        # Check if filter is applied by looking at request
        request = getattr(self, '_current_request', None)
        if request:
            filter_name = self._get_applied_filter_name(request)
            if filter_name:
                # Build URL with filter info
                url = reverse('admin:sms_newsletter_seller_send_single_sms', args=[obj.pk])
                # Preserve filter parameters
                filter_params = self._get_filter_params(request)
                if filter_params:
                    url += '?' + filter_params
                return format_html(
                    '<a class="button" href="{}" style="padding: 5px 10px; background-color: #417690; color: white; text-decoration: none; border-radius: 3px;">ارسال پیامک</a>',
                    url
                )
            else:
                return format_html(
                    '<span style="color: #999; font-size: 12px;">ابتدا فیلتر اعمال کنید</span>'
                )
        return format_html(
            '<span style="color: #999; font-size: 12px;">ابتدا فیلتر اعمال کنید</span>'
        )
    send_sms_button.short_description = 'ارسال پیامک'
    
    def changelist_view(self, request, extra_context=None):
        """Override to store request for use in list_display methods"""
        self._current_request = request
        return super().changelist_view(request, extra_context)
    
    def get_actions(self, request):
        """Only show SMS action when filter is applied"""
        actions = super().get_actions(request)
        
        # Check if filter is applied
        filter_name = self._get_applied_filter_name(request)
        if not filter_name:
            # Remove SMS action if no filter is applied
            if 'send_sms_to_selected_sellers' in actions:
                del actions['send_sms_to_selected_sellers']
        else:
            # Add SMS action if filter is applied
            actions['send_sms_to_selected_sellers'] = (
                send_sms_to_selected_sellers,
                'send_sms_to_selected_sellers',
                'ارسال پیامک به فروشندگان انتخاب شده'
            )
        
        return actions
    
    def _get_filter_params(self, request):
        """Get filter query parameters from request"""
        filter_params = []
        # Get all parameters that start with 'working_fields'
        for key, values in request.GET.lists():
            if key.startswith('working_fields'):
                for value in values:
                    filter_params.append(f'{key}={value}')
        return '&'.join(filter_params)
    
    def _get_applied_filter_name(self, request):
        """Get the name of applied filter(s) from request"""
        working_field_ids = []
        
        # Django admin for ManyToMany filters typically uses 'working_fields__id__exact'
        # but we'll check all possible formats
        for param_name in ['working_fields__id__exact', 'working_fields', 'working_fields__id']:
            ids = request.GET.getlist(param_name)
            if ids:
                working_field_ids = ids
                break
        
        # If not found, check all GET params for working_fields patterns
        if not working_field_ids:
            for key in request.GET.keys():
                if 'working_fields' in key and 'id' in key:
                    working_field_ids = request.GET.getlist(key)
                    break
        
        if not working_field_ids:
            return None
        
        try:
            # Convert to integers and filter out invalid values
            working_field_ids = [int(id) for id in working_field_ids if id and str(id).isdigit()]
            if not working_field_ids:
                return None
            
            # Get subcategory names
            subcategories = Subcategory.objects.filter(id__in=working_field_ids)
            if subcategories.exists():
                # Combine names, limit to 30 chars total (to avoid URL length issues)
                names = [sc.name for sc in subcategories]
                combined = ", ".join(names)
                if len(combined) > 30:
                    # Try to fit as many as possible within 30 chars
                    result = ""
                    for name in names:
                        if len(result) + len(name) + 2 <= 30:  # +2 for ", "
                            if result:
                                result += ", "
                            result += name
                        else:
                            break
                    if not result:  # Even first name is too long
                        result = names[0][:27] + "..."
                    else:
                        result = result[:27] + "..."
                    return result
                return combined
        except Exception:
            pass
        return None
    
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
        """Send SMS to a single seller - requires filter to be applied"""
        try:
            seller = Seller.objects.get(pk=seller_id)
        except Seller.DoesNotExist:
            self.message_user(request, 'فروشنده یافت نشد.', messages.ERROR)
            return HttpResponseRedirect(reverse('admin:sms_newsletter_seller_changelist'))
        
        # Get applied filter name
        filter_name = self._get_applied_filter_name(request)
        if not filter_name:
            self.message_user(
                request,
                'لطفاً ابتدا فیلتر را اعمال کنید. ارسال پیامک نیاز به فیلتر دارد.',
                messages.ERROR
            )
            # Redirect back to changelist with filter preserved
            changelist_url = reverse('admin:sms_newsletter_seller_changelist')
            filter_params = self._get_filter_params(request)
            if filter_params:
                changelist_url += '?' + filter_params
            return HttpResponseRedirect(changelist_url)
        
        # Send SMS with filter name
        result = send_sms_via_kavenegar(seller, filter_name=filter_name)
        
        if result['success']:
            self.message_user(
                request,
                f'پیامک با موفقیت به {seller.name} ارسال شد. (فیلتر: {filter_name})',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f'خطا در ارسال پیامک به {seller.name}: {result["message"]}',
                messages.ERROR
            )
        
        # Redirect back to changelist with filter preserved
        changelist_url = reverse('admin:sms_newsletter_seller_changelist')
        filter_params = self._get_filter_params(request)
        if filter_params:
            changelist_url += '?' + filter_params
        return HttpResponseRedirect(changelist_url)


# Register the model
admin.site.register(Seller, SellerAdmin)

