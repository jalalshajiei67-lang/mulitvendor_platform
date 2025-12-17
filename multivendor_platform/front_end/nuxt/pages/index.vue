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
                  خرید و فروش ماشین‌آلات از بهترین تولیدکنندگان کشور
                </h1>
                <p class="hero-subtitle text-body-1 text-md-h6 text-center mb-6">
                  دستگاه و تجهیزات مورد نیاز خود را به راحتی پیدا کنید
                </p>

                <!-- Search Container -->
                <div class="search-wrapper" ref="searchContainer">
                  <v-text-field
                    v-model="searchQuery"
                    :placeholder="animatedPlaceholder"
                    append-inner-icon="mdi-magnify"
                    variant="outlined"
                    rounded="lg"
                    hide-details
                    class="hero-search-input mb-6"
                    density="comfortable"
                    @focus="handleSearchFocus"
                    @blur="handleSearchBlur"
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
                        <span>در حال پیدا کردن...</span>
                      </div>

                      <div v-else-if="!hasResults && searchQuery.length >= 2" class="no-results pa-4 text-center">
                        <p class="text-body-2 text-medium-emphasis">متأسفانه چیزی پیدا نشد. لطفاً کلمه دیگری امتحان کنید</p>
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
                            target="_blank"
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
                            target="_blank"
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
                            نمایش همه ({{ searchResults.total - totalDisplayed }} مورد دیگر)
                          </v-btn>
                        </div>
                      </div>
                    </v-card>
                  </transition>
                </div>

                <!-- Filters Row - Category Only -->
                <v-row class="mb-4 filters-row" align="center">
                  <v-col cols="12">
                    <v-select
                      v-model="selectedCategory"
                      :items="categoryOptions"
                      item-title="name"
                      item-value="id"
                      variant="outlined"
                      density="comfortable"
                      :label="t('selectCategory')"
                      clearable
                      class="filter-select"
                      @update:model-value="applyFilters"
                    >
                      <template #prepend-inner>
                        <v-icon color="primary" size="20">mdi-shape</v-icon>
                      </template>
                      <template #selection="{ item }">
                        <div class="d-flex align-center">
                          <v-icon size="16" color="success" class="ml-2">mdi-check-circle</v-icon>
                          <span class="font-weight-medium">{{ item.title }}</span>
                        </div>
                      </template>
                      <template #item="{ props, item }">
                        <v-list-item v-bind="props" class="filter-menu-item">
                          <template #prepend>
                            <v-icon color="primary" size="18">mdi-shape</v-icon>
                          </template>
                        </v-list-item>
                      </template>
                    </v-select>
                  </v-col>
                </v-row>

                <!-- Filter header with active count -->
                <div v-if="activeFiltersCount > 0" class="filters-header mb-4">
                  <div class="d-flex align-center justify-space-between">
                    <div class="d-flex align-center gap-2">
                      <v-icon size="24" color="primary">mdi-filter-variant</v-icon>
                      <h3 class="text-h6 font-weight-bold">فیلترها</h3>
                      <v-chip
                        size="small"
                        color="primary"
                        variant="flat"
                        class="mr-2"
                      >
                        {{ activeFiltersCount }}
                      </v-chip>
                    </div>
                    <v-btn
                      variant="text"
                      color="error"
                      size="small"
                      prepend-icon="mdi-close-circle"
                      @click="resetFilters"
                    >
                      پاک کردن همه
                    </v-btn>
                  </div>
                </div>

                <!-- Desktop layout: subcategory + labels + active chips -->
                <template v-if="mdAndUp">
                  <!-- Only show divider if category is selected or there are subcategories -->
                  <v-divider v-if="selectedCategory || subcategoryOptions.length" class="mb-6" />
                  
                  <v-row v-if="selectedCategory" class="mb-4" align="center">
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="selectedSubcategory"
                        :items="subcategoryOptions"
                        item-title="name"
                        item-value="id"
                        variant="outlined"
                        density="comfortable"
                        label="انتخاب زیرشاخه"
                        prepend-inner-icon="mdi-file-tree"
                        clearable
                        :disabled="!subcategoryOptions.length"
                        @update:model-value="onSubcategorySelect"
                        :hint="!subcategoryOptions.length ? 'زیرشاخه‌ای برای این دسته وجود ندارد' : ''"
                        persistent-hint
                      >
                        <template #selection="{ item }">
                          <div class="d-flex align-center">
                            <v-icon size="16" class="ml-2">mdi-check-circle</v-icon>
                            <span>{{ item.title }}</span>
                          </div>
                        </template>
                      </v-select>
                    </v-col>
                  </v-row>

                  <!-- Label Filters Section - Only show when category is selected and has labels -->
                  <transition name="slide-fade">
                    <v-row v-if="shouldShowLabelFilters" class="label-filters-row">
                      <v-col cols="12">
                        <div class="label-section-header mb-3">
                          <div class="d-flex align-center justify-space-between">
                            <div class="d-flex align-center gap-2">
                              <v-icon size="20" color="primary">mdi-tag-multiple</v-icon>
                              <span class="text-subtitle-2 font-weight-bold">فیلترهای پیشرفته</span>
                              <v-chip
                                v-if="selectedLabels.length"
                                size="x-small"
                                color="success"
                                variant="flat"
                              >
                                {{ selectedLabels.length }}
                              </v-chip>
                            </div>
                            <v-btn
                              v-if="selectedLabels.length"
                              variant="text"
                              color="primary"
                              size="small"
                              @click="clearLabelFilters"
                            >
                              پاک کردن
                            </v-btn>
                          </div>
                        </div>
                        
                        <LabelFilters
                          v-model="selectedLabels"
                          v-model:ordering="ordering"
                          :subcategory-id="selectedSubcategory"
                          @labels-loaded="onLabelsLoaded"
                        />
                      </v-col>
                    </v-row>
                  </transition>

                  <!-- Active Labels Summary -->
                  <transition name="slide-fade">
                    <div v-if="selectedLabelDetails.length" class="active-labels-summary mt-4">
                      <v-card variant="tonal" color="primary" rounded="lg">
                        <v-card-text class="pa-3">
                          <div class="d-flex align-center gap-2 mb-2">
                            <v-icon size="18">mdi-filter-check</v-icon>
                            <span class="text-caption font-weight-medium">فیلترهای فعال:</span>
                          </div>
                          <div class="d-flex flex-wrap gap-2">
                            <v-chip
                              v-for="label in selectedLabelDetails"
                              :key="label.slug"
                              size="small"
                              variant="elevated"
                              closable
                              class="active-label-chip"
                              @click:close="removeLabel(label.slug)"
                            >
                              <v-icon start size="14">mdi-check</v-icon>
                              {{ label.name }}
                            </v-chip>
                          </div>
                        </v-card-text>
                      </v-card>
                    </div>
                  </transition>
                </template>

                <!-- Mobile layout: extra filters and labels inside a drawer -->
                <template v-else>
                  <v-divider v-if="selectedCategory || mobileActiveFiltersCount > 0" class="my-4" />
                  
                  <v-expansion-panels v-model="mobileFiltersExpanded" class="mt-2" elevation="0">
                    <v-expansion-panel>
                      <v-expansion-panel-title class="filters-card__drawer-title">
                        <div class="d-flex align-center justify-space-between w-100">
                          <div class="d-flex align-center gap-2">
                            <v-icon size="20">mdi-tune</v-icon>
                            <span class="font-weight-medium">فیلترهای بیشتر</span>
                            <v-chip
                              v-if="mobileActiveFiltersCount"
                              size="x-small"
                              color="primary"
                              variant="flat"
                            >
                              {{ mobileActiveFiltersCount }}
                            </v-chip>
                          </div>
                        </div>
                      </v-expansion-panel-title>
                      <v-expansion-panel-text>
                        <v-row class="mb-3" align="center">
                          <v-col v-if="selectedCategory" cols="12">
                            <v-select
                              v-model="selectedSubcategory"
                              :items="subcategoryOptions"
                              item-title="name"
                              item-value="id"
                              variant="outlined"
                              density="comfortable"
                              label="انتخاب زیرشاخه"
                              prepend-inner-icon="mdi-file-tree"
                              clearable
                              :disabled="!subcategoryOptions.length"
                              @update:model-value="onSubcategorySelect"
                              :hint="!subcategoryOptions.length ? 'زیرشاخه‌ای برای این دسته وجود ندارد' : ''"
                              persistent-hint
                            />
                          </v-col>
                        </v-row>

                        <!-- Label Filters for Mobile - Only show when category is selected -->
                        <transition name="slide-fade">
                          <div v-if="shouldShowLabelFilters" class="label-section-mobile mb-3">
                            <div class="d-flex align-center gap-2 mb-3">
                              <v-icon size="18" color="primary">mdi-tag-multiple</v-icon>
                              <span class="text-subtitle-2 font-weight-bold">فیلترهای پیشرفته</span>
                            </div>
                            <LabelFilters
                              v-model="selectedLabels"
                              v-model:ordering="ordering"
                              :subcategory-id="selectedSubcategory"
                              @labels-loaded="onLabelsLoaded"
                            />
                          </div>
                        </transition>

                        <!-- Active Labels in Mobile -->
                        <transition name="slide-fade">
                          <div v-if="selectedLabelDetails.length" class="active-labels-mobile mt-3">
                            <v-card variant="tonal" color="primary" rounded="lg">
                              <v-card-text class="pa-3">
                                <div class="d-flex align-center gap-2 mb-2">
                                  <v-icon size="16">mdi-filter-check</v-icon>
                                  <span class="text-caption font-weight-medium">فیلترهای فعال:</span>
                                </div>
                                <div class="d-flex flex-wrap gap-2">
                                  <v-chip
                                    v-for="label in selectedLabelDetails"
                                    :key="label.slug"
                                    size="small"
                                    variant="elevated"
                                    closable
                                    @click:close="removeLabel(label.slug)"
                                  >
                                    <v-icon start size="12">mdi-check</v-icon>
                                    {{ label.name }}
                                  </v-chip>
                                </div>
                                <v-btn
                                  block
                                  variant="text"
                                  color="error"
                                  size="small"
                                  class="mt-3"
                                  prepend-icon="mdi-close-circle"
                                  @click="clearLabelFilters"
                                >
                                  پاک کردن همه فیلترها
                                </v-btn>
                              </v-card-text>
                            </v-card>
                          </div>
                        </transition>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </template>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Products Results Section -->
    <v-container class="py-8">

      <!-- Products Results - Always show -->
      <ListSkeleton
        v-if="loading"
        type="product"
        variant="grid"
        :count="9"
        :cols="12"
        :sm="6"
        :md="4"
        :lg="3"
      />

      <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
        {{ error }}
      </v-alert>

      <template v-else>
        <v-row v-if="products.length" class="products-grid">
          <v-col v-for="product in products" :key="product.id" cols="12" sm="6" md="4" xl="3">
            <ProductCard :product="product" />
          </v-col>
        </v-row>

        <v-card v-else elevation="1" rounded="xl" class="pa-10 text-center">
          <v-icon size="56" color="primary" class="mb-4">mdi-package-variant</v-icon>
          <h3 class="text-h6 mb-2">{{ t('noProductsFound') }}</h3>
          <p class="text-body-2 text-medium-emphasis mb-6">
            {{ t('tryDifferentFilters') }}
          </p>
          <v-btn color="primary" @click="resetFilters">
            {{ t('resetFilters') }}
          </v-btn>
        </v-card>

        <div v-if="pagination.count > products.length" class="d-flex justify-center mt-10">
          <v-pagination
            v-model="page"
            :length="pageCount"
            :total-visible="5"
            @update:model-value="onPageChange"
          />
        </div>
      </template>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { debounce } from '@/composables/useDebounce'
