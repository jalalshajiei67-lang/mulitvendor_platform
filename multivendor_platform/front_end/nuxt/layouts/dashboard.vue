<template>
  <v-layout class="dashboard-layout d-flex flex-column" dir="rtl">
    <!-- Dashboard Header -->
    <v-app-bar
      density="comfortable"
      color="primary"
      elevation="2"
      class="dashboard-header"
    >
      <v-container class="d-flex align-center justify-space-between py-2" fluid>
        <!-- Logo and Dashboard Title -->
        <div class="d-flex align-center gap-4">
          <NuxtLink to="/" class="d-flex align-center text-decoration-none">
            <v-avatar size="40" class="bg-white">
              <span class="text-primary text-h6 font-weight-bold">ای</span>
            </v-avatar>
          </NuxtLink>
          <div>
            <div class="text-subtitle-1 font-weight-bold text-white">
              {{ dashboardTitle }}
            </div>
            <NuxtLink
              to="/"
              class="text-caption text-white text-decoration-none"
            >
              بازگشت به سایت اصلی
            </NuxtLink>
          </div>
        </div>

        <!-- Right Side Actions -->
        <div class="d-flex align-center gap-2">
          <v-btn
            v-if="isSeller"
            color="amber"
            variant="tonal"
            size="small"
            prepend-icon="mdi-crown"
            class="text-white"
            to="/seller/pricing"
          >
            پلن‌ها
          </v-btn>
          <template v-if="isAuthenticated">
            <!-- Notification Bell (Buyer Only) -->
            <template v-if="isBuyer">
              <v-menu
                v-model="showNotificationsMenu"
                location="bottom end"
                offset="10"
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    icon
                    v-bind="props"
                    variant="text"
                    size="small"
                    class="text-white"
                  >
                    <v-badge
                      :content="notificationCount"
                      :model-value="notificationCount > 0"
                      color="error"
                      overlap
                    >
                      <v-icon color="white">mdi-bell</v-icon>
                    </v-badge>
                  </v-btn>
                </template>

                <v-card min-width="300" max-width="400">
                  <v-card-title class="d-flex align-center justify-space-between">
                    <span>اعلان‌ها</span>
                    <v-btn
                      icon
                      size="small"
                      variant="text"
                      @click="showNotificationsMenu = false"
                    >
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-list>
                    <v-list-item
                      v-if="notifications.length === 0"
                      class="text-center py-4"
                    >
                      <v-list-item-title class="text-grey">
                        هیچ اعلانی وجود ندارد
                      </v-list-item-title>
                    </v-list-item>
                    <v-list-item
                      v-for="notification in notifications"
                      :key="notification.id"
                      @click="handleNotificationClick(notification)"
                      class="notification-item"
                    >
                      <template v-slot:prepend>
                        <v-icon :color="notification.color">
                          {{ notification.icon }}
                        </v-icon>
                      </template>
                      <v-list-item-title>{{ notification.title }}</v-list-item-title>
                      <v-list-item-subtitle>{{ notification.subtitle }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-menu>
            </template>

            <!-- User Menu -->
            <v-menu location="bottom end">
              <template v-slot:activator="{ props }">
                <v-btn
                  icon
                  v-bind="props"
                  variant="text"
                  size="small"
                  class="text-white"
                >
                  <div class="avatar-with-badge">
                    <v-avatar size="32" class="user-avatar">
                      <v-icon>mdi-account</v-icon>
                    </v-avatar>
                    <!-- Progress Ring -->
                    <svg
                      v-if="isSeller && gamificationStore.userTier"
                      class="progress-ring"
                      width="40"
                      height="40"
                    >
                      <circle
                        cx="20"
                        cy="20"
                        r="18"
                        fill="none"
                        stroke="rgba(255, 255, 255, 0.3)"
                        stroke-width="2"
                      />
                      <circle
                        cx="20"
                        cy="20"
                        r="18"
                        fill="none"
                        :stroke="getTierColor(gamificationStore.userTier)"
                        stroke-width="2"
                        :stroke-dasharray="circumference"
                        :stroke-dashoffset="progressOffset"
                        stroke-linecap="round"
                        transform="rotate(-90 20 20)"
                        class="progress-circle"
                      />
                    </svg>
                    <!-- Tier Badge -->
                    <v-avatar
                      v-if="isSeller && gamificationStore.userTier"
                      :color="getTierColor(gamificationStore.userTier)"
                      size="16"
                      class="tier-badge"
                    >
                      <v-icon size="10" color="white">{{ getTierIcon(gamificationStore.userTier) }}</v-icon>
                    </v-avatar>
                  </div>
                </v-btn>
              </template>
              <v-list>
                <v-list-item>
                  <v-list-item-title class="font-weight-bold">
                    {{ authStore.user?.first_name || authStore.user?.username }}
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ authStore.user?.email }}</v-list-item-subtitle>
                  <template v-if="isSeller && gamificationStore.userTier" v-slot:append>
                    <v-chip
                      :color="getTierColor(gamificationStore.userTier)"
                      size="small"
                      variant="flat"
                    >
                      {{ getTierDisplayName(gamificationStore.userTier) }}
                    </v-chip>
                  </template>
                </v-list-item>
                <v-list-item v-if="isSeller && gamificationStore.userRank" class="px-4 py-2">
                  <v-list-item-subtitle class="text-caption">
                    رتبه: {{ gamificationStore.userRank }} | امتیاز: {{ formatNumber(gamificationStore.engagement?.total_points || 0) }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-divider></v-divider>
                <v-list-item
                  :to="dashboardLink"
                  prepend-icon="mdi-view-dashboard"
                >
                  <v-list-item-title>داشبورد</v-list-item-title>
                </v-list-item>
                <v-list-item
                  :to="`${dashboardLink}?tab=profile`"
                  prepend-icon="mdi-account"
                >
                  <v-list-item-title>پروفایل</v-list-item-title>
                </v-list-item>
                <v-divider></v-divider>
                <v-list-item
                  to="/logout"
                  prepend-icon="mdi-logout"
                >
                  <v-list-item-title>خروج</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </div>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="dashboard-main">
      <slot />
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { ref, computed, watch, onUnmounted, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useGamificationStore } from '~/stores/gamification'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const gamificationStore = useGamificationStore()
const { isAuthenticated, isAdmin, isSeller, isBuyer } = storeToRefs(authStore)

const showNotificationsMenu = ref(false)
const notifications = ref<any[]>([])

const dashboardTitle = computed(() => {
  if (isAdmin.value) return 'پنل مدیریت'
  if (isSeller.value) return 'داشبورد فروشنده'
  return 'داشبورد خریدار'
})

const dashboardLink = computed(() => {
  if (isAdmin.value) return '/admin/dashboard'
  if (isSeller.value) return '/seller/dashboard'
  return '/buyer/dashboard'
})

// Notification logic for buyers
let notificationInterval: ReturnType<typeof setInterval> | null = null

const loadNotifications = async () => {
  if (!isBuyer.value) return
  
  try {
    const { useBuyerApi } = await import('~/composables/useBuyerApi')
    const buyerApi = useBuyerApi()
    const orders = await buyerApi.getBuyerOrders()
    
    const newNotifications: any[] = []
    
    // Add pending orders notifications
    const pendingOrders = orders.filter((order: any) => 
      !order.is_rfq && order.status === 'pending'
    )
    if (pendingOrders.length > 0) {
      newNotifications.push({
        id: 'pending_orders',
        type: 'orders',
        title: `${pendingOrders.length} سفارش در انتظار`,
        subtitle: 'سفارشات شما در حال بررسی است',
        icon: 'mdi-package-variant',
        color: 'warning',
        link: '/buyer/dashboard?tab=orders'
      })
    }
    
    // Add pending RFQs notifications
    const pendingRFQs = orders.filter((order: any) => 
      order.is_rfq && order.status === 'pending'
    )
    if (pendingRFQs.length > 0) {
      newNotifications.push({
        id: 'pending_rfqs',
        type: 'rfqs',
        title: `${pendingRFQs.length} درخواست قیمت در انتظار`,
        subtitle: 'درخواست‌های قیمت شما در حال بررسی است',
        icon: 'mdi-file-document-edit',
        color: 'info',
        link: '/buyer/dashboard?tab=rfqs'
      })
    }
    
    notifications.value = newNotifications
  } catch (error) {
    console.error('Failed to load notifications:', error)
  }
}

const notificationCount = computed(() => notifications.value.length)

const handleNotificationClick = (notification: any) => {
  showNotificationsMenu.value = false
  if (notification.link) {
    navigateTo(notification.link)
  }
}

// Load notifications when authenticated buyer
watch([isAuthenticated, isBuyer], ([auth, buyer]) => {
  if (notificationInterval) {
    clearInterval(notificationInterval)
    notificationInterval = null
  }
  
  if (auth && buyer) {
    loadNotifications()
    // Refresh notifications every 30 seconds
    notificationInterval = setInterval(() => {
      if (isAuthenticated.value && isBuyer.value) {
        loadNotifications()
      }
    }, 30000)
  }
}, { immediate: true })

// Cleanup on unmount
onUnmounted(() => {
  if (notificationInterval) {
    clearInterval(notificationInterval)
  }
})

// Load gamification data for sellers
onMounted(async () => {
  if (isSeller.value) {
    try {
      await gamificationStore.hydrate()
    } catch (error) {
      console.warn('Failed to load gamification data', error)
    }
  }
})

// Tier helper functions
const getTierColor = (tier: string | null) => {
  if (!tier) return 'grey'
  const colorMap: Record<string, string> = {
    diamond: 'purple',
    gold: 'amber',
    silver: 'grey',
    bronze: 'brown',
    inactive: 'red',
  }
  return colorMap[tier] || 'grey'
}

const getTierIcon = (tier: string | null) => {
  if (!tier) return 'mdi-account'
  const iconMap: Record<string, string> = {
    diamond: 'mdi-diamond-stone',
    gold: 'mdi-trophy',
    silver: 'mdi-medal',
    bronze: 'mdi-award',
    inactive: 'mdi-account-off',
  }
  return iconMap[tier] || 'mdi-account'
}

const getTierDisplayName = (tier: string | null) => {
  if (!tier) return ''
  const nameMap: Record<string, string> = {
    diamond: 'الماس',
    gold: 'طلا',
    silver: 'نقره',
    bronze: 'برنز',
    inactive: 'غیرفعال',
  }
  return nameMap[tier] || ''
}

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('fa-IR').format(num)
}

