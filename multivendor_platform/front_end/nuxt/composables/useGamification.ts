export const useGamificationApi = () => {
  return {
    fetchScores() {
      return useApiFetch<Record<string, any>>('gamification/score/', { method: 'GET' })
    },
    fetchEngagement() {
      return useApiFetch<{ engagement: any }>('gamification/engagement/', { method: 'GET' })
    },
    fetchBadges() {
      return useApiFetch<{ available: any[]; earned: any[] }>('gamification/badges/', { method: 'GET' })
    },
    fetchPoints() {
      return useApiFetch<{ results: any[] }>('gamification/points/', { method: 'GET' })
    },
    fetchLeaderboard(params: Record<string, any> = {}) {
      return useApiFetch<{ overall: any[] }>('gamification/leaderboard/', { method: 'GET', params })
    },
    trackAction(action: string, metadata: Record<string, any> = {}, points?: number) {
      return useApiFetch('gamification/track-action/', {
        method: 'POST',
        body: { action, metadata, points }
      })
    }
  }
}
