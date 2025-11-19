<template>
  <v-card :loading="loading" class="form-quality-score" rounded="xl">
    <v-card-text>
      <div class="d-flex justify-space-between align-start flex-wrap mb-4 gap-4">
        <div>
          <p class="text-caption text-medium-emphasis mb-1">{{ caption }}</p>
          <h3 class="text-h6 font-weight-bold">{{ title }}</h3>
        </div>
        <div class="text-center">
          <div class="score-circle" :class="colorClass">
            <span class="text-h4 font-weight-bold">{{ score }}</span>
            <span class="text-caption">/100</span>
          </div>
          <small class="d-block text-medium-emphasis mt-2">{{ mood }}</small>
        </div>
      </div>

      <v-progress-linear
        :model-value="score"
        height="10"
        rounded
        :color="progressColor"
        class="mb-4"
      ></v-progress-linear>

      <v-list density="comfortable" class="bg-transparent">
        <v-list-item
          v-for="metric in metrics"
          :key="metric.key"
          :title="metric.label"
          class="metric-row"
        >
          <template #prepend>
            <v-avatar size="32" :color="metric.passed ? 'success' : 'warning'" class="me-2">
              <v-icon size="18">{{ metric.passed ? 'mdi-check' : 'mdi-alert' }}</v-icon>
            </v-avatar>
          </template>
          <template #subtitle>
            <span class="text-caption text-medium-emphasis">{{ metric.tip }}</span>
          </template>
          <template #append>
            <span class="text-caption text-medium-emphasis">{{ Math.round(metric.weight * 100) }}%</span>
          </template>
        </v-list-item>
      </v-list>

      <div v-if="tips.length" class="mt-4 p-3 rounded-lg bg-grey-lighten-4">
        <p class="text-subtitle-2 font-weight-bold mb-2">
          {{ t('suggestions') }}
        </p>
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
import { computed } from 'vue'
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

const t = (key: string) => {
  const dict: Record<string, string> = {
    suggestions: 'پیشنهادهای فوری'
  }
  return dict[key] ?? key
}
</script>

<style scoped>
.form-quality-score {
  min-height: 100%;
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
}
.score-success {
  border-color: #2e7d32;
}
.score-warning {
  border-color: #fdd835;
}
.score-danger {
  border-color: #e53935;
}
.metric-row + .metric-row {
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}
ul.suggestions {
  list-style-type: '• ';
  padding-inline-start: 1.2rem;
  margin: 0;
}
</style>
