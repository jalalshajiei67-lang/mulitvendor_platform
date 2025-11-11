<template>
  <v-container fluid dir="rtl">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">
          <v-icon left>mdi-store</v-icon>
          داشبورد فروشنده
        </h1>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="text-h6">کل محصولات</div>
            <div class="text-h3">{{ dashboardData.total_products || 0 }}</div>
            <div class="text-caption">فعال: {{ dashboardData.active_products || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark>
          <v-card-text>
            <div class="text-h6">کل فروش</div>
            <div class="text-h3">{{ formatPrice(dashboardData.total_sales || 0) }} تومان</div>
            <div class="text-caption">{{ dashboardData.total_orders || 0 }} سفارش</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark>
          <v-card-text>
            <div class="text-h6">بازدید محصولات</div>
            <div class="text-h3">{{ dashboardData.product_views || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark>
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
            <v-tab value="products">
              <v-icon left>mdi-package-variant</v-icon>
              محصولات
            </v-tab>
            <v-tab value="ads">
              <v-icon left>mdi-bullhorn</v-icon>
              آگهی‌ها
            </v-tab>
            <v-tab value="orders">
              <v-icon left>mdi-cart</v-icon>
              سفارشات
            </v-tab>
            <v-tab value="reviews">
              <v-icon left>mdi-star</v-icon>
              نظرات مشتریان
            </v-tab>
            <v-tab value="analytics">
              <v-icon left>mdi-chart-line</v-icon>
              آمار و تحلیل
            </v-tab>
          </v-tabs>

          <v-card-text>
            <v-window v-model="tab">
              <!-- Profile Tab -->
              <v-window-item value="profile">
                <v-form ref="profileForm" @submit.prevent="updateProfile">
                  <h3 class="text-h6 mb-3">اطلاعات شخصی</h3>
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
                  
                  <v-divider class="my-4"></v-divider>
                  <h3 class="text-h6 mb-3">اطلاعات فروشگاه</h3>
                  <v-text-field
                    v-model="profileData.store_name"
                    label="نام فروشگاه"
                    prepend-icon="mdi-store"
                  ></v-text-field>
                  <v-textarea
                    v-model="profileData.description"
                    label="توضیحات فروشگاه"
                    prepend-icon="mdi-text"
                    rows="3"
                  ></v-textarea>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.contact_email"
                        label="ایمیل تماس"
                        prepend-icon="mdi-email-outline"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="profileData.contact_phone"
                        label="تلفن تماس"
                        prepend-icon="mdi-phone-outline"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-text-field
                    v-model="profileData.website"
                    label="وب‌سایت"
                    prepend-icon="mdi-web"
                  ></v-text-field>
                  <v-btn color="primary" type="submit" :loading="saving">
                    به‌روزرسانی پروفایل
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- Products Tab -->
              <v-window-item value="products">
                <v-btn color="primary" class="mb-4" @click="navigateTo('/admin/dashboard/products/new')">
                  <v-icon left>mdi-plus</v-icon>
                  افزودن محصول جدید
                </v-btn>
                <v-btn color="secondary" class="mb-4 mr-2" @click="navigateTo('/products')">
                  <v-icon left>mdi-eye</v-icon>
                  مشاهده همه محصولات
                </v-btn>
              </v-window-item>

              <!-- Ads Tab -->
              <v-window-item value="ads">
                <v-btn color="primary" class="mb-4" @click="showAdDialog = true">
                  <v-icon left>mdi-plus</v-icon>
                  ایجاد آگهی جدید
                </v-btn>
                <v-data-table
                  :headers="adHeaders"
                  :items="ads"
                  :loading="loadingAds"
                  item-value="id"
                >
                  <template v-slot:item.title="{ item }">
                    <strong>{{ item.title }}</strong>
                  </template>
                  <template v-slot:item.is_active="{ item }">
                    <v-chip :color="item.is_active ? 'success' : 'grey'" small>
                      {{ item.is_active ? 'فعال' : 'غیرفعال' }}
                    </v-chip>
                  </template>
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-btn icon size="small" @click="editAd(item)">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon size="small" color="error" @click="deleteAd(item.id)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
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
                  <template v-slot:item.created_at="{ item }">
                    {{ formatDate(item.created_at) }}
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
                  <template v-slot:item.buyer="{ item }">
                    {{ item.author?.username || 'نامشخص' }}
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

              <!-- Analytics Tab -->
              <v-window-item value="analytics">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-card>
                      <v-card-title>عملکرد محصولات</v-card-title>
                      <v-card-text>
                        <div class="text-h4">{{ dashboardData.product_views || 0 }}</div>
                        <div class="text-caption">کل بازدید محصولات</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-card>
                      <v-card-title>آمار سفارشات</v-card-title>
                      <v-card-text>
                        <div>کل سفارشات: <strong>{{ dashboardData.total_orders || 0 }}</strong></div>
                        <div>کل درآمد: <strong>{{ formatPrice(dashboardData.total_sales || 0) }} تومان</strong></div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Ad Dialog -->
    <v-dialog v-model="showAdDialog" max-width="600px">
      <v-card>
        <v-card-title>{{ editingAd ? 'ویرایش آگهی' : 'ایجاد آگهی جدید' }}</v-card-title>
        <v-card-text>
          <v-form ref="adForm" @submit.prevent="saveAd">
            <v-text-field
              v-model="adData.title"
              label="عنوان *"
              required
            ></v-text-field>
            <v-textarea
              v-model="adData.description"
              label="توضیحات *"
              rows="4"
              required
            ></v-textarea>
            <v-textarea
              v-model="adData.contact_info"
              label="اطلاعات تماس *"
              rows="2"
              required
            ></v-textarea>
            <v-switch
              v-model="adData.is_active"
              label="فعال"
              color="primary"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeAdDialog">لغو</v-btn>
          <v-btn color="primary" @click="saveAd" :loading="savingAd">ذخیره</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSellerApi } from '~/composables/useSellerApi'
import type { SellerOrder, SellerReview, SellerAd } from '~/composables/useSellerApi'

definePageMeta({
  middleware: 'authenticated'
})

const authStore = useAuthStore()
const sellerApi = useSellerApi()

const tab = ref('profile')
const dashboardData = ref({
  total_products: 0,
  active_products: 0,
  total_sales: '0',
  total_orders: 0,
  product_views: 0,
  total_reviews: 0
})
const orders = ref<SellerOrder[]>([])
const reviews = ref<SellerReview[]>([])
const ads = ref<SellerAd[]>([])
const loading = ref(false)
const loadingOrders = ref(false)
const loadingReviews = ref(false)
const loadingAds = ref(false)
const saving = ref(false)
const savingAd = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')
const showAdDialog = ref(false)
const editingAd = ref(false)

const profileData = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  store_name: '',
  description: '',
  contact_email: '',
  contact_phone: '',
  website: ''
})

const adData = ref({
  id: 0,
  title: '',
  description: '',
  contact_info: '',
  is_active: true
})

const adHeaders = [
  { title: 'عنوان', key: 'title' },
  { title: 'وضعیت', key: 'is_active' },
  { title: 'تاریخ ایجاد', key: 'created_at' },
  { title: 'عملیات', key: 'actions', sortable: false }
]

const orderHeaders = [
  { title: 'شماره سفارش', key: 'order_number' },
  { title: 'خریدار', key: 'buyer_username' },
  { title: 'وضعیت', key: 'status' },
  { title: 'مبلغ کل', key: 'total_amount' },
  { title: 'تاریخ', key: 'created_at' }
]

const reviewHeaders = [
  { title: 'محصول', key: 'product' },
  { title: 'خریدار', key: 'buyer' },
  { title: 'امتیاز', key: 'rating' },
  { title: 'نظر', key: 'comment' },
  { title: 'تاریخ', key: 'created_at' }
]

const loadDashboardData = async () => {
  loading.value = true
  try {
    const response = await sellerApi.getSellerDashboard()
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
    const response = await sellerApi.getSellerOrders()
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
    const response = await sellerApi.getSellerReviews()
    reviews.value = response
  } catch (error) {
    console.error('Failed to load reviews:', error)
    showSnackbar('خطا در بارگذاری نظرات', 'error')
  } finally {
    loadingReviews.value = false
  }
}

const loadAds = async () => {
  loadingAds.value = true
  try {
    const response = await sellerApi.getSellerAds()
    ads.value = response
  } catch (error) {
    console.error('Failed to load ads:', error)
    showSnackbar('خطا در بارگذاری آگهی‌ها', 'error')
  } finally {
    loadingAds.value = false
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

const saveAd = async () => {
  savingAd.value = true
  try {
    if (editingAd.value) {
      await sellerApi.updateSellerAd(adData.value.id, adData.value)
      showSnackbar('آگهی با موفقیت به‌روزرسانی شد', 'success')
    } else {
      await sellerApi.createSellerAd(adData.value)
      showSnackbar('آگهی با موفقیت ایجاد شد', 'success')
    }
    await loadAds()
    closeAdDialog()
  } catch (error) {
    console.error('Failed to save ad:', error)
    showSnackbar('خطا در ذخیره آگهی', 'error')
  } finally {
    savingAd.value = false
  }
}

const editAd = (ad: SellerAd) => {
  editingAd.value = true
  adData.value = { ...ad }
  showAdDialog.value = true
}

const deleteAd = async (id: number) => {
  if (confirm('آیا مطمئن هستید که می‌خواهید این آگهی را حذف کنید؟')) {
    try {
      await sellerApi.deleteSellerAd(id)
      showSnackbar('آگهی با موفقیت حذف شد', 'success')
      await loadAds()
    } catch (error) {
      console.error('Failed to delete ad:', error)
      showSnackbar('خطا در حذف آگهی', 'error')
    }
  }
}

const closeAdDialog = () => {
  showAdDialog.value = false
  editingAd.value = false
  adData.value = {
    id: 0,
    title: '',
    description: '',
    contact_info: '',
    is_active: true
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
      store_name: authStore.user.vendor_profile?.store_name || '',
      description: authStore.user.vendor_profile?.description || '',
      contact_email: authStore.user.vendor_profile?.contact_email || '',
      contact_phone: authStore.user.vendor_profile?.contact_phone || '',
      website: authStore.user.vendor_profile?.website || ''
    }
  }
  loadDashboardData()
  loadOrders()
  loadReviews()
  loadAds()
})
</script>

