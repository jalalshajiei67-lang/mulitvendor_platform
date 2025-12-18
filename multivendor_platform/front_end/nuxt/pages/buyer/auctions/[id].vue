<template>
  <v-container fluid dir="rtl" class="pt-6">
    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else-if="auction">
      <v-col cols="12">
        <v-btn
          variant="text"
          prepend-icon="mdi-arrow-right"
          @click="navigateTo('/buyer/dashboard?tab=auctions')"
          class="mb-4"
        >
          بازگشت به لیست مناقصه‌ها
        </v-btn>

        <v-card elevation="2">
          <v-card-title class="d-flex align-center justify-space-between bg-primary text-white pa-4">
            <div>
              <h2 class="text-h5">مناقصه #{{ auction.id }}</h2>
              <v-chip
                :color="getStatusColor(auction.status)"
                class="mt-2"
              >
                {{ getStatusLabel(auction.status) }}
              </v-chip>
            </div>
            <v-chip
              v-if="auction.deposit_status === 'held_in_escrow'"
              color="success"
              prepend-icon="mdi-check-circle"
            >
              واریز پرداخت شده
            </v-chip>
          </v-card-title>

          <v-card-text class="pa-6">
            <!-- Auction Details -->
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4">
                  <h3 class="text-subtitle-1 mb-3">اطلاعات مناقصه</h3>
                  <v-list density="compact">
                    <v-list-item>
                      <v-list-item-title>نوع مناقصه</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ auction.auction_style === 'sealed' ? 'پاکتی' : 'زنده معکوس' }}
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>زمان شروع</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ formatDateTime(auction.start_time) }}
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>زمان پایان</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ formatDateTime(auction.end_time) }}
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="auction.time_remaining">
                      <v-list-item-title>زمان باقی‌مانده</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ formatTimeRemaining(auction.time_remaining) }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4">
                  <h3 class="text-subtitle-1 mb-3">توضیحات</h3>
                  <p class="text-body-1">{{ auction.description }}</p>
                </v-card>
              </v-col>
            </v-row>

            <!-- Bids Section -->
            <v-card variant="outlined" class="pa-4 mb-4">
              <div class="d-flex align-center justify-space-between mb-4">
                <h3 class="text-subtitle-1">پیشنهادات ({{ auction.bid_count }})</h3>
                <v-btn
                  v-if="auction.status === 'active' && auction.can_close_early"
                  color="success"
                  @click="handleCloseEarly"
                  :loading="closing"
                >
                  بستن زودهنگام
                </v-btn>
              </div>

              <v-data-table
                :headers="bidHeaders"
                :items="auction.bids || []"
                item-value="id"
                class="elevation-1"
              >
                <template v-slot:item.seller_name="{ item }">
                  <strong>{{ item.seller_name || 'نامشخص' }}</strong>
                </template>
                <template v-slot:item.price="{ item }">
                  <span class="font-weight-bold text-success">
                    {{ formatPrice(item.price) }} تومان
                  </span>
                </template>
                <template v-slot:item.created_at="{ item }">
                  {{ formatDate(item.created_at) }}
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    v-if="auction.status === 'active' && auction.can_close_early"
                    color="primary"
                    size="small"
                    @click="handleAcceptBid(item.id)"
                    :loading="accepting"
                  >
                    پذیرش
                  </v-btn>
                </template>
                <template v-slot:no-data>
                  <div class="text-center py-8">
                    <v-icon size="64" color="grey-lighten-1">mdi-gavel</v-icon>
                    <p class="text-body-1 mt-4 text-grey">هنوز پیشنهادی ثبت نشده است</p>
                  </div>
                </template>
              </v-data-table>
            </v-card>

            <!-- Photos -->
            <v-card v-if="auction.photos && auction.photos.length > 0" variant="outlined" class="pa-4 mb-4">
              <h3 class="text-subtitle-1 mb-3">تصاویر</h3>
              <div class="d-flex flex-wrap gap-2">
                <v-img
                  v-for="photo in auction.photos"
                  :key="photo.id"
                  :src="photo.image_url"
                  width="150"
                  height="150"
                  cover
                  class="rounded"
                ></v-img>
              </div>
            </v-card>

            <!-- Documents -->
            <v-card v-if="auction.documents && auction.documents.length > 0" variant="outlined" class="pa-4">
              <h3 class="text-subtitle-1 mb-3">مستندات</h3>
              <v-list>
                <v-list-item
                  v-for="doc in auction.documents"
                  :key="doc.id"
                  :href="doc.file_url"
                  target="_blank"
                >
                  <template v-slot:prepend>
                    <v-icon>mdi-file-document</v-icon>
                  </template>
                  <v-list-item-title>{{ doc.file_name }}</v-list-item-title>
                  <template v-slot:append>
                    <v-btn icon variant="text" :href="doc.file_url" target="_blank">
                      <v-icon>mdi-download</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col cols="12" class="text-center">
        <v-alert type="error">مناقصه یافت نشد</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuctionApi, type AuctionRequest } from '~/composables/useAuctionApi'
