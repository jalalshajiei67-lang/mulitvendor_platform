<template>
  <div class="home" dir="rtl">
    <!-- Background Decorative Shapes -->
    <div class="background-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
    </div>

    <!-- Hero Section -->
    <section class="hero-section">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <v-card elevation="8" rounded="xl" class="hero-card pa-6 pa-md-8" color="surface">
              <div class="hero-content">
                <h1 class="hero-title text-h3 text-md-h2 font-weight-bold text-center mb-4">
                  ارتباط با تامین‌کنندگان برتر ماشین‌آلات در سراسر کشور
                </h1>
                <p class="hero-subtitle text-body-1 text-md-h6 text-center mb-6">
                  تجهیزات مناسب برای نیازهای کسب‌وکار خود را پیدا کنید
                </p>

                <!-- Search Container -->
                <div class="search-wrapper" ref="searchContainer">
                  <v-text-field
                    v-model="searchQuery"
                    placeholder="جستجوی ماشین‌آلات، تجهیزات، قطعات..."
                    append-inner-icon="mdi-magnify"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    class="hero-search-input mb-6"
                    density="comfortable"
                    @focus="isSearchFocused = true"
                    @keydown.enter.prevent="performSearch"
                    @keydown.escape="closeAutocomplete"
                    @click:append-inner="performSearch"
                    @update:model-value="onSearchQueryChange"
                  />

                  <!-- Autocomplete Dropdown -->
                  <transition name="dropdown">
                    <v-card
                      v-if="showAutocomplete && (hasResults || isLoadingSearch)"
                      elevation="8"
                      rounded="lg"
                      class="autocomplete-dropdown"
                    >
                      <div v-if="isLoadingSearch" class="search-loading pa-4">
                        <v-progress-circular indeterminate color="primary" size="24" class="mr-2" />
                        <span>در حال جستجو...</span>
                      </div>

                      <div v-else-if="!hasResults && searchQuery.length >= 2" class="no-results pa-4 text-center">
                        <p class="text-body-2 text-medium-emphasis">نتیجه‌ای یافت نشد</p>
                      </div>

                      <div v-else-if="hasResults" class="results-container">
                        <div
                          v-if="searchResults.products && searchResults.products.length > 0"
                          class="result-section"
                        >
                          <div class="section-label pa-2 text-caption font-weight-bold">محصولات</div>
                          <NuxtLink
                            v-for="product in searchResults.products"
                            :key="`product-${product.id}`"
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
                                <span class="result-price">
                                  {{ product.price ? formatPrice(product.price) : 'تماس بگیرید' }}
                                </span>
                              </div>
                            </div>
                          </NuxtLink>
                        </div>

                        <div
                          v-if="searchResults.blogs && searchResults.blogs.length > 0"
                          class="result-section"
                        >
                          <div class="section-label pa-2 text-caption font-weight-bold">وبلاگ</div>
                          <NuxtLink
                            v-for="blog in searchResults.blogs"
                            :key="`blog-${blog.id}`"
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
                          </NuxtLink>
                        </div>

                        <div v-if="searchResults.total > totalDisplayed" class="view-all pa-2 text-center">
                          <v-btn variant="text" size="small" @click="performSearch" class="text-caption">
                            مشاهده همه نتایج ({{ searchResults.total - totalDisplayed }} نتیجه دیگر)
                          </v-btn>
                        </div>
                      </div>
                    </v-card>
                  </transition>
                </div>

                <!-- Hero Buttons -->
                <div class="hero-buttons d-flex flex-column flex-sm-row gap-3 justify-center">
                  <v-btn
                    color="primary"
                    size="x-large"
                    rounded="lg"
                    elevation="4"
                    prepend-icon="mdi-cart"
                    @click="navigateToProducts"
                  >
                    مشاهده محصولات
                  </v-btn>
                  <v-btn
                    color="primary"
                    size="x-large"
                    rounded="lg"
                    variant="outlined"
                    prepend-icon="mdi-storefront"
                    @click="handleSellerCTA"
                  >
                    فروشنده شوید
                  </v-btn>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Popular Categories Section -->
    <v-container class="categories-section py-8 py-md-12">
      <h2 class="section-title text-h3 text-md-h2 font-weight-bold mb-8">دسته‌بندی‌های محبوب</h2>
      
      <v-row>
        <v-col
          v-for="(category, index) in categories"
          :key="`category-${index}`"
          cols="6"
          sm="4"
          md="4"
          lg="2"
        >
          <v-card
            elevation="2"
            rounded="lg"
            class="category-card pa-4 text-center"
            color="surface"
            hover
            @click="navigateToCategory(category)"
          >
            <v-icon :icon="category.icon" size="48" color="primary" class="mb-3" />
            <h3 class="category-title text-body-1 font-weight-bold">
              {{ category.title }}
            </h3>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Verification Section -->
    <v-container class="verification-section py-8 py-md-12">
      <v-card elevation="4" rounded="xl" class="verification-card pa-6 pa-md-8" color="surface">
        <v-row align="center">
          <v-col cols="12" md="5">
            <h3 class="text-h4 text-md-h3 font-weight-bold mb-3">تامین‌کنندگان معتبر</h3>
            <p class="text-body-1 text-md-h6 text-medium-emphasis">
              تمام تامین‌کنندگان ما از فرآیند احراز هویت دقیق عبور می‌کنند
            </p>
          </v-col>
          
          <v-col cols="12" md="7">
            <v-row>
              <v-col
                v-for="(badge, index) in verificationBadges"
                :key="`badge-${index}`"
                cols="4"
                class="text-center"
              >
                <div class="badge-wrapper">
                  <div class="badge-icon-container mb-3 mx-auto">
                    <v-icon :icon="badge.icon" size="40" color="primary" />
                  </div>
                  <p class="badge-text text-body-2 font-weight-medium">{{ badge.text }}</p>
                </div>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-container>

    <!-- Platform Statistics Section -->
    <v-container class="statistics-section py-8 py-md-12">
      <h2 class="section-title text-h3 text-md-h2 font-weight-bold mb-8 text-center">آمار پلتفرم</h2>
      
      <v-row>
        <v-col
          v-for="(stat, index) in statistics"
          :key="`stat-${index}`"
          cols="6"
          sm="6"
          md="3"
        >
          <v-card
            elevation="2"
            rounded="lg"
            class="stat-card pa-6 text-center"
            color="surface"
          >
            <div class="stat-number text-h3 text-md-h2 font-weight-bold mb-2" style="color: rgb(var(--v-theme-primary))">
              {{ stat.number }}
            </div>
            <div class="stat-label text-body-2 text-md-body-1 text-medium-emphasis">
              {{ stat.label }}
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { debounce } from '@/composables/useDebounce'

