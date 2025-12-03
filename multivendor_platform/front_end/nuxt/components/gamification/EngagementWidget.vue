<template>
  <v-card 
    class="engagement-widget" 
    rounded="xl" 
    :loading="loading" 
    elevation="0"
    variant="tonal"
    color="primary"
  >
    <v-card-text class="pa-4 pa-md-6">
      <!-- Header Section -->
      <div class="d-flex justify-space-between align-start mb-4 gap-3">
        <div class="flex-grow-1">
          <p class="text-caption text-medium-emphasis mb-1">{{ t('todayStatus') }}</p>
          <h3 class="text-h6 font-weight-bold mb-1">{{ t('keepGoing') }}</h3>
          <p class="text-body-2 text-medium-emphasis">{{ subtitle }}</p>
        </div>
        <div class="text-center">
          <v-avatar 
            :color="streakColor" 
            size="56"
            class="mb-2"
            variant="flat"
          >
            <v-icon size="28" color="white">mdi-fire</v-icon>
          </v-avatar>
          <p class="text-body-2 font-weight-medium">{{ streakLabel }}</p>
        </div>
      </div>

      <!-- Stats Grid -->
      <v-row dense class="mb-4">
        <v-col cols="4">
          <div class="stat-pill text-center">
            <v-icon size="20" color="primary" class="mb-1">mdi-star-circle</v-icon>
            <div class="text-h6 font-weight-bold mt-1">{{ engagement?.today_points ?? 0 }}</div>
            <span class="text-caption text-medium-emphasis d-block mt-1">{{ t('pointsToday') }}</span>
          </div>
        </v-col>
        <v-col cols="4">
          <div class="stat-pill text-center">
            <v-icon size="20" color="secondary" class="mb-1">mdi-trophy</v-icon>
            <div class="text-h6 font-weight-bold mt-1">{{ formatNumber(engagement?.total_points ?? 0) }}</div>
            <span class="text-caption text-medium-emphasis d-block mt-1">{{ t('totalPoints') }}</span>
          </div>
        </v-col>
        <v-col cols="4">
          <div class="stat-pill text-center">
            <v-icon size="20" color="success" class="mb-1">mdi-clock-fast</v-icon>
            <div class="text-h6 font-weight-bold mt-1">{{ avgResponse }}</div>
            <span class="text-caption text-medium-emphasis d-block mt-1">{{ t('responseSpeed') }}</span>
          </div>
        </v-col>
      </v-row>

      <!-- CTA Button -->
      <v-btn
        color="primary"
        class="mt-2"
        block
        size="large"
        prepend-icon="mdi-plus-circle"
        elevation="2"
        rounded="lg"
        @click="$emit('cta')"
      >
        {{ ctaText }}
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
interface Engagement {
  today_points: number
  total_points: number
  current_streak_days: number
  longest_streak_days: number
  avg_response_minutes: number
}

const props = defineProps<{ engagement: Engagement | null; loading?: boolean }>()
const emit = defineEmits<{ (e: 'cta'): void }>()
const loading = computed(() => props.loading ?? false)

const streakLabel = computed(() => {
  if (!props.engagement) return 'بدون نوار فعالیت'
  if (props.engagement.current_streak_days === 0) return 'امروز شروع کنید'
  return `${props.engagement.current_streak_days} روز متوالی`
})

const subtitle = computed(() => {
  if (!props.engagement) return 'با انجام کارهای ساده امتیاز بگیرید'
  return 'هر فرم کامل = امتیاز بیشتر و جایگاه بهتر'
})

const avgResponse = computed(() => {
  if (!props.engagement || !props.engagement.avg_response_minutes) return '---'
  const minutes = Math.round(props.engagement.avg_response_minutes)
  if (minutes < 60) return `${minutes} دقیقه`
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return mins > 0 ? `${hours}س ${mins}د` : `${hours} ساعت`
})

const streakColor = computed(() => {
  const streak = props.engagement?.current_streak_days ?? 0
  if (streak >= 7) return 'error'
  if (streak >= 3) return 'warning'
  return 'deep-orange'
})

const ctaText = computed(() => {
  const todayPoints = props.engagement?.today_points ?? 0
  if (todayPoints >= 50) return 'عالی! ادامه دهید'
  if (todayPoints >= 20) return 'یک محصول دیگر ثبت کنید'
  return 'امروز محصول جدید ثبت کنید'
})

const formatNumber = (num: number) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const t = (key: string) => {
  const dict: Record<string, string> = {
    todayStatus: 'وضعیت امروز',
    keepGoing: 'همین حالا امتیاز جمع کنید',
    pointsToday: 'امتیاز امروز',
    totalPoints: 'امتیاز کل',
    responseSpeed: 'میانگین پاسخ‌گویی'
  }
  return dict[key] ?? key
}
</script>

<style scoped>
.engagement-widget {
  height: 100%;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.engagement-widget:hover {
  transform: translateY(-2px);
}

.stat-pill {
  background: rgba(var(--v-theme-surface), 0.6);
  border-radius: 12px;
  padding: 12px 8px;
  min-height: 90px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.stat-pill:hover {
  background: rgba(var(--v-theme-surface), 0.9);
}

@media (max-width: 600px) {
  .stat-pill {
    min-height: 80px;
    padding: 10px 6px;
  }
  
  .stat-pill .text-h6 {
    font-size: 1.1rem !important;
  }
}
</style>
