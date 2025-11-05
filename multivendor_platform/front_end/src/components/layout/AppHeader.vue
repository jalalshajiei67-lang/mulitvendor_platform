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
      <!-- Hamburger Menu Button -->
      <v-app-bar-nav-icon 
        @click.stop="toggleDrawer"
        variant="text"
        color="white"
      ></v-app-bar-nav-icon>

      <v-toolbar-title class="font-weight-bold d-flex align-center">
        <router-link to="/" class="text-white text-decoration-none d-flex align-center">
          <v-img 
            src="/indexo.jpg" 
            alt="Logo" 
            max-width="40" 
            max-height="40" 
            class="me-2"
            contain
          ></v-img>
          <span class="d-none d-sm-inline">  ایندکسو</span>
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
      <!-- Desktop Layout: Logo on Left Side -->
      <router-link to="/" class="logo-link d-flex align-center me-4">
        <v-img 
          src="/indexo.jpg" 
          alt="Logo" 
          max-width="50" 
          max-height="50" 
          contain
          class="logo-image"
        ></v-img>
      </router-link>

      <!-- Desktop Layout: Brand Title -->
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
      
      <v-btn 
        color="white" 
        variant="text" 
        to="/contact-us"
        prepend-icon="mdi-email"
      >
        تماس با ما
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

  <!-- Mobile Navigation Drawer -->
  <v-navigation-drawer
    v-if="isMobile && drawer"
    v-model="drawer"
    temporary
    location="start"
    :width="280"
    dir="rtl"
  >
    <v-list nav dense>
      <!-- User Info -->
      <v-list-item v-if="authStore.isAuthenticated" class="mb-4">
        <template v-slot:prepend>
          <v-avatar color="primary" size="40">
            <span class="text-white">
              {{ authStore.user?.username?.charAt(0)?.toUpperCase() }}
            </span>
          </v-avatar>
        </template>
        <v-list-item-title class="font-weight-bold">
          {{ authStore.user?.username }}
        </v-list-item-title>
        <v-list-item-subtitle>
          {{ authStore.user?.role }}
        </v-list-item-subtitle>
      </v-list-item>

      <v-divider></v-divider>

      <!-- Navigation Items -->
      <v-list-item
        prepend-icon="mdi-home"
        title="خانه"
        value="home"
        @click="navigateAndClose('/')"
      ></v-list-item>

      <v-list-item
        prepend-icon="mdi-package-variant"
        title="محصولات"
        value="products"
        @click="navigateAndClose('/departments')"
      ></v-list-item>

      <v-list-item
        prepend-icon="mdi-store"
        title="تامین‌کنندگان"
        value="suppliers"
        @click="navigateAndClose('/suppliers')"
      ></v-list-item>

      <v-list-item
        prepend-icon="mdi-post"
        title="وبلاگ"
        value="blog"
        @click="navigateAndClose('/blog')"
      ></v-list-item>

      <v-list-item
        prepend-icon="mdi-email"
        title="تماس با ما"
        value="contact"
        @click="navigateAndClose('/contact-us')"
      ></v-list-item>

      <!-- Authenticated User Menu Items -->
      <template v-if="authStore.isAuthenticated">
        <v-divider class="my-2"></v-divider>

        <v-list-item
          v-if="authStore.isAdmin"
          prepend-icon="mdi-shield-crown"
          title="پنل مدیریت جنگو"
          value="admin"
          @click="goToDjangoAdmin"
        ></v-list-item>

        <v-list-item
          v-if="authStore.isSeller"
          prepend-icon="mdi-package"
          title="محصولات من"
          value="my-products"
          @click="navigateAndClose('/my-products')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-post-outline"
          title="داشبورد وبلاگ"
          value="blog-dashboard"
          @click="navigateAndClose('/blog/dashboard')"
        ></v-list-item>

        <v-list-item
          v-if="authStore.isSeller"
          prepend-icon="mdi-store"
          title="داشبورد فروشنده"
          value="seller"
          @click="navigateAndClose('/seller/dashboard')"
        ></v-list-item>

        <v-list-item
          v-if="authStore.isBuyer"
          prepend-icon="mdi-view-dashboard"
          title="داشبورد خریدار"
          value="buyer"
          @click="navigateAndClose('/buyer/dashboard')"
        ></v-list-item>

        <v-divider class="my-2"></v-divider>

        <v-list-item
          prepend-icon="mdi-logout"
          title="خروج"
          value="logout"
          @click="handleLogout"
        ></v-list-item>
      </template>

      <!-- Guest Actions -->
      <template v-else>
        <v-divider class="my-2"></v-divider>
        
        <v-list-item
          prepend-icon="mdi-login"
          title="ورود"
          value="login"
          @click="navigateAndClose('/login')"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-account-plus"
          title="ثبت‌نام"
          value="register"
          @click="navigateAndClose('/register')"
        ></v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
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

// Drawer state for mobile navigation
const drawer = ref(false)

const toggleDrawer = () => {
  drawer.value = !drawer.value
}

watch(isMobile, (value) => {
  if (!value) {
    drawer.value = false
  }
})

const navigateTo = (route) => {
  router.push(route)
}

const navigateAndClose = (route) => {
  drawer.value = false
  router.push(route)
}

const handleLogout = async () => {
  drawer.value = false
  await authStore.logout()
  router.push('/')
}

const goToDjangoAdmin = () => {
  drawer.value = false
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

/* Logo Styles */
.logo-link {
  text-decoration: none;
  transition: opacity 0.3s ease;
}

.logo-link:hover {
  opacity: 0.8;
}

.logo-image {
  border-radius: 4px;
}
</style>

