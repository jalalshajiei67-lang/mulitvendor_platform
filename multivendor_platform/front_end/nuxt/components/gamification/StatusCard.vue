<template>
  <v-card elevation="3" rounded="xl" class="status-card overflow-visible">
    <!-- Gradient Header -->
    <div class="status-header pa-6" :style="headerGradient">
      <v-row align="center" class="ma-0">
        <!-- Circular Progress -->
        <v-col cols="auto">
          <div class="position-relative">
            <v-progress-circular
              :model-value="overallPercentage"
              :size="120"
              :width="12"
              :color="tierColor"
              class="circular-progress"
            >
              <div class="text-center">
                <div class="text-h4 font-weight-bold text-white">
                  {{ Math.round(overallPercentage) }}%
                </div>
                <div class="text-caption text-white">تکمیل پروفایل</div>
              </div>
            </v-progress-circular>
            
            <!-- Tier Badge -->
            <v-avatar
              :color="tierColor"
              size="40"
              class="tier-badge"
              elevation="3"
            >
              <v-icon size="24" color="white">{{ tierIcon }}</v-icon>
            </v-avatar>
          </div>
        </v-col>

        <!-- Status Info -->
        <v-col>
          <div class="text-white">
            <h2 class="text-h5 font-weight-bold mb-2">
              {{ tierDisplay }}
            </h2>
            <div class="d-flex flex-wrap gap-3 text-body-1">
              <div class="d-flex align-center gap-1">
                <v-icon size="20" color="white">mdi-trophy</v-icon>
                <span>رتبه {{ rank || '—' }}</span>
              </div>
              <div class="d-flex align-center gap-1">
                <v-icon size="20" color="white">mdi-star</v-icon>
                <span>{{ totalPoints.toLocaleString('fa-IR') }} امتیاز</span>
              </div>
            </div>
          </div>
        </v-col>

        <!-- Expand Button -->
        <v-col cols="auto">
          <v-btn
            :icon="expanded ? 'mdi-chevron-up' : 'mdi-chevron-down'"
            variant="text"
            color="white"
            @click="expanded = !expanded"
          />
        </v-col>
      </v-row>
    </div>

    <!-- Milestone Progress Bar -->
    <v-card-text class="px-6 pt-6 pb-4">
      <div class="milestone-container">
        <div class="d-flex justify-space-between align-center mb-2">
          <span class="text-body-2 font-weight-medium">
            پیشرفت مسیر جلب اعتماد
          </span>
          <span class="text-body-2 text-medium-emphasis">
            {{ requiredStepsCompleted }} از {{ totalRequiredSteps }} مرحله
          </span>
        </div>

        <!-- Milestone Steps -->
        <div class="milestone-steps">
          <div
            v-for="(milestone, index) in milestones"
            :key="milestone.name"
            class="milestone-step"
            :class="{ 'completed': milestone.completed }"
          >
            <!-- Connector Line -->
            <div
              v-if="index < milestones.length - 1"
              class="milestone-connector"
              :class="{ 'completed': milestone.completed }"
            />
            
            <!-- Milestone Circle -->
            <v-tooltip location="top">
              <template #activator="{ props: tooltipProps }">
                <div
                  v-bind="tooltipProps"
                  class="milestone-circle"
                  :class="{ 'completed': milestone.completed, 'current': !milestone.completed && index === currentMilestoneIndex }"
                >
                  <v-icon
                    v-if="milestone.completed"
                    size="16"
                    color="white"
                  >
                    mdi-check
                  </v-icon>
                  <span v-else class="text-caption">{{ index + 1 }}</span>
                </div>
              </template>
              <div class="text-center">
                <div class="font-weight-bold">{{ milestone.title }}</div>
                <div class="text-caption">امتیاز: {{ milestone.score }}%</div>
              </div>
            </v-tooltip>

            <!-- Label (shown only on desktop) -->
            <div class="milestone-label d-none d-md-block text-caption text-center mt-1">
              {{ milestone.title }}
            </div>
          </div>
        </div>
      </div>
    </v-card-text>

    <!-- Expanded Details -->
    <v-expand-transition>
      <v-card-text v-if="expanded" class="px-6 pt-0 pb-6">
        <v-divider class="mb-4" />
        
        <v-row class="metrics-grid">
          <!-- Reputation Score -->
          <v-col cols="12" sm="6" md="3">
            <div class="metric-item">
              <div class="d-flex align-center gap-2 mb-2">
                <v-icon size="24" :color="tierColor">mdi-shield-star</v-icon>
                <span class="text-body-2 text-medium-emphasis">اعتبار شما</span>
              </div>
              <div class="text-h6 font-weight-bold">
                {{ Math.round(reputationScore) }}<span class="text-body-2">/100</span>
              </div>
              <v-progress-linear
                :model-value="reputationScore"
                :color="tierColor"
                height="6"
                rounded
                class="mt-2"
              />
            </div>
          </v-col>

          <!-- Streak -->
          <v-col cols="12" sm="6" md="3">
            <div class="metric-item">
              <div class="d-flex align-center gap-2 mb-2">
                <v-icon size="24" color="orange">mdi-fire</v-icon>
                <span class="text-body-2 text-medium-emphasis">روزهای پیاپی</span>
              </div>
              <div class="text-h6 font-weight-bold">
                {{ streakDays }} روز
              </div>
            </div>
          </v-col>

          <!-- Response Time -->
          <v-col cols="12" sm="6" md="3">
            <div class="metric-item">
              <div class="d-flex align-center gap-2 mb-2">
                <v-icon size="24" color="blue">mdi-clock-fast</v-icon>
                <span class="text-body-2 text-medium-emphasis">سرعت پاسخ</span>
              </div>
              <div class="text-h6 font-weight-bold">
                {{ formatResponseTime(avgResponseMinutes) }}
              </div>
            </div>
          </v-col>

          <!-- Total Points -->
          <v-col cols="12" sm="6" md="3">
            <div class="metric-item">
              <div class="d-flex align-center gap-2 mb-2">
                <v-icon size="24" color="purple">mdi-star-circle</v-icon>
                <span class="text-body-2 text-medium-emphasis">مجموع امتیاز</span>
              </div>
              <div class="text-h6 font-weight-bold">
                {{ totalPoints.toLocaleString('fa-IR') }}
              </div>
            </div>
          </v-col>
        </v-row>

        <!-- Tier Benefits Info -->
        <v-alert
          v-if="nextTierInfo"
          variant="tonal"
          :color="tierColor"
          rounded="lg"
          class="mt-4"
          density="compact"
        >
          <div class="d-flex align-center gap-2">
            <v-icon>mdi-information</v-icon>
            <span class="text-body-2">
              {{ nextTierInfo }}
            </span>
          </div>
        </v-alert>
      </v-card-text>
    </v-expand-transition>
  </v-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Milestone } from '~/composables/useGamificationDashboard'

