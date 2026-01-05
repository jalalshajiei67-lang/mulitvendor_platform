<template>
  <div v-if="product" class="product-detail">
    <section class="hero">
      <v-container class="py-8">
        <h1 class="product-title-hero font-weight-bold text-white mb-3">
          {{ product.name }}
        </h1>
        <p class="product-description-hero text-white opacity-85 max-w-720">
          {{ product.short_description }}
        </p>
      </v-container>
    </section>

    <v-container class="breadcrumbs-container">
      <v-breadcrumbs
        :items="breadcrumbs"
        class="pa-0"
        density="comfortable"
      >
        <template #divider>
          <v-icon>mdi-chevron-left</v-icon>
        </template>
      </v-breadcrumbs>
    </v-container>

    <v-container class="py-8">
      <v-row>
        <v-col cols="12" md="6">
          <v-sheet elevation="3" rounded="xl" class="pa-4">
            <div v-if="primaryImageUrl" class="image-container" style="position: relative; min-height: 420px; width: 100%;">
              <!-- Skeleton Loader -->
              <div v-if="!primaryImageLoaded && !primaryImageError" class="skeleton-overlay" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; z-index: 2;">
                <v-skeleton-loader type="image" width="100%" height="420" class="rounded-lg" />
              </div>
              <!-- Actual Image -->
              <img
                :key="`primary-${product.id}-${primaryImageUrl}`"
                :src="primaryImageUrl"
                :alt="product.name"
                class="rounded-lg"
                style="width: 100%; height: 420px; object-fit: cover; position: relative; z-index: 1;"
                @error="handlePrimaryImageError"
                @load="handlePrimaryImageLoad"
              />
              <!-- Error State -->
              <div v-if="primaryImageError" class="d-flex align-center justify-center no-image" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; z-index: 3; background: white;">
                <v-icon size="64" color="grey-lighten-1">mdi-image-broken</v-icon>
              </div>
            </div>
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
                  :src="image.image_url || image.image"
                  :alt="product.name"
                  height="80"
                  width="120"
                  cover
                  class="rounded-lg mx-2"
                  loading="lazy"
                  @click="setPrimary(image.image_url || image.image)"
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
            <h2 class="section-heading-sm font-weight-bold mb-4">
              {{ t('keySpecifications') }}
            </h2>
            <div v-if="product.availability_status || product.condition || product.origin || product.sku || product.stock || product.minimum_order_quantity || product.country_of_origin || product.lead_time_days">
              <div class="d-flex flex-column gap-3">
                <!-- Availability Status -->
                <div v-if="product.availability_status" class="d-flex align-center gap-2">
                  <v-icon color="primary">mdi-package-variant-closed</v-icon>
                  <span class="font-weight-medium">وضعیت موجودی:</span>
                  <v-chip 
                    size="small" 
                    :color="product.availability_status === 'in_stock' ? 'success' : 'warning'"
                    variant="tonal"
                  >
                    {{ product.availability_status === 'in_stock' ? 'موجود در انبار' : 'سفارشی' }}
                  </v-chip>
                </div>

                <!-- Condition (if in stock) -->
                <div v-if="product.availability_status === 'in_stock' && product.condition" class="d-flex align-center gap-2">
                  <v-icon color="info">mdi-check-circle</v-icon>
                  <span class="font-weight-medium">وضعیت:</span>
                  <v-chip 
                    size="small" 
                    :color="product.condition === 'new' ? 'success' : 'default'"
                    variant="tonal"
                  >
                    {{ product.condition === 'new' ? 'نو' : 'دست دوم' }}
                  </v-chip>
                </div>

                <!-- Lead Time (if made to order) -->
                <div v-if="product.availability_status === 'made_to_order' && product.lead_time_days" class="d-flex align-center gap-2">
                  <v-icon color="warning">mdi-calendar-clock</v-icon>
                  <span class="font-weight-medium">زمان تحویل:</span>
                  <v-chip size="small" color="warning" variant="tonal">
                    {{ product.lead_time_days }} روز کاری
                  </v-chip>
                </div>

                <!-- Origin -->
                <div v-if="product.origin" class="d-flex align-center gap-2">
                  <v-icon color="secondary">mdi-earth</v-icon>
                  <span class="font-weight-medium">مبدا:</span>
                  <v-chip size="small" color="secondary" variant="tonal">
                    {{ product.origin === 'iran' ? 'ساخت ایران' : 'وارداتی' }}
                  </v-chip>
                </div>

                <!-- SKU -->
                <div v-if="product.sku" class="d-flex align-center gap-2">
                  <v-icon color="primary">mdi-barcode</v-icon>
                  <span class="font-weight-medium">{{ t('sku') }}:</span>
                  <v-chip size="small" color="primary" variant="tonal">
                    {{ product.sku }}
                  </v-chip>
                </div>

                <!-- Stock -->
                <div v-if="product.stock" class="d-flex align-center gap-2">
                  <v-icon color="info">mdi-warehouse</v-icon>
                  <span class="font-weight-medium">{{ t('stockStatus') }}:</span>
                  <v-chip size="small" color="info" variant="tonal">
                    {{ product.stock }}
                  </v-chip>
                </div>

                <!-- Minimum Order Quantity -->
                <div v-if="product.minimum_order_quantity" class="d-flex align-center gap-2">
                  <v-icon color="warning">mdi-cart-arrow-down</v-icon>
                  <span class="font-weight-medium">{{ t('minimumOrder') }}:</span>
                  <v-chip size="small" color="warning" variant="tonal">
                    {{ product.minimum_order_quantity }}
                  </v-chip>
                </div>

                <!-- Country of Origin -->
                <div v-if="product.country_of_origin" class="d-flex align-center gap-2">
                  <v-icon color="secondary">mdi-flag</v-icon>
                  <span class="font-weight-medium">{{ t('originCountry') }}:</span>
                  <v-chip size="small" color="secondary" variant="tonal">
                    {{ product.country_of_origin }}
                  </v-chip>
                </div>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-8">
        <v-col cols="12" md="8">
          <v-card elevation="1" rounded="xl" class="pa-6">
            <h2 class="section-heading font-weight-bold mb-4 readable-heading">توضیحات محصول</h2>
            
            <!-- Key Features Table -->
            <div v-if="product.features && product.features.length > 0" class="mb-6">
              <h3 class="subsection-heading font-weight-bold mb-3">ویژگی‌های کلیدی</h3>
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
            <h2 class="section-heading-sm font-weight-bold mb-4">{{ t('relatedProducts') }}</h2>
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

  <ProductDetailSkeleton v-else-if="pending || !product" />

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
import { formatImageUrl } from '~/utils/imageUtils'

definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const productStore = useProductStore()
const { currentProduct } = storeToRefs(productStore)
const t = productStore.t

const showRFQDialog = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const primaryImageLoaded = ref(false)
const primaryImageError = ref(false)

const fetchPage = async () => {
  try {
    primaryImageLoaded.value = false
    primaryImageError.value = false
    const product = await productStore.fetchProductBySlug(slug.value)
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'products/[slug].vue:fetchPage',message:'Product fetched',data:{productId:product?.id,hasPrimaryImage:!!product?.primary_image,primaryImageType:typeof product?.primary_image,primaryImageLength:product?.primary_image?.length,imagesCount:product?.images?.length},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
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

const { data: productData, pending, error: asyncError } = await useAsyncData(`product-detail-${slug.value}`, fetchPage, {
  server: true,
  default: () => null
})

// Use product from store, but fallback to useAsyncData result if store is not set yet
const product = computed(() => currentProduct.value || productData.value)
const vendorBadges = computed(() => {
  const badges = product.value?.vendor_badges
  return Array.isArray(badges) ? badges : []
})

const primaryImageUrl = computed(() => {
  if (!product.value?.primary_image) return null
  const formatted = formatImageUrl(product.value.primary_image)
  // #region agent log
  fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'products/[slug].vue:primaryImageUrl',message:'Primary image URL computed',data:{original:product.value.primary_image,formatted,productId:product.value?.id},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
  // #endregion
  // Reset loading state when URL changes
  if (formatted) {
    primaryImageLoaded.value = false
    primaryImageError.value = false
  }
  return formatted
})

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
  // #region agent log
  fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'products/[slug].vue:setPrimary',message:'setPrimary called',data:{imageUrl,productId:product.value?.id},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
  // #endregion
  if (product.value) {
    primaryImageLoaded.value = false
    primaryImageError.value = false
    product.value.primary_image = imageUrl
  }
}

const handlePrimaryImageError = (event: Event) => {
  const imgElement = event.target as HTMLImageElement
  const imageSrc = imgElement?.src
  primaryImageError.value = true
  primaryImageLoaded.value = false
  // #region agent log
  fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'products/[slug].vue:handlePrimaryImageError',message:'Primary image error',data:{imageSrc,productId:product.value?.id,productName:product.value?.name,currentPrimaryImage:product.value?.primary_image},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
  // #endregion
  console.error('Primary image failed to load:', imageSrc)
  // Try to fallback to first thumbnail if available
  if (product.value?.images?.length > 0) {
    const firstImage = product.value.images[0]
    const fallbackUrl = firstImage?.image_url || firstImage?.image
    if (fallbackUrl && fallbackUrl !== product.value.primary_image) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'products/[slug].vue:handlePrimaryImageError',message:'Primary image fallback',data:{fallbackUrl,originalUrl:product.value.primary_image},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
      // #endregion
      product.value.primary_image = fallbackUrl
      primaryImageError.value = false
    }
  }
}

