<template>
  <div class="home" dir="rtl">
    <section class="hero-section">
      <v-container class="pa-0">
        <v-row no-gutters justify="center" align="center" class="hero-content">
          <v-col cols="12" md="10" lg="8" class="pa-4 pa-md-8">
            <div class="search-wrapper" ref="searchContainer">
              <v-card elevation="8" rounded="xl" class="search-card pa-4 pa-md-6 mb-4" color="surface">
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
                  />
                </v-card-text>
              </v-card>

              <transition name="dropdown">
                <v-card
                  v-if="showAutocomplete && (hasResults || isLoadingSearch)"
                  elevation="8"
                  rounded="lg"
                  class="autocomplete-dropdown"
                >
                  <div v-if="isLoadingSearch" class="search-loading pa-4">
                    <v-progress-circular
                      indeterminate
                      color="primary"
                      size="24"
                      class="mr-2"
                    />
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
                      <div class="section-title pa-2 text-caption font-weight-bold">
                        محصولات
                      </div>
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
                      <div class="section-title pa-2 text-caption font-weight-bold">
                        وبلاگ
                      </div>
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

            <p class="search-subtitle text-center text-body-1 text-md-h6">
              از بین تولیدات بهترین تولید کنندگان ماشین آلات نیاز خود را جستجو کنید
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <v-container class="buyers-section py-8 py-md-12">
      <v-card elevation="4" rounded="xl" class="section-card buyers-card" color="primary" variant="tonal">
        <v-card-title class="section-title text-h4 text-md-h3 text-center pa-6 pa-md-8">
          <v-icon size="large" class="ml-2">mdi-account-group</v-icon>
          ایندکسو برای خریداران
        </v-card-title>

        <v-card-text class="pa-4 pa-md-6">
          <v-row class="advantages-grid mb-6">
            <v-col
              v-for="(advantage, index) in buyerAdvantages"
              :key="`buyer-${index}`"
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
                <v-icon :icon="advantage.icon" size="64" :color="advantage.color" class="mb-4" />
                <h3 class="text-h6 text-md-h5 font-weight-bold mb-3">
                  {{ advantage.title }}
                </h3>
                <p class="text-body-2 text-md-body-1 text-medium-emphasis">
                  {{ advantage.description }}
                </p>
              </v-card>
            </v-col>
          </v-row>

          <v-card elevation="2" rounded="lg" class="cta-card pa-4 pa-md-6 mb-4" color="surface">
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

    <v-container class="sellers-section py-8 py-md-12">
      <v-card elevation="4" rounded="xl" class="section-card sellers-card" color="secondary" variant="tonal">
        <v-card-title class="section-title text-h4 text-md-h3 text-center pa-6 pa-md-8">
          <v-icon size="large" class="ml-2">mdi-store</v-icon>
          ایندکسو برای فروشندگان
        </v-card-title>

        <v-card-text class="pa-4 pa-md-6">
          <v-row class="advantages-grid mb-6">
            <v-col
              v-for="(advantage, index) in sellerAdvantages"
              :key="`seller-${index}`"
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
                <v-icon :icon="advantage.icon" size="64" :color="advantage.color" class="mb-4" />
                <h3 class="text-h6 text-md-h5 font-weight-bold mb-3">
                  {{ advantage.title }}
                </h3>
                <p class="text-body-2 text-md-body-1 text-medium-emphasis">
                  {{ advantage.description }}
                </p>
              </v-card>
            </v-col>
          </v-row>

          <v-card elevation="2" rounded="lg" class="cta-card pa-4 pa-md-6 mb-4" color="surface">
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

const buyerAdvantages = [
  {
    icon: 'mdi-account-switch',
    title: 'ارتباط مستقیم',
    description: 'بدون واسطه و اصطکاک، مستقیماً با تامین‌کنندگان معتبر در ارتباط باشید',
    color: 'primary'
  },
  {
    icon: 'mdi-shield-check',
    title: 'تامین‌کنندگان معتبر',
    description: 'از بین بهترین تولیدکنندگان ماشین‌آلات، تامین‌کننده مناسب خود را پیدا کنید',
    color: 'secondary'
  },
  {
    icon: 'mdi-lightning-bolt',
    title: 'مسیر کوتاه خرید',
    description: 'فرآیند خرید را کوتاه کرده و سریع‌تر به محصول مورد نظر خود برسید',
    color: 'accent'
  }
]

const sellerAdvantages = [
  {
    icon: 'mdi-cash',
    title: 'هزینه کم',
    description: 'با حداقل هزینه، محصولات خود را به خریداران هدف معرفی کنید',
    color: 'secondary'
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
    color: 'accent'
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

const handleBuyerCTA = () => {
  if (import.meta.client) {
    window.location.hash = '#rfq'
  }
}

const handleSellerCTA = () => {
  router.push('/register')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.hero-section {
  background: linear-gradient(135deg, rgba(0, 197, 142, 0.22), rgba(0, 111, 82, 0.26));
  min-height: 400px;
  display: flex;
  align-items: center;
  padding: 60px 20px;
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  margin: 16px auto 36px;
  max-width: 1440px;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.12);
}

.hero-section::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(255, 255, 255, 0.28), transparent 60%);
  pointer-events: none;
}

@media (min-width: 960px) {
  .hero-section {
    min-height: 500px;
  }
}

.hero-content {
  width: 100%;
  position: relative;
  z-index: 1;
  color: rgba(var(--v-theme-on-primary), 0.96);
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
  background: rgba(var(--v-theme-surface), 0.95) !important;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12) !important;
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

.home-search-input :deep(.v-field__append-inner .v-icon) {
  font-size: 32px !important;
  width: 32px !important;
  height: 32px !important;
  margin-inline-start: 5px !important;
  margin-inline-end: 10px !important;
}

@media (min-width: 960px) {
  .home-search-input :deep(.v-field__append-inner .v-icon) {
    font-size: 40px !important;
    width: 40px !important;
    height: 40px !important;
    margin-inline-start: 10px !important;
  }
}

.search-subtitle {
  color: rgba(var(--v-theme-on-primary), 0.9);
  opacity: 0.95;
  font-weight: 400;
  margin-top: 24px;
}

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

.section-title {
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
  border-radius: 6px;
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

.autocomplete-dropdown :deep(.v-card-text),
.autocomplete-dropdown {
  scrollbar-width: thin;
  scrollbar-color: rgba(var(--v-theme-primary), 0.4) rgba(var(--v-theme-surface), 0.5);
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

.section-card {
  max-width: 1200px;
  margin: 0 auto;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  box-shadow: 0 20px 40px rgba(var(--v-theme-on-surface), 0.08);
}

.buyers-card {
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-primary), 0.12) 0%,
    rgba(var(--v-theme-secondary), 0.16) 100%
  );
  border-left: 4px solid rgba(var(--v-theme-primary), 0.4);
}

.sellers-card {
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-secondary), 0.14) 0%,
    rgba(var(--v-theme-primary), 0.16) 100%
  );
  border-left: 4px solid rgba(var(--v-theme-secondary), 0.4);
}

.advantages-grid {
  margin-top: 24px;
}

.advantage-card {
  height: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  background: rgba(var(--v-theme-surface), 0.92);
}

.advantage-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 16px rgba(var(--v-theme-on-surface), 0.15) !important;
}

.cta-card {
  background: rgb(var(--v-theme-surface));
}

.cta-button {
  font-weight: 600;
  letter-spacing: 0.5px;
}

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
</style>


