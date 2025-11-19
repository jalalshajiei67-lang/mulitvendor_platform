<template>
  <div class="supplier-mini-website" dir="rtl" :style="brandingStyles">
    <!-- Enhanced Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-content">
        <div class="loading-spinner">
          <v-progress-circular
            indeterminate
            color="primary"
            size="80"
            width="6"
            class="main-spinner"
          ></v-progress-circular>
          <div class="spinner-ring"></div>
        </div>
        <div class="loading-text">
          <h3 class="text-h6 font-weight-bold mb-2">در حال بارگذاری...</h3>
          <p class="text-body-2 text-medium-emphasis">لطفاً کمی صبر کنید</p>
        </div>
      </div>
    </div>

    <!-- Enhanced Error State -->
    <div v-else-if="error" class="error-container animate-in">
      <v-card elevation="8" class="error-card glass-card">
        <v-card-text class="text-center pa-8">
          <div class="error-icon mb-4">
            <v-icon size="80" color="error" class="error-main-icon">mdi-alert-circle</v-icon>
            <div class="error-particles">
              <span class="particle"></span>
              <span class="particle"></span>
              <span class="particle"></span>
            </div>
          </div>
          <h3 class="text-h5 font-weight-bold mb-2 text-error">خطا در بارگذاری</h3>
          <p class="text-body-1 text-medium-emphasis mb-6">{{ error }}</p>
          <v-btn
            color="primary"
            size="large"
            prepend-icon="mdi-refresh"
            @click="fetchSupplier"
            class="retry-btn"
            elevation="4"
          >
            تلاش مجدد
          </v-btn>
        </v-card-text>
      </v-card>
    </div>

    <!-- Supplier Mini Website Content -->
    <div v-else-if="supplier">
      <!-- Hero Section -->
      <SupplierHero
        :supplier="supplier"
        @contact-click="scrollToContact"
      />

      <!-- Navigation Tabs -->
      <div class="tabs-container">
        <v-container>
          <!-- Mobile Tab Selector -->
          <div class="mobile-tab-selector d-md-none">
            <v-select
              v-model="activeTab"
              :items="mobileTabItems"
              variant="outlined"
              density="comfortable"
              class="mobile-tabs-select"
              prepend-inner-icon="mdi-menu"
              bg-color="rgba(255, 255, 255, 0.9)"
              hide-details
            >
              <template v-slot:selection="{ item }">
                <div class="d-flex align-center">
                  <v-icon :color="item.raw.color" class="me-2">{{ item.raw.icon }}</v-icon>
                  <span>{{ item.title }}</span>
                  <v-badge
                    v-if="item.raw.badge"
                    :content="item.raw.badge"
                    :color="item.raw.badgeColor"
                    class="ms-2"
                  ></v-badge>
                </div>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props">
                  <template v-slot:prepend>
                    <v-icon :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                  </template>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                  <template v-slot:append>
                    <v-badge
                      v-if="item.raw.badge"
                      :content="item.raw.badge"
                      :color="item.raw.badgeColor"
                    ></v-badge>
                  </template>
                </v-list-item>
              </template>
            </v-select>
          </div>

          <!-- Desktop Tabs -->
          <v-tabs
            v-model="activeTab"
            :bg-color="supplier.brand_color_primary || 'primary'"
            color="white"
            align-tabs="center"
            show-arrows
            class="mini-website-tabs d-none d-md-flex"
            height="70"
          >
            <v-tab value="overview" class="modern-tab">
              <template v-slot:default>
                <div class="tab-content-wrapper">
                  <v-icon size="large" class="tab-icon">mdi-information</v-icon>
                  <span class="tab-text">معرفی</span>
                  <div class="tab-indicator"></div>
                </div>
              </template>
            </v-tab>
            <v-tab value="products" v-if="products.length > 0" class="modern-tab">
              <template v-slot:default>
                <div class="tab-content-wrapper">
                  <v-icon size="large" class="tab-icon">mdi-package-variant</v-icon>
                  <span class="tab-text">محصولات</span>
                  <v-badge :content="products.length" color="white" text-color="primary" class="tab-badge"></v-badge>
                  <div class="tab-indicator"></div>
                </div>
              </template>
            </v-tab>
            <v-tab value="portfolio" v-if="portfolioItems.length > 0" class="modern-tab">
              <template v-slot:default>
                <div class="tab-content-wrapper">
                  <v-icon size="large" class="tab-icon">mdi-briefcase</v-icon>
                  <span class="tab-text">نمونه کارها</span>
                  <div class="tab-indicator"></div>
                </div>
              </template>
            </v-tab>
            <v-tab value="team" v-if="teamMembers.length > 0" class="modern-tab">
              <template v-slot:default>
                <div class="tab-content-wrapper">
                  <v-icon size="large" class="tab-icon">mdi-account-group</v-icon>
                  <span class="tab-text">تیم ما</span>
                  <div class="tab-indicator"></div>
                </div>
              </template>
            </v-tab>
            <v-tab value="certifications" v-if="hasCertifications" class="modern-tab">
              <template v-slot:default>
                <div class="tab-content-wrapper">
                  <v-icon size="large" class="tab-icon">mdi-certificate</v-icon>
                  <span class="tab-text">گواهینامه‌ها</span>
                  <div class="tab-indicator"></div>
                </div>
              </template>
            </v-tab>
            <v-tab value="reviews" v-if="comments.length > 0" class="modern-tab">
              <template v-slot:default>
                <div class="tab-content-wrapper">
                  <v-icon size="large" class="tab-icon">mdi-star</v-icon>
                  <span class="tab-text">نظرات</span>
                  <v-badge :content="comments.length" color="white" text-color="primary" class="tab-badge"></v-badge>
                  <div class="tab-indicator"></div>
                </div>
              </template>
            </v-tab>
            <v-tab value="contact" class="modern-tab contact-tab">
              <template v-slot:default>
                <div class="tab-content-wrapper">
                  <v-icon size="large" class="tab-icon">mdi-email</v-icon>
                  <span class="tab-text">تماس با ما</span>
                  <v-icon class="contact-pulse" size="small">mdi-circle</v-icon>
                  <div class="tab-indicator"></div>
                </div>
              </template>
            </v-tab>
          </v-tabs>

          <!-- Progress Bar -->
          <div class="tab-progress-container d-none d-md-block">
            <div class="tab-progress-bar">
              <div
                class="tab-progress-fill"
                :style="{ width: progressWidth + '%' }"
              ></div>
            </div>
            <div class="progress-dots">
              <span
                v-for="(tab, index) in availableTabs"
                :key="tab.value"
                class="progress-dot"
                :class="{ active: index <= currentTabIndex, completed: index < currentTabIndex }"
                @click="activeTab = tab.value"
              ></span>
            </div>
          </div>
        </v-container>
      </div>

      <!-- Tab Content -->
      <v-window v-model="activeTab" class="tab-content">
        <!-- Overview Tab -->
        <v-window-item value="overview">
          <v-container class="py-6 py-md-8">
            <v-row>
              <v-col cols="12" md="8">
                <v-card elevation="2" class="mb-4 overview-card" rounded="lg">
                  <v-card-title class="text-h5 font-weight-bold readable-heading pa-6">
                    <div class="title-wrapper">
                      <v-icon color="primary" size="large" class="me-3">mdi-information</v-icon>
                      <span>درباره {{ supplier.store_name }}</span>
                    </div>
                  </v-card-title>
                  <v-card-text class="pa-6">
                    <div class="content-body">
                      <p class="readable-text" style="white-space: pre-line;">
                        {{ supplier.about || supplier.description || 'اطلاعاتی در دسترس نیست.' }}
                      </p>
                    </div>
                  </v-card-text>
                </v-card>

                <v-card v-if="supplier.work_resume" elevation="2" class="mb-4 overview-card" rounded="lg">
                  <v-card-title class="text-h6 font-weight-bold readable-heading pa-6">
                    <div class="title-wrapper">
                      <v-icon color="primary" size="large" class="me-3">mdi-file-document</v-icon>
                      <span>رزومه کاری</span>
                    </div>
                  </v-card-title>
                  <v-card-text class="pa-6">
                    <div class="content-body">
                      <p class="readable-text" style="white-space: pre-line;">
                        {{ supplier.work_resume }}
                      </p>
                    </div>
                  </v-card-text>
                </v-card>

                <v-card v-if="supplier.history" elevation="2" class="mb-4 overview-card" rounded="lg">
                  <v-card-title class="text-h6 font-weight-bold readable-heading pa-6">
                    <div class="title-wrapper">
                      <v-icon color="primary" size="large" class="me-3">mdi-history</v-icon>
                      <span>تاریخچه</span>
                    </div>
                  </v-card-title>
                  <v-card-text class="pa-6">
                    <div class="content-body">
                      <p class="readable-text" style="white-space: pre-line;">
                        {{ supplier.history }}
                      </p>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" md="4">
                <v-card elevation="4" class="sticky-sidebar contact-quick-card" rounded="lg">
                  <v-card-title class="text-h6 font-weight-bold pa-6">
                    <div class="title-wrapper">
                      <v-icon color="primary" size="large" class="me-3">mdi-contact-mail</v-icon>
                      <span>اطلاعات تماس سریع</span>
                    </div>
                  </v-card-title>
                  <v-list class="pa-2">
                    <v-list-item 
                      v-if="supplier.contact_email" 
                      prepend-icon="mdi-email"
                      class="contact-quick-item"
                      @click="copyToClipboard(supplier.contact_email)"
                    >
                      <v-list-item-title class="text-body-1">{{ supplier.contact_email }}</v-list-item-title>
                      <template v-slot:append>
                        <v-btn icon="mdi-content-copy" size="small" variant="text" color="primary"></v-btn>
                      </template>
                    </v-list-item>
                    <v-list-item 
                      v-if="supplier.contact_phone" 
                      prepend-icon="mdi-phone"
                      class="contact-quick-item"
                      :href="`tel:${supplier.contact_phone}`"
                    >
                      <v-list-item-title class="text-body-1">{{ supplier.contact_phone }}</v-list-item-title>
                      <template v-slot:append>
                        <v-btn icon="mdi-phone-in-talk" size="small" variant="text" color="success"></v-btn>
                      </template>
                    </v-list-item>
                    <v-list-item 
                      v-if="supplier.address" 
                      prepend-icon="mdi-map-marker"
                      class="contact-quick-item"
                      @click="copyToClipboard(supplier.address)"
                    >
                      <v-list-item-title class="text-body-1">{{ supplier.address }}</v-list-item-title>
                      <template v-slot:append>
                        <v-btn icon="mdi-content-copy" size="small" variant="text" color="info"></v-btn>
                      </template>
                    </v-list-item>
                  </v-list>
                  <v-divider class="mx-4"></v-divider>
                  <v-card-actions class="pa-4">
                    <v-btn 
                      block 
                      color="primary" 
                      size="large"
                      prepend-icon="mdi-email" 
                      @click="activeTab = 'contact'"
                      class="contact-cta-btn"
                    >
                      ارسال پیام
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>

        <!-- Products Tab -->
        <v-window-item value="products">
          <SupplierProductCatalog
            :products="products"
            :loading="productsLoading"
            @add-to-cart="handleAddToCart"
          />
        </v-window-item>

        <!-- Portfolio Tab -->
        <v-window-item value="portfolio">
          <SupplierPortfolio
            :items="portfolioItems"
            :loading="portfolioLoading"
          />
        </v-window-item>

        <!-- Team Tab -->
        <v-window-item value="team">
          <SupplierTeam
            :members="teamMembers"
            :loading="teamLoading"
          />
        </v-window-item>

        <!-- Certifications Tab -->
        <v-window-item value="certifications">
          <SupplierCertifications
            :certifications="supplier.certifications"
            :awards="supplier.awards"
          />
        </v-window-item>

        <!-- Reviews Tab -->
        <v-window-item value="reviews">
          <v-container class="py-6 py-md-8">
            <div class="section-header mb-8">
              <h2 class="text-h4 font-weight-bold mb-2">نظرات مشتریان</h2>
              <p class="text-body-1 text-medium-emphasis">
                تجربه مشتریان ما از خدمات و محصولات
              </p>
            </div>
            
            <v-row v-if="comments.length > 0" class="reviews-grid">
              <v-col
                v-for="comment in comments"
                :key="comment.id"
                cols="12"
                md="6"
              >
                <v-card elevation="3" class="comment-card" rounded="lg">
                  <v-card-text class="pa-6">
                    <div class="d-flex justify-space-between align-start mb-4">
                      <div class="d-flex align-center flex-grow-1">
                        <v-avatar size="48" color="primary" class="me-3 comment-avatar">
                          <span class="text-white text-h6 font-weight-bold">{{ comment.user_username.charAt(0).toUpperCase() }}</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <div class="font-weight-bold text-h6 mb-1">{{ comment.user_username }}</div>
                          <div class="text-caption text-medium-emphasis d-flex align-center">
                            <v-icon size="x-small" class="me-1">mdi-calendar</v-icon>
                            {{ formatDate(comment.created_at) }}
                          </div>
                        </div>
                      </div>
                      <v-rating
                        :model-value="comment.rating"
                        readonly
                        density="compact"
                        color="amber"
                        size="small"
                        class="rating-badge"
                      ></v-rating>
                    </div>
                    <h4 v-if="comment.title" class="text-h6 font-weight-bold mb-3 comment-title">{{ comment.title }}</h4>
                    <p class="text-body-1 comment-text mb-4">{{ comment.comment }}</p>
                    <v-divider v-if="comment.supplier_reply" class="my-4"></v-divider>
                    <div v-if="comment.supplier_reply" class="supplier-reply">
                      <div class="d-flex align-center mb-2">
                        <v-icon size="small" color="primary" class="me-2">mdi-store</v-icon>
                        <span class="text-subtitle-2 font-weight-bold text-primary">پاسخ فروشنده</span>
                      </div>
                      <p class="text-body-1">{{ comment.supplier_reply }}</p>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <v-row v-else justify="center" class="my-8">
              <v-col cols="12" class="text-center">
                <v-icon size="80" color="grey-lighten-2">mdi-comment-off</v-icon>
                <h3 class="text-h6 mt-3">نظری ثبت نشده است</h3>
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>

        <!-- Contact Tab -->
        <v-window-item value="contact">
          <SupplierContact ref="contactSection" :supplier="supplier" />
        </v-window-item>
      </v-window>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import { useSupplierApi, type Supplier, type SupplierComment } from '~/composables/useSupplierApi'
