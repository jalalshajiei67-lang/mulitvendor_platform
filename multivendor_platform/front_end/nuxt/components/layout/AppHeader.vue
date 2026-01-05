<template>
  <div>
    <v-app-bar density="comfortable" color="white" elevation="1" class="app-header">
      <v-container class="d-flex align-center justify-space-between py-2" fluid>
        <div class="d-flex align-center gap-3">
          <v-btn icon variant="text" class="d-md-none" @click="toggleDrawer">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
          <NuxtLink to="/" class="d-flex align-center text-decoration-none logo">
            <img 
              src="/indexo.jpg" 
              alt="لوگو ایندکسو" 
              class="logo-image"
            />
            <div class="mr-3 logo-text">
              <strong class="text-primary text-subtitle-1">ایندکسو</strong>
              <div class="text-caption text-medium-emphasis logo-subtitle">خرید و فروش آسان ماشین‌آلات</div>
            </div>
          </NuxtLink>
        </div>

        <div class="d-none d-md-flex align-center gap-4">
          <NuxtLink
            v-for="item in navigationLinks"
            :key="item.to"
            :to="item.to"
            class="nav-link text-body-2"
          >
            {{ item.label }}
          </NuxtLink>
        </div>

        <ClientOnly>
          <div class="d-flex align-center gap-2 header-buttons">
            <template v-if="isAuthenticated">
              <!-- Notification Bell -->
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
                    class="notification-btn"
                  >
                    <v-badge
                      :content="notificationCount"
                      :model-value="notificationCount > 0"
                      color="error"
                      overlap
                    >
                      <v-icon>mdi-bell</v-icon>
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
                      <v-list-item-title class="text-grey">هیچ اعلانی وجود ندارد</v-list-item-title>
                    </v-list-item>
                    <v-list-item
                      v-for="notification in notifications"
                      :key="notification.id"
                      @click="handleNotificationClick(notification)"
                      class="notification-item"
                    >
                      <template v-slot:prepend>
                        <v-icon :color="notification.color">{{ notification.icon }}</v-icon>
                      </template>
                      <v-list-item-title>{{ notification.title }}</v-list-item-title>
                      <v-list-item-subtitle>{{ notification.subtitle }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-menu>

              <v-btn color="primary" variant="flat" size="small" :to="dashboardLink">
                پنل کاربری
              </v-btn>
              <v-btn color="secondary" variant="outlined" size="small" to="/logout">
                خروج
              </v-btn>
            </template>
            <template v-else>
              <v-btn color="primary" variant="flat" size="small" to="/login">
                ورود
              </v-btn>
              <v-btn color="secondary" variant="outlined" size="small" to="/register">
                ثبت‌نام
              </v-btn>
            </template>
          </div>
          <template #fallback>
            <div class="d-flex align-center gap-2">
              <v-btn color="primary" variant="flat" size="small" to="/login">
                ورود
              </v-btn>
              <v-btn color="secondary" variant="outlined" size="small" to="/register">
                ثبت‌نام
              </v-btn>
            </div>
          </template>
        </ClientOnly>
      </v-container>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary location="right">
      <ClientOnly>
        <v-list nav>
          <v-list-item
            v-for="item in drawerItems"
            :key="item.to"
            :to="item.to"
            rounded="lg"
            @click="drawer = false"
          >
            <template #prepend>
              <v-icon>{{ item.icon }}</v-icon>
            </template>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
            <template #append>
              <v-icon>mdi-chevron-left</v-icon>
            </template>
          </v-list-item>
        </v-list>
        <template #fallback>
          <v-list nav>
            <v-list-item
              v-for="item in navigationLinks"
              :key="item.to"
              :to="item.to"
              rounded="lg"
              @click="drawer = false"
            >
              <template #prepend>
                <v-icon>{{ item.icon }}</v-icon>
              </template>
              <v-list-item-title>{{ item.label }}</v-list-item-title>
              <template #append>
                <v-icon>mdi-chevron-left</v-icon>
              </template>
            </v-list-item>
            <v-list-item to="/login" rounded="lg" @click="drawer = false">
              <template #prepend>
                <v-icon>mdi-login</v-icon>
              </template>
              <v-list-item-title>ورود</v-list-item-title>
              <template #append>
                <v-icon>mdi-chevron-left</v-icon>
              </template>
            </v-list-item>
            <v-list-item to="/register" rounded="lg" @click="drawer = false">
              <template #prepend>
                <v-icon>mdi-account-plus</v-icon>
              </template>
              <v-list-item-title>ثبت‌نام</v-list-item-title>
              <template #append>
                <v-icon>mdi-chevron-left</v-icon>
              </template>
            </v-list-item>
          </v-list>
        </template>
      </ClientOnly>
    </v-navigation-drawer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const drawer = ref(false)
const authStore = useAuthStore()
const route = useRoute()
const { isAuthenticated, isAdmin, isSeller, isBuyer } = storeToRefs(authStore)

const showNotificationsMenu = ref(false)
const notifications = ref<any[]>([])

// Fetch notifications for buyers
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

let notificationInterval: ReturnType<typeof setInterval> | null = null

// Setup notification polling when component mounts (client-side only)
onMounted(() => {
  if (isAuthenticated.value && isBuyer.value) {
    loadNotifications()
    // Refresh notifications every 30 seconds
    notificationInterval = setInterval(() => {
      if (isAuthenticated.value && isBuyer.value) {
        loadNotifications()
      }
    }, 30000)
  }
})

// Update notifications when authentication state changes
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
})

