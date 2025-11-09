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
          {{ product.title }}
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
              :alt="product.title"
              height="420"
              class="rounded-lg"
              cover
            />
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
                  :alt="product.title"
                  height="80"
                  width="120"
                  cover
                  class="rounded-lg mx-2"
                  @click="setPrimary(image.image)"
                />
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

            <v-btn block color="primary" size="large">
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
                    <v-img :src="item.primary_image" :alt="item.title" cover />
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-medium">
                  {{ item.title }}
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

const productStore = useProductStore()
const { currentProduct } = storeToRefs(productStore)
const t = productStore.t

const product = computed(() => currentProduct.value)

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('products'), to: '/products' },
  { title: product.value?.title ?? '', disabled: true }
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
  title: () => product.value?.meta_title ?? product.value?.title ?? 'محصول',
  description: () => product.value?.meta_description ?? product.value?.short_description ?? '',
  ogTitle: () => product.value?.meta_title ?? product.value?.title ?? '',
  ogDescription: () => product.value?.meta_description ?? product.value?.short_description ?? '',
  ogType: 'product',
  ogImage: () => product.value?.primary_image ?? ''
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, rgba(0, 197, 142, 0.9), rgba(0, 111, 82, 0.9));
  color: white;
}

.product-detail .no-image {
  height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
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

