<template>
  <div dir="rtl" class="admin-dashboard-wrapper">
    <v-container fluid class="pa-4">
      <!-- Dashboard View -->
      <div v-if="activeView === 'dashboard'" class="dashboard-view">
        <!-- Stats Cards -->
        <v-row class="mb-6">
          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" elevation="0" variant="outlined">
              <v-card-text class="pa-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <v-icon color="primary" size="32">mdi-account-group</v-icon>
                </div>
                <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.users?.total || 0 }}</div>
                <div class="text-body-2 text-grey">کل کاربران</div>
                <div class="text-caption text-grey mt-2">
                  خریدار: {{ dashboardData.users?.buyers || 0 }} | فروشنده: {{ dashboardData.users?.sellers || 0 }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" elevation="0" variant="outlined">
              <v-card-text class="pa-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <v-icon color="success" size="32">mdi-package-variant</v-icon>
                </div>
                <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.products?.total || 0 }}</div>
                <div class="text-body-2 text-grey">کل محصولات</div>
                <div class="text-caption text-grey mt-2">
                  فعال: {{ dashboardData.products?.active || 0 }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" elevation="0" variant="outlined">
              <v-card-text class="pa-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <v-icon color="info" size="32">mdi-cart</v-icon>
                </div>
                <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.orders?.total || 0 }}</div>
                <div class="text-body-2 text-grey">کل سفارشات</div>
                <div class="text-caption text-grey mt-2">
                  در انتظار: {{ dashboardData.orders?.pending || 0 }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-card class="stat-card" elevation="0" variant="outlined">
              <v-card-text class="pa-4">
                <div class="d-flex align-center justify-space-between mb-2">
                  <v-icon color="purple" size="32">mdi-file-document-edit-outline</v-icon>
                </div>
                <div class="text-h4 font-weight-bold mb-1">{{ dashboardData.rfqs?.total || 0 }}</div>
                <div class="text-body-2 text-grey">درخواست‌های استعلام قیمت</div>
                <div class="text-caption text-grey mt-2">
                  در انتظار: {{ dashboardData.rfqs?.pending || 0 }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <!-- Users Management View -->
      <div v-if="activeView === 'users'" class="users-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">لیست کاربران</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="userHeaders"
              :items="users"
              :loading="loadingUsers"
              item-value="id"
            >
              <template v-slot:item.username="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" class="mr-2">
                    <v-icon>mdi-account</v-icon>
                  </v-avatar>
                  <strong>{{ item.username }}</strong>
                </div>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn size="small" variant="text" @click="toggleBlockUser(item)">
                  {{ item.profile?.is_blocked ? 'رفع مسدودی' : 'مسدود' }}
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- Products Management View -->
      <div v-if="activeView === 'products'" class="products-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">لیست محصولات</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="productHeaders"
              :items="products"
              :loading="loadingProducts"
              item-value="id"
            >
              <template v-slot:item.name="{ item }">
                <strong>{{ item.name }}</strong>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn size="small" variant="text" @click="deleteProduct(item)">
                  حذف
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- Departments Management View -->
      <div v-if="activeView === 'departments'" class="departments-view">
        <AdminDepartmentManagement />
      </div>

      <!-- Categories Management View -->
      <div v-if="activeView === 'categories'" class="categories-view">
        <AdminCategoryManagement />
      </div>

      <!-- Subcategories Management View -->
      <div v-if="activeView === 'subcategories'" class="subcategories-view">
        <AdminSubcategoryManagement />
      </div>

      <!-- Activities View -->
      <div v-if="activeView === 'activities'" class="activities-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">گزارش فعالیت‌ها</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="activityHeaders"
              :items="activities"
              :loading="loadingActivities"
              item-value="id"
            >
              <template v-slot:item.user_username="{ item }">
                {{ item.user_username || 'نامشخص' }}
              </template>
              <template v-slot:item.action="{ item }">
                <v-chip size="small">{{ item.action_display }}</v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- Blog Management View -->
      <div v-if="activeView === 'blog'" class="blog-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">لیست پست‌های وبلاگ</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="blogHeaders"
              :items="blogPosts"
              :loading="loadingBlog"
              item-value="id"
            >
              <template v-slot:item.title="{ item }">
                <strong>{{ item.title }}</strong>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn size="small" variant="text" :to="`/admin/dashboard/blog/${item.slug}/edit`">
                  ویرایش
                </v-btn>
                <v-btn size="small" variant="text" color="error" @click="deleteBlogPost(item)">
                  حذف
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- RFQs View -->
      <div v-if="activeView === 'rfqs'" class="rfqs-view">
        <v-card elevation="0" variant="outlined">
          <v-card-title class="pa-4">درخواست‌های استعلام قیمت</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-data-table
              :headers="rfqHeaders"
              :items="rfqs"
              :loading="loadingRFQs"
              item-value="id"
            >
              <template v-slot:item.status="{ item }">
                <v-chip size="small" :color="getRFQStatusColor(item.status)">
                  {{ getRFQStatusText(item.status) }}
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>
    </v-container>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const adminApi = useAdminApi()

const activeView = ref((route.query.view as string) || 'dashboard')
const dashboardData = ref<any>({})
const users = ref<any[]>([])
const products = ref<any[]>([])
const activities = ref<any[]>([])
const blogPosts = ref<any[]>([])
const rfqs = ref<any[]>([])

const loading = ref(false)
const loadingUsers = ref(false)
const loadingProducts = ref(false)
const loadingActivities = ref(false)
const loadingBlog = ref(false)
const loadingRFQs = ref(false)

const userHeaders = [
  { title: 'نام کاربری', key: 'username' },
  { title: 'ایمیل', key: 'email' },
  { title: 'نقش', key: 'role' },
  { title: 'عملیات', key: 'actions' }
]

const productHeaders = [
  { title: 'نام', key: 'name' },
  { title: 'قیمت', key: 'price' },
  { title: 'وضعیت', key: 'is_active' },
  { title: 'عملیات', key: 'actions' }
]

const activityHeaders = [
  { title: 'کاربر', key: 'user_username' },
  { title: 'عملیات', key: 'action' },
  { title: 'تاریخ', key: 'created_at' }
]

const blogHeaders = [
  { title: 'عنوان', key: 'title' },
  { title: 'وضعیت', key: 'status' },
  { title: 'تاریخ', key: 'created_at' },
  { title: 'عملیات', key: 'actions' }
]

const rfqHeaders = [
  { title: 'شماره درخواست', key: 'order_number' },
  { title: 'نام', key: 'first_name' },
  { title: 'وضعیت', key: 'status' }
]

const loadDashboardData = async () => {
  loading.value = true
  try {
    const data = await adminApi.getDashboard()
    dashboardData.value = data
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  loadingUsers.value = true
  try {
    const data = await adminApi.getUsers()
    users.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load users:', error)
  } finally {
    loadingUsers.value = false
  }
}

const loadProducts = async () => {
  loadingProducts.value = true
  try {
    const data = await adminApi.getAdminProducts()
    products.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load products:', error)
  } finally {
    loadingProducts.value = false
  }
}

const loadActivities = async () => {
  loadingActivities.value = true
  try {
    const data = await adminApi.getActivities()
    activities.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load activities:', error)
  } finally {
    loadingActivities.value = false
  }
}

const loadBlogPosts = async () => {
  loadingBlog.value = true
  try {
    const data = await adminApi.getAdminBlogPosts()
    blogPosts.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load blog posts:', error)
  } finally {
    loadingBlog.value = false
  }
}

const loadRFQs = async () => {
  loadingRFQs.value = true
  try {
    const data = await adminApi.getRFQs()
    rfqs.value = Array.isArray(data) ? data : data.results || []
  } catch (error) {
    console.error('Failed to load RFQs:', error)
  } finally {
    loadingRFQs.value = false
  }
}

const toggleBlockUser = async (user: any) => {
  try {
    await adminApi.blockUser(user.id, !user.profile?.is_blocked)
    await loadUsers()
  } catch (error) {
    console.error('Failed to toggle block user:', error)
  }
}

const deleteProduct = async (product: any) => {
  if (confirm(`آیا مطمئن هستید که می‌خواهید محصول "${product.name}" را حذف کنید؟`)) {
    try {
      await adminApi.deleteProduct(product.id)
      await loadProducts()
    } catch (error) {
      console.error('Failed to delete product:', error)
    }
  }
}

const deleteBlogPost = async (post: any) => {
  if (confirm(`آیا مطمئن هستید که می‌خواهید پست "${post.title}" را حذف کنید؟`)) {
    try {
      await adminApi.deleteBlogPost(post.slug)
      await loadBlogPosts()
    } catch (error) {
      console.error('Failed to delete blog post:', error)
    }
  }
}

const getRFQStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'warning',
    confirmed: 'success',
    rejected: 'error',
    processing: 'info'
  }
  return colors[status] || 'grey'
}

const getRFQStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: 'در انتظار',
    confirmed: 'تأیید شده',
    rejected: 'رد شده',
    processing: 'در حال پردازش'
  }
  return texts[status] || status
}

const handleNavigate = (view: string) => {
  activeView.value = view
  navigateTo({
    path: '/admin/dashboard',
    query: { view }
  })
}

watch(activeView, (newView) => {
  if (newView === 'dashboard') {
    loadDashboardData()
  } else if (newView === 'users') {
    loadUsers()
  } else if (newView === 'products') {
    loadProducts()
  } else if (newView === 'activities') {
    loadActivities()
  } else if (newView === 'blog') {
    loadBlogPosts()
  } else if (newView === 'rfqs') {
    loadRFQs()
  }
})

watch(() => route.query.view, (newView) => {
  if (typeof newView === 'string') {
    activeView.value = newView
  }
})

onMounted(() => {
  if (activeView.value === 'dashboard') {
    loadDashboardData()
  }
})
</script>

<style scoped>
.admin-dashboard-wrapper {
  min-height: 100vh;
}

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
}
</style>

