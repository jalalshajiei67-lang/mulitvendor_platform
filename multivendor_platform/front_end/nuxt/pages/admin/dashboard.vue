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
              <template v-slot:item.order_number="{ item }">
                <strong>{{ item.order_number }}</strong>
              </template>
              <template v-slot:item.buyer_info="{ item }">
                <div>
                  <div class="font-weight-bold">{{ item.first_name }} {{ item.last_name }}</div>
                  <div class="text-caption text-grey">{{ item.company_name }}</div>
                  <div class="text-caption text-grey">{{ item.phone_number }}</div>
                </div>
              </template>
              <template v-slot:item.product_name="{ item }">
                <div>
                  <div class="font-weight-bold">{{ item.product_name || 'نامشخص' }}</div>
                  <div v-if="item.category_name" class="text-caption text-grey">
                    دسته‌بندی: {{ item.category_name }}
                  </div>
                </div>
              </template>
              <template v-slot:item.images="{ item }">
                <div v-if="item.images && item.images.length > 0" class="d-flex gap-2">
                  <v-avatar
                    v-for="(img, idx) in item.images.slice(0, 3)"
                    :key="idx"
                    size="40"
                    @click="viewImage(img.image_url || img.image)"
                  >
                    <v-img :src="img.image_url || img.image" cover></v-img>
                  </v-avatar>
                  <v-chip v-if="item.images.length > 3" size="small" color="primary">
                    +{{ item.images.length - 3 }}
                  </v-chip>
                </div>
                <span v-else class="text-grey">بدون تصویر</span>
              </template>
              <template v-slot:item.status="{ item }">
                <v-chip size="small" :color="getRFQStatusColor(item.status)">
                  {{ getRFQStatusText(item.status) }}
                </v-chip>
              </template>
              <template v-slot:item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  @click="viewRFQDetail(item)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn icon size="small" variant="text" v-bind="props">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="updateRFQStatus(item, 'confirmed')">
                      <v-list-item-title>تأیید</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="updateRFQStatus(item, 'rejected')">
                      <v-list-item-title>رد</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="updateRFQStatus(item, 'processing')">
                      <v-list-item-title>در حال پردازش</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </div>

      <!-- RFQ Detail Dialog -->
      <v-dialog v-model="showRFQDetailDialog" max-width="900px" scrollable>
        <v-card v-if="selectedRFQ">
          <v-card-title class="d-flex justify-space-between align-center pa-4" style="background: rgb(var(--v-theme-primary)); color: white;">
            <div>
              <div class="text-h6">جزئیات درخواست استعلام قیمت</div>
              <div class="text-caption">{{ selectedRFQ.order_number }}</div>
            </div>
            <v-btn icon variant="text" color="white" @click="showRFQDetailDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text class="pa-6">
            <v-row>
              <!-- Buyer Information -->
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-account</v-icon>
                    اطلاعات خریدار
                  </div>
                  <v-list density="compact">
                    <v-list-item>
                      <v-list-item-title>نام و نام خانوادگی</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.first_name }} {{ selectedRFQ.last_name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>نام شرکت</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.company_name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>شماره تماس</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.phone_number }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedRFQ.buyer_username">
                      <v-list-item-title>نام کاربری</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.buyer_username }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>

              <!-- Order Information -->
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-information</v-icon>
                    اطلاعات درخواست
                  </div>
                  <v-list density="compact">
                    <v-list-item>
                      <v-list-item-title>وضعیت</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip size="small" :color="getRFQStatusColor(selectedRFQ.status)">
                          {{ getRFQStatusText(selectedRFQ.status) }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>تاریخ ایجاد</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDate(selectedRFQ.created_at) }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedRFQ.product_name">
                      <v-list-item-title>محصول</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.product_name }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item v-if="selectedRFQ.category_name">
                      <v-list-item-title>دسته‌بندی</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedRFQ.category_name }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>

              <!-- Description -->
              <v-col cols="12">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-text-box</v-icon>
                    نیازهای خاص
                  </div>
                  <p class="text-body-1">{{ selectedRFQ.unique_needs || 'توضیحی ارائه نشده است' }}</p>
                </v-card>
              </v-col>

              <!-- Images -->
              <v-col cols="12" v-if="selectedRFQ.images && selectedRFQ.images.length > 0">
                <v-card variant="outlined" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
                    <v-icon color="primary">mdi-image</v-icon>
                    تصاویر ({{ selectedRFQ.images.length }})
                  </div>
                  <v-row>
                    <v-col
                      v-for="(img, idx) in selectedRFQ.images"
                      :key="idx"
                      cols="6"
                      sm="4"
                      md="3"
                    >
                      <v-card
                        class="image-card"
                        @click="viewImage(img.image_url || img.image)"
                      >
                        <v-img
                          :src="img.image_url || img.image"
                          aspect-ratio="1"
                          cover
                          class="cursor-pointer"
                        >
                          <template v-slot:placeholder>
                            <div class="d-flex align-center justify-center fill-height">
                              <v-progress-circular
                                indeterminate
                                color="primary"
                              ></v-progress-circular>
                            </div>
                          </template>
                        </v-img>
                        <v-card-actions class="pa-2">
                          <v-btn
                            icon
                            size="small"
                            variant="text"
                            @click.stop="viewImage(img.image_url || img.image)"
                          >
                            <v-icon>mdi-magnify</v-icon>
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="showRFQDetailDialog = false">
              بستن
            </v-btn>
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn color="primary" v-bind="props">
                  تغییر وضعیت
                  <v-icon class="ms-2">mdi-menu-down</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="updateRFQStatus(selectedRFQ, 'confirmed')">
                  <v-list-item-title>تأیید</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateRFQStatus(selectedRFQ, 'rejected')">
                  <v-list-item-title>رد</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateRFQStatus(selectedRFQ, 'processing')">
                  <v-list-item-title>در حال پردازش</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-card-actions>
        </v-card>
      </v-dialog>
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
const showRFQDetailDialog = ref(false)
const selectedRFQ = ref<any>(null)
const loadingRFQDetail = ref(false)

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
  { title: 'اطلاعات خریدار', key: 'buyer_info' },
  { title: 'محصول', key: 'product_name' },
  { title: 'تصاویر', key: 'images' },
  { title: 'وضعیت', key: 'status' },
  { title: 'تاریخ', key: 'created_at' },
  { title: 'عملیات', key: 'actions' }
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
    console.log('Loaded RFQs:', rfqs.value)
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

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const viewRFQDetail = async (rfq: any) => {
  loadingRFQDetail.value = true
  try {
    // Fetch full details from API
    const detail = await adminApi.getRFQDetail(rfq.id)
    selectedRFQ.value = detail
    showRFQDetailDialog.value = true
  } catch (error) {
    console.error('Failed to load RFQ detail:', error)
    // Fallback to using the data we already have
    selectedRFQ.value = rfq
    showRFQDetailDialog.value = true
  } finally {
    loadingRFQDetail.value = false
  }
}

const viewImage = (imageUrl: string) => {
  // Open image in a new window or dialog
  window.open(imageUrl, '_blank')
}

const updateRFQStatus = async (rfq: any, newStatus: string) => {
  try {
    await adminApi.updateRFQStatus(rfq.id, newStatus)
    // Update the selected RFQ if dialog is open
    if (selectedRFQ.value && selectedRFQ.value.id === rfq.id) {
      selectedRFQ.value.status = newStatus
    }
    await loadRFQs()
    await loadDashboardData()
  } catch (error) {
    console.error('Failed to update RFQ status:', error)
  }
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

.image-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.image-card:hover {
  transform: scale(1.05);
}

.cursor-pointer {
  cursor: pointer;
}
</style>

