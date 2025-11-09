<template>
  <div v-if="subcategory" class="subcategory-detail">
    <section class="hero">
      <v-container class="py-10 text-white">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ subcategory.name }}
        </h1>
        <p class="text-subtitle-1 opacity-90 max-w-720">
          {{ subcategory.description || 'جزئیات این زیردسته به زودی تکمیل می‌شود.' }}
        </p>
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
          <v-row v-if="products.length" class="ga-4">
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

const breadcrumbs = computed(() => {
  const items = [
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
.hero {
  background: linear-gradient(135deg, rgba(0, 197, 142, 0.85), rgba(0, 111, 82, 0.85));
  color: white;
}

.max-w-720 {
  max-width: 720px;
}
</style>

