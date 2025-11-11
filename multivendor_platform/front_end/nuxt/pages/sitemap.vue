<template>
  <v-container class="sitemap-page py-8" dir="rtl">
    <!-- Page Header -->
    <v-row class="mb-8">
      <v-col cols="12">
        <h1 class="text-h3 text-center mb-4">
          <v-icon size="large" class="ml-2">mdi-sitemap</v-icon>
          نقشه سایت
        </h1>
        <p class="text-center text-body-1 text-medium-emphasis">
          راهنمای کامل صفحات و بخش‌های پلتفرم
        </p>
      </v-col>
    </v-row>

    <!-- Sitemap Sections -->
    <v-row>
      <!-- Public Pages -->
      <v-col cols="12" md="6" lg="4">
        <v-card elevation="2" class="h-100">
          <v-card-title class="bg-primary">
            <v-icon class="ml-2">mdi-earth</v-icon>
            صفحات عمومی
          </v-card-title>
          <v-card-text>
            <v-list density="compact" nav>
              <v-list-item :to="{ path: '/' }" prepend-icon="mdi-home" link>
                <v-list-item-title>صفحه اصلی</v-list-item-title>
              </v-list-item>
              <v-list-item :to="{ path: '/about' }" prepend-icon="mdi-information" link>
                <v-list-item-title>درباره ما</v-list-item-title>
              </v-list-item>
              <v-list-item :to="{ path: '/contact' }" prepend-icon="mdi-email" link>
                <v-list-item-title>تماس با ما</v-list-item-title>
              </v-list-item>
              <v-list-item :to="{ path: '/sitemap' }" prepend-icon="mdi-sitemap" link>
                <v-list-item-title>نقشه سایت</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Products -->
      <v-col cols="12" md="6" lg="4">
        <v-card elevation="2" class="h-100">
          <v-card-title class="bg-success">
            <v-icon class="ml-2">mdi-package-variant</v-icon>
            محصولات
          </v-card-title>
          <v-card-text>
            <v-list density="compact" nav>
              <v-list-item :to="{ path: '/products' }" prepend-icon="mdi-view-grid" link>
                <v-list-item-title>لیست محصولات</v-list-item-title>
              </v-list-item>
              <v-list-item v-if="isAuthenticated && isSeller" :to="{ path: '/admin/dashboard/products/new' }" prepend-icon="mdi-plus-circle" link>
                <v-list-item-title>افزودن محصول جدید</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Departments & Categories -->
      <v-col cols="12" md="6" lg="4">
        <v-card elevation="2" class="h-100">
          <v-card-title class="bg-info">
            <v-icon class="ml-2">mdi-folder-multiple</v-icon>
            بخش‌ها و دسته‌بندی‌ها
          </v-card-title>
          <v-card-text>
            <v-list density="compact" nav>
              <v-list-item :to="{ path: '/departments' }" prepend-icon="mdi-view-dashboard" link>
                <v-list-item-title>لیست بخش‌ها</v-list-item-title>
              </v-list-item>
              <v-list-subheader v-if="departments.length > 0">بخش‌های موجود:</v-list-subheader>
              <v-list-item 
                v-for="dept in departments.slice(0, 5)" 
                :key="dept.id"
                :to="{ path: `/departments/${dept.slug}` }"
                prepend-icon="mdi-folder"
                class="pr-8"
                link
              >
                <v-list-item-title>{{ dept.name }}</v-list-item-title>
              </v-list-item>
              <v-list-item v-if="departments.length > 5" disabled>
                <v-list-item-title class="text-caption">و {{ departments.length - 5 }} بخش دیگر...</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Suppliers -->
      <v-col cols="12" md="6" lg="4">
        <v-card elevation="2" class="h-100">
          <v-card-title class="bg-warning">
            <v-icon class="ml-2">mdi-store</v-icon>
            تامین‌کنندگان
          </v-card-title>
          <v-card-text>
            <v-list density="compact" nav>
              <v-list-item :to="{ path: '/suppliers' }" prepend-icon="mdi-view-list" link>
                <v-list-item-title>لیست تامین‌کنندگان</v-list-item-title>
              </v-list-item>
              <v-list-subheader v-if="suppliers.length > 0">تامین‌کنندگان برتر:</v-list-subheader>
              <v-list-item 
                v-for="supplier in suppliers.slice(0, 5)" 
                :key="supplier.id"
                :to="{ path: `/suppliers/${supplier.id}` }"
                prepend-icon="mdi-store-outline"
                class="pr-8"
                link
              >
                <v-list-item-title>{{ supplier.store_name || supplier.username }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Blog -->
      <v-col cols="12" md="6" lg="4">
        <v-card elevation="2" class="h-100">
          <v-card-title class="bg-secondary">
            <v-icon class="ml-2">mdi-post</v-icon>
            وبلاگ
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item :to="{ path: '/blog' }" prepend-icon="mdi-newspaper" link>
                <v-list-item-title>لیست مقالات</v-list-item-title>
              </v-list-item>
              <v-list-item v-if="isAuthenticated" :to="{ path: '/admin/dashboard/blog/new' }" prepend-icon="mdi-pencil-plus" link>
                <v-list-item-title>نوشتن مقاله جدید</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Authentication -->
      <v-col cols="12" md="6" lg="4">
        <v-card elevation="2" class="h-100">
          <v-card-title class="bg-error" v-if="!isAuthenticated">
            <v-icon class="ml-2">mdi-account-key</v-icon>
            ورود و ثبت‌نام
          </v-card-title>
          <v-card-title class="bg-primary" v-else>
            <v-icon class="ml-2">mdi-account-circle</v-icon>
            داشبورد کاربری
          </v-card-title>
          <v-card-text>
            <v-list density="compact" v-if="!isAuthenticated" nav>
              <v-list-item :to="{ path: '/login' }" prepend-icon="mdi-login" link>
                <v-list-item-title>ورود به سیستم</v-list-item-title>
              </v-list-item>
              <v-list-item :to="{ path: '/register' }" prepend-icon="mdi-account-plus" link>
                <v-list-item-title>ثبت‌نام</v-list-item-title>
              </v-list-item>
            </v-list>
            <v-list density="compact" v-else nav>
              <v-list-item v-if="isBuyer" :to="{ path: '/buyer/dashboard' }" prepend-icon="mdi-view-dashboard" link>
                <v-list-item-title>داشبورد خریدار</v-list-item-title>
              </v-list-item>
              <v-list-item v-if="isSeller" :to="{ path: '/seller/dashboard' }" prepend-icon="mdi-storefront" link>
                <v-list-item-title>داشبورد فروشنده</v-list-item-title>
              </v-list-item>
              <v-list-item v-if="isAdmin" :to="{ path: '/admin/dashboard' }" prepend-icon="mdi-shield-account" link>
                <v-list-item-title>پنل مدیریت</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- SEO Sitemap Link -->
    <v-row class="mt-8">
      <v-col cols="12">
        <v-card elevation="1" class="text-center pa-4">
          <v-card-text>
            <v-icon size="large" class="mb-2">mdi-file-xml</v-icon>
            <p class="text-body-1 mb-2">نقشه سایت XML (برای موتورهای جستجو)</p>
            <v-btn 
              color="primary" 
              variant="outlined"
              :href="sitemapXmlUrl"
              target="_blank"
              prepend-icon="mdi-open-in-new"
            >
              مشاهده sitemap.xml
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Statistics -->
    <v-row class="mt-4">
      <v-col cols="12" sm="6" md="3">
        <v-card class="text-center pa-4" color="primary" variant="tonal">
          <v-card-text>
            <div class="text-h4 mb-2">{{ stats.totalProducts }}</div>
            <div class="text-body-2">محصول</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="text-center pa-4" color="success" variant="tonal">
          <v-card-text>
            <div class="text-h4 mb-2">{{ stats.totalDepartments }}</div>
            <div class="text-body-2">بخش</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="text-center pa-4" color="warning" variant="tonal">
          <v-card-text>
            <div class="text-h4 mb-2">{{ stats.totalSuppliers }}</div>
            <div class="text-body-2">تامین‌کننده</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="text-center pa-4" color="info" variant="tonal">
          <v-card-text>
            <div class="text-h4 mb-2">{{ stats.totalBlogPosts }}</div>
            <div class="text-body-2">مقاله</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApiFetch } from '~/composables/useApiFetch'

