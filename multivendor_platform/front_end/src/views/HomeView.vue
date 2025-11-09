<template>
  <div class="home" dir="rtl">
    <!-- Hero Section with Large Search -->
    <v-container fluid class="hero-section pa-0">
      <v-row no-gutters justify="center" align="center" class="hero-content">
        <v-col cols="12" md="10" lg="8" class="pa-4 pa-md-8">
          <!-- Large Search Box -->
          <div class="search-wrapper" ref="searchContainer">
            <v-card 
              elevation="8" 
              rounded="xl" 
              class="search-card pa-4 pa-md-6 mb-4"
              color="surface"
            >
              <v-card-text class="pa-0">
                <v-text-field
                  v-model="searchQuery"
                  placeholder="چه دستگاهی نیاز دارید؟"
                  append-inner-icon="mdi-magnify"
                  variant="outlined"
                  rounded="lg"
                  hide-details
                  class="home-search-input"
                  density="comfortable"
                  @focus="isSearchFocused = true"
                  @keydown.enter.prevent="performSearch"
                  @keydown.escape="closeAutocomplete"
                  @click:append-inner="performSearch"
                  @update:model-value="onSearchQueryChange"
                >
                </v-text-field>
              </v-card-text>
            </v-card>

            <!-- Autocomplete Dropdown -->
            <transition name="dropdown">
              <v-card
                v-if="showAutocomplete && (hasResults || isLoadingSearch)"
                elevation="8"
                rounded="lg"
                class="autocomplete-dropdown"
              >
                <!-- Loading State -->
                <div v-if="isLoadingSearch" class="search-loading pa-4">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    size="24"
                    class="mr-2"
                  ></v-progress-circular>
                  <span>در حال جستجو...</span>
                </div>

                <!-- No Results -->
                <div v-else-if="!hasResults && searchQuery.length >= 2" class="no-results pa-4 text-center">
                  <p class="text-body-2 text-medium-emphasis">نتیجه‌ای یافت نشد</p>
                </div>

                <!-- Results -->
                <div v-else-if="hasResults" class="results-container">
                  <!-- Products -->
                  <div v-if="searchResults.products && searchResults.products.length > 0" class="result-section">
                    <div class="section-title pa-2 text-caption font-weight-bold">
                      محصولات
                    </div>
                    <router-link
                      v-for="product in searchResults.products"
                      :key="'product-' + product.id"
                      :to="product.slug ? `/products/${product.slug}` : `/products/${product.id}`"
                      @click="closeAutocomplete"
                      class="result-item"
                    >
                      <div class="result-image">
                        <img 
                          v-if="product.primary_image" 
                          :src="product.primary_image" 
                          :alt="product.name"
                        />
                        <div v-else class="placeholder-image">
                          <v-icon size="small">mdi-image</v-icon>
                        </div>
                      </div>
                      <div class="result-content">
                        <div class="result-title">{{ product.name }}</div>
                        <div class="result-meta">
                          <v-chip size="x-small" color="primary" variant="flat">محصول</v-chip>
                          <span class="result-price">{{ formatPrice(product.price) }} تومان</span>
                        </div>
                      </div>
                    </router-link>
                  </div>

                  <!-- Blogs -->
                  <div v-if="searchResults.blogs && searchResults.blogs.length > 0" class="result-section">
                    <div class="section-title pa-2 text-caption font-weight-bold">
                      وبلاگ
                    </div>
                    <router-link
                      v-for="blog in searchResults.blogs"
                      :key="'blog-' + blog.id"
                      :to="`/blog/${blog.slug}`"
                      @click="closeAutocomplete"
                      class="result-item"
                    >
                      <div class="result-image">
                        <img 
                          v-if="blog.featured_image" 
                          :src="blog.featured_image" 
                          :alt="blog.title"
                        />
                        <div v-else class="placeholder-image">
                          <v-icon size="small">mdi-file-document</v-icon>
                        </div>
                      </div>
                      <div class="result-content">
                        <div class="result-title">{{ blog.title }}</div>
                        <div class="result-meta">
                          <v-chip size="x-small" color="purple" variant="flat">وبلاگ</v-chip>
                          <span class="result-excerpt">{{ truncate(blog.excerpt, 60) }}</span>
                        </div>
                      </div>
                    </router-link>
                  </div>

                  <!-- View All Results Link -->
                  <div v-if="searchResults.total > totalDisplayed" class="view-all pa-2 text-center">
                    <v-btn
                      variant="text"
                      size="small"
                      @click="performSearch"
                      class="text-caption"
                    >
                      مشاهده همه نتایج ({{ searchResults.total - totalDisplayed }} نتیجه دیگر)
                    </v-btn>
                  </div>
                </div>
              </v-card>
            </transition>
          </div>

          <!-- Subtitle -->
          <p class="search-subtitle text-center text-body-1 text-md-h6">
            از بین تولیدات بهترین تولید کنندگان ماشین آلات نیاز خود را جستجو کنید
          </p>
        </v-col>
      </v-row>
    </v-container>

    <!-- Indexo for Buyers Section -->
    <v-container class="buyers-section py-8 py-md-12">
      <v-card 
        elevation="4" 
        rounded="xl" 
        class="section-card buyers-card"
        color="info"
      >
        <v-card-title class="section-title text-h4 text-md-h3 text-center pa-6 pa-md-8">
          <v-icon size="large" class="ml-2">mdi-account-group</v-icon>
          ایندکسو برای خریداران
        </v-card-title>

        <v-card-text class="pa-4 pa-md-6">
          <!-- Advantages Grid -->
          <v-row class="advantages-grid mb-6">
            <v-col 
              v-for="(advantage, index) in buyerAdvantages" 
              :key="index"
              cols="12" 
              sm="6" 
              md="4"
              class="d-flex justify-center"
            >
              <v-card 
                elevation="2" 
                rounded="lg" 
                class="advantage-card pa-4 pa-md-6 text-center"
                color="surface"
              >
                <v-icon 
                  :icon="advantage.icon" 
                  size="64" 
                  :color="advantage.color"
                  class="mb-4"
                ></v-icon>
                <h3 class="text-h6 text-md-h5 font-weight-bold mb-3">
                  {{ advantage.title }}
                </h3>
                <p class="text-body-2 text-md-body-1 text-medium-emphasis">
                  {{ advantage.description }}
                </p>
              </v-card>
            </v-col>
          </v-row>

          <!-- CTA Section -->
          <v-card 
            elevation="2" 
            rounded="lg" 
            class="cta-card pa-4 pa-md-6 mb-4"
            color="surface"
          >
            <v-row align="center" no-gutters>
              <v-col cols="12" md="8" class="pa-2 pa-md-4">
                <p class="text-body-1 text-md-h6 mb-0">
                  همین الان درخواست خودت را ثبت کن و منتظر تماس تامین کنندگان معتبر باش
                </p>
              </v-col>
              <v-col cols="12" md="4" class="pa-2 pa-md-4 text-center text-md-end">
                <v-btn
                  color="primary"
                  size="large"
                  rounded="lg"
                  elevation="2"
                  prepend-icon="mdi-file-document-edit"
                  @click="handleBuyerCTA"
                  block
                  class="cta-button"
                >
                  ثبت درخواست
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </v-card-text>
      </v-card>
    </v-container>

    <!-- Indexo for Sellers Section -->
    <v-container class="sellers-section py-8 py-md-12">
      <v-card 
        elevation="4" 
        rounded="xl" 
        class="section-card sellers-card"
        color="success"
      >
        <v-card-title class="section-title text-h4 text-md-h3 text-center pa-6 pa-md-8">
          <v-icon size="large" class="ml-2">mdi-store</v-icon>
          ایندکسو برای فروشندگان
        </v-card-title>

        <v-card-text class="pa-4 pa-md-6">
          <!-- Advantages Grid -->
          <v-row class="advantages-grid mb-6">
            <v-col 
              v-for="(advantage, index) in sellerAdvantages" 
              :key="index"
              cols="12" 
              sm="6" 
              md="4"
              class="d-flex justify-center"
            >
              <v-card 
                elevation="2" 
                rounded="lg" 
                class="advantage-card pa-4 pa-md-6 text-center"
                color="surface"
              >
                <v-icon 
                  :icon="advantage.icon" 
                  size="64" 
                  :color="advantage.color"
                  class="mb-4"
                ></v-icon>
                <h3 class="text-h6 text-md-h5 font-weight-bold mb-3">
                  {{ advantage.title }}
                </h3>
                <p class="text-body-2 text-md-body-1 text-medium-emphasis">
                  {{ advantage.description }}
                </p>
              </v-card>
            </v-col>
          </v-row>

          <!-- CTA Section -->
          <v-card 
            elevation="2" 
            rounded="lg" 
            class="cta-card pa-4 pa-md-6 mb-4"
            color="surface"
          >
            <v-row align="center" no-gutters>
              <v-col cols="12" md="8" class="pa-2 pa-md-4">
                <p class="text-body-1 text-md-h6 mb-0">
                  برای شروع همکاری و بهره بردن از امکانات ایندکسو ثبت نام کنید
                </p>
              </v-col>
              <v-col cols="12" md="4" class="pa-2 pa-md-4 text-center text-md-end">
                <v-btn
                  color="primary"
                  size="large"
                  rounded="lg"
                  elevation="2"
                  prepend-icon="mdi-account-plus"
                  @click="handleSellerCTA"
                  block
                  class="cta-button"
                >
                  ثبت نام بعنوان تامین کننده
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'
import { debounce } from '@/composables/useDebounce'

