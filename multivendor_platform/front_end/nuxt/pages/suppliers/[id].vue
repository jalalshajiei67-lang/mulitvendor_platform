<template>
  <div class="supplier-page" dir="rtl" :style="brandingStyles">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
        width="6"
      />
      <p class="text-subtitle-1 mt-4 text-medium-emphasis">در حال بارگذاری...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <v-container class="py-8">
        <v-card class="error-card mx-auto" max-width="500">
          <v-card-text class="text-center pa-8">
            <v-icon size="64" color="error" class="mb-4">
              mdi-alert-circle-outline
            </v-icon>
            <h2 class="text-h5 font-weight-bold mb-3">
              مشکلی پیش آمده
            </h2>
            <p class="text-body-1 mb-6 text-medium-emphasis">
              {{ error }}
            </p>
            <v-btn
              color="primary"
              variant="flat"
              size="large"
              @click="fetchSupplier"
              rounded="lg"
            >
              <v-icon start>mdi-refresh</v-icon>
              تلاش مجدد
            </v-btn>
          </v-card-text>
        </v-card>
      </v-container>
    </div>

    <!-- Supplier Mini Website -->
    <div v-else-if="supplier">
      <!-- Simplified Hero -->
      <div class="hero-section">
        <div class="hero-bg" v-if="bannerImageUrl" :style="{ backgroundImage: `url(${bannerImageUrl})` }"></div>
        <div class="hero-overlay"></div>
        
        <v-container class="hero-content">
          <!-- Logo and Title -->
          <div class="text-center py-8">
            <v-avatar
              v-if="supplier.logo"
              :image="supplier.logo"
              size="100"
              class="mb-4 logo-avatar"
            />
            <h1 class="text-h4 text-md-h3 font-weight-bold mb-2">
              {{ supplier.store_name }}
            </h1>
            <p v-if="supplier.slogan" class="text-body-1 text-medium-emphasis mb-6">
              {{ supplier.slogan }}
            </p>
            
            <!-- Quick Actions -->
            <div class="d-flex gap-2 justify-center flex-wrap">
              <v-btn
                color="primary"
                variant="flat"
                size="large"
                rounded="lg"
                @click="activeSection = 'contact'"
              >
                <v-icon start>mdi-phone</v-icon>
                تماس با ما
              </v-btn>
              <v-btn
                v-if="products.length > 0"
                color="white"
                variant="flat"
                size="large"
                rounded="lg"
                @click="activeSection = 'products'"
              >
                <v-icon start>mdi-shopping</v-icon>
                محصولات
              </v-btn>
            </div>
          </div>

          <!-- Navigation Tabs -->
          <v-tabs
            v-model="activeSection"
            bg-color="transparent"
            color="primary"
            grow
            class="nav-tabs"
          >
            <v-tab
              v-for="section in availableSections"
              :key="section.value"
              :value="section.value"
              class="nav-tab"
            >
              <v-icon start size="20">{{ section.icon }}</v-icon>
              <span class="d-none d-sm-inline">{{ section.label }}</span>
            </v-tab>
          </v-tabs>
        </v-container>
      </div>

      <!-- Main Content -->
      <v-container class="main-content py-6">
        <!-- HOME SECTION -->
        <div v-if="activeSection === 'home'" class="home-section">
          <!-- Metrics -->
          <v-row class="mb-6">
            <v-col
              v-if="supplier.year_established"
              cols="6"
              md="3"
            >
              <div class="metric-card">
                <v-icon color="primary" size="32" class="mb-2">mdi-calendar-check</v-icon>
                <div class="metric-value">{{ yearsOfExperience }} سال</div>
                <div class="metric-label">سابقه فعالیت</div>
              </div>
            </v-col>

            <v-col
              v-if="supplier.employee_count"
              cols="6"
              md="3"
            >
              <div class="metric-card">
                <v-icon color="primary" size="32" class="mb-2">mdi-account-group</v-icon>
                <div class="metric-value">{{ supplier.employee_count }}</div>
                <div class="metric-label">تعداد پرسنل</div>
              </div>
            </v-col>

            <v-col cols="6" md="3">
              <div class="metric-card">
                <v-icon color="primary" size="32" class="mb-2">mdi-star</v-icon>
                <div class="metric-value">{{ supplier.rating_average || 0 }}</div>
                <div class="metric-label">امتیاز</div>
              </div>
            </v-col>

            <v-col cols="6" md="3">
              <div class="metric-card">
                <v-icon color="primary" size="32" class="mb-2">mdi-package-variant</v-icon>
                <div class="metric-value">{{ supplier.product_count || 0 }}</div>
                <div class="metric-label">محصولات</div>
              </div>
            </v-col>
          </v-row>

          <!-- About Section -->
          <v-card v-if="supplier.about || supplier.description" class="content-card mb-4" rounded="lg" elevation="0">
            <v-card-title class="d-flex align-center gap-2 pb-2">
              <v-icon color="primary">mdi-information</v-icon>
              <span class="text-h6 font-weight-bold">درباره ما</span>
            </v-card-title>
            <v-card-text class="text-body-1 content-text">
              {{ supplier.about || supplier.description }}
            </v-card-text>
          </v-card>

          <!-- Work Resume -->
          <v-card v-if="supplier.work_resume" class="content-card mb-4" rounded="lg" elevation="0">
            <v-card-title class="d-flex align-center gap-2 pb-2">
              <v-icon color="primary">mdi-briefcase</v-icon>
              <span class="text-h6 font-weight-bold">پروژه‌ها و تجربیات</span>
            </v-card-title>
            <v-card-text class="text-body-1 content-text">
              {{ supplier.work_resume }}
            </v-card-text>
          </v-card>

          <!-- History -->
          <v-card v-if="supplier.history" class="content-card mb-4" rounded="lg" elevation="0">
            <v-card-title class="d-flex align-center gap-2 pb-2">
              <v-icon color="primary">mdi-history</v-icon>
              <span class="text-h6 font-weight-bold">داستان ما</span>
            </v-card-title>
            <v-card-text class="text-body-1 content-text">
              {{ supplier.history }}
            </v-card-text>
          </v-card>

          <!-- Portfolio Section -->
          <div v-if="portfolioItems.length > 0" class="mb-6">
            <h2 class="section-title mb-4">
              <v-icon color="primary" class="me-2">mdi-image-multiple</v-icon>
              نمونه کارها
            </h2>
            <SupplierPortfolio
              :items="portfolioItems"
              :loading="portfolioLoading"
            />
          </div>
          <!-- Certifications Section -->
          <div v-if="hasCertifications" class="mb-6">
            <h2 class="section-title mb-4">
              <v-icon color="primary" class="me-2">mdi-certificate</v-icon>
              مدارک و گواهینامه‌ها
            </h2>
            <SupplierCertifications
              :certifications="supplier.certifications"
              :awards="supplier.awards"
            />
          </div>
        </div>

        <!-- PRODUCTS SECTION -->
        <div v-if="activeSection === 'products'" class="products-section">
          <h2 class="section-title mb-4">
            <v-icon color="primary" class="me-2">mdi-shopping</v-icon>
            محصولات ما
          </h2>
          <SupplierProductCatalog
            :products="products"
            :loading="productsLoading"
            @add-to-cart="handleAddToCart"
          />
        </div>

        <!-- TEAM SECTION -->
        <div v-if="activeSection === 'team'" class="team-section">
          <h2 class="section-title mb-4">
            <v-icon color="primary" class="me-2">mdi-account-group</v-icon>
            تیم ما
          </h2>
          <SupplierTeam
            :members="teamMembers"
            :loading="teamLoading"
          />
        </div>

        <!-- REVIEWS SECTION -->
        <div v-if="activeSection === 'reviews'" class="reviews-section">
          <h2 class="section-title mb-4">
            <v-icon color="primary" class="me-2">mdi-comment-quote</v-icon>
            نظرات مشتریان
          </h2>

          <div v-if="comments.length > 0" class="comments-list">
            <v-card
              v-for="comment in comments"
              :key="comment.id"
              class="comment-card mb-4"
              rounded="lg"
              elevation="0"
            >
              <v-card-text class="pa-4">
                <!-- Header -->
                <div class="d-flex justify-space-between align-start mb-3">
                  <div class="d-flex align-center gap-3 flex-grow-1">
                    <v-avatar size="48" color="primary">
                      <span class="text-white text-h6">
                        {{ comment.user_username.charAt(0).toUpperCase() }}
                      </span>
                    </v-avatar>
                    <div>
                      <p class="font-weight-bold text-body-1 mb-1">
                        {{ comment.user_username }}
                      </p>
                      <p class="text-caption text-medium-emphasis">
                        {{ formatDate(comment.created_at) }}
                      </p>
                    </div>
                  </div>
                  <v-rating
                    :model-value="comment.rating"
                    readonly
                    color="amber"
                    size="small"
                    density="compact"
                  />
                </div>

                <!-- Content -->
                <h4 v-if="comment.title" class="text-subtitle-1 font-weight-bold mb-2">
                  {{ comment.title }}
                </h4>
                <p class="text-body-2 mb-3">
                  {{ comment.comment }}
                </p>

                <!-- Supplier Reply -->
                <div v-if="comment.supplier_reply" class="supplier-reply pa-3">
                  <p class="text-caption font-weight-bold text-primary mb-2">
                    <v-icon size="16" class="me-1">mdi-reply</v-icon>
                    پاسخ فروشنده
                  </p>
                  <p class="text-body-2">
                    {{ comment.supplier_reply }}
                  </p>
                </div>
              </v-card-text>
            </v-card>
          </div>

          <!-- Empty State -->
          <v-card v-else class="text-center pa-8" rounded="lg" elevation="0">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">
              mdi-comment-off-outline
            </v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">
              هنوز نظری ثبت نشده
            </h3>
            <p class="text-body-2 text-medium-emphasis">
              اولین نفری باشید که نظر می‌دهد
            </p>
          </v-card>
        </div>

        <!-- CONTACT SECTION -->
        <div v-if="activeSection === 'contact'" class="contact-section">
          <h2 class="section-title mb-4">
            <v-icon color="primary" class="me-2">mdi-phone-in-talk</v-icon>
            تماس با ما
          </h2>
          <SupplierContact
            ref="contactSection"
            :supplier="supplier"
          />
        </div>
      </v-container>

      <!-- Fixed Contact Button (mobile) -->
      <v-btn
        v-if="display.mdAndDown.value && activeSection !== 'contact'"
        class="floating-contact-btn"
        color="primary"
        size="large"
        icon
        elevation="8"
        @click="activeSection = 'contact'"
      >
        <v-icon size="28">mdi-phone</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDisplay } from 'vuetify'
