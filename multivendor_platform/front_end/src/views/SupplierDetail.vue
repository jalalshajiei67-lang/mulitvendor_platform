<!-- src/views/SupplierDetail.vue - Supplier Detail Page -->
<template>
  <v-container fluid dir="rtl" class="supplier-detail-container">
    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-16">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <p class="text-h6 mt-4">در حال بارگذاری اطلاعات تامین‌کننده...</p>
      </v-col>
    </v-row>

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
      <v-breadcrumbs
        dir="rtl"
        :items="breadcrumbItems"
        class="px-4 py-2"
        divider="/"
      >
        <template v-slot:prepend>
          <v-icon size="small">mdi-home</v-icon>
        </template>
      </v-breadcrumbs>

      <!-- Header Section -->
      <v-card elevation="3" rounded="lg" class="mb-4 mb-md-6">
        <v-card-text class="pa-4 pa-md-6">
          <v-row align="center">
            <v-col cols="12" md="3" class="text-center">
              <v-avatar
                :size="display.xs.value ? 120 : 180"
                rounded="lg"
              >
                <v-img :src="getSupplierLogo(supplier)" cover></v-img>
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
                      ></v-img>
                      <v-card-text>
                        <h3 class="text-subtitle-1 font-weight-bold mb-2">{{ product.name }}</h3>
                        <div class="text-h6 text-primary font-weight-bold">${{ product.price }}</div>
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
                  <router-link to="/login" class="text-primary font-weight-bold">وارد شوید</router-link>
                  یا
                  <router-link to="/register" class="text-primary font-weight-bold">ثبت‌نام کنید</router-link>
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
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import config from '@/config'

export default {
  name: 'SupplierDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const display = useDisplay()
    const authStore = useAuthStore()

    const supplier = ref(null)
    const products = ref([])
    const comments = ref([])
    const loading = ref(false)
    const productsLoading = ref(false)
    const error = ref(null)
    const activeTab = ref('about')
    const commentSubmitting = ref(false)
    
    const newComment = ref({
      rating: 5,
      title: '',
      comment: ''
    })

    const breadcrumbItems = computed(() => [
      { title: 'خانه', to: '/', disabled: false },
      { title: 'تامین‌کنندگان', to: '/suppliers', disabled: false },
      { title: supplier.value?.store_name || 'جزئیات', disabled: true }
    ])

    const getSupplierLogo = (supplier) => {
      if (supplier.logo) {
        if (!supplier.logo.startsWith('http')) {
          return `${config.mediaUrl}${supplier.logo}`
        }
        return supplier.logo
      }
      return 'https://via.placeholder.com/250x250?text=No+Logo'
    }

    const getProductImage = (product) => {
      if (product.primary_image) {
        return product.primary_image
      }
      if (product.images && product.images.length > 0) {
        return product.images[0].image
      }
      return product.image || 'https://via.placeholder.com/250x250?text=No+Image'
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('fa-IR').format(date)
    }

    const fetchSupplier = async () => {
      loading.value = true
      error.value = null
      
      try {
        const supplierId = route.params.id
        const response = await axios.get(`${config.apiBaseUrl}/users/suppliers/${supplierId}/`)
        supplier.value = response.data
        
        // Fetch products and comments
        fetchProducts(supplierId)
        fetchComments(supplierId)
      } catch (err) {
        console.error('Error fetching supplier:', err)
        error.value = 'خطا در بارگذاری اطلاعات تامین‌کننده. لطفاً دوباره تلاش کنید.'
      } finally {
        loading.value = false
      }
    }

    const fetchProducts = async (supplierId) => {
      productsLoading.value = true
      try {
        const response = await axios.get(`${config.apiBaseUrl}/users/suppliers/${supplierId}/products/`)
        products.value = response.data
      } catch (err) {
        console.error('Error fetching products:', err)
      } finally {
        productsLoading.value = false
      }
    }

    const fetchComments = async (supplierId) => {
      try {
        const response = await axios.get(`${config.apiBaseUrl}/users/suppliers/${supplierId}/comments/`)
        comments.value = response.data
      } catch (err) {
        console.error('Error fetching comments:', err)
      }
    }

    const submitComment = async () => {
      if (!newComment.value.comment || newComment.value.rating < 1) {
        alert('لطفاً امتیاز و متن نظر را وارد کنید.')
        return
      }

      commentSubmitting.value = true
      
      try {
        const token = localStorage.getItem('token')
        const response = await axios.post(
          `${config.apiBaseUrl}/users/supplier-comments/`,
          {
            supplier: route.params.id,
            rating: newComment.value.rating,
            title: newComment.value.title,
            comment: newComment.value.comment
          },
          {
            headers: {
              'Authorization': `Token ${token}`
            }
          }
        )
        
        // Reset form
        newComment.value = {
          rating: 5,
          title: '',
          comment: ''
        }
        
        // Refresh comments
        await fetchComments(route.params.id)
        
        alert('نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده خواهد شد.')
      } catch (err) {
        console.error('Error submitting comment:', err)
        alert('خطا در ثبت نظر. لطفاً دوباره تلاش کنید.')
      } finally {
        commentSubmitting.value = false
      }
    }

    const goToProduct = (product) => {
      if (!product) return
      const slug = typeof product === 'object' ? product.slug : undefined
      const id = typeof product === 'object' ? product.id : product
      if (slug) {
        router.push(`/products/${slug}`)
      } else if (id) {
        router.push(`/products/${id}`)
      }
    }

    onMounted(() => {
      fetchSupplier()
    })

    return {
      supplier,
      products,
      comments,
      loading,
      productsLoading,
      error,
      activeTab,
      breadcrumbItems,
      display,
      authStore,
      newComment,
      commentSubmitting,
      getSupplierLogo,
      getProductImage,
      formatDate,
      fetchSupplier,
      submitComment,
      goToProduct
    }
  }
}
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

/* Medium.com-inspired spacing for content sections */
.content-section h1,
.content-section h2,
.content-section h3,
.content-section h4,
.content-section h5,
.content-section h6 {
  font-weight: 700;
  line-height: 1.3;
  color: rgba(var(--v-theme-on-surface), 0.96);
  margin-bottom: 0;
}

.content-section h1 {
  margin-top: 3rem;
  margin-bottom: 1.5rem;
}

.content-section h1:first-child {
  margin-top: 0;
}

.content-section h2 {
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
}

.content-section h3 {
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.content-section h4 {
  margin-top: 1.75rem;
  margin-bottom: 0.875rem;
}

.content-section p {
  line-height: 1.75;
  margin-top: 0;
  margin-bottom: 1.75rem;
}

/* First paragraph after heading */
.content-section h1 + p,
.content-section h2 + p,
.content-section h3 + p,
.content-section h4 + p {
  margin-top: 0.5rem;
}
</style>

