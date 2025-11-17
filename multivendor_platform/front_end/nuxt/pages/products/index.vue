<template>
  <div class="products-page">
    <section class="hero">
      <v-container class="py-10 text-white">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0 mb-4">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3 text-center">
          {{ t('products') }}
        </h1>
        <p class="text-subtitle-1 opacity-90 mx-auto max-w-640 text-center">
          {{ t('discoverMarketplace') }}
        </p>
      </v-container>
    </section>

    <v-container class="py-8">
      <v-card class="filters-card mb-8" elevation="2" rounded="xl">
        <div class="filters-card__inner">
          <!-- Filter header with active count -->
          <div class="filters-header mb-4">
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center gap-2">
                <v-icon size="24" color="primary">mdi-filter-variant</v-icon>
                <h3 class="text-h6 font-weight-bold">فیلترها</h3>
                <v-chip
                  v-if="activeFiltersCount"
                  size="small"
                  color="primary"
                  variant="flat"
                  class="mr-2"
                >
                  {{ activeFiltersCount }}
                </v-chip>
              </div>
              <v-btn
                v-if="activeFiltersCount"
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

          <v-divider class="mb-6" />

          <!-- Top row: search + category (always visible) -->
          <v-row class="mb-4" align="center">
            <v-col cols="12" md="4">
              <div class="search-wrapper">
                <v-text-field
                  v-model="search"
                  :label="t('searchProducts')"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-magnify"
                  clearable
                  @keyup.enter="applyFilters"
                  @click:clear="() => { search = ''; applyFilters(); }"
                >
                  <template #append-inner>
                    <v-btn
                      icon="mdi-arrow-left"
                      size="x-small"
                      variant="flat"
                      color="primary"
                      @click="applyFilters"
                    />
                  </template>
                </v-text-field>
              </div>
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="selectedCategory"
                :items="categoryOptions"
                item-title="name"
                item-value="id"
                variant="outlined"
                density="comfortable"
                :label="t('selectCategory')"
                prepend-inner-icon="mdi-shape"
                clearable
                @update:model-value="applyFilters"
              >
                <template #selection="{ item }">
                  <div class="d-flex align-center">
                    <v-icon size="16" class="ml-2">mdi-check-circle</v-icon>
                    <span>{{ item.title }}</span>
                  </div>
                </template>
              </v-select>
            </v-col>
            <v-col v-if="mdAndUp" cols="12" md="4">
              <v-select
                v-model="ordering"
                :items="orderingOptions"
                variant="outlined"
                density="comfortable"
                :label="t('sortBy')"
                prepend-inner-icon="mdi-sort"
                clearable
                @update:model-value="applyFilters"
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

          <!-- Desktop layout: subcategory + labels + active chips inside the same card -->
          <template v-if="mdAndUp">
            <!-- Only show divider if category is selected or there are subcategories -->
            <v-divider v-if="selectedCategory || subcategoryOptions.length" class="mb-6" />
            
            <v-row v-if="selectedCategory" class="mb-4" align="center">
              <v-col cols="12" md="4">
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
            <v-divider class="my-4" />
            
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
                    <v-col cols="12">
                      <v-select
                        v-model="ordering"
                        :items="orderingOptions"
                        variant="outlined"
                        density="comfortable"
                        :label="t('sortBy')"
                        prepend-inner-icon="mdi-sort"
                        clearable
                        @update:model-value="applyFilters"
                      />
                    </v-col>
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

      <ListSkeleton
        v-if="loading"
        type="product"
        variant="grid"
        :count="12"
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
definePageMeta({
  layout: 'default'
})

useSeoMeta({
  title: 'محصولات',
  description: 'همه محصولات ایندکسو را مرور کنید و بهترین پیشنهادها را بیابید.',
  ogTitle: 'محصولات ایندکسو',
  ogDescription: 'مقایسه و انتخاب محصولات از فروشندگان متعدد در ایندکسو.',
  ogType: 'website'
})

import { useDisplay } from 'vuetify'
import LabelFilters from '~/components/product/LabelFilters.vue'
import ListSkeleton from '~/components/skeletons/ListSkeleton.vue'
import type { LocationQueryValue } from 'vue-router'
import { useLabelStore } from '~/stores/label'

const productStore = useProductStore()
const { products, loading, error, pagination } = storeToRefs(productStore)
const t = productStore.t
const { mdAndUp } = useDisplay()

const search = ref('')
const selectedCategory = ref<number | null>(null)
const selectedSubcategory = ref<number | null>(null)
const ordering = ref<string | null>(null)
const page = ref(1)
const pageSize = 12
const mobileFiltersExpanded = ref<number | undefined>(undefined)
const hasLabelGroups = ref(false)

const labelStore = useLabelStore()
const route = useRoute()
const router = useRouter()
const selectedLabels = ref<string[]>([])
const subcategoryOptions = ref<any[]>([])
let skipLabelWatcher = false