import { toJalaali } from 'jalaali-js'
import { useAuthStore } from '~/stores/auth'
import {
  useSupplierApi,
  type Supplier,
  type SupplierComment
} from '~/composables/useSupplierApi'
import {
  useSupplierPortfolioApi,
  type SupplierPortfolioItem
} from '~/composables/useSupplierPortfolioApi'
import {
  useSupplierTeamApi,
  type SupplierTeamMember
} from '~/composables/useSupplierTeamApi'
import { generateOrganizationSchema, generateBreadcrumbSchema, prepareSchemaScripts } from '~/composables/useSchema'
import { formatImageUrl } from '~/utils/imageUtils'

const route = useRoute()
const authStore = useAuthStore()
const supplierApi = useSupplierApi()
const portfolioApi = useSupplierPortfolioApi()
const teamApi = useSupplierTeamApi()
const display = useDisplay()

const supplier = ref<Supplier | null>(null)
const products = ref<any[]>([])
const portfolioItems = ref<SupplierPortfolioItem[]>([])
const teamMembers = ref<SupplierTeamMember[]>([])
const comments = ref<SupplierComment[]>([])

const loading = ref(true)
const productsLoading = ref(false)
const portfolioLoading = ref(false)
const teamLoading = ref(false)
const error = ref<string | null>(null)

