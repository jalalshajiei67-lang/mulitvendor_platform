<!-- src/views/ProductList.vue - Vuetify Material Design 3 -->
<template>
  <v-container fluid class="product-list-container">
    <!-- Breadcrumbs -->
    <v-breadcrumbs
      :items="breadcrumbItems"
      class="px-4 py-2"
      divider="/"
    >
      <template v-slot:prepend>
        <v-icon size="small">mdi-home</v-icon>
      </template>
    </v-breadcrumbs>

    <!-- Header Section -->
    <v-row class="mb-4 mb-md-6" align="center">
      <v-col cols="12" md="6">
        <h1 class="text-h4 text-sm-h3 font-weight-bold">
          {{ isMyProducts ? t('myProducts') : t('products') }}
        </h1>
      </v-col>
      <v-col cols="12" md="6" class="d-flex justify-end justify-sm-end">
        <v-btn
          v-if="isMyProducts || (authStore.isAuthenticated && authStore.isSeller)"
          color="primary"
          :size="display.xs.value ? 'large' : 'large'"
          prepend-icon="mdi-plus"
          to="/products/new"
          variant="elevated"
          rounded="lg"
          :block="display.xs.value"
        >
          {{ t('addNewProduct') }}
        </v-btn>
      </v-col>
    </v-row>

    <!-- Filters Section -->
    <v-card v-if="!isMyProducts" elevation="2" rounded="lg" class="mb-4 mb-md-6">
      <v-card-text class="pa-3 pa-md-4">
        <v-row dense>
          <v-col cols="12" sm="6" md="4">
            <v-select
              v-model="selectedCategory"
              :items="categories"
              item-title="name"
              item-value="id"
              :label="t('allCategories')"
              prepend-inner-icon="mdi-filter"
              variant="outlined"
              clearable
              rounded="lg"
              @update:model-value="filterProducts"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="searchQuery"
              :label="t('searchProducts')"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              clearable
              rounded="lg"
              @update:model-value="filterProducts"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="12" md="4">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              item-title="text"
              item-value="value"
              :label="t('sortBy') || 'مرتب‌سازی'"
              prepend-inner-icon="mdi-sort"
              variant="outlined"
              rounded="lg"
              @update:model-value="filterProducts"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <v-row v-if="loading" justify="center" class="my-16">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <p class="text-h6 mt-4">{{ t('loadingProducts') }}</p>
      </v-col>
    </v-row>

    <!-- Error State -->
    <v-alert
      v-else-if="error"
      type="error"
      variant="tonal"
      prominent
      class="my-4"
    >
      <v-row align="center">
        <v-col>
          <div class="text-h6">{{ error }}</div>
          <v-btn
            color="error"
            variant="text"
            prepend-icon="mdi-refresh"
            @click="filterProducts"
            class="mt-2"
          >
            {{ t('tryAgain') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Products Grid -->
    <v-row v-else-if="products.length > 0" class="product-grid">
      <v-col
        v-for="product in products"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card
          elevation="4"
          rounded="lg"
          hover
          class="product-card h-100"
          @click="goToProductDetail(product.id)"
        >
          <!-- Product Image -->
          <v-img
            :src="getProductImage(product)"
            :height="display.xs.value ? 200 : 250"
            cover
            class="cursor-pointer"
          >
            <template v-slot:placeholder>
              <v-row
                class="fill-height ma-0"
                align="center"
                justify="center"
              >
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </v-row>
            </template>

            <!-- Badge if product is inactive -->
            <div v-if="!product.is_active" class="product-badge">
              <v-chip
                color="error"
                size="small"
                variant="elevated"
              >
                غیرفعال
              </v-chip>
            </div>
          </v-img>

          <v-card-text class="pa-3 pa-sm-4 pb-2">
            <!-- Product Name -->
            <h3 class="text-subtitle-1 text-sm-h6 font-weight-bold mb-2 text-truncate">
              {{ product.name }}
            </h3>

            <!-- Category -->
            <v-chip
              color="primary"
              size="small"
              variant="tonal"
              class="mb-2"
            >
              {{ product.category_name }}
            </v-chip>

            <!-- Price and Stock -->
            <div class="d-flex justify-space-between align-center mt-2 mt-sm-3">
              <div class="text-h6 text-sm-h5 font-weight-bold text-primary">
                ${{ product.price }}
              </div>
              <div class="text-caption text-sm-body-2 text-medium-emphasis">
                <v-icon size="small" class="ml-1">mdi-package-variant</v-icon>
                {{ product.stock }}
              </div>
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <!-- Action Buttons -->
          <v-card-actions class="px-3 px-sm-4 py-2 py-sm-3">
            <v-btn
              color="primary"
              variant="text"
              prepend-icon="mdi-eye"
              :size="display.xs.value ? 'x-small' : 'small'"
              @click.stop="goToProductDetail(product.id)"
            >
              {{ t('view') }}
            </v-btn>

            <v-spacer></v-spacer>

            <v-btn
              v-if="isOwner(product)"
              color="warning"
              variant="text"
              icon="mdi-pencil"
              :size="display.xs.value ? 'x-small' : 'small'"
              @click.stop="$router.push(`/products/${product.id}/edit`)"
            ></v-btn>

            <v-btn
              v-if="isOwner(product)"
              color="error"
              variant="text"
              icon="mdi-delete"
              :size="display.xs.value ? 'x-small' : 'small'"
              @click.stop="confirmDelete(product)"
            ></v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <v-row v-else justify="center" class="my-8 my-md-16">
      <v-col cols="12" class="text-center px-4">
        <v-icon :size="display.xs.value ? 80 : 120" color="grey-lighten-2">mdi-package-variant-closed</v-icon>
        <h3 class="text-h6 text-sm-h5 font-weight-bold mt-3 mt-sm-4">{{ t('noProductsFound') }}</h3>
        <p class="text-body-2 text-sm-body-1 text-medium-emphasis mt-2">{{ t('noProductsAvailable') }}</p>
        <v-btn
          v-if="authStore.isAuthenticated && authStore.isSeller"
          color="primary"
          size="large"
          prepend-icon="mdi-plus"
          to="/products/new"
          variant="elevated"
          rounded="lg"
          class="mt-4"
          :block="display.xs.value"
        >
          {{ t('addNewProduct') }}
        </v-btn>
      </v-col>
    </v-row>

    <!-- Pagination -->
    <v-row v-if="!isMyProducts && pagination.count > 0" justify="center" class="mt-6 mt-md-8">
      <v-col cols="12" class="d-flex justify-center align-center flex-wrap ga-2">
        <v-btn
          :disabled="!pagination.previous"
          color="primary"
          variant="elevated"
          prepend-icon="mdi-chevron-right"
          @click="previousPage"
          :size="display.xs.value ? 'small' : 'default'"
          rounded="lg"
        >
          {{ display.xs.value ? '' : t('previous') }}
        </v-btn>

        <v-chip
          color="primary"
          variant="elevated"
          :size="display.xs.value ? 'default' : 'large'"
          class="font-weight-bold mx-1 mx-sm-2"
        >
          {{ t('page') }} {{ currentPage }} {{ t('of') }} {{ totalPages }}
        </v-chip>

        <v-btn
          :disabled="!pagination.next"
          color="primary"
          variant="elevated"
          append-icon="mdi-chevron-left"
          @click="nextPage"
          :size="display.xs.value ? 'small' : 'default'"
          rounded="lg"
        >
          {{ display.xs.value ? '' : t('next') }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useProductStore } from '@/stores/modules/productStore'
import { useAuthStore } from '@/stores/auth'
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'

export default {
  name: 'ProductList',
  setup() {
    const productStore = useProductStore()
    const authStore = useAuthStore()
    const route = useRoute()
    const router = useRouter()
    const display = useDisplay()

    const selectedCategory = ref('')
    const searchQuery = ref(route.query.search || '')
    const sortBy = ref('-created_at')
    const currentPage = ref(1)

    const isMyProducts = computed(() => route.meta?.showOnlyMyProducts)

    const breadcrumbItems = computed(() => {
      if (isMyProducts.value) {
        return [
          { title: t.value('home'), to: '/', disabled: false },
          { title: t.value('myProducts'), disabled: true }
        ]
      }
      return [
        { title: t.value('home'), to: '/', disabled: false },
        { title: t.value('products'), disabled: true }
      ]
    })

    const sortOptions = computed(() => [
      { text: t.value('newestFirst'), value: '-created_at' },
      { text: t.value('oldestFirst'), value: 'created_at' },
      { text: t.value('priceLowToHigh'), value: 'price' },
      { text: t.value('priceHighToLow'), value: '-price' },
      { text: t.value('nameAToZ'), value: 'name' },
      { text: t.value('nameZToA'), value: '-name' }
    ])

    const products = computed(() => productStore.products)
    const categories = computed(() => productStore.categories)
    const loading = computed(() => productStore.loading)
    const error = computed(() => productStore.error)
    const pagination = computed(() => productStore.pagination)

    const totalPages = computed(() => {
      return Math.ceil(pagination.value.count / 10)
    })

    const isOwner = (product) => {
      return authStore.isAuthenticated && authStore.user.id === product.vendor
    }

    const getProductImage = (product) => {
      if (product.primary_image) {
        return product.primary_image
      }

      if (product.images && product.images.length > 0) {
        return product.images[0].image
      }

      return product.image || 'https://via.placeholder.com/250x250?text=No+Image'
    }

    const filterProducts = () => {
      if (isMyProducts.value) {
        productStore.fetchMyProducts()
      } else {
        const params = {
          page: currentPage.value,
          ordering: sortBy.value,
        }

        if (selectedCategory.value) {
          params.category = selectedCategory.value
        }

        if (searchQuery.value) {
          params.search = searchQuery.value
        }

        productStore.fetchProducts(params)
      }
    }

    const nextPage = () => {
      if (pagination.value.next) {
        currentPage.value++
        filterProducts()
      }
    }

    const previousPage = () => {
      if (pagination.value.previous) {
        currentPage.value--
        filterProducts()
      }
    }

    const confirmDelete = (product) => {
      if (confirm(t.value('confirmDelete') + ` "${product.name}"?`)) {
        productStore.deleteProduct(product.id)
      }
    }

    const goToProductDetail = (productId) => {
      router.push(`/products/${productId}`)
    }

    // Watch for route query changes to update search
    watch(() => route.query.search, (newSearch) => {
      if (newSearch !== undefined) {
        searchQuery.value = newSearch || ''
        currentPage.value = 1
        filterProducts()
      }
    })

    onMounted(() => {
      console.log('ProductList mounted, fetching data...')
      productStore.fetchCategories()
      filterProducts()
    })

    const t = computed(() => productStore.t)

    return {
      products,
      categories,
      loading,
      error,
      pagination,
      selectedCategory,
      searchQuery,
      sortBy,
      sortOptions,
      currentPage,
      totalPages,
      isMyProducts,
      breadcrumbItems,
      authStore,
      display,
      isOwner,
      getProductImage,
      filterProducts,
      nextPage,
      previousPage,
      confirmDelete,
      goToProductDetail,
      t,
    }
  },
}
</script>

<style scoped>
.product-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

/* Reduce hover effect on mobile for better touch experience */
@media (max-width: 600px) {
  .product-card:hover {
    transform: translateY(-4px);
  }
}

.cursor-pointer {
  cursor: pointer;
}

.product-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 1;
}

.h-100 {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Ensure card content takes up available space */
.product-card :deep(.v-card-text) {
  flex: 1;
}

/* Responsive grid spacing */
.product-grid {
  margin: -8px;
}

.product-grid > .v-col {
  padding: 8px;
}

@media (min-width: 600px) {
  .product-grid {
    margin: -12px;
  }
  
  .product-grid > .v-col {
    padding: 12px;
  }
}

/* Container width improvements for better desktop experience */
.product-list-container {
  max-width: 100%;
  padding-left: 16px;
  padding-right: 16px;
}

/* Better container constraints for different screen sizes */
@media (min-width: 960px) {
  .product-list-container {
    max-width: 100%;
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (min-width: 1280px) {
  .product-list-container {
    max-width: 1600px;
    margin: 0 auto;
    padding-left: 32px;
    padding-right: 32px;
  }
}

@media (min-width: 1920px) {
  .product-list-container {
    max-width: 1800px;
    margin: 0 auto;
    padding-left: 40px;
    padding-right: 40px;
  }
}
</style>