import { useSupplierPortfolioApi, type SupplierPortfolioItem } from '~/composables/useSupplierPortfolioApi'
import { useSupplierTeamApi, type SupplierTeamMember } from '~/composables/useSupplierTeamApi'

const route = useRoute()
const authStore = useAuthStore()
const supplierApi = useSupplierApi()
const portfolioApi = useSupplierPortfolioApi()
const teamApi = useSupplierTeamApi()

const supplier = ref<Supplier | null>(null)
const products = ref<any[]>([])
const portfolioItems = ref<SupplierPortfolioItem[]>([])
const teamMembers = ref<SupplierTeamMember[]>([])
const comments = ref<SupplierComment[]>([])

const loading = ref(false)
const productsLoading = ref(false)
const portfolioLoading = ref(false)
const teamLoading = ref(false)
const error = ref<string | null>(null)

const activeTab = ref('overview')
const contactSection = ref()

// Mobile tabs computed property
const mobileTabItems = computed(() => {
  const tabs = [
    { title: 'معرفی', value: 'overview', icon: 'mdi-information', color: 'primary' }
  ]

  if (products.value.length > 0) {
    tabs.push({
      title: 'محصولات',
      value: 'products',
      icon: 'mdi-package-variant',
      color: 'primary',
      badge: products.value.length.toString(),
      badgeColor: 'white'
    })
  }

  if (portfolioItems.value.length > 0) {
    tabs.push({
      title: 'نمونه کارها',
      value: 'portfolio',
      icon: 'mdi-briefcase',
      color: 'secondary'
    })
  }

  if (teamMembers.value.length > 0) {
    tabs.push({
      title: 'تیم ما',
      value: 'team',
      icon: 'mdi-account-group',
      color: 'info'
    })
  }

  if (hasCertifications.value) {
    tabs.push({
      title: 'گواهینامه‌ها',
      value: 'certifications',
      icon: 'mdi-certificate',
      color: 'success'
    })
  }

  if (comments.value.length > 0) {
    tabs.push({
      title: 'نظرات',
      value: 'reviews',
      icon: 'mdi-star',
      color: 'amber',
      badge: comments.value.length.toString(),
      badgeColor: 'white'
    })
  }

  tabs.push({
    title: 'تماس با ما',
    value: 'contact',
    icon: 'mdi-email',
    color: 'primary'
  })

  return tabs
})

