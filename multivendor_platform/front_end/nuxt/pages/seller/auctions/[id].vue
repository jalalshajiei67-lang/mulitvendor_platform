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
          @click="navigateTo('/seller/dashboard?tab=auctions')"
          class="mb-4"
        >
          بازگشت به لیست مناقصه‌ها
        </v-btn>

        <v-card elevation="2">
          <v-card-title class="d-flex align-center justify-space-between bg-primary text-white pa-4">
            <div>
              <h2 class="text-h5">مناقصه #{{ auction.id }}</h2>
              <v-chip
                :color="getDepositBadgeColor(auction.deposit_status)"
                class="mt-2"
              >
                {{ getDepositBadgeLabel(auction.deposit_status) }}
              </v-chip>
            </div>
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
                  <h3 class="text-subtitle-1 mb-3">توضیحات نیاز</h3>
                  <p class="text-body-1">{{ auction.description }}</p>
                </v-card>
              </v-col>
            </v-row>

            <!-- Technical Specs -->
            <v-card v-if="auction.technical_specs && Object.keys(auction.technical_specs).length > 0" variant="outlined" class="pa-4 mb-4">
              <h3 class="text-subtitle-1 mb-3">مشخصات فنی مورد نیاز</h3>
              <v-list density="compact">
                <v-list-item
                  v-for="(value, key) in auction.technical_specs"
                  :key="key"
                >
                  <v-list-item-title>{{ key }}</v-list-item-title>
                  <v-list-item-subtitle>{{ value }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card>

            <!-- Other Bids (with identity masking) -->
            <v-card variant="outlined" class="pa-4 mb-4">
              <h3 class="text-subtitle-1 mb-3">پیشنهادات دیگر ({{ auction.bid_count }})</h3>
              <v-data-table
                :headers="bidHeaders"
                :items="otherBids"
                item-value="id"
                class="elevation-1"
              >
                <template v-slot:item.seller_name="{ item }">
                  <span v-if="item.bidder_number">{{ item.bidder_number }}</span>
                  <span v-else>{{ item.seller_name || 'نامشخص' }}</span>
                </template>
                <template v-slot:item.price="{ item }">
                  <span class="font-weight-bold text-success">
                    {{ formatPrice(item.price) }} تومان
                  </span>
                </template>
                <template v-slot:item.created_at="{ item }">
                  {{ formatDate(item.created_at) }}
                </template>
                <template v-slot:no-data>
                  <div class="text-center py-4">
                    <p class="text-body-2 text-grey">هنوز پیشنهادی ثبت نشده است</p>
                  </div>
                </template>
              </v-data-table>
            </v-card>

            <!-- My Bid -->
            <v-card v-if="myBid" variant="tonal" class="pa-4 mb-4" color="primary">
              <h3 class="text-subtitle-1 mb-3">پیشنهاد من</h3>
              <v-list density="compact">
                <v-list-item>
                  <v-list-item-title>قیمت پیشنهادی</v-list-item-title>
                  <v-list-item-subtitle class="font-weight-bold text-success">
                    {{ formatPrice(myBid.price) }} تومان
                  </v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>تاریخ ثبت</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(myBid.created_at) }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item v-if="myBid.is_winner">
                  <v-chip color="success" size="small">برنده</v-chip>
                </v-list-item>
              </v-list>
            </v-card>

            <!-- Bid Form -->
            <v-card v-if="!myBid && auction.status === 'active'" variant="outlined" class="pa-4">
              <h3 class="text-subtitle-1 mb-4">ثبت پیشنهاد</h3>
              <v-form ref="bidFormRef" @submit.prevent="submitBid">
                <!-- Technical Compliance -->
                <div v-if="featureTemplates.length > 0" class="mb-4">
                  <h4 class="text-body-1 mb-3">ماتریس انطباق فنی</h4>
                  <v-card variant="outlined" class="pa-4">
                    <div
                      v-for="template in featureTemplates"
                      :key="template.id"
                      class="mb-3"
                    >
                      <v-text-field
                        v-model="bidForm.technical_compliance[template.feature_name]"
                        :label="template.feature_name"
                        :required="template.is_required"
                        variant="outlined"
                        :rules="template.is_required ? [v => !!v || 'این فیلد الزامی است'] : []"
                      ></v-text-field>
                    </div>
                  </v-card>
                </div>

                <!-- Price -->
                <v-text-field
                  v-model.number="bidForm.price"
                  label="قیمت پیشنهادی (تومان)"
                  prepend-inner-icon="mdi-currency-usd"
                  variant="outlined"
                  type="number"
                  :rules="[v => !!v || 'قیمت الزامی است', v => v > 0 || 'قیمت باید بیشتر از صفر باشد']"
                  required
                  class="mb-4"
                ></v-text-field>

                <!-- Additional Notes -->
                <v-textarea
                  v-model="bidForm.additional_notes"
                  label="یادداشت‌های اضافی (اختیاری)"
                  variant="outlined"
                  rows="3"
                  class="mb-4"
                ></v-textarea>

                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  block
                  :loading="submitting"
                  prepend-icon="mdi-send"
                >
                  ثبت پیشنهاد
                </v-btn>
              </v-form>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuctionApi, type AuctionRequest, type Bid } from '~/composables/useAuctionApi'
