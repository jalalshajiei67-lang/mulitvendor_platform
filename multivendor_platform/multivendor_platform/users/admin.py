from django.contrib import admin
from .models import (
    UserProfile, BuyerProfile, VendorProfile, Supplier, SellerAd, SellerAdImage, 
    ProductReview, SupplierComment, UserActivity, SupplierPortfolioItem, 
    SupplierTeamMember, SupplierContactMessage, OTP
)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_verified', 'is_blocked', 'created_at']
    list_filter = ['role', 'is_verified', 'is_blocked']
    search_fields = ['user__username', 'user__email', 'phone']
    list_editable = ['is_blocked', 'is_verified']  # Allow inline editing
    actions = ['verify_users', 'block_users', 'unblock_users', 'delete_selected']
    
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} user(s) verified successfully.')
    verify_users.short_description = "✅ Verify selected users"
    
    def block_users(self, request, queryset):
        updated = queryset.update(is_blocked=True)
        self.message_user(request, f'{updated} user(s) blocked successfully.')
    block_users.short_description = "🚫 Block selected users"
    
    def unblock_users(self, request, queryset):
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f'{updated} user(s) unblocked successfully.')
    unblock_users.short_description = "🔓 Unblock selected users"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username', 'user__email']
    actions = ['delete_selected']  # Include delete action
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }
    
class SupplierPortfolioItemInline(admin.TabularInline):
    model = SupplierPortfolioItem
    extra = 1
    fields = ['title', 'image', 'project_date', 'category', 'sort_order', 'is_featured']
    verbose_name = "Portfolio Item"
    verbose_name_plural = "Portfolio Items"

class SupplierTeamMemberInline(admin.TabularInline):
    model = SupplierTeamMember
    extra = 1
    fields = ['name', 'position', 'photo', 'sort_order']
    verbose_name = "Team Member"
    verbose_name_plural = "Team Members"

class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'user', 'is_approved', 'contact_email', 'created_at']
    list_filter = ['is_approved']
    search_fields = ['store_name', 'user__username', 'contact_email']
    actions = ['approve_vendors', 'delete_selected']  # Include delete action
    inlines = [SupplierPortfolioItemInline, SupplierTeamMemberInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'store_name', 'logo', 'description', 'slogan')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'website', 'address')
        }),
        ('Company Details', {
            'fields': ('about', 'work_resume', 'successful_projects', 'history', 
                      'year_established', 'employee_count')
        }),
        ('Mini Website Branding', {
            'fields': ('banner_image', 'brand_color_primary', 'brand_color_secondary', 
                      'video_url'),
            'classes': ('collapse',)
        }),
        ('Certifications & Awards', {
            'fields': ('certifications', 'awards'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('social_media',),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_approved', 'created_at', 'updated_at'),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def approve_vendors(self, request, queryset):
        queryset.update(is_approved=True)
    approve_vendors.short_description = "Approve selected suppliers"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

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
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

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
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

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
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['user', 'action', 'description', 'ip_address', 'user_agent', 'content_type', 'object_id', 'created_at']
    actions = ['delete_selected']  # Include delete action
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

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
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

class SupplierPortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_profile', 'project_date', 'category', 'is_featured', 'sort_order']
    list_filter = ['is_featured', 'category', 'project_date']
    search_fields = ['title', 'description', 'vendor_profile__store_name', 'client_name']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_featured', 'unmark_featured', 'delete_selected']
    
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_featured.short_description = "Mark as featured"
    
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
    unmark_featured.short_description = "Unmark as featured"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

class SupplierTeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'vendor_profile', 'sort_order']
    list_filter = ['position']
    search_fields = ['name', 'position', 'vendor_profile__store_name', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['delete_selected']
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

class SupplierContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'vendor_profile', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender_name', 'sender_email', 'subject', 'message', 'vendor_profile__store_name']
    readonly_fields = ['vendor_profile', 'sender_name', 'sender_email', 'sender_phone', 'subject', 'message', 'created_at', 'updated_at']
    actions = ['mark_read', 'mark_unread', 'delete_selected']
    
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_read.short_description = "Mark as read"
    
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_unread.short_description = "Mark as unread"
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

class OTPAdmin(admin.ModelAdmin):
    list_display = ['phone', 'user', 'purpose', 'is_used', 'attempts', 'expires_at', 'created_at']
    list_filter = ['purpose', 'is_used', 'created_at', 'expires_at']
    search_fields = ['phone', 'user__username', 'code']
    readonly_fields = ['code', 'created_at', 'expires_at']
    actions = ['delete_selected']
    
    class Media:
        js = ('admin/js/fix_action_button.js',)
        css = {
            'all': ('admin/css/force_action_button.css',)
        }

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(BuyerProfile, BuyerProfileAdmin)
admin.site.register(VendorProfile, VendorProfileAdmin)
admin.site.register(SellerAd, SupplierAdAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(SupplierComment, SupplierCommentAdmin)
admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(SupplierPortfolioItem, SupplierPortfolioItemAdmin)
admin.site.register(SupplierTeamMember, SupplierTeamMemberAdmin)
admin.site.register(SupplierContactMessage, SupplierContactMessageAdmin)
admin.site.register(OTP, OTPAdmin)