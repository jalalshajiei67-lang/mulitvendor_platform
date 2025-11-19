<template>
  <v-card class="engagement-widget" rounded="xl" :loading="loading" elevation="2">
    <v-card-text>
      <div class="d-flex justify-space-between align-center mb-4 flex-wrap gap-4">
        <div>
          <p class="text-caption text-medium-emphasis mb-1">{{ t('todayStatus') }}</p>
          <h3 class="text-h6 font-weight-bold">{{ t('keepGoing') }}</h3>
          <p class="text-body-2 text-medium-emphasis">{{ subtitle }}</p>
        </div>
        <div class="text-center">
          <v-avatar color="deep-orange" size="64">
            <v-icon size="36">mdi-fire</v-icon>
          </v-avatar>
          <p class="text-body-2 mt-2">{{ streakLabel }}</p>
        </div>
      </div>

      <v-row>
        <v-col cols="12" md="4">
          <div class="stat-pill">
            <span class="text-caption text-medium-emphasis">{{ t('pointsToday') }}</span>
            <strong class="text-h6">{{ engagement?.today_points ?? 0 }}</strong>
          </div>
        </v-col>
        <v-col cols="12" md="4">
          <div class="stat-pill">
            <span class="text-caption text-medium-emphasis">{{ t('totalPoints') }}</span>
            <strong class="text-h6">{{ engagement?.total_points ?? 0 }}</strong>
          </div>
        </v-col>
        <v-col cols="12" md="4">
          <div class="stat-pill">
            <span class="text-caption text-medium-emphasis">{{ t('responseSpeed') }}</span>
            <strong class="text-h6">{{ avgResponse }}</strong>
          </div>
        </v-col>
      </v-row>

      <v-btn
        color="primary"
        class="mt-4"
        block
        prepend-icon="mdi-plus-circle"
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
  return `${Math.round(props.engagement.avg_response_minutes)} دقیقه`
})

const ctaText = computed(() => (props.engagement?.today_points ?? 0) >= 20 ? 'یک محصول دیگر ثبت کنید' : 'امروز محصول جدید ثبت کنید')

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
.stat-pill {
  background: #fafafa;
  border-radius: 16px;
  padding: 16px;
  text-align: center;
}
</style>