const props = defineProps<{
  tier: string
  tierDisplay: string
  tierColor: string
  rank: number | null
  totalPoints: number
  reputationScore: number
  streakDays: number
  avgResponseMinutes: number
  overallPercentage: number
  milestones: Milestone[]
  requiredStepsCompleted: number
  totalRequiredSteps: number
}>()

const expanded = ref(false)

const tierIcon = computed(() => {
  const icons: Record<string, string> = {
    diamond: 'mdi-diamond-stone',
    gold: 'mdi-trophy',
    silver: 'mdi-medal',
    bronze: 'mdi-award',
    inactive: 'mdi-account-off'
  }
  return icons[props.tier] || 'mdi-star'
})

const headerGradient = computed(() => {
  const gradients: Record<string, string> = {
    purple: 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    amber: 'background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    grey: 'background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    brown: 'background: linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    red: 'background: linear-gradient(135deg, #f2709c 0%, #ff9472 100%)'
  }
  return gradients[props.tierColor] || gradients.grey
})

const currentMilestoneIndex = computed(() => {
  return props.milestones.findIndex(m => !m.completed)
})

const nextTierInfo = computed(() => {
  const incompleteMilestones = props.milestones.filter(m => !m.completed)
  if (incompleteMilestones.length === 0) {
    return 'عالی! پروفایل شما کاملاً حرفه‌ای و قابل اعتماد است.'
  }
  const nextMilestone = incompleteMilestones[0]
  return `قدم بعدی برای موفقیت: ${nextMilestone.title}`
})

const formatResponseTime = (minutes: number): string => {
  if (minutes === 0) return '—'
  if (minutes < 60) return `${Math.round(minutes)} دقیقه`
  const hours = Math.round(minutes / 60)
  return `${hours} ساعت`
}
</script>

<style scoped>
.status-card {
  border: none;
}

.status-header {
  position: relative;
  border-radius: 24px 24px 0 0;
}

.circular-progress {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  backdrop-filter: blur(10px);
}

.tier-badge {
  position: absolute;
  bottom: -8px;
  right: -8px;
  border: 3px solid white;
}

.milestone-container {
  position: relative;
}

.milestone-steps {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  position: relative;
  padding: 20px 0;
}

.milestone-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.milestone-connector {
  position: absolute;
  top: 20px;
  left: 50%;
  right: -50%;
  height: 3px;
  background: rgb(var(--v-theme-surface-variant));
  z-index: 0;
  transition: background 0.3s ease;
}

.milestone-connector.completed {
  background: rgb(var(--v-theme-primary));
}

.milestone-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgb(var(--v-theme-surface-variant));
  border: 3px solid rgb(var(--v-theme-surface));
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  transition: all 0.3s ease;
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface-variant));
}

.milestone-circle.completed {
  background: rgb(var(--v-theme-primary));
  transform: scale(1.1);
}

.milestone-circle.current {
  background: rgb(var(--v-theme-primary));
  opacity: 0.5;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.7;
  }
}

.milestone-label {
  max-width: 80px;
  word-wrap: break-word;
  font-size: 11px;
}

.metrics-grid .metric-item {
  padding: 16px;
  background: rgb(var(--v-theme-surface-variant));
  border-radius: 12px;
}

@media (max-width: 600px) {
  .status-header {
    padding: 16px !important;
  }

  .circular-progress {
    --v-progress-circular-size: 100px !important;
  }

  .milestone-circle {
    width: 32px;
    height: 32px;
  }

  .milestone-connector {
    top: 16px;
  }
}
</style>

