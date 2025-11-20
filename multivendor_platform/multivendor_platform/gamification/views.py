from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Badge, SupplierEngagement, PointsHistory
from .serializers import (
    ScoreSerializer,
    SupplierEngagementSerializer,
    BadgeSerializer,
    EarnedBadgeSerializer,
    PointsHistorySerializer,
)
from .services import GamificationService


class GamificationScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = GamificationService.for_user(request.user)
        scores = {
            'product': service.compute_product_score(),
            'profile': service.compute_profile_score(),
            'miniWebsite': service.compute_mini_site_score(),
            'portfolio': service.compute_portfolio_score(),
            'team': service.compute_team_score(),
        }
        serialized = {key: ScoreSerializer(value).data for key, value in scores.items()}
        return Response(serialized)


class GamificationEngagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = GamificationService.for_user(request.user)
        engagement = service.get_or_create_engagement()
        serializer = SupplierEngagementSerializer(engagement) if engagement else None
        return Response({
            'engagement': serializer.data if serializer else None,
        })


class GamificationBadgesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = GamificationService.for_user(request.user)
        vendor_profile = service.vendor_profile
        earned = vendor_profile.earned_badges.select_related('badge') if vendor_profile else []
        payload = {
            'available': BadgeSerializer(Badge.objects.filter(is_active=True), many=True).data,
            'earned': EarnedBadgeSerializer(earned, many=True).data,
        }
        return Response(payload)


class GamificationPointsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = GamificationService.for_user(request.user)
        vendor_profile = service.vendor_profile
        history = vendor_profile.points_history.all()[:50] if vendor_profile else PointsHistory.objects.none()
        serializer = PointsHistorySerializer(history, many=True)
        return Response({
            'results': serializer.data,
        })


class GamificationLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        leaderboard = (
            SupplierEngagement.objects.select_related('vendor_profile')
            .order_by('-total_points')[:limit]
        )
        data = [
            {
                'vendor': item.vendor_profile.store_name,
                'points': item.total_points,
                'streak': item.current_streak_days,
            }
            for item in leaderboard
        ]
        return Response({'overall': data})


class TrackGamificationActionView(APIView):
    permission_classes = [IsAuthenticated]

    ACTION_POINTS = {
        'login': 5,
        'product_save': 20,
        'profile_update': 15,
        'mini_site': 15,
        'fast_response': 20,
        'tutorial': 10,
    }

    def post(self, request):
        action = request.data.get('action')
        if not action:
            return Response({'detail': 'Action is required'}, status=status.HTTP_400_BAD_REQUEST)
        points = int(request.data.get('points') or self.ACTION_POINTS.get(action, 0))
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        service.add_points(action, points, metadata=request.data.get('metadata'))
        return Response({'detail': 'recorded', 'points': points})


class AwardSectionCompletionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        section = request.data.get('section')
        if not section:
            return Response({'detail': 'Section is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        valid_sections = ['profile', 'product', 'miniWebsite', 'portfolio', 'team']
        if section not in valid_sections:
            return Response(
                {'detail': f'Invalid section. Must be one of: {", ".join(valid_sections)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        points_awarded = service.award_section_completion_points(section)
        
        return Response({
            'detail': 'points_awarded',
            'points': points_awarded,
            'section': section
        })


class AwardAllSectionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Award points for all sections based on their current completion scores.
        This ensures all section scores are accumulated into the total score.
        """
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        awarded = service.award_all_section_scores()
        total_awarded = sum(awarded.values())
        
        return Response({
            'detail': 'all_sections_processed',
            'sections': awarded,
            'total_points_awarded': total_awarded
        })