useHead({
  title: 'نقشه سایت',
  meta: [
    {
      name: 'description',
      content: 'راهنمای کامل صفحات و بخش‌های پلتفرم ایندکسو'
    }
  ]
})

const authStore = useAuthStore()
const config = useRuntimeConfig()

// Auth computed properties
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isBuyer = computed(() => authStore.isBuyer)
const isSeller = computed(() => authStore.isSeller)
const isAdmin = computed(() => authStore.isAdmin)

// Data
const departments = ref<Array<{ id: number; name: string; slug: string }>>([])
const suppliers = ref<Array<{ id: number; store_name?: string; username: string }>>([])
const stats = ref({
  totalProducts: 0,
  totalDepartments: 0,
  totalSuppliers: 0,
  totalBlogPosts: 0
})

// Sitemap XML URL
const sitemapXmlUrl = computed(() => {
  const apiBase = config.public.apiBase.replace('/api', '')
  return `${apiBase}/sitemap.xml`
})

// Methods
const fetchDepartments = async () => {
  try {
    const response = await useApiFetch<{ results?: Array<{ id: number; name: string; slug: string }> } | Array<{ id: number; name: string; slug: string }>>('departments/')
    const depts = Array.isArray(response) ? response : response.results || []
    departments.value = depts
    stats.value.totalDepartments = depts.length
  } catch (error) {
    console.error('Error fetching departments:', error)
  }
}