import { useTypingAnimation } from '@/composables/useTypingAnimation'
import { useDisplay } from 'vuetify'
import LabelFilters from '~/components/product/LabelFilters.vue'
import ListSkeleton from '~/components/skeletons/ListSkeleton.vue'
import ProductCard from '~/components/product/ProductCard.vue'
import type { LocationQueryValue } from 'vue-router'
import { useLabelStore } from '~/stores/label'

definePageMeta({
  layout: 'default',
  title: 'خانه'
})

useSeoMeta({
  title: 'خانه',
  ogTitle: 'ایندکسو | پلتفرم چندفروشنده',
  description:
    'ایندکسو: خرید و فروش آسان ماشین‌آلات و تجهیزات از بهترین تولیدکنندگان کشور',
  ogDescription:
    'ایندکسو: خرید و فروش آسان ماشین‌آلات و تجهیزات از بهترین تولیدکنندگان کشور',
  ogImage: '/favicon.ico',
  ogType: 'website'
})

const router = useRouter()
const route = useRoute()
const { globalSearch } = useSearchApi()

type SearchResponse = Awaited<ReturnType<typeof globalSearch>>

// Search autocomplete state
const searchQuery = ref<string>('')
const searchResults = ref<SearchResponse extends Promise<infer R> ? R : SearchResponse>({
  products: [],
  blogs: [],
  total: 0
})
const isLoadingSearch = ref(false)
const isSearchFocused = ref(false)
const searchContainer = ref<HTMLElement | null>(null)

