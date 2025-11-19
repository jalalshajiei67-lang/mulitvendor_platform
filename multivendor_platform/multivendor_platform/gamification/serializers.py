from rest_framework import serializers

from .models import Badge, EarnedBadge, SupplierEngagement, PointsHistory


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
        ]


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'slug', 'title', 'tier', 'icon', 'description', 'category', 'criteria']


class EarnedBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = EarnedBadge
        fields = ['id', 'badge', 'achieved_at', 'congratulation_message']


class PointsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsHistory
        fields = ['id', 'points', 'reason', 'metadata', 'created_at']
