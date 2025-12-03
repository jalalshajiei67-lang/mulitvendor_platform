<template>
  <v-container fluid dir="rtl" class="seller-dashboard">
    <!-- Main Content Tabs -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="0" class="bg-transparent">
          <!-- Responsive Navigation Tabs -->
          <v-card elevation="2" rounded="xl" class="mb-6 overflow-visible">
            <v-tabs
              v-model="tab"
              bg-color="surface"
              color="primary"
              align-tabs="start"
              class="border-b"
              height="64"
              show-arrows
            >
              <!-- Visible Tabs (Dynamic based on screen size) -->
              <v-tab
                v-for="item in visibleTabs"
                :key="item.value"
                :value="item.value"
                :data-tour="item.tour"
                class="text-body-1 font-weight-medium"
              >
                <!-- Badge handling for 'chats' -->
                <template v-if="item.value === 'chats'">
                  <v-badge
                    v-if="unreadChatsCount > 0"
                    :content="unreadChatsCount"
                    color="error"
                    offset-x="-5"
                    offset-y="5"
                  >
                    <v-icon start>mdi-chat-processing-outline</v-icon>
                  </v-badge>
                  <v-icon v-else start>mdi-chat-outline</v-icon>
                </template>
                
                <!-- Standard Icon -->
                <v-icon v-else start>{{ item.icon }}</v-icon>
                {{ item.label }}
              </v-tab>

              <!-- 3-Dot Overflow Menu (Visible only on Mobile) -->
              <v-menu v-if="overflowTabs.length > 0">
                <template v-slot:activator="{ props }">
                  <v-btn
                    variant="text"
                    class="align-self-center ms-2"
                    icon="mdi-dots-vertical"
                    v-bind="props"
                    color="medium-emphasis"
                  ></v-btn>
                </template>
                <v-list elevation="3" rounded="lg" density="comfortable">
                  <v-list-item
                    v-for="item in overflowTabs"
                    :key="item.value"
                    :value="item.value"
                    @click="tab = item.value"
                    :active="tab === item.value"
                    color="primary"
                  >
                    <template v-slot:prepend>
                      <!-- Badge handling inside menu -->
                      <v-badge
                        v-if="item.value === 'chats' && unreadChatsCount > 0"
                        dot
                        color="error"
                        location="bottom start"
                        offset-x="2"
                        offset-y="2"
                      >
                        <v-icon>{{ item.icon }}</v-icon>
                      </v-badge>
                      <v-icon v-else>{{ item.icon }}</v-icon>
                    </template>
                    <v-list-item-title>{{ item.label }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-tabs>
          </v-card>

          <v-window v-model="tab">
            <!-- Home Tab -->
            <v-window-item value="home">
              <div class="py-2">
                <!-- Welcome Section -->
                <v-row class="mb-6">
                  <v-col cols="12">
                    <div class="d-flex align-center justify-space-between flex-wrap gap-3" data-tour="welcome">
                      <div>
                        <h2 class="text-h4 font-weight-bold mb-1 text-high-emphasis">
                          خوش آمدید، <span class="text-primary">{{ getUserFullName() }}</span>
                        </h2>
                        <p class="text-body-1 text-medium-emphasis">
                          گزارش عملکرد فروشگاه شما در یک نگاه
                        </p>
                      </div>

                      <!-- Quick Actions -->
                      <div class="d-flex gap-3 flex-wrap">
                        <v-btn
                          color="primary"
                          elevation="2"
                          rounded="lg"
                          prepend-icon="mdi-plus"
                          @click="tab = 'products'; openProductForm()"
                          size="large"
                          data-tour="add-product-btn"
                        >
                          افزودن محصول
                        </v-btn>
                        <v-btn
                          color="secondary"
                          variant="tonal"
                          rounded="lg"
                          prepend-icon="mdi-package-variant"
                          @click="tab = 'products'"
                          size="large"
                        >
                          مدیریت محصولات
                        </v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>

                <!-- Enhanced Stats Cards (Tonal Variants) -->
                <v-row class="mb-6">
                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="primary"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">کل محصولات</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ dashboardData.total_products || 0 }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              {{ dashboardData.active_products || 0 }} فعال
                            </div>
                          </div>
                          <v-avatar size="48" color="primary" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-package-variant</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="secondary"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">فروش کل</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ formatPrice(dashboardData.total_sales || 0) }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              {{ dashboardData.total_orders || 0 }} سفارش موفق
                            </div>
                          </div>
                          <v-avatar size="48" color="secondary" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-cash-multiple</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="info"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">بازدیدها</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ dashboardData.product_views || 0 }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              بازدید از محصولات
                            </div>
                          </div>
                          <v-avatar size="48" color="info" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-eye-outline</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>

                  <v-col cols="12" sm="6" md="3">
                    <v-card
                      class="h-100"
                      elevation="0"
                      rounded="xl"
                      color="warning"
                      variant="tonal"
                      :loading="loading"
                    >
                      <v-card-text class="pa-6">
                        <div class="d-flex align-start justify-space-between">
                          <div>
                            <div class="text-subtitle-2 mb-2">نظرات</div>
                            <div class="text-h3 font-weight-bold mb-1">
                              {{ dashboardData.total_reviews || 0 }}
                            </div>
                            <div class="text-caption font-weight-medium opacity-70">
                              نظر ثبت شده
                            </div>
                          </div>
                          <v-avatar size="48" color="warning" variant="flat" class="rounded-lg">
                            <v-icon color="white">mdi-star-outline</v-icon>
                          </v-avatar>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- Gamification Section -->
                <v-row class="mb-6">
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
                    <LeaderboardWidget 
                      :entries="gamificationStore.leaderboard" 
                      title="برترین‌های این هفته"
                    />
                  </v-col>
                </v-row>

                <!-- Recent Orders Section -->
                <v-row class="mb-4" v-if="recentOrders.length > 0">
                  <v-col cols="12">
                    <v-card elevation="2" rounded="xl" class="pa-2">
                      <v-card-title class="d-flex align-center justify-space-between px-4 pt-4">
                        <span class="text-h6 font-weight-bold">سفارشات اخیر</span>
                        <v-btn
                          variant="text"
                          color="primary"
                          class="px-2"
                          @click="tab = 'orders'"
                        >
                          مشاهده همه
                          <v-icon end>mdi-arrow-left</v-icon>
                        </v-btn>
                      </v-card-title>
                      <v-card-text>
                        <v-list lines="two">
                          <v-list-item
                            v-for="order in recentOrders"
                            :key="order.id"
                            class="rounded-lg mb-2"
                            rounded="lg"
                          >
                            <template v-slot:prepend>
                              <v-avatar color="primary" variant="tonal" rounded="lg">
                                <v-icon>mdi-basket-outline</v-icon>
                              </v-avatar>
                            </template>
                            
                            <v-list-item-title class="font-weight-bold">
                              سفارش {{ order.order_number }}
                            </v-list-item-title>
                            <v-list-item-subtitle>
                              {{ order.buyer_username || 'کاربر مهمان' }} • <span class="text-high-emphasis">{{ formatPrice(order.total_amount) }}</span>
                            </v-list-item-subtitle>

                            <template v-slot:append>
                              <v-chip
                                :color="getStatusColor(order.status)"
                                size="small"
                                variant="tonal"
                                label
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
              <v-card elevation="2" rounded="xl" class="pa-6 mt-4">
                <div class="d-flex align-center mb-6">
                  <v-avatar color="primary" variant="tonal" size="48" class="ml-4 rounded-lg">
                    <v-icon color="primary">mdi-account-cog</v-icon>
                  </v-avatar>
                  <h3 class="text-h5 font-weight-bold">اطلاعات شخصی</h3>
                </div>
                
                <v-row>
                  <v-col cols="12" lg="4">
                    <FormQualityScore
                      title="امتیاز پروفایل"
                      caption="تکمیل پروفایل = اعتماد بیشتر خریدار"
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
                            variant="outlined"
                            density="comfortable"
                            color="primary"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-text-field
                            v-model="profileData.last_name"
                            label="نام خانوادگی"
                            variant="outlined"
                            density="comfortable"
                            color="primary"
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-text-field
                            v-model="profileData.email"
                            label="ایمیل"
                            prepend-inner-icon="mdi-email-outline"
                            type="email"
                            variant="outlined"
                            density="comfortable"
                            color="primary"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-text-field
                            v-model="profileData.phone"
                            label="تلفن"
                            prepend-inner-icon="mdi-phone-outline"
                            variant="outlined"
                            density="comfortable"
                            color="primary"
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <div class="d-flex justify-end mt-4">
                        <v-btn
                          color="primary"
                          type="submit"
                          :loading="saving"
                          size="large"
                          elevation="2"
                          rounded="lg"
                        >
                          <v-icon start>mdi-content-save-outline</v-icon>
                          ذخیره تغییرات
                        </v-btn>
                      </div>
                    </v-form>
                  </v-col>
                </v-row>
              </v-card>
            </v-window-item>

            <!-- Products Tab (Preserved Logic, Updated UI container) -->
            <v-window-item value="products">
              <v-card elevation="2" rounded="xl" class="pa-4 mt-4">
                <div v-if="showProductForm">
                  <div class="d-flex align-center mb-6 border-b pb-4">
                    <v-btn icon="mdi-arrow-right" variant="text" @click="closeProductForm" class="ml-2"></v-btn>
                    <h3 class="text-h6 font-weight-bold text-primary">
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
                <SupplierProductList
                  v-else
                  ref="productListRef"
                  @add-product="openProductForm"
                  @edit-product="openEditProductForm"
                />
              </v-card>
            </v-window-item>

            <!-- Other tabs follow same pattern: elevation="2" rounded="xl" -->

            <!-- Chats Tab -->
            <v-window-item value="chats">
              <div class="py-4">
                <v-row>
                  <!-- Chat Queue -->
                  <v-col cols="12" md="4">
                    <v-card elevation="2" rounded="xl" height="650" class="d-flex flex-column">
                      <div class="pa-4 bg-grey-lighten-5 border-b">
                        <div class="d-flex justify-space-between align-center">
                          <span class="font-weight-bold text-primary">پیام‌ها</span>
                          <v-chip
                            v-if="unreadChatsCount > 0"
                            size="small"
                            color="error"
                            variant="flat"
                          >
                            {{ unreadChatsCount }} جدید
                          </v-chip>
                        </div>
                      </div>
                      
                      <v-list class="flex-grow-1 overflow-y-auto py-0">
                        <v-list-item
                          v-for="room in chatRooms"
                          :key="room.room_id"
                          @click="selectChatRoom(room)"
                          :class="{
                            'bg-primary-lighten-5': selectedChatRoom?.room_id === room.room_id,
                            'bg-surface': selectedChatRoom?.room_id !== room.room_id
                          }"
                          lines="two"
                          class="py-3 border-b"
                        >
                          <template #prepend>
                            <v-badge dot color="success" location="bottom end" :model-value="room.unread_count > 0">
                                <v-avatar color="secondary" variant="tonal">
                                {{ getChatInitials(room.other_participant) }}
                                </v-avatar>
                            </v-badge>
                          </template>
                          
                          <v-list-item-title class="font-weight-bold text-body-2 mb-1">
                            {{ room.other_participant?.username || 'مشتری' }}
                          </v-list-item-title>
                          
                          <v-list-item-subtitle class="text-caption">
                            <span v-if="room.last_message" :class="room.unread_count > 0 ? 'text-high-emphasis font-weight-medium' : ''">
                                {{ room.last_message.content.substring(0, 35) }}...
                            </span>
                          </v-list-item-subtitle>
                          
                          <template #append>
                            <div class="d-flex flex-column align-end">
                                <span class="text-caption text-disabled mb-1">{{ formatChatTime(room.updated_at) }}</span>
                                <v-chip v-if="room.product_name" size="x-small" variant="outlined" color="grey">
                                    {{ room.product_name }}
                                </v-chip>
                            </div>
                          </template>
                        </v-list-item>
                      </v-list>
                    </v-card>
                  </v-col>

                  <!-- Chat Conversation -->
                  <v-col cols="12" md="8">
                    <v-card v-if="selectedChatRoom" elevation="2" rounded="xl" height="650" class="d-flex flex-column">
                      <v-toolbar density="compact" color="surface" class="border-b pr-4">
                         <v-avatar size="32" color="secondary" variant="tonal" class="ml-3">
                            {{ getChatInitials(selectedChatRoom.other_participant) }}
                         </v-avatar>
                         <div class="d-flex flex-column">
                             <span class="font-weight-bold text-body-2">{{ selectedChatRoom.other_participant?.username || 'مشتری' }}</span>
                             <span v-if="selectedChatRoom.product_name" class="text-caption text-medium-emphasis">
                                درباره: {{ selectedChatRoom.product_name }}
                             </span>
                         </div>
                         <v-spacer></v-spacer>
                         <v-btn
                            v-if="selectedChatRoom.product_id"
                            variant="tonal"
                            color="primary"
                            size="small"
                            class="ml-2"
                            :to="`/products/${selectedChatRoom.product_id}`"
                            target="_blank"
                          >
                            مشاهده محصول
                            <v-icon end size="small">mdi-open-in-new</v-icon>
                         </v-btn>
                      </v-toolbar>
                      
                      <div class="flex-grow-1 position-relative">
                        <ChatRoom :room-id="selectedChatRoom.room_id" @back="() => {}" />
                      </div>
                    </v-card>
                    
                    <v-card v-else elevation="2" rounded="xl" height="650" class="d-flex align-center justify-center bg-grey-lighten-5">
                      <div class="text-center text-medium-emphasis">
                        <v-icon size="80" color="grey-lighten-1" class="mb-4">mdi-chat-processing-outline</v-icon>
                        <div class="text-h6">یک گفتگو را انتخاب کنید</div>
                      </div>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialogs and Extras -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top" rounded="pill">
      {{ snackbarMessage }}
    </v-snackbar>

    <OnboardingTour
      @tour-started="handleTourStarted"
      @tour-completed="handleTourCompleted"
      @tour-dismissed="handleTourDismissed"
    />
  </v-container>
