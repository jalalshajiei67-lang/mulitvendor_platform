from django.urls import path
from .views import (
    GamificationScoreView,
    GamificationEngagementView,
    GamificationBadgesView,
    GamificationPointsView,
    GamificationLeaderboardView,
    TrackGamificationActionView,
)

urlpatterns = [
    path('score/', GamificationScoreView.as_view(), name='gamification-score'),
    path('engagement/', GamificationEngagementView.as_view(), name='gamification-engagement'),
    path('badges/', GamificationBadgesView.as_view(), name='gamification-badges'),
    path('points/', GamificationPointsView.as_view(), name='gamification-points'),
    path('leaderboard/', GamificationLeaderboardView.as_view(), name='gamification-leaderboard'),
    path('track-action/', TrackGamificationActionView.as_view(), name='gamification-track-action'),
]
