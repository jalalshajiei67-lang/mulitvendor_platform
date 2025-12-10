from django.contrib import admin
from .models import (
    SupplierEngagement,
    Badge,
    EarnedBadge,
    PointsHistory,
    LeaderboardSnapshot,
    Invitation,
    Endorsement,
    InvitationBlockLog,
    ReviewFlagLog,
)


@admin.register(SupplierEngagement)
class SupplierEngagementAdmin(admin.ModelAdmin):
    list_display = ('vendor_profile', 'total_points', 'current_streak_days', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('vendor_profile__store_name', 'vendor_profile__user__username')
    readonly_fields = ('updated_at',)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tier', 'category', 'is_active')
    list_filter = ('tier', 'category', 'is_active')
    search_fields = ('title', 'slug', 'description')


@admin.register(EarnedBadge)
class EarnedBadgeAdmin(admin.ModelAdmin):
    list_display = ('vendor_profile', 'badge', 'achieved_at')
    list_filter = ('badge__tier', 'achieved_at')
    search_fields = ('vendor_profile__store_name', 'badge__title')
    readonly_fields = ('achieved_at',)


@admin.register(PointsHistory)
class PointsHistoryAdmin(admin.ModelAdmin):
    list_display = ('vendor_profile', 'points', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('vendor_profile__store_name',)
    readonly_fields = ('created_at',)


@admin.register(LeaderboardSnapshot)
class LeaderboardSnapshotAdmin(admin.ModelAdmin):
    list_display = ('period', 'generated_at')
    list_filter = ('period', 'generated_at')
    readonly_fields = ('generated_at',)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('invite_code', 'inviter', 'invitee', 'status', 'created_at', 'accepted_at')
    list_filter = ('status', 'created_at', 'accepted_at')
    search_fields = ('invite_code', 'inviter__store_name', 'invitee_email')
    readonly_fields = ('created_at', 'accepted_at')
    raw_id_fields = ('inviter', 'invitee')


@admin.register(Endorsement)
class EndorsementAdmin(admin.ModelAdmin):
    list_display = ('endorser', 'endorsed', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('endorser__username', 'endorsed__store_name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('endorser', 'endorsed')


@admin.register(InvitationBlockLog)
class InvitationBlockLogAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invitee_email', 'invitee_phone', 'reason', 'resolved', 'created_at')
    list_filter = ('reason', 'resolved', 'created_at')
    search_fields = ('inviter__store_name', 'invitee_email', 'invitee_phone')
    readonly_fields = ('created_at',)
    raw_id_fields = ('inviter', 'resolved_by')


@admin.register(ReviewFlagLog)
class ReviewFlagLogAdmin(admin.ModelAdmin):
    list_display = ('vendor_profile', 'reason', 'cleared', 'created_at')
    list_filter = ('reason', 'cleared', 'created_at')
    search_fields = ('vendor_profile__store_name',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('vendor_profile', 'cleared_by')