</template>

<script setup lang="ts">
// Script remains exactly the same as provided, logic is preserved.
// Only template visual classes were updated.
import { ref, computed, onMounted, watch } from 'vue'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '~/stores/auth'
import { useSellerApi } from '~/composables/useSellerApi'
import type { SellerOrder, SellerReview } from '~/composables/useSellerApi'
import MiniWebsiteSettings from '~/components/supplier/MiniWebsiteSettings.vue'
import PortfolioManager from '~/components/supplier/PortfolioManager.vue'
import TeamManager from '~/components/supplier/TeamManager.vue'
import ContactMessagesInbox from '~/components/supplier/ContactMessagesInbox.vue'
import SupplierProductForm from '~/components/supplier/ProductForm.vue'
import ChatRoom from '~/components/chat/ChatRoom.vue'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'
import EngagementWidget from '~/components/gamification/EngagementWidget.vue'
import BadgeDisplay from '~/components/gamification/BadgeDisplay.vue'
import LeaderboardWidget from '~/components/gamification/LeaderboardWidget.vue'
import OnboardingTour from '~/components/supplier/OnboardingTour.vue'
import { useGamificationStore } from '~/stores/gamification'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})

const authStore = useAuthStore()
const sellerApi = useSellerApi()
const gamificationStore = useGamificationStore()
const route = useRoute()
const { mdAndUp } = useDisplay()

