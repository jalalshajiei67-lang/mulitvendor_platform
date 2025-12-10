<template>
  <v-card
    v-if="visible"
    rounded="xl"
    variant="tonal"
    color="primary"
    class="tier-nudge"
  >
    <v-card-text class="d-flex flex-column flex-sm-row align-center justify-space-between gap-4">
      <div class="d-flex align-center gap-3">
        <v-avatar color="primary" size="44">
          <v-icon color="on-primary">mdi-rocket-launch</v-icon>
        </v-avatar>
        <div>
          <div class="text-body-1 font-weight-bold">{{ headline }}</div>
          <div class="text-body-2 text-medium-emphasis mt-1">{{ subtext }}</div>
          <div class="text-caption text-high-emphasis mt-1">
            تاییدیه‌ها: {{ endorsements }} · امتیاز شهرت: {{ Math.round(reputation) }}
          </div>
        </div>
      </div>
      <div class="d-flex flex-column flex-sm-row gap-2 w-100 w-sm-auto">
        <v-btn color="primary" variant="flat" prepend-icon="mdi-account-star" @click="$emit('cta-primary')">
          اقدام پیشنهادی
        </v-btn>
        <v-btn color="secondary" variant="text" prepend-icon="mdi-target" @click="$emit('cta-secondary')">
          راهنمای بهبود
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  tier: string | null
  engagement?: {
    endorsements_received?: number
    reputation_score?: number
  } | null
  isPremium?: boolean
}>()

const visible = computed(() => !props.isPremium && ['gold', 'silver'].includes(props.tier || ''))
const endorsements = computed(() => props.engagement?.endorsements_received ?? 0)
const reputation = computed(() => props.engagement?.reputation_score ?? 0)

const headline = computed(() => {
  if (props.tier === 'gold') return 'فاصله کمی تا الماس دارید!'
  if (props.tier === 'silver') return 'یک قدم تا طلایی شدن'
  return ''
})

const subtext = computed(() => {
  if (props.tier === 'gold') {
    return '۳ تاییدیه تازه بگیرید و امتیاز شهرت را به ۸۰ برسانید تا الماسی شوید.'
  }
  if (props.tier === 'silver') {
    return 'پورتفو را کامل کنید و ۵ تاییدیه جمع کنید تا به سطح طلا برسید.'
  }
  return ''
})
</script>

<style scoped>
.tier-nudge {
  direction: rtl;
  text-align: right;
}
</style>