// Available tabs for progress indicator
const availableTabs = computed(() => {
  const tabs = [
    { value: 'overview', label: 'معرفی' }
  ]

  if (products.value.length > 0) tabs.push({ value: 'products', label: 'محصولات' })
  if (portfolioItems.value.length > 0) tabs.push({ value: 'portfolio', label: 'نمونه کارها' })
  if (teamMembers.value.length > 0) tabs.push({ value: 'team', label: 'تیم ما' })
  if (hasCertifications.value) tabs.push({ value: 'certifications', label: 'گواهینامه‌ها' })
  if (comments.value.length > 0) tabs.push({ value: 'reviews', label: 'نظرات' })
  tabs.push({ value: 'contact', label: 'تماس با ما' })

  return tabs
})

// Current tab index for progress
const currentTabIndex = computed(() => {
  return availableTabs.value.findIndex(tab => tab.value === activeTab.value)
})

// Progress width calculation
const progressWidth = computed(() => {
  if (availableTabs.value.length === 0) return 0
  return ((currentTabIndex.value + 1) / availableTabs.value.length) * 100
})

const brandingStyles = computed(() => {
  if (!supplier.value) return {}
  
  const styles: any = {}
  if (supplier.value.brand_color_primary) {
    styles['--brand-primary'] = supplier.value.brand_color_primary
  }
  if (supplier.value.brand_color_secondary) {
    styles['--brand-secondary'] = supplier.value.brand_color_secondary
  }
  return styles
})