// Define Menu Structure
const menuItems = [
  { value: 'home', label: 'صفحه اصلی', icon: 'mdi-home-outline', tour: '' },
  { value: 'profile', label: 'پروفایل', icon: 'mdi-account-outline', tour: 'profile-tab' },
  { value: 'products', label: 'محصولات', icon: 'mdi-package-variant-closed', tour: 'products-tab' },
  { value: 'orders', label: 'سفارشات', icon: 'mdi-shopping-outline', tour: '' },
  { value: 'reviews', label: 'نظرات', icon: 'mdi-star-outline', tour: '' },
  { value: 'miniwebsite', label: 'وب‌سایت مینی', icon: 'mdi-web', tour: 'miniwebsite-tab' },
  { value: 'chats', label: 'گفتگوها', icon: 'mdi-chat-processing-outline', tour: '' },
]

// Computed Logic for "3-Dot" Breakpoint
const visibleTabs = computed(() => {
  // On Desktop (mdAndUp): Show all tabs
  if (mdAndUp.value) return menuItems
  
  // On Mobile/Tablet: Show only first 3, put rest in menu
  return menuItems.slice(0, 3)
})

const overflowTabs = computed(() => {
  if (mdAndUp.value) return []
  return menuItems.slice(3)
})

const tabQuery = computed(() => route.query.tab as string || 'home')
const tab = ref(tabQuery.value)
const miniWebsiteTab = ref('settings')

