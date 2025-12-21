"""
Django Admin configuration for Payment models
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import PremiumSubscriptionPayment, PaymentInvoice, DiscountCampaign, DiscountUsage


@admin.register(PremiumSubscriptionPayment)
class PremiumSubscriptionPaymentAdmin(admin.ModelAdmin):
    """Admin interface for Premium Subscription Payments"""
    
    list_display = [
        'id',
        'user_link',
        'billing_period',
        'amount_display',
        'status_badge',
        'track_id',
        'ref_number',
        'created_at',
        'paid_at',
    ]
    
    list_filter = [
        'status',
        'billing_period',
        'payment_method',
        'created_at',
        'paid_at',
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'track_id',
        'order_id',
        'ref_number',
    ]
    
    readonly_fields = [
        'user',
        'created_at',
        'paid_at',
        'verified_at',
        'track_id',
        'order_id',
        'ref_number',
        'card_number',
        'zibal_response_display',
    ]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'billing_period')
        }),
        ('Payment Details', {
            'fields': ('amount', 'status', 'payment_method', 'description')
        }),
        ('Zibal Information', {
            'fields': ('track_id', 'order_id', 'ref_number', 'card_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'paid_at', 'verified_at')
        }),
        ('Response Data', {
            'fields': ('zibal_response_display',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_failed', 'regenerate_invoice']
    
    def user_link(self, obj):
        """Link to user in admin"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def amount_display(self, obj):
        """Display amount in both Rial and Toman"""
        rial = int(obj.amount)
        toman = rial / 10
        return f"{rial:,} ریال ({toman:,.0f} تومان)"
    amount_display.short_description = 'Amount'
    
    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'pending': 'gray',
            'paid': 'blue',
            'verified': 'green',
            'failed': 'red',
            'cancelled': 'orange',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def zibal_response_display(self, obj):
        """Display Zibal response in readable format"""
        if obj.zibal_response:
            import json
            return format_html(
                '<pre>{}</pre>',
                json.dumps(obj.zibal_response, indent=2, ensure_ascii=False)
            )
        return '-'
    zibal_response_display.short_description = 'Zibal Response'
    
    def mark_as_failed(self, request, queryset):
        """Mark selected payments as failed"""
        count = queryset.update(status='failed')
        self.message_user(request, f'{count} payment(s) marked as failed.')
    mark_as_failed.short_description = 'Mark as failed'
    
    def regenerate_invoice(self, request, queryset):
        """Regenerate invoices for verified payments"""
        from .invoice_generator import create_invoice_for_payment
        count = 0
        for payment in queryset.filter(status='verified'):
            create_invoice_for_payment(payment)
            count += 1
        self.message_user(request, f'Regenerated {count} invoice(s).')
    regenerate_invoice.short_description = 'Regenerate invoice'


