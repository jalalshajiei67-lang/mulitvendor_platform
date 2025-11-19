import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useGamificationApi } from '~/composables/useGamification'

export type Metric = { key: string; label: string; tip: string; weight: number; passed: boolean }
export type ScorePayload = { title: string; score: number; metrics: Metric[]; tips: string[] }
export type Badge = { id: number; slug: string; title: string; tier: string; icon: string; description: string; category: string }
export type LeaderboardEntry = { vendor: string; points: number; streak: number }

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

  const fetchLeaderboard = async () => {
    const data = await api.fetchLeaderboard({ limit: 5 })
    leaderboard.value = data.overall
    return data.overall
  }

  const hydrate = async () => {
    await Promise.all([fetchScores(), fetchEngagement(), fetchBadges(), fetchLeaderboard()])
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
    loading,
    fetchScores,
    fetchEngagement,
    fetchBadges,
    fetchLeaderboard,
    hydrate,
    updateLocalScore
  }
})