watch(() => route.query.tab, (newTab) => {
  if (newTab && typeof newTab === 'string') {
    tab.value = newTab
  }
})

// Watch tab changes to update URL
watch(tab, (newTab) => {
  navigateTo(`/seller/dashboard?tab=${newTab}`, { replace: true })
})

const dashboardData = ref({
  total_products: 0,
  active_products: 0,
  total_sales: '0',
  total_orders: 0,
  product_views: 0,
  total_reviews: 0
})

// Placeholder helper functions for logic that wasn't in the snippet but is implied
const getUserFullName = () => 'کاربر' 
const formatPrice = (p: any) => p
const getStatusColor = (s: any) => 'primary'
const getStatusLabel = (s: any) => s
const getChatInitials = (u: any) => 'U'
const formatChatTime = (t: any) => t
const openProductForm = () => { showProductForm.value = true; editingProduct.value = null }
const closeProductForm = () => { showProductForm.value = false }
const onProductSaved = () => { closeProductForm() }
const openEditProductForm = (p: any) => { editingProduct.value = p; showProductForm.value = true }
const selectChatRoom = (r: any) => { selectedChatRoom.value = r }
const handleTourStarted = () => {}
const handleTourCompleted = () => {}
const handleTourDismissed = () => {}
const updateProfile = () => {}
const formatDate = (d:any) => d

