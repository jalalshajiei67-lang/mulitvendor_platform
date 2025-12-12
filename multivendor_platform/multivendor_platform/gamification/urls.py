from django.urls import path
from .views import (
    GamificationScoreView,
    GamificationEngagementView,
    GamificationBadgesView,
    GamificationPointsView,
    GamificationLeaderboardView,
    LowScoreCheckView,
    TrackGamificationActionView,
    AwardSectionCompletionView,
    AwardAllSectionsView,
    GenerateInviteCodeView,
    InvitationStatusView,
    EndorseInviterView,
    CanEndorseView,
    AdminGamificationFlagsView,
    AdminGamificationFlagActionView,
    SellerInsightListCreateView,
    SellerInsightLikeView,
    SellerInsightCommentView,
    GamificationDashboardView,
    CompleteTaskView,
)

urlpatterns = [
    # New simplified dashboard endpoints
    path('dashboard/', GamificationDashboardView.as_view(), name='gamification-dashboard'),
    path('tasks/complete/', CompleteTaskView.as_view(), name='gamification-task-complete'),
    
    # Legacy endpoints (keep for backward compatibility)
    path('score/', GamificationScoreView.as_view(), name='gamification-score'),
    path('engagement/', GamificationEngagementView.as_view(), name='gamification-engagement'),
    path('badges/', GamificationBadgesView.as_view(), name='gamification-badges'),
    path('points/', GamificationPointsView.as_view(), name='gamification-points'),
    path('leaderboard/', GamificationLeaderboardView.as_view(), name='gamification-leaderboard'),
    path('low-score-check/', LowScoreCheckView.as_view(), name='gamification-low-score-check'),
    path('track-action/', TrackGamificationActionView.as_view(), name='gamification-track-action'),
    path('award-section/', AwardSectionCompletionView.as_view(), name='gamification-award-section'),
    path('award-all-sections/', AwardAllSectionsView.as_view(), name='gamification-award-all-sections'),
    path('invite/generate/', GenerateInviteCodeView.as_view(), name='gamification-invite-generate'),
    path('invite/status/', InvitationStatusView.as_view(), name='gamification-invite-status'),
    path('endorse/', EndorseInviterView.as_view(), name='gamification-endorse'),
    path('can-endorse/', CanEndorseView.as_view(), name='gamification-can-endorse'),
    path('admin/flags/', AdminGamificationFlagsView.as_view(), name='gamification-admin-flags'),
    path('admin/flags/clear/', AdminGamificationFlagActionView.as_view(), name='gamification-admin-flags-clear'),
    path('insights/', SellerInsightListCreateView.as_view(), name='gamification-insights'),
    path('insights/<int:pk>/like/', SellerInsightLikeView.as_view(), name='gamification-insights-like'),
    path('insights/<int:pk>/comments/', SellerInsightCommentView.as_view(), name='gamification-insights-comments'),
]
