<template>
  <div class="label-page">
    <v-container v-if="!labelSeo && !pageError" class="py-16 text-center">
      <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
      <p class="text-body-1 text-medium-emphasis">{{ t('loading') }}</p>
    </v-container>

    <div v-else>
      <section class="hero">
        <v-container class="py-10 text-white">
          <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0 mb-4">
            <template #divider>
              <v-icon>mdi-chevron-left</v-icon>
            </template>
          </v-breadcrumbs>
          <h1 class="text-h3 text-md-h2 font-weight-bold mb-3 text-center">
            {{ pageTitle }}
          </h1>
          <p
            v-if="labelSeo?.seo_intro_text"
            class="text-subtitle-1 opacity-90 mx-auto max-w-640 text-center"
            v-html="labelSeo.seo_intro_text"
          />
        </v-container>
      </section>

    <v-container class="py-8">
      <div v-if="labelBadges.length" class="label-badges mb-6">
        <h3 class="text-subtitle-1 mb-2">فیلترهای فعال</h3>
        <div class="d-flex flex-wrap gap-2">
          <v-chip
            v-for="badge in labelBadges"
            :key="badge.slug"
            size="small"
            variant="tonal"
            class="label-badge-chip"
          >
            {{ badge.name }}
          </v-chip>
        </div>
      </div>

      <ListSkeleton
        v-if="loadingProducts"
        type="product"
        variant="grid"
        :count="pageSize"
        :cols="12"
        :sm="6"
        :md="4"
        :lg="3"
      />

      <v-alert v-else-if="pageError" type="error" variant="tonal" class="mb-6">
        {{ pageError }}
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
        </v-card>

        <div v-if="pagination.count > products.length" class="d-flex justify-center mt-10">
          <v-pagination v-model="page" :length="pageCount" :total-visible="5" @update:model-value="onPageChange" />
        </div>
      </template>

      <v-card v-if="labelSeo?.description" elevation="4" rounded="xl" class="description-card mt-12">
        <v-card-title class="d-flex align-center gap-3">
          <v-avatar size="48" class="description-icon" variant="tonal" color="primary">
            <v-icon>mdi-text-box</v-icon>
          </v-avatar>
          <div>
            <h2 class="text-h6 text-md-h5 font-weight-bold mb-1">
              درباره {{ labelSeo.name }}
            </h2>
            <p class="text-body-2 text-medium-emphasis mb-0">
              توضیحاتی درباره این برچسب و کاربردهای آن
            </p>
          </div>
        </v-card-title>
        <v-card-text>
          <div
            v-html="descriptionHtml"
            class="content-body"
            data-testid="label-description"
          />
        </v-card-text>
      </v-card>

      <section v-if="faqItems.length" class="faq-section mt-12">
        <h3 class="text-h6 mb-3">سوالات متداول</h3>
        <div v-for="item in faqItems" :key="item.question" class="faq-item mb-4">
          <h4 class="text-subtitle-2 font-weight-medium mb-1">{{ item.question }}</h4>
          <p class="text-body-2 text-medium-emphasis">{{ item.answer }}</p>
        </div>
      </section>
    </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createError } from 'h3'

import ListSkeleton from '~/components/skeletons/ListSkeleton.vue'
import ProductCard from '~/components/product/ProductCard.vue'
import { useProductStore } from '~/stores/product'
import { useApiFetch } from '~/composables/useApiFetch'
import { generateCollectionPageSchema, generateBreadcrumbSchema, prepareSchemaScripts } from '~/composables/useSchema'

type Product = Record<string, any>
type PaginatedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

const config = useRuntimeConfig()
const productStore = useProductStore()
const t = productStore.t
const route = useRoute()
const slugParam = computed(() => route.params.labelSlug)
const slugSegments = computed(() => {
  if (!slugParam.value) {
    return []
  }

  const segments = Array.isArray(slugParam.value) ? slugParam.value : [slugParam.value]
  return segments.filter(Boolean)
})

const labelSeo = ref<Record<string, any> | null>(null)
const products = ref<Product[]>([])
const pagination = reactive({
  count: 0,
  next: null as string | null,
  previous: null as string | null
})
const page = ref(1)
const pageSize = 12
const loadingProducts = ref(false)
const pageError = ref<string | null>(null)