const handlePrimaryImageLoad = (event: Event) => {
  const imgElement = event.target as HTMLImageElement
  const imageSrc = imgElement?.src
  primaryImageLoaded.value = true
  primaryImageError.value = false
  // #region agent log
  fetch('http://127.0.0.1:7242/ingest/62116b0f-d571-42f7-a49f-52eb30bf1f17',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'products/[slug].vue:handlePrimaryImageLoad',message:'Primary image loaded',data:{imageSrc,productId:product.value?.id,expectedSrc:product.value?.primary_image,imageComplete:imgElement?.complete,imageNaturalWidth:imgElement?.naturalWidth,imageNaturalHeight:imgElement?.naturalHeight},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
  // #endregion
}

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
/* Shared container width matching v-container */
.hero,
.breadcrumbs-container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 600px) {
  .hero,
  .breadcrumbs-container {
    max-width: 600px;
  }
}

@media (min-width: 960px) {
  .hero,
  .breadcrumbs-container {
    max-width: 960px;
  }
}

@media (min-width: 1280px) {
  .hero,
  .breadcrumbs-container {
    max-width: 1200px;
  }
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.9), rgba(var(--v-theme-secondary), 0.9));
  color: rgb(var(--v-theme-on-primary));
  border-radius: 24px;
  margin-top: 16px;
  margin-bottom: 36px;
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

.breadcrumbs-container {
  margin-top: -24px;
  margin-bottom: 16px;
  padding: 0 16px;
  position: relative;
  z-index: 1;
}

/* Typography optimized for users over 40 */
.product-title-hero {
  font-size: 1.5rem; /* 24px - reduced from ~48-60px */
  line-height: 1.5;
  letter-spacing: -0.01em;
}

@media (min-width: 600px) {
  .product-title-hero {
    font-size: 1.75rem; /* 28px */
  }
}

@media (min-width: 960px) {
  .product-title-hero {
    font-size: 2rem; /* 32px - much more reasonable than 60px */
    line-height: 1.4;
  }
}

.product-description-hero {
  font-size: 1.0625rem; /* 17px base - increased from 16px */
  line-height: 1.7;
  letter-spacing: 0.01em;
}

@media (min-width: 600px) {
  .product-description-hero {
    font-size: 1.125rem; /* 18px - increased from 17px */
  }
}

@media (min-width: 960px) {
  .product-description-hero {
    font-size: 1.1875rem; /* 19px - increased from 18px */
    line-height: 1.75;
  }
}

.section-heading {
  font-size: 1.375rem; /* 22px */
  line-height: 1.5;
  letter-spacing: -0.01em;
}

@media (min-width: 600px) {
  .section-heading {
    font-size: 1.5rem; /* 24px */
  }
}

@media (min-width: 960px) {
  .section-heading {
    font-size: 1.625rem; /* 26px */
  }
}

.section-heading-sm {
  font-size: 1.125rem; /* 18px */
  line-height: 1.5;
  letter-spacing: 0;
}

@media (min-width: 600px) {
  .section-heading-sm {
    font-size: 1.25rem; /* 20px */
  }
}

.subsection-heading {
  font-size: 1.125rem; /* 18px */
  line-height: 1.5;
  letter-spacing: 0;
}

@media (min-width: 600px) {
  .subsection-heading {
    font-size: 1.25rem; /* 20px */
  }
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

/* Typography improvements - optimized for users over 40 */
.readable-heading {
  line-height: 1.5; /* Improved from 1.4 for better readability */
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
  font-size: 0.9375rem; /* 15px - slightly larger from 0.875rem/14px for better readability */
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

/* Heading spacing optimized for users over 40 - reduced sizes */
.product-detail .content-body :deep(h1) {
  font-size: 1.75rem; /* 28px - reduced from 2.5rem/40px */
  line-height: 1.5;
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
}

.product-detail .content-body :deep(h1:first-child) {
  margin-top: 0;
}

.product-detail .content-body :deep(h2) {
  font-size: 1.5rem; /* 24px - reduced from 2rem/32px */
  line-height: 1.5;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.product-detail .content-body :deep(h3) {
  font-size: 1.375rem; /* 22px - reduced from 1.75rem/28px */
  line-height: 1.5;
  margin-top: 1.75rem;
  margin-bottom: 0.875rem;
}

.product-detail .content-body :deep(h4) {
  font-size: 1.25rem; /* 20px - reduced from 1.5rem/24px */
  line-height: 1.5;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.product-detail .content-body :deep(h5) {
  font-size: 1.125rem; /* 18px - reduced from 1.25rem/20px */
  line-height: 1.5;
  margin-top: 1.25rem;
  margin-bottom: 0.625rem;
}

.product-detail .content-body :deep(h6) {
  font-size: 1.0625rem; /* 17px - reduced from 1.125rem/18px */
  line-height: 1.5;
  margin-top: 1.25rem;
  margin-bottom: 0.625rem;
}

/* Paragraph spacing optimized for readability */
.product-detail .content-body :deep(p) {
  line-height: 1.8;
  margin-top: 0;
  margin-bottom: 1.75rem;
  color: rgba(var(--v-theme-on-surface), 0.87);
  font-size: 1.125rem; /* 18px - increased from 17px for better readability */
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

