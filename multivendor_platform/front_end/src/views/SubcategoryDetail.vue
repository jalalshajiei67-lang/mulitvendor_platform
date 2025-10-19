<!-- src/views/SubcategoryDetail.vue -->
<template>
  <div class="subcategory-detail" dir="rtl">
    <Breadcrumb :items="breadcrumbItems" />

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>در حال بارگذاری...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
      <button @click="fetchSubcategoryData" class="retry-btn">دوباره تلاش کنید</button>
    </div>

    <!-- Subcategory Content -->
    <div v-else-if="subcategory">
      <!-- Subcategory Header -->
      <div class="subcategory-header">
        <div class="subcategory-image">
          <img 
            v-if="subcategory.image" 
            :src="subcategory.image" 
            :alt="subcategory.name"
          />
          <div v-else class="placeholder-image">
            <i class="fas fa-layer-group"></i>
          </div>
        </div>
        <div class="subcategory-info">
          <h1>{{ subcategory.name }}</h1>
          <p v-if="subcategory.description" class="description">{{ subcategory.description }}</p>
        </div>
      </div>

      <!-- Products Section -->
      <div class="products-section">
        <h2>محصولات این زیردسته</h2>
        
        <!-- Search Box -->
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="جستجوی محصول..."
            @input="handleSearch"
          />
        </div>

        <!-- Products Grid -->
        <div v-if="paginatedProducts.length > 0" class="items-grid">
          <div 
            v-for="product in paginatedProducts" 
            :key="product.id" 
            class="item-card"
            @click="goToProductDetail(product.id)"
          >
            <div class="circular-image">
              <img 
                v-if="getProductImage(product)" 
                :src="getProductImage(product)" 
                :alt="product.name"
              />
              <div v-else class="placeholder-image">
                <i class="fas fa-box"></i>
              </div>
            </div>
            <h3 class="item-title">{{ product.name }}</h3>
            <p class="item-price">${{ product.price }}</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <i class="fas fa-box-open"></i>
          <h3>محصولی وجود ندارد</h3>
          <p>هیچ محصولی در این زیردسته وجود ندارد.</p>
        </div>

        <!-- Pagination -->
        <div class="pagination" v-if="totalPages > 1">
          <button 
            @click="previousPage" 
            :disabled="currentPage === 1" 
            class="btn btn-secondary"
          >
            قبلی
          </button>
          <span>صفحه {{ currentPage }} از {{ totalPages }}</span>
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages" 
            class="btn btn-secondary"
          >
            بعدی
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import Breadcrumb from '@/components/Breadcrumb.vue'

