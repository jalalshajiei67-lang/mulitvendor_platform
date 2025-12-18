from django.contrib import admin
from .models import (
    AuctionRequest, AuctionPhoto, AuctionDocument, Bid,
    AuctionDepositPayment, AuctionReport, AuctionNotification
)


class AuctionPhotoInline(admin.TabularInline):
    model = AuctionPhoto
    extra = 0
    fields = ['image', 'uploaded_at']
    readonly_fields = ['uploaded_at']


class AuctionDocumentInline(admin.TabularInline):
    model = AuctionDocument
    extra = 0
    fields = ['file', 'file_name', 'uploaded_at']
    readonly_fields = ['uploaded_at']


class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    fields = ['seller', 'price', 'is_winner', 'rank', 'created_at']
    readonly_fields = ['created_at']
    can_delete = False


@admin.register(AuctionRequest)
class AuctionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'product', 'subcategory', 'status', 'request_type', 
                   'deposit_status', 'auction_style', 'created_at']
    list_filter = ['status', 'request_type', 'deposit_status', 'auction_style', 'created_at']
    search_fields = ['buyer__username', 'buyer__email', 'product__name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'closed_at']
    inlines = [AuctionPhotoInline, AuctionDocumentInline, BidInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('buyer', 'product', 'subcategory', 'status', 'request_type')
        }),
        ('Deposit Information', {
            'fields': ('deposit_amount', 'deposit_status', 'deposit_payment')
        }),
        ('Auction Configuration', {
            'fields': ('auction_style', 'start_time', 'end_time')
        }),
        ('Content', {
            'fields': ('description', 'technical_specs')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'reviewed_by', 'reviewed_at', 'winner')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'closed_at')
        }),
    )
    
    actions = ['approve_auctions', 'reject_auctions', 'activate_auctions']
    
    def approve_auctions(self, request, queryset):
        """Approve selected auctions"""
        from django.utils import timezone
        from .models import AuctionNotification
        
        auctions_to_approve = queryset.filter(status='pending_review')
        updated = 0
        
        for auction in auctions_to_approve:
            auction.status = 'approved'
            auction.reviewed_by = request.user
            auction.reviewed_at = timezone.now()
            auction.save()
            
            # Send notification to buyer
            AuctionNotification.objects.create(
                auction=auction,
                user=auction.buyer,
                notification_type='auction_approved',
                message=f'درخواست مناقصه #{auction.id} شما تایید شد'
            )
            updated += 1
        
        self.message_user(request, f'{updated} auction(s) approved.')
    approve_auctions.short_description = 'Approve selected auctions'
    
    def reject_auctions(self, request, queryset):
        """Reject selected auctions"""
        from django.utils import timezone
        from .models import AuctionNotification
        
        auctions_to_reject = queryset.filter(status='pending_review')
        updated = 0
        
        for auction in auctions_to_reject:
            auction.status = 'rejected'
            auction.reviewed_by = request.user
            auction.reviewed_at = timezone.now()
            auction.save()
            
            # Send notification to buyer
            AuctionNotification.objects.create(
                auction=auction,
                user=auction.buyer,
                notification_type='auction_rejected',
                message=f'درخواست مناقصه #{auction.id} شما رد شد'
            )
            updated += 1
        
        self.message_user(request, f'{updated} auction(s) rejected.')
    reject_auctions.short_description = 'Reject selected auctions'
    
    def activate_auctions(self, request, queryset):
        """Activate approved auctions"""
        # Use save() instead of update() to trigger signals
        auctions_to_activate = queryset.filter(status='approved')
        updated = 0
        
        for auction in auctions_to_activate:
            auction.status = 'active'
            auction.save(update_fields=['status'])
            # Signal will handle notifications to sellers
            updated += 1
        
        self.message_user(request, f'{updated} auction(s) activated.')
    activate_auctions.short_description = 'Activate approved auctions'


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['id', 'auction', 'seller', 'price', 'is_winner', 'rank', 'created_at']
    list_filter = ['is_winner', 'created_at']
    search_fields = ['seller__username', 'auction__id', 'additional_notes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Bid Information', {
            'fields': ('auction', 'seller', 'price')
        }),
        ('Technical Compliance', {
            'fields': ('technical_compliance', 'additional_notes')
        }),
        ('Status', {
            'fields': ('is_winner', 'rank')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(AuctionDepositPayment)
class AuctionDepositPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'auction', 'user', 'amount', 'status', 'track_id', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'track_id', 'order_id', 'ref_number']
    readonly_fields = ['created_at', 'paid_at', 'verified_at', 'order_id']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('auction', 'user', 'amount', 'status', 'payment_method')
        }),
        ('Zibal Tracking', {
            'fields': ('track_id', 'order_id', 'ref_number', 'card_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'paid_at', 'verified_at')
        }),
        ('Additional Info', {
            'fields': ('description', 'zibal_response')
        }),
    )


@admin.register(AuctionReport)
class AuctionReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'auction', 'admin', 'created_at']
    list_filter = ['created_at']
    search_fields = ['auction__id', 'admin__username', 'report_text']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('auction', 'admin', 'report_text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(AuctionNotification)
class AuctionNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'auction', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('auction', 'user', 'notification_type', 'message', 'is_read')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


# Register inline models
admin.site.register(AuctionPhoto)
admin.site.register(AuctionDocument)
