<template>
  <div class="supplier-mini-website" dir="rtl" :style="brandingStyles">
    <!-- Loading State -->
    <v-container v-if="loading" class="my-8">
      <v-row justify="center">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-row>
    </v-container>

    <!-- Error State -->
    <v-container v-else-if="error">
      <v-alert type="error" variant="tonal" prominent class="my-4">
        <v-row align="center">
          <v-col>
            <div class="text-h6">{{ error }}</div>
            <v-btn color="error" variant="text" prepend-icon="mdi-refresh" @click="fetchSupplier" class="mt-2">
              تلاش مجدد
            </v-btn>
          </v-col>
        </v-row>
      </v-alert>
    </v-container>

    <!-- Supplier Mini Website Content -->
    <div v-else-if="supplier">
      <!-- Hero Section -->
      <SupplierHero
        :supplier="supplier"
        @contact-click="scrollToContact"
      />

      <!-- Navigation Tabs -->
      <v-container class="tabs-container">
        <v-tabs
          v-model="activeTab"
          :bg-color="supplier.brand_color_primary || 'primary'"
          color="white"
          align-tabs="center"
          show-arrows
          class="mini-website-tabs"
        >
          <v-tab value="overview">
            <v-icon start>mdi-information</v-icon>
            معرفی
          </v-tab>
          <v-tab value="products" v-if="products.length > 0">
            <v-icon start>mdi-package-variant</v-icon>
            محصولات
            <v-badge :content="products.length" color="white" text-color="primary" inline class="ms-2"></v-badge>
          </v-tab>
          <v-tab value="portfolio" v-if="portfolioItems.length > 0">
            <v-icon start>mdi-briefcase</v-icon>
            نمونه کارها
          </v-tab>
          <v-tab value="team" v-if="teamMembers.length > 0">
            <v-icon start>mdi-account-group</v-icon>
            تیم ما
          </v-tab>
          <v-tab value="certifications" v-if="hasCertifications">
            <v-icon start>mdi-certificate</v-icon>
            گواهینامه‌ها
          </v-tab>
          <v-tab value="reviews" v-if="comments.length > 0">
            <v-icon start>mdi-star</v-icon>
            نظرات
            <v-badge :content="comments.length" color="white" text-color="primary" inline class="ms-2"></v-badge>
          </v-tab>
          <v-tab value="contact">
            <v-icon start>mdi-email</v-icon>
            تماس با ما
          </v-tab>
        </v-tabs>
      </v-container>

      <!-- Tab Content -->
      <v-window v-model="activeTab" class="tab-content">
        <!-- Overview Tab -->
        <v-window-item value="overview">
          <v-container class="py-8">
            <v-row>
              <v-col cols="12" md="8">
                <v-card elevation="2" class="mb-4">
                  <v-card-title class="text-h5 font-weight-bold">
                    <v-icon color="primary" class="me-2">mdi-information</v-icon>
                    درباره {{ supplier.store_name }}
                  </v-card-title>
                  <v-card-text>
                    <p class="text-body-1" style="white-space: pre-line; line-height: 1.8;">
                      {{ supplier.about || supplier.description || 'اطلاعاتی در دسترس نیست.' }}
                    </p>
                  </v-card-text>
                </v-card>

                <v-card v-if="supplier.work_resume" elevation="2" class="mb-4">
                  <v-card-title class="text-h6 font-weight-bold">
                    <v-icon color="primary" class="me-2">mdi-file-document</v-icon>
                    رزومه کاری
                  </v-card-title>
                  <v-card-text>
                    <p class="text-body-2" style="white-space: pre-line;">
                      {{ supplier.work_resume }}
                    </p>
                  </v-card-text>
                </v-card>

                <v-card v-if="supplier.history" elevation="2" class="mb-4">
                  <v-card-title class="text-h6 font-weight-bold">
                    <v-icon color="primary" class="me-2">mdi-history</v-icon>
                    تاریخچه
                  </v-card-title>
                  <v-card-text>
                    <p class="text-body-2" style="white-space: pre-line;">
                      {{ supplier.history }}
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" md="4">
                <v-card elevation="2" class="sticky-sidebar">
                  <v-card-title class="text-h6 font-weight-bold">اطلاعات تماس سریع</v-card-title>
                  <v-list>
                    <v-list-item v-if="supplier.contact_email" prepend-icon="mdi-email">
                      <v-list-item-title>{{ supplier.contact_email }}</v-list-item-title>
                    </v-list-item>
                    <v-list-item v-if="supplier.contact_phone" prepend-icon="mdi-phone">
                      <v-list-item-title>{{ supplier.contact_phone }}</v-list-item-title>
                    </v-list-item>
                    <v-list-item v-if="supplier.address" prepend-icon="mdi-map-marker">
                      <v-list-item-title>{{ supplier.address }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                  <v-card-actions>
                    <v-btn block color="primary" prepend-icon="mdi-email" @click="activeTab = 'contact'">
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
          <v-container class="py-8">
            <h2 class="text-h4 font-weight-bold text-center mb-6">نظرات مشتریان</h2>
            
            <v-row v-if="comments.length > 0">
              <v-col
                v-for="comment in comments"
                :key="comment.id"
                cols="12"
                md="6"
              >
                <v-card elevation="2" class="comment-card">
                  <v-card-text>
                    <div class="d-flex justify-space-between align-center mb-2">
                      <div class="d-flex align-center">
                        <v-avatar size="40" color="primary" class="me-2">
                          <span class="text-white">{{ comment.user_username.charAt(0).toUpperCase() }}</span>
                        </v-avatar>
                        <div>
                          <div class="font-weight-bold">{{ comment.user_username }}</div>
                          <div class="text-caption text-medium-emphasis">
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
                      ></v-rating>
                    </div>
                    <p v-if="comment.title" class="font-weight-bold mb-1">{{ comment.title }}</p>
                    <p class="text-body-2">{{ comment.comment }}</p>
                    <v-divider v-if="comment.supplier_reply" class="my-2"></v-divider>
                    <div v-if="comment.supplier_reply" class="supplier-reply">
                      <div class="text-caption text-medium-emphasis mb-1">پاسخ فروشنده:</div>
                      <p class="text-body-2">{{ comment.supplier_reply }}</p>
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
      // For public access, use the regular API (only approved suppliers)
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
    if (err?.response?.status === 404) {
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

onMounted(() => {
  fetchSupplier()
})
</script>

<style scoped>
.supplier-mini-website {
  --brand-primary: rgb(var(--v-theme-primary));
  --brand-secondary: rgb(var(--v-theme-secondary));
  min-height: 100vh;
  background: linear-gradient(to bottom, rgba(var(--v-theme-surface), 0.5), rgb(var(--v-theme-surface)));
}

.tabs-container {
  position: sticky;
  top: 64px;
  z-index: 10;
  background: rgb(var(--v-theme-surface));
  padding-top: 1rem;
  padding-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mini-website-tabs {
  border-radius: 12px;
  overflow: hidden;
}

.tab-content {
  min-height: 60vh;
}

.sticky-sidebar {
  position: sticky;
  top: 200px;
}

.comment-card {
  border-radius: 12px;
  height: 100%;
}

.supplier-reply {
  background-color: rgba(var(--v-theme-primary), 0.05);
  padding: 12px;
  border-radius: 8px;
  border-left: 3px solid var(--brand-primary);
}
</style>