// Typing animation for search placeholder
const searchQueries = [
  'جت پرینتر',
  'خط تولید لنت',
  'پرس هیدرولیک',
  'دستگاه جوش لیزر',
  'لیزر حکاکی',
  'کمپرسور هوا',
  'دستگاه برش لیزری',
]

const typingAnimation = useTypingAnimation(searchQueries, {
  typingSpeed: 80,
  deletingSpeed: 40,
  pauseAfterTyping: 2500,
  pauseAfterDeleting: 800,
  startDelay: 1000
})

const animatedPlaceholder = computed(() => {
  // Show animated text only when input is empty and not focused
  if (!searchQuery.value && !isSearchFocused.value) {
    return typingAnimation.currentText.value || 'نام دستگاه یا ماشین آلات مورد نظر خود را بنویسید'
  }
  return 'نام دستگاه یا ماشین آلات مورد نظر خود را بنویسید'
})

// Products store and state
const productStore = useProductStore()
const { products, loading, error, pagination } = storeToRefs(productStore)
const t = productStore.t
const { mdAndUp } = useDisplay()

// Products filter state
const search = ref('')
const selectedCategory = ref<number | null>(null)
const selectedSubcategory = ref<number | null>(null)
const ordering = ref<string | null>(null)
const page = ref(1)
const pageSize = 9 // Changed to 9 products per page
const mobileFiltersExpanded = ref<number | undefined>(undefined)
const hasLabelGroups = ref(false)