const activeSection = ref('home')
const contactSection = ref()

// Mobile nav
const mobileNavItems = computed(() => {
  const sections: Array<{
    title: string
    value: string
    icon: string
    color: string
  }> = [
    { title: 'خانه', value: 'home', icon: 'mdi-home', color: 'primary' }
  ]

  if (products.value.length > 0) {
    sections.push({
      title: 'محصولات',
      value: 'products',
      icon: 'mdi-package-variant',
      color: 'primary'
    })
  }

  if (teamMembers.value.length > 0) {
    sections.push({
      title: 'تیم ما',
      value: 'team',
      icon: 'mdi-account-group',
      color: 'primary'
    })
  }

  if (comments.value.length > 0) {
    sections.push({
      title: 'نظرات',
      value: 'reviews',
      icon: 'mdi-star',
      color: 'primary'
    })
  }

  sections.push({
    title: 'تماس با ما',
    value: 'contact',
    icon: 'mdi-email',
    color: 'primary'
  })

  return sections
})

// Desktop nav
const availableSections = computed(() => {
  const sections: Array<{ value: string; label: string; icon: string }> = [
    { value: 'home', label: 'خانه', icon: 'mdi-home' }
  ]

  if (products.value.length > 0) {
    sections.push({
      value: 'products',
      label: 'محصولات',
      icon: 'mdi-package-variant'
    })
  }
  if (teamMembers.value.length > 0) {
    sections.push({
      value: 'team',
      label: 'تیم ما',
      icon: 'mdi-account-group'
    })
  }
  if (comments.value.length > 0) {
    sections.push({
      value: 'reviews',
      label: 'نظرات',
      icon: 'mdi-star'
    })
  }
  sections.push({
    value: 'contact',
    label: 'تماس با ما',
    icon: 'mdi-email'
  })

  return sections
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

const bannerImageUrl = computed(() => {
  if (!supplier.value?.banner_image) return null
  return formatImageUrl(supplier.value.banner_image)
})

const hasCertifications = computed(() => {
  return (
    (supplier.value?.certifications &&
      supplier.value.certifications.length > 0) ||
    (supplier.value?.awards && supplier.value.awards.length > 0)
  )
})

// Years of experience (Jalaali)
const yearsOfExperience = computed(() => {
  if (!supplier.value?.year_established) return 0

  const now = new Date()
  const currentJalaali = toJalaali(
    now.getFullYear(),
    now.getMonth() + 1,
    now.getDate()
  )
  const currentYear = currentJalaali.jy
  const years = currentYear - supplier.value.year_established

  return years > 0 ? years : 0
})

const config = useRuntimeConfig()
const baseUrl = computed(() => {
  if (typeof window !== 'undefined') {
    return config.public.siteUrl || window.location.origin
  }
  return config.public.siteUrl || 'https://indexo.ir'
})

// Generate schemas
const organizationSchema = computed(() => {
  if (!supplier.value) return null
  return generateOrganizationSchema(supplier.value, baseUrl.value)
})

// Breadcrumbs for supplier page
const supplierBreadcrumbs = computed(() => [
  { title: 'خانه', to: '/' },
  { title: 'تامین‌کنندگان', to: '/suppliers' },
  { title: supplier.value?.store_name || 'تامین‌کننده', disabled: true }
])

const breadcrumbSchema = computed(() => {
  if (!supplierBreadcrumbs.value.length) return null
  return generateBreadcrumbSchema(
    supplierBreadcrumbs.value.map(item => ({
      name: item.title,
      url: item.to ? `${baseUrl.value}${item.to}` : undefined
    })),
    baseUrl.value
  )
})

// Get canonical URL (default from ID, no DB field for suppliers)
const canonicalUrl = computed(() => {
  if (!supplier.value?.id) return ''
  return `${baseUrl.value}/suppliers/${supplier.value.id}`
})

// Get OG image (primary image: logo or banner)
const ogImage = computed(() => {
  return supplier.value?.logo || supplier.value?.banner_image || ''
})

// Meta tags with Twitter Cards
useHead(() => ({
  title:
    supplier.value?.meta_title ||
    supplier.value?.store_name ||
    'تامین‌کننده',
  meta: [
    {
      name: 'description',
      content:
        supplier.value?.meta_description ||
        supplier.value?.description ||
        ''
    },
    {
      property: 'og:title',
      content: supplier.value?.meta_title || supplier.value?.store_name || ''
    },
    {
      property: 'og:description',
      content: supplier.value?.meta_description || supplier.value?.description || ''
    },
    {
      property: 'og:type',
      content: 'website'
    },
    {
      property: 'og:image',
      content: ogImage.value
    },
    {
      name: 'twitter:card',
      content: 'summary_large_image'
    },
    {
      name: 'twitter:title',
      content: supplier.value?.meta_title || supplier.value?.store_name || ''
    },
    {
      name: 'twitter:description',
      content: supplier.value?.meta_description || supplier.value?.description || ''
    },
    {
      name: 'twitter:image',
      content: ogImage.value
    }
  ],
  link: [
    { rel: 'canonical', href: canonicalUrl.value }
  ],
  ...(organizationSchema.value || breadcrumbSchema.value ? {
    script: prepareSchemaScripts([
      ...(organizationSchema.value ? [organizationSchema.value] : []),
      ...(breadcrumbSchema.value ? [breadcrumbSchema.value] : [])
    ])
  } : {})
}))

const fetchSupplier = async () => {
  loading.value = true
  error.value = null

  try {
    const id = route.params.id

    // #region agent log
    try {
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'suppliers/[id].vue:613',message:'fetchSupplier called',data:{id,hasUser:!!authStore.user,hasToken:!!authStore.token,vendorProfileId:authStore.vendorProfile?.id},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{})
    } catch {}
    // #endregion

    // Refresh user data if authenticated to ensure we have latest vendor profile
    if (typeof window !== 'undefined' && authStore.token) {
      if (!authStore.user || authStore.vendorProfile?.id === parseInt(id as string)) {
        // Refresh if no user loaded, or if viewing own profile to get latest data
        await authStore.fetchCurrentUser()
      }
    }

    // Use single source of truth from store
    const vendorProfile = authStore.vendorProfile
    const isOwner = vendorProfile?.id === parseInt(id as string)

    // #region agent log
    try {
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'suppliers/[id].vue:628',message:'checking owner status',data:{isOwner,vendorProfileId:vendorProfile?.id,requestedId:id,vendorProfileApproved:vendorProfile?.is_approved},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{})
    } catch {}
    // #endregion

    if (isOwner && vendorProfile) {
      // #region agent log
      try {
        fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'suppliers/[id].vue:629',message:'using owner profile',data:{},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{})
      } catch {}
      // #endregion
      supplier.value = vendorProfile

      await Promise.all([
        fetchProducts(id as string),
        fetchPortfolio(id as string),
        fetchTeam(id as string),
        fetchComments(id as string)
      ])
    } else {
      // #region agent log
      try {
        fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'suppliers/[id].vue:638',message:'calling supplierApi.getSupplier',data:{},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{})
      } catch {}
      // #endregion
      supplier.value = await supplierApi.getSupplier(id as string)

      await Promise.all([
        fetchProducts(id as string),
        fetchPortfolio(id as string),
        fetchTeam(id as string),
        fetchComments(id as string)
      ])
    }
  } catch (err: any) {
    console.error('Error fetching supplier:', err)
    const statusCode = err?.response?.status || err?.statusCode || err?.status
    if (statusCode === 404) {
      const errorMessage = err?.data?.detail || err?.response?.data?.detail || err?.message
      error.value = errorMessage || 'صفحه تامین‌کننده یافت نشد یا هنوز تایید نشده است.'
    } else {
      const errorMessage = err?.data?.detail || err?.response?.data?.detail || err?.data?.error || err?.message
      error.value = errorMessage || 'خطا در بارگذاری اطلاعات تامین‌کننده'
    }
  } finally {
    loading.value = false
  }
}