export default {
  name: 'SubcategoryDetail',
  components: {
    Breadcrumb
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const subcategory = ref(null)
    const products = ref([])
    const loading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const itemsPerPage = 12

    const breadcrumbItems = computed(() => {
      const items = [
        { text: 'خانه', to: '/' },
        { text: 'بخش‌ها', to: '/departments' }
      ]
      
      // Add department if available
      if (subcategory.value?.departments && subcategory.value.departments.length > 0) {
        const dept = subcategory.value.departments[0]
        items.push({ text: dept.name, to: `/departments/${dept.slug}` })
      }
      
      // Add category if available
      if (subcategory.value?.categories && subcategory.value.categories.length > 0) {
        const cat = subcategory.value.categories[0]
        items.push({ text: cat.name, to: `/categories/${cat.slug}` })
      }
      
      items.push({ text: subcategory.value?.name || 'زیردسته', to: `/subcategories/${route.params.slug}` })
      
      return items
    })

    const fetchSubcategoryData = async () => {
      loading.value = true
      error.value = null
      try {
        // Fetch subcategory by slug
        console.log('Fetching subcategory with slug:', route.params.slug)
        const subResponse = await api.getSubcategoryBySlug(route.params.slug)
        console.log('Subcategory response:', subResponse.data)
        
        // Handle paginated or array response
        let subcategoryData = null
        if (subResponse.data && subResponse.data.results && subResponse.data.results.length > 0) {
          // Paginated response
          subcategoryData = subResponse.data.results[0]
        } else if (subResponse.data && Array.isArray(subResponse.data) && subResponse.data.length > 0) {
          // Direct array response
          subcategoryData = subResponse.data[0]
        }
        
        if (subcategoryData) {
          subcategory.value = subcategoryData
          console.log('Subcategory found:', subcategory.value)
          
          // Fetch products filtered by subcategory ID using the correct parameter name
          console.log('Fetching products for subcategory ID:', subcategory.value.id)
          const prodResponse = await api.getProducts({ subcategories: subcategory.value.id })
          console.log('Products response:', prodResponse.data)
          
          // Handle paginated response
          let productsList = []
          if (prodResponse.data && prodResponse.data.results) {
            productsList = prodResponse.data.results
          } else if (Array.isArray(prodResponse.data)) {
            productsList = prodResponse.data
          }
          
          // Filter only active products
          products.value = productsList.filter(prod => prod.is_active)
          console.log('Active products found:', products.value.length, products.value)
        } else {
          error.value = 'زیردسته یافت نشد'
          console.log('No subcategory found in response')
        }
      } catch (err) {
        error.value = 'بارگذاری اطلاعات با خطا مواجه شد. لطفاً دوباره تلاش کنید.'
        console.error('Error fetching subcategory data:', err)
        console.error('Error details:', err.response?.data)
      } finally {
        loading.value = false
      }
    }

    const getProductImage = (product) => {
      if (product.primary_image) {
        return product.primary_image
      }
      if (product.images && product.images.length > 0) {
        return product.images[0].image_url || product.images[0].image
      }
      if (product.image) {
        return product.image
      }
      return null
    }

    const filteredProducts = computed(() => {
      if (!searchQuery.value) {
        return products.value
      }
      const query = searchQuery.value.toLowerCase()
      return products.value.filter(prod => 
        prod.name.toLowerCase().includes(query) ||
        (prod.description && prod.description.toLowerCase().includes(query))
      )
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredProducts.value.length / itemsPerPage)
    })

    const paginatedProducts = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return filteredProducts.value.slice(start, end)
    })

    const handleSearch = () => {
      currentPage.value = 1
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }

    const goToProductDetail = (id) => {
      router.push({ name: 'ProductDetail', params: { id } })
    }

    watch(() => route.params.slug, () => {
      if (route.name === 'SubcategoryDetail') {
        fetchSubcategoryData()
      }
    })

    onMounted(() => {
      fetchSubcategoryData()
    })

    return {
      subcategory,
      products,
      filteredProducts,
      paginatedProducts,
      loading,
      error,
      searchQuery,
      currentPage,
      totalPages,
      breadcrumbItems,
      handleSearch,
      nextPage,
      previousPage,
      goToProductDetail,
      getProductImage,
      fetchSubcategoryData
    }
  }
}
</script>

<style scoped>
.subcategory-detail {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Subcategory Header */
.subcategory-header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 50px;
  padding: 30px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 15px;
  color: white;
}

.subcategory-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  background: white;
}

.subcategory-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.subcategory-image .placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 4rem;
}

.subcategory-info {
  flex: 1;
}

.subcategory-info h1 {
  font-size: 2.5rem;
  margin: 0 0 15px 0;
}

.subcategory-info .description {
  font-size: 1.2rem;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
}

/* Products Section */
.products-section {
  margin-top: 40px;
}

.products-section h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.search-box {
  max-width: 500px;
  margin: 0 auto 40px;
}

.search-box input {
  width: 100%;
  padding: 12px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-box input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

/* Grid Layout */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.item-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s ease;
  padding: 20px;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.item-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Circular Image */
.circular-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-card:hover .circular-image {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.circular-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.circular-image .placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
  font-size: 3rem;
}

.item-title {
  font-size: 1.1rem;
  color: #333;
  text-align: center;
  margin: 0 0 10px 0;
  font-weight: 600;
  transition: color 0.3s ease;
}

.item-price {
  font-size: 1.2rem;
  color: #4CAF50;
  font-weight: bold;
  margin: 0;
}

.item-card:hover .item-title {
  color: #4CAF50;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-state {
  text-align: center;
  padding: 60px 20px;
  color: #d32f2f;
}

.error-state i {
  font-size: 3rem;
  margin-bottom: 20px;
}

.retry-btn {
  margin-top: 20px;
  padding: 10px 30px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.retry-btn:hover {
  background: #45a049;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: #ccc;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.pagination button {
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.pagination button:hover:not(:disabled) {
  background: #45a049;
}

.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.pagination span {
  font-size: 1rem;
  color: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .subcategory-header {
    flex-direction: column;
    text-align: center;
  }

  .subcategory-info h1 {
    font-size: 1.8rem;
  }

  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 20px;
  }

  .circular-image {
    width: 120px;
    height: 120px;
  }

  .subcategory-image {
    width: 120px;
    height: 120px;
  }
}
</style>