const hasCertifications = computed(() => {
  return (supplier.value?.certifications && supplier.value.certifications.length > 0) ||
         (supplier.value?.awards && supplier.value.awards.length > 0)
})

useHead(() => ({
  title: supplier.value?.meta_title || supplier.value?.store_name || 'تامین‌کننده',
  meta: [
    {
      name: 'description',
      content: supplier.value?.meta_description || supplier.value?.description || ''
    },
    // Open Graph tags
    {
      property: 'og:title',
      content: supplier.value?.store_name || ''
    },
    {
      property: 'og:description',
      content: supplier.value?.description || ''
    },
    {
      property: 'og:type',
      content: 'website'
    }
  ]
}))

const fetchSupplier = async () => {
  loading.value = true
  error.value = null

  try {
    const id = route.params.id

    // Initialize auth if needed (for new tabs/windows)
    if (process.client && !authStore.user && authStore.token) {
      await authStore.fetchCurrentUser()
    }

    // Check if current user is the owner of this supplier profile
    const isOwner = authStore.user?.vendor_profile?.id === parseInt(id as string)

    if (isOwner && authStore.user?.vendor_profile) {
      // For the owner, use their vendor profile data directly
      supplier.value = authStore.user.vendor_profile

      // Fetch related data using the user's vendor profile
      await Promise.all([
        fetchProducts(id as string),
        fetchPortfolio(id as string),
        fetchTeam(id as string),
        fetchComments(id as string)
      ])
    } else {
      // For public access or if owner check failed, use the API
      // The backend will allow owners to view their own profile even if not approved
      supplier.value = await supplierApi.getSupplier(id as string)

      // Fetch related data
      await Promise.all([
        fetchProducts(id as string),
        fetchPortfolio(id as string),
        fetchTeam(id as string),
        fetchComments(id as string)
      ])
    }
  } catch (err: any) {
    console.error('Error fetching supplier:', err)
    if (err?.response?.status === 404 || err?.statusCode === 404) {
      error.value = 'صفحه تامین‌کننده یافت نشد یا هنوز تایید نشده است.'
    } else {
      error.value = 'خطا در بارگذاری اطلاعات تامین‌کننده'
    }
  } finally {
    loading.value = false
  }
}