// Computed property to determine if label filters should be shown
const shouldShowLabelFilters = computed(() => {
  // Show if a category is selected AND there are label groups available
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

// Computed property for mobile filters count (excluding search and category which are always visible)
const mobileActiveFiltersCount = computed(() => {
  let count = 0
  if (selectedSubcategory.value) count++
  if (ordering.value) count++
  if (selectedLabels.value.length) count += selectedLabels.value.length
  return count
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
    // Only apply filters if labels actually changed (not from route sync)
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
  // labelStore.labelGroups is now guaranteed to be an array via computed getter
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
    hasLabelGroups.value = false // Reset label groups flag
    
    if (newCategory) {
      void fetchSubcategories(newCategory)
      // Fetch label groups for the selected category
      void labelStore.fetchLabelGroupsForSubcategory(null, true)
    } else {
      // Clear label groups when no category is selected
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

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('products'), disabled: true }
])

const fetchCategories = async () => {
  try {
    const data = await useApiFetch<any[] | { results: any[] }>('categories/')
    categoryOptions.value = Array.isArray(data) ? data : data.results ?? []
  } catch (err) {
    console.error('Error fetching categories for filters:', err)
  }
}

const fetchPage = async () => {
  await productStore.fetchProducts({
    page: page.value,
    page_size: pageSize,
    search: search.value || undefined,
    category: selectedCategory.value || undefined,
    subcategory: selectedSubcategory.value || undefined,
    ordering: ordering.value || undefined,
    labels: selectedLabels.value.length ? selectedLabels.value.join(',') : undefined
  })
}

await useAsyncData('product-list-page', async () => {
  await Promise.all([
    fetchCategories(),
    fetchPage(),
    labelStore.fetchLabelGroupsForSubcategory(null, true)
  ])
})

const onPageChange = async (value: number) => {
  page.value = value
  await fetchPage()
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
  selectedCategory.value = null
  ordering.value = null
  page.value = 1
  skipLabelWatcher = true
  selectedLabels.value = []
  updateLabelsQuery([])
  await labelStore.fetchLabelGroupsForSubcategory(null, true)
  await fetchPage()
}
</script>

<style scoped>
.products-page {
  min-height: 100vh;
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.85), rgba(var(--v-theme-secondary), 0.9));
  color: rgba(var(--v-theme-on-primary), 0.98);
  border-radius: 24px;
  margin: 16px auto 36px;
  max-width: 1440px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.28), transparent 60%);
  pointer-events: none;
}

.max-w-640 {
  max-width: 640px;
}

/* Filters Card Styling */
.filters-card {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  background: linear-gradient(to bottom, rgba(var(--v-theme-surface), 1), rgba(var(--v-theme-surface), 0.98));
  transition: all 0.3s ease;
}

.filters-card:hover {
  box-shadow: 0 8px 24px rgba(var(--v-theme-on-surface), 0.08);
}

.filters-card__inner {
  padding: 20px 16px;
}

@media (min-width: 960px) {
  .filters-card__inner {
    padding: 28px 32px;
  }
}

/* Filters Header */
.filters-header {
  position: relative;
}

.filters-header::after {
  content: '';
  position: absolute;
  bottom: -12px;
  right: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(to left, rgb(var(--v-theme-primary)), transparent);
  border-radius: 2px;
}

/* Search Wrapper */
.search-wrapper {
  position: relative;
}

.search-wrapper :deep(.v-field--focused) {
  box-shadow: 0 0 0 3px rgba(var(--v-theme-primary), 0.1);
}

/* Label Section Headers */
.label-section-header,
.label-section-mobile {
  padding: 8px 0;
}

/* Active Labels Summary */
.active-labels-summary,
.active-labels-mobile {
  animation: slideIn 0.3s ease-out;
}

.active-label-chip {
  transition: all 0.2s ease;
}

.active-label-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(var(--v-theme-on-surface), 0.12);
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
:deep(.v-field__input) {
  color: rgba(var(--v-theme-on-surface), 0.92);
  font-size: 0.95rem;
}

:deep(.v-field__label) {
  color: rgba(var(--v-theme-on-surface), 0.72);
}

:deep(.v-field__input::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.56);
}

:deep(.v-field--variant-outlined) {
  transition: all 0.2s ease;
}

:deep(.v-field--variant-outlined:hover .v-field__outline) {
  --v-field-border-opacity: 0.4;
}

:deep(.v-field--focused .v-field__outline) {
  --v-field-border-width: 2px;
}

/* Mobile Expansion Panel Styling */
.filters-card__drawer-title {
  background: rgba(var(--v-theme-primary), 0.04);
  border-radius: 8px;
  font-weight: 500;
}

:deep(.v-expansion-panel) {
  border-radius: 12px !important;
  overflow: hidden;
}

:deep(.v-expansion-panel-title) {
  padding: 16px;
}

:deep(.v-expansion-panel-text__wrapper) {
  padding: 16px;
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

/* Mobile Optimizations */
@media (max-width: 959px) {
  .filters-card__inner {
    padding: 16px 12px;
  }
  
  .filters-header h3 {
    font-size: 1.1rem;
  }
}

/* Responsive Typography */
@media (max-width: 599px) {
  :deep(.v-field__input) {
    font-size: 0.9rem;
  }
}
</style>

