<template>
  <div v-if="subcategory" class="subcategory-detail">
    <section class="hero">
      <v-container class="py-10">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ subcategory.name }}
        </h1>
      </v-container>
    </section>

    <v-container class="py-8">
      <section class="mb-12">
        <header class="d-flex flex-column flex-md-row justify-space-between align-center gap-4 mb-6">
          <div>
            <h2 class="text-h5 font-weight-bold mb-2">
              {{ t('products') }}
            </h2>
            <p class="text-body-2 text-medium-emphasis">
              محصولاتی که در این زیردسته قرار دارند.
            </p>
          </div>
        </header>

        <div v-if="productLoading" class="text-center py-10">
          <v-progress-circular indeterminate color="primary" size="56" class="mb-4" />
          <p class="text-body-1 text-medium-emphasis">{{ t('loading') }}</p>
        </div>

        <v-alert v-else-if="productError" type="error" variant="tonal" class="mb-6">
          {{ productError }}
        </v-alert>

        <template v-else>
          <v-row v-if="products.length" class="g-4">
            <v-col v-for="product in products" :key="product.id" cols="12" sm="6" md="4" xl="3">
              <ProductCard :product="product" />
            </v-col>
          </v-row>

          <v-card v-else elevation="1" rounded="xl" class="pa-10 text-center">
            <v-icon size="56" color="primary" class="mb-4">mdi-package-variant</v-icon>
            <h3 class="text-h6 mb-2">محصولی یافت نشد</h3>
            <p class="text-body-2 text-medium-emphasis mb-6">
              برای این زیردسته هنوز محصولی ثبت نشده است.
            </p>
          </v-card>

          <div v-if="pageCount > 1" class="d-flex justify-center mt-10">
            <v-pagination
              v-model="page"
              :length="pageCount"
              :total-visible="5"
              @update:model-value="onPageChange"
            />
          </div>
        </template>
      </section>

      <v-card elevation="4" rounded="xl" class="description-card">
        <v-card-title class="d-flex align-center gap-3">
          <v-avatar size="48" class="description-icon" variant="tonal" color="primary">
            <v-icon>mdi-text-box</v-icon>
          </v-avatar>
          <div>
            <h2 class="text-h6 text-md-h5 font-weight-bold mb-1">
              درباره {{ subcategory.name }}
            </h2>
            <p class="text-body-2 text-medium-emphasis mb-0">
              توضیحاتی درباره این زیردسته و کاربردهای آن
            </p>
          </div>
        </v-card-title>
        <v-card-text class="description-text">
          <div
            v-html="subcategory.description_html"
            class="text-body-1"
            data-testid="subcategory-description"
          />
        </v-card-text>
      </v-card>
    </v-container>
  </div>

  <v-container v-else class="py-16 text-center">
    <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
    <p class="text-body-1 text-medium-emphasis">{{ t('loading') }}</p>
  </v-container>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const subcategoryStore = useSubcategoryStore()
const productStore = useProductStore()

const { currentSubcategory } = storeToRefs(subcategoryStore)
const { products, pagination, loading: productLoading, error: productError } = storeToRefs(productStore)
const t = subcategoryStore.t

const subcategory = computed(() => currentSubcategory.value)

const page = ref(1)
const pageSize = 12
const pageCount = computed(() =>
  Math.max(1, Math.ceil((pagination.value.count || products.value.length || 0) / pageSize))
)

type BreadcrumbItem = {
  title: string
  to?: string
  disabled?: boolean
}

const breadcrumbs = computed(() => {
  const items: BreadcrumbItem[] = [
    { title: t('home'), to: '/' },
    { title: t('subcategories'), to: '/subcategories' }
  ]

  if (subcategory.value?.department_slug && subcategory.value?.department_name) {
    items.push({
      title: subcategory.value.department_name,
      to: `/departments/${subcategory.value.department_slug}`
    })
  }

  if (subcategory.value?.category_slug && subcategory.value?.category_name) {
    items.push({
      title: subcategory.value.category_name,
      to: `/categories/${subcategory.value.category_slug}`
    })
  }

  items.push({
    title: subcategory.value?.name ?? t('subcategory'),
    disabled: true
  })

  return items
})

const loadSubcategory = async () => {
  await subcategoryStore.fetchSubcategoryBySlug(slug.value)
}

const refreshProducts = async () => {
  if (!subcategory.value) return
  await productStore.fetchProducts({
    subcategory: subcategory.value.id,
    page: page.value,
    page_size: pageSize
  })
}

await useAsyncData(`subcategory-detail-${slug.value}`, async () => {
  await loadSubcategory()
  await refreshProducts()
  return true
})

const onPageChange = async (nextPage: number) => {
  page.value = nextPage
  await refreshProducts()
}

watch(
  () => route.params.slug,
  async (next, prev) => {
    if (next !== prev) {
      page.value = 1
      await loadSubcategory()
      await refreshProducts()
    }
  }
)

useSeoMeta({
  title: () => subcategory.value?.meta_title ?? subcategory.value?.name ?? 'زیردسته',
  description: () =>
    subcategory.value?.meta_description ?? subcategory.value?.description ?? '',
  ogTitle: () => subcategory.value?.meta_title ?? subcategory.value?.name ?? '',
  ogDescription: () =>
    subcategory.value?.meta_description ?? subcategory.value?.description ?? '',
  ogType: 'website'
})
</script>

<style scoped>
.subcategory-detail {
  min-height: 100vh;
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.24), rgba(var(--v-theme-secondary), 0.28));
  color: rgba(var(--v-theme-on-primary), 0.96);
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.24), transparent 60%);
  pointer-events: none;
}

.description-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.08);
  margin-top: 16px;
}

.description-icon :deep(.v-icon) {
  color: rgb(var(--v-theme-primary));
}

.description-text {
  line-height: 2;
}
</style>

