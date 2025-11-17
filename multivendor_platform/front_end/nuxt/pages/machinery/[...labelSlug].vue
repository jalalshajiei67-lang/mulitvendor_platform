<template>
  <div class="label-page">
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

      <section v-if="faqItems.length" class="faq-section mt-12">
        <h3 class="text-h6 mb-3">سوالات متداول</h3>
        <div v-for="item in faqItems" :key="item.question" class="faq-item mb-4">
          <h4 class="text-subtitle-2 font-weight-medium mb-1">{{ item.question }}</h4>
          <p class="text-body-2 text-medium-emphasis">{{ item.answer }}</p>
        </div>
      </section>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { createError } from 'h3'

import ListSkeleton from '~/components/skeletons/ListSkeleton.vue'
import ProductCard from '~/components/product/ProductCard.vue'
import { useProductStore } from '~/stores/product'
import { useApiFetch } from '~/composables/useApiFetch'
import { createLabelPageSchema } from '~/utils/schemaMarkup'

type Product = Record<string, any>
type PaginatedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

const runtimeConfig = useRuntimeConfig()
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

const labelQuery = computed(() => slugSegments.value.filter(Boolean).join(','))
const comboSlug = computed(() => slugSegments.value.join('-'))
const isIndexable = computed(() => Boolean(labelSeo.value?.is_indexable ?? labelSeo.value?.is_seo_page))
const canonicalUrl = computed(() => `/machinery/${labelSeo.value?.slug ?? slugSegments.value.join('/')}/`)

const loadSeoContent = async () => {
  if (!slugSegments.value.length) {
    throw createError({
      statusCode: 404,
      statusMessage: 'آدرس وارد شده معتبر نیست.'
    })
  }

  let payload = null

  if (comboSlug.value) {
    try {
      payload = await useApiFetch(`label-combos/${comboSlug.value}/`)
    } catch (err) {
      // Fallback to single label if combo is not defined
    }
  }

  if (!payload) {
    const fallback = slugSegments.value[slugSegments.value.length - 1]
    try {
      payload = await useApiFetch(`labels/${fallback}/seo-content/`)
    } catch (err) {
      //
    }
  }

  if (!payload) {
    throw createError({
      statusCode: 404,
      statusMessage: 'محتوای مورد نظر یافت نشد.'
    })
  }

  labelSeo.value = payload
}

const fetchProductsForPage = async (pageNumber = 1) => {
  loadingProducts.value = true
  pageError.value = null

  try {
    const response = await useApiFetch<PaginatedResponse<Product>>('products/', {
      query: {
        page: pageNumber,
        page_size: pageSize,
        labels: labelQuery.value || undefined,
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
}

await useAsyncData(() => ['label-page', comboSlug.value], loadLabelPage)

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
const labelSchema = computed(() => {
  if (!labelSeo.value) {
    return []
  }

  return createLabelPageSchema({
    label: labelSeo.value,
    products: products.value,
    canonical: canonicalUrl.value,
    siteUrl: runtimeConfig.public.siteUrl
  })
})

watch(
  () => labelSeo.value,
  (value) => {
    if (!value) {
      return
    }

    useSeoMeta({
      title: value.seo_title ?? `${value.name} | ${t('products')}`,
      description: value.seo_description ?? '',
      ogTitle: value.seo_title ?? value.name,
      ogDescription: value.seo_description ?? '',
      ogImage: value.og_image,
      canonical: canonicalUrl.value,
      robots: isIndexable.value ? 'index, follow' : 'noindex, follow'
    })
  },
  { immediate: true }
)

watch(
  () => labelSeo.value?.schema_markup,
  (schema) => {
    if (!schema) {
      return
    }

    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: schema
        }
      ]
    })
  },
  { immediate: true }
)

watch(
  labelSchema,
  (schema) => {
    if (!schema.length) {
      return
    }

    useHead({
      script: schema.map((entry) => ({
        type: 'application/ld+json',
        children: JSON.stringify(entry)
      }))
    })
  },
  { immediate: true }
)

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

.faq-section {
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.1);
  padding-top: 24px;
}
</style>