// Build label query from API response (for combo pages) or from slug segments (for single labels)
const labelQuery = computed(() => {
  if (labelSeo.value?.labels && Array.isArray(labelSeo.value.labels) && labelSeo.value.labels.length > 0) {
    // For combo pages, use all label slugs from the response
    return labelSeo.value.labels.map((l: any) => l.slug || l).join(',')
  }
  // For single labels, use the slug from the response or fallback to URL segments
  if (labelSeo.value?.slug) {
    return labelSeo.value.slug
  }
  return slugSegments.value.filter(Boolean).join(',')
})
const comboSlug = computed(() => slugSegments.value.join('-'))
const isIndexable = computed(() => Boolean(labelSeo.value?.is_indexable ?? labelSeo.value?.is_seo_page))

const baseUrl = config.public.siteUrl || (process.client ? window.location.origin : 'https://indexo.ir')

// Get canonical URL (check DB first, then fallback to slug)
const canonicalUrl = computed(() => {
  if (!labelSeo.value) return ''
  if (labelSeo.value.canonical_url) {
    return labelSeo.value.canonical_url
  }
  return `${baseUrl}/machinery/${labelSeo.value.slug ?? slugSegments.value.join('/')}/`
})

// Get OG image (primary image)
const ogImage = computed(() => {
  return labelSeo.value?.og_image_url || labelSeo.value?.og_image || ''
})

const loadSeoContent = async () => {
  if (!slugSegments.value.length) {
    throw createError({
      statusCode: 404,
      message: 'آدرس وارد شده معتبر نیست.'
    })
  }

  let payload = null

  if (comboSlug.value) {
    try {
      // Use skip404Redirect to prevent navigation on expected 404s
      payload = await useApiFetch(`label-combos/${comboSlug.value}/`, {
        skip404Redirect: true
      })
    } catch (err) {
      // Fallback to single label if combo is not defined - this is expected
    }
  }

  if (!payload) {
    const fallback = slugSegments.value[slugSegments.value.length - 1]
    try {
      payload = await useApiFetch(`labels/seo-content/${fallback}/`, {
        skip404Redirect: true
      })
    } catch (err) {
      console.error('Error loading label SEO content:', err)
    }
  }

  if (!payload) {
    throw createError({
      statusCode: 404,
      message: 'محتوای مورد نظر یافت نشد.'
    })
  }

  labelSeo.value = payload
}

const fetchProductsForPage = async (pageNumber = 1) => {
  // Wait for label to be loaded if not already
  if (!labelSeo.value) {
    await loadSeoContent()
  }
  
  loadingProducts.value = true
  pageError.value = null

  try {
    // Use the label slug from the API response
    const labelsParam = labelQuery.value || (labelSeo.value?.slug ? labelSeo.value.slug : undefined)
    
    const response = await useApiFetch<PaginatedResponse<Product>>('products/', {
      query: {
        page: pageNumber,
        page_size: pageSize,
        labels: labelsParam,
        ordering: '-created_at'
      }
    })

    const data = Array.isArray(response) ? response : response.results ?? []
    products.value = data

    if (!Array.isArray(response)) {
      pagination.count = response.count ?? data.length
      pagination.next = response.next ?? null
      pagination.previous = response.previous ?? null
    } else {
      pagination.count = data.length
      pagination.next = null
      pagination.previous = null
    }

    page.value = pageNumber
  } catch (err: any) {
    pageError.value = err?.data?.detail ?? err?.message ?? 'خطا در دریافت محصولات'
  } finally {
    loadingProducts.value = false
  }
}

const loadLabelPage = async () => {
  await loadSeoContent()
  await fetchProductsForPage(1)
  // Return the data to ensure it's available for SSR
  return { 
    labelSeo: labelSeo.value, 
    products: products.value,
    pagination: { ...pagination }
  }
}

const { data: pageData, pending, error: asyncError, refresh } = await useAsyncData(
  `label-page-${comboSlug.value}`,
  loadLabelPage,
  {
    // Ensure data is available during SSR
    server: true,
    default: () => ({ labelSeo: null, products: [], pagination: { count: 0, next: null, previous: null } })
  }
)

// Sync data from useAsyncData to refs (for reactivity)
if (pageData.value) {
  if (pageData.value.labelSeo) {
    labelSeo.value = pageData.value.labelSeo
  }
  if (pageData.value.products) {
    products.value = pageData.value.products
  }
  if (pageData.value.pagination) {
    Object.assign(pagination, pageData.value.pagination)
  }
}

