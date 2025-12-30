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
                <div v-if="auction.reserve_price" class="mb-4">
                  <strong>قیمت رزرو:</strong>
                  <span class="text-h6 text-info ms-2">
                    {{ formatPrice(auction.reserve_price) }} تومان
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
                <div class="mb-4">
                  <strong>تعداد پیشنهادات:</strong>
                  <span class="ms-2">{{ auction.bid_count || 0 }}</span>
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

        <!-- Bids Section -->
        <v-card v-if="showBids" elevation="2" rounded="xl" class="mb-4">
          <v-card-title class="pa-4 pa-md-6 d-flex align-center justify-space-between">
            <span>پیشنهادات</span>
            <v-btn
              v-if="auction.status === 'closed' && !auction.winner_info"
              color="primary"
              @click="loadBids"
            >
              مشاهده پیشنهادات
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-4 pa-md-6">
            <v-data-table
              v-if="bids.length > 0"
              :headers="bidHeaders"
              :items="bids"
              :loading="loadingBids"
              class="elevation-0"
            >
              <template v-slot:item.amount="{ item }">
                <span class="text-h6 text-primary">
                  {{ formatPrice(item.amount) }} تومان
                </span>
              </template>
              <template v-slot:item.rank="{ item }">
                <RankBadge :rank="item.rank" size="small" />
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  v-if="auction.status === 'closed' && !auction.winner_info"
                  color="success"
                  size="small"
                  :loading="awardingBidId === item.id"
                  @click="awardAuction(item.id)"
                >
                  اعطا
                </v-btn>
                <v-chip
                  v-else-if="auction.winner_info && auction.winner_info.bid_id === item.id"
                  color="success"
                  variant="tonal"
                >
                  برنده
                </v-chip>
              </template>
            </v-data-table>
            <v-alert
              v-else-if="!loadingBids"
              type="info"
              variant="tonal"
            >
              هنوز پیشنهادی ثبت نشده است
            </v-alert>
          </v-card-text>
        </v-card>

        <!-- Winner Info -->
        <v-card v-if="auction.winner_info" elevation="2" rounded="xl" class="mb-4">
          <v-card-title class="pa-4 pa-md-6 text-success">
            <v-icon start>mdi-trophy</v-icon>
            برنده مناقصه
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-4 pa-md-6">
            <div>
              <strong>تامین‌کننده:</strong>
              <span class="ms-2">{{ auction.winner_info.supplier_name }}</span>
            </div>
            <div class="mt-2">
              <strong>مبلغ پیشنهاد:</strong>
              <span class="text-h6 text-primary ms-2">
                {{ formatPrice(auction.winner_info.amount) }} تومان
              </span>
            </div>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuctionApi } from '~/composables/useAuctionApi'
import { useToast } from '~/composables/useToast'
import CountdownTimer from '~/components/auction/CountdownTimer.vue'
import RankBadge from '~/components/auction/RankBadge.vue'

definePageMeta({
  middleware: 'authenticated'
})

const route = useRoute()
const router = useRouter()
const { getAuctionDetail, getBids, awardAuction: awardAuctionApi } = useAuctionApi()
const { showToast } = useToast()

const loading = ref(true)
const loadingBids = ref(false)
const auction = ref<any>(null)
const bids = ref<any[]>([])
const awardingBidId = ref<number | null>(null)

const showBids = computed(() => {
  if (!auction.value) return false
  const now = new Date()
  const deadline = new Date(auction.value.deadline)
  return auction.value.status !== 'active' || now >= deadline
})

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

const bidHeaders = [
  { title: 'رتبه', key: 'rank', align: 'start' },
  { title: 'تامین‌کننده', key: 'supplier_name', align: 'start' },
  { title: 'مبلغ', key: 'amount', align: 'start' },
  { title: 'تاریخ', key: 'created_at', align: 'start' },
  { title: 'عملیات', key: 'actions', align: 'start', sortable: false }
]

const formatPrice = (price: number | string) => {
  const num = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(num)
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

const loadBids = async () => {
  try {
    loadingBids.value = true
    const id = parseInt(route.params.id as string)
    const response = await getBids(id)
    bids.value = response.bids || []
  } catch (error: any) {
    console.error('Error loading bids:', error)
    showToast('خطا در بارگذاری پیشنهادات', 'error')
  } finally {
    loadingBids.value = false
  }
}

const awardAuction = async (bidId: number) => {
  try {
    awardingBidId.value = bidId
    const id = parseInt(route.params.id as string)
    await awardAuctionApi(id, bidId)
    showToast('مناقصه با موفقیت اعطا شد', 'success')
    await loadAuction()
    await loadBids()
  } catch (error: any) {
    console.error('Error awarding auction:', error)
    showToast(error.data?.error || 'خطا در اعطای مناقصه', 'error')
  } finally {
    awardingBidId.value = null
  }
}

onMounted(async () => {
  await loadAuction()
  if (showBids.value) {
    await loadBids()
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