definePageMeta({
  layout: 'default',
  title: 'خانه'
})

useSeoMeta({
  title: 'خانه',
  ogTitle: 'ایندکسو | پلتفرم چندفروشنده',
  description:
    'ایندکسو پلتفرمی برای اتصال خریداران و فروشندگان در بازار B2B است که بر تجربه فارسی و سئو تمرکز دارد.',
  ogDescription:
    'با ایندکسو فروشگاه چندفروشنده خود را بسازید، مدیریت کنید و مشتریان بیشتری جذب کنید.',
  ogImage: '/favicon.ico',
  ogType: 'website'
})

const router = useRouter()
const route = useRoute()
const { globalSearch } = useSearchApi()

type SearchResponse = Awaited<ReturnType<typeof globalSearch>>

const searchQuery = ref<string>('')
const searchResults = ref<SearchResponse extends Promise<infer R> ? R : SearchResponse>({
  products: [],
  blogs: [],
  total: 0
})
const isLoadingSearch = ref(false)
const isSearchFocused = ref(false)
const searchContainer = ref<HTMLElement | null>(null)

// Categories Data
const categories = [
  {
    icon: 'mdi-hammer-wrench',
    title: 'تجهیزات ساختمانی',
    slug: 'construction'
  },
  {
    icon: 'mdi-cog',
    title: 'ماشین‌آلات تولیدی',
    slug: 'manufacturing'
  },
  {
    icon: 'mdi-tractor',
    title: 'تجهیزات کشاورزی',
    slug: 'agriculture'
  },
  {
    icon: 'mdi-forklift',
    title: 'حمل و نقل مواد',
    slug: 'material-handling'
  },
  {
    icon: 'mdi-tools',
    title: 'ابزارآلات صنعتی',
    slug: 'industrial-tools'
  },
  {
    icon: 'mdi-factory',
    title: 'تجهیزات فرآوری',
    slug: 'processing'
  }
]