const router = useRouter()
const route = useRoute()

// Search state
const searchQuery = ref('')
const searchResults = ref({ products: [], blogs: [], total: 0 })
const isLoadingSearch = ref(false)
const isSearchFocused = ref(false)
const searchContainer = ref(null)

// Buyer Advantages
const buyerAdvantages = [
  {
    icon: 'mdi-account-switch',
    title: 'ارتباط مستقیم',
    description: 'بدون واسطه و اصطکاک، مستقیماً با تامین‌کنندگان معتبر در ارتباط باشید',
    color: 'info'
  },
  {
    icon: 'mdi-shield-check',
    title: 'تامین‌کنندگان معتبر',
    description: 'از بین بهترین تولیدکنندگان ماشین‌آلات، تامین‌کننده مناسب خود را پیدا کنید',
    color: 'success'
  },
  {
    icon: 'mdi-lightning-bolt',
    title: 'مسیر کوتاه خرید',
    description: 'فرآیند خرید را کوتاه کرده و سریع‌تر به محصول مورد نظر خود برسید',
    color: 'warning'
  }
]

// Seller Advantages
const sellerAdvantages = [
  {
    icon: 'mdi-cash',
    title: 'هزینه کم',
    description: 'با حداقل هزینه، محصولات خود را به خریداران هدف معرفی کنید',
    color: 'success'
  },
  {
    icon: 'mdi-chart-line',
    title: 'فروش آسان',
    description: 'مدل کسب‌وکار بدون زحمت و با حداقل تلاش برای افزایش فروش',
    color: 'primary'
  },
  {
    icon: 'mdi-handshake',
    title: 'دسترسی به خریداران',
    description: 'مستقیماً با خریداران واقعی در صنعت ماشین‌آلات ارتباط برقرار کنید',
    color: 'info'
  }
]

