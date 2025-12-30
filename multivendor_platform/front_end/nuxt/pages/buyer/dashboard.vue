<template>
  <v-container fluid dir="rtl" class="buyer-dashboard pt-6">
    <!-- Main Content Tabs -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2">
          <v-tabs
            v-model="tab"
            bg-color="primary"
            color="white"
            align-tabs="start"
          >
            <v-tab value="home">
              <v-icon start>mdi-home</v-icon>
              صفحه اصلی
            </v-tab>
            <v-tab value="profile">
              <v-icon start>mdi-account</v-icon>
              پروفایل
            </v-tab>
            <v-tab value="orders">
              <v-icon start>mdi-package-variant</v-icon>
              سفارشات
            </v-tab>
            <v-tab value="rfqs">
              <v-icon start>mdi-file-document-edit</v-icon>
              درخواست‌های قیمت
              <v-badge
                v-if="dashboardData.pending_rfqs"
                :content="dashboardData.pending_rfqs"
                color="error"
                inline
                class="mr-1"
              ></v-badge>
            </v-tab>
            <v-tab value="auctions">
              <v-icon start>mdi-gavel</v-icon>
              مناقصه‌ها
            </v-tab>
            <v-tab value="payments">
              <v-icon start>mdi-credit-card</v-icon>
              سوابق پرداخت
            </v-tab>
            <v-tab value="reviews">
              <v-icon start>mdi-comment-text</v-icon>
              نظرات من
            </v-tab>
          </v-tabs>

          <v-card-text class="pa-4">
            <v-window v-model="tab">
              <!-- Home Tab -->
              <v-window-item value="home">
                <div class="py-4">
                  <!-- Welcome Section -->
                  <v-row class="mb-4">
                    <v-col cols="12">
                      <div class="d-flex align-center justify-space-between flex-wrap gap-3">
                        <div>
                          <h2 class="text-h5 mb-2">
                            خوش آمدید {{ authStore.user?.first_name || authStore.user?.username }}!
                          </h2>
                          <p class="text-body-1 text-medium-emphasis">
                            خلاصه فعالیت‌ها و سفارش‌های شما
                          </p>
                        </div>
                        <!-- Quick Actions -->
                        <div class="d-flex gap-2 flex-wrap">
                          <v-btn
                            color="primary"
                            variant="elevated"
                            prepend-icon="mdi-plus-circle"
                            :to="'/rfq'"
                            size="default"
                          >
                            ثبت درخواست جدید
                          </v-btn>
                          <v-btn
                            color="secondary"
                            variant="outlined"
                            prepend-icon="mdi-package-variant"
                            :to="'/products'"
                            size="default"
                          >
                            مشاهده محصولات
                          </v-btn>
                        </div>
                      </div>
                    </v-col>
                  </v-row>

                  <!-- Enhanced Stats Cards -->
                  <v-row class="mb-4">
      <v-col cols="12" sm="6" md="3">
        <v-card
          class="stat-card stat-card-primary"
          elevation="2"
          :loading="loading"
        >
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-caption text-medium-emphasis mb-1">
                  کل سفارشات
                </div>
                <div class="text-h3 font-weight-bold">
                  {{ dashboardData.total_orders || 0 }}
                </div>
              </div>
              <v-avatar
                size="56"
                color="primary"
                class="stat-icon"
              >
                <v-icon size="28">mdi-package-variant</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card
          class="stat-card stat-card-warning"
          elevation="2"
          :loading="loading"
        >
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-caption text-medium-emphasis mb-1">
                  سفارشات در انتظار
                </div>
                <div class="text-h3 font-weight-bold">
                  {{ dashboardData.pending_orders || 0 }}
                </div>
              </div>
              <v-avatar
                size="56"
                color="warning"
                class="stat-icon"
              >
                <v-icon size="28">mdi-clock-outline</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card
          class="stat-card stat-card-success"
          elevation="2"
          :loading="loading"
        >
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-caption text-medium-emphasis mb-1">
                  سفارشات تکمیل شده
                </div>
                <div class="text-h3 font-weight-bold">
                  {{ dashboardData.completed_orders || 0 }}
                </div>
              </div>
              <v-avatar
                size="56"
                color="success"
                class="stat-icon"
              >
                <v-icon size="28">mdi-check-circle</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card
          class="stat-card stat-card-info"
          elevation="2"
          :loading="loading"
        >
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-caption text-medium-emphasis mb-1">
                  درخواست‌های قیمت
                </div>
                <div class="text-h3 font-weight-bold">
                  {{ dashboardData.total_rfqs || 0 }}
                </div>
                <div v-if="dashboardData.pending_rfqs" class="text-caption text-warning mt-1">
                  {{ dashboardData.pending_rfqs }} در انتظار
                </div>
              </div>
              <v-avatar
                size="56"
                color="info"
                class="stat-icon"
              >
                <v-icon size="28">mdi-file-document-edit</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
                  </v-row>

                  <!-- Recent Orders Section -->
                  <v-row class="mb-4" v-if="recentOrders.length > 0">
                    <v-col cols="12">
                      <v-card elevation="1">
                        <v-card-title class="d-flex align-center justify-space-between">
                          <span>سفارشات اخیر</span>
                          <v-btn
                            variant="text"
                            size="small"
                            @click="tab = 'orders'"
                          >
                            مشاهده همه
                            <v-icon end>mdi-chevron-left</v-icon>
                          </v-btn>
                        </v-card-title>
                        <v-card-text>
                          <v-list>
                            <v-list-item
                              v-for="order in recentOrders"
                              :key="order.id"
                              :title="`سفارش ${order.order_number}`"
                              :subtitle="`مبلغ: ${formatPrice(order.total_amount)} تومان - ${formatDate(order.created_at)}`"
                            >
                              <template v-slot:append>
                                <v-chip
                                  :color="getStatusColor(order.status)"
                                  size="small"
                                  variant="flat"
                                >
                                  {{ getStatusLabel(order.status) }}
                                </v-chip>
                              </template>
                            </v-list-item>
                          </v-list>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>

                  <!-- Recent RFQs Section -->
                  <v-row class="mb-4" v-if="recentRFQs.length > 0">
                    <v-col cols="12">
                      <v-card elevation="1">
                        <v-card-title class="d-flex align-center justify-space-between">
                          <span>درخواست‌های قیمت اخیر</span>
                          <v-btn
                            variant="text"
                            size="small"
                            @click="tab = 'rfqs'"
                          >
                            مشاهده همه
                            <v-icon end>mdi-chevron-left</v-icon>
                          </v-btn>
                        </v-card-title>
                        <v-card-text>
                          <v-list>
                            <v-list-item
                              v-for="rfq in recentRFQs"
                              :key="rfq.id"
                              :title="`درخواست ${rfq.order_number}`"
                              :subtitle="`${rfq.items?.[0]?.product?.name || 'محصول'} - ${formatDate(rfq.created_at)}`"
                            >
                              <template v-slot:append>
                                <v-chip
                                  :color="getStatusColor(rfq.status)"
                                  size="small"
                                  variant="flat"
                                >
                                  {{ getStatusLabel(rfq.status) }}
                                </v-chip>
                              </template>
                            </v-list-item>
                          </v-list>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>
              </v-window-item>
              <!-- Profile Tab -->
              <v-window-item value="profile">
                <div class="py-4">
                  <h3 class="text-h6 mb-4">اطلاعات شخصی</h3>
                  <v-form ref="profileForm" @submit.prevent="updateProfile">
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileData.first_name"
                          label="نام"
                          prepend-inner-icon="mdi-account"
                          variant="outlined"
                          density="comfortable"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileData.last_name"
                          label="نام خانوادگی"
                          prepend-inner-icon="mdi-account"
                          variant="outlined"
                          density="comfortable"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileData.email"
                          label="ایمیل"
                          prepend-inner-icon="mdi-email"
                          type="email"
                          variant="outlined"
                          density="comfortable"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="profileData.phone"
                          label="تلفن"
                          prepend-inner-icon="mdi-phone"
                          variant="outlined"
                          density="comfortable"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-textarea
                      v-model="profileData.address"
                      label="آدرس"
                      prepend-inner-icon="mdi-map-marker"
                      rows="3"
                      variant="outlined"
                      density="comfortable"
                    ></v-textarea>
                    <v-btn
                      color="primary"
                      type="submit"
                      :loading="saving"
                      size="large"
                      prepend-icon="mdi-content-save"
                    >
                      به‌روزرسانی پروفایل
                    </v-btn>
                  </v-form>
                </div>
              </v-window-item>

              <!-- Orders Tab -->
              <v-window-item value="orders">
                <div class="py-4">
                  <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                    <h3 class="text-h6">سفارشات من</h3>
                    <div class="d-flex gap-2">
                      <v-select
                        v-model="orderStatusFilter"
                        :items="statusFilters"
                        label="فیلتر بر اساس وضعیت"
                        density="compact"
                        variant="outlined"
                        hide-details
                        style="max-width: 200px;"
                      ></v-select>
                    </div>
                  </div>
                  
                  <v-data-table
                    :headers="orderHeaders"
                    :items="filteredOrders"
                    :loading="loadingOrders"
                    item-value="id"
                    class="elevation-1"
                    :items-per-page="10"
                  >
                    <template v-slot:item.order_number="{ item }">
                      <strong class="text-primary">{{ item.order_number }}</strong>
                    </template>
                    <template v-slot:item.status="{ item }">
                      <v-chip
                        :color="getStatusColor(item.status)"
                        size="small"
                        variant="flat"
                      >
                        {{ getStatusLabel(item.status) }}
                      </v-chip>
                    </template>
                    <template v-slot:item.total_amount="{ item }">
                      <span class="font-weight-bold">
                        {{ formatPrice(item.total_amount) }} تومان
                      </span>
                    </template>
                    <template v-slot:item.is_paid="{ item }">
                      <v-icon :color="item.is_paid ? 'success' : 'error'">
                        {{ item.is_paid ? 'mdi-check-circle' : 'mdi-close-circle' }}
                      </v-icon>
                      <span class="mr-2 text-caption">
                        {{ item.is_paid ? 'پرداخت شده' : 'پرداخت نشده' }}
                      </span>
                    </template>
                    <template v-slot:item.created_at="{ item }">
                      {{ formatDate(item.created_at) }}
                    </template>
                    <template v-slot:no-data>
                      <div class="text-center py-8">
                        <v-icon size="64" color="grey-lighten-1">mdi-package-variant</v-icon>
                        <p class="text-body-1 mt-4 text-grey">سفارشی یافت نشد</p>
                      </div>
                    </template>
                  </v-data-table>
                </div>
              </v-window-item>

              <!-- RFQs Tab -->
              <v-window-item value="rfqs">
                <div class="py-4">
                  <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
                    <h3 class="text-h6">درخواست‌های قیمت من</h3>
                    <v-btn
                      color="primary"
                      prepend-icon="mdi-plus"
                      @click="navigateTo('/rfq')"
                    >
                      ایجاد درخواست جدید
                    </v-btn>
                  </div>
                  
                  <v-data-table
                    :headers="rfqHeaders"
                    :items="rfqs"
                    :loading="loadingRFQs"
                    item-value="id"
                    class="elevation-1"
                    :items-per-page="10"
                  >
                    <template v-slot:item.order_number="{ item }">
                      <strong class="text-info">{{ item.order_number }}</strong>
                    </template>
                    <template v-slot:item.product="{ item }">
                      {{ item.items?.[0]?.product?.name || 'محصول حذف شده' }}
                    </template>
                    <template v-slot:item.status="{ item }">
                      <v-chip
                        :color="getStatusColor(item.status)"
                        size="small"
                        variant="flat"
                      >
                        {{ getStatusLabel(item.status) }}
                      </v-chip>
                    </template>
                    <template v-slot:item.unique_needs="{ item }">
                      <span class="text-body-2">
                        {{ item.unique_needs || '-' }}
                      </span>
                    </template>
                    <template v-slot:item.created_at="{ item }">
                      {{ formatDate(item.created_at) }}
                    </template>
                    <template v-slot:no-data>
                      <div class="text-center py-8">
                        <v-icon size="64" color="grey-lighten-1">mdi-file-document-edit</v-icon>
                        <p class="text-body-1 mt-4 text-grey">درخواست قیمتی یافت نشد</p>
                        <v-btn
                          color="primary"
                          class="mt-4"
                          prepend-icon="mdi-plus"
                          @click="navigateTo('/rfq')"
                        >
                          ایجاد درخواست جدید
                        </v-btn>
                      </div>
                    </template>
                  </v-data-table>
                </div>
              </v-window-item>

              <!-- Payments Tab -->
              <v-window-item value="payments">
                <div class="py-4">
                  <h3 class="text-h6 mb-4">سوابق پرداخت</h3>
                  <v-data-table
                    :headers="paymentHeaders"
                    :items="paymentRecords"
                    :loading="loadingOrders"
                    item-value="id"
                    class="elevation-1"
                    :items-per-page="10"
                  >
                    <template v-slot:item.order_number="{ item }">
                      <strong class="text-primary">{{ item.order_number }}</strong>
                    </template>
                    <template v-slot:item.total_amount="{ item }">
                      <span class="font-weight-bold text-success">
                        {{ formatPrice(item.total_amount) }} تومان
                      </span>
                    </template>
                    <template v-slot:item.payment_method="{ item }">
                      <v-chip size="small" variant="outlined">
                        {{ item.payment_method || 'N/A' }}
                      </v-chip>
                    </template>
                    <template v-slot:item.payment_date="{ item }">
                      {{ item.payment_date ? formatDate(item.payment_date) : 'N/A' }}
                    </template>
                    <template v-slot:no-data>
                      <div class="text-center py-8">
                        <v-icon size="64" color="grey-lighten-1">mdi-credit-card</v-icon>
                        <p class="text-body-1 mt-4 text-grey">سابقه پرداختی یافت نشد</p>
                      </div>
                    </template>
                  </v-data-table>
                </div>
              </v-window-item>

              <!-- Reviews Tab -->
              <v-window-item value="reviews">
                <div class="py-4">
                  <h3 class="text-h6 mb-4">نظرات من</h3>
                  <v-data-table
                    :headers="reviewHeaders"
                    :items="reviews"
                    :loading="loadingReviews"
                    item-value="id"
                    class="elevation-1"
                    :items-per-page="10"
                  >
                    <template v-slot:item.product="{ item }">
                      <strong>{{ item.product?.name || 'محصول حذف شده' }}</strong>
                    </template>
                    <template v-slot:item.rating="{ item }">
                      <v-rating
                        :model-value="item.rating"
                        readonly
                        size="small"
                        density="compact"
                        color="warning"
                      ></v-rating>
                    </template>
                    <template v-slot:item.comment="{ item }">
                      <span class="text-body-2">{{ item.comment || '-' }}</span>
                    </template>
                    <template v-slot:item.created_at="{ item }">
                      {{ formatDate(item.created_at) }}
                    </template>
                    <template v-slot:no-data>
                      <div class="text-center py-8">
                        <v-icon size="64" color="grey-lighten-1">mdi-comment-text</v-icon>
                        <p class="text-body-1 mt-4 text-grey">نظری ثبت نشده است</p>
                      </div>
                    </template>
                  </v-data-table>
                </div>
              </v-window-item>
              <!-- Auctions Tab -->
              <v-window-item value="auctions">
                <div class="py-4">
                  <div class="d-flex align-center justify-space-between mb-4">
                    <h3 class="text-h6">مناقصه‌ها</h3>
                    <v-btn
                      color="primary"
                      prepend-icon="mdi-plus"
                      :to="'/buyer/create-auction'"
                    >
                      ایجاد مناقصه جدید
                    </v-btn>
                  </div>
                  <v-row v-if="loadingAuctions" justify="center">
                    <v-col cols="12" class="text-center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-col>
                  </v-row>
                  <v-row v-else-if="auctions.length > 0">
                    <v-col
                      v-for="auction in auctions"
                      :key="auction.id"
                      cols="12"
                      md="6"
                      lg="4"
                    >
                      <AuctionCard :auction="auction" user-role="buyer" />
                    </v-col>
                  </v-row>
                  <v-alert v-else type="info" variant="tonal">
                    هنوز مناقصه‌ای ایجاد نکرده‌اید
                  </v-alert>
                </div>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useBuyerApi } from '~/composables/useBuyerApi'
