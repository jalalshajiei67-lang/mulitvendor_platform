<template>
  <v-container fluid dir="rtl" class="seller-dashboard pt-6">
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
            <v-tab value="miniwebsite">
              <v-icon left>mdi-web</v-icon>
              وب‌سایت مینی
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
                          خوش آمدید {{ getUserFullName() }}!
                        </h2>
                        <p class="text-body-1 text-medium-emphasis">
                          خلاصه فعالیت‌ها و فروش‌های شما
                        </p>
                      </div>
                        <!-- Quick Actions -->
                        <div class="d-flex gap-2 flex-wrap">
                          <v-btn
                            color="primary"
                            variant="elevated"
                            prepend-icon="mdi-plus-circle"
                            @click="tab = 'products'; openProductForm()"
                            size="default"
                          >
                            افزودن محصول جدید
                          </v-btn>
                          <v-btn
                            color="secondary"
                            variant="outlined"
                            prepend-icon="mdi-package-variant"
                            @click="tab = 'products'"
                            size="default"
                          >
                            مدیریت محصولات
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
                                کل محصولات
                              </div>
                              <div class="text-h3 font-weight-bold">
                                {{ dashboardData.total_products || 0 }}
                              </div>
                              <div class="text-caption mt-1">
                                فعال: {{ dashboardData.active_products || 0 }}
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
                        class="stat-card stat-card-success"
                        elevation="2"
                        :loading="loading"
                      >
                        <v-card-text>
                          <div class="d-flex align-center justify-space-between">
                            <div>
                              <div class="text-caption text-medium-emphasis mb-1">
                                کل فروش
                              </div>
                              <div class="text-h3 font-weight-bold">
                                {{ formatPrice(dashboardData.total_sales || 0) }}
                              </div>
                              <div class="text-caption mt-1">
                                {{ dashboardData.total_orders || 0 }} سفارش
                              </div>
                            </div>
                            <v-avatar
                              size="56"
                              color="success"
                              class="stat-icon"
                            >
                              <v-icon size="28">mdi-currency-usd</v-icon>
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
                                بازدید محصولات
                              </div>
                              <div class="text-h3 font-weight-bold">
                                {{ dashboardData.product_views || 0 }}
                              </div>
                            </div>
                            <v-avatar
                              size="56"
                              color="info"
                              class="stat-icon"
                            >
                              <v-icon size="28">mdi-eye</v-icon>
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
                                کل نظرات
                              </div>
                              <div class="text-h3 font-weight-bold">
                                {{ dashboardData.total_reviews || 0 }}
                              </div>
                            </div>
                            <v-avatar
                              size="56"
                              color="warning"
                              class="stat-icon"
                            >
                              <v-icon size="28">mdi-star</v-icon>
                            </v-avatar>
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>

                  <v-row class="mb-4">
                    <v-col cols="12" md="4">
                      <EngagementWidget
                        :engagement="gamificationStore.engagement"
                        :loading="gamificationStore.loading"
                        @cta="openProductForm"
                      />
                    </v-col>
                    <v-col cols="12" md="4">
                      <BadgeDisplay
                        :badges="gamificationStore.badges.slice(0, 4)"
                        title="نشان‌های پیش رو"
                      />
                    </v-col>
                    <v-col cols="12" md="4">
                      <LeaderboardWidget :entries="gamificationStore.leaderboard" />
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
                              :subtitle="`خریدار: ${order.buyer_username || 'نامشخص'} - مبلغ: ${formatPrice(order.total_amount)} تومان`"
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
                </div>
              </v-window-item>
              
              <!-- Profile Tab -->
              <v-window-item value="profile">
                <div class="py-4">
                  <h3 class="text-h6 mb-4">اطلاعات شخصی</h3>
                  <v-row>
                    <v-col cols="12" lg="4">
                      <FormQualityScore
                        title="امتیاز پروفایل"
                        caption="این مراحل اعتماد خریدار را بالا می‌برد"
                        :score="profileScore"
                        :metrics="profileMetrics"
                        :tips="profileTips"
                      />
                    </v-col>
                    <v-col cols="12" lg="8">
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
                    </v-col>
                  </v-row>
                </div>
              </v-window-item>

              <!-- Products Tab -->
              <v-window-item value="products">
                <div class="py-4">
                  <!-- Show Product Form when adding/editing -->
                  <div v-if="showProductForm">
                    <div class="d-flex align-center mb-4">
                      <v-btn
                        icon
                        size="small"
                        @click="closeProductForm"
                        class="ml-2"
                      >
                        <v-icon>mdi-arrow-right</v-icon>
                      </v-btn>
                      <h3 class="text-h6">
                        {{ editingProduct ? 'ویرایش محصول' : 'افزودن محصول جدید' }}
                      </h3>
                    </div>
                    <SupplierProductForm
                      :product-data="editingProduct"
                      :edit-mode="!!editingProduct"
                      @saved="onProductSaved"
                      @cancel="closeProductForm"
                    />
                  </div>
                  
                  <!-- Show Product List by default -->
                  <SupplierProductList
                    v-else
                    ref="productListRef"
                    @add-product="openProductForm"
                    @edit-product="openEditProductForm"
                  />
                </div>
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
                <div class="py-4">
                  <h3 class="text-h6 mb-4">سفارشات من</h3>
                  <v-data-table
                    :headers="orderHeaders"
                    :items="orders"
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
                    <template v-slot:item.created_at="{ item }">
                      {{ formatDate(item.created_at) }}
                    </template>
                    <template v-slot:no-data>
                      <div class="text-center py-8">
                        <v-icon size="64" color="grey-lighten-1">mdi-cart</v-icon>
                        <p class="text-body-1 mt-4 text-grey">سفارشی یافت نشد</p>
                      </div>
                    </template>
                  </v-data-table>
                </div>
              </v-window-item>

              <!-- Reviews Tab -->
              <v-window-item value="reviews">
                <div class="py-4">
                  <h3 class="text-h6 mb-4">نظرات مشتریان</h3>
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
                    <template v-slot:item.buyer="{ item }">
                      {{ item.author?.username || 'نامشخص' }}
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
                        <v-icon size="64" color="grey-lighten-1">mdi-star</v-icon>
                        <p class="text-body-1 mt-4 text-grey">نظری ثبت نشده است</p>
                      </div>
                    </template>
                  </v-data-table>
                </div>
              </v-window-item>

              <!-- Mini Website Tab -->
              <v-window-item value="miniwebsite">
                <div class="py-4">
                  <v-tabs
                    v-model="miniWebsiteTab"
                    bg-color="grey-lighten-4"
                    color="primary"
                    align-tabs="start"
                    class="mb-4"
                  >
                    <v-tab value="settings">
                      <v-icon start size="small">mdi-palette</v-icon>
                      تنظیمات
                    </v-tab>
                    <v-tab value="portfolio">
                      <v-icon start size="small">mdi-briefcase</v-icon>
                      نمونه کارها
                    </v-tab>
                    <v-tab value="team">
                      <v-icon start size="small">mdi-account-group</v-icon>
                      تیم
                    </v-tab>
                    <v-tab value="messages">
                      <v-icon start size="small">mdi-email</v-icon>
                      پیام‌ها
                    </v-tab>
                  </v-tabs>

                  <v-window v-model="miniWebsiteTab">
                    <!-- Settings Sub-Tab -->
                    <v-window-item value="settings">
                      <MiniWebsiteSettings />
                    </v-window-item>

                    <!-- Portfolio Sub-Tab -->
                    <v-window-item value="portfolio">
                      <PortfolioManager />
                    </v-window-item>

                    <!-- Team Sub-Tab -->
                    <v-window-item value="team">
                      <TeamManager />
                    </v-window-item>

                    <!-- Messages Sub-Tab -->
                    <v-window-item value="messages">
                      <ContactMessagesInbox />
                    </v-window-item>
                  </v-window>
                </div>
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
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSellerApi } from '~/composables/useSellerApi'
import type { SellerOrder, SellerReview, SellerAd } from '~/composables/useSellerApi'
import MiniWebsiteSettings from '~/components/supplier/MiniWebsiteSettings.vue'
import PortfolioManager from '~/components/supplier/PortfolioManager.vue'
import TeamManager from '~/components/supplier/TeamManager.vue'
import ContactMessagesInbox from '~/components/supplier/ContactMessagesInbox.vue'
import SupplierProductForm from '~/components/supplier/ProductForm.vue'
import EngagementWidget from '~/components/gamification/EngagementWidget.vue'
import BadgeDisplay from '~/components/gamification/BadgeDisplay.vue'
import LeaderboardWidget from '~/components/gamification/LeaderboardWidget.vue'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'
import { useGamificationStore } from '~/stores/gamification'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const authStore = useAuthStore()
const sellerApi = useSellerApi()
const gamificationStore = useGamificationStore()
const route = useRoute()

