<!-- src/App.vue -->
<template>
  <v-app>
    <!-- App Bar with Material Design 3 and RTL Support -->
    <v-app-bar 
      color="primary" 
      elevation="2"
      prominent
      class="px-2"
    >
      <!-- Mobile/Tablet: Navigation icon (Hamburger button) -->
      <template v-slot:prepend>
        <v-app-bar-nav-icon 
          @click="drawer = !drawer" 
          class="d-md-none"
        ></v-app-bar-nav-icon>
      </template>
      
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

      <!-- Search Bar -->
      <div style="max-width: 400px; flex: 1;" class="mx-4 d-none d-sm-block">
        <GlobalSearch />
      </div>

      <v-spacer></v-spacer>

      <!-- User Menu -->
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
          <v-list>
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
        <v-btn color="white" variant="text" @click="navigateTo('/login')" class="mx-1" size="small">
          ورود
        </v-btn>
        <v-btn color="white" variant="outlined" @click="navigateTo('/register')" size="small">
          ثبت‌نام
        </v-btn>
      </template>
    </v-app-bar>

    <!-- Navigation Drawer with RTL Support (Mobile/Tablet Only) -->
    <v-navigation-drawer 
      v-model="drawer" 
      temporary
      location="middle"
      :width="280"
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
          @click="navigateTo('/')"
        ></v-list-item>

  

        <v-list-item
          prepend-icon="mdi-package-variant"
          title="محصولات"
          value="products"
          @click="navigateTo('/departments')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-store"
          title="تامین‌کنندگان"
          value="suppliers"
          @click="navigateTo('/suppliers')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-post"
          title="وبلاگ"
          value="blog"
          @click="navigateTo('/blog')"
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
            @click="navigateTo('/my-products')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-post-outline"
            title="داشبورد وبلاگ"
            value="blog-dashboard"
            @click="navigateTo('/blog/dashboard')"
          ></v-list-item>

          <v-list-item
            v-if="authStore.isSeller"
            prepend-icon="mdi-store"
            title="داشبورد فروشنده"
            value="seller"
            @click="navigateTo('/seller/dashboard')"
          ></v-list-item>

          <v-list-item
            v-if="authStore.isBuyer"
            prepend-icon="mdi-view-dashboard"
            title="داشبورد خریدار"
            value="buyer"
            @click="navigateTo('/buyer/dashboard')"
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
            @click="navigateTo('/login')"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-account-plus"
            title="ثبت‌نام"
            value="register"
            @click="navigateTo('/register')"
          ></v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main class="bg-background">
      <router-view />
    </v-main>

    <!-- Footer with Material Design 3 -->
    <v-footer color="primary" class="text-center" elevation="8">
      <v-container>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <h3 class="text-subtitle-1 text-sm-h6 mb-2">درباره ما</h3>
            <p class="text-caption text-sm-body-2">پلتفرم چند فروشنده برای محصولات و خدمات متنوع</p>
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
            <p class="text-caption text-sm-body-2">تلفن: +۹۸ ۲۱ ۱۲۳۴ ۵۶۷۸</p>
          </v-col>
        </v-row>
        <v-divider class="my-3 my-sm-4"></v-divider>
        <p class="text-caption text-sm-body-2">&copy; {{ new Date().getFullYear() }} پلتفرم چند فروشنده. تمامی حقوق محفوظ است.</p>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import GlobalSearch from '@/components/GlobalSearch.vue'
import config from '@/config'

export default {
  name: 'App',
  components: {
    GlobalSearch,
  },
  setup() {
    const authStore = useAuthStore()
    const { t } = useI18n()

    onMounted(() => {
      authStore.initializeAuth()
    })

    return {
      authStore,
      t
    }
  },
  data() {
    return {
      drawer: false
    }
  },
  methods: {
    navigateTo(route) {
      this.drawer = false // Close drawer when navigating
      this.$router.push(route)
    },
    async handleLogout() {
      this.drawer = false
      await this.authStore.logout()
      this.$router.push('/')
    },
    goToDjangoAdmin() {
      this.drawer = false
      window.location.href = config.djangoAdminUrl
    }
  }
}
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
</style>