import { useAuctionApi } from '~/composables/useAuctionApi'
import type { BuyerOrder, BuyerReview, BuyerRFQ } from '~/composables/useBuyerApi'
import AuctionCard from '~/components/auction/AuctionCard.vue'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const authStore = useAuthStore()
const buyerApi = useBuyerApi()
const auctionApi = useAuctionApi()
const route = useRoute()

// Check for tab query parameter - default to 'home'
const tabQuery = computed(() => route.query.tab as string || 'home')
const tab = ref(tabQuery.value)

// Watch for route query changes
watch(() => route.query.tab, (newTab) => {
  if (newTab && typeof newTab === 'string') {
    tab.value = newTab
  }
})

const dashboardData = ref({
  total_orders: 0,
  pending_orders: 0,
  completed_orders: 0,
  total_reviews: 0,
  total_rfqs: 0,
  pending_rfqs: 0
})

const orders = ref<BuyerOrder[]>([])
const rfqs = ref<BuyerRFQ[]>([])
const reviews = ref<BuyerReview[]>([])
const auctions = ref<any[]>([])
const loading = ref(false)
const loadingOrders = ref(false)
const loadingRFQs = ref(false)
const loadingReviews = ref(false)
const loadingAuctions = ref(false)
const saving = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')
const orderStatusFilter = ref('all')

