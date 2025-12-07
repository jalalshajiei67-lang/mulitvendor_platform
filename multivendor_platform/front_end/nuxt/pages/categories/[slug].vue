<template>
  <div v-if="category" class="category-detail">
    <section class="hero" :class="{ 'has-image': formatImageUrl(category) }" :style="heroImageStyle">
      <v-container class="py-10">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0 mb-4">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <v-row align="center" class="text-white">
          <v-col cols="12" md="8">
            <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
              {{ category.name }}
            </h1>
          </v-col>
          <v-col v-if="formatImageUrl(category)" cols="12" md="4" class="text-center">
            <v-img
              :src="formatImageUrl(category) || ''"
              max-width="200"
              max-height="200"
              class="mx-auto rounded-xl hero-category-image"
              cover
            >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-skeleton-loader type="image" width="100%" height="100%" />
                </div>
              </template>
            </v-img>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <v-container class="py-8">
      <v-row class="mb-6" v-if="category.department_name">
        <v-col cols="12" md="4">
          <v-card elevation="2" rounded="xl" class="pa-6">
            <h2 class="text-subtitle-1 font-weight-bold mb-2">دپارتمان مرتبط</h2>
            <p class="text-body-2 text-medium-emphasis mb-4">
              {{ category.department_name }}
            </p>
            <v-btn
              v-if="category.department_slug"
              color="primary"
              variant="tonal"
              @click="navigateTo(`/departments/${category.department_slug}`)"
            >
              مشاهده دپارتمان
              <v-icon class="mr-2">mdi-arrow-left</v-icon>
            </v-btn>
          </v-card>
        </v-col>
      </v-row>

      <section class="mb-12">
        <header class="section-header d-flex align-center justify-space-between mb-6">
          <div>
            <h2 class="text-h5 text-md-h4 font-weight-bold mb-1">زیردسته‌های مرتبط</h2>
            <p v-if="!subLoading && subcategories.length" class="text-body-2 text-medium-emphasis mb-0">
              {{ subcategories.length }} زیردسته موجود است
            </p>
          </div>
          <v-btn variant="text" color="primary" @click="refreshSubcategories" size="small" :disabled="subLoading">
            بروزرسانی
            <v-icon class="mr-2" size="18">mdi-refresh</v-icon>
          </v-btn>
        </header>

        <div v-if="subLoading" class="text-center py-10">
          <v-progress-circular indeterminate color="primary" size="56" class="mb-4" />
          <p class="text-body-1 text-medium-emphasis">در حال دریافت زیردسته‌ها...</p>
        </div>

        <v-alert v-else-if="subError" type="error" variant="tonal">
          {{ subError }}
        </v-alert>

        <v-row v-else-if="subcategories.length" class="g-4">
          <v-col
            v-for="sub in subcategories"
            :key="sub.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card 
              rounded="xl" 
              elevation="2" 
              class="subcategory-card h-100" 
              hover
              @click="navigateTo(`/subcategories/${sub.slug}`)"
            >
              <v-card-text class="pa-6 d-flex flex-column h-100">
                <v-img
                  v-if="formatImageUrl(sub)"
                  height="180"
                  :src="formatImageUrl(sub) || ''"
                  cover
                  class="mb-4 rounded-lg"
                  loading="lazy"
                >
                  <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                      <v-skeleton-loader type="image" width="100%" height="100%" />
                    </div>
                  </template>
                </v-img>
                <div v-else class="d-flex align-center justify-center mb-4 subcategory-placeholder">
                  <v-icon size="56" color="primary">mdi-tag-multiple</v-icon>
                </div>
                <h3 class="text-h6 font-weight-bold mb-2 flex-grow-1">{{ sub.name }}</h3>
                <div class="d-flex align-center justify-space-between mt-auto pt-2">
                  <span class="text-primary text-body-2 font-weight-medium">
                    مشاهده محصولات
                  </span>
                  <v-icon color="primary" size="20">mdi-arrow-left</v-icon>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else elevation="1" rounded="xl" class="pa-8 text-center">
          <v-icon size="48" color="primary" class="mb-3">mdi-layers-triple-outline</v-icon>
          <h3 class="text-subtitle-1 mb-2">زیردسته‌ای یافت نشد</h3>
          <p class="text-body-2 text-medium-emphasis">
            برای این دسته هنوز زیردسته‌ای ثبت نشده است.
          </p>
        </v-card>
      </section>

      <v-card elevation="4" rounded="xl" class="description-card">
        <v-card-title class="d-flex align-center gap-3">
          <v-avatar size="48" class="description-icon" variant="tonal" color="primary">
            <v-icon>mdi-text-box-edit-outline</v-icon>
          </v-avatar>
          <div>
            <h2 class="text-h6 text-md-h5 font-weight-bold mb-1">
              درباره {{ category.name }}
            </h2>
            <p class="text-body-2 text-medium-emphasis mb-0">
              توضیحاتی کوتاه درباره این دسته‌بندی و کاربردهای آن
            </p>
          </div>
        </v-card-title>
        <v-card-text>
          <div
            v-html="category.description_html"
            class="content-body"
            data-testid="category-description"
          />
        </v-card-text>
      </v-card>
    </v-container>
  </div>

  <ProductDetailSkeleton v-else />
</template>

<script setup lang="ts">
import { formatImageUrl } from '~/utils/imageUtils'
import { generateCollectionPageSchema, generateBreadcrumbSchema, prepareSchemaScripts } from '~/composables/useSchema'

definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()
const productStore = useProductStore()

