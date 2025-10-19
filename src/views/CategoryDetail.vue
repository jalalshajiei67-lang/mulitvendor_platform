<!-- src/views/CategoryDetail.vue -->
<template>
  <div class="category-detail" dir="rtl">
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
      <button @click="fetchCategoryData" class="retry-btn">دوباره تلاش کنید</button>
    </div>

    <!-- Category Content -->
    <div v-else-if="category">
      <!-- Category Header -->
      <div class="category-header">
        <div class="category-image">
          <img 
            v-if="category.image" 
            :src="category.image" 
            :alt="category.name"
          />
          <div v-else class="placeholder-image">
            <i class="fas fa-tag"></i>
          </div>
        </div>
        <div class="category-info">
          <h1>{{ category.name }}</h1>
          <p v-if="category.description" class="description">{{ category.description }}</p>
        </div>
      </div>

      <!-- Subcategories Section -->
      <div class="subcategories-section">
        <h2>زیردسته‌های این دسته‌بندی</h2>
        
        <!-- Search Box -->
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="جستجوی زیردسته..."
            @input="handleSearch"
          />
        </div>

        <!-- Subcategories Grid -->
        <div v-if="paginatedSubcategories.length > 0" class="items-grid">
          <div 
            v-for="subcategory in paginatedSubcategories" 
            :key="subcategory.id" 
            class="item-card"
            @click="goToSubcategoryDetail(subcategory.slug)"
          >
            <div class="circular-image">
              <img 
                v-if="subcategory.image" 
                :src="subcategory.image" 
                :alt="subcategory.name"
              />
              <div v-else class="placeholder-image">
                <i class="fas fa-layer-group"></i>
              </div>
            </div>
            <h3 class="item-title">{{ subcategory.name }}</h3>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <i class="fas fa-layer-group"></i>
          <h3>زیردسته‌ای وجود ندارد</h3>
          <p>هیچ زیردسته‌ای در این دسته‌بندی وجود ندارد.</p>
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
  name: 'CategoryDetail',
  components: {
    Breadcrumb
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const category = ref(null)
    const subcategories = ref([])
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
      if (category.value?.departments && category.value.departments.length > 0) {
        const dept = category.value.departments[0]
        items.push({ text: dept.name, to: `/departments/${dept.slug}` })
      }
      
      items.push({ text: category.value?.name || 'دسته‌بندی', to: `/categories/${route.params.slug}` })
      
      return items
    })

    const fetchCategoryData = async () => {
      loading.value = true
      error.value = null
      try {
        // Fetch category by slug
        console.log('Fetching category with slug:', route.params.slug)
        const catResponse = await api.getCategoryBySlug(route.params.slug)
        console.log('Category response:', catResponse)
        console.log('Category response data:', catResponse.data)
        
        // Handle different response structures
        let catData = catResponse.data
        if (catResponse.data.results) {
          catData = catResponse.data.results
        }
        
        if (catData && (Array.isArray(catData) ? catData.length > 0 : catData.id)) {
          category.value = Array.isArray(catData) ? catData[0] : catData
          console.log('Category found:', category.value)
          
          // Fetch all subcategories and filter by category
          const subResponse = await api.getSubcategories()
          console.log('Subcategories response:', subResponse)
          console.log('Subcategories data:', subResponse.data)
          
          let subcategoriesData = subResponse.data
          if (subResponse.data.results) {
            subcategoriesData = subResponse.data.results
          }
          
          console.log('All subcategories:', subcategoriesData)
          
          // Filter subcategories - temporarily not filtering by is_active
          if (Array.isArray(subcategoriesData)) {
            subcategories.value = subcategoriesData.filter(sub => 
              sub.categories && sub.categories.some(cat => cat.id === category.value.id)
            )
          } else {
            subcategories.value = []
          }
          
          console.log('Filtered subcategories for this category:', subcategories.value)
          console.log('Number of subcategories:', subcategories.value.length)
        } else {
          error.value = 'دسته‌بندی یافت نشد'
          console.log('Category not found')
        }
      } catch (err) {
        error.value = 'بارگذاری اطلاعات با خطا مواجه شد. لطفاً دوباره تلاش کنید.'
        console.error('Error fetching category data:', err)
        console.error('Error details:', err.response)
      } finally {
        loading.value = false
      }
    }

    const filteredSubcategories = computed(() => {
      if (!searchQuery.value) {
        return subcategories.value
      }
      const query = searchQuery.value.toLowerCase()
      return subcategories.value.filter(sub => 
        sub.name.toLowerCase().includes(query) ||
        (sub.description && sub.description.toLowerCase().includes(query))
      )
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredSubcategories.value.length / itemsPerPage)
    })

    const paginatedSubcategories = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return filteredSubcategories.value.slice(start, end)
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

    const goToSubcategoryDetail = (slug) => {
      router.push({ name: 'SubcategoryDetail', params: { slug } })
    }

    watch(() => route.params.slug, () => {
      if (route.name === 'CategoryDetail') {
        fetchCategoryData()
      }
    })

    onMounted(() => {
      fetchCategoryData()
    })

    return {
      category,
      subcategories,
      filteredSubcategories,
      paginatedSubcategories,
      loading,
      error,
      searchQuery,
      currentPage,
      totalPages,
      breadcrumbItems,
      handleSearch,
      nextPage,
      previousPage,
      goToSubcategoryDetail,
      fetchCategoryData
    }
  }
}
</script>

<style scoped>
.category-detail {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Category Header */
.category-header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 50px;
  padding: 30px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 15px;
  color: white;
}

.category-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  background: white;
}

.category-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-image .placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 4rem;
}

.category-info {
  flex: 1;
}

.category-info h1 {
  font-size: 2.5rem;
  margin: 0 0 15px 0;
}

.category-info .description {
  font-size: 1.2rem;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
}

/* Subcategories Section */
.subcategories-section {
  margin-top: 40px;
}

.subcategories-section h2 {
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
}

.item-card:hover {
  transform: translateY(-5px);
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
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  font-size: 3rem;
}

.item-title {
  font-size: 1.1rem;
  color: #333;
  text-align: center;
  margin: 0;
  font-weight: 600;
  transition: color 0.3s ease;
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
  .category-header {
    flex-direction: column;
    text-align: center;
  }

  .category-info h1 {
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

  .category-image {
    width: 120px;
    height: 120px;
  }
}
</style>