const profileData = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address: ''
})

const statusFilters = [
  { title: 'همه', value: 'all' },
  { title: 'در انتظار', value: 'pending' },
  { title: 'تایید شده', value: 'confirmed' },
  { title: 'در حال پردازش', value: 'processing' },
  { title: 'ارسال شده', value: 'shipped' },
  { title: 'تحویل داده شده', value: 'delivered' },
  { title: 'لغو شده', value: 'cancelled' }
]

const orderHeaders = [
  { title: 'شماره سفارش', key: 'order_number', sortable: true },
  { title: 'وضعیت', key: 'status', sortable: true },
  { title: 'مبلغ کل', key: 'total_amount', sortable: true },
  { title: 'پرداخت', key: 'is_paid', sortable: true },
  { title: 'تاریخ', key: 'created_at', sortable: true }
]

const rfqHeaders = [
  { title: 'شماره درخواست', key: 'order_number', sortable: true },
  { title: 'محصول', key: 'product', sortable: false },
  { title: 'وضعیت', key: 'status', sortable: true },
  { title: 'نیازهای خاص', key: 'unique_needs', sortable: false },
  { title: 'تاریخ', key: 'created_at', sortable: true }
]

const paymentHeaders = [
  { title: 'شماره سفارش', key: 'order_number', sortable: true },
  { title: 'مبلغ', key: 'total_amount', sortable: true },
  { title: 'روش پرداخت', key: 'payment_method', sortable: false },
  { title: 'تاریخ پرداخت', key: 'payment_date', sortable: true }
]

