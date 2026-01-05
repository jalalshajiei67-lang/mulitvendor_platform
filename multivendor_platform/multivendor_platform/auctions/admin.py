from django.contrib import admin
from .models import ReverseAuction, AuctionInvitation, Bid


class BidInline(admin.TabularInline):
    """Inline admin for bids"""
    model = Bid
    extra = 0
    readonly_fields = ['supplier', 'amount', 'rank', 'is_winning', 'created_at']
    can_delete = False


class AuctionInvitationInline(admin.TabularInline):
    """Inline admin for invitations"""
    model = AuctionInvitation
    extra = 0
    readonly_fields = ['supplier', 'invited_at', 'viewed_at', 'notification_sent']
    can_delete = False


@admin.register(ReverseAuction)
class ReverseAuctionAdmin(admin.ModelAdmin):
    """Admin interface for reverse auctions"""
    list_display = ['title', 'buyer', 'category', 'starting_price', 'deadline', 'status', 'bid_count', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'deadline']
    search_fields = ['title', 'description', 'buyer__username', 'buyer__email']
    readonly_fields = ['created_at', 'updated_at', 'extended_count']
    inlines = [AuctionInvitationInline, BidInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('buyer', 'title', 'description', 'category')
        }),
        ('Pricing', {
            'fields': ('starting_price', 'reserve_price', 'minimum_decrement')
        }),
        ('Timing', {
            'fields': ('deadline', 'status', 'extended_count')
        }),
        ('Winner', {
            'fields': ('winner',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def bid_count(self, obj):
        """Display number of bids"""
        return obj.bids.count()
    bid_count.short_description = 'Bids'


@admin.register(AuctionInvitation)
class AuctionInvitationAdmin(admin.ModelAdmin):
    """Admin interface for auction invitations"""
    list_display = ['auction', 'supplier', 'invited_at', 'viewed_at', 'notification_sent']
    list_filter = ['invited_at', 'notification_sent', 'auction__status']
    search_fields = ['auction__title', 'supplier__username', 'supplier__email']
    readonly_fields = ['invited_at', 'viewed_at']


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """Admin interface for bids"""
    list_display = ['auction', 'supplier', 'amount', 'rank', 'is_winning', 'created_at']
    list_filter = ['is_winning', 'created_at', 'auction__status']
    search_fields = ['auction__title', 'supplier__username', 'supplier__email']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('auction', 'supplier')




