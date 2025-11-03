<!-- src/App.vue -->
<template>
  <v-app>
    <!-- Persistent Header with Large Mobile-Compatible Search Bar -->
    <AppHeader />

    <!-- Main Content -->
    <v-main class="bg-background" :class="{ 'mobile-main': isMobile }">
      <router-view />
    </v-main>

    <!-- Footer with Material Design 3 (Desktop Only) -->
    <v-footer 
      color="primary" 
      class="text-center d-none d-md-block" 
      elevation="8"
    >
      <v-container>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <h3 class="text-subtitle-1 text-sm-h6 mb-2">درباره ما</h3>
            <p class="text-caption text-sm-body-2">ایندکسو</p>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <h3 class="text-subtitle-1 text-sm-h6 mb-2">لینک‌های سریع</h3>
            <div class="d-flex flex-column align-center">
              <router-link to="/departments" class="text-white text-decoration-none mb-1 hover-link">محصولات</router-link>
              <router-link to="/suppliers" class="text-white text-decoration-none mb-1 hover-link">تامین‌کنندگان</router-link>
              <router-link to="/blog" class="text-white text-decoration-none mb-1 hover-link">وبلاگ</router-link>
              <router-link to="/sitemap" class="text-white text-decoration-none mb-1 hover-link">نقشه سایت</router-link>
            </div>
          </v-col>
          <v-col cols="12" md="4">
            <h3 class="text-subtitle-1 text-sm-h6 mb-2">تماس با ما</h3>
            <p class="text-caption text-sm-body-2 mb-1">ایمیل: info@example.com</p>
            <p class="text-caption text-sm-body-2">تلفن02188311001 </p>
          </v-col>
        </v-row>
        <v-divider class="my-3 my-sm-4"></v-divider>
        <p class="text-caption text-sm-body-2">&copy; {{ new Date().getFullYear() }} پلتفرم چند فروشنده. تمامی حقوق محفوظ است.</p>
      </v-container>
    </v-footer>

    <!-- Bottom Navigation (Mobile/Tablet Only - replaces drawer) -->
    <BottomNavigation v-if="isMobile" />
  </v-app>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import AppHeader from '@/components/layout/AppHeader.vue'
import BottomNavigation from '@/components/layout/BottomNavigation.vue'

const { mdAndDown } = useDisplay()
const authStore = useAuthStore()
const { t } = useI18n()

// Check if mobile/tablet (< 960px / md breakpoint)
const isMobile = computed(() => mdAndDown.value)

onMounted(() => {
  authStore.initializeAuth()
})
</script>

<style>
/* Global styles for Vuetify Material Design 3 */
.text-white {
  color: white !important;
}

.text-decoration-none {
  text-decoration: none !important;
}

/* Hover effect for footer links */
.hover-link {
  transition: opacity 0.2s ease-in-out;
}

.hover-link:hover {
  opacity: 0.8;
}

/* Background color helper */
.bg-background {
  background-color: rgb(var(--v-theme-background)) !important;
}

/* Mobile main content padding for bottom navigation */
.mobile-main {
  padding-bottom: 80px !important; /* Space for bottom navigation */
}

/* RTL support */
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}
</style>