const fetchProducts = async (id: string) => {
  productsLoading.value = true
  try {
    const response = await supplierApi.getSupplierProducts(id, 1)
    // Handle paginated response
    if (response && typeof response === 'object' && 'results' in response) {
      products.value = response.results || []
    } else if (Array.isArray(response)) {
      // Fallback for non-paginated response (backward compatibility)
      products.value = response
    } else {
      products.value = []
    }
  } catch (err) {
    console.error('Error fetching products:', err)
    products.value = []
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

const scrollToSection = (section: string) => {
  activeSection.value = section

  setTimeout(() => {
    const element = document.querySelector(
      `[data-section="${section}"]`
    )
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    } else if (section === 'contact' && contactSection.value) {
      contactSection.value?.$el.scrollIntoView({ behavior: 'smooth' })
    }
  }, 100)
}

const scrollToContact = () => {
  scrollToSection('contact')
}

const handleAddToCart = (product: any) => {
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

onMounted(() => {
  fetchSupplier()
})
</script>

<style scoped>
.supplier-page {
  --brand-primary: rgb(var(--v-theme-primary));
  --brand-secondary: rgb(var(--v-theme-secondary));
  min-height: 100vh;
  background: #fafafa;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  gap: 1rem;
}

/* Error State */
.error-state {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-card {
  border: 2px solid rgb(var(--v-theme-error));
}

/* Hero Section */
.hero-section {
  position: relative;
  background: white;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background-size: cover;
  background-position: center;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(255, 255, 255, 0.95));
}

.hero-content {
  position: relative;
  z-index: 1;
}

.logo-avatar {
  border: 4px solid white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

/* Navigation Tabs */
.nav-tabs {
  background: white !important;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.nav-tab {
  min-width: auto !important;
  text-transform: none;
  font-weight: 500;
}

/* Main Content */
.main-content {
  max-width: 1200px;
}

/* Metrics */
.metric-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
  transition: all 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.87);
  margin: 0.25rem 0;
}

.metric-label {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
}

/* Content Cards */
.content-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

.content-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.content-text {
  line-height: 1.8;
  white-space: pre-line;
  color: rgba(0, 0, 0, 0.87);
}

/* Section Title */
.section-title {
  display: flex;
  align-items: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.87);
}

/* Comment Card */
.comment-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

.comment-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.supplier-reply {
  background: rgba(var(--v-theme-primary), 0.05);
  border-radius: 8px;
  border-right: 3px solid rgb(var(--v-theme-primary));
}

/* Floating Contact Button */
.floating-contact-btn {
  position: fixed;
  bottom: 24px;
  left: 24px;
  z-index: 100;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
}

.floating-contact-btn:hover {
  transform: scale(1.05);
}

/* Mobile Optimizations */
@media (max-width: 600px) {
  .hero-bg,
  .hero-overlay {
    height: 150px;
  }

  .logo-avatar {
    width: 80px !important;
    height: 80px !important;
  }

  .metric-value {
    font-size: 1.5rem;
  }

  .metric-label {
    font-size: 0.813rem;
  }

  .section-title {
    font-size: 1.125rem;
  }

  .floating-contact-btn {
    bottom: 16px;
    left: 16px;
  }
}

/* Tablet & Up */
@media (min-width: 960px) {
  .main-content {
    padding-top: 2rem;
    padding-bottom: 2rem;
  }
}

/* Print */
@media print {
  .nav-tabs,
  .floating-contact-btn {
    display: none;
  }

  .supplier-page {
    background: white;
  }
}
</style>
