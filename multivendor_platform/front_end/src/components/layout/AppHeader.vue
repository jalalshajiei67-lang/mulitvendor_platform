<!-- src/components/layout/AppHeader.vue -->
<template>
  <v-app-bar 
    color="primary" 
    elevation="2"
    :prominent="isMobile"
    :fixed="isMobile"
    class="px-2"
    app
    dir="rtl"
  >
    <!-- Mobile Layout: Logo and User Menu on Top Row -->
    <template v-if="isMobile">
      <v-toolbar-title class="font-weight-bold d-flex align-center">
        <router-link to="/" class="text-white text-decoration-none">
          پلتفرم چند فروشنده
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- User Menu on Mobile -->
      <v-menu v-if="authStore.isAuthenticated" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn 
            icon="mdi-account-circle" 
            v-bind="props"
            variant="text"
            color="white"
            size="small"
          ></v-btn>
        </template>
        <v-list dir="rtl">
          <v-list-item>
            <v-list-item-title class="font-weight-bold">{{ authStore.user?.username }}</v-list-item-title>
            <v-list-item-subtitle>{{ authStore.user?.role }}</v-list-item-subtitle>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item v-if="authStore.isAdmin" @click="goToDjangoAdmin" prepend-icon="mdi-shield-crown">
            <v-list-item-title>پنل مدیریت جنگو</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="authStore.isSeller" @click="navigateTo('/seller/dashboard')" prepend-icon="mdi-store">
            <v-list-item-title>داشبورد فروشنده</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="authStore.isBuyer" @click="navigateTo('/buyer/dashboard')" prepend-icon="mdi-view-dashboard">
            <v-list-item-title>داشبورد خریدار</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="handleLogout" prepend-icon="mdi-logout">
            <v-list-item-title>خروج</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>

    <!-- Desktop Layout -->
    <template v-else>
      <!-- Desktop Layout: Logo/Brand Title -->
      <v-toolbar-title class="font-weight-bold">
        <router-link to="/" class="text-white text-decoration-none">
          پلتفرم چند فروشنده
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Desktop: Navigation Menu Items -->
      <div class="d-none d-md-flex flex-row-reverse align-center mx-4">
      <v-btn 
        color="white" 
        variant="text" 
        to="/"
        prepend-icon="mdi-home"
      >
        خانه
      </v-btn>
     
      <v-btn 
        color="white" 
        variant="text" 
        to="/departments"
        prepend-icon="mdi-package-variant"
      >
        محصولات
      </v-btn>

      <v-btn 
        color="white" 
        variant="text" 
        to="/suppliers"
        prepend-icon="mdi-store"
      >
        تامین‌کنندگان
      </v-btn>
      
      <v-btn 
        color="white" 
        variant="text" 
        to="/blog"
        prepend-icon="mdi-post"
      >
        وبلاگ
      </v-btn>
      
      <!-- Desktop: My Products for Sellers -->
      <v-btn 
        v-if="authStore.isAuthenticated && authStore.isSeller"
        color="white" 
        variant="text" 
        to="/my-products"
        prepend-icon="mdi-package"
      >
        محصولات من
      </v-btn>
      
      <!-- Desktop: Blog Dashboard for authenticated users -->
      <v-btn 
        v-if="authStore.isAuthenticated"
        color="white" 
        variant="text" 
        to="/blog/dashboard"
        prepend-icon="mdi-post-outline"
      >
        داشبورد وبلاگ
      </v-btn>
      </div>

      <v-spacer></v-spacer>

      <!-- Desktop: Search Bar -->
      <div 
        class="search-container desktop-search mx-auto"
        style="max-width: 400px;"
      >
        <GlobalSearch />
      </div>

      <v-spacer></v-spacer>

      <!-- Desktop: User Menu -->
      <template v-if="authStore.isAuthenticated">
        <v-btn 
          icon="mdi-bell" 
          variant="text"
          color="white"
          class="d-none d-sm-flex"
        ></v-btn>
        
        <v-menu location="bottom">
          <template v-slot:activator="{ props }">
            <v-btn 
              icon="mdi-account-circle" 
              v-bind="props"
              variant="text"
              color="white"
            ></v-btn>
          </template>
          <v-list dir="rtl">
            <v-list-item>
              <v-list-item-title class="font-weight-bold">{{ authStore.user?.username }}</v-list-item-title>
              <v-list-item-subtitle>{{ authStore.user?.role }}</v-list-item-subtitle>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item v-if="authStore.isAdmin" @click="goToDjangoAdmin" prepend-icon="mdi-shield-crown">
              <v-list-item-title>پنل مدیریت جنگو</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="authStore.isSeller" @click="navigateTo('/seller/dashboard')" prepend-icon="mdi-store">
              <v-list-item-title>داشبورد فروشنده</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="authStore.isBuyer" @click="navigateTo('/buyer/dashboard')" prepend-icon="mdi-view-dashboard">
              <v-list-item-title>داشبورد خریدار</v-list-item-title>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item @click="handleLogout" prepend-icon="mdi-logout">
              <v-list-item-title>خروج</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
      <template v-else>
        <v-btn 
          color="white" 
          variant="text" 
          @click="navigateTo('/login')" 
          class="mx-1" 
          size="small"
        >
          ورود
        </v-btn>
        <v-btn 
          color="white" 
          variant="outlined" 
          @click="navigateTo('/register')" 
          size="small"
        >
          ثبت‌نام
        </v-btn>
      </template>
    </template>

    <!-- Mobile: Large Search Bar (Below title row) -->
    <template v-if="isMobile" v-slot:extension>
      <div class="mobile-search-container pa-2 d-flex justify-center">
        <GlobalSearch />
      </div>
    </template>
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '@/stores/auth'
import GlobalSearch from '@/components/GlobalSearch.vue'
import config from '@/config'

const router = useRouter()
const { mdAndDown } = useDisplay()
const authStore = useAuthStore()

// Check if mobile/tablet (< 960px / md breakpoint)
const isMobile = computed(() => mdAndDown.value)

const navigateTo = (route) => {
  router.push(route)
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/')
}

const goToDjangoAdmin = () => {
  window.location.href = config.djangoAdminUrl
}
</script>

<style scoped>
.search-container {
  transition: all 0.3s ease;
}

.mobile-search-container {
  width: 100%;
  padding: 0.5rem 0.75rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.desktop-search {
  max-width: 400px;
  margin: 0 auto;
}

/* RTL Support */
.text-white {
  color: white !important;
}

.text-decoration-none {
  text-decoration: none !important;
}
</style>

