<template>
  <v-alert
    v-if="status.low_score"
    type="warning"
    variant="tonal"
    border="start"
    class="low-score-banner"
    :icon="loading ? 'mdi-loading' : 'mdi-alert-decagram-outline'"
  >
    <div class="d-flex flex-column flex-sm-row align-center justify-space-between gap-4">
      <div class="d-flex align-center gap-3">
        <v-avatar color="warning" size="44">
          <v-icon color="on-warning" size="24">mdi-trending-down</v-icon>
        </v-avatar>
        <div class="text-body-1 font-weight-medium">
          <div>امتیاز پروفایل شما پایین است.</div>
          <div class="text-body-2 text-medium-emphasis">
            برای دیده‌شدن در نتایج جستجو، پروفایل را بهبود دهید یا پلن پریمیوم را فعال کنید.
          </div>
          <div class="text-caption text-medium-emphasis mt-1">
            وضعیت فعلی: {{ tierLabel }} · امتیاز {{ status.points }} · اعتبار {{ Math.round(status.reputation_score) }}
          </div>
        </div>
      </div>

      <div class="d-flex flex-column flex-sm-row gap-2 w-100 w-sm-auto">
        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-account-cog"
          @click="$emit('improve-profile')"
        >
          تکمیل پروفایل
        </v-btn>
        <v-btn
          color="secondary"
          variant="tonal"
          prepend-icon="mdi-crown"
          @click="$emit('upgrade-premium')"
        >
          ارتقای پریمیوم
        </v-btn>
      </div>
    </div>
  </v-alert>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: {
    low_score: boolean
    tier: string | null
    is_premium: boolean
    points: number
    reputation_score: number
  }
  loading?: boolean
}>()

const tierLabel = computed(() => {
  const map: Record<string, string> = {
    diamond: 'الماس',
    gold: 'طلا',
    silver: 'نقره',
    bronze: 'برنز',
    inactive: 'غیرفعال'
  }
  return map[props.status.tier || 'inactive'] || 'نامشخص'
})
</script>

<style scoped>
.low-score-banner {
  direction: rtl;
  text-align: right;
  border-radius: 16px;
}
</style>