// Verification Badges
const verificationBadges = [
  {
    icon: 'mdi-shield-check',
    text: 'گواهی کیفیت'
  },
  {
    icon: 'mdi-security',
    text: 'تضمین معامله'
  },
  {
    icon: 'mdi-clock-check',
    text: 'تحویل به موقع'
  }
]

// Platform Statistics
const statistics = [
  {
    number: '۵۰,۰۰۰+',
    label: 'تامین‌کننده معتبر'
  },
  {
    number: '۱ میلیون+',
    label: 'محصولات ماشین‌آلات'
  },
  {
    number: '۳۱',
    label: 'استان‌های تحت پوشش'
  },
  {
    number: '۹۸٪',
    label: 'رضایت مشتریان'
  }
]

const showAutocomplete = computed(() => isSearchFocused.value && searchQuery.value.length >= 2)
const hasResults = computed(() => searchResults.value.total > 0)
const totalDisplayed = computed(
  () =>
    (searchResults.value.products?.length ?? 0) + (searchResults.value.blogs?.length ?? 0)
)

const performAutocompleteSearch = debounce(async (query: string) => {
  if (!query || query.length < 2) {
    searchResults.value = { products: [], blogs: [], total: 0 } as SearchResponse
    isLoadingSearch.value = false
    return
  }

  isLoadingSearch.value = true
  try {
    const data = await globalSearch(query, 5)
    searchResults.value = data ?? { products: [], blogs: [], total: 0 }
  } catch (error) {
    console.error('Search error:', error)
    searchResults.value = { products: [], blogs: [], total: 0 } as SearchResponse
  } finally {
    isLoadingSearch.value = false
  }
}, 300)

const onSearchQueryChange = () => {
  if (searchQuery.value.length >= 2) {
    performAutocompleteSearch(searchQuery.value)
  } else {
    searchResults.value = { products: [], blogs: [], total: 0 } as SearchResponse
    isLoadingSearch.value = false
  }
}

const performSearch = () => {
  const value = searchQuery.value?.trim()
  if (!value) {
    return
  }

  closeAutocomplete()
  router.push({
    path: '/products',
    query: { search: value }
  })
}

const closeAutocomplete = () => {
  isSearchFocused.value = false
}

const formatPrice = (price: number | string) => {
  const numericPrice = Number(price)
  if (Number.isNaN(numericPrice) || numericPrice <= 0) {
    return 'تماس بگیرید'
  }
  return new Intl.NumberFormat('fa-IR').format(numericPrice)
}

const truncate = (text: string, length: number) => {
  if (!text) return ''
  return text.length > length ? `${text.substring(0, length)}...` : text
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as Node
  if (searchContainer.value && !searchContainer.value.contains(target)) {
    closeAutocomplete()
  }
}

const initializeFromRoute = () => {
  const initialSearch = route.query.search
  if (typeof initialSearch === 'string') {
    searchQuery.value = initialSearch
  }
}

watch(
  () => route.query.search,
  (newSearch) => {
    if (typeof newSearch === 'string' && newSearch !== searchQuery.value) {
      searchQuery.value = newSearch
    }
  }
)

onMounted(() => {
  initializeFromRoute()
  if (import.meta.client) {
    document.addEventListener('click', handleClickOutside)
  }
})

onUnmounted(() => {
  if (import.meta.client) {
    document.removeEventListener('click', handleClickOutside)
  }
})

const navigateToProducts = () => {
  router.push('/products')
}

const navigateToCategory = (category: { slug: string }) => {
  router.push(`/categories/${category.slug}`)
}

const handleSellerCTA = () => {
  router.push('/register')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  position: relative;
  overflow: hidden;
}

/* Background Decorative Shapes */
.background-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.3;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background-color: rgb(var(--v-theme-primary));
  top: -100px;
  left: -100px;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background-color: rgb(var(--v-theme-secondary));
  bottom: 20%;
  right: -100px;
}

/* Hero Section */
.hero-section {
  padding: 80px 0 60px;
  position: relative;
  z-index: 1;
}

.hero-card {
  background: rgba(var(--v-theme-surface), 0.95) !important;
  backdrop-filter: blur(10px);
  box-shadow: 0 20px 60px rgba(var(--v-theme-on-surface), 0.1) !important;
  position: relative;
  overflow: hidden;
}