// Computed properties
const showAutocomplete = computed(() => {
  return isSearchFocused.value && searchQuery.value.length >= 2
})

const hasResults = computed(() => {
  return searchResults.value.total > 0
})

const totalDisplayed = computed(() => {
  return (searchResults.value.products?.length || 0) + (searchResults.value.blogs?.length || 0)
})

// Debounced search function for autocomplete
const performAutocompleteSearch = debounce(async (query) => {
  if (!query || query.length < 2) {
    searchResults.value = { products: [], blogs: [], total: 0 }
    isLoadingSearch.value = false
    return
  }

  isLoadingSearch.value = true
  try {
    const response = await api.globalSearch(query, 5)
    searchResults.value = response.data
  } catch (error) {
    console.error('Search error:', error)
    searchResults.value = { products: [], blogs: [], total: 0 }
  } finally {
    isLoadingSearch.value = false
  }
}, 300) // 300ms debounce

// Handle search query changes
const onSearchQueryChange = () => {
  if (searchQuery.value.length >= 2) {
    performAutocompleteSearch(searchQuery.value)
  } else {
    searchResults.value = { products: [], blogs: [], total: 0 }
    isLoadingSearch.value = false
  }
}

// Perform full search and navigate to products page
const performSearch = () => {
  if (!searchQuery.value || !searchQuery.value.trim()) {
    return
  }

  closeAutocomplete()
  router.push({
    path: '/products',
    query: { search: searchQuery.value.trim() }
  })
}

// Close autocomplete dropdown
const closeAutocomplete = () => {
  isSearchFocused.value = false
}

// Helper functions
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price)
}

const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

// Click outside to close autocomplete
const handleClickOutside = (event) => {
  if (searchContainer.value && !searchContainer.value.contains(event.target)) {
    closeAutocomplete()
  }
}

// Initialize search query from URL params
const initializeFromRoute = () => {
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
}

// Watch for route changes to update search query
watch(() => route.query.search, (newSearch) => {
  if (newSearch && newSearch !== searchQuery.value) {
    searchQuery.value = newSearch
  }
})