const fetchProducts = async (id: string) => {
  productsLoading.value = true
  try {
    products.value = await supplierApi.getSupplierProducts(id)
  } catch (err) {
    console.error('Error fetching products:', err)
  } finally {
    productsLoading.value = false
  }
}

const fetchPortfolio = async (id: string) => {
  portfolioLoading.value = true
  try {
    portfolioItems.value = await supplierApi.getSupplierPortfolio(id)
  } catch (err) {
    console.error('Error fetching portfolio:', err)
  } finally {
    portfolioLoading.value = false
  }
}

const fetchTeam = async (id: string) => {
  teamLoading.value = true
  try {
    teamMembers.value = await supplierApi.getSupplierTeam(id)
  } catch (err) {
    console.error('Error fetching team:', err)
  } finally {
    teamLoading.value = false
  }
}

const fetchComments = async (id: string) => {
  try {
    comments.value = await supplierApi.getSupplierComments(id)
  } catch (err) {
    console.error('Error fetching comments:', err)
  }
}

const scrollToContact = () => {
  activeTab.value = 'contact'
  setTimeout(() => {
    contactSection.value?.$el.scrollIntoView({ behavior: 'smooth' })
  }, 100)
}

const handleAddToCart = (product: any) => {
  // Add to cart logic
  console.log('Add to cart:', product)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const copyToClipboard = (text: string) => {
  if (process.client && navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      // Could show a snackbar here
    })
  }
}

onMounted(() => {
  fetchSupplier()
})
</script>

<style scoped>
.supplier-mini-website {
  --brand-primary: rgb(var(--v-theme-primary));
  --brand-secondary: rgb(var(--v-theme-secondary));
  min-height: 100vh;
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-surface), 0.8) 0%,
    rgba(var(--v-theme-surface-variant), 0.6) 50%,
    rgba(var(--v-theme-surface), 0.9) 100%
  );
  position: relative;
  overflow-x: hidden;
}

/* Global micro-interactions */
.supplier-mini-website::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(var(--v-theme-primary), 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(var(--v-theme-secondary, var(--v-theme-primary)), 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}

/* Enhanced Loading State */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  position: relative;
}

.loading-content {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  position: relative;
  margin-bottom: 2rem;
}

.main-spinner {
  position: relative;
  z-index: 2;
}

.spinner-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border: 3px solid rgba(var(--v-theme-primary), 0.1);
  border-top: 3px solid rgb(var(--v-theme-primary));
  border-radius: 50%;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

.loading-text {
  animation: fadeInUp 0.5s ease-out;
}

/* Enhanced Error State */
.error-container {
  padding: 4rem 2rem;
}

.error-card {
  max-width: 500px;
  margin: 0 auto;
  border-radius: 24px;
}

.error-icon {
  position: relative;
  display: inline-block;
}

.error-main-icon {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.error-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: rgb(var(--v-theme-error));
  border-radius: 50%;
  animation: particleFloat 3s ease-in-out infinite;
}

.particle:nth-child(1) {
  top: 10%;
  left: 20%;
  animation-delay: 0s;
}

.particle:nth-child(2) {
  top: 60%;
  left: 80%;
  animation-delay: 1s;
}

.particle:nth-child(3) {
  top: 80%;
  left: 10%;
  animation-delay: 2s;
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0px) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-20px) scale(1.2);
    opacity: 1;
  }
}

.retry-btn {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-primary-variant, var(--v-theme-primary)))) !important;
  color: white !important;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(var(--v-theme-primary), 0.4);
}

