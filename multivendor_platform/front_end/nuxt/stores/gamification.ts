import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useGamificationApi } from '~/composables/useGamification'
import { useGamificationDashboard, type DashboardData } from '~/composables/useGamificationDashboard'

// Legacy types for backward compatibility
export type Metric = { key: string; label: string; tip: string; weight: number; passed: boolean }
export type ScorePayload = { title: string; score: number; metrics: Metric[]; tips: string[] }
export type Badge = { id: number; slug: string; title: string; tier: string; icon: string; description: string; category: string }
export type LeaderboardEntry = { vendor: string; points: number; streak: number; tier?: string }

/**
 * Simplified Gamification Store
 * Now tracks only the new unified dashboard data
 * Legacy methods kept for backward compatibility
 */
export const useGamificationStore = defineStore('gamification', () => {
  const legacyApi = useGamificationApi()
  const dashboardApi = useGamificationDashboard()
  
  // NEW: Unified dashboard data
  const dashboardData = ref<DashboardData | null>(null)
  const loading = ref(false)
  
  // LEGACY: Keep for backward compatibility (will be deprecated)
  const scores = ref<Record<string, ScorePayload | null>>({
    product: null,
    profile: null,
    miniWebsite: null,
    portfolio: null,
    team: null
  })
  const engagement = ref<any | null>(null)
  const badges = ref<Badge[]>([])
  const earnedBadges = ref<any[]>([])
  const leaderboard = ref<LeaderboardEntry[]>([])
  const userRank = ref<number | null>(null)
  const userTier = ref<string | null>(null)

  /**
   * NEW: Fetch unified dashboard data
   * This is the main method to use going forward
   */
  const fetchDashboard = async () => {
    loading.value = true
    try {
      const result = await dashboardApi.fetchDashboardData()
      if (result.error.value) {
        console.error('Failed to fetch dashboard:', result.error.value)
        return null
      }
      if (result.data.value) {
        dashboardData.value = result.data.value
        
        // Update legacy state for backward compatibility
        userRank.value = result.data.value.leaderboard_position
        userTier.value = result.data.value.status.tier
        engagement.value = {
          total_points: result.data.value.status.total_points,
          reputation_score: result.data.value.status.reputation_score,
          current_streak_days: result.data.value.status.current_streak_days,
          avg_response_minutes: result.data.value.status.avg_response_minutes
        }
      }
      return dashboardData.value
    } finally {
      loading.value = false
    }
  }

  /**
   * Complete a task and update dashboard
   */
  const completeTask = async (taskType: string, metadata?: Record<string, any>) => {
    const result = await dashboardApi.completeTask(taskType, metadata)
    if (result.error.value) {
      console.error('Failed to complete task:', result.error.value)
      return null
    }
    
    // Refresh dashboard after task completion
    if (result.data.value) {
      await fetchDashboard()
    }
    
    return result.data.value
  }

  // LEGACY METHODS: Keep for backward compatibility, but use new API internally where possible
  const fetchScores = async () => {
    loading.value = true
    try {
      const data = await legacyApi.fetchScores()
      scores.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  const fetchEngagement = async () => {
    const data = await legacyApi.fetchEngagement()
    engagement.value = data.engagement
    return engagement.value
  }

  const fetchBadges = async () => {
    const data = await legacyApi.fetchBadges()
    badges.value = data.available
    earnedBadges.value = data.earned
    return data
  }

  const fetchLeaderboard = async () => {
    try {
      const data = await legacyApi.fetchLeaderboard({ limit: 10 })
      leaderboard.value = data.overall || []
      userRank.value = data.user_rank ?? null
      userTier.value = data.user_tier ?? null
      return data.overall || []
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error)
      return []
    }
  }

  /**
   * Hydrate the store with all data
   * NEW: Now primarily uses the unified dashboard endpoint
   */
  const hydrate = async () => {
    await fetchDashboard()
    // Optionally fetch badges separately if needed
    await fetchBadges()
  }

  const updateLocalScore = (key: string, payload: ScorePayload) => {
    scores.value = {
      ...scores.value,
      [key]: payload
    }
  }

  return {
    // NEW: Primary state
    dashboardData,
    loading,
    
    // NEW: Primary methods
    fetchDashboard,
    completeTask,
    hydrate,
    
    // LEGACY: For backward compatibility
    scores,
    engagement,
    badges,
    earnedBadges,
    leaderboard,
    userRank,
    userTier,
    fetchScores,
    fetchEngagement,
    fetchBadges,
    fetchLeaderboard,
    updateLocalScore
  }
})