@admin.register(PaymentInvoice)
class PaymentInvoiceAdmin(admin.ModelAdmin):
    """Admin interface for Payment Invoices"""
    
    list_display = [
        'invoice_number',
        'payment_user',
        'total_amount_display',
        'issue_date',
        'has_pdf',
        'download_link',
    ]
    
    list_filter = [
        'issue_date',
        'due_date',
    ]
    
    search_fields = [
        'invoice_number',
        'payment__user__username',
        'payment__user__email',
        'payment__track_id',
    ]
    
    readonly_fields = [
        'payment',
        'invoice_number',
        'issue_date',
        'created_at',
        'updated_at',
        'invoice_preview',
    ]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('payment', 'invoice_number', 'issue_date', 'due_date')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax_amount', 'total_amount')
        }),
        ('PDF', {
            'fields': ('invoice_pdf', 'invoice_preview')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['regenerate_pdf']
    
    def payment_user(self, obj):
        """Display payment user"""
        return obj.payment.user.username
    payment_user.short_description = 'User'
    
    def total_amount_display(self, obj):
        """Display total amount"""
        rial = int(obj.total_amount)
        toman = rial / 10
        return f"{rial:,} ریال ({toman:,.0f} تومان)"
    total_amount_display.short_description = 'Total Amount'
    
    def has_pdf(self, obj):
        """Check if PDF exists"""
        if obj.invoice_pdf:
            return format_html(
                '<span style="color: green;">✓</span>'
            )
        return format_html(
            '<span style="color: red;">✗</span>'
        )
    has_pdf.short_description = 'PDF'
    
    def download_link(self, obj):
        """Download link for PDF"""
        if obj.invoice_pdf:
            return format_html(
                '<a href="{}" target="_blank">Download PDF</a>',
                obj.invoice_pdf.url
            )
        return '-'
    download_link.short_description = 'Download'
    
    def invoice_preview(self, obj):
        """Preview invoice PDF"""
        if obj.invoice_pdf:
            return format_html(
                '<a href="{}" target="_blank">View PDF</a>',
                obj.invoice_pdf.url
            )
        return 'No PDF available'
    invoice_preview.short_description = 'PDF Preview'
    
    def regenerate_pdf(self, request, queryset):
        """Regenerate PDF for selected invoices"""
        from .invoice_generator import InvoiceGenerator
        generator = InvoiceGenerator()
        count = 0
        for invoice in queryset:
            generator.generate_and_save_invoice(invoice, invoice.payment)
            count += 1
        self.message_user(request, f'Regenerated {count} PDF(s).')
    regenerate_pdf.short_description = 'Regenerate PDF'


@admin.register(DiscountCampaign)
class DiscountCampaignAdmin(admin.ModelAdmin):
    """Admin interface for Discount Campaigns"""
    
    list_display = [
        'code',
        'name',
        'discount_display',
        'billing_period',
        'valid_from',
        'valid_until',
        'usage_stats',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'discount_type',
        'billing_period',
        'valid_from',
        'valid_until',
        'created_at',
    ]
    
    search_fields = [
        'code',
        'name',
        'description',
    ]
    
    readonly_fields = [
        'used_count',
        'created_at',
        'updated_at',
        'usage_stats_display',
    ]
    
    fieldsets = (
        ('Campaign Information', {
            'fields': ('code', 'name', 'description', 'is_active', 'created_by')
        }),
        ('Discount Settings', {
            'fields': (
                'discount_type',
                'discount_value',
                'max_discount_toman',
            )
        }),
        ('Applicability', {
            'fields': (
                'billing_period',
                'min_amount_toman',
            )
        }),
        ('Usage Limits', {
            'fields': (
                'max_uses',
                'max_uses_per_user',
                'used_count',
            )
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Statistics', {
            'fields': ('usage_stats_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['activate_campaigns', 'deactivate_campaigns']
    
    def discount_display(self, obj):
        """Display discount in readable format"""
        if obj.discount_type == 'percentage':
            return f"{obj.discount_value}%"
        else:
            return f"{int(obj.discount_value):,} تومان"
    discount_display.short_description = 'Discount'
    
    def usage_stats(self, obj):
        """Display usage statistics"""
        if obj.max_uses:
            percentage = (obj.used_count / obj.max_uses) * 100
            color = 'green' if percentage < 80 else 'orange' if percentage < 95 else 'red'
            percentage_str = f"{int(percentage)}%"
            return format_html(
                '<span style="color: {};">{}/{} ({})</span>',
                color,
                obj.used_count,
                obj.max_uses,
                percentage_str
            )
        return format_html('{} استفاده', obj.used_count)
    usage_stats.short_description = 'Usage'
    
    def usage_stats_display(self, obj):
        """Detailed usage statistics"""
        from django.utils import timezone
        from django.db.models import Count
        
        usages = DiscountUsage.objects.filter(campaign=obj)
        total_usages = usages.count()
        unique_users = usages.values('user').distinct().count()
        
        # Recent usages (last 7 days)
        recent_usages = usages.filter(
            used_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()
        
        return format_html(
            '<div style="padding: 10px;">'
            '<strong>آمار استفاده:</strong><br>'
            '• کل استفاده‌ها: {}<br>'
            '• کاربران منحصر به فرد: {}<br>'
            '• استفاده‌های ۷ روز اخیر: {}<br>'
            '</div>',
            total_usages,
            unique_users,
            recent_usages
        )
    usage_stats_display.short_description = 'Usage Statistics'
    
    def activate_campaigns(self, request, queryset):
        """Activate selected campaigns"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} campaign(s) activated.')
    activate_campaigns.short_description = 'Activate selected campaigns'
    
    def deactivate_campaigns(self, request, queryset):
        """Deactivate selected campaigns"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} campaign(s) deactivated.')
    deactivate_campaigns.short_description = 'Deactivate selected campaigns'
    
    def save_model(self, request, obj, form, change):
        """Set created_by when creating new campaign"""
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DiscountUsage)
class DiscountUsageAdmin(admin.ModelAdmin):
    """Admin interface for Discount Usage tracking"""
    
    list_display = [
        'id',
        'campaign_code',
        'user_link',
        'discount_amount_display',
        'used_at',
        'payment_link',
    ]
    
    list_filter = [
        'campaign',
        'used_at',
    ]
    
    search_fields = [
        'campaign__code',
        'user__username',
        'user__email',
        'payment__track_id',
    ]
    
    readonly_fields = [
        'campaign',
        'user',
        'payment',
        'discount_amount_toman',
        'used_at',
    ]
    
    fieldsets = (
        ('Usage Information', {
            'fields': ('campaign', 'user', 'payment', 'discount_amount_toman', 'used_at')
        }),
    )
    
    def campaign_code(self, obj):
        """Display campaign code"""
        return obj.campaign.code
    campaign_code.short_description = 'Campaign Code'
    
    def user_link(self, obj):
        """Link to user in admin"""
        from django.urls import reverse
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def discount_amount_display(self, obj):
        """Display discount amount"""
        return f"{int(obj.discount_amount_toman):,} تومان"
    discount_amount_display.short_description = 'Discount Amount'
    
    def payment_link(self, obj):
        """Link to payment in admin"""
        if obj.payment:
            from django.urls import reverse
            url = reverse('admin:payments_premiumsubscriptionpayment_change', args=[obj.payment.id])
            return format_html('<a href="{}">Payment #{}</a>', url, obj.payment.id)
        return '-'
    payment_link.short_description = 'Payment'