const fetchSuppliers = async () => {
  try {
    const response = await useApiFetch<{ results?: Array<{ id: number; store_name?: string; username: string }> } | Array<{ id: number; store_name?: string; username: string }>>('users/suppliers/')
    const supps = Array.isArray(response) ? response : response.results || []
    suppliers.value = supps
    stats.value.totalSuppliers = supps.length
  } catch (error) {
    console.error('Error fetching suppliers:', error)
  }
}

const fetchStats = async () => {
  try {
    // Fetch products count
    const productsResponse = await useApiFetch<{ count?: number }>('products/', {
      params: { page_size: 1 }
    })
    stats.value.totalProducts = productsResponse.count || 0

    // Fetch blog posts count
    const blogResponse = await useApiFetch<{ count?: number }>('blog/posts/', {
      params: { page_size: 1 }
    })
    stats.value.totalBlogPosts = blogResponse.count || 0
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

// Lifecycle
onMounted(() => {
  fetchDepartments()
  fetchSuppliers()
  fetchStats()
})
</script>

<style scoped>
.sitemap-page {
  max-width: 1400px;
  margin: 0 auto;
}

.v-card-title {
  color: white;
  font-weight: bold;
}

.h-100 {
  height: 100%;
}

/* Make links more visible */
:deep(.v-list-item) {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

:deep(.v-list-item:hover) {
  background-color: rgba(0, 0, 0, 0.05);
}

:deep(.v-list-item-title) {
  color: rgb(var(--v-theme-primary));
  font-weight: 500;
}

:deep(.v-list-item:hover .v-list-item-title) {
  text-decoration: underline;
}

:deep(.v-list-item[disabled]) {
  opacity: 0.6;
  cursor: default;
}

:deep(.v-list-item[disabled]:hover) {
  background-color: transparent;
}

:deep(.v-list-item[disabled] .v-list-item-title) {
  color: inherit;
}
</style>