// Set pageError if asyncData failed
if (asyncError.value) {
  pageError.value = asyncError.value.message || 'خطا در بارگذاری صفحه'
}

// Watch for route changes and reload data
watch(
  () => route.params.labelSlug,
  async (newSlug, oldSlug) => {
    if (newSlug !== oldSlug) {
      // Reset state
      labelSeo.value = null
      products.value = []
      pageError.value = null
      // Reload data
      await refresh()
    }
  }
)

const pageTitle = computed(() => labelSeo.value?.seo_h1 ?? labelSeo.value?.name ?? t('products'))
const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: pageTitle.value, disabled: true }
])
const labelBadges = computed(() => {
  if (!labelSeo.value) {
    return []
  }

  if (Array.isArray(labelSeo.value.labels) && labelSeo.value.labels.length) {
    return labelSeo.value.labels
  }

  return [
    {
      name: labelSeo.value.name ?? slugSegments.value[slugSegments.value.length - 1] ?? '',
      slug: labelSeo.value.slug ?? slugSegments.value[slugSegments.value.length - 1]
    }
  ]
})
const faqItems = computed(() => (Array.isArray(labelSeo.value?.seo_faq) ? labelSeo.value!.seo_faq : []))
const pageCount = computed(() => Math.max(1, Math.ceil(pagination.count / pageSize)))

// Format description as HTML (similar to subcategory store)
const descriptionHtml = computed(() => {
  if (!labelSeo.value?.description) {
    return `<p>برای این برچسب هنوز توضیحاتی ثبت نشده است.</p>`
  }
  
  const desc = labelSeo.value.description.trim()
  // Check if it already contains HTML tags
  const hasHtmlTags = /<\/?[a-z][\w-]*\b[^>]*>/i.test(desc)
  // If it has HTML tags, return as is, otherwise wrap in paragraph
  return hasHtmlTags ? desc : `<p>${desc}</p>`
})

// Generate schemas using products already loaded
const collectionSchema = computed(() => {
  if (!labelSeo.value) return null
  return generateCollectionPageSchema(
    {
      name: labelSeo.value.name,
      description: labelSeo.value.description,
      slug: labelSeo.value.slug,
      meta_description: labelSeo.value.seo_description
    },
    products.value.slice(0, 10).map(p => ({
      name: p.name,
      slug: p.slug,
      id: p.id
    })),
    baseUrl,
    'Subcategory' // Using Subcategory type for CollectionPage schema
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

// SEO Meta Tags
useSeoMeta({
  title: () => labelSeo.value?.seo_title ?? labelSeo.value?.name ?? 'برچسب',
  description: () =>
    labelSeo.value?.seo_description ?? labelSeo.value?.description ?? '',
  ogTitle: () => labelSeo.value?.seo_title ?? labelSeo.value?.name ?? '',
  ogDescription: () =>
    labelSeo.value?.seo_description ?? labelSeo.value?.description ?? '',
  ogType: 'website',
  ogImage: () => ogImage.value,
  twitterCard: 'summary_large_image',
  twitterTitle: () => labelSeo.value?.seo_title ?? labelSeo.value?.name ?? '',
  twitterDescription: () =>
    labelSeo.value?.seo_description ?? labelSeo.value?.description ?? '',
  twitterImage: () => ogImage.value,
  robots: () => isIndexable.value ? 'index, follow' : 'noindex, follow'
})

// Schema markup and canonical URL
useHead(() => {
  const schemas: any[] = []
  
  // Add custom schema_markup from DB if available
  if (labelSeo.value?.schema_markup) {
    try {
      const parsed = typeof labelSeo.value.schema_markup === 'string' 
        ? JSON.parse(labelSeo.value.schema_markup) 
        : labelSeo.value.schema_markup
      schemas.push(parsed)
    } catch (e) {
      console.warn('Failed to parse schema_markup:', e)
    }
  }
  
  // Add generated collection schema
  if (collectionSchema.value) {
    schemas.push(collectionSchema.value)
  }
  
  // Add breadcrumb schema
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

const onPageChange = async (value: number) => {
  page.value = value
  await fetchProductsForPage(value)
}
</script>

<style scoped>
.label-page {
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

.label-badges {
  padding: 0 12px;
}

.label-badge-chip {
  font-weight: 500;
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

.faq-section {
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.1);
  padding-top: 24px;
}
</style>