/* Smooth transitions for tab content */
.tab-content {
  min-height: 60vh;
  position: relative;
}

.tab-content > * {
  animation: fadeInScale 0.4s ease-out;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Enhanced glass card effects */
.glass-card {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Scroll animations */
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  animation: slideInUp 0.6s ease-out forwards;
}

@keyframes slideInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Hover effects for interactive elements */
.v-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.v-btn:hover {
  transform: translateY(-1px);
}

.v-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Ripple effect enhancement */
.v-btn::before {
  transition: all 0.3s ease;
}

/* Focus states */
.v-text-field:focus-within,
.v-select:focus-within {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.15);
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(var(--v-theme-surface), 0.5);
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.7);
}

/* Enhanced Typography */
.supplier-mini-website {
  font-family: 'Vazirmatn', 'Roboto', 'Helvetica', 'Arial', sans-serif;
  line-height: 1.6;
  letter-spacing: 0.01em;
}

/* Heading Hierarchy */
.text-h1, .text-h2, .text-h3, .text-h4, .text-h5, .text-h6 {
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.02em;
  color: rgba(var(--v-theme-on-surface), 0.9);
}

.text-h1 {
  font-size: 2.5rem !important;
}

.text-h2 {
  font-size: 2rem !important;
}

.text-h3 {
  font-size: 1.75rem !important;
}

.text-h4 {
  font-size: 1.5rem !important;
}

.text-h5 {
  font-size: 1.25rem !important;
}

.text-h6 {
  font-size: 1.125rem !important;
}

/* Body Text */
.text-body-1 {
  font-size: 1rem;
  line-height: 1.7;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.text-body-2 {
  font-size: 0.875rem;
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.75);
}

/* Caption Text */
.text-caption {
  font-size: 0.75rem;
  line-height: 1.5;
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-weight: 500;
}

/* Subtitle Text */
.text-subtitle-1 {
  font-size: 1rem;
  line-height: 1.5;
  color: rgba(var(--v-theme-on-surface), 0.8);
  font-weight: 500;
}

.text-subtitle-2 {
  font-size: 0.875rem;
  line-height: 1.5;
  color: rgba(var(--v-theme-on-surface), 0.75);
  font-weight: 500;
}

/* Enhanced spacing for overview section */
.overview-content {
  padding: 2rem 0;
}

.overview-content .v-card {
  margin-bottom: 2rem;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.overview-content .v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* Enhanced spacing for reviews section */
.reviews-section {
  padding: 3rem 0;
}

.comment-card {
  border-radius: 16px;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.comment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* Reading experience improvements */
.readable-heading {
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: rgba(var(--v-theme-on-surface), 0.96);
  margin-bottom: 1rem;
}

.readable-text {
  line-height: 1.8;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
  text-align: justify;
  max-width: 70ch;
}

/* Content body styling */
.content-body {
  max-width: 100%;
  line-height: 1.8;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
}

/* Enhanced content spacing */
.content-body p {
  margin-bottom: 1.5rem;
  text-align: justify;
}

.content-body p:last-child {
  margin-bottom: 0;
}

/* Enhanced list styling */
.content-body ul,
.content-body ol {
  margin: 1.5rem 0;
  padding-right: 2rem;
  line-height: 1.8;
}

.content-body li {
  margin-bottom: 0.75rem;
  line-height: 1.8;
}

.content-body li:last-child {
  margin-bottom: 0;
}

/* Quote styling */
.content-body blockquote {
  border-right: 4px solid rgba(var(--v-theme-primary), 0.5);
  padding-right: 1.5rem;
  margin: 2rem 0;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), 0.75);
  line-height: 1.8;
  background: rgba(var(--v-theme-primary), 0.05);
  padding: 1.5rem;
  border-radius: 0 8px 8px 0;
}

/* Link styling */
.content-body a {
  color: rgb(var(--v-theme-primary));
  text-decoration: underline;
  text-decoration-color: rgba(var(--v-theme-primary), 0.3);
  transition: all 0.3s ease;
}

.content-body a:hover {
  color: rgb(var(--v-theme-primary-variant, var(--v-theme-primary)));
  text-decoration-color: rgba(var(--v-theme-primary), 0.6);
}

/* Code styling */
.content-body code {
  background-color: rgba(var(--v-theme-on-surface), 0.08);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
}

.content-body pre {
  background-color: rgba(var(--v-theme-on-surface), 0.05);
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5rem 0;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.content-body pre code {
  background-color: transparent;
  padding: 0;
}

/* Image styling in content */
.content-body img {
  max-width: 100%;
  border-radius: 16px;
  margin: 1.5rem 0;
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.1);
  transition: transform 0.3s ease;
}

.content-body img:hover {
  transform: scale(1.02);
}

/* Table styling */
.content-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.content-body th,
.content-body td {
  padding: 0.75rem;
  text-align: right;
  border-bottom: 1px solid rgba(var(--v-theme-outline), 0.2);
}

