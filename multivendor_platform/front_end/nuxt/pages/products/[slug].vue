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
            </div>

            <div class="price-wrapper mb-6">
              <div class="text-caption text-medium-emphasis">{{ t('price') }}</div>
              <div class="text-h4 font-weight-bold">
                {{ product.price ? formatPrice(product.price) : t('contactForPrice') }}
              </div>
            </div>

            <v-btn block color="primary" size="large" @click="showRFQDialog = true">
              {{ t('requestQuote') }}
            </v-btn>
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
            <h2 class="text-h5 font-weight-bold mb-4">{{ t('productDescription') }}</h2>
            <div class="text-body-1 text-medium-emphasis" v-html="product.description"></div>
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

definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const productStore = useProductStore()
const { currentProduct } = storeToRefs(productStore)
const t = productStore.t

const product = computed(() => currentProduct.value)

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
    await productStore.fetchProductBySlug(slug.value)
  } catch (error) {
    console.error('Error loading product detail:', error)
  }
}

await useAsyncData(`product-detail-${slug.value}`, fetchPage)

watch(
  () => route.params.slug,
  async (next, prev) => {
    if (next !== prev) {
      await fetchPage()
    }
  }
)

useSeoMeta({
  title: () => product.value?.meta_title ?? product.value?.name ?? 'محصول',
  description: () => product.value?.meta_description ?? product.value?.short_description ?? '',
  ogTitle: () => product.value?.meta_title ?? product.value?.name ?? '',
  ogDescription: () => product.value?.meta_description ?? product.value?.short_description ?? '',
  ogType: 'product',
  ogImage: () => product.value?.primary_image ?? ''
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
</style>