const reviewHeaders = [
  { title: 'محصول', key: 'product', sortable: false },
  { title: 'امتیاز', key: 'rating', sortable: true },
  { title: 'نظر', key: 'comment', sortable: false },
  { title: 'تاریخ', key: 'created_at', sortable: true }
]

const filteredOrders = computed(() => {
  const regularOrders = orders.value.filter(order => !order.is_rfq)
  if (orderStatusFilter.value === 'all') {
    return regularOrders
  }
  return regularOrders.filter(order => order.status === orderStatusFilter.value)
})

const paymentRecords = computed(() => {
  return orders.value.filter(order => order.is_paid && !order.is_rfq)
})

const loadDashboardData = async () => {
  loading.value = true
  try {
    const response = await buyerApi.getBuyerDashboard()
    dashboardData.value = response
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    showSnackbar('خطا در بارگذاری اطلاعات داشبورد', 'error')
  } finally {
    loading.value = false
  }
}

const loadOrders = async () => {
  loadingOrders.value = true
  try {
    const response = await buyerApi.getBuyerOrders()
    orders.value = response
  } catch (error) {
    console.error('Failed to load orders:', error)
    showSnackbar('خطا در بارگذاری سفارشات', 'error')
  } finally {
    loadingOrders.value = false
  }
}