.content-body th {
  background: rgba(var(--v-theme-primary), 0.1);
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.9);
}

.content-body tr:nth-child(even) {
  background: rgba(var(--v-theme-surface-variant), 0.3);
}

.content-body tr:hover {
  background: rgba(var(--v-theme-primary), 0.05);
}

/* RTL-specific typography adjustments */
[dir="rtl"] .content-body blockquote {
  border-right: none;
  border-left: 4px solid rgba(var(--v-theme-primary), 0.5);
  padding-right: 0;
  padding-left: 1.5rem;
  border-radius: 8px 0 0 8px;
}

[dir="rtl"] .content-body ul,
[dir="rtl"] .content-body ol {
  padding-right: 0;
  padding-left: 2rem;
}

/* Improved spacing for mobile */
@media (max-width: 600px) {
  .supplier-mini-website {
    font-size: 0.9rem;
  }

  .text-h1 {
    font-size: 2rem !important;
  }

  .text-h2 {
    font-size: 1.75rem !important;
  }

  .text-h3 {
    font-size: 1.5rem !important;
  }

  .readable-text {
    text-align: right;
    max-width: 100%;
  }

  .content-body p {
    text-align: right;
  }

  .content-body blockquote {
    text-align: right;
  }

  .overview-content .v-card {
    margin-bottom: 1.5rem;
  }

  .comment-card {
    margin-bottom: 1rem;
  }
}

/* Print styles */
@media print {
  .supplier-mini-website {
    background: white !important;
  }

  .readable-text {
    color: black !important;
  }

  .readable-heading {
    color: black !important;
  }
}

.tabs-container {
  position: sticky;
  top: 64px;
  z-index: 10;
  background: linear-gradient(135deg, rgba(var(--v-theme-surface), 0.95), rgba(var(--v-theme-surface-variant), 0.9));
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(var(--v-theme-outline), 0.2);
  padding: 1.5rem 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.tabs-container:hover {
  background: linear-gradient(135deg, rgba(var(--v-theme-surface), 0.98), rgba(var(--v-theme-surface-variant), 0.95));
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

/* Mobile Tab Selector */
.mobile-tab-selector {
  margin-bottom: 1rem;
}

.mobile-tabs-select {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.mobile-tabs-select :deep(.v-field) {
  border-radius: 12px;
}

/* Modern Desktop Tabs */
.mini-website-tabs {
  border-radius: 16px;
  overflow: visible;
  background: transparent !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.mini-website-tabs :deep(.v-tabs-slider) {
  height: 4px;
  border-radius: 2px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.modern-tab {
  min-width: 140px;
  height: 70px;
  border-radius: 12px;
  margin: 0 4px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.modern-tab::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modern-tab:hover::before {
  opacity: 1;
}

.modern-tab:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.modern-tab.v-tab--selected {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modern-tab.v-tab--selected::before {
  opacity: 1;
}

.tab-content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 8px;
  position: relative;
}

.tab-icon {
  margin-bottom: 4px;
  transition: transform 0.3s ease;
}

.modern-tab:hover .tab-icon {
  transform: scale(1.1);
}

.tab-text {
  font-size: 0.85rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-align: center;
}

.tab-badge {
  margin-top: 4px;
  font-size: 0.7rem;
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 3px;
  background: white;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.modern-tab:hover .tab-indicator {
  width: 60%;
}

.modern-tab.v-tab--selected .tab-indicator {
  width: 80%;
}

/* Contact Tab Special Styling */
.contact-tab {
  background: linear-gradient(135deg, rgba(25, 118, 210, 0.1), rgba(66, 165, 245, 0.1));
  border: 1px solid rgba(25, 118, 210, 0.3);
}

.contact-pulse {
  position: absolute;
  top: 8px;
  right: 8px;
  color: #4caf50;
  animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Progress Indicator */
.tab-progress-container {
  margin-top: 1rem;
  padding: 0 1rem;
}

.tab-progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tab-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #81c784);
  border-radius: 2px;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
}

.progress-dots {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  padding: 0 2px;
}

.progress-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.progress-dot:hover {
  background: rgba(255, 255, 255, 0.6);
  transform: scale(1.2);
}

.progress-dot.active {
  background: #4caf50;
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.5);
}

.progress-dot.completed {
  background: #81c784;
}

.progress-dot.completed::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 8px;
  font-weight: bold;
}

.tab-content {
  min-height: 60vh;
}

.sticky-sidebar {
  position: sticky;
  top: 200px;
  transition: all 0.3s ease;
}

@media (max-width: 960px) {
  .sticky-sidebar {
    position: relative;
    top: 0;
  }
}

.contact-quick-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.95)) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(var(--v-theme-outline), 0.1);
}

.contact-quick-item {
  border-radius: 12px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.contact-quick-item:hover {
  background: rgba(var(--v-theme-primary), 0.05);
  transform: translateX(-4px);
}

.contact-cta-btn {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.contact-cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(var(--v-theme-primary), 0.3);
}

.title-wrapper {
  display: flex;
  align-items: center;
}

.overview-card {
  transition: all 0.3s ease;
  background: white;
}

.overview-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1) !important;
}

.comment-card {
  border-radius: 16px;
  height: 100%;
  transition: all 0.3s ease;
  background: white;
}

.comment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1) !important;
}

