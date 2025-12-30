<template>
  <v-card
    rounded="xl"
    elevation="2"
    class="auction-card"
    hover
    @click="navigateToDetail"
  >
    <v-card-title class="d-flex align-center justify-space-between">
      <span class="text-h6">{{ auction.title }}</span>
      <v-chip
        :color="statusColor"
        size="small"
        variant="tonal"
      >
        {{ statusText }}
      </v-chip>
    </v-card-title>

    <v-card-subtitle v-if="auction.category_name">
      {{ auction.category_name }}
    </v-card-subtitle>

    <v-card-text>
      <div class="mb-2">
        <strong>قیمت شروع:</strong>
        <span class="text-h6 text-primary ms-2">
          {{ formatPrice(auction.starting_price) }} تومان
        </span>
      </div>

      <div v-if="auction.bid_count !== undefined" class="mb-2">
        <v-icon size="small" class="me-1">mdi-account-multiple</v-icon>
        {{ auction.bid_count }} پیشنهاد
      </div>

      <CountdownTimer
        v-if="auction.time_remaining"
        :deadline="auction.deadline"
      />
    </v-card-text>

    <v-card-actions v-if="userRole === 'supplier'">
      <RankBadge
        v-if="auction.my_rank"
        :rank="auction.my_rank"
        size="small"
      />
      <v-chip
        v-else-if="auction.is_invited"
        color="info"
        variant="tonal"
        size="small"
      >
        هنوز پیشنهاد نداده‌اید
      </v-chip>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CountdownTimer from './CountdownTimer.vue'
import RankBadge from './RankBadge.vue'

interface Props {
  auction: any
  userRole?: 'buyer' | 'supplier'
}

const props = withDefaults(defineProps<Props>(), {
  userRole: 'buyer'
})

const router = useRouter()

const statusColor = computed(() => {
  const status = props.auction.status
  if (status === 'active') return 'success'
  if (status === 'closed') return 'warning'
  if (status === 'awarded') return 'info'
  if (status === 'cancelled') return 'error'
  return 'grey'
})

const statusText = computed(() => {
  const statusMap: Record<string, string> = {
    'draft': 'پیش‌نویس',
    'active': 'فعال',
    'closed': 'بسته شده',
    'awarded': 'اعطا شده',
    'cancelled': 'لغو شده'
  }
  return statusMap[props.auction.status] || props.auction.status
})

const formatPrice = (price: number | string) => {
  const num = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(num)
}

const navigateToDetail = () => {
  const route = props.userRole === 'buyer' 
    ? `/buyer/auctions/${props.auction.id}`
    : `/seller/auctions/${props.auction.id}`
  router.push(route)
}
</script>

<style scoped>
.auction-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.auction-card:hover {
  transform: translateY(-4px);
}
</style>

