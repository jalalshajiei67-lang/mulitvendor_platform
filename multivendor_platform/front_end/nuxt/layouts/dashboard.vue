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
                  <v-avatar size="32">
                    <v-icon>mdi-account</v-icon>
                  </v-avatar>
                </v-btn>
              </template>
              <v-list>
                <v-list-item>
                  <v-list-item-title class="font-weight-bold">
                    {{ authStore.user?.first_name || authStore.user?.username }}
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ authStore.user?.email }}</v-list-item-subtitle>
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
import { ref, computed, watch, onUnmounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
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
</style>