.comment-avatar {
  border: 3px solid rgba(var(--v-theme-primary), 0.1);
  transition: all 0.3s ease;
}

.comment-card:hover .comment-avatar {
  border-color: rgba(var(--v-theme-primary), 0.3);
  transform: scale(1.05);
}

.comment-title {
  color: rgba(var(--v-theme-on-surface), 0.95);
}

.comment-text {
  color: rgba(var(--v-theme-on-surface), 0.8);
  line-height: 1.7;
}

.rating-badge {
  flex-shrink: 0;
}

.supplier-reply {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08), rgba(var(--v-theme-primary), 0.03));
  padding: 16px;
  border-radius: 12px;
  border-right: 4px solid rgb(var(--v-theme-primary));
  transition: all 0.3s ease;
}

.supplier-reply:hover {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12), rgba(var(--v-theme-primary), 0.06));
}

.reviews-grid {
  margin: -12px;
}

.reviews-grid > .v-col {
  padding: 12px;
}

.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

@media (max-width: 600px) {
  .overview-card .v-card-title,
  .overview-card .v-card-text {
    padding: 1rem !important;
  }
  
  .comment-card .v-card-text {
    padding: 1rem !important;
  }
  
  .title-wrapper {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .title-wrapper .v-icon {
    margin: 0;
  }
}

/* Typography improvements - matching blog section */
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

/* Content body styling */
.content-body {
  max-width: 100%;
  line-height: 1.8;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
}

.content-body :deep(img) {
  max-width: 100%;
  border-radius: 16px;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.1);
}

.content-body :deep(h1),
.content-body :deep(h2),
.content-body :deep(h3),
.content-body :deep(h4),
.content-body :deep(h5),
.content-body :deep(h6) {
  font-weight: 700;
  line-height: 1.3;
  color: rgba(var(--v-theme-on-surface), 0.96);
  margin-bottom: 0;
}

/* Medium.com-inspired heading spacing */
.content-body :deep(h1) {
  font-size: 2.5rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
}

.content-body :deep(h1:first-child) {
  margin-top: 0;
}

.content-body :deep(h2) {
  font-size: 2rem;
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
}

.content-body :deep(h3) {
  font-size: 1.75rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.content-body :deep(h4) {
  font-size: 1.5rem;
  margin-top: 1.75rem;
  margin-bottom: 0.875rem;
}

.content-body :deep(h5) {
  font-size: 1.25rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.content-body :deep(h6) {
  font-size: 1.125rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

/* Medium.com-inspired paragraph spacing */
.content-body :deep(p) {
  line-height: 1.8;
  margin-top: 0;
  margin-bottom: 1.75rem;
  color: rgba(var(--v-theme-on-surface), 0.87);
  font-size: 1.05rem;
  text-align: justify;
  max-width: 65ch;
}

/* First paragraph after heading has less top margin */
.content-body :deep(h1 + p),
.content-body :deep(h2 + p),
.content-body :deep(h3 + p),
.content-body :deep(h4 + p),
.content-body :deep(h5 + p),
.content-body :deep(h6 + p) {
  margin-top: 0.5rem;
}

.content-body :deep(ul),
.content-body :deep(ol) {
  margin-top: 1.5rem;
  margin-bottom: 1.75rem;
  padding-right: 2rem;
  line-height: 1.8;
}

.content-body :deep(li) {
  margin-bottom: 0.875rem;
  line-height: 1.8;
}

.content-body :deep(li:last-child) {
  margin-bottom: 0;
}

.content-body :deep(blockquote) {
  border-right: 4px solid rgba(var(--v-theme-primary), 0.5);
  padding-right: 1.5rem;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), 0.75);
  line-height: 1.8;
}

.content-body :deep(blockquote p) {
  margin-bottom: 1rem;
}

.content-body :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

.content-body :deep(a) {
  color: rgb(var(--v-theme-primary));
  text-decoration: underline;
  transition: opacity 0.2s ease;
}

.content-body :deep(a:hover) {
  opacity: 0.8;
}

.content-body :deep(code) {
  background-color: rgba(var(--v-theme-on-surface), 0.08);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Courier New', monospace;
}

.content-body :deep(pre) {
  background-color: rgba(var(--v-theme-on-surface), 0.05);
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
}

.content-body :deep(pre code) {
  background-color: transparent;
  padding: 0;
}
</style>
