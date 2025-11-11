<template>
  <v-container fluid dir="rtl">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">
          <v-icon left>mdi-view-dashboard</v-icon>
          داشبورد خریدار
        </h1>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="text-h6">کل سفارشات</div>
            <div class="text-h3">{{ dashboardData.total_orders || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark>
          <v-card-text>
            <div class="text-h6">سفارشات در انتظار</div>
            <div class="text-h3">{{ dashboardData.pending_orders || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark>
          <v-card-text>
            <div class="text-h6">سفارشات تکمیل شده</div>
            <div class="text-h3">{{ dashboardData.completed_orders || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark>
          <v-card-text>
            <div class="text-h6">کل نظرات</div>
            <div class="text-h3">{{ dashboardData.total_reviews || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tabs -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-tabs v-model="tab" bg-color="primary">
            <v-tab value="profile">
              <v-icon left>mdi-account</v-icon>
              پروفایل
            </v-tab>
            <v-tab value="orders">
              <v-icon left>mdi-package-variant</v-icon>
              تاریخچه سفارشات
            </v-tab>
            <v-tab value="payments">
              <v-icon left>mdi-credit-card</v-icon>
              سوابق پرداخت
            </v-tab>
            <v-tab value="reviews">
              <v-icon left>mdi-comment-text</v-icon>
              نظرات من
            </v-tab>
          </v-tabs>

          <v-card-text>
            <v-window v-model="tab">
              <!-- Profile Tab -->
              <v-window-item value="profile">
                <v-form ref="profileForm" @submit.prevent="updateProfile">
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.first_name"
                        label="نام"
                        prepend-icon="mdi-account"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.last_name"
                        label="نام خانوادگی"
                        prepend-icon="mdi-account"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.email"
                        label="ایمیل"
                        prepend-icon="mdi-email"
                        type="email"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.phone"
                        label="تلفن"
                        prepend-icon="mdi-phone"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-textarea
                    v-model="profileData.address"
                    label="آدرس"
                    prepend-icon="mdi-map-marker"
                    rows="3"
                  ></v-textarea>
                  <v-btn color="primary" type="submit" :loading="saving">
                    به‌روزرسانی پروفایل
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- Orders Tab -->
              <v-window-item value="orders">
                <v-data-table
                  :headers="orderHeaders"
                  :items="orders"
                  :loading="loadingOrders"
                  item-value="id"
                >
                  <template v-slot:item.order_number="{ item }">
                    <strong>{{ item.order_number }}</strong>
                  </template>
                  <template v-slot:item.status="{ item }">
                    <v-chip :color="getStatusColor(item.status)" small>
                      {{ item.status }}
                    </v-chip>
                  </template>
                  <template v-slot:item.total_amount="{ item }">
                    {{ formatPrice(item.total_amount) }} تومان
                  </template>
                  <template v-slot:item.is_paid="{ item }">
                    <v-icon :color="item.is_paid ? 'success' : 'error'">
                      {{ item.is_paid ? 'mdi-check-circle' : 'mdi-close-circle' }}
                    </v-icon>
                  </template>
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                  </template>
                </v-data-table>
              </v-window-item>

              <!-- Payments Tab -->
              <v-window-item value="payments">
                <v-data-table
                  :headers="paymentHeaders"
                  :items="paymentRecords"
                  :loading="loadingOrders"
                  item-value="id"
                >
                  <template v-slot:item.order_number="{ item }">
                    <strong>{{ item.order_number }}</strong>
                  </template>
                  <template v-slot:item.total_amount="{ item }">
                    {{ formatPrice(item.total_amount) }} تومان
                  </template>
                  <template v-slot:item.payment_method="{ item }">
                    <v-chip small>{{ item.payment_method || 'N/A' }}</v-chip>
                  </template>
                  <template v-slot:item.payment_date="{ item }">
                    {{ item.payment_date ? formatDate(item.payment_date) : 'N/A' }}
                  </template>
                </v-data-table>
              </v-window-item>

              <!-- Reviews Tab -->
              <v-window-item value="reviews">
                <v-data-table
                  :headers="reviewHeaders"
                  :items="reviews"
                  :loading="loadingReviews"
                  item-value="id"
                >
                  <template v-slot:item.product="{ item }">
                    {{ item.product?.name || 'محصول حذف شده' }}
                  </template>
                  <template v-slot:item.rating="{ item }">
                    <v-rating
                      :model-value="item.rating"
                      readonly
                      size="small"
                      density="compact"
                    ></v-rating>
                  </template>
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                  </template>
                </v-data-table>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useBuyerApi } from '~/composables/useBuyerApi'
import type { BuyerOrder, BuyerReview } from '~/composables/useBuyerApi'

definePageMeta({
  middleware: 'authenticated'
})

const authStore = useAuthStore()
const buyerApi = useBuyerApi()

const tab = ref('profile')
const dashboardData = ref({
  total_orders: 0,
  pending_orders: 0,
  completed_orders: 0,
  total_reviews: 0
})
const orders = ref<BuyerOrder[]>([])
const reviews = ref<BuyerReview[]>([])
const loading = ref(false)
const loadingOrders = ref(false)
const loadingReviews = ref(false)
const saving = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const profileData = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address: ''
})

const orderHeaders = [
  { title: 'شماره سفارش', key: 'order_number' },
  { title: 'وضعیت', key: 'status' },
  { title: 'مبلغ کل', key: 'total_amount' },
  { title: 'پرداخت شده', key: 'is_paid' },
  { title: 'تاریخ', key: 'created_at' }
]

const paymentHeaders = [
  { title: 'شماره سفارش', key: 'order_number' },
  { title: 'مبلغ', key: 'total_amount' },
  { title: 'روش پرداخت', key: 'payment_method' },
  { title: 'تاریخ پرداخت', key: 'payment_date' }
]

const reviewHeaders = [
  { title: 'محصول', key: 'product' },
  { title: 'امتیاز', key: 'rating' },
  { title: 'نظر', key: 'comment' },
  { title: 'تاریخ', key: 'created_at' }
]

const paymentRecords = computed(() => {
  return orders.value.filter(order => order.is_paid)
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

const updateProfile = async () => {
  saving.value = true
  try {
    await authStore.updateProfile(profileData.value)
    showSnackbar('پروفایل با موفقیت به‌روزرسانی شد', 'success')
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
    shipped: 'cyan',
    delivered: 'success',
    cancelled: 'error',
    rejected: 'error'
  }
  return colors[status] || 'grey'
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

const formatPrice = (price: string | number) => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(numPrice)
}

const showSnackbar = (message: string, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

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
})
</script>