// Check for tab query parameter - default to 'home'
const tabQuery = computed(() => route.query.tab as string || 'home')
const tab = ref(tabQuery.value)
const miniWebsiteTab = ref('settings')

// Watch for route query changes
watch(() => route.query.tab, (newTab) => {
  if (newTab && typeof newTab === 'string') {
    tab.value = newTab
  }
})
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
const showProductForm = ref(false)
const editingProduct = ref<any>(null)
const productListRef = ref<any>(null)

const profileData = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: ''
})

const vendorProfile = computed(() => authStore.user?.vendor_profile || authStore.vendorProfile || null)

const profileMetrics = computed(() => [
  {
    key: 'name',
    label: 'نام و نام خانوادگی',
    tip: 'نام کامل خود را بنویسید تا روی فاکتورها و کارت ویزیت نمایش داده شود.',
    weight: 0.2,
    passed: Boolean(profileData.value.first_name && profileData.value.last_name)
  },
  {
    key: 'contact',
    label: 'اطلاعات تماس',
    tip: 'ایمیل و شماره تماس فعال وارد کنید.',
    weight: 0.3,
    passed: Boolean(profileData.value.email && profileData.value.phone)
  },
  {
    key: 'address',
    label: 'آدرس و موقعیت',
    tip: 'آدرس کارگاه یا شهر فعالیت را وارد کنید.',
    weight: 0.15,
    passed: Boolean(vendorProfile.value?.address)
  },
  {
    key: 'logo',
    label: 'لوگو',
    tip: 'لوگوی شرکت را در پروفایل بارگذاری کنید.',
    weight: 0.15,
    passed: Boolean(vendorProfile.value?.logo)
  },
  {
    key: 'bio',
    label: 'شرح فروشگاه',
    tip: 'چند جمله درباره تجربه و تخصص خود بنویسید.',
    weight: 0.2,
    passed: Boolean(vendorProfile.value?.description && vendorProfile.value?.description.length > 80)
  }
])

