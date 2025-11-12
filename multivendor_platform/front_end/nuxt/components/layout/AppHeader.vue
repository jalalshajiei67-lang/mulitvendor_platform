<template>
  <div>
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
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary location="right">
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
    </v-navigation-drawer>
  </div>
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
  { to: '/', label: 'خانه', icon: 'mdi-home' },
  { to: '/products', label: 'محصولات', icon: 'mdi-package-variant' },
  { to: '/categories', label: 'دسته‌بندی', icon: 'mdi-shape' },
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
</style>

