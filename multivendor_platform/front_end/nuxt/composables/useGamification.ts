export interface SellerInsight {
  id: number
  title: string
  content: string
  author_name?: string
  created_at?: string
  likes_count?: number
  liked_by_me?: boolean
  comments_count?: number
}

export interface SellerInsightPayload {
  title: string
  content: string
}

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
    fetchLowScoreCheck() {
      return useApiFetch<{
        low_score: boolean
        tier: string
        is_premium: boolean
        points: number
        reputation_score: number
      }>('gamification/low-score-check/', { method: 'GET' })
    },
    fetchPoints() {
      return useApiFetch<{ results: any[] }>('gamification/points/', { method: 'GET' })
    },
    fetchLeaderboard(params: Record<string, any> = {}) {
      return useApiFetch<{
        overall: any[]
        user_rank?: number
        user_tier?: string
        user_points?: number
        ranks_to_next_tier?: number
        next_tier?: string | null
        next_tier_points_needed?: number
      }>('gamification/leaderboard/', { method: 'GET', params })
    },
    trackAction(action: string, metadata: Record<string, any> = {}, points?: number) {
      return useApiFetch('gamification/track-action/', {
        method: 'POST',
        body: { action, metadata, points }
      })
    },
    generateInviteCode(inviteeEmail?: string) {
      return useApiFetch<{
        invite_code: string
        invite_link: string
        invitation_id: number
        remaining_invites?: number
        limit?: number
      }>('gamification/invite/generate/', {
        method: 'POST',
        body: inviteeEmail ? { invitee_email: inviteeEmail } : {}
      })
    },
    getInvitationStatus() {
      return useApiFetch<{
        invitations: Array<{
          id: number
          invite_code: string
          invitee_email: string | null
          invitee_phone?: string | null
          status: string
          created_at: string
          accepted_at: string | null
          inviter_name: string
          invitee_name: string | null
          points_earned: number
        }>
        total_points_earned: number
        total_invitations: number
        accepted_count: number
        pending_count: number
        remaining_invites: number
        invite_limit: number
      }>('gamification/invite/status/', { method: 'GET' })
    },
    endorseInviter() {
      return useApiFetch<{
        detail: string
        endorsement: {
          id: number
          endorser: number
          endorsed: number
          endorser_username: string
          endorsed_store_name: string
          created_at: string
        }
      }>('gamification/endorse/', { method: 'POST' })
    },
    canEndorse() {
      return useApiFetch<{
        can_endorse: boolean
        reason?: 'not_vendor' | 'not_invited' | 'already_endorsed'
        inviter_name?: string
      }>('gamification/can-endorse/', { method: 'GET' })
    },
    fetchSellerInsights(params: Record<string, any> = {}) {
      return useApiFetch<{ results?: SellerInsight[] }>('gamification/insights/', {
        method: 'GET',
        params
      })
    },
    createSellerInsight(payload: SellerInsightPayload) {
      return useApiFetch<SellerInsight>('gamification/insights/', {
        method: 'POST',
        body: payload
      })
    },
    likeSellerInsight(id: number) {
      return useApiFetch<{ liked: boolean; likes_count: number }>(`gamification/insights/${id}/like/`, {
        method: 'POST'
      })
    },
    fetchSellerInsightComments(insightId: number, params: Record<string, any> = {}) {
      return useApiFetch<{ results?: Array<{ id: number; content: string; author_name?: string; created_at?: string }> }>(
        `gamification/insights/${insightId}/comments/`,
        { method: 'GET', params }
      )
    },
    createSellerInsightComment(insightId: number, content: string) {
      return useApiFetch<{ id: number; content: string; author_name?: string; created_at?: string }>(
        `gamification/insights/${insightId}/comments/`,
        {
          method: 'POST',
          body: { content }
        }
      )
    },
    getBadgeProgress(badges: any[], slug: string) {
      const targetBadge = badges.find((badge: any) => {
        const currentSlug = badge.slug || badge?.badge?.slug
        return currentSlug === slug
      })
      const progress = targetBadge?.progress || targetBadge?.badge?.progress
      return progress || { current: 0, target: 0, percentage: 0 }
    }
  }
}