const { currentCategory } = storeToRefs(categoryStore)
const { subcategories, loading: subLoading, error: subError } = storeToRefs(subcategoryStore)
const { products: storeProducts } = storeToRefs(productStore)
const t = categoryStore.t

const category = computed(() => currentCategory.value)

const heroImageStyle = computed(() => {
  const imageUrl = formatImageUrl(category.value)
  if (imageUrl) {
    return {
      '--hero-bg-image': `url(${imageUrl})`
    } as Record<string, string>
  }
  return {}
})

type BreadcrumbItem = {
  title: string
  to?: string
  disabled?: boolean
}

const breadcrumbs = computed((): BreadcrumbItem[] => [
  { title: t('home'), to: '/' },
  { title: t('categories'), to: '/categories' },
  { title: category.value?.name ?? '', disabled: true }
])

const loadCategory = async () => {
  await categoryStore.fetchCategoryBySlug(slug.value)
}

const refreshSubcategories = async () => {
  if (!category.value) return
  await subcategoryStore.fetchSubcategories({
    category: category.value.id,
    page_size: 100
  })
}

await useAsyncData(`category-detail-${slug.value}`, async () => {
  await loadCategory()
  await refreshSubcategories()
  return true
})

watch(
  () => route.params.slug,
  async (next, prev) => {
    if (next !== prev) {
      await loadCategory()
      await refreshSubcategories()
    }
  }
)

const config = useRuntimeConfig()
const baseUrl = config.public.siteUrl || (process.client ? window.location.origin : 'https://indexo.ir')

// Fetch products for CollectionPage schema (first 10)
const fetchProductsForSchema = async () => {
  if (!category.value) return
  try {
    await productStore.fetchProducts({
      category: category.value.id,
      page_size: 10
    })
  } catch (error) {
    console.warn('Error fetching products for schema:', error)
  }
}

// Generate schemas
const collectionSchema = computed(() => {
  if (!category.value) return null
  return generateCollectionPageSchema(
    {
      name: category.value.name,
      description: category.value.description,
      slug: category.value.slug,
      meta_description: category.value.meta_description
    },
    storeProducts.value.slice(0, 10).map(p => ({
      name: p.name,
      slug: p.slug,
      id: p.id
    })),
    baseUrl,
    'Category'
  )
})

const breadcrumbSchema = computed(() => {
  if (!breadcrumbs.value.length) return null
  return generateBreadcrumbSchema(
    breadcrumbs.value.map(item => ({
      name: item.title,
      url: item.to ? `${baseUrl}${item.to}` : undefined
    })),
    baseUrl
  )
})

// Get canonical URL (check DB first, then fallback to slug)
const canonicalUrl = computed(() => {
  if (!category.value) return ''
  if (category.value.canonical_url) {
    return category.value.canonical_url
  }
  return `${baseUrl}/categories/${category.value.slug}`
})

// Get OG image (primary image)
const ogImage = computed(() => {
  return category.value?.og_image_url || category.value?.image_url || ''
})

// SEO Meta Tags
useSeoMeta({
  title: () => category.value?.meta_title ?? category.value?.name ?? 'دسته‌بندی',
  description: () =>
    category.value?.meta_description ?? category.value?.description ?? '',
  ogTitle: () => category.value?.meta_title ?? category.value?.name ?? '',
  ogDescription: () =>
    category.value?.meta_description ?? category.value?.description ?? '',
  ogType: 'website',
  ogImage: () => ogImage.value,
  twitterCard: 'summary_large_image',
  twitterTitle: () => category.value?.meta_title ?? category.value?.name ?? '',
  twitterDescription: () =>
    category.value?.meta_description ?? category.value?.description ?? '',
  twitterImage: () => ogImage.value
})

// Schema markup and canonical URL
useHead(() => {
  const schemas: any[] = []
  
  if (collectionSchema.value) {
    schemas.push(collectionSchema.value)
  }
  
  if (breadcrumbSchema.value) {
    schemas.push(breadcrumbSchema.value)
  }

  return {
    link: [
      { rel: 'canonical', href: canonicalUrl.value }
    ],
    ...(schemas.length > 0 && {
      script: prepareSchemaScripts(schemas)
    })
  }
})

// Fetch products for schema when category is loaded
watch(() => category.value, async (newCategory) => {
  if (newCategory) {
    await fetchProductsForSchema()
  }
}, { immediate: true })
</script>

<style scoped>
.category-detail {
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

.hero.has-image {
  background-image: var(--hero-bg-image);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.hero.has-image::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.85), rgba(var(--v-theme-secondary), 0.9));
  z-index: 0;
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.28), transparent 60%);
  pointer-events: none;
  z-index: 1;
}

.hero :deep(.v-container),
.hero :deep(.v-row),
.hero :deep(.v-col) {
  position: relative;
  z-index: 2;
}

.hero-category-image {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.subcategory-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  background: rgb(var(--v-theme-surface));
  overflow: hidden;
}

.subcategory-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 36px rgba(var(--v-theme-on-surface), 0.15);
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.subcategory-placeholder {
  height: 180px;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08), rgba(var(--v-theme-secondary), 0.08));
  border-radius: 8px;
  border: 2px dashed rgba(var(--v-theme-primary), 0.2);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.section-header {
  padding-bottom: 16px;
  border-bottom: 2px solid rgba(var(--v-theme-primary), 0.1);
}

.subcategory-card :deep(.text-medium-emphasis) {
  color: rgba(var(--v-theme-on-surface), 0.68) !important;
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

/* Content body styling - matching product detail page */
.content-body {
  max-width: 100%;
  line-height: 1.8;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
}
</style>

