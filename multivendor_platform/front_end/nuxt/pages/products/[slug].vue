<template>
  <div v-if="product" class="product-detail">
    <section class="hero">
      <v-container class="py-8">
        <v-breadcrumbs
          :items="breadcrumbs"
          class="pa-0 text-white"
          density="comfortable"
        >
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold text-white mb-3">
          {{ product.name }}
        </h1>
        <p class="text-body-1 text-white opacity-85 max-w-720">
          {{ product.short_description }}
        </p>
      </v-container>
    </section>

    <v-container class="py-8">
      <v-row>
        <v-col cols="12" md="6">
          <v-sheet elevation="3" rounded="xl" class="pa-4">
            <v-img
              v-if="product.primary_image"
              :src="product.primary_image"
              :alt="product.name"
              height="420"
              class="rounded-lg"
              cover
              loading="lazy"
            >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-skeleton-loader type="image" width="100%" height="100%" />
                </div>
              </template>
            </v-img>
            <div v-else class="no-image">
              <v-icon size="64" color="grey-lighten-1">mdi-cube-outline</v-icon>
            </div>

            <v-slide-group
              v-if="product.images?.length"
              class="mt-4"
              show-arrows
            >
              <v-slide-group-item v-for="image in product.images" :key="image.id">
                <v-img
                  :src="image.image"
                  :alt="product.name"
                  height="80"
                  width="120"
                  cover
                  class="rounded-lg mx-2"
                  loading="lazy"
                  @click="setPrimary(image.image)"
                >
                  <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                      <v-skeleton-loader type="image" width="100%" height="100%" />
                    </div>
                  </template>
                </v-img>
              </v-slide-group-item>
            </v-slide-group>
          </v-sheet>
        </v-col>

        <v-col cols="12" md="6">
          <v-card elevation="3" rounded="xl" class="pa-6 mb-6">
            <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
              <v-chip color="primary" variant="tonal" v-if="product.category_name">
                {{ product.category_name }}
              </v-chip>
              <v-chip color="secondary" variant="tonal" v-if="product.vendor_name">
                {{ product.vendor_name }}
              </v-chip>
              <div class="d-flex align-center gap-2" v-if="vendorBadges.length">
                <BadgeIcon
                  v-for="badge in vendorBadges"
                  :key="badge.slug"
                  :badge="badge"
                  size="sm"
                />
              </div>
            </div>

            <div class="price-wrapper mb-6">
              <div class="text-caption text-medium-emphasis">{{ t('price') }}</div>
              <div class="text-h4 font-weight-bold">
                {{ product.price ? formatPrice(product.price) : t('contactForPrice') }}
              </div>
            </div>

            <v-btn block color="primary" size="large" @click="showRFQDialog = true" class="mb-3">
              {{ t('requestQuote') }}
            </v-btn>
            
            <!-- Debug: Show vendor info -->
            <div v-if="product" class="text-caption mb-2">
              Vendor ID: {{ product.vendor }} | Product ID: {{ product.id }}
            </div>
            
            <ProductChatButton
              v-if="product && product.vendor"
              :product-id="product.id"
              :vendor-id="product.vendor"
              block
            />
            <v-alert v-else-if="product && !product.vendor" type="warning" density="compact">
              No vendor assigned to this product
            </v-alert>

            <!-- Social Media Sharing Buttons -->
            <ProductShareButtons
              v-if="product"
              :url="productUrl"
              :title="product.name"
            />
          </v-card>

          <v-card elevation="1" rounded="xl" class="pa-6">
            <h2 class="text-subtitle-1 font-weight-bold mb-4">
              {{ t('keySpecifications') }}
            </h2>
            <v-list lines="two" density="comfortable">
              <v-list-item v-if="product.sku">
                <v-list-item-title>{{ t('sku') }}</v-list-item-title>
                <v-list-item-subtitle>{{ product.sku }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="product.stock">
                <v-list-item-title>{{ t('stockStatus') }}</v-list-item-title>
                <v-list-item-subtitle>{{ product.stock }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="product.minimum_order_quantity">
                <v-list-item-title>{{ t('minimumOrder') }}</v-list-item-title>
                <v-list-item-subtitle>{{ product.minimum_order_quantity }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="product.country_of_origin">
                <v-list-item-title>{{ t('originCountry') }}</v-list-item-title>
                <v-list-item-subtitle>{{ product.country_of_origin }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-8">
        <v-col cols="12" md="8">
          <v-card elevation="1" rounded="xl" class="pa-6">
            <h2 class="text-h5 font-weight-bold mb-4 readable-heading">توضیحات محصول</h2>
            
            <!-- Product Status Information -->
            <div v-if="product.availability_status || product.condition || product.origin || product.lead_time_days" class="mb-6">
              <v-divider class="mb-4"></v-divider>
              
              <div class="d-flex flex-column gap-3">
                <!-- Availability Status -->
                <div v-if="product.availability_status" class="d-flex align-center gap-2">
                  <v-icon color="primary">mdi-package-variant-closed</v-icon>
                  <span class="font-weight-medium">وضعیت موجودی:</span>
                  <v-chip size="small" :color="product.availability_status === 'in_stock' ? 'success' : 'warning'">
                    {{ product.availability_status === 'in_stock' ? 'موجود در انبار' : 'سفارشی' }}
                  </v-chip>
                </div>

                <!-- Condition (if in stock) -->
                <div v-if="product.availability_status === 'in_stock' && product.condition" class="d-flex align-center gap-2">
                  <v-icon color="info">mdi-check-circle</v-icon>
                  <span class="font-weight-medium">وضعیت:</span>
                  <v-chip size="small" :color="product.condition === 'new' ? 'success' : 'default'">
                    {{ product.condition === 'new' ? 'نو' : 'دست دوم' }}
                  </v-chip>
                </div>

                <!-- Lead Time (if made to order) -->
                <div v-if="product.availability_status === 'made_to_order' && product.lead_time_days" class="d-flex align-center gap-2">
                  <v-icon color="warning">mdi-calendar-clock</v-icon>
                  <span class="font-weight-medium">زمان تحویل:</span>
                  <span>{{ product.lead_time_days }} روز کاری</span>
                </div>

                <!-- Origin -->
                <div v-if="product.origin" class="d-flex align-center gap-2">
                  <v-icon color="secondary">mdi-earth</v-icon>
                  <span class="font-weight-medium">مبدا:</span>
                  <v-chip size="small" color="secondary" variant="tonal">
                    {{ product.origin === 'iran' ? 'ساخت ایران' : 'وارداتی' }}
                  </v-chip>
                </div>
              </div>

              <v-divider class="mt-4"></v-divider>
            </div>

            <!-- Key Features Table -->
            <div v-if="product.features && product.features.length > 0" class="mb-6">
              <h3 class="text-h6 font-weight-bold mb-3">ویژگی‌های کلیدی</h3>
              <v-table density="comfortable">
                <thead>
                  <tr>
                    <th class="text-right">نام ویژگی</th>
                    <th class="text-right">مقدار</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="feature in product.features" :key="feature.id">
                    <td class="font-weight-medium">{{ feature.name }}</td>
                    <td>{{ feature.value }}</td>
                  </tr>
                </tbody>
              </v-table>
              <v-divider class="mt-4"></v-divider>
            </div>

            <!-- Description -->
            <div class="content content-body" v-html="product.description"></div>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card v-if="product.related_products?.length" elevation="1" rounded="xl" class="pa-6">
            <h2 class="text-subtitle-1 font-weight-bold mb-4">{{ t('relatedProducts') }}</h2>
            <v-list lines="two" density="comfortable">
              <v-list-item
                v-for="item in product.related_products"
                :key="item.id"
                @click="navigateTo(`/products/${item.slug ?? item.id}`)"
                class="rounded-lg"
              >
                <template #prepend>
                  <v-avatar size="48" rounded="lg">
                    <v-img
                      :src="item.primary_image"
                      :alt="item.name"
                      cover
                      loading="lazy"
                    >
                      <template v-slot:placeholder>
                        <v-skeleton-loader type="avatar" />
                      </template>
                    </v-img>
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-medium">
                  {{ item.name }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ item.price ? formatPrice(item.price) : t('contactForPrice') }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>

  <ProductDetailSkeleton v-else />

  <!-- RFQ Form Dialog -->
  <LazyRFQForm
    v-if="showRFQDialog"
    v-model="showRFQDialog"
    :product-id="product?.id"
    :category-id="getCategoryId(product)"
    @submitted="handleRFQSubmitted"
    @error="handleRFQError"
  />

  <!-- Success/Error Messages -->
  <v-snackbar
    v-model="showSuccess"
    color="success"
    :timeout="3000"
    location="top"
  >
    درخواست استعلام قیمت با موفقیت ارسال شد
  </v-snackbar>

  <v-snackbar
    v-model="showError"
    color="error"
    :timeout="5000"
    location="top"
  >
    {{ errorMessage }}
  </v-snackbar>
</template>

<script setup lang="ts">
import { createError } from 'h3'
import { generateProductSchema, generateBreadcrumbSchema, prepareSchemaScripts } from '~/composables/useSchema'
import BadgeIcon from '~/components/gamification/BadgeIcon.vue'
import ProductDetailSkeleton from '~/components/skeletons/ProductDetailSkeleton.vue'

definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const productStore = useProductStore()
const { currentProduct } = storeToRefs(productStore)
const t = productStore.t

const product = computed(() => currentProduct.value)
const vendorBadges = computed(() => {
  const badges = product.value?.vendor_badges
  return Array.isArray(badges) ? badges : []
})

const showRFQDialog = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')

const handleRFQSubmitted = () => {
  showSuccess.value = true
  showRFQDialog.value = false
  showError.value = false
}

const handleRFQError = (message: string) => {
  errorMessage.value = message || 'خطا در ارسال درخواست. لطفاً دوباره تلاش کنید.'
  showError.value = true
}

const getCategoryId = (product: any): number | null => {
  if (!product) return null
  const category = product.primary_category
  if (!category) return null
  // Handle both object and ID cases
  return typeof category === 'object' ? category.id : category
}

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('products'), to: '/products' },
  { title: product.value?.name ?? '', disabled: true }
])

const formatPrice = (value: number | string) => {
  const amount = Number(value)
  if (Number.isNaN(amount)) {
    return value
  }
  return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان'
}

const setPrimary = (imageUrl: string) => {
  if (product.value) {
    product.value.primary_image = imageUrl
  }
}

const fetchPage = async () => {
  try {
    const product = await productStore.fetchProductBySlug(slug.value)
    return product
  } catch (error: any) {
    // Check if it's a 404 error (product not found or inactive)
    const statusCode = error?.statusCode || error?.status || error?.response?.status
    if (statusCode === 404) {
      // Create a proper 404 error that will be handled by Nuxt
      // Inactive products are correctly filtered by the backend and should return 404
      throw createError({
        statusCode: 404,
        message: 'محصول مورد نظر یافت نشد یا غیرفعال است.'
      })
    }
    // For other errors, log and re-throw
    console.error('Error loading product detail:', error)
    throw error
  }
}

await useAsyncData(`product-detail-${slug.value}`, fetchPage, {
  server: true,
  default: () => null
})

watch(
  () => route.params.slug,
  async (next, prev) => {
    if (next !== prev) {
      await fetchPage()
    }
  }
)

const config = useRuntimeConfig()
const baseUrl = config.public.siteUrl || (process.client ? window.location.origin : 'https://indexo.ir')

// Product URL for sharing
const productUrl = computed(() => {
  if (!product.value) return ''
  if (product.value.canonical_url) {
    return product.value.canonical_url
  }
  return `${baseUrl}/products/${product.value.slug}`
})

// Generate schemas
const productSchema = computed(() => {
  if (!product.value) return null
  return generateProductSchema(product.value, baseUrl)
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
  if (!product.value) return ''
  if (product.value.canonical_url) {
    return product.value.canonical_url
  }
  return `${baseUrl}/products/${product.value.slug}`
})

// Get OG image (primary image)
const ogImage = computed(() => {
  return product.value?.og_image_url || product.value?.primary_image || ''
})

// SEO Meta Tags
useSeoMeta({
  title: () => product.value?.meta_title ?? product.value?.name ?? 'محصول',
  description: () => product.value?.meta_description ?? product.value?.short_description ?? '',
  ogTitle: () => product.value?.meta_title ?? product.value?.name ?? '',
  ogDescription: () => product.value?.meta_description ?? product.value?.short_description ?? '',
  ogType: 'product',
  ogImage: () => ogImage.value,
  twitterCard: 'summary_large_image',
  twitterTitle: () => product.value?.meta_title ?? product.value?.name ?? '',
  twitterDescription: () => product.value?.meta_description ?? product.value?.short_description ?? '',
  twitterImage: () => ogImage.value
})

// Schema markup and canonical URL
useHead(() => {
  const schemas: any[] = []
  
  if (productSchema.value) {
    schemas.push(productSchema.value)
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
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.9), rgba(var(--v-theme-secondary), 0.9));
  color: rgb(var(--v-theme-on-primary));
}

.product-detail .no-image {
  height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--v-theme-on-surface), 0.06);
  border-radius: 12px;
}

