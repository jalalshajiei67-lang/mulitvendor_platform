<template>
  <v-app-bar density="comfortable" color="white" elevation="1" class="app-header">
    <v-container class="d-flex align-center justify-space-between py-2" fluid>
      <div class="d-flex align-center gap-3">
        <NuxtLink to="/" class="d-flex align-center text-decoration-none logo">
          <v-avatar size="40" class="bg-primary/10">
            <span class="text-primary text-h6 font-weight-bold">ای</span>
          </v-avatar>
          <div class="mr-3">
            <strong class="text-primary text-subtitle-1">ایندکسو</strong>
            <div class="text-caption text-medium-emphasis">بازار چندفروشنده</div>
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

      <div class="d-flex align-center gap-2">
        <template v-if="isAuthenticated">
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
        <v-btn icon variant="text" class="d-md-none" @click="toggleDrawer">
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </div>
    </v-container>

    <v-navigation-drawer v-model="drawer" temporary location="right">
      <v-list nav>
        <v-list-item
          v-for="item in drawerItems"
          :key="item.to"
          :to="item.to"
          rounded="lg"
          @click="drawer = false"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
          <template #append>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-app-bar>
</template>

<script setup lang="ts">
const drawer = ref(false)
const authStore = useAuthStore()
const route = useRoute()
const { isAuthenticated, isAdmin, isSeller } = storeToRefs(authStore)

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
  { to: '/', label: 'خانه' },
  { to: '/products', label: 'محصولات' },
  { to: '/categories', label: 'دسته‌بندی‌ها' },
  { to: '/departments', label: 'دپارتمان‌ها' },
  { to: '/subcategories', label: 'زیردسته‌ها' },
  { to: '/suppliers', label: 'تأمین‌کنندگان' },
  { to: '/blog', label: 'مجله' },
  { to: '/contact', label: 'تماس با ما' }
]

const drawerItems = computed(() => {
  const baseItems = navigationLinks.map((item) => ({
    title: item.label,
    to: item.to
  }))

  if (isAuthenticated.value) {
    baseItems.push({ title: 'پنل کاربری', to: dashboardLink.value })
    baseItems.push({ title: 'خروج', to: '/logout' })
  } else {
    baseItems.push({ title: 'ورود', to: '/login' })
    baseItems.push({ title: 'ثبت‌نام', to: '/register' })
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
  border-bottom: 1px solid rgba(33, 33, 33, 0.08);
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
}

.logo span {
  letter-spacing: -2px;
}

.nav-link {
  color: #333;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #00c58e;
}
</style>

