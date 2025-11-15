<template>
  <v-container fluid dir="rtl" class="supplier-detail-container">
    <!-- Loading State -->
    <SupplierDetailSkeleton v-if="loading" />

    <!-- Error State -->
    <v-alert
      v-else-if="error"
      type="error"
      variant="tonal"
      prominent
      class="my-4"
    >
      <v-row align="center">
        <v-col>
          <div class="text-h6">{{ error }}</div>
          <v-btn
            color="error"
            variant="text"
            prepend-icon="mdi-refresh"
            @click="fetchSupplier"
            class="mt-2"
          >
            تلاش مجدد
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Supplier Detail Content -->
    <div v-else-if="supplier">
      <!-- Breadcrumbs -->
      <Breadcrumb :items="breadcrumbItems" />

      <!-- Header Section -->
      <v-card elevation="3" rounded="lg" class="mb-4 mb-md-6">
        <v-card-text class="pa-4 pa-md-6">
          <v-row align="center">
            <v-col cols="12" md="3" class="text-center">
              <v-avatar
                :size="display.xs.value ? 120 : 180"
                rounded="lg"
              >
                <v-img
                  :src="getSupplierLogo(supplier)"
                  cover
                  loading="lazy"
                >
                  <template v-slot:placeholder>
                    <v-skeleton-loader type="avatar" />
                  </template>
                </v-img>
              </v-avatar>
            </v-col>
            <v-col cols="12" md="9">
              <h1 class="text-h4 text-sm-h3 font-weight-bold mb-2 readable-heading">
                {{ supplier.store_name }}
              </h1>
              <p v-if="supplier.user && (supplier.user.first_name || supplier.user.last_name)" class="text-subtitle-1 text-medium-emphasis mb-1 meta-text">
                <v-icon size="small" class="me-1">mdi-account</v-icon>
                مالک: {{ supplier.user.first_name }} {{ supplier.user.last_name }}
              </p>
              <p class="text-body-1 text-medium-emphasis mb-3 readable-text">
                {{ supplier.description }}
              </p>

              <v-row dense class="mb-3">
                <v-col cols="12" sm="6" md="4">
                  <v-chip prepend-icon="mdi-star" color="amber" variant="tonal">
                    امتیاز: {{ supplier.rating_average || 0 }}
                  </v-chip>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-chip prepend-icon="mdi-package-variant" color="primary" variant="tonal">
                    {{ supplier.product_count || 0 }} محصول
                  </v-chip>
                </v-col>
                <v-col cols="12" sm="6" md="4" v-if="supplier.created_at">
                  <v-chip prepend-icon="mdi-calendar" color="secondary" variant="tonal">
                    عضویت: {{ formatDate(supplier.created_at) }}
                  </v-chip>
                </v-col>
              </v-row>

              <!-- Contact Info -->
              <div class="contact-info">
                <v-chip
                  v-if="supplier.contact_email"
                  class="ma-1"
                  prepend-icon="mdi-email"
                  variant="outlined"
                  color="primary"
                >
                  {{ supplier.contact_email }}
                </v-chip>
                <v-chip
                  v-if="supplier.contact_phone"
                  class="ma-1"
                  prepend-icon="mdi-phone"
                  variant="outlined"
                  color="primary"
                >
                  {{ supplier.contact_phone }}
                </v-chip>
                <v-chip
                  v-if="supplier.website"
                  class="ma-1"
                  prepend-icon="mdi-web"
                  variant="outlined"
                  color="primary"
                  :href="supplier.website"
                  target="_blank"
                  link
                >
                  وب‌سایت
                </v-chip>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Tabs Section -->
      <v-card elevation="2" rounded="lg" class="mb-4">
        <v-tabs
          v-model="activeTab"
          bg-color="primary"
          color="white"
          align-tabs="center"
        >
          <v-tab value="projects">پروژه‌های موفق</v-tab>
          <v-tab value="resume">رزومه کاری</v-tab>
          <v-tab value="about">درباره</v-tab>
          <v-tab value="history">تاریخچه</v-tab>
          <v-tab value="products">محصولات</v-tab>
          <v-tab value="comments">نظرات ({{ comments.length }})</v-tab>
        </v-tabs>

        <v-card-text class="pa-4 pa-md-6">
          <v-window v-model="activeTab">
            <!-- About Tab -->
            <v-window-item value="about">
              <div class="content-section">
                <h2 class="text-h5 font-weight-bold mb-4 readable-heading">درباره {{ supplier.store_name }}</h2>

                <!-- User Profile Information -->
                <v-card v-if="supplier.user" elevation="0" color="grey-lighten-4" class="mb-4" rounded="lg">
                  <v-card-text class="pa-4">
                    <h3 class="text-subtitle-1 font-weight-bold mb-3">
                      <v-icon color="primary" class="me-1">mdi-account-circle</v-icon>
                      اطلاعات مالک
                    </h3>
                    <v-row dense>
                      <v-col cols="12" sm="6" md="4">
                        <div class="text-caption text-medium-emphasis">نام کاربری</div>
                        <div class="text-body-1 font-weight-medium">{{ supplier.user.username }}</div>
                      </v-col>
                      <v-col v-if="supplier.user.first_name || supplier.user.last_name" cols="12" sm="6" md="4">
                        <div class="text-caption text-medium-emphasis">نام و نام خانوادگی</div>
                        <div class="text-body-1 font-weight-medium">
                          {{ supplier.user.first_name }} {{ supplier.user.last_name }}
                        </div>
                      </v-col>
                      <v-col v-if="supplier.user.email" cols="12" sm="6" md="4">
                        <div class="text-caption text-medium-emphasis">ایمیل کاربری</div>
                        <div class="text-body-1 font-weight-medium">{{ supplier.user.email }}</div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>

                <!-- About Content -->
                <p class="text-body-1 description-text" style="white-space: pre-line;">
                  {{ supplier.about || 'اطلاعاتی در دسترس نیست.' }}
                </p>

                <!-- Address -->
                <div v-if="supplier.address" class="mt-4">
                  <h3 class="text-h6 font-weight-bold mb-2 readable-heading">
                    <v-icon color="primary">mdi-map-marker</v-icon>
                    آدرس
                  </h3>
                  <p class="text-body-1 readable-text">{{ supplier.address }}</p>
                </div>
              </div>
            </v-window-item>

            <!-- Work Resume Tab -->
            <v-window-item value="resume">
              <div class="content-section">
                <h2 class="text-h5 font-weight-bold mb-4 readable-heading">رزومه کاری</h2>
                <p class="text-body-1 description-text" style="white-space: pre-line;">
                  {{ supplier.work_resume || 'اطلاعاتی در دسترس نیست.' }}
                </p>
              </div>
            </v-window-item>

            <!-- Successful Projects Tab -->
            <v-window-item value="projects">
              <div class="content-section">
                <h2 class="text-h5 font-weight-bold mb-4 readable-heading">پروژه‌های موفق</h2>
                <p class="text-body-1 description-text" style="white-space: pre-line;">
                  {{ supplier.successful_projects || 'اطلاعاتی در دسترس نیست.' }}
                </p>
              </div>
            </v-window-item>

            <!-- History Tab -->
            <v-window-item value="history">
              <div class="content-section">
                <h2 class="text-h5 font-weight-bold mb-4 readable-heading">تاریخچه</h2>
                <p class="text-body-1 description-text" style="white-space: pre-line;">
                  {{ supplier.history || 'اطلاعاتی در دسترس نیست.' }}
                </p>
              </div>
            </v-window-item>

            <!-- Products Tab -->
            <v-window-item value="products">
              <div class="content-section">
                <h2 class="text-h5 font-weight-bold mb-4 readable-heading">محصولات</h2>

                <!-- Products Loading -->
                <v-row v-if="productsLoading" justify="center" class="my-8">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </v-row>

                <!-- Products Grid -->
                <v-row v-else-if="products.length > 0">
                  <v-col
                    v-for="product in products"
                    :key="product.id"
                    cols="12"
                    sm="6"
                    md="4"
                    lg="3"
                  >
                    <v-card
                      elevation="2"
                      rounded="lg"
                      hover
                      @click="goToProduct(product)"
                      class="cursor-pointer"
                    >
                      <v-img
                        :src="getProductImage(product)"
                        height="200"
                        cover
                        loading="lazy"
                      >
                        <template v-slot:placeholder>
                          <div class="d-flex align-center justify-center fill-height">
                            <v-skeleton-loader type="image" width="100%" height="100%" />
                          </div>
                        </template>
                      </v-img>
                      <v-card-text>
                        <h3 class="text-subtitle-1 font-weight-bold mb-2">{{ product.name }}</h3>
                        <div class="text-h6 text-primary font-weight-bold">{{ formatPrice(product.price) }} تومان</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- Empty Products -->
                <v-alert v-else type="info" variant="tonal">
                  محصولی برای این تامین‌کننده موجود نیست.
                </v-alert>
              </div>
            </v-window-item>

            <!-- Comments Tab -->
            <v-window-item value="comments">
              <div class="content-section">
                <h2 class="text-h5 font-weight-bold mb-4 readable-heading">نظرات کاربران</h2>

                <!-- Comment Form -->
                <v-card elevation="1" rounded="lg" class="mb-6" v-if="authStore.isAuthenticated">
                  <v-card-title class="bg-primary">
                    <span class="text-white">ثبت نظر جدید</span>
                  </v-card-title>
                  <v-card-text class="pa-4">
                    <v-form @submit.prevent="submitComment">
                      <v-row>
                        <v-col cols="12">
                          <v-rating
                            v-model="newComment.rating"
                            color="amber"
                            half-increments
                            hover
                            length="5"
                            size="large"
                          >
                            <template v-slot:item-label="{ index }">
                              {{ index + 1 }}
                            </template>
                          </v-rating>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field
                            v-model="newComment.title"
                            label="عنوان نظر"
                            variant="outlined"
                            rounded="lg"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-textarea
                            v-model="newComment.comment"
                            label="متن نظر"
                            variant="outlined"
                            rounded="lg"
                            rows="4"
                            required
                          ></v-textarea>
                        </v-col>
                        <v-col cols="12">
                          <v-btn
                            type="submit"
                            color="primary"
                            size="large"
                            prepend-icon="mdi-send"
                            :loading="commentSubmitting"
                            rounded="lg"
                          >
                            ثبت نظر
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-form>
                  </v-card-text>
                </v-card>

                <!-- Login prompt for guests -->
                <v-alert v-else type="info" variant="tonal" class="mb-6">
                  برای ثبت نظر لطفاً
                  <NuxtLink to="/login" class="text-primary font-weight-bold">وارد شوید</NuxtLink>
                  یا
                  <NuxtLink to="/register" class="text-primary font-weight-bold">ثبت‌نام کنید</NuxtLink>
                </v-alert>

                <!-- Comments List -->
                <v-row v-if="comments.length > 0">
                  <v-col
                    v-for="comment in comments"
                    :key="comment.id"
                    cols="12"
                  >
                    <v-card elevation="2" rounded="lg" class="mb-3">
                      <v-card-text>
                        <div class="d-flex justify-space-between align-start mb-2">
                          <div>
                            <div class="d-flex align-center mb-1">
                              <v-avatar size="32" color="primary" class="me-2">
                                <span class="text-white text-caption">
                                  {{ comment.user_username?.charAt(0)?.toUpperCase() }}
                                </span>
                              </v-avatar>
                              <div>
                                <div class="font-weight-bold">{{ comment.user_username }}</div>
                                <div class="text-caption text-medium-emphasis">
                                  {{ formatDate(comment.created_at) }}
                                </div>
                              </div>
                            </div>
                          </div>
                          <v-rating
                            :model-value="comment.rating"
                            color="amber"
                            density="compact"
                            readonly
                            size="small"
                          ></v-rating>
                        </div>

                        <h4 v-if="comment.title" class="text-subtitle-1 font-weight-bold mb-2 readable-heading">
                          {{ comment.title }}
                        </h4>
                        <p class="text-body-2 comment-text">{{ comment.comment }}</p>

                        <!-- Supplier Reply -->
                        <v-alert
                          v-if="comment.supplier_reply"
                          type="success"
                          variant="tonal"
                          density="compact"
                          class="mt-3"
                        >
                          <div class="text-caption font-weight-bold mb-1">پاسخ تامین‌کننده:</div>
                          <div class="text-body-2">{{ comment.supplier_reply }}</div>
                        </v-alert>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- No Comments -->
                <v-alert v-else type="info" variant="tonal">
                  هنوز نظری برای این تامین‌کننده ثبت نشده است. اولین نظر را شما بنویسید!
                </v-alert>
              </div>
            </v-window-item>
          </v-window>
        </v-card-text>
      </v-card>
    </div>
  </v-container>

  <!-- Success Snackbar -->
  <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
    {{ snackbarMessage }}
  </v-snackbar>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '~/stores/auth'
