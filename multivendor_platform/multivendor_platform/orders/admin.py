from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'seller', 'price', 'quantity', 'subtotal']

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'buyer', 'status', 'total_amount', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['order_number', 'buyer__username', 'buyer__email']
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    actions = ['delete_selected']  # Include delete action
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

admin.site.register(Order, OrderAdmin)