const labelStore = useLabelStore()
const selectedLabels = ref<string[]>([])
const subcategoryOptions = ref<any[]>([])
let skipLabelWatcher = false

// Computed property to determine if label filters should be shown
const shouldShowLabelFilters = computed(() => {
  return selectedCategory.value !== null && (hasLabelGroups.value || labelStore.labelGroups.length > 0)
})

// Computed property for active filters count
const activeFiltersCount = computed(() => {
  let count = 0
  if (search.value) count++
  if (selectedCategory.value) count++
  if (selectedSubcategory.value) count++
  if (ordering.value) count++
  if (selectedLabels.value.length) count += selectedLabels.value.length
  return count
})

// Computed property for mobile filters count
const mobileActiveFiltersCount = computed(() => {
  let count = 0
  if (selectedSubcategory.value) count++
  if (ordering.value) count++
  if (selectedLabels.value.length) count += selectedLabels.value.length
  return count
})

// Show products section only when filters are active
const hasActiveFilters = computed(() => {
  const hasFilters = !!(
    search.value ||
    selectedCategory.value ||
    selectedSubcategory.value ||
    ordering.value ||
    selectedLabels.value.length ||
    route.query.search ||
    route.query.category ||
    route.query.subcategory ||
    route.query.ordering ||
    route.query.labels
  )
  return hasFilters
})