.max-w-720 {
  max-width: 720px;
}

.price-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* Typography improvements */
.readable-heading {
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: rgba(var(--v-theme-on-surface), 0.96);
}

.readable-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.meta-text {
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.72);
  font-size: 0.875rem;
}

/* Content body styling */
.content-body {
  max-width: 100%;
  line-height: 1.8;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
}

.product-detail .content-body :deep(img) {
  max-width: 100%;
  border-radius: 16px;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.1);
}

.product-detail .content-body :deep(h1),
.product-detail .content-body :deep(h2),
.product-detail .content-body :deep(h3),
.product-detail .content-body :deep(h4),
.product-detail .content-body :deep(h5),
.product-detail .content-body :deep(h6) {
  font-weight: 700;
  line-height: 1.3;
  color: rgba(var(--v-theme-on-surface), 0.96);
  margin-bottom: 0;
}

/* Medium.com-inspired heading spacing */
.product-detail .content-body :deep(h1) {
  font-size: 2.5rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
}

.product-detail .content-body :deep(h1:first-child) {
  margin-top: 0;
}

.product-detail .content-body :deep(h2) {
  font-size: 2rem;
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
}

.product-detail .content-body :deep(h3) {
  font-size: 1.75rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.product-detail .content-body :deep(h4) {
  font-size: 1.5rem;
  margin-top: 1.75rem;
  margin-bottom: 0.875rem;
}

.product-detail .content-body :deep(h5) {
  font-size: 1.25rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.product-detail .content-body :deep(h6) {
  font-size: 1.125rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

/* Medium.com-inspired paragraph spacing */
.product-detail .content-body :deep(p) {
  line-height: 1.8;
  margin-top: 0;
  margin-bottom: 1.75rem;
  color: rgba(var(--v-theme-on-surface), 0.87);
  font-size: 1.05rem;
  text-align: justify;
  max-width: 65ch;
}

/* First paragraph after heading has less top margin */
.product-detail .content-body :deep(h1 + p),
.product-detail .content-body :deep(h2 + p),
.product-detail .content-body :deep(h3 + p),
.product-detail .content-body :deep(h4 + p),
.product-detail .content-body :deep(h5 + p),
.product-detail .content-body :deep(h6 + p) {
  margin-top: 0.5rem;
}

.product-detail .content-body :deep(ul),
.product-detail .content-body :deep(ol) {
  margin-top: 1.5rem;
  margin-bottom: 1.75rem;
  padding-right: 2rem;
  line-height: 1.8;
}

.product-detail .content-body :deep(li) {
  margin-bottom: 0.875rem;
  line-height: 1.8;
}

.product-detail .content-body :deep(li:last-child) {
  margin-bottom: 0;
}

.product-detail .content-body :deep(blockquote) {
  border-right: 4px solid rgba(var(--v-theme-primary), 0.5);
  padding-right: 1.5rem;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), 0.75);
  line-height: 1.8;
}

.product-detail .content-body :deep(blockquote p) {
  margin-bottom: 1rem;
}

.product-detail .content-body :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

.product-detail .content-body :deep(a) {
  color: rgb(var(--v-theme-primary));
  text-decoration: underline;
  transition: opacity 0.2s ease;
}

.product-detail .content-body :deep(a:hover) {
  opacity: 0.8;
}

.product-detail .content-body :deep(code) {
  background-color: rgba(var(--v-theme-on-surface), 0.08);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Courier New', monospace;
}

.product-detail .content-body :deep(pre) {
  background-color: rgba(var(--v-theme-on-surface), 0.05);
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
}

.product-detail .content-body :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

/* Table styling */
.product-detail .content-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
  border: 1px solid #e0e0e0;
}

.product-detail .content-body :deep(table th),
.product-detail .content-body :deep(table td) {
  padding: 0.75em;
  border: 1px solid #e0e0e0;
  text-align: right;
}

.product-detail .content-body :deep(table th) {
  background-color: #f5f7fa;
  font-weight: 700;
  color: rgba(var(--v-theme-on-surface), 0.96);
}
</style>

