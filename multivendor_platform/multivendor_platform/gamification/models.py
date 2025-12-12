from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import VendorProfile

User = get_user_model()


class SupplierEngagement(models.Model):
    vendor_profile = models.OneToOneField(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='engagement'
    )
    total_points = models.PositiveIntegerField(default=0)
    today_points = models.PositiveIntegerField(default=0)
    current_streak_days = models.PositiveIntegerField(default=0)
    longest_streak_days = models.PositiveIntegerField(default=0)
    last_login = models.DateTimeField(blank=True, null=True)
    avg_response_minutes = models.FloatField(default=0)
    last_tip_shown = models.CharField(max_length=255, blank=True, null=True)
    endorsements_received = models.PositiveIntegerField(default=0, help_text='Number of peer endorsements received')
    positive_reviews_count = models.PositiveIntegerField(default=0, help_text='Count of positive reviews (rating >= 4)')
    reputation_score = models.FloatField(default=0.0, help_text='Calculated reputation score based on endorsements, reviews, and response speed')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Engagement for {self.vendor_profile.store_name}"


class Badge(models.Model):
    TIER_CHOICES = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    )
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=150)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='bronze')
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, default='form')
    criteria = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_tier_display()})"


class EarnedBadge(models.Model):
    vendor_profile = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='earned_badges'
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awards')
    achieved_at = models.DateTimeField(default=timezone.now)
    congratulation_message = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('vendor_profile', 'badge')
        ordering = ['-achieved_at']

    def __str__(self):
        return f"{self.vendor_profile.store_name} - {self.badge.title}"


class PointsHistory(models.Model):
    REASON_CHOICES = (
        ('login', 'Login'),
        ('product_save', 'Product Save'),
        ('profile_update', 'Profile Update'),
        ('mini_site', 'Mini Website Update'),
        ('fast_response', 'Fast Order Response'),
        ('tutorial', 'Watched Tutorial'),
        ('insight_share', 'Insight Share'),
        ('insight_comment', 'Insight Comment'),
        ('insight_like', 'Insight Liked'),
        ('badge', 'Badge Earned'),
        ('section_completion', 'Section Completion'),
        ('peer_invitation', 'Peer Invitation'),
        ('endorsement_received', 'Endorsement Received'),
        ('custom', 'Custom Action'),
    )
    vendor_profile = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='points_history'
    )
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=30, choices=REASON_CHOICES, default='custom')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor_profile.store_name} ({self.reason} +{self.points})"


class LeaderboardSnapshot(models.Model):
    PERIOD_CHOICES = (
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('overall', 'Overall'),
    )
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    data = models.JSONField(default=list, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.get_period_display()} snapshot @ {self.generated_at.date()}"


class Invitation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
    )
    inviter = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='sent_invitations'
    )
    invite_code = models.CharField(max_length=50, unique=True, db_index=True)
    invitee_email = models.EmailField(blank=True, null=True)
    invitee_phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    invitee = models.ForeignKey(
        VendorProfile,
        on_delete=models.SET_NULL,
        related_name='received_invitation',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invite_code']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"Invitation {self.invite_code} from {self.inviter.store_name} ({self.status})"


class InvitationBlockLog(models.Model):
    """Audit log for blocked invitation attempts (rate-limit or validation)."""
    inviter = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='invitation_block_logs'
    )
    invitee_email = models.EmailField(blank=True, null=True)
    invitee_phone = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='resolved_invitation_block_logs'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reason', 'created_at']),
        ]

    def __str__(self):
        return f"Blocked invite by {self.inviter.store_name} ({self.reason})"


class ReviewFlagLog(models.Model):
    """Track suspicious review flags for admin moderation."""
    vendor_profile = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='review_flag_logs'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reason = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    cleared = models.BooleanField(default=False)
    cleared_at = models.DateTimeField(blank=True, null=True)
    cleared_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='cleared_review_flag_logs'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reason', 'created_at']),
        ]

    def __str__(self):
        return f"Flagged review for {self.vendor_profile.store_name} ({self.reason})"


class Endorsement(models.Model):
    """Endorsement given by an invited user to their inviter"""
    endorser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='endorsements_given',
        help_text='User who gave the endorsement (invited user)'
    )
    endorsed = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='endorsements_received',
        help_text='Vendor profile that received the endorsement (inviter)'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('endorser', 'endorsed')
        indexes = [
            models.Index(fields=['endorsed', 'created_at']),
        ]

    def __str__(self):
        return f"{self.endorser.username} endorsed {self.endorsed.store_name}"


class SellerInsight(models.Model):
    vendor_profile = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='insights'
    )
    title = models.CharField(max_length=150)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_insights', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.vendor_profile.store_name}: {self.title[:30]}"

    @property
    def likes_count(self):
        return self.likes.count()


class SellerInsightComment(models.Model):
    insight = models.ForeignKey(
        SellerInsight,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    vendor_profile = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name='insight_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['insight', 'created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.vendor_profile.store_name} on {self.insight_id}"
