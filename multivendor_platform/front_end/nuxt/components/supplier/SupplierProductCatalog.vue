<template>
  <div class="supplier-product-catalog" dir="rtl">
    <v-container>
      <!-- Header with Search and Sort -->
      <div class="catalog-header mb-6">
        <v-row align="center">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchQuery"
              label="جستجوی محصولات"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              clearable
              density="comfortable"
              hide-details
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              label="مرتب‌سازی"
              prepend-inner-icon="mdi-sort"
              variant="outlined"
              density="comfortable"
              hide-details
            ></v-select>
          </v-col>
        </v-row>
      </div>

      <!-- Loading State -->
      <v-row v-if="loading" justify="center" class="my-8">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-row>

      <!-- Products Grid -->
      <v-row v-else-if="filteredProducts.length > 0" class="product-grid">
        <v-col
          v-for="product in filteredProducts"
          :key="product.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="product-card"
            elevation="4"
            hover
            @click="navigateTo(`/products/${product.slug || product.id}`)"
          >
            <v-img
              :src="getProductImage(product)"
              :height="display.xs.value ? 200 : 250"
              cover
            >
              <template v-slot:placeholder>
                <v-skeleton-loader type="image" />
              </template>
              
              <!-- Featured Badge -->
              <v-chip
                v-if="product.is_featured"
                color="amber"
                size="small"
                class="product-badge"
              >
                ویژه
              </v-chip>
              
              <!-- Stock Status -->
              <v-chip
                v-if="product.stock <= 0"
                color="error"
                size="small"
                class="stock-badge"
              >
                ناموجود
              </v-chip>
            </v-img>

            <v-card-text class="pa-3">
              <h3 class="text-subtitle-1 font-weight-bold mb-1 line-clamp-2">
                {{ product.name }}
              </h3>
              
              <div class="price-section mt-2 mb-2">
                <span class="price text-h6 font-weight-bold text-primary">
                  {{ formatPrice(product.price) }}
                </span>
                <span class="currency text-caption text-medium-emphasis">تومان</span>
              </div>

              <div class="product-meta d-flex align-center justify-space-between">
                <div class="d-flex align-center">
                  <v-icon size="small" color="amber" class="me-1">mdi-star</v-icon>
                  <span class="text-caption">{{ product.rating || 0 }}</span>
                </div>
                <div class="text-caption text-medium-emphasis">
                  موجودی: {{ product.stock }}
                </div>
              </div>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions class="px-3 py-2">
              <v-btn
                color="primary"
                variant="text"
                size="small"
                @click.stop="navigateTo(`/products/${product.slug || product.id}`)"
              >
                مشاهده جزئیات
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                icon="mdi-cart-plus"
                variant="text"
                size="small"
                color="primary"
                :disabled="product.stock <= 0"
                @click.stop="$emit('add-to-cart', product)"
              ></v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Empty State -->
      <v-row v-else justify="center" class="my-8">
        <v-col cols="12" class="text-center">
          <v-icon size="80" color="grey-lighten-2">mdi-package-variant-closed</v-icon>
          <h3 class="text-h6 mt-3">محصولی یافت نشد</h3>
          <p class="text-body-2 text-medium-emphasis">
            {{ searchQuery ? 'نتیجه‌ای برای جستجوی شما یافت نشد' : 'هنوز محصولی ثبت نشده است' }}
          </p>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'
import { formatImageUrl } from '~/utils/imageUtils'

interface Product {
  id: number
  name: string
  slug?: string
  price: number
  stock: number
  image?: string
  images?: any[]
  rating?: number
  is_featured?: boolean
}

interface Props {
  products: Product[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

defineEmits(['add-to-cart'])

const display = useDisplay()
const searchQuery = ref('')
const sortBy = ref('default')

const sortOptions = [
  { title: 'پیش‌فرض', value: 'default' },
  { title: 'جدیدترین', value: 'newest' },
  { title: 'ارزان‌ترین', value: 'price_asc' },
  { title: 'گران‌ترین', value: 'price_desc' },
  { title: 'پرفروش‌ترین', value: 'popular' }
]

const filteredProducts = computed(() => {
  let filtered = [...props.products]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(product =>
      product.name.toLowerCase().includes(query)
    )
  }

  // Sort
  switch (sortBy.value) {
    case 'newest':
      filtered.sort((a, b) => b.id - a.id)
      break
    case 'price_asc':
      filtered.sort((a, b) => a.price - b.price)
      break
    case 'price_desc':
      filtered.sort((a, b) => b.price - a.price)
      break
    case 'popular':
      filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0))
      break
  }

  return filtered
})

const getProductImage = (product: Product) => {
  if (product.image) {
    return formatImageUrl(product.image)
  }
  if (product.images && product.images.length > 0) {
    return formatImageUrl(product.images[0].image || product.images[0])
  }
  return 'https://via.placeholder.com/250x250?text=No+Image'
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('fa-IR').format(price)
}
</script>

<style scoped>
.catalog-header {
  background-color: rgba(var(--v-theme-surface), 0.5);
  border-radius: 12px;
  padding: 1rem;
}

.product-grid {
  margin: -8px;
}

.product-grid > .v-col {
  padding: 8px;
}

.product-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15) !important;
}

.product-badge {
  position: absolute;
  top: 8px;
  right: 8px;
}

.stock-badge {
  position: absolute;
  top: 8px;
  left: 8px;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.price-section {
  display: flex;
  align-items: baseline;
  gap: 4px;
}
</style>