import { useSupplierApi, type Supplier, type SupplierComment } from '~/composables/useSupplierApi'
import { formatImageUrl } from '~/utils/imageUtils'

const route = useRoute()
const display = useDisplay()
const authStore = useAuthStore()
const supplierApi = useSupplierApi()

const supplier = ref<Supplier | null>(null)
const products = ref<any[]>([])
const comments = ref<SupplierComment[]>([])
const loading = ref(false)
const productsLoading = ref(false)
const error = ref<string | null>(null)
const activeTab = ref('about')
const commentSubmitting = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const newComment = ref({
  rating: 5,
  title: '',
  comment: ''
})

const breadcrumbItems = computed(() => [
  { text: 'خانه', to: '/' },
  { text: 'تامین‌کنندگان', to: '/suppliers' },
  { text: supplier.value?.store_name || 'جزئیات', to: null }
])

const getSupplierLogo = (supplier: Supplier) => {
  if (supplier.logo) {
    const formattedUrl = formatImageUrl(supplier.logo)
    if (formattedUrl) return formattedUrl
  }
  return 'https://via.placeholder.com/250x250?text=No+Logo'
}

const getProductImage = (product: any) => {
  if (product.primary_image) {
    return formatImageUrl(product.primary_image) || product.primary_image
  }
  if (product.images && product.images.length > 0) {
    return formatImageUrl(product.images[0].image) || product.images[0].image
  }
  return formatImageUrl(product.image) || product.image || 'https://via.placeholder.com/250x250?text=No+Image'
}

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const formatPrice = (price: number | string) => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('fa-IR').format(numPrice)
}