// Event handler when labels are loaded from LabelFilters component
const onLabelsLoaded = (groupsCount: number) => {
  hasLabelGroups.value = groupsCount > 0
}

const parseLabelParam = (value: LocationQueryValue | LocationQueryValue[] | null | undefined) => {
  if (!value) {
    return []
  }

  const normalized = Array.isArray(value) ? value : [value]
  return normalized
    .filter((item): item is string => typeof item === 'string')
    .flatMap((item) => item.split(','))
    .map((item) => item.trim())
    .filter(Boolean)
}

watch(
  () => route.query.labels,
  (value) => {
    const parsed = parseLabelParam(value)
    if (parsed.join(',') !== selectedLabels.value.join(',')) {
      selectedLabels.value = parsed
    }
  },
  { immediate: true }
)

// Watch selectedLabels changes and apply filters
watch(
  selectedLabels,
  async (newLabels, oldLabels) => {
    if (skipLabelWatcher) {
      skipLabelWatcher = false
      return
    }
    const newStr = newLabels.join(',')
    const oldStr = oldLabels ? oldLabels.join(',') : ''
    if (newStr !== oldStr) {
      await applyFilters()
      updateLabelsQuery(newLabels)
    }
  }
)

const labelLookup = computed(() => {
  const map = new Map<string, Record<string, any>>()
  labelStore.labelGroups.forEach((group) => {
    const labels = Array.isArray(group.labels) ? group.labels : []
    labels.forEach((label: Record<string, any>) => {
      map.set(label.slug, label)
    })
  })
  return map
})

const selectedLabelDetails = computed(() =>
  selectedLabels.value
    .map((slug) => labelLookup.value.get(slug))
    .filter(Boolean) as Record<string, any>[]
)

const updateLabelsQuery = (labels: string[]) => {
  if (typeof window === 'undefined') {
    return
  }

  const query = { ...route.query }
  if (labels.length) {
    query.labels = labels.join(',')
  } else {
    delete query.labels
  }

  router.replace({ query }).catch(() => {})
}

const fetchSubcategories = async (categoryId: number) => {
  try {
    const data = await useApiFetch<any[] | { results: any[] }>(`subcategories/?category=${categoryId}`)
    subcategoryOptions.value = Array.isArray(data) ? data : data.results ?? []
  } catch (err) {
    console.error('Error fetching subcategories:', err)
    subcategoryOptions.value = []
  }
}

watch(
  selectedCategory,
  (newCategory, oldCategory) => {
    if (newCategory === oldCategory) {
      return
    }
    skipLabelWatcher = true
    selectedLabels.value = []
    updateLabelsQuery([])
    selectedSubcategory.value = null
    subcategoryOptions.value = []
    hasLabelGroups.value = false
    
    if (newCategory) {
      void fetchSubcategories(newCategory)
      void labelStore.fetchLabelGroupsForSubcategory(null, true)
    } else {
      hasLabelGroups.value = false
    }
  }
)

const onSubcategorySelect = async (value: number | null) => {
  selectedSubcategory.value = value
  skipLabelWatcher = true
  selectedLabels.value = []
  updateLabelsQuery([])
  await applyFilters()
}

const categoryOptions = ref<any[]>([])

const orderingOptions = [
  { title: t('newest'), value: '-created_at' },
  { title: t('priceLowToHigh'), value: 'price' },
  { title: t('priceHighToLow'), value: '-price' }
]

const pageCount = computed(() =>
  Math.max(1, Math.ceil((pagination.value.count || products.value.length || 1) / pageSize))
)

