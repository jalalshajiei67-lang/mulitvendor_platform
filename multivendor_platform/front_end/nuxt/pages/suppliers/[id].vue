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
        </div>
        <div class="loading-text mt-6">
          <h3 class="text-h6 font-weight-bold">در حال بارگذاری...</h3>
        </div>
      </div>
    </div>

    <!-- Enhanced Error State -->
    <div v-else-if="error" class="error-container">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8" lg="6">
            <v-card elevation="0" class="error-card" rounded="lg">
              <v-card-text class="text-center pa-8">
                <v-icon size="72" color="error" class="mb-4 d-block">
                  mdi-alert-circle
                </v-icon>
                <h2 class="text-h5 font-weight-bold mb-4 text-error">
                  خطا در بارگذاری
                </h2>
                <p class="text-body-1 mb-6 line-height-relaxed">
                  {{ error }}
                </p>
                <v-btn
                  color="primary"
                  size="large"
                  class="px-8"
                  @click="fetchSupplier"
                  rounded="lg"
                  elevation="2"
                >
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
        @contact-click="scrollToContact"
      />

      <!-- Navigation Bar -->
      <div class="navigation-container">
        <v-container>
          <!-- Desktop Navigation -->
          <div class="desktop-nav d-none d-md-block">
            <div class="nav-wrapper">
              <button
                v-for="section in availableSections"
                :key="section.value"
                class="nav-button"
                :class="{ active: activeSection === section.value }"
                @click="scrollToSection(section.value)"
              >
                <v-icon size="28" class="me-3">{{ section.icon }}</v-icon>
                <span class="nav-label">{{ section.label }}</span>
              </button>
            </div>
          </div>

          <!-- Mobile Navigation -->
          <div class="mobile-nav-selector d-md-none">
            <v-select
              :model-value="activeSection"
              :items="mobileNavItems"
              variant="outlined"
              density="comfortable"
              class="mobile-nav-select"
              hide-details
              rounded="lg"
              bg-color="white"
              @update:model-value="scrollToSection"
            >
              <template v-slot:selection="{ item }">
                <div class="d-flex align-center gap-2">
                  <v-icon :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                  <span class="font-weight-500">{{ item.title }}</span>
                </div>
              </template>
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" rounded="lg">
                  <template v-slot:prepend>
                    <v-icon :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                  </template>
                  <v-list-item-title class="font-weight-500">
                    {{ item.title }}
                  </v-list-item-title>
                </v-list-item>
              </template>
            </v-select>
          </div>
        </v-container>
      </div>

      <!-- Main Content Area -->
      <div class="main-content">
        <!-- Company Information Section -->
        <v-container v-if="activeSection === 'about'" class="py-8 py-md-12" data-section="about">
          <v-row :gutter="6">
            <!-- Main Content -->
            <v-col cols="12" md="8">
              <!-- About Section -->
              <div class="content-section mb-8">
                <div class="section-header">
                  <h2 class="section-title mb-6">درباره {{ supplier.store_name }}</h2>
                  <div class="title-decoration"></div>
                </div>
                <v-card elevation="0" class="content-card" rounded="lg">
                  <v-card-text class="pa-6 pa-md-8">
                    <p class="readable-text" style="white-space: pre-line;">
                      {{ supplier.about || supplier.description || 'اطلاعاتی در دسترس نیست.' }}
                    </p>
                  </v-card-text>
                </v-card>
              </div>

              <!-- Work Resume -->
              <div v-if="supplier.work_resume" class="content-section mb-8">
                <div class="section-header">
                  <h3 class="section-title-sm mb-6">رزومه کاری</h3>
                  <div class="title-decoration"></div>
                </div>
                <v-card elevation="0" class="content-card" rounded="lg">
                  <v-card-text class="pa-6 pa-md-8">
                    <p class="readable-text" style="white-space: pre-line;">
                      {{ supplier.work_resume }}
                    </p>
                  </v-card-text>
                </v-card>
              </div>

              <!-- History -->
              <div v-if="supplier.history" class="content-section">
                <div class="section-header">
                  <h3 class="section-title-sm mb-6">تاریخچه</h3>
                  <div class="title-decoration"></div>
                </div>
                <v-card elevation="0" class="content-card" rounded="lg">
                  <v-card-text class="pa-6 pa-md-8">
                    <p class="readable-text" style="white-space: pre-line;">
                      {{ supplier.history }}
                    </p>
                  </v-card-text>
                </v-card>
              </div>
            </v-col>

            <!-- Sidebar - Contact Info -->
            <v-col cols="12" md="4">
              <div class="sticky-sidebar">
                <!-- Quick Contact Card -->
                <v-card elevation="0" class="contact-card" rounded="lg">
                  <v-card-text class="pa-6">
                    <h3 class="text-h6 font-weight-bold mb-6 text-center">
                      اطلاعات تماس
                    </h3>

                    <!-- Contact Items -->
                    <div class="contact-item mb-5 pb-5" v-if="supplier.contact_phone">
                      <div class="d-flex align-start gap-4">
                        <div class="contact-icon-wrapper">
                          <v-icon size="24" color="white">mdi-phone</v-icon>
                        </div>
                        <div class="flex-grow-1">
                          <p class="text-caption text-medium-emphasis mb-2">شماره تماس</p>
                          <p class="text-body-1 font-weight-600">{{ supplier.contact_phone }}</p>
                        </div>
                      </div>
                    </div>

                    <v-divider v-if="supplier.contact_phone" class="my-4"></v-divider>

                    <div class="contact-item mb-5 pb-5" v-if="supplier.contact_email">
                      <div class="d-flex align-start gap-4">
                        <div class="contact-icon-wrapper">
                          <v-icon size="24" color="white">mdi-email</v-icon>
                        </div>
                        <div class="flex-grow-1">
                          <p class="text-caption text-medium-emphasis mb-2">ایمیل</p>
                          <p class="text-body-1 font-weight-600 break-all">
                            {{ supplier.contact_email }}
                          </p>
                        </div>
                      </div>
                    </div>

                    <v-divider v-if="supplier.contact_email" class="my-4"></v-divider>

                    <div class="contact-item" v-if="supplier.address">
                      <div class="d-flex align-start gap-4">
                        <div class="contact-icon-wrapper">
                          <v-icon size="24" color="white">mdi-map-marker</v-icon>
                        </div>
                        <div class="flex-grow-1">
                          <p class="text-caption text-medium-emphasis mb-2">آدرس</p>
                          <p class="text-body-1 font-weight-600">{{ supplier.address }}</p>
                        </div>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>

                <!-- CTA Button -->
                <v-btn
                  block
                  color="primary"
                  size="x-large"
                  class="mt-6 font-weight-bold contact-btn"
                  prepend-icon="mdi-email"
                  @click="activeSection = 'contact'"
                  rounded="lg"
                  elevation="2"
                >
                  ارسال پیام
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </v-container>

        <!-- Products Section -->
        <v-container v-if="activeSection === 'products'" class="py-8 py-md-12" data-section="products">
          <div class="section-header mb-8">
            <h2 class="section-title">محصولات</h2>
            <div class="title-decoration"></div>
          </div>
          <SupplierProductCatalog
            :products="products"
            :loading="productsLoading"
            @add-to-cart="handleAddToCart"
          />
        </v-container>

        <!-- Portfolio Section -->
        <v-container v-if="activeSection === 'portfolio'" class="py-8 py-md-12" data-section="portfolio">
          <div class="section-header mb-8">
            <h2 class="section-title">نمونه کارها</h2>
            <div class="title-decoration"></div>
          </div>
          <SupplierPortfolio
            :items="portfolioItems"
            :loading="portfolioLoading"
          />
        </v-container>

        <!-- Team Section -->
        <v-container v-if="activeSection === 'team'" class="py-8 py-md-12" data-section="team">
          <div class="section-header mb-8">
            <h2 class="section-title">تیم ما</h2>
            <div class="title-decoration"></div>
          </div>
          <SupplierTeam
            :members="teamMembers"
            :loading="teamLoading"
          />
        </v-container>

        <!-- Certifications Section -->
        <v-container v-if="activeSection === 'certifications'" class="py-8 py-md-12" data-section="certifications">
          <div class="section-header mb-8">
            <h2 class="section-title">گواهینامه‌ها و جوایز</h2>
            <div class="title-decoration"></div>
          </div>
          <SupplierCertifications
            :certifications="supplier.certifications"
            :awards="supplier.awards"
          />
        </v-container>

        <!-- Reviews Section -->
        <v-container v-if="activeSection === 'reviews'" class="py-8 py-md-12" data-section="reviews">
          <div class="section-header mb-8">
            <h2 class="section-title">نظرات مشتریان</h2>
            <div class="title-decoration"></div>
          </div>

          <v-row v-if="comments.length > 0" :gutter="6">
            <v-col
              v-for="comment in comments"
              :key="comment.id"
              cols="12"
              md="6"
            >
              <v-card elevation="0" class="comment-card" rounded="lg">
                <v-card-text class="pa-6">
                  <!-- Comment Header -->
                  <div class="d-flex justify-space-between align-start mb-4">
                    <div class="d-flex align-center flex-grow-1">
                      <v-avatar size="48" color="primary" class="me-3">
                        <span class="text-white text-subtitle-1 font-weight-bold">
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
                    <div class="rating-container">
                      <v-rating
                        :model-value="comment.rating"
                        readonly
                        density="compact"
                        color="amber"
                        size="small"
                      ></v-rating>
                      <span class="rating-value">{{ comment.rating }}</span>
                    </div>
                  </div>

                  <!-- Comment Content -->
                  <h4 v-if="comment.title" class="text-body-1 font-weight-bold mb-3">
                    {{ comment.title }}
                  </h4>
                  <p class="text-body-2 mb-4 line-height-relaxed">
                    {{ comment.comment }}
                  </p>

                  <!-- Supplier Reply -->
                  <div v-if="comment.supplier_reply" class="supplier-reply mt-4 pt-4">
                    <p class="text-caption font-weight-bold text-primary mb-3">
                      <v-icon size="small" class="me-1">mdi-store</v-icon>
                      پاسخ فروشنده
                    </p>
                    <p class="text-body-2 line-height-relaxed">
                      {{ comment.supplier_reply }}
                    </p>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Empty State -->
          <v-row v-else justify="center" class="my-12">
            <v-col cols="12" class="text-center">
              <v-icon size="64" color="grey-lighten-2" class="mb-4 d-block">
                mdi-comment-off
              </v-icon>
              <h3 class="text-h6">نظری ثبت نشده است</h3>
            </v-col>
          </v-row>
        </v-container>

        <!-- Contact Section -->
        <v-container v-if="activeSection === 'contact'" class="py-8 py-md-12" data-section="contact">
          <div class="section-header mb-8">
            <h2 class="section-title">تماس با ما</h2>
            <div class="title-decoration"></div>
          </div>
          <SupplierContact ref="contactSection" :supplier="supplier" />
        </v-container>
      </div>

      <!-- Fixed Contact Button for Mobile -->
      <v-btn
        v-if="$vuetify.display.mdAndDown"
        class="fixed-contact-btn"
        color="primary"
        icon="mdi-phone"
        size="large"
        elevation="6"
        @click="activeSection = 'contact'"
      ></v-btn>
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

