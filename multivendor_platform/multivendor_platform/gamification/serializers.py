from rest_framework import serializers

from .models import (
    Badge,
    EarnedBadge,
    SupplierEngagement,
    PointsHistory,
    Invitation,
    Endorsement,
    SellerInsight,
    SellerInsightComment,
)


class MetricSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()
    tip = serializers.CharField()
    weight = serializers.FloatField()
    passed = serializers.BooleanField()


class ScoreSerializer(serializers.Serializer):
    title = serializers.CharField()
    score = serializers.IntegerField()
    metrics = MetricSerializer(many=True)
    tips = serializers.ListField(child=serializers.CharField(), allow_empty=True)


class SupplierEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierEngagement
        fields = [
            'total_points',
            'today_points',
            'current_streak_days',
            'longest_streak_days',
            'last_login',
            'avg_response_minutes',
            'last_tip_shown',
            'endorsements_received',
            'positive_reviews_count',
            'reputation_score',
        ]


class BadgeSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    is_earned = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = [
            'id',
            'slug',
            'title',
            'tier',
            'icon',
            'description',
            'category',
            'criteria',
            'progress',
            'is_earned',
        ]

    def get_progress(self, obj):
        service = self.context.get('service')
        if not service:
            return None
        return service.get_badge_progress(obj)

    def get_is_earned(self, obj):
        earned_slugs = self.context.get('earned_slugs') or set()
        return obj.slug in earned_slugs


class EarnedBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    achieved_at_display = serializers.SerializerMethodField()

    class Meta:
        model = EarnedBadge
        fields = ['id', 'badge', 'achieved_at', 'achieved_at_display', 'congratulation_message']

    def get_achieved_at_display(self, obj):
        return obj.achieved_at.strftime('%Y-%m-%d %H:%M')


class PointsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsHistory
        fields = ['id', 'points', 'reason', 'metadata', 'created_at']


class InvitationSerializer(serializers.ModelSerializer):
    inviter_name = serializers.CharField(source='inviter.store_name', read_only=True)
    invitee_name = serializers.CharField(source='invitee.store_name', read_only=True, allow_null=True)
    points_earned = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = [
            'id', 'invite_code', 'invitee_email', 'invitee_phone', 'status', 
            'created_at', 'accepted_at', 'inviter_name', 'invitee_name', 'points_earned'
        ]
        read_only_fields = ['invite_code', 'created_at', 'accepted_at', 'points_earned']

    def get_points_earned(self, obj):
        """Calculate points earned from this invitation"""
        if obj.status == 'accepted':
            # Points are awarded when invitation is accepted (100 points per Phase 5 spec)
            return 100
        return 0


class EndorsementSerializer(serializers.ModelSerializer):
    endorser_username = serializers.CharField(source='endorser.username', read_only=True)
    endorsed_store_name = serializers.CharField(source='endorsed.store_name', read_only=True)

    class Meta:
        model = Endorsement
        fields = ['id', 'endorser', 'endorsed', 'endorser_username', 'endorsed_store_name', 'created_at']
        read_only_fields = ['created_at']


class SellerInsightSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    liked_by_me = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = SellerInsight
        fields = [
            'id',
            'title',
            'content',
            'author_name',
            'created_at',
            'likes_count',
            'liked_by_me',
            'comments_count',
        ]
        read_only_fields = ['id', 'author_name', 'created_at', 'likes_count', 'liked_by_me', 'comments_count']

    def get_author_name(self, obj: SellerInsight):
        return getattr(obj.vendor_profile, 'store_name', '') or getattr(getattr(obj.vendor_profile, 'user', None), 'username', 'فروشنده')

    def get_liked_by_me(self, obj: SellerInsight):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return obj.likes.filter(pk=request.user.pk).exists()

    def get_comments_count(self, obj: SellerInsight):
        return obj.comments.count()

    def validate_title(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('عنوان الزامی است.')
        if len(value) > 150:
            raise serializers.ValidationError('عنوان نباید بیشتر از ۱۵۰ کاراکتر باشد.')
        return value

    def validate_content(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('متن بینش الزامی است.')
        if len(value) > 2000:
            raise serializers.ValidationError('متن نباید بیشتر از ۲۰۰۰ کاراکتر باشد.')
        return value


class SellerInsightCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = SellerInsightComment
        fields = ['id', 'insight', 'content', 'author_name', 'created_at']
        read_only_fields = ['id', 'author_name', 'created_at']

    def get_author_name(self, obj: SellerInsightComment):
        return getattr(obj.vendor_profile, 'store_name', '') or getattr(getattr(obj.vendor_profile, 'user', None), 'username', 'فروشنده')

    def validate_content(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('متن نظر الزامی است.')
        if len(value) > 1000:
            raise serializers.ValidationError('متن نباید بیشتر از ۱۰۰۰ کاراکتر باشد.')
        return value
