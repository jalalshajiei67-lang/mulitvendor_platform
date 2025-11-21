<template>
  <div class="supplier-mini-website" dir="rtl" :style="brandingStyles">
    <!-- Enhanced Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-content">
        <v-progress-circular
          indeterminate
          color="primary"
          size="100"
          width="8"
        ></v-progress-circular>
        <h3 class="text-h4 font-weight-bold mt-8">لطفاً صبر کنید...</h3>
        <p class="text-h6 mt-4 text-medium-emphasis">در حال آماده‌سازی صفحه</p>
      </div>
    </div>

    <!-- Enhanced Error State -->
    <div v-else-if="error" class="error-container">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <v-card elevation="4" class="error-card pa-8" rounded="xl">
              <v-card-text class="text-center pa-8">
                <v-icon size="100" color="error" class="mb-6">
                  mdi-alert-circle-outline
                </v-icon>
                <h2 class="text-h3 font-weight-bold mb-6 text-error">
                  مشکلی پیش آمده
                </h2>
                <p class="text-h6 mb-8">
                  {{ error }}
                </p>
                <v-btn
                  color="primary"
                  size="x-large"
                  class="px-12 text-h6"
                  @click="fetchSupplier"
                  rounded="xl"
                  elevation="4"
                >
                  <v-icon start size="28">mdi-refresh</v-icon>
                  تلاش مجدد
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Supplier Mini Website Content -->
    <div v-else-if="supplier">
      <!-- Simplified Hero Section -->
      <SupplierHero
        :supplier="supplier"
        :available-sections="availableSections"
        :mobile-nav-items="mobileNavItems"
        :active-section="activeSection"
        @contact-click="scrollToContact"
        @section-click="scrollToSection"
      />

      <!-- Main Content Area -->
      <div class="main-content">
        <!-- Home Section -->
        <v-container v-if="activeSection === 'home'" class="py-8 py-md-12" data-section="home">
          <!-- Logo, Metrics, and Action Buttons -->
          <v-row align="center" justify="center" class="home-hero-content mb-12">
            <!-- Logo -->
            <v-col cols="12" md="4" class="text-center logo-section">
              <div class="logo-container">
                <v-avatar
                  :size="display.xs.value ? 140 : 200"
                  class="hero-logo elevation-12"
                  rounded="lg"
                >
                  <v-img
                    v-if="supplier.logo"
                    :src="supplier.logo"
                    cover
                  >
                    <template v-slot:placeholder>
                      <v-skeleton-loader type="avatar" />
                    </template>
                  </v-img>
                  <v-icon v-else :size="display.xs.value ? 70 : 100" color="white">
                    mdi-store
                  </v-icon>
                </v-avatar>

                <!-- Trust Indicators -->
                <div class="trust-indicators mt-6">
                  <v-chip
                    v-if="(supplier as any).is_verified"
                    color="success"
                    size="large"
                    variant="elevated"
                    class="me-3 mb-3 pa-6"
                  >
                    <v-icon start size="28">mdi-check-decagram</v-icon>
                    <span class="text-h6 font-weight-bold">فروشنده معتبر</span>
                  </v-chip>
                  <v-chip
                    v-if="(supplier as any).is_featured"
                    color="amber"
                    size="large"
                    variant="elevated"
                    class="mb-3 pa-6"
                  >
                    <v-icon start size="28">mdi-star</v-icon>
                    <span class="text-h6 font-weight-bold">فروشنده برتر</span>
                  </v-chip>
                </div>
              </div>
            </v-col>

            <!-- Store Info -->
            <v-col cols="12" md="8">
              <div class="store-info">
                <p v-if="supplier.description" class="store-description text-h5 mb-8 line-height-relaxed">
                  {{ supplier.description }}
                </p>

                <!-- Key Metrics -->
                <v-row class="metrics mt-8" justify="center" justify-md="start">
                  <v-col cols="12" sm="6" md="3" v-if="supplier.year_established">
                    <v-card class="metric-card metric-card-1 pa-6 pa-md-8 text-center" elevation="3" rounded="xl">
                      <v-icon size="64" class="metric-icon mb-4" color="indigo">mdi-calendar-check</v-icon>
                      <div class="metric-value text-h2 font-weight-black mb-2">
                        {{ yearsOfExperience }}
                      </div>
                      <div class="metric-label text-h6 font-weight-bold">سال سابقه کار</div>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6" md="3" v-if="supplier.employee_count">
                    <v-card class="metric-card metric-card-2 pa-6 pa-md-8 text-center" elevation="3" rounded="xl">
                      <v-icon size="64" class="metric-icon mb-4" color="pink">mdi-account-group</v-icon>
                      <div class="metric-value text-h2 font-weight-black mb-2">
                        {{ supplier.employee_count }}
                      </div>
                      <div class="metric-label text-h6 font-weight-bold">نفر پرسنل</div>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <v-card class="metric-card metric-card-3 pa-6 pa-md-8 text-center" elevation="3" rounded="xl">
                      <v-icon size="64" class="metric-icon mb-4" color="amber">mdi-star</v-icon>
                      <div class="metric-value text-h2 font-weight-black mb-2">
                        {{ supplier.rating_average || 0 }}
                      </div>
                      <div class="metric-label text-h6 font-weight-bold">امتیاز مشتریان</div>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <v-card class="metric-card metric-card-4 pa-6 pa-md-8 text-center" elevation="3" rounded="xl">
                      <v-icon size="64" class="metric-icon mb-4" color="green">mdi-package-variant</v-icon>
                      <div class="metric-value text-h2 font-weight-black mb-2">
                        {{ supplier.product_count || 0 }}
                      </div>
                      <div class="metric-label text-h6 font-weight-bold">تنوع محصولات</div>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </v-col>
          </v-row>

          <!-- About Section -->
          <div class="content-section mb-16">
            <div class="section-header mb-10">
              <v-icon size="48" color="primary" class="mb-4">mdi-information</v-icon>
              <h2 class="section-title text-h3 font-weight-black mb-4">معرفی {{ supplier.store_name }}</h2>
            </div>
            <v-card elevation="4" class="content-card" rounded="xl" color="blue-grey-lighten-5">
              <v-card-text class="pa-8 pa-md-12">
                <p class="readable-text text-h5" style="white-space: pre-line;">
                  {{ supplier.about || supplier.description || 'اطلاعاتی در دسترس نیست.' }}
                </p>
              </v-card-text>
            </v-card>
          </div>

          <!-- Work Resume -->
          <div v-if="supplier.work_resume" class="content-section mb-16">
            <div class="section-header mb-10">
              <v-icon size="48" color="primary" class="mb-4">mdi-briefcase</v-icon>
              <h3 class="section-title text-h3 font-weight-black mb-4">پروژه‌ها و تجربیات</h3>
            </div>
            <v-card elevation="4" class="content-card" rounded="xl" color="green-lighten-5">
              <v-card-text class="pa-8 pa-md-12">
                <p class="readable-text text-h5" style="white-space: pre-line;">
                  {{ supplier.work_resume }}
                </p>
              </v-card-text>
            </v-card>
          </div>

          <!-- History -->
          <div v-if="supplier.history" class="content-section mb-16">
            <div class="section-header mb-10">
              <v-icon size="48" color="primary" class="mb-4">mdi-history</v-icon>
              <h3 class="section-title text-h3 font-weight-black mb-4">داستان ما</h3>
            </div>
            <v-card elevation="4" class="content-card" rounded="xl" color="amber-lighten-5">
              <v-card-text class="pa-8 pa-md-12">
                <p class="readable-text text-h5" style="white-space: pre-line;">
                  {{ supplier.history }}
                </p>
              </v-card-text>
            </v-card>
          </div>

          <!-- Portfolio Section -->
          <div v-if="portfolioItems.length > 0" class="content-section mb-16">
            <div class="section-header mb-10">
              <v-icon size="48" color="primary" class="mb-4">mdi-image-multiple</v-icon>
              <h2 class="section-title text-h3 font-weight-black mb-4">نمونه کارهای ما</h2>
              <p class="text-h6 text-medium-emphasis">پروژه‌هایی که با موفقیت انجام داده‌ایم</p>
            </div>
            <SupplierPortfolio
              :items="portfolioItems"
              :loading="portfolioLoading"
            />
          </div>

          <!-- Certifications Section -->
          <div v-if="hasCertifications" class="content-section mb-16">
            <div class="section-header mb-10">
              <v-icon size="48" color="primary" class="mb-4">mdi-certificate</v-icon>
              <h2 class="section-title text-h3 font-weight-black mb-4">مدارک و افتخارات</h2>
              <p class="text-h6 text-medium-emphasis">گواهی‌های رسمی و جوایز دریافتی</p>
            </div>
            <SupplierCertifications
              :certifications="supplier.certifications"
              :awards="supplier.awards"
            />
          </div>

          <!-- Empty State -->
          <div v-if="portfolioItems.length === 0 && !hasCertifications" class="text-center py-16">
            <v-icon size="120" color="grey-lighten-1" class="mb-6">
              mdi-folder-open-outline
            </v-icon>
            <h3 class="text-h4 font-weight-bold mb-4">در حال آماده‌سازی</h3>
            <p class="text-h6 text-medium-emphasis">
              به زودی نمونه کارها و گواهینامه‌ها اضافه می‌شوند
            </p>
          </div>
        </v-container>

        <!-- Products Section -->
        <v-container v-if="activeSection === 'products'" class="py-12 py-md-16" data-section="products">
          <div class="section-header mb-10 text-center">
            <v-icon size="56" color="primary" class="mb-4">mdi-shopping</v-icon>
            <h2 class="section-title text-h2 font-weight-black mb-4">محصولات ما</h2>
            <p class="text-h6 text-medium-emphasis">انتخاب کنید و سفارش دهید</p>
          </div>
          <SupplierProductCatalog
            :products="products"
            :loading="productsLoading"
            @add-to-cart="handleAddToCart"
          />
        </v-container>

        <!-- Team Section -->
        <v-container v-if="activeSection === 'team'" class="py-12 py-md-16" data-section="team">
          <div class="section-header mb-10 text-center">
            <v-icon size="56" color="primary" class="mb-4">mdi-account-group</v-icon>
            <h2 class="section-title text-h2 font-weight-black mb-4">تیم ما را بشناسید</h2>
            <p class="text-h6 text-medium-emphasis">همکاران ما که برای شما تلاش می‌کنند</p>
          </div>
          <SupplierTeam
            :members="teamMembers"
            :loading="teamLoading"
          />
        </v-container>

        <!-- Reviews Section -->
        <v-container v-if="activeSection === 'reviews'" class="py-12 py-md-16" data-section="reviews">
          <div class="section-header mb-10 text-center">
            <v-icon size="56" color="primary" class="mb-4">mdi-comment-quote</v-icon>
            <h2 class="section-title text-h2 font-weight-black mb-4">نظر مشتریان درباره ما</h2>
            <p class="text-h6 text-medium-emphasis">تجربه دیگران از همکاری با ما</p>
          </div>

          <v-row v-if="comments.length > 0">
            <v-col
              v-for="comment in comments"
              :key="comment.id"
              cols="12"
            >
              <v-card elevation="4" class="comment-card mb-6" rounded="xl">
                <v-card-text class="pa-8 pa-md-10">
                  <!-- Comment Header -->
                  <div class="d-flex justify-space-between align-start mb-6">
                    <div class="d-flex align-center flex-grow-1">
                      <v-avatar size="72" color="primary" class="me-4">
                        <span class="text-white text-h4 font-weight-bold">
                          {{ comment.user_username.charAt(0).toUpperCase() }}
                        </span>
                      </v-avatar>
                      <div>
                        <p class="font-weight-bold text-h5 mb-2">
                          {{ comment.user_username }}
                        </p>
                        <p class="text-h6 text-medium-emphasis">
                          {{ formatDate(comment.created_at) }}
                        </p>
                      </div>
                    </div>
                    <div class="rating-container">
                      <v-rating
                        :model-value="comment.rating"
                        readonly
                        color="amber"
                        size="large"
                      ></v-rating>
                      <span class="rating-value text-h5 font-weight-bold mt-2">{{ comment.rating }} از ۵</span>
                    </div>
                  </div>

                  <!-- Comment Content -->
                  <h4 v-if="comment.title" class="text-h5 font-weight-bold mb-4">
                    {{ comment.title }}
                  </h4>
                  <p class="text-h6 mb-6 line-height-relaxed">
                    {{ comment.comment }}
                  </p>

                  <!-- Supplier Reply -->
                  <div v-if="comment.supplier_reply" class="supplier-reply mt-6 pt-6">
                    <p class="text-h6 font-weight-bold text-primary mb-4">
                      <v-icon size="28" class="me-2">mdi-reply</v-icon>
                      پاسخ فروشنده:
                    </p>
                    <p class="text-h6 line-height-relaxed">
                      {{ comment.supplier_reply }}
                    </p>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Empty State -->
          <v-row v-else justify="center" class="my-16">
            <v-col cols="12" class="text-center">
              <v-icon size="120" color="grey-lighten-1" class="mb-6">
                mdi-comment-off-outline
              </v-icon>
              <h3 class="text-h3 font-weight-bold mb-4">هنوز نظری ثبت نشده</h3>
              <p class="text-h6 text-medium-emphasis">اولین نفری باشید که نظر می‌دهد</p>
            </v-col>
          </v-row>
        </v-container>

        <!-- Contact Section -->
        <v-container v-if="activeSection === 'contact'" class="py-12 py-md-16" data-section="contact">
          <div class="section-header mb-10 text-center">
            <v-icon size="56" color="primary" class="mb-4">mdi-phone-in-talk</v-icon>
            <h2 class="section-title text-h2 font-weight-black mb-4">تماس با ما</h2>
            <p class="text-h6 text-medium-emphasis">برای سفارش و مشاوره با ما در ارتباط باشید</p>
          </div>
          <SupplierContact ref="contactSection" :supplier="supplier" />
        </v-container>
      </div>

      <!-- Fixed Contact Button for Mobile -->
      <v-btn
        v-if="display.mdAndDown.value"
        class="fixed-contact-btn"
        color="primary"
        size="x-large"
        elevation="8"
        rounded="xl"
        @click="activeSection = 'contact'"
      >
        <v-icon size="32" class="me-2">mdi-phone</v-icon>
        <span class="text-h6 font-weight-bold">تماس</span>
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
import { useSupplierApi, type Supplier, type SupplierComment } from '~/composables/useSupplierApi'
import { useSupplierPortfolioApi, type SupplierPortfolioItem } from '~/composables/useSupplierPortfolioApi'
import { useSupplierTeamApi, type SupplierTeamMember } from '~/composables/useSupplierTeamApi'

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