// Progress ring calculations
const circumference = computed(() => 2 * Math.PI * 18) // radius is 18

const progressPercentage = computed(() => {
  if (!isSeller.value || !gamificationStore.userTier || !gamificationStore.nextTier) return 0
  
  const thresholds: Record<string, number> = {
    diamond: 1000,
    gold: 500,
    silver: 200,
    bronze: 50,
    inactive: 0,
  }
  
  const currentTier = gamificationStore.userTier
  const currentPoints = gamificationStore.engagement?.total_points || 0
  const currentThreshold = thresholds[currentTier] || 0
  const nextThreshold = thresholds[gamificationStore.nextTier] || 1000
  const range = nextThreshold - currentThreshold
  
  if (range === 0) return 100
  
  const progress = ((currentPoints - currentThreshold) / range) * 100
  return Math.max(0, Math.min(100, progress))
})

const progressOffset = computed(() => {
  const progress = progressPercentage.value
  return circumference.value - (progress / 100) * circumference.value
})
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard-header {
  position: sticky;
  top: 0;
  z-index: 100;
}

.dashboard-main {
  padding: 0;
  background-color: #f5f5f5;
}

.notification-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.04);
}

.avatar-with-badge {
  position: relative;
  display: inline-block;
}

.user-avatar {
  position: relative;
  z-index: 2;
}

.progress-ring {
  position: absolute;
  top: -4px;
  left: -4px;
  z-index: 1;
}

.progress-circle {
  transition: stroke-dashoffset 0.5s ease;
}

.tier-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  z-index: 3;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>