.hero-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 200px;
  height: 200px;
  background: rgb(var(--v-theme-primary));
  opacity: 0.05;
  border-radius: 0 0 200px 0;
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-title {
  color: rgb(var(--v-theme-primary));
  line-height: 1.2;
}

.hero-subtitle {
  color: rgba(var(--v-theme-on-surface), 0.7);
}

/* Search Input */
.search-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 0;
}

.hero-search-input :deep(.v-field) {
  font-size: 1.125rem;
  padding: 12px 16px;
  border: 1px solid rgba(var(--v-theme-primary), 0.2);
}

.hero-search-input :deep(.v-field__input) {
  min-height: 56px;
  text-align: right;
  direction: rtl;
}

.hero-search-input :deep(.v-field):focus-within {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.1);
}

.hero-search-input :deep(.v-field__append-inner .v-icon) {
  font-size: 28px !important;
  cursor: pointer;
  color: rgb(var(--v-theme-primary));
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
  direction: rtl;
}

.search-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.no-results {
  color: rgba(var(--v-theme-on-surface), 0.5);
}

.results-container {
  padding: 0;
}

.result-section {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.result-section:last-child {
  border-bottom: none;
}

.section-label {
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.6);
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  text-decoration: none;
  color: rgba(var(--v-theme-on-surface), 0.87);
  transition: background-color 0.2s;
  cursor: pointer;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.04);
}

.result-image {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background-color: rgba(var(--v-theme-on-surface), 0.06);
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
  background-color: rgba(var(--v-theme-on-surface), 0.08);
  color: rgba(var(--v-theme-on-surface), 0.5);
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
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.result-price {
  font-weight: 500;
  color: rgb(var(--v-theme-primary));
}

.result-excerpt {
  color: rgba(var(--v-theme-on-surface), 0.5);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.view-all {
  background-color: rgba(var(--v-theme-surface), 0.97);
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.autocomplete-dropdown::-webkit-scrollbar {
  width: 6px;
}

.autocomplete-dropdown::-webkit-scrollbar-track {
  background: rgba(var(--v-theme-surface), 0.5);
  border-radius: 4px;
}

.autocomplete-dropdown::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.4);
  border-radius: 4px;
}

.autocomplete-dropdown::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.6);
}

/* Hero Buttons */
.hero-buttons {
  margin-top: 0;
}

/* Section Styles */
.categories-section,
.verification-section,
.statistics-section {
  position: relative;
  z-index: 1;
}

.section-title {
  position: relative;
  display: inline-block;
  padding-bottom: 12px;
}

.section-title::after {
  content: "";
  position: absolute;
  bottom: 0;
  right: 0;
  width: 60px;
  height: 4px;
  background-color: rgb(var(--v-theme-primary));
  border-radius: 2px;
}

/* Category Cards */
.category-card {
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  min-height: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(var(--v-theme-on-surface), 0.15) !important;
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.category-title {
  color: rgba(var(--v-theme-on-surface), 0.87);
}

/* Verification Card */
.verification-card {
  background: rgba(var(--v-theme-surface), 0.98) !important;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.badge-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.badge-icon-container {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1), rgba(var(--v-theme-secondary), 0.1));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-text {
  color: rgba(var(--v-theme-on-surface), 0.87);
}

/* Statistics Cards */
.stat-card {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-number {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  color: rgba(var(--v-theme-on-surface), 0.7);
}

/* Mobile Responsive */
@media (max-width: 959px) {
  .hero-section {
    padding: 40px 0 30px;
  }

  .hero-title {
    font-size: 1.75rem !important;
  }

  .hero-subtitle {
    font-size: 1rem !important;
  }

  .hero-search-input :deep(.v-field__input) {
    min-height: 48px;
  }

  .autocomplete-dropdown {
    max-height: 400px;
  }

  .section-title {
    font-size: 1.5rem !important;
  }

  .category-card {
    min-height: 120px;
  }

  .badge-icon-container {
    width: 60px;
    height: 60px;
  }

  .badge-icon-container .v-icon {
    font-size: 30px !important;
  }

  .hero-buttons {
    flex-direction: column;
  }
}

@media (max-width: 599px) {
  .shape-1,
  .shape-2 {
    display: none;
  }

  .stat-number {
    font-size: 1.5rem !important;
  }
}
</style>