const activeSection = ref('about')
const contactSection = ref()

// Simplified mobile navigation
const mobileNavItems = computed(() => {
  const sections = [
    { title: 'درباره شرکت', value: 'about', icon: 'mdi-information', color: 'primary' }
  ]

  if (products.value.length > 0) {
    sections.push({
      title: 'محصولات',
      value: 'products',
      icon: 'mdi-package-variant',
      color: 'primary'
    })
  }

  if (portfolioItems.value.length > 0) {
    sections.push({
      title: 'نمونه کارها',
      value: 'portfolio',
      icon: 'mdi-briefcase',
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

  if (hasCertifications.value) {
    sections.push({
      title: 'گواهینامه‌ها',
      value: 'certifications',
      icon: 'mdi-certificate',
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
    { value: 'about', label: 'درباره شرکت', icon: 'mdi-information' }
  ]

  if (products.value.length > 0) {
    sections.push({ value: 'products', label: 'محصولات', icon: 'mdi-package-variant' })
  }
  if (portfolioItems.value.length > 0) {
    sections.push({ value: 'portfolio', label: 'نمونه کارها', icon: 'mdi-briefcase' })
  }
  if (teamMembers.value.length > 0) {
    sections.push({ value: 'team', label: 'تیم ما', icon: 'mdi-account-group' })
  }
  if (hasCertifications.value) {
    sections.push({ value: 'certifications', label: 'گواهینامه‌ها', icon: 'mdi-certificate' })
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
  background: #f8f9fa;
  position: relative;
  overflow-x: hidden;
  font-size: 16px;
}

/* Loading State */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}

.loading-content {
  text-align: center;
  padding: 2rem;
}

.main-spinner {
  position: relative;
  z-index: 2;
}

.loading-text {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Error State */
.error-container {
  padding: 3rem 1rem;
}

.error-card {
  border: 2px solid rgba(var(--v-theme-error), 0.1);
  background: white;
}

/* Simplified Navigation */
.navigation-container {
  position: sticky;
  top: 64px;
  z-index: 10;
  background: white;
  border-bottom: 3px solid rgba(var(--v-theme-primary), 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.desktop-nav {
  width: 100%;
}

.nav-wrapper {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding: 1rem;
}

.nav-wrapper::-webkit-scrollbar {
  height: 4px;
}

.nav-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.nav-wrapper::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.3);
  border-radius: 2px;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  border: none;
  background: transparent;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.6);
  transition: all 0.3s ease;
  white-space: nowrap;
  border-bottom: 4px solid transparent;
}

.nav-button:hover {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
}

.nav-button.active {
  color: rgb(var(--v-theme-primary));
  border-bottom-color: rgb(var(--v-theme-primary));
  background: rgba(var(--v-theme-primary), 0.08);
}

.nav-label {
  font-weight: 700;
}

/* Mobile Navigation */
.mobile-nav-selector {
  padding: 1rem;
}

.mobile-nav-select {
  font-size: 16px;
}

.mobile-nav-select :deep(.v-field) {
  border-radius: 12px;
  border: 2px solid #e0e0e0;
}

/* Main Content */
.main-content {
  min-height: 50vh;
  animation: fadeIn 0.3s ease-out;
}

/* Section Headers */
.section-header {
  position: relative;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.95);
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 1;
}

.section-title-sm {
  font-size: 1.5rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.95);
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 1;
}

.title-decoration {
  height: 8px;
  width: 80px;
  background: rgb(var(--v-theme-primary));
  border-radius: 4px;
  margin-top: -0.5rem;
}

/* Content Sections */
.content-section {
  width: 100%;
}

/* Content Cards */
.content-card {
  background: white;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.content-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Readable Text */
.readable-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: rgba(0, 0, 0, 0.87);
  word-spacing: 0.05em;
}

.line-height-relaxed {
  line-height: 1.8;
}

/* Contact Card */
.sticky-sidebar {
  position: sticky;
  top: 250px;
  transition: all 0.3s ease;
}

@media (max-width: 960px) {
  .sticky-sidebar {
    position: relative;
    top: 0;
  }
}

.contact-card {
  background: white;
  border: 2px solid rgba(var(--v-theme-primary), 0.15);
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.contact-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.3);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.1);
}

.contact-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgb(var(--v-theme-primary));
  flex-shrink: 0;
}

.contact-item {
  transition: all 0.3s ease;
}

.contact-item:hover {
  padding-right: 12px;
}

.contact-btn {
  font-size: 1.1rem;
  padding: 16px;
}

/* Comment Card */
.comment-card {
  background: white;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.comment-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.rating-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-value {
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: 2px;
}

.supplier-reply {
  background: rgba(var(--v-theme-primary), 0.08);
  padding: 12px;
  border-radius: 8px;
  border-right: 3px solid rgb(var(--v-theme-primary));
}

/* Fixed Contact Button */
.fixed-contact-btn {
  position: fixed;
  bottom: 24px;
  left: 24px;
  z-index: 100;
  width: 64px;
  height: 64px;
}

/* Typography */
.font-weight-bold {
  font-weight: 700;
}

.font-weight-600 {
  font-weight: 600;
}

.font-weight-500 {
  font-weight: 500;
}

.text-h5 {
  font-size: 1.5rem;
  font-weight: 700;
}

.text-h6 {
  font-size: 1.25rem;
  font-weight: 700;
}

.text-body-1 {
  font-size: 1rem;
  line-height: 1.6;
}

.text-body-2 {
  font-size: 0.95rem;
  line-height: 1.6;
}

.text-caption {
  font-size: 0.85rem;
}

.text-subtitle-1 {
  font-size: 1rem;
  font-weight: 500;
}

/* Spacing Utilities */
.gap-2 {
  gap: 8px;
}

.gap-4 {
  gap: 16px;
}

.break-all {
  word-break: break-all;
}

/* Smooth Scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.4);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.6);
}

/* Mobile Responsive */
@media (max-width: 600px) {
  .supplier-mini-website {
    font-size: 15px;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .section-title-sm {
    font-size: 1.25rem;
  }

  .nav-button {
    padding: 12px 16px;
    font-size: 14px;
  }

  .readable-text {
    font-size: 1rem;
    line-height: 1.7;
  }

  .sticky-sidebar {
    margin-top: 2rem;
  }

  .contact-card {
    margin-top: 2rem;
  }

  .fixed-contact-btn {
    bottom: 16px;
    left: 16px;
    width: 56px;
    height: 56px;
  }
}

@media (max-width: 400px) {
  .nav-button {
    padding: 10px 14px;
    font-size: 13px;
  }

  .nav-icon {
    display: none;
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