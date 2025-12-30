<template>
  <v-container fluid dir="rtl" class="auction-detail-page">
    <v-row v-if="loading" justify="center">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else-if="auction" justify="center">
      <v-col cols="12" md="10" lg="8">
        <!-- Auction Header -->
        <v-card elevation="2" rounded="xl" class="mb-4">
          <v-card-title class="text-h5 pa-4 pa-md-6">
            {{ auction.title }}
          </v-card-title>
          <v-card-subtitle v-if="auction.category_name" class="pa-4 pa-md-6 pt-0">
            {{ auction.category_name }}
          </v-card-subtitle>
          <v-divider></v-divider>
          <v-card-text class="pa-4 pa-md-6">
            <div v-html="auction.description"></div>
          </v-card-text>
        </v-card>

        <!-- Auction Info -->
        <v-card elevation="2" rounded="xl" class="mb-4">
          <v-card-title class="pa-4 pa-md-6">
            اطلاعات مناقصه
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-4 pa-md-6">
            <v-row>
              <v-col cols="12" md="6">
                <div class="mb-4">
                  <strong>قیمت شروع:</strong>
                  <span class="text-h6 text-primary ms-2">
                    {{ formatPrice(auction.starting_price) }} تومان
                  </span>
                </div>
                <div class="mb-4">
                  <strong>حداقل کاهش:</strong>
                  <span class="ms-2">
                    {{ formatPrice(auction.minimum_decrement) }} تومان
                  </span>
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="mb-4">
                  <strong>وضعیت:</strong>
                  <v-chip
                    :color="statusColor"
                    variant="tonal"
                    class="ms-2"
                  >
                    {{ statusText }}
                  </v-chip>
                </div>
                <div v-if="auction.time_remaining" class="mb-4">
                  <strong>زمان باقی‌مانده:</strong>
                  <CountdownTimer
                    :deadline="auction.deadline"
                    class="ms-2"
                  />
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- My Status Card -->
        <v-card elevation="2" rounded="xl" class="mb-4">
          <v-card-title class="pa-4 pa-md-6">
            وضعیت شما
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-4 pa-md-6">
            <div v-if="auction.my_bid">
              <div class="d-flex align-center mb-4">
                <strong class="me-2">رتبه شما:</strong>
                <RankBadge :rank="auction.my_rank" />
              </div>
              <div class="mb-4">
                <strong>پیشنهاد شما:</strong>
                <span class="text-h6 text-primary ms-2">
                  {{ formatPrice(auction.my_bid.amount) }} تومان
                </span>
              </div>
              <v-alert
                v-if="auction.my_bid.is_winning"
                type="success"
                variant="tonal"
              >
                <v-icon start>mdi-trophy</v-icon>
                شما در حال حاضر برنده هستید!
              </v-alert>
              <v-alert
                v-else-if="auction.my_rank && auction.my_rank <= 3"
                type="warning"
                variant="tonal"
              >
                شما در رتبه {{ auction.my_rank }} هستید. برای برنده شدن، پیشنهاد بهتری ارائه دهید.
              </v-alert>
              <v-alert
                v-else
                type="error"
                variant="tonal"
              >
                شما در رتبه {{ auction.my_rank }} هستید. برای بهبود رتبه، پیشنهاد بهتری ارائه دهید.
              </v-alert>
            </div>
            <v-alert v-else type="info" variant="tonal">
              شما هنوز پیشنهاد نداده‌اید
            </v-alert>
          </v-card-text>
        </v-card>

        <!-- Bid Form -->
        <v-card v-if="auction.can_bid" elevation="2" rounded="xl" class="mb-4">
          <BidForm
            :starting-price="auction.starting_price"
            :previous-bid="auction.my_bid?.amount"
            :minimum-decrement="auction.minimum_decrement"
            :can-bid="auction.can_bid"
            @submit="handleBidSubmit"
          />
        </v-card>

        <!-- Bid History -->
        <v-card v-if="auction.my_bid" elevation="2" rounded="xl">
          <v-card-title class="pa-4 pa-md-6">
            تاریخچه پیشنهادات شما
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-4 pa-md-6">
            <v-list>
              <v-list-item>
                <v-list-item-title>
                  {{ formatPrice(auction.my_bid.amount) }} تومان
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ formatDate(auction.my_bid.created_at) }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else justify="center">
      <v-col cols="12" class="text-center">
        <v-alert type="error" variant="tonal">
          مناقصه یافت نشد
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuctionApi } from '~/composables/useAuctionApi'
import { useToast } from '~/composables/useToast'
import CountdownTimer from '~/components/auction/CountdownTimer.vue'
import RankBadge from '~/components/auction/RankBadge.vue'
import BidForm from '~/components/auction/BidForm.vue'

definePageMeta({
  middleware: 'authenticated'
})

const route = useRoute()
const { getAuctionDetail, placeBid, getMyStatus } = useAuctionApi()
const { showToast } = useToast()

const loading = ref(true)
const auction = ref<any>(null)

const statusColor = computed(() => {
  if (!auction.value) return 'grey'
  const status = auction.value.status
  if (status === 'active') return 'success'
  if (status === 'closed') return 'warning'
  if (status === 'awarded') return 'info'
  if (status === 'cancelled') return 'error'
  return 'grey'
})

const statusText = computed(() => {
  if (!auction.value) return ''
  const statusMap: Record<string, string> = {
    'draft': 'پیش‌نویس',
    'active': 'فعال',
    'closed': 'بسته شده',
    'awarded': 'اعطا شده',
    'cancelled': 'لغو شده'
  }
  return statusMap[auction.value.status] || auction.value.status
})

const formatPrice = (price: number | string) => {
  const num = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(num)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const loadAuction = async () => {
  try {
    loading.value = true
    const id = parseInt(route.params.id as string)
    auction.value = await getAuctionDetail(id)
  } catch (error: any) {
    console.error('Error loading auction:', error)
    showToast('خطا در بارگذاری مناقصه', 'error')
  } finally {
    loading.value = false
  }
}

const handleBidSubmit = async (amount: number) => {
  try {
    const id = parseInt(route.params.id as string)
    const response = await placeBid(id, amount)
    showToast('پیشنهاد با موفقیت ثبت شد', 'success')
    
    if (response.deadline_extended) {
      showToast('مهلت مناقصه 5 دقیقه تمدید شد', 'info')
    }
    
    await loadAuction()
  } catch (error: any) {
    console.error('Error placing bid:', error)
    showToast(error.data?.error || 'خطا در ثبت پیشنهاد', 'error')
  }
}

let interval: NodeJS.Timeout | null = null

onMounted(() => {
  loadAuction()
  
  // Auto-refresh every 10 seconds to check for deadline extensions
  interval = setInterval(() => {
    if (auction.value && auction.value.status === 'active') {
      loadAuction()
    }
  }, 10000)
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})
</script>

<style scoped>
.auction-detail-page {
  min-height: 100vh;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
</style>