import { useToast } from '~/composables/useToast'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const route = useRoute()
const auctionApi = useAuctionApi()
const { showToast } = useToast()

const auction = ref<AuctionRequest | null>(null)
const loading = ref(true)
const accepting = ref(false)
const closing = ref(false)

const bidHeaders = [
  { title: 'فروشنده', key: 'seller_name', sortable: false },
  { title: 'قیمت', key: 'price', sortable: true },
  { title: 'تاریخ', key: 'created_at', sortable: true },
  { title: 'عملیات', key: 'actions', sortable: false },
]

const loadAuction = async () => {
  loading.value = true
  try {
    const auctionId = parseInt(route.params.id as string)
    auction.value = await auctionApi.getAuctionRequest(auctionId)
  } catch (error) {
    console.error('Error loading auction:', error)
    showToast({ message: 'خطا در بارگذاری مناقصه', color: 'error' })
  } finally {
    loading.value = false
  }
}

const handleAcceptBid = async (bidId: number) => {
  accepting.value = true
  try {
    const auctionId = parseInt(route.params.id as string)
    await auctionApi.acceptBid(auctionId, bidId)
    showToast({ message: 'پیشنهاد با موفقیت پذیرفته شد', color: 'success' })
    await loadAuction()
  } catch (error: any) {
    console.error('Error accepting bid:', error)
    showToast({ message: error.message || 'خطا در پذیرش پیشنهاد', color: 'error' })
  } finally {
    accepting.value = false
  }
}

const handleCloseEarly = async () => {
  closing.value = true
  try {
    const auctionId = parseInt(route.params.id as string)
    await auctionApi.closeEarly(auctionId)
    showToast({ message: 'مناقصه با موفقیت بسته شد', color: 'success' })
    await loadAuction()
  } catch (error: any) {
    console.error('Error closing auction:', error)
    showToast({ message: error.message || 'خطا در بستن مناقصه', color: 'error' })
  } finally {
    closing.value = false
  }
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    draft: 'grey',
    pending_review: 'warning',
    approved: 'info',
    rejected: 'error',
    active: 'success',
    closed: 'primary',
    abandoned: 'error'
  }
  return colors[status] || 'grey'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    draft: 'پیش‌نویس',
    pending_review: 'در انتظار بررسی',
    approved: 'تایید شده',
    rejected: 'رد شده',
    active: 'فعال',
    closed: 'بسته شده',
    abandoned: 'لغو شده'
  }
  return labels[status] || status
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const formatDateTime = (dateString: string | null) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const formatTimeRemaining = (seconds: number) => {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (days > 0) return `${days} روز و ${hours} ساعت`
  if (hours > 0) return `${hours} ساعت و ${minutes} دقیقه`
  return `${minutes} دقیقه`
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('fa-IR').format(price)
}

onMounted(() => {
  loadAuction()
})
</script>