// Cleanup on unmount
onUnmounted(() => {
  if (notificationInterval) {
    clearInterval(notificationInterval)
  }
})

const dashboardLink = computed(() => {
  if (isAdmin.value) {
    return '/admin/dashboard'
  }
  if (isSeller.value) {
    return '/seller/dashboard'
  }
  return '/buyer/dashboard'
})

const navigationLinks = [
  { to: '/', label: 'خانه', icon: 'mdi-home' },
  { to: '/suppliers', label: 'فروشندگان', icon: 'mdi-store' },
  { to: '/rfq', label: 'درخواست قیمت', icon: 'mdi-file-document-edit' },
  { to: '/blog', label: 'مجله', icon: 'mdi-post' },
  { to: '/about', label: 'درباره ما', icon: 'mdi-information' },
  { to: '/contact', label: 'تماس', icon: 'mdi-phone' }
]

const drawerItems = computed(() => {
  const baseItems = navigationLinks.map((item) => ({
    title: item.label,
    to: item.to,
    icon: item.icon
  }))

  if (isAuthenticated.value) {
    baseItems.push({ title: 'پنل کاربری', to: dashboardLink.value, icon: 'mdi-view-dashboard' })
    baseItems.push({ title: 'خروج', to: '/logout', icon: 'mdi-logout' })
  } else {
    baseItems.push({ title: 'ورود', to: '/login', icon: 'mdi-login' })
    baseItems.push({ title: 'ثبت‌نام', to: '/register', icon: 'mdi-account-plus' })
  }

  return baseItems
})

const toggleDrawer = () => {
  drawer.value = !drawer.value
}

watch(
  () => route.fullPath,
  () => {
    drawer.value = false
  }
)
</script>

<style scoped>
.app-header {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  background-color: rgba(var(--v-theme-surface), 0.95);
  backdrop-filter: blur(8px);
}

.logo-image {
  height: 48px;
  width: auto;
  object-fit: contain;
  border-radius: 8px;
}

.logo span {
  letter-spacing: -2px;
}

.nav-link {
  color: rgba(var(--v-theme-on-surface), 0.87);
  transition: color 0.2s;
  margin: 0 10px;
}

.nav-link:hover {
  color: rgb(var(--v-theme-primary));
}

.notification-btn {
  margin-left: 8px;
}

.header-buttons .v-btn + .v-btn {
  margin-left: 2px;
}

.notification-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.notification-item:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.04);
}

/* Mobile responsive logo */
@media (max-width: 600px) {
  .logo-image {
    height: 40px;
  }

  .logo-text {
    max-width: 140px;
    overflow: hidden;
  }

  .logo-subtitle {
    display: none;
  }
}

@media (max-width: 400px) {
  .logo-text {
    max-width: 100px;
  }
}
</style>

