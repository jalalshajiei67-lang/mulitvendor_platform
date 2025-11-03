<!-- src/components/layout/BottomNavigation.vue -->
<template>
  <v-bottom-navigation
    :model-value="activeTab"
    @update:model-value="handleTabChange"
    color="primary"
    grow
    elevation="8"
    app
    fixed
    dir="rtl"
    class="bottom-nav"
  >
    <!-- Home -->
    <v-btn
      value="home"
      to="/"
      @click="navigateTo('/')"
    >
      <v-icon>mdi-home</v-icon>
      <span>خانه</span>
    </v-btn>

    <!-- Products -->
    <v-btn
      value="products"
      to="/departments"
      @click="navigateTo('/departments')"
    >
      <v-icon>mdi-package-variant</v-icon>
      <span>محصولات</span>
    </v-btn>

    <!-- Suppliers -->
    <v-btn
      value="suppliers"
      to="/suppliers"
      @click="navigateTo('/suppliers')"
    >
      <v-icon>mdi-store</v-icon>
      <span>تامین‌کنندگان</span>
    </v-btn>

    <!-- Blog -->
    <v-btn
      value="blog"
      to="/blog"
      @click="navigateTo('/blog')"
    >
      <v-icon>mdi-post</v-icon>
      <span>وبلاگ</span>
    </v-btn>

    <!-- My Products (for Sellers) -->
    <v-btn
      v-if="authStore.isAuthenticated && authStore.isSeller"
      value="my-products"
      to="/my-products"
      @click="navigateTo('/my-products')"
    >
      <v-icon>mdi-package</v-icon>
      <span>محصولات من</span>
    </v-btn>

    <!-- Blog Dashboard (for authenticated users) -->
    <v-btn
      v-else-if="authStore.isAuthenticated"
      value="blog-dashboard"
      to="/blog/dashboard"
      @click="navigateTo('/blog/dashboard')"
    >
      <v-icon>mdi-post-outline</v-icon>
      <span>داشبورد وبلاگ</span>
    </v-btn>

    <!-- Account/Login (for guests or additional menu) -->
    <v-menu
      v-if="authStore.isAuthenticated"
      location="top"
      offset-y
    >
      <template v-slot:activator="{ props }">
        <v-btn
          value="account"
          v-bind="props"
        >
          <v-icon>mdi-account-circle</v-icon>
          <span>حساب کاربری</span>
        </v-btn>
      </template>
      <v-list dir="rtl" density="compact">
        <v-list-item>
          <v-list-item-title class="font-weight-bold text-center">
            {{ authStore.user?.username }}
          </v-list-item-title>
          <v-list-item-subtitle class="text-center">
            {{ authStore.user?.role }}
          </v-list-item-subtitle>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item 
          v-if="authStore.isAdmin" 
          @click="goToDjangoAdmin"
          prepend-icon="mdi-shield-crown"
        >
          <v-list-item-title>پنل مدیریت جنگو</v-list-item-title>
        </v-list-item>
        <v-list-item 
          v-if="authStore.isSeller" 
          @click="navigateTo('/seller/dashboard')"
          prepend-icon="mdi-store"
        >
          <v-list-item-title>داشبورد فروشنده</v-list-item-title>
        </v-list-item>
        <v-list-item 
          v-if="authStore.isBuyer" 
          @click="navigateTo('/buyer/dashboard')"
          prepend-icon="mdi-view-dashboard"
        >
          <v-list-item-title>داشبورد خریدار</v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item 
          @click="handleLogout"
          prepend-icon="mdi-logout"
        >
          <v-list-item-title>خروج</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- Login button for guests -->
    <v-btn
      v-else
      value="login"
      to="/login"
      @click="navigateTo('/login')"
    >
      <v-icon>mdi-login</v-icon>
      <span>ورود</span>
    </v-btn>
  </v-bottom-navigation>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import config from '@/config'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Determine active tab based on current route
const activeTab = computed(() => {
  const path = route.path
  
  if (path === '/') return 'home'
  if (path.startsWith('/departments') || path.startsWith('/categories') || path.startsWith('/subcategories') || path.startsWith('/products')) {
    return path.startsWith('/my-products') ? 'my-products' : 'products'
  }
  if (path.startsWith('/suppliers')) return 'suppliers'
  if (path.startsWith('/blog')) {
    return path.includes('/dashboard') ? 'blog-dashboard' : 'blog'
  }
  if (path.startsWith('/login') || path.startsWith('/register')) return 'login'
  if (path.startsWith('/seller/dashboard') || path.startsWith('/buyer/dashboard') || path.startsWith('/admin/dashboard')) {
    return 'account'
  }
  
  return null
})

const navigateTo = (routePath) => {
  router.push(routePath)
}

const handleTabChange = (value) => {
  // Navigation is handled by the @click handlers
  // This is just for the v-model binding
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}

const goToDjangoAdmin = () => {
  window.location.href = config.djangoAdminUrl
}

// Watch route changes to update active tab
watch(() => route.path, () => {
  // Active tab will be automatically updated via computed property
})
</script>

<style scoped>
.bottom-nav {
  direction: rtl;
  z-index: 1000;
}

/* RTL optimization for bottom navigation */
.bottom-nav :deep(.v-btn) {
  flex-direction: column;
  gap: 0.25rem;
}

.bottom-nav :deep(.v-btn__content) {
  flex-direction: column;
  gap: 0.25rem;
}

/* Ensure icons and labels are properly aligned for RTL */
.bottom-nav :deep(span) {
  font-size: 0.75rem;
  line-height: 1.2;
  text-align: center;
}

/* Active state styling */
.bottom-nav :deep(.v-btn--active) {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Mobile-specific adjustments */
@media (max-width: 600px) {
  .bottom-nav :deep(span) {
    font-size: 0.7rem;
  }
  
  .bottom-nav :deep(.v-icon) {
    font-size: 1.5rem;
  }
}

/* Tablet adjustments */
@media (min-width: 600px) and (max-width: 959px) {
  .bottom-nav :deep(span) {
    font-size: 0.8rem;
  }
  
  .bottom-nav :deep(.v-icon) {
    font-size: 1.75rem;
  }
}
</style>

