<template>
  <v-card 
    class="benefits-rank-widget" 
    rounded="xl" 
    :loading="loading" 
    elevation="2"
    :color="tierColor"
    variant="tonal"
  >
    <v-card-text class="pa-6">
      <!-- Tier Badge Section -->
      <div class="text-center mb-6">
        <v-avatar 
          :color="tierColor" 
          size="80"
          class="mb-3"
          variant="flat"
        >
          <v-icon size="40" color="white">{{ tierIcon }}</v-icon>
        </v-avatar>
        <h2 class="text-h4 font-weight-bold mb-2">{{ tierDisplayName }}</h2>
        <p class="text-body-1 text-medium-emphasis">{{ tierDescription }}</p>
      </div>

      <!-- Rank and Points Section -->
      <v-row class="mb-4">
        <v-col cols="6" class="text-center">
          <div class="rank-display">
            <v-icon size="24" :color="tierColor" class="mb-2">mdi-trophy-variant</v-icon>
            <div class="text-h5 font-weight-bold">{{ userRank ? `رتبه ${userRank}` : '—' }}</div>
            <span class="text-caption text-medium-emphasis">رتبه شما</span>
          </div>
        </v-col>
        <v-col cols="6" class="text-center">
          <div class="points-display">
            <v-icon size="24" :color="tierColor" class="mb-2">mdi-star-circle</v-icon>
            <div class="text-h5 font-weight-bold">{{ formatNumber(userPoints) }}</div>
            <span class="text-caption text-medium-emphasis">امتیاز کل</span>
          </div>
        </v-col>
      </v-row>

      <!-- Reputation Score Section -->
      <v-card
        v-if="userReputationScore !== null"
        elevation="0"
        variant="outlined"
        rounded="lg"
        class="pa-4 mb-4"
      >
        <div class="d-flex align-center justify-space-between mb-2">
          <div class="d-flex align-center gap-2">
            <v-icon :color="reputationColor" size="20">mdi-shield-check</v-icon>
            <span class="text-body-1 font-weight-medium">امتیاز اعتبار</span>
          </div>
          <div class="text-h6 font-weight-bold" :style="{ color: reputationColor }">
            {{ Math.round(userReputationScore) }}/100
          </div>
        </div>
        <v-progress-linear
          :model-value="userReputationScore"
          :color="reputationColor"
          height="8"
          rounded
          class="mb-2"
        ></v-progress-linear>
        <p class="text-caption text-medium-emphasis">
          بر اساس تأیید همکاران، نظرات مثبت مشتریان و سرعت پاسخگویی
        </p>
      </v-card>

      <!-- Progress to Next Tier -->
      <div v-if="nextTier && nextTier !== 'diamond'" class="mb-4">
        <div class="d-flex justify-space-between align-center mb-2">
          <span class="text-body-2 font-weight-medium">پیشرفت به {{ nextTierDisplayName }}</span>
          <span class="text-body-2 font-weight-bold">{{ progressPercentage }}%</span>
        </div>
        <v-progress-linear
          :model-value="progressPercentage"
          :color="tierColor"
          height="8"
          rounded
          class="mb-2"
        ></v-progress-linear>
        <div class="text-center">
          <p class="text-body-2 text-medium-emphasis mb-1">
            <span v-if="ranksToNextTier && ranksToNextTier > 0">
              {{ ranksToNextTier }} رتبه تا {{ nextTierDisplayName }}
            </span>
            <span v-else-if="nextTierPointsNeeded > 0">
              {{ formatNumber(nextTierPointsNeeded) }} امتیاز تا {{ nextTierDisplayName }}
            </span>
            <span v-else>
              در حال حاضر در بالاترین سطح هستید!
            </span>
          </p>
        </div>
      </div>

      <!-- Tier Benefits -->
      <v-expansion-panels variant="accordion" class="mt-4">
        <v-expansion-panel>
          <v-expansion-panel-title>
            <v-icon start :color="tierColor">mdi-gift-outline</v-icon>
            <span class="mr-2">مزایای سطح {{ tierDisplayName }}</span>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-list density="compact">
              <v-list-item
                v-for="(benefit, index) in currentTierBenefits"
                :key="index"
                class="px-0"
              >
                <template v-slot:prepend>
                  <v-icon size="20" :color="tierColor">mdi-check-circle</v-icon>
                </template>
                <v-list-item-title class="text-body-2">{{ benefit }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-expansion-panel-text>
        </v-expansion-panel>
        <v-expansion-panel v-if="nextTier && nextTier !== 'diamond'">
          <v-expansion-panel-title>
            <v-icon start :color="tierColor">mdi-trending-up</v-icon>
            <span class="mr-2">مزایای سطح {{ nextTierDisplayName }}</span>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-list density="compact">
              <v-list-item
                v-for="(benefit, index) in nextTierBenefits"
                :key="index"
                class="px-0"
              >
                <template v-slot:prepend>
                  <v-icon size="20" color="grey">mdi-circle-outline</v-icon>
                </template>
                <v-list-item-title class="text-body-2">{{ benefit }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useGamificationStore } from '~/stores/gamification'

const props = defineProps<{
  loading?: boolean
}>()

const gamificationStore = useGamificationStore()

const userRank = computed(() => gamificationStore.userRank)
const userTier = computed(() => gamificationStore.userTier || 'inactive')
const userPoints = computed(() => gamificationStore.engagement?.total_points || 0)
const userReputationScore = computed(() => gamificationStore.engagement?.reputation_score ?? null)
const ranksToNextTier = computed(() => gamificationStore.ranksToNextTier)
const nextTier = computed(() => gamificationStore.nextTier)
const nextTierPointsNeeded = computed(() => gamificationStore.nextTierPointsNeeded)

const tierColor = computed(() => {
  const colorMap: Record<string, string> = {
    diamond: 'purple',
    gold: 'amber',
    silver: 'grey',
    bronze: 'brown',
    inactive: 'red',
  }
  return colorMap[userTier.value] || 'grey'
})

const tierIcon = computed(() => {
  const iconMap: Record<string, string> = {
    diamond: 'mdi-diamond-stone',
    gold: 'mdi-trophy',
    silver: 'mdi-medal',
    bronze: 'mdi-award',
    inactive: 'mdi-account-off',
  }
  return iconMap[userTier.value] || 'mdi-account'
})

const tierDisplayName = computed(() => {
  const nameMap: Record<string, string> = {
    diamond: 'الماس',
    gold: 'طلا',
    silver: 'نقره',
    bronze: 'برنز',
    inactive: 'غیرفعال',
  }
  return nameMap[userTier.value] || 'نامشخص'
})

const tierDescription = computed(() => {
  const descMap: Record<string, string> = {
    diamond: 'بالاترین سطح - شما در رتبه برتر هستید!',
    gold: 'سطح عالی - عملکرد شما قابل تحسین است',
    silver: 'سطح خوب - در مسیر پیشرفت هستید',
    bronze: 'سطح پایه - شروع خوبی داشته‌اید',
    inactive: 'نیاز به بهبود - برای شروع اقدام کنید',
  }
  return descMap[userTier.value] || ''
})

const nextTierDisplayName = computed(() => {
  if (!nextTier.value) return ''
  const nameMap: Record<string, string> = {
    diamond: 'الماس',
    gold: 'طلا',
    silver: 'نقره',
    bronze: 'برنز',
  }
  return nameMap[nextTier.value] || ''
})

const progressPercentage = computed(() => {
  if (!nextTier.value || nextTier.value === 'diamond') return 100
  
  const thresholds: Record<string, number> = {
    diamond: 1000,
    gold: 500,
    silver: 200,
    bronze: 50,
    inactive: 0,
  }
  
  const currentThreshold = thresholds[userTier.value] || 0
  const nextThreshold = thresholds[nextTier.value] || 1000
  const range = nextThreshold - currentThreshold
  
  if (range === 0) return 100
  
  const progress = ((userPoints.value - currentThreshold) / range) * 100
  return Math.max(0, Math.min(100, Math.round(progress)))
})

const currentTierBenefits = computed(() => {
  const benefits: Record<string, string[]> = {
    diamond: [
      'اولویت در نتایج جستجو',
      'نمایش ویژه در صفحه اصلی',
      'پشتیبانی 24/7',
      'گزارش‌های تحلیلی پیشرفته',
      'بدون محدودیت در تبلیغات',
    ],
    gold: [
      'اولویت بالا در نتایج جستجو',
      'نمایش برجسته محصولات',
      'پشتیبانی اولویت‌دار',
      'گزارش‌های تحلیلی',
      'تبلیغات با تخفیف 50%',
    ],
    silver: [
      'اولویت متوسط در نتایج جستجو',
      'نمایش استاندارد محصولات',
      'پشتیبانی استاندارد',
      'گزارش‌های پایه',
      'تبلیغات با تخفیف 25%',
    ],
    bronze: [
      'نمایش در نتایج جستجو',
      'پشتیبانی پایه',
      'گزارش‌های ساده',
    ],
    inactive: [
      'دسترسی به پنل فروشنده',
      'امکان بهبود امتیاز',
    ],
  }
  return benefits[userTier.value] || []
})

const nextTierBenefits = computed(() => {
  if (!nextTier.value) return []
  const benefits: Record<string, string[]> = {
    diamond: [
      'اولویت در نتایج جستجو',
      'نمایش ویژه در صفحه اصلی',
      'پشتیبانی 24/7',
      'گزارش‌های تحلیلی پیشرفته',
      'بدون محدودیت در تبلیغات',
    ],
    gold: [
      'اولویت بالا در نتایج جستجو',
      'نمایش برجسته محصولات',
      'پشتیبانی اولویت‌دار',
      'گزارش‌های تحلیلی',
      'تبلیغات با تخفیف 50%',
    ],
    silver: [
      'اولویت متوسط در نتایج جستجو',
      'نمایش استاندارد محصولات',
      'پشتیبانی استاندارد',
      'گزارش‌های پایه',
      'تبلیغات با تخفیف 25%',
    ],
    bronze: [
      'نمایش در نتایج جستجو',
      'پشتیبانی پایه',
      'گزارش‌های ساده',
    ],
  }
  return benefits[nextTier.value] || []
})

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('fa-IR').format(num)
}

const reputationColor = computed(() => {
  if (userReputationScore.value === null) return 'grey'
  if (userReputationScore.value >= 80) return 'success'
  if (userReputationScore.value >= 60) return 'info'
  if (userReputationScore.value >= 40) return 'warning'
  return 'error'
})
</script>

<style scoped>
.benefits-rank-widget {
  transition: all 0.3s ease;
}

.rank-display,
.points-display {
  padding: 8px;
}

.v-expansion-panel-title {
  font-weight: 500;
}
</style>

