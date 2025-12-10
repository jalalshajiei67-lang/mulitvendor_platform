<template>
  <v-card 
    :loading="loading" 
    class="form-quality-score h-100" 
    rounded="xl"
    elevation="0"
    variant="tonal"
    :color="scoreColorVariant"
  >
    <v-card-text class="pa-4 pa-md-6">
      <div class="d-flex justify-space-between align-start flex-wrap mb-4 gap-4">
        <div class="flex-grow-1">
          <p class="text-caption text-medium-emphasis mb-1">{{ caption }}</p>
          <h3 class="text-h6 font-weight-bold">{{ title }}</h3>
        </div>
        <div class="text-center">
          <v-progress-circular
            :model-value="animatedScore"
            :size="96"
            :width="8"
            :color="progressColor"
            rotate="270"
            class="mb-1"
          >
            <span class="text-h5 font-weight-bold">{{ Math.round(animatedScore) }}</span>
          </v-progress-circular>
          <div class="text-caption text-medium-emphasis">از ۱۰۰</div>
          <small class="d-block text-medium-emphasis mt-2 font-weight-medium">{{ mood }}</small>
        </div>
      </div>

      <v-progress-linear
        :model-value="animatedScore"
        height="12"
        rounded
        :color="progressColor"
        class="mb-4"
        :bg-color="progressBgColor"
      ></v-progress-linear>

      <v-list density="comfortable" class="bg-transparent">
        <v-list-item
          v-for="metric in metrics"
          :key="metric.key"
          :title="metric.label"
          class="metric-row"
        >
          <template #prepend>
            <v-avatar 
              size="36" 
              :color="metric.passed ? 'success' : 'warning'" 
              class="me-3"
              variant="flat"
            >
              <v-icon size="18" color="white">
                {{ metric.passed ? 'mdi-check-circle' : 'mdi-alert-circle' }}
              </v-icon>
            </v-avatar>
          </template>
          <template #subtitle>
            <span class="text-caption text-medium-emphasis mt-1 d-block">{{ metric.tip }}</span>
          </template>
          <template #append>
            <v-chip 
              size="x-small" 
              :color="metric.passed ? 'success' : 'warning'"
              variant="flat"
            >
              {{ Math.round(metric.weight * 100) }}%
            </v-chip>
          </template>
        </v-list-item>
      </v-list>

      <div v-if="tips.length" class="mt-4 p-4 rounded-lg" :class="tipsBgClass">
        <div class="d-flex align-center gap-2 mb-2">
          <v-icon :color="tipsIconColor" size="20">mdi-lightbulb-on</v-icon>
          <p class="text-subtitle-2 font-weight-bold mb-0">
            {{ t('suggestions') }}
          </p>
        </div>
        <ul class="text-caption suggestions">
          <li v-for="tip in tips" :key="tip">
            {{ tip }}
          </li>
        </ul>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
const props = withDefaults(defineProps<{
  title?: string
  caption?: string
  score: number
  metrics: Array<{ key: string; label: string; tip: string; weight: number; passed: boolean }>
  tips?: string[]
  loading?: boolean
}>(), {
  title: 'امتیاز کیفیت فرم',
  caption: 'راهنمای قدم‌به‌قدم',
  tips: () => [],
  loading: false
})

const colorClass = computed(() => {
  if (props.score >= 70) return 'score-success'
  if (props.score >= 40) return 'score-warning'
  return 'score-danger'
})

const progressColor = computed(() => {
  if (props.score >= 70) return 'success'
  if (props.score >= 40) return 'warning'
  return 'error'
})

const mood = computed(() => {
  if (props.score >= 90) return 'عالی'
  if (props.score >= 70) return 'خوب'
  if (props.score >= 40) return 'در حال پیشرفت'
  return 'نیازمند توجه'
})

const scoreColorVariant = computed(() => {
  if (props.score >= 70) return 'success'
  if (props.score >= 40) return 'warning'
  return 'error'
})

const progressBgColor = computed(() => {
  if (props.score >= 70) return 'success-lighten-5'
  if (props.score >= 40) return 'warning-lighten-5'
  return 'error-lighten-5'
})

const tipsBgClass = computed(() => {
  if (props.score >= 70) return 'bg-success-lighten-5'
  if (props.score >= 40) return 'bg-warning-lighten-5'
  return 'bg-error-lighten-5'
})

const tipsIconColor = computed(() => {
  if (props.score >= 70) return 'success'
  if (props.score >= 40) return 'warning'
  return 'error'
})

// Animated score value for smooth transitions
const animatedScore = ref(props.score)
watch(
  () => props.score,
  (newVal, oldVal) => {
    const start = animatedScore.value
    const end = newVal
    const duration = 400
    const startTime = performance.now()

    const animate = (time: number) => {
      const progress = Math.min((time - startTime) / duration, 1)
      animatedScore.value = start + (end - start) * progress
      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }
)

const t = (key: string) => {
  const dict: Record<string, string> = {
    suggestions: 'پیشنهادهای فوری'
  }
  return dict[key] ?? key
}
</script>

<style scoped>
.form-quality-score {
  transition: transform 0.2s ease;
}

.form-quality-score:hover {
  transform: translateY(-2px);
}

.score-circle {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 4px solid transparent;
  transition: transform 0.2s ease;
}

.score-circle:hover {
  transform: scale(1.05);
}

.score-success {
  border-color: #4caf50;
  background: rgba(76, 175, 80, 0.1);
}

.score-warning {
  border-color: #ff9800;
  background: rgba(255, 152, 0, 0.1);
}

.score-danger {
  border-color: #f44336;
  background: rgba(244, 67, 54, 0.1);
}

.metric-row {
  transition: background 0.2s ease;
  border-radius: 8px;
  margin: 2px 0;
}

.metric-row:hover {
  background: rgba(var(--v-theme-surface), 0.5);
}

.metric-row + .metric-row {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

ul.suggestions {
  list-style-type: '• ';
  padding-inline-start: 1.2rem;
  margin: 0;
}

ul.suggestions li {
  margin-bottom: 6px;
  line-height: 1.6;
}

.gap-2 {
  gap: 8px;
}

.gap-4 {
  gap: 16px;
}

@media (max-width: 600px) {
  .score-circle {
    width: 80px;
    height: 80px;
  }
  
  .score-circle .text-h4 {
    font-size: 1.5rem !important;
  }
}
</style>
