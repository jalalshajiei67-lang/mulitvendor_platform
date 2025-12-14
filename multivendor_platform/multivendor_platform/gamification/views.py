from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import secrets
import logging
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from .models import (
    Badge,
    EarnedBadge,
    SupplierEngagement,
    PointsHistory,
    Invitation,
    Endorsement,
    InvitationBlockLog,
    ReviewFlagLog,
    SellerInsight,
    SellerInsightComment,
)
from .serializers import (
    ScoreSerializer,
    SupplierEngagementSerializer,
    BadgeSerializer,
    EarnedBadgeSerializer,
    PointsHistorySerializer,
    InvitationSerializer,
    EndorsementSerializer,
    SellerInsightSerializer,
    SellerInsightCommentSerializer,
)
from .services import GamificationService, _get_vendor_profile
from users.models import SupplierComment, ProductReview
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


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
        earned_qs = vendor_profile.earned_badges.select_related('badge') if vendor_profile else EarnedBadge.objects.none()
        earned_slugs = {eb.badge.slug for eb in earned_qs}

        available = Badge.objects.filter(is_active=True)
        available_serialized = BadgeSerializer(
            available,
            many=True,
            context={'service': service, 'earned_slugs': earned_slugs},
        ).data

        earned_serialized = EarnedBadgeSerializer(
            earned_qs,
            many=True,
            context={'service': service, 'earned_slugs': earned_slugs},
        ).data

        return Response({
            'available': available_serialized,
            'earned': earned_serialized,
        })


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
        service = GamificationService.for_user(request.user)
        
        # Get all engagements ordered by points for ranking
        # We need all to calculate rank, but only return top 'limit' for display
        all_engagements = list(
            SupplierEngagement.objects.select_related('vendor_profile')
            .order_by('-total_points', 'id')
        )
        
        # Get current user's engagement
        user_engagement = service.get_or_create_engagement()
        user_rank = None
        user_tier = None
        user_points = 0
        ranks_to_next_tier = None
        next_tier_info = {}
        
        if user_engagement:
            user_points = user_engagement.total_points
            user_tier = service.calculate_tier(user_points, user_engagement.reputation_score)
            
            # Calculate user's rank (1-based)
            for idx, engagement in enumerate(all_engagements, start=1):
                if engagement.id == user_engagement.id:
                    user_rank = idx
                    break
            
            # Calculate ranks to next tier
            next_tier_info = service.get_next_tier_info(user_tier)
            if next_tier_info.get('name'):
                # Count how many users are between current user and next tier threshold
                next_threshold = next_tier_info.get('next_tier_threshold', 0)
                # Count users with points >= next threshold
                ranks_ahead = sum(1 for e in all_engagements if e.total_points >= next_threshold)
                if user_rank:
                    # How many ranks the user needs to move up to reach next tier
                    ranks_to_next_tier = max(0, ranks_ahead - user_rank + 1)
            else:
                ranks_to_next_tier = 0
        
        # Get top leaderboard entries for display
        leaderboard_entries = all_engagements[:limit]
        leaderboard_data = []
        for item in leaderboard_entries:
            tier = service.calculate_tier(item.total_points, item.reputation_score)
            leaderboard_data.append({
                'vendor': item.vendor_profile.store_name,
                'points': item.total_points,
                'streak': item.current_streak_days,
                'tier': tier,
                'reputation_score': item.reputation_score,
            })
        
        response_data = {
            'overall': leaderboard_data,
        }
        
        # Add user context if available
        if user_engagement:
            response_data['user_rank'] = user_rank
            response_data['user_tier'] = user_tier
            response_data['user_points'] = user_points
            response_data['user_reputation_score'] = user_engagement.reputation_score
            response_data['ranks_to_next_tier'] = ranks_to_next_tier
            response_data['next_tier'] = next_tier_info.get('name')
            response_data['next_tier_points_needed'] = next_tier_info.get('points_needed', 0)
        
        return Response(response_data)


class LowScoreCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = GamificationService.for_user(request.user)
        vendor_profile = service.vendor_profile

        engagement = service.get_or_create_engagement()
        points = engagement.total_points if engagement else 0
        reputation = engagement.reputation_score if engagement else 0
        tier = service.calculate_tier(points, reputation)
        is_premium = bool(getattr(getattr(request.user, 'profile', None), 'is_verified', False))

        return Response(
            {
                'low_score': tier == 'inactive' and not is_premium,
                'tier': tier,
                'is_premium': is_premium,
                'points': points,
                'reputation_score': reputation,
            }
        )


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
        
        rate_limit_response = self._check_award_rate_limit(request.user)
        if rate_limit_response:
            return rate_limit_response

        points_awarded = service.award_section_completion_points(section)
        
        return Response({
            'detail': 'points_awarded',
            'points': points_awarded,
            'section': section
        })

    def _check_award_rate_limit(self, user):
        """
        Limit section award calls to 10 per hour per user.
        """
        key = f"gamification:award:{user.id}"
        window_seconds = 60 * 60
        limit = 10
        now_ts = int(timezone.now().timestamp())
        data = cache.get(key)

        if not data or now_ts >= data.get('reset_at', 0):
            data = {'count': 0, 'reset_at': now_ts + window_seconds}

        if data['count'] >= limit:
            reset_in = data['reset_at'] - now_ts
            logger.info("Award rate limit hit for user %s", user.id)
            return Response(
                {
                    'detail': 'محدودیت اهدا امتیاز: لطفاً بعداً دوباره تلاش کنید.',
                    'remaining': 0,
                    'reset_in_seconds': max(0, reset_in),
                    'limit': limit,
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        data['count'] += 1
        cache.set(key, data, timeout=window_seconds)
        return None


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

        rate_limit_response = AwardSectionCompletionView()._check_award_rate_limit(request.user)
        if rate_limit_response:
            return rate_limit_response
        
        awarded = service.award_all_section_scores()
        total_awarded = sum(awarded.values())
        
        return Response({
            'detail': 'all_sections_processed',
            'sections': awarded,
            'total_points_awarded': total_awarded
        })


class GenerateInviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def permission_denied(self, request, message=None, code=None):
        if not request.user or not request.user.is_authenticated:
            raise exceptions.NotAuthenticated()
        return super().permission_denied(request, message=message, code=code)

    def post(self, request):
        """
        Generate a unique invite code for the current user.
        Returns the invite link that can be shared.
        """
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)

        invitee_email = request.data.get('invitee_email', None)
        invitee_phone = request.data.get('invitee_phone', None)
        daily_limit = getattr(settings, 'GAMIFICATION_INVITE_DAILY_LIMIT', 10)
        now = timezone.now()
        window_start = now - timedelta(days=1)
        recent_invites_qs = Invitation.objects.filter(
            inviter=service.vendor_profile,
            created_at__gte=window_start
        )
        recent_invite_count = recent_invites_qs.count()

        if recent_invite_count >= daily_limit:
            InvitationBlockLog.objects.create(
                inviter=service.vendor_profile,
                invitee_email=invitee_email,
                invitee_phone=invitee_phone,
                reason='invite_rate_limit'
            )
            return Response(
                {
                    'detail': f'حداکثر {daily_limit} دعوت در روز مجاز است. لطفاً فردا دوباره تلاش کنید.',
                    'remaining_invites': 0,
                    'limit': daily_limit,
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Self-referral prevention
        normalized_email = (invitee_email or '').strip().lower()
        inviter_emails = {
            (service.vendor_profile.contact_email or '').lower(),
            (getattr(request.user, 'email', '') or '').lower(),
        }
        inviter_phones = {
            (service.vendor_profile.contact_phone or '').strip(),
            (getattr(getattr(request.user, 'profile', None), 'phone', '') or '').strip(),
        }

        if normalized_email and normalized_email in inviter_emails:
            InvitationBlockLog.objects.create(
                inviter=service.vendor_profile,
                invitee_email=invitee_email,
                invitee_phone=invitee_phone,
                reason='self_referral'
            )
            return Response(
                {'detail': 'ارسال دعوت به خودتان مجاز نیست.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if invitee_phone and invitee_phone.strip() and invitee_phone.strip() in inviter_phones:
            InvitationBlockLog.objects.create(
                inviter=service.vendor_profile,
                invitee_email=invitee_email,
                invitee_phone=invitee_phone,
                reason='self_referral'
            )
            return Response(
                {'detail': 'ارسال دعوت به شماره تلفن خودتان مجاز نیست.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Circular invite check: if this vendor was invited by someone, they cannot invite that inviter back
        reverse_invite = Invitation.objects.filter(
            invitee=service.vendor_profile,
            status='accepted'
        ).select_related('inviter__user').first()
        if reverse_invite and normalized_email:
            reverse_inviter_email = (reverse_invite.inviter.user.email or '').lower()
            reverse_inviter_contact = (reverse_invite.inviter.contact_email or '').lower()
            if normalized_email in {reverse_inviter_email, reverse_inviter_contact}:
                InvitationBlockLog.objects.create(
                    inviter=service.vendor_profile,
                    invitee_email=invitee_email,
                    invitee_phone=invitee_phone,
                    reason='circular_invite'
                )
                return Response(
                    {'detail': 'دعوت دوطرفه مجاز نیست.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Generate unique invite code
        invite_code = secrets.token_urlsafe(16)
        
        # Ensure uniqueness
        while Invitation.objects.filter(invite_code=invite_code).exists():
            invite_code = secrets.token_urlsafe(16)
        
        # Create invitation
        invitation = Invitation.objects.create(
            inviter=service.vendor_profile,
            invite_code=invite_code,
            invitee_email=invitee_email,
            invitee_phone=invitee_phone,
            status='pending'
        )
        
        # Generate invite link
        # Get base URL from settings or request
        base_url = getattr(settings, 'FRONTEND_URL', request.build_absolute_uri('/'))
        if not base_url.endswith('/'):
            base_url += '/'
        invite_link = f"{base_url}register?ref={invite_code}"
        
        return Response({
            'invite_code': invite_code,
            'invite_link': invite_link,
            'invitation_id': invitation.id,
            'remaining_invites': max(0, daily_limit - (recent_invite_count + 1)),
            'limit': daily_limit,
        }, status=status.HTTP_201_CREATED)


class InvitationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def permission_denied(self, request, message=None, code=None):
        if not request.user or not request.user.is_authenticated:
            raise exceptions.NotAuthenticated()
        return super().permission_denied(request, message=message, code=code)

    def get(self, request):
        """
        Get list of invitations sent by the current user.
        Shows status and points earned from each.
        """
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        invitations = Invitation.objects.filter(
            inviter=service.vendor_profile
        ).select_related('invitee').order_by('-created_at')
        
        serializer = InvitationSerializer(invitations, many=True)
        
        # Calculate total points earned from invitations
        total_points = sum(
            100 for inv in invitations if inv.status == 'accepted'
        )

        daily_limit = 5
        window_start = timezone.now() - timedelta(days=1)
        recent_invite_count = Invitation.objects.filter(
            inviter=service.vendor_profile,
            created_at__gte=window_start
        ).count()
        remaining_invites = max(0, daily_limit - recent_invite_count)
        
        return Response({
            'invitations': serializer.data,
            'total_points_earned': total_points,
            'total_invitations': invitations.count(),
            'accepted_count': invitations.filter(status='accepted').count(),
            'pending_count': invitations.filter(status='pending').count(),
            'remaining_invites': remaining_invites,
            'invite_limit': daily_limit,
        })


class CanEndorseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Check if the current user can endorse their inviter.
        Returns whether they were invited and if they've already endorsed.
        """
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({
                'can_endorse': False,
                'reason': 'not_vendor'
            })
        
        # Check if user was invited
        invitation = Invitation.objects.filter(
            invitee=service.vendor_profile,
            status='accepted'
        ).first()
        
        if not invitation:
            return Response({
                'can_endorse': False,
                'reason': 'not_invited'
            })
        
        # Check if already endorsed
        if Endorsement.objects.filter(
            endorser=request.user,
            endorsed=invitation.inviter
        ).exists():
            return Response({
                'can_endorse': False,
                'reason': 'already_endorsed',
                'inviter_name': invitation.inviter.store_name
            })
        
        return Response({
            'can_endorse': True,
            'inviter_name': invitation.inviter.store_name
        })


class EndorseInviterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Allow a new user to endorse their inviter.
        Only works if the current user was invited and hasn't endorsed yet.
        Awards 50 points to the inviter.
        """
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user was invited
        try:
            invitation = Invitation.objects.filter(
                invitee=service.vendor_profile,
                status='accepted'
            ).first()
            
            if not invitation:
                return Response({
                    'detail': 'شما از طریق دعوت ثبت‌نام نکرده‌اید'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            inviter = invitation.inviter
            
            # Check if already endorsed
            if Endorsement.objects.filter(
                endorser=request.user,
                endorsed=inviter
            ).exists():
                return Response({
                    'detail': 'شما قبلاً این فروشنده را تأیید کرده‌اید'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create endorsement
            endorsement = Endorsement.objects.create(
                endorser=request.user,
                endorsed=inviter
            )
            
            # Increment endorsements_received on inviter's engagement
            inviter_engagement = GamificationService(inviter).get_or_create_engagement()
            if inviter_engagement:
                inviter_engagement.endorsements_received += 1
                inviter_engagement.save(update_fields=['endorsements_received', 'updated_at'])
            
            # Award 50 points to inviter (per Phase 6 spec)
            inviter_service = GamificationService(inviter)
            inviter_service.add_points('endorsement_received', 50, metadata={
                'endorser_username': request.user.username,
                'endorsement_id': endorsement.id
            })
            
            # Recalculate reputation score for inviter
            inviter_service.compute_reputation_score()
            
            serializer = EndorsementSerializer(endorsement)
            return Response({
                'detail': 'تأیید با موفقیت ثبت شد',
                'endorsement': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'detail': f'خطا در ثبت تأیید: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SellerInsightListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        qs = (
            SellerInsight.objects.select_related('vendor_profile__user')
            .prefetch_related('likes', 'comments')
            .order_by('-created_at')
        )
        total = qs.count()
        insights = qs[offset: offset + limit]
        serializer = SellerInsightSerializer(insights, many=True, context={'request': request})
        return Response({
            'count': total,
            'results': serializer.data,
            'limit': limit,
            'offset': offset,
        })

    def post(self, request):
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SellerInsightSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        insight = serializer.save(vendor_profile=service.vendor_profile)
        # Award points for sharing insight
        service.add_points('insight_share', 15, metadata={'insight_id': insight.id})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SellerInsightLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int):
        try:
            insight = SellerInsight.objects.select_related('vendor_profile').get(pk=pk)
        except SellerInsight.DoesNotExist:
            return Response({'detail': 'بینش یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        liked = insight.likes.filter(pk=request.user.pk).exists()
        if liked:
            insight.likes.remove(request.user)
            liked = False
        else:
            insight.likes.add(request.user)
            liked = True
            # Award points to author when someone else likes their insight
            if insight.vendor_profile and insight.vendor_profile.user != request.user:
                GamificationService(insight.vendor_profile).add_points(
                    'insight_like',
                    5,
                    metadata={'insight_id': insight.id, 'liked_by': request.user.id}
                )

        return Response({'liked': liked, 'likes_count': insight.likes.count()})


class SellerInsightCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk: int):
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        try:
            insight = SellerInsight.objects.get(pk=pk)
        except SellerInsight.DoesNotExist:
            return Response({'detail': 'بینش یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        comments_qs = insight.comments.select_related('vendor_profile__user').order_by('created_at')
        total = comments_qs.count()
        comments = comments_qs[offset: offset + limit]
        serializer = SellerInsightCommentSerializer(comments, many=True, context={'request': request})
        return Response({
            'count': total,
            'results': serializer.data,
            'limit': limit,
            'offset': offset,
        })

    def post(self, request, pk: int):
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            insight = SellerInsight.objects.get(pk=pk)
        except SellerInsight.DoesNotExist:
            return Response({'detail': 'بینش یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SellerInsightCommentSerializer(
            data={**request.data, 'insight': insight.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(vendor_profile=service.vendor_profile)
        # Award points to commenter
        service.add_points('insight_comment', 5, metadata={'insight_id': insight.id, 'comment_id': comment.id})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminGamificationFlagsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        flagged_supplier_comments = SupplierComment.objects.filter(
            is_flagged=True
        ).select_related('supplier', 'user')[:100]

        flagged_product_reviews = ProductReview.objects.filter(
            is_flagged=True
        ).select_related('product__vendor', 'buyer')[:100]

        invite_blocks = InvitationBlockLog.objects.filter(
            resolved=False
        ).select_related('inviter__user')[:100]

        supplier_data = [
            {
                'id': c.id,
                'vendor_id': c.supplier.id,
                'vendor_name': c.supplier.store_name,
                'reviewer': c.user.username,
                'rating': c.rating,
                'comment': c.comment,
                'flag_reason': c.flag_reason,
                'created_at': c.created_at,
            }
            for c in flagged_supplier_comments
        ]

        product_data = []
        for pr in flagged_product_reviews:
            vendor_profile = _get_vendor_profile(pr.product.vendor)
            product_data.append({
                'id': pr.id,
                'vendor_id': vendor_profile.id if vendor_profile else None,
                'vendor_name': vendor_profile.store_name if vendor_profile else '',
                'product': pr.product.name,
                'reviewer': pr.buyer.username,
                'rating': pr.rating,
                'comment': pr.comment,
                'flag_reason': pr.flag_reason,
                'created_at': pr.created_at,
            })

        invite_block_data = [
            {
                'id': b.id,
                'vendor_id': b.inviter.id,
                'vendor_name': b.inviter.store_name,
                'invitee_email': b.invitee_email,
                'invitee_phone': b.invitee_phone,
                'reason': b.reason,
                'created_at': b.created_at,
            }
            for b in invite_blocks
        ]

        return Response({
            'flagged_supplier_comments': supplier_data,
            'flagged_product_reviews': product_data,
            'invitation_blocks': invite_block_data,
        })


class AdminGamificationFlagActionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        object_type = request.data.get('object_type')
        object_id = request.data.get('id')

        if not object_type or not object_id:
            return Response({'detail': 'object_type و id الزامی هستند.'}, status=status.HTTP_400_BAD_REQUEST)

        if object_type == 'supplier_comment':
            return self._clear_supplier_comment_flag(request.user, object_id)
        if object_type == 'product_review':
            return self._clear_product_review_flag(request.user, object_id)
        if object_type == 'invitation_block':
            return self._resolve_invitation_block(request.user, object_id)

        return Response({'detail': 'object_type نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

    def _clear_supplier_comment_flag(self, admin_user, object_id):
        try:
            comment = SupplierComment.objects.select_related('supplier').get(id=object_id)
        except SupplierComment.DoesNotExist:
            return Response({'detail': 'نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        comment.is_flagged = False
        comment.flag_reason = None
        comment.save(update_fields=['is_flagged', 'flag_reason'])

        ReviewFlagLog.objects.filter(
            object_id=comment.id,
            content_type=ContentType.objects.get_for_model(SupplierComment),
            cleared=False
        ).update(cleared=True, cleared_at=timezone.now(), cleared_by=admin_user)

        GamificationService(comment.supplier).compute_reputation_score()
        return Response({'detail': 'پرچم پاک شد', 'id': comment.id})

    def _clear_product_review_flag(self, admin_user, object_id):
        try:
            review = ProductReview.objects.select_related('product__vendor').get(id=object_id)
        except ProductReview.DoesNotExist:
            return Response({'detail': 'بازبینی یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        review.is_flagged = False
        review.flag_reason = None
        review.save(update_fields=['is_flagged', 'flag_reason'])

        ReviewFlagLog.objects.filter(
            object_id=review.id,
            content_type=ContentType.objects.get_for_model(ProductReview),
            cleared=False
        ).update(cleared=True, cleared_at=timezone.now(), cleared_by=admin_user)

        vendor_profile = _get_vendor_profile(review.product.vendor)
        if vendor_profile:
            GamificationService(vendor_profile).compute_reputation_score()
        return Response({'detail': 'پرچم پاک شد', 'id': review.id})

    def _resolve_invitation_block(self, admin_user, object_id):
        try:
            block = InvitationBlockLog.objects.get(id=object_id)
        except InvitationBlockLog.DoesNotExist:
            return Response({'detail': 'رکورد یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        block.resolved = True
        block.resolved_at = timezone.now()
        block.resolved_by = admin_user
        block.save(update_fields=['resolved', 'resolved_at', 'resolved_by'])
        return Response({'detail': 'رکورد رسیدگی شد', 'id': block.id})


class GamificationDashboardView(APIView):
    """
    Single endpoint returning all dashboard data for the simplified gamification dashboard.
    Returns status, progress, current task, and leaderboard position.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = GamificationService.for_user(request.user)
        
        # If user doesn't have vendor_profile, try to create it if user is a seller
        if not service.vendor_profile:
            # Check if user is a seller and try to create vendor profile
            try:
                from users.models import UserProfile, VendorProfile
                profile = request.user.profile
                if profile.is_seller():
                    # Try to create vendor profile (signal should have done this, but ensure it exists)
                    import uuid
                    vendor_profile, created = VendorProfile.objects.get_or_create(
                        user=request.user,
                        defaults={
                            'store_name': f"فروشگاه_{request.user.username}_{uuid.uuid4().hex[:6]}",
                            'description': ''
                        }
                    )
                    # Re-initialize service with the new vendor profile
                    service = GamificationService.for_user(request.user)
            except (UserProfile.DoesNotExist, AttributeError, Exception):
                # User is not a seller or profile doesn't exist, return empty data
                pass
        
        # If still no vendor_profile, return empty/default data
        if not service.vendor_profile:
            return Response({
                'status': {
                    'tier': 'inactive',
                    'tier_display': 'غیرفعال',
                    'tier_color': 'grey',
                    'rank': None,
                    'total_points': 0,
                    'reputation_score': 0,
                    'current_streak_days': 0,
                    'avg_response_minutes': 0,
                },
                'progress': {
                    'overall_percentage': 0,
                    'milestones': [],
                    'required_steps_completed': 0,
                    'total_required_steps': 5
                },
                'current_task': None,
                'leaderboard_position': None
            })
        
        engagement = service.get_or_create_engagement()
        
        # Calculate tier and rank
        tier = service.calculate_tier()
        
        # Get all engagements for ranking
        all_engagements = list(
            SupplierEngagement.objects.select_related('vendor_profile')
            .order_by('-total_points', 'id')
        )
        
        user_rank = None
        if engagement:
            for idx, eng in enumerate(all_engagements, start=1):
                if eng.id == engagement.id:
                    user_rank = idx
                    break
        
        # Get progress and current task
        progress = service.get_overall_progress()
        current_task = service.get_current_task()
        
        return Response({
            'status': {
                'tier': tier,
                'tier_display': service.get_tier_display_name(tier),
                'tier_color': service.get_tier_color(tier),
                'rank': user_rank,
                'total_points': engagement.total_points if engagement else 0,
                'reputation_score': engagement.reputation_score if engagement else 0,
                'current_streak_days': engagement.current_streak_days if engagement else 0,
                'avg_response_minutes': engagement.avg_response_minutes if engagement else 0,
            },
            'progress': progress,
            'current_task': current_task,
            'leaderboard_position': user_rank
        })


class CompleteTaskView(APIView):
    """
    Mark task as completed, award points, return celebration data and next task.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task_type = request.data.get('task_type')
        metadata = request.data.get('metadata', {})
        
        if not task_type:
            return Response({'detail': 'نوع وظیفه الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = GamificationService.for_user(request.user)
        if not service.vendor_profile:
            return Response({'detail': 'فروشنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Map task types to point values and reasons
        task_points = {
            'profile': 50,
            'mini_website': 75,
            'products': 20,  # Per product or improvement
            'team': 50,
            'portfolio': 50,
            'invite': 100,
            'insights': 15,
            'onboarding_quest': 25  # Welcome tour completion
        }
        
        points_awarded = task_points.get(task_type, 0)
        
        # Award points if not already awarded for this specific action
        if points_awarded > 0:
            # Check if this is a unique action (e.g., adding a new product vs improving existing)
            should_award = True
            
            if task_type in ['profile', 'mini_website']:
                # For profile and mini_website, check if section score improved
                section_name = 'profile' if task_type == 'profile' else 'miniWebsite'
                awarded_points = service.award_section_completion_points(section_name)
                points_awarded = awarded_points
                should_award = awarded_points > 0
            
            if should_award and task_type not in ['profile', 'mini_website']:
                service.add_points(
                    reason='section_completion' if task_type in ['team', 'portfolio'] else task_type,
                    points=points_awarded,
                    metadata={**metadata, 'task_type': task_type}
                )
        
        # Get next task after completion
        next_task = service.get_current_task()
        
        # Get updated progress
        progress = service.get_overall_progress()
        
        return Response({
            'points_awarded': points_awarded,
            'celebration': points_awarded > 0,
            'next_task': next_task,
            'progress': progress,
            'message': f'عالی! {points_awarded} امتیاز دریافت کردید.' if points_awarded > 0 else 'وظیفه ثبت شد.'
        })
