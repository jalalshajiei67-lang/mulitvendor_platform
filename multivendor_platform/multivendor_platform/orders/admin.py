from django import forms
from django.contrib import admin
from .models import Order, OrderItem, Payment, OrderImage


class OrderAdminForm(forms.ModelForm):
    """Ensure admin form keeps email optional."""

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'seller', 'price', 'quantity', 'subtotal']


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


class OrderImageInline(admin.TabularInline):
    model = OrderImage
    extra = 0
    readonly_fields = ['created_at']


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ['order_number', 'buyer', 'status', 'is_rfq', 'is_free', 'category', 'total_amount', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'is_rfq', 'is_free', 'category', 'created_at']
    search_fields = ['order_number', 'buyer__username', 'buyer__email', 'first_name', 'last_name', 'phone_number']
    inlines = [OrderItemInline, PaymentInline, OrderImageInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    actions = ['delete_selected']  # Include delete action
    filter_horizontal = ['suppliers']

    fieldsets = (
        ('اطلاعات سفارش/سرنخ', {
            'fields': ('order_number', 'is_rfq', 'is_free', 'status', 'lead_source', 'category', 'suppliers')
        }),
        ('اطلاعات تماس', {
            'fields': ('first_name', 'last_name', 'company_name', 'phone_number', 'email')
        }),
        ('نیاز مشتری', {
            'fields': ('unique_needs', 'notes')
        }),
        ('ارسال و پرداخت', {
            'fields': ('shipping_address', 'shipping_phone', 'payment_method', 'payment_date', 'is_paid', 'total_amount')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.setdefault('is_rfq', True)
        initial.setdefault('status', 'pending')
        return initial
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }


admin.site.register(Order, OrderAdmin)
