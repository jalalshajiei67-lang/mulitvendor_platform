<template>
  <v-app class="admin-layout" dir="rtl">
    <LazyAdminSidebar
      :drawer="drawer"
      :rail="rail"
      :is-mobile="isMobile"
      :active-view="activeView"
      :user="authStore.user"
      @update:drawer="drawer = $event"
      @update:rail="rail = $event"
      @navigate="handleNavigate"
      @create-blog-post="handleCreateBlogPost"
    />

    <v-app-bar
      :elevation="2"
      color="primary"
      class="admin-header"
      fixed
    >
      <NuxtLink to="/" class="logo-link">
        <v-img
          src="/indexo.jpg"
          alt="Logo"
          max-height="40"
          max-width="120"
          contain
          class="logo-img"
        ></v-img>
      </NuxtLink>

      <v-spacer></v-spacer>

      <v-app-bar-nav-icon
        v-if="isMobile"
        @click="drawer = !drawer"
        class="hamburger-btn"
      ></v-app-bar-nav-icon>

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

      <v-menu location="bottom end">
        <template v-slot:activator="{ props }">
          <v-btn
            icon
            v-bind="props"
            variant="text"
          >
            <v-avatar size="32">
              <v-icon>mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="handleLogout">
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            <v-list-item-title>خروج</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <div
      class="admin-main"
      :style="{
        paddingLeft: !isMobile && drawer ? (rail ? '64px' : '271px') : '0'
      }"
    >
      <v-main>
        <slot />
      </v-main>
    </div>
  </v-app>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const { mdAndDown } = useDisplay()

const drawer = ref(!mdAndDown.value)
const rail = ref(false)
const isMobile = computed(() => mdAndDown.value)
const activeView = ref('dashboard')
const showNotificationsMenu = ref(false)
const notifications = ref<any[]>([])

const notificationCount = computed(() => notifications.value.length)

watch(() => mdAndDown.value, (newVal) => {
  drawer.value = !newVal
})

const handleNavigate = (view: string) => {
  activeView.value = view
  if (isMobile.value) {
    drawer.value = false
  }
  // Update route query if on dashboard page
  if (route.path === '/admin/dashboard') {
    navigateTo({
      path: '/admin/dashboard',
      query: { view }
    })
  }
}

const handleCreateBlogPost = () => {
  navigateTo('/admin/dashboard/blog/new')
}

const handleNotificationClick = (notification: any) => {
  showNotificationsMenu.value = false
  if (notification.link) {
    navigateTo(notification.link)
  }
}

const handleLogout = async () => {
  await authStore.logout()
  navigateTo('/login')
}

// Watch route query for view changes
watch(() => route.query.view, (newView) => {
  if (typeof newView === 'string') {
    activeView.value = newView
  }
}, { immediate: true })
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.admin-header {
  z-index: 1000;
}

.logo-link {
  text-decoration: none;
  display: flex;
  align-items: center;
}

.admin-main {
  transition: padding-left 0.3s ease;
  min-height: 100vh;
  padding-top: 64px;
}
</style>