import { useProductApi } from '~/composables/useProductApi'
import { useAuthStore } from '~/stores/auth'
import { useToast } from '~/composables/useToast'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const route = useRoute()
const auctionApi = useAuctionApi()
const productApi = useProductApi()
const authStore = useAuthStore()
const { showToast } = useToast()

const auction = ref<AuctionRequest | null>(null)
const loading = ref(true)
const submitting = ref(false)
const featureTemplates = ref<any[]>([])
const bidFormRef = ref()

const bidForm = ref({
  price: null as number | null,
  technical_compliance: {} as Record<string, string>,
  additional_notes: ''
})

const bidHeaders = [
  { title: 'پیشنهاددهنده', key: 'seller_name', sortable: false },
  { title: 'قیمت', key: 'price', sortable: true },
  { title: 'تاریخ', key: 'created_at', sortable: true },
]

const myBid = computed(() => {
  if (!auction.value || !auction.value.bids) return null
  return auction.value.bids.find((bid: Bid) => bid.seller_id === authStore.user?.id) || null
})

const otherBids = computed(() => {
  if (!auction.value || !auction.value.bids) return []
  return auction.value.bids.filter((bid: Bid) => bid.seller_id !== authStore.user?.id)
})

const loadAuction = async () => {
  loading.value = true
  try {
    const auctionId = parseInt(route.params.id as string)
    auction.value = await auctionApi.getAuctionRequest(auctionId)
    
    // Load feature templates if subcategory exists
    if (auction.value.subcategory) {
      await loadFeatureTemplates(auction.value.subcategory)
    }
  } catch (error) {
    console.error('Error loading auction:', error)
    showToast({ message: 'خطا در بارگذاری مناقصه', color: 'error' })
  } finally {
    loading.value = false
  }
}

const loadFeatureTemplates = async (subcategoryId: number) => {
  try {
    const response = await productApi.getSubcategoryFeatureTemplates(subcategoryId)
    if (response && (response as any).results) {
      featureTemplates.value = (response as any).results
      // Initialize technical_compliance
      featureTemplates.value.forEach((template: any) => {
        bidForm.value.technical_compliance[template.feature_name] = ''
      })
    }
  } catch (error) {
    console.error('Error loading feature templates:', error)
  }
}

const submitBid = async () => {
  const { valid } = await bidFormRef.value.validate()
  if (!valid) return

  submitting.value = true
  try {
    const auctionId = parseInt(route.params.id as string)
    await auctionApi.createBid({
      auction: auctionId,
      price: bidForm.value.price,
      technical_compliance: bidForm.value.technical_compliance,
      additional_notes: bidForm.value.additional_notes
    })
    
    showToast({ message: 'پیشنهاد با موفقیت ثبت شد', color: 'success' })
    await loadAuction()
    
    // Reset form
    bidForm.value = {
      price: null,
      technical_compliance: {},
      additional_notes: ''
    }
  } catch (error: any) {
    console.error('Error submitting bid:', error)
    showToast({ message: error.message || 'خطا در ثبت پیشنهاد', color: 'error' })
  } finally {
    submitting.value = false
  }
}

const getDepositBadgeColor = (status: string) => {
  if (status === 'held_in_escrow') return 'success'
  if (status === 'paid') return 'success'
  return 'grey'
}

const getDepositBadgeLabel = (status: string) => {
  if (status === 'held_in_escrow') return 'واریز پرداخت شده'
  if (status === 'paid') return 'پرداخت شده'
  return 'بدون واریز'
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