const fetchCategories = async () => {
  try {
    const data = await useApiFetch<any[] | { results: any[] }>('categories/')
    categoryOptions.value = Array.isArray(data) ? data : data.results ?? []
  } catch (err) {
    console.error('Error fetching categories for filters:', err)
  }
}

const fetchPage = async () => {
  try {
    await productStore.fetchProducts({
      page: page.value,
      page_size: pageSize,
      search: search.value || undefined,
      category: selectedCategory.value || undefined,
      subcategory: selectedSubcategory.value || undefined,
      ordering: ordering.value || undefined,
      labels: selectedLabels.value.length ? selectedLabels.value.join(',') : undefined
    })
  } catch (err: any) {
    // If we get a 404 error (invalid page), reset to page 1
    if (err?.statusCode === 404 || err?.status === 404) {
      console.warn('Page not found, resetting to page 1')
      page.value = 1
      await productStore.fetchProducts({
        page: 1,
        page_size: pageSize,
        search: search.value || undefined,
        category: selectedCategory.value || undefined,
        subcategory: selectedSubcategory.value || undefined,
        ordering: ordering.value || undefined,
        labels: selectedLabels.value.length ? selectedLabels.value.join(',') : undefined
      })
    }
  }
}

// Initialize from route query params
const initializeFromRoute = () => {
  const routeSearch = route.query.search
  if (typeof routeSearch === 'string') {
    searchQuery.value = routeSearch
    search.value = routeSearch
  }

  const routeCategory = route.query.category
  if (routeCategory) {
    const categoryId = typeof routeCategory === 'string' ? parseInt(routeCategory) : parseInt(routeCategory[0])
    if (!isNaN(categoryId)) {
      selectedCategory.value = categoryId
    }
  }

  const routeSubcategory = route.query.subcategory
  if (routeSubcategory) {
    const subcategoryId = typeof routeSubcategory === 'string' ? parseInt(routeSubcategory) : parseInt(routeSubcategory[0])
    if (!isNaN(subcategoryId)) {
      selectedSubcategory.value = subcategoryId
    }
  }

  const routeOrdering = route.query.ordering
  if (typeof routeOrdering === 'string') {
    ordering.value = routeOrdering
  }

  const routeLabels = parseLabelParam(route.query.labels)
  if (routeLabels.length) {
    selectedLabels.value = routeLabels
  }
}

// Initialize data
await useAsyncData('homepage-products', async () => {
  await Promise.all([
    fetchCategories(),
    labelStore.fetchLabelGroupsForSubcategory(null, true)
  ])
  
  initializeFromRoute()
  
  // Always fetch products on page load (show all products by default)
  await fetchPage()
})

