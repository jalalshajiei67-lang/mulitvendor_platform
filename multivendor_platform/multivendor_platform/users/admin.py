from django.contrib import admin
from .models import UserProfile, BuyerProfile, VendorProfile, Supplier, SellerAd, SellerAdImage, ProductReview, SupplierComment, UserActivity

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_verified', 'is_blocked', 'created_at']
    list_filter = ['role', 'is_verified', 'is_blocked']
    search_fields = ['user__username', 'user__email', 'phone']
    actions = ['verify_users', 'block_users', 'unblock_users', 'delete_selected']  # Include delete action
    
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
    verify_users.short_description = "Verify selected users"
    
    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)
    block_users.short_description = "Block selected users"
    
    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)
    unblock_users.short_description = "Unblock selected users"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username', 'user__email']
    actions = ['delete_selected']  # Include delete action
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
    
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'user', 'is_approved', 'contact_email', 'created_at']
    list_filter = ['is_approved']
    search_fields = ['store_name', 'user__username', 'contact_email']
    actions = ['approve_vendors', 'delete_selected']  # Include delete action
    
    def approve_vendors(self, request, queryset):
        queryset.update(is_approved=True)
    approve_vendors.short_description = "Approve selected suppliers"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

class SupplierAdImageInline(admin.TabularInline):
    model = SellerAdImage
    extra = 1
    verbose_name = "Supplier Ad Image"
    verbose_name_plural = "Supplier Ad Images"

class SupplierAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description', 'seller__username']
    inlines = [SupplierAdImageInline]
    actions = ['delete_selected']  # Include delete action
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'product', 'rating', 'is_verified_purchase', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
    search_fields = ['buyer__username', 'product__name', 'title', 'comment']
    readonly_fields = ['buyer', 'product', 'order', 'created_at', 'updated_at']
    actions = ['approve_reviews', 'disapprove_reviews', 'delete_selected']  # Include delete action
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "Disapprove selected reviews"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

class SupplierCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'supplier', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['user__username', 'supplier__store_name', 'title', 'comment']
    readonly_fields = ['user', 'supplier', 'created_at', 'updated_at']
    actions = ['approve_comments', 'disapprove_comments', 'delete_selected']  # Include delete action
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Disapprove selected comments"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['user', 'action', 'description', 'ip_address', 'user_agent', 'content_type', 'object_id', 'created_at']
    actions = ['delete_selected']  # Include delete action
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'website', 'phone', 'email', 'is_active', 'get_product_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'website', 'phone', 'email', 'description')
    readonly_fields = ('get_product_count', 'created_at', 'updated_at')
    actions = ['delete_selected']  # Include delete action
    
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'website', 'description', 'logo')
        }),
        ('Contact Details', {
            'fields': ('phone', 'mobile', 'email', 'address')
        }),
        ('Management', {
            'fields': ('vendor', 'is_active', 'get_product_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_product_count(self, obj):
        return obj.get_product_count()
    get_product_count.short_description = 'Products'
    
    class Media:
        js = ('admin/js/fix_action_button.js',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(BuyerProfile, BuyerProfileAdmin)
admin.site.register(VendorProfile, VendorProfileAdmin)
admin.site.register(SellerAd, SupplierAdAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(SupplierComment, SupplierCommentAdmin)
admin.site.register(UserActivity, UserActivityAdmin)