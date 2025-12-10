import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useGamificationApi } from '~/composables/useGamification'

export type Metric = { key: string; label: string; tip: string; weight: number; passed: boolean }
export type ScorePayload = { title: string; score: number; metrics: Metric[]; tips: string[] }
export type Badge = { id: number; slug: string; title: string; tier: string; icon: string; description: string; category: string }
export type LeaderboardEntry = { vendor: string; points: number; streak: number; tier?: string }

export const useGamificationStore = defineStore('gamification', () => {
  const api = useGamificationApi()
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
  const lowScoreStatus = ref<{
    low_score: boolean
    tier: string | null
    is_premium: boolean
    points: number
    reputation_score: number
  }>({
    low_score: false,
    tier: null,
    is_premium: false,
    points: 0,
    reputation_score: 0
  })
  const ranksToNextTier = ref<number | null>(null)
  const nextTier = ref<string | null>(null)
  const nextTierPointsNeeded = ref<number>(0)
  const loading = ref(false)

  const fetchScores = async () => {
    loading.value = true
    try {
      const data = await api.fetchScores()
      scores.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  const fetchEngagement = async () => {
    const data = await api.fetchEngagement()
    engagement.value = data.engagement
    return engagement.value
  }

  const fetchBadges = async () => {
    const data = await api.fetchBadges()
    badges.value = data.available
    earnedBadges.value = data.earned
    return data
  }

  const fetchLowScoreStatus = async () => {
    const data = await api.fetchLowScoreCheck()
    lowScoreStatus.value = data
    return data
  }

  const fetchLeaderboard = async () => {
    const data = await api.fetchLeaderboard({ limit: 5 })
    leaderboard.value = data.overall
    userRank.value = data.user_rank ?? null
    userTier.value = data.user_tier ?? null
    ranksToNextTier.value = data.ranks_to_next_tier ?? null
    nextTier.value = data.next_tier ?? null
    nextTierPointsNeeded.value = data.next_tier_points_needed ?? 0
    return data.overall
  }

  const hydrate = async () => {
    await Promise.all([fetchScores(), fetchEngagement(), fetchBadges(), fetchLeaderboard(), fetchLowScoreStatus()])
  }

  const updateLocalScore = (key: string, payload: ScorePayload) => {
    scores.value = {
      ...scores.value,
      [key]: payload
    }
  }

  return {
    scores,
    engagement,
    badges,
    earnedBadges,
    leaderboard,
    userRank,
    userTier,
    ranksToNextTier,
    nextTier,
    nextTierPointsNeeded,
    lowScoreStatus,
    loading,
    fetchScores,
    fetchEngagement,
    fetchBadges,
    fetchLowScoreStatus,
    fetchLeaderboard,
    hydrate,
    updateLocalScore
  }
})
