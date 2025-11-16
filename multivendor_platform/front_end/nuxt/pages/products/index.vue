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
      <v-row class="mb-6" align="center">
        <v-col cols="12" md="4">
          <v-text-field
            v-model="search"
            :label="t('searchProducts')"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-magnify"
            @keyup.enter="applyFilters"
          />
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
            clearable
            @update:model-value="applyFilters"
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="ordering"
            :items="orderingOptions"
            variant="outlined"
            density="comfortable"
            :label="t('sortBy')"
            @update:model-value="applyFilters"
          />
        </v-col>
      </v-row>

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

const productStore = useProductStore()
const { products, loading, error, pagination } = storeToRefs(productStore)
const t = productStore.t

const search = ref('')
const selectedCategory = ref<number | null>(null)
const ordering = ref<string | null>(null)
const page = ref(1)
const pageSize = 12

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
    ordering: ordering.value || undefined
  })
}

await useAsyncData('product-list-page', async () => {
  await Promise.all([fetchCategories(), fetchPage()])
})

const onPageChange = async (value: number) => {
  page.value = value
  await fetchPage()
}

const applyFilters = async () => {
  page.value = 1
  await fetchPage()
}

const resetFilters = async () => {
  search.value = ''
  selectedCategory.value = null
  ordering.value = null
  page.value = 1
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
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.2), rgba(var(--v-theme-secondary), 0.2));
  color: rgba(var(--v-theme-on-surface), 0.98);
  border-radius: 24px;
  margin-top: 12px;
  margin-bottom: 32px;
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

:deep(.v-field__input) {
  color: rgba(var(--v-theme-on-surface), 0.92);
}

:deep(.v-field__label) {
  color: rgba(var(--v-theme-on-surface), 0.72);
}

:deep(.v-field__input::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.56);
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
</style>