const onPageChange = async (value: number) => {
  // Validate page number before fetching
  if (value < 1 || value > pageCount.value) {
    console.warn(`Invalid page number: ${value}. Valid range: 1-${pageCount.value}`)
    return
  }
  page.value = value
  await fetchPage()
  // Scroll to top on page change
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const applyFilters = async () => {
  page.value = 1
  await fetchPage()
}

const onLabelsChange = async (labels: string[]) => {
  selectedLabels.value = labels
  await applyFilters()
  updateLabelsQuery(labels)
}

const clearLabelFilters = async () => {
  if (!selectedLabels.value.length) {
    return
  }
  await onLabelsChange([])
}

const removeLabel = async (slug: string) => {
  const remaining = selectedLabels.value.filter((value) => value !== slug)
  await onLabelsChange(remaining)
}

const resetFilters = async () => {
  search.value = ''
  searchQuery.value = ''
  selectedCategory.value = null
  selectedSubcategory.value = null
  ordering.value = null
  page.value = 1
  skipLabelWatcher = true
  selectedLabels.value = []
  updateLabelsQuery([])
  await labelStore.fetchLabelGroupsForSubcategory(null, true)
  
  // Clear route query
  router.replace({ query: {} }).catch(() => {})
}

// Search autocomplete functions
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

const performSearch = async () => {
  const value = searchQuery.value?.trim()
  if (!value) {
    return
  }

  closeAutocomplete()
  // Set search filter and apply
  search.value = value
  
  // Update route query first
  await router.replace({
    query: { ...route.query, search: value }
  }).catch(() => {})
  
  // Then apply filters to fetch products
  await applyFilters()
}

// Sync hero search with filter search and control animation
watch(searchQuery, (newValue) => {
  // Sync with filter search
  if (newValue && newValue !== search.value) {
    search.value = newValue
  }
  
  // Control typing animation
  if (newValue) {
    // Stop animation when user types
    typingAnimation.pause()
  } else if (!isSearchFocused.value) {
    // Resume animation when input is cleared and not focused
    typingAnimation.resume()
  }
})

const closeAutocomplete = () => {
  isSearchFocused.value = false
}

const handleSearchFocus = () => {
  isSearchFocused.value = true
  // Pause animation when user focuses on input
  typingAnimation.pause()
}

const handleSearchBlur = () => {
  isSearchFocused.value = false
  // Resume animation when user blurs and input is empty
  if (!searchQuery.value) {
    typingAnimation.resume()
  }
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

watch(
  () => route.query.search,
  async (newSearch) => {
    if (typeof newSearch === 'string' && newSearch !== searchQuery.value) {
      searchQuery.value = newSearch
      search.value = newSearch
      if (hasActiveFilters.value) {
        await applyFilters()
      }
    } else if (!newSearch && search.value) {
      // Clear search if query param is removed
      search.value = ''
      searchQuery.value = ''
    }
  }
)

onMounted(() => {
  if (import.meta.client) {
    document.addEventListener('click', handleClickOutside)
    // Start typing animation
    typingAnimation.start()
  }
})

onUnmounted(() => {
  if (import.meta.client) {
    document.removeEventListener('click', handleClickOutside)
  }
})

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

/* Filters Card Styling */
.filters-card {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.12);
  background: linear-gradient(to bottom, rgba(var(--v-theme-surface), 1), rgba(var(--v-theme-surface), 0.98));
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(var(--v-theme-on-surface), 0.04);
}

.filters-card:hover {
  box-shadow: 0 8px 24px rgba(var(--v-theme-on-surface), 0.1);
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.filters-card__inner {
  padding: 24px 20px;
}

@media (min-width: 960px) {
  .filters-card__inner {
    padding: 32px 36px;
  }
}

/* Filters Header */
.filters-header {
  position: relative;
  padding-bottom: 16px;
  margin-bottom: 16px;
  border-bottom: 2px solid rgba(var(--v-theme-on-surface), 0.06);
}

.filters-header::after {
  content: '';
  position: absolute;
  bottom: -2px;
  right: 0;
  width: 80px;
  height: 2px;
  background: linear-gradient(to left, rgb(var(--v-theme-primary)), transparent);
  border-radius: 2px;
  animation: slideRight 0.5s ease-out;
}

@keyframes slideRight {
  from {
    width: 0;
    opacity: 0;
  }
  to {
    width: 80px;
    opacity: 1;
  }
}

/* Label Section Headers */
.label-section-header,
.label-section-mobile {
  padding: 12px 0 8px;
  background: rgba(var(--v-theme-primary), 0.02);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 8px;
}

.label-section-header .v-icon,
.label-section-mobile .v-icon {
  transition: transform 0.3s ease;
}

.label-section-header:hover .v-icon,
.label-section-mobile:hover .v-icon {
  transform: rotate(10deg) scale(1.1);
}

/* Active Labels Summary */
.active-labels-summary,
.active-labels-mobile {
  animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.active-label-chip {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.active-label-chip:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 6px 12px rgba(var(--v-theme-on-surface), 0.15);
}

.active-label-chip :deep(.v-chip__close) {
  transition: all 0.2s ease;
}

.active-label-chip:hover :deep(.v-chip__close) {
  transform: rotate(90deg);
}

/* Slide Fade Transition */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Animation Keyframes */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Field Styling */
.filters-row {
  gap: 16px;
}

.filter-select {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-select :deep(.v-field) {
  box-shadow: 0 2px 8px rgba(var(--v-theme-on-surface), 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-select :deep(.v-field:hover) {
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.08);
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.filter-select :deep(.v-field--focused) {
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.12);
}

.filter-menu-item {
  transition: all 0.2s ease;
  border-radius: 8px;
  margin: 4px 8px;
}

.filter-menu-item:hover {
  background: rgba(var(--v-theme-primary), 0.08) !important;
  transform: translateX(-4px);
}

:deep(.v-field__input) {
  color: rgba(var(--v-theme-on-surface), 0.92);
  font-size: 0.95rem;
}

:deep(.v-field__label) {
  color: rgba(var(--v-theme-on-surface), 0.72);
  font-weight: 500;
}

:deep(.v-field__input::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.56);
}

:deep(.v-field--variant-outlined) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.v-field--variant-outlined .v-field__outline) {
  border-radius: 12px;
}

:deep(.v-field--variant-outlined:hover .v-field__outline) {
  --v-field-border-opacity: 0.5;
  color: rgb(var(--v-theme-primary));
}

:deep(.v-field--focused .v-field__outline) {
  --v-field-border-width: 2px;
  color: rgb(var(--v-theme-primary)) !important;
}

:deep(.v-field--focused) {
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.08);
}

:deep(.v-select .v-field__prepend-inner) {
  margin-inline-end: 8px;
}

:deep(.v-select .v-field__prepend-inner .v-icon) {
  opacity: 0.7;
  transition: all 0.2s ease;
}

:deep(.v-select:hover .v-field__prepend-inner .v-icon) {
  opacity: 1;
  color: rgb(var(--v-theme-primary));
}

/* Mobile Expansion Panel Styling */
.filters-card__drawer-title {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.06), rgba(var(--v-theme-primary), 0.02));
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid rgba(var(--v-theme-primary), 0.12);
}