const loadRFQs = async () => {
  loadingRFQs.value = true
  try {
    const response = await buyerApi.getBuyerRFQs()
    rfqs.value = response
  } catch (error) {
    console.error('Failed to load RFQs:', error)
    showSnackbar('خطا در بارگذاری درخواست‌های قیمت', 'error')
  } finally {
    loadingRFQs.value = false
  }
}

const loadReviews = async () => {
  loadingReviews.value = true
  try {
    const response = await buyerApi.getBuyerReviews()
    reviews.value = response
  } catch (error) {
    console.error('Failed to load reviews:', error)
    showSnackbar('خطا در بارگذاری نظرات', 'error')
  } finally {
    loadingReviews.value = false
  }
}

const loadAuctions = async () => {
  loadingAuctions.value = true
  try {
    const response = await auctionApi.getAuctions()
    auctions.value = response.results || response || []
  } catch (error) {
    console.error('Failed to load auctions:', error)
    showSnackbar('خطا در بارگذاری مناقصه‌ها', 'error')
  } finally {
    loadingAuctions.value = false
  }
}

const updateProfile = async () => {
  saving.value = true
  try {
    await authStore.updateProfile(profileData.value)
    showSnackbar('پروفایل با موفقیت به‌روزرسانی شد', 'success')
    // Redirect to home tab after successful update
    setTimeout(() => {
      tab.value = 'home'
      navigateTo('/buyer/dashboard?tab=home', { replace: true })
    }, 1000)
  } catch (error) {
    console.error('Failed to update profile:', error)
    showSnackbar('خطا در به‌روزرسانی پروفایل', 'error')
  } finally {
    saving.value = false
  }
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'warning',
    confirmed: 'info',
    processing: 'primary',
    shipped: 'pink',
    delivered: 'success',
    cancelled: 'error',
    rejected: 'error'
  }
  return colors[status] || 'grey'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    pending: 'در انتظار',
    confirmed: 'تایید شده',
    processing: 'در حال پردازش',
    shipped: 'ارسال شده',
    delivered: 'تحویل داده شده',
    cancelled: 'لغو شده',
    rejected: 'رد شده'
  }
  return labels[status] || status
}

