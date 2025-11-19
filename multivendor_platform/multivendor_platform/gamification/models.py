from django.db import models
from django.utils import timezone
from users.models import VendorProfile


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
        ('badge', 'Badge Earned'),
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