const loading = ref(false)
const productsLoading = ref(false)
const portfolioLoading = ref(false)
const teamLoading = ref(false)
const error = ref<string | null>(null)

const activeSection = ref('home')
const contactSection = ref()

// Simplified mobile navigation
const mobileNavItems = computed(() => {
  const sections = [
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

// Simplified available sections
const availableSections = computed(() => {
  const sections = [
    { value: 'home', label: 'خانه', icon: 'mdi-home' }
  ]

  if (products.value.length > 0) {
    sections.push({ value: 'products', label: 'محصولات', icon: 'mdi-package-variant' })
  }
  if (teamMembers.value.length > 0) {
    sections.push({ value: 'team', label: 'تیم ما', icon: 'mdi-account-group' })
  }
  if (comments.value.length > 0) {
    sections.push({ value: 'reviews', label: 'نظرات', icon: 'mdi-star' })
  }
  sections.push({ value: 'contact', label: 'تماس با ما', icon: 'mdi-email' })

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

const hasCertifications = computed(() => {
  return (supplier.value?.certifications && supplier.value.certifications.length > 0) ||
         (supplier.value?.awards && supplier.value.awards.length > 0)
})

// Calculate years of experience based on Hijri/Jalaali calendar
const yearsOfExperience = computed(() => {
  if (!supplier.value?.year_established) return 0
  
  // Get current Gregorian date
  const now = new Date()
  
  // Convert to Jalaali
  const currentJalaali = toJalaali(now.getFullYear(), now.getMonth() + 1, now.getDate())
  const currentYear = currentJalaali.jy
  
  // Calculate difference (both are in Jalaali/Hijri calendar)
  const years = currentYear - supplier.value.year_established
  
  return years > 0 ? years : 0
})

useHead(() => ({
  title: supplier.value?.meta_title || supplier.value?.store_name || 'تامین‌کننده',
  meta: [
    {
      name: 'description',
      content: supplier.value?.meta_description || supplier.value?.description || ''
    },
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

    if (typeof window !== 'undefined' && !authStore.user && authStore.token) {
      await authStore.fetchCurrentUser()
    }

    const isOwner = authStore.user?.vendor_profile?.id === parseInt(id as string)

    if (isOwner && authStore.user?.vendor_profile) {
      supplier.value = authStore.user.vendor_profile

      await Promise.all([
        fetchProducts(id as string),
        fetchPortfolio(id as string),
        fetchTeam(id as string),
        fetchComments(id as string)
      ])
    } else {
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

const scrollToSection = (section: string) => {
  activeSection.value = section
  // Smooth scroll to section after a brief delay to ensure DOM update
  setTimeout(() => {
    const element = document.querySelector(`[data-section="${section}"]`)
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
.supplier-mini-website {
  --brand-primary: rgb(var(--v-theme-primary));
  --brand-secondary: rgb(var(--v-theme-secondary));
  min-height: 100vh;
  background: linear-gradient(to bottom, #f5f5f5 0%, #fafafa 100%);
  position: relative;
  overflow-x: hidden;
  font-size: 18px;
  line-height: 1.8;
}

/* Loading State */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  flex-direction: column;
}

.loading-content {
  text-align: center;
  padding: 3rem;
}

/* Error State */
.error-container {
  padding: 4rem 2rem;
}

.error-card {
  background: white;
  border: 3px solid rgba(var(--v-theme-error), 0.2);
}

/* Main Content */
.main-content {
  min-height: 50vh;
}

/* Section Headers */
.section-header {
  position: relative;
  text-align: center;
}

.section-title {
  color: rgba(0, 0, 0, 0.9);
  line-height: 1.4;
}

/* Content Sections */
.content-section {
  width: 100%;
}

/* Content Cards */
.content-card {
  background: white;
  border: 2px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.content-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* Readable Text */
.readable-text {
  line-height: 2;
  color: rgba(0, 0, 0, 0.87);
  word-spacing: 0.1em;
  letter-spacing: 0.02em;
}

.line-height-relaxed {
  line-height: 2;
}


/* Comment Card */
.comment-card {
  background: white;
  border: 2px solid rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.comment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.rating-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-value {
  font-weight: 700;
  color: rgba(0, 0, 0, 0.87);
}

.supplier-reply {
  background: rgba(var(--v-theme-primary), 0.1);
  padding: 1.5rem;
  border-radius: 16px;
  border-right: 5px solid rgb(var(--v-theme-primary));
}

/* Fixed Contact Button */
.fixed-contact-btn {
  position: fixed;
  bottom: 32px;
  left: 32px;
  z-index: 100;
  padding: 1.5rem 2.5rem !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25) !important;
}

.fixed-contact-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.5);
  border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.7);
}

/* Home Hero Content Styles */
.home-hero-content {
  padding: 3rem 0;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-logo {
  border: 6px solid rgba(var(--v-theme-primary), 0.3);
  background: white;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

.hero-logo:hover {
  transform: scale(1.03);
}

.trust-indicators {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.store-info {
  text-align: center;
}

@media (min-width: 960px) {
  .store-info {
    text-align: right;
  }
}

.store-description {
  color: rgba(0, 0, 0, 0.87);
  max-width: 900px;
  line-height: 2;
  margin: 0 auto;
  font-weight: 500;
}

@media (min-width: 960px) {
  .store-description {
    margin: 0;
  }
}

/* Metrics */
.metrics {
  margin-top: 3rem;
  gap: 1.5rem;
}

.metric-card {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 3px solid !important;
  background: white !important;
}

.metric-card:hover {
  transform: translateY(-8px);
}

.metric-card-1 {
  border-color: rgb(var(--v-theme-indigo)) !important;
}

.metric-card-1:hover {
  background: rgb(var(--v-theme-indigo-lighten-5)) !important;
}

.metric-card-2 {
  border-color: rgb(var(--v-theme-pink)) !important;
}

.metric-card-2:hover {
  background: rgb(var(--v-theme-pink-lighten-5)) !important;
}

.metric-card-3 {
  border-color: rgb(var(--v-theme-amber)) !important;
}

.metric-card-3:hover {
  background: rgb(var(--v-theme-amber-lighten-5)) !important;
}

.metric-card-4 {
  border-color: rgb(var(--v-theme-green)) !important;
}

.metric-card-4:hover {
  background: rgb(var(--v-theme-green-lighten-5)) !important;
}

.metric-icon {
  opacity: 0.9;
}

.metric-value {
  color: rgba(0, 0, 0, 0.9);
}

.metric-label {
  color: rgba(0, 0, 0, 0.7);
  letter-spacing: 0.5px;
}


/* Mobile Responsive */
@media (max-width: 600px) {
  .supplier-mini-website {
    font-size: 17px;
  }

  .section-title {
    font-size: 2rem !important;
  }

  .readable-text {
    font-size: 1.125rem !important;
    line-height: 2;
  }

  .fixed-contact-btn {
    bottom: 20px;
    left: 20px;
    padding: 1.25rem 2rem !important;
  }

  .metrics {
    margin-top: 2rem;
    gap: 1rem;
  }

  .hero-logo {
    border-width: 4px !important;
  }

  .trust-indicators {
    gap: 0.75rem;
  }

  .store-description {
    font-size: 1.125rem !important;
  }

  .content-card {
    margin-bottom: 1rem;
  }
}

/* Print Styles */
@media print {
  .supplier-mini-website {
    background: white;
  }

  .navigation-container {
    display: none;
  }

  .fixed-contact-btn {
    display: none;
  }
}
</style>