const fetchSupplier = async () => {
  loading.value = true
  error.value = null

  try {
    const supplierId = route.params.id as string
    const response = await supplierApi.getSupplier(supplierId)
    supplier.value = response

    // Fetch products and comments
    fetchProducts(supplierId)
    fetchComments(supplierId)

    // Set page title
    useHead({
      title: supplier.value.store_name,
      meta: [
        {
          name: 'description',
          content: supplier.value.description || ''
        }
      ]
    })
  } catch (err: any) {
    console.error('Error fetching supplier:', err)
    error.value = 'خطا در بارگذاری اطلاعات تامین‌کننده. لطفاً دوباره تلاش کنید.'
  } finally {
    loading.value = false
  }
}

const fetchProducts = async (supplierId: string) => {
  productsLoading.value = true
  try {
    const response = await supplierApi.getSupplierProducts(supplierId)
    products.value = response
  } catch (err) {
    console.error('Error fetching products:', err)
  } finally {
    productsLoading.value = false
  }
}

const fetchComments = async (supplierId: string) => {
  try {
    const response = await supplierApi.getSupplierComments(supplierId)
    comments.value = response
  } catch (err) {
    console.error('Error fetching comments:', err)
  }
}

const submitComment = async () => {
  if (!newComment.value.comment || newComment.value.rating < 1) {
    showSnackbar('لطفاً امتیاز و متن نظر را وارد کنید.', 'error')
    return
  }

  commentSubmitting.value = true

  try {
    const supplierId = route.params.id as string
    await supplierApi.createSupplierComment(supplierId, {
      rating: newComment.value.rating,
      title: newComment.value.title || undefined,
      comment: newComment.value.comment
    })

    // Reset form
    newComment.value = {
      rating: 5,
      title: '',
      comment: ''
    }

    // Refresh comments
    await fetchComments(supplierId)

    showSnackbar('نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده خواهد شد.', 'success')
  } catch (err: any) {
    console.error('Error submitting comment:', err)
    showSnackbar('خطا در ثبت نظر. لطفاً دوباره تلاش کنید.', 'error')
  } finally {
    commentSubmitting.value = false
  }
}

const goToProduct = (product: any) => {
  if (!product) return
  const slug = product.slug
  const id = product.id
  if (slug) {
    navigateTo(`/products/${slug}`)
  } else if (id) {
    navigateTo(`/products/${id}`)
  }
}

const showSnackbar = (message: string, color = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

onMounted(() => {
  fetchSupplier()
})
</script>

<style scoped>
.supplier-detail-container {
  max-width: 100%;
  padding-left: 16px;
  padding-right: 16px;
}

@media (min-width: 960px) {
  .supplier-detail-container {
    max-width: 100%;
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (min-width: 1280px) {
  .supplier-detail-container {
    max-width: 1400px;
    margin: 0 auto;
    padding-left: 32px;
    padding-right: 32px;
  }
}

.content-section {
  min-height: 300px;
}

.cursor-pointer {
  cursor: pointer;
}

.contact-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* Typography improvements */
.readable-heading {
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: rgba(var(--v-theme-on-surface), 0.96);
}

.readable-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.meta-text {
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.72);
  font-size: 0.875rem;
}

.description-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
  white-space: pre-line;
}

.comment-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.content-section h2 {
  line-height: 1.4;
  margin-bottom: 1.5rem;
}

.content-section p {
  line-height: 1.75;
}
</style>

