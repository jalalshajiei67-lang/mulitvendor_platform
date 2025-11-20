from django.urls import path
from .views import (
    GamificationScoreView,
    GamificationEngagementView,
    GamificationBadgesView,
    GamificationPointsView,
    GamificationLeaderboardView,
    TrackGamificationActionView,
    AwardSectionCompletionView,
    AwardAllSectionsView,
)

urlpatterns = [
    path('score/', GamificationScoreView.as_view(), name='gamification-score'),
    path('engagement/', GamificationEngagementView.as_view(), name='gamification-engagement'),
    path('badges/', GamificationBadgesView.as_view(), name='gamification-badges'),
    path('points/', GamificationPointsView.as_view(), name='gamification-points'),
    path('leaderboard/', GamificationLeaderboardView.as_view(), name='gamification-leaderboard'),
    path('track-action/', TrackGamificationActionView.as_view(), name='gamification-track-action'),
    path('award-section/', AwardSectionCompletionView.as_view(), name='gamification-award-section'),
    path('award-all-sections/', AwardAllSectionsView.as_view(), name='gamification-award-all-sections'),
]