// Lifecycle hooks
onMounted(() => {
  initializeFromRoute()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// CTA handlers
const handleBuyerCTA = () => {
  // Navigate to # as placeholder
  window.location.href = '#'
}

const handleSellerCTA = () => {
  // Navigate to register page
  router.push('/register')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  direction: rtl;
  background-color: #F5F5F5;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #1565C0 0%, #0277BD 100%);
  min-height: 400px;
  display: flex;
  align-items: center;
  padding: 60px 20px;
}

@media (min-width: 960px) {
  .hero-section {
    min-height: 500px;
  }
}

.hero-content {
  width: 100%;
}

.search-wrapper {
  position: relative;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
}

.search-card {
  max-width: 100%;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.home-search-input :deep(.v-field) {
  font-size: 1.125rem;
  padding: 12px 16px;
}

@media (min-width: 960px) {
  .home-search-input :deep(.v-field) {
    font-size: 1.25rem;
    padding: 16px 20px;
  }
}

.home-search-input :deep(.v-field__input) {
  min-height: 56px;
  text-align: right;
  direction: rtl;
}

@media (min-width: 960px) {
  .home-search-input :deep(.v-field__input) {
    min-height: 64px;
  }
}

/* Magnifier icon sizing */
.home-search-input :deep(.v-field__append-inner .v-icon) {
  font-size: 32px !important;
  width: 32px !important;
  height: 32px !important;
  margin-right: 5 px !important;
  margin-left: 10 px !important;
}

@media (min-width: 960px) {
  .home-search-input :deep(.v-field__append-inner .v-icon) {
    font-size: 40px !important;
    width: 40px !important;
    height: 40px !important;
    margin-right: 10px !important;
  }
}

.search-subtitle {
  color: white;
  opacity: 0.95;
  font-weight: 400;
  margin-top: 24px;
}

/* Autocomplete Dropdown */
.autocomplete-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  left: 0;
  max-height: 500px;
  overflow-y: auto;
  z-index: 1000;
  margin-top: 0;
  direction: rtl;
}

.search-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #666;
}

.no-results {
  color: #999;
}

.results-container {
  padding: 0;
}

.result-section {
  border-bottom: 1px solid #f0f0f0;
}

.result-section:last-child {
  border-bottom: none;
}

.section-title {
  background-color: #f8f9fa;
  color: #666;
  border-bottom: 1px solid #e0e0e0;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  text-decoration: none;
  color: #333;
  transition: background-color 0.2s;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background-color: #f8f9fa;
}

.result-image {
  width: 50px;
  height: 50px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e0e0e0;
  color: #999;
}

.result-content {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-weight: 500;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.9rem;
}

.result-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: #666;
}

.result-price {
  font-weight: 500;
  color: #2c3e50;
}

.result-excerpt {
  color: #999;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.view-all {
  background-color: #f8f9fa;
  border-top: 1px solid #e0e0e0;
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Scrollbar styling */
.autocomplete-dropdown :deep(.v-card-text),
.autocomplete-dropdown {
  scrollbar-width: thin;
  scrollbar-color: #ccc #f1f1f1;
}

.autocomplete-dropdown::-webkit-scrollbar {
  width: 6px;
}

.autocomplete-dropdown::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.autocomplete-dropdown::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}

.autocomplete-dropdown::-webkit-scrollbar-thumb:hover {
  background: #999;
}

/* Section Cards */
.section-card {
  max-width: 1200px;
  margin: 0 auto;
}

.buyers-card {
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
  border-left: 4px solid #1565C0;
}

.sellers-card {
  background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
  border-left: 4px solid #FF6F00;
}

.section-title {
  color: #212121;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Advantages Grid */
.advantages-grid {
  margin-top: 24px;
}

.advantage-card {
  height: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.advantage-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}

/* CTA Cards */
.cta-card {
  background: white;
}

.cta-button {
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Mobile Responsive */
@media (max-width: 959px) {
  .hero-section {
    padding: 40px 16px;
    min-height: 350px;
  }

  .search-card {
    padding: 16px !important;
  }

  .autocomplete-dropdown {
    max-height: 400px;
  }

  .section-title {
    font-size: 1.75rem !important;
    flex-direction: column;
    gap: 8px;
  }

  .advantage-card {
    margin-bottom: 16px;
  }

  .cta-card .v-row {
    flex-direction: column-reverse;
  }

  .cta-card .v-col {
    text-align: center !important;
  }
}

/* RTL Support */
:deep(.v-field__prepend-inner) {
  padding-left: 12px;
  padding-right: 0;
}

:deep(.v-field__append-inner) {
  padding-right: 16px;
  padding-left: 0;
}
</style>
