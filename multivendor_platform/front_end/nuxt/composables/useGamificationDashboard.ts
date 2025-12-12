/**
 * Simplified Gamification Dashboard Composable
 * Provides API access for the new 2-section dashboard
 */

export interface DashboardStatus {
  tier: string
  tier_display: string
  tier_color: string
  rank: number | null
  total_points: number
  reputation_score: number
  current_streak_days: number
  avg_response_minutes: number
}

export interface Milestone {
  name: string
  title: string
  completed: boolean
  score: number
  order: number
  current?: number
  target?: number
}

export interface DashboardProgress {
  overall_percentage: number
  milestones: Milestone[]
  required_steps_completed: number
  total_required_steps: number
}

export interface CurrentTask {
  type: string
  title: string
  description: string
  action_url: string
  points: number
  is_required: boolean
  icon: string
  milestone_name?: string
  current_progress?: number
  target_progress?: number
}

export interface DashboardData {
  status: DashboardStatus
  progress: DashboardProgress
  current_task: CurrentTask | null
  leaderboard_position: number | null
}

export interface TaskCompletionResponse {
  points_awarded: number
  celebration: boolean
  next_task: CurrentTask | null
  progress: DashboardProgress
  message: string
}

export const useGamificationDashboard = () => {
  return {
    /**
     * Fetch all dashboard data in one call
     */
    async fetchDashboardData() {
      const data = ref<DashboardData | null>(null)
      const error = ref<Error | null>(null)
      
      try {
        const result = await useApiFetch<DashboardData>('gamification/dashboard/', { 
          method: 'GET' 
        })
        data.value = result
      } catch (e: any) {
        error.value = e
      }
      
      return { data, error }
    },

    /**
     * Mark a task as completed
     */
    async completeTask(taskType: string, metadata?: Record<string, any>) {
      const data = ref<TaskCompletionResponse | null>(null)
      const error = ref<Error | null>(null)
      
      try {
        const result = await useApiFetch<TaskCompletionResponse>('gamification/tasks/complete/', {
          method: 'POST',
          body: { task_type: taskType, metadata: metadata || {} }
        })
        data.value = result
      } catch (e: any) {
        error.value = e
      }
      
      return { data, error }
    }
  }
}