const profileScore = computed(() => {
  const metrics = profileMetrics.value
  const totalWeight = metrics.reduce((sum, metric) => sum + metric.weight, 0) || 1
  const earned = metrics.reduce((sum, metric) => sum + (metric.passed ? metric.weight : 0), 0)
  return Math.round((earned / totalWeight) * 100)
})

const profileTips = computed(() => profileMetrics.value.filter(metric => !metric.passed).map(metric => metric.tip))

watch(profileScore, (score) => {
  gamificationStore.updateLocalScore('profile', {
    title: 'profile',
    score,
    metrics: profileMetrics.value,
    tips: profileTips.value
  })
}, { immediate: true })

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
    // Redirect to home tab after successful update
    setTimeout(() => {
      tab.value = 'home'
      navigateTo('/seller/dashboard?tab=home', { replace: true })
    }, 1000)
  } catch (error) {
    console.error('Failed to update profile:', error)
    showSnackbar('خطا در به‌روزرسانی پروفایل', 'error')
  } finally {
    saving.value = false
  }
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

// Computed for recent orders
const recentOrders = computed(() => {
  return orders.value.slice(0, 5)
})

// Watch tab changes to load data
watch(tab, (newTab) => {
  // Update URL query when tab changes
  navigateTo(`/seller/dashboard?tab=${newTab}`, { replace: true })
})

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
    shipped: 'pink',
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

const getUserFullName = () => {
  const user = authStore.user
  if (!user) return 'کاربر'
  
  // Try to get first name and last name
  const firstName = user.first_name || ''
  const lastName = user.last_name || ''
  
  // If both exist, return full name
  if (firstName && lastName) {
    return `${firstName} ${lastName}`
  }
  
  // If only one exists, return it
  if (firstName) return firstName
  if (lastName) return lastName
  
  // Fallback to username
  return user.username || 'کاربر'
}

const showSnackbar = (message: string, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

const openProductForm = () => {
  editingProduct.value = null
  showProductForm.value = true
  tab.value = 'products'
}

const openEditProductForm = (product: any) => {
  editingProduct.value = product
  showProductForm.value = true
}

const closeProductForm = () => {
  showProductForm.value = false
  editingProduct.value = null
}

const onProductSaved = async (product: any) => {
  showSnackbar(`محصول "${product.name}" با موفقیت ذخیره شد`, 'success')
  closeProductForm()
  
  // Refresh product list
  if (productListRef.value) {
    await productListRef.value.loadProducts()
  }
  
  // Refresh dashboard data to update stats
  await loadDashboardData()
}

onMounted(() => {
  if (authStore.user) {
    profileData.value = {
      first_name: authStore.user.first_name || '',
      last_name: authStore.user.last_name || '',
      email: authStore.user.email || '',
      phone: authStore.user.profile?.phone || ''
    }
  }
  loadDashboardData()
  loadOrders()
  loadReviews()
  loadAds()
  gamificationStore.hydrate().catch((error) => console.warn('Failed to load gamification data', error))
})
</script>

<style scoped>
.seller-dashboard {
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
.stat-card-info :deep(.text-h3) {
  color: white !important;
}
</style>