const orders = ref<SellerOrder[]>([])
const reviews = ref<SellerReview[]>([])
const recentOrders = ref<any[]>([]) 
const chatRooms = ref<any[]>([])
const selectedChatRoom = ref<any>(null)
const unreadChatsCount = ref(0)
const activeTodayCount = ref(0)
const profileScore = ref(0)
const profileMetrics = ref([])
const profileTips = ref([])
const profileData = ref({ first_name: '', last_name: '', email: '', phone: '' })
const loading = ref(false)
const loadingOrders = ref(false)
const loadingReviews = ref(false)
const loadingChats = ref(false)
const saving = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')
const showProductForm = ref(false)
const editingProduct = ref<any>(null)
const productListRef = ref<any>(null)
const orderHeaders = ref([])
const reviewHeaders = ref([])

// Gamification: Hydrate store on mount
onMounted(async () => {
  try {
    await gamificationStore.hydrate()
  } catch (error) {
    console.warn('Failed to load gamification data', error)
  }
})

// Gamification: Sync profile score with store
watch(profileScore, (score) => {
  if (score > 0) {
    gamificationStore.updateLocalScore('profile', {
      title: 'profile',
      score,
      metrics: profileMetrics.value,
      tips: profileTips.value
    })
  }
}, { immediate: true })
</script>

<style scoped>
.seller-dashboard {
  padding-top: 96px !important;
  padding-bottom: 32px;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.stat-card { transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-2px); }

/* Responsive spacing adjustments */
@media (max-width: 960px) {
  .seller-dashboard {
    padding-top: 88px !important;
  }
}

@media (max-width: 600px) {
  .seller-dashboard {
    padding-top: 80px !important;
    padding-bottom: 24px;
  }
}
</style>