.filters-card__drawer-title:hover {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08), rgba(var(--v-theme-primary), 0.04));
  border-color: rgba(var(--v-theme-primary), 0.2);
}

:deep(.v-expansion-panel) {
  border-radius: 16px !important;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(var(--v-theme-on-surface), 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.v-expansion-panel--active) {
  box-shadow: 0 4px 16px rgba(var(--v-theme-on-surface), 0.1);
}

:deep(.v-expansion-panel-title) {
  padding: 18px 20px;
  font-weight: 500;
}

:deep(.v-expansion-panel-title__icon) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.v-expansion-panel--active .v-expansion-panel-title__icon) {
  transform: rotate(180deg);
  color: rgb(var(--v-theme-primary));
}

:deep(.v-expansion-panel-text__wrapper) {
  padding: 20px;
  background: rgba(var(--v-theme-surface), 0.98);
}

/* Grid spacing adjustments for desktop to fit 3 rows comfortably */
.products-grid {
  /* default (mobile/tablet) */
  --v-gutter-x: 12px;
  --v-gutter-y: 16px;
}

@media (min-width: 960px) {
  .products-grid {
    --v-gutter-x: 16px;
    --v-gutter-y: 18px;
  }
}

@media (min-width: 1280px) {
  .products-grid {
    --v-gutter-x: 18px;
    --v-gutter-y: 20px;
  }
}

.label-filters-row {
  margin-bottom: 16px;
}

/* Utility Classes */
.gap-2 {
  gap: 8px;
}

.w-100 {
  width: 100%;
}

/* Chip Styling */
:deep(.v-chip) {
  transition: all 0.2s ease;
}

:deep(.v-chip:hover) {
  transform: translateY(-1px);
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

  .filters-card__inner {
    padding: 16px 12px;
  }
  
  .filters-header h3 {
    font-size: 1.1rem;
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

  :deep(.v-field__input) {
    font-size: 0.9rem;
  }
}
</style>