const formatDate = (dateString: string) => {
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

const formatPrice = (price: string | number) => {
  if (!price) return '0'
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(numPrice)
}

const showSnackbar = (message: string, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

// Computed for recent orders and RFQs
const recentOrders = computed(() => {
  return orders.value
    .filter(order => !order.is_rfq)
    .slice(0, 5)
})

const recentRFQs = computed(() => {
  return rfqs.value.slice(0, 3)
})

// Watch tab changes to load data
watch(tab, (newTab) => {
  // Update URL query when tab changes
  navigateTo(`/buyer/dashboard?tab=${newTab}`, { replace: true })
  
  if (newTab === 'rfqs' && rfqs.value.length === 0) {
    loadRFQs()
  } else if (newTab === 'orders' && orders.value.length === 0) {
    loadOrders()
  } else if (newTab === 'reviews' && reviews.value.length === 0) {
    loadReviews()
  } else if (newTab === 'auctions' && auctions.value.length === 0) {
    loadAuctions()
  }
})

onMounted(() => {
  if (authStore.user) {
    profileData.value = {
      first_name: authStore.user.first_name || '',
      last_name: authStore.user.last_name || '',
      email: authStore.user.email || '',
      phone: authStore.user.profile?.phone || '',
      address: authStore.user.profile?.address || ''
    }
  }
  loadDashboardData()
  loadOrders()
  loadReviews()
  loadRFQs() // Load RFQs for home tab display
})
</script>

<style scoped>
.buyer-dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding-top: 80px !important;
}

.stat-card {
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.stat-icon {
  opacity: 0.9;
}

.stat-card-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-card-warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-card-success {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-card-info {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-card-primary :deep(.text-caption),
.stat-card-primary :deep(.text-h3) {
  color: white !important;
}

.stat-card-warning :deep(.text-caption),
.stat-card-warning :deep(.text-h3) {
  color: white !important;
}

.stat-card-success :deep(.text-caption),
.stat-card-success :deep(.text-h3) {
  color: white !important;
}

.stat-card-info :deep(.text-caption),
.stat-card-info :deep(.text-h3),
.stat-card-info :deep(.text-warning) {
  color: white !important;
}
</style>
