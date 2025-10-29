<!-- src/views/DepartmentDetail.vue -->
<template>
  <div class="department-detail" dir="rtl">
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
      <button @click="fetchDepartmentData" class="retry-btn">دوباره تلاش کنید</button>
    </div>

    <!-- Department Content -->
    <div v-else-if="department">
      <!-- Department Header -->
      <div class="department-header">
        <div class="department-image">
          <img 
            v-if="department.image" 
            :src="department.image" 
            :alt="department.name"
          />
          <div v-else class="placeholder-image">
            <i class="fas fa-folder"></i>
          </div>
        </div>
        <div class="department-info">
          <h1>{{ department.name }}</h1>
          <p v-if="department.description" class="description">{{ department.description }}</p>
        </div>
      </div>

      <!-- Categories Section -->
      <div class="categories-section">
        <h2>دسته‌بندی‌های این بخش</h2>
        
        <!-- Search Box -->
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="جستجوی دسته‌بندی..."
            @input="handleSearch"
          />
        </div>

        <!-- Categories Grid -->
        <div v-if="paginatedCategories.length > 0" class="items-grid">
          <div 
            v-for="category in paginatedCategories" 
            :key="category.id" 
            class="item-card"
            @click="goToCategoryDetail(category.slug)"
          >
            <div class="circular-image">
              <img 
                v-if="category.image" 
                :src="category.image" 
                :alt="category.name"
              />
              <div v-else class="placeholder-image">
                <i class="fas fa-tag"></i>
              </div>
            </div>
            <h3 class="item-title">{{ category.name }}</h3>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <i class="fas fa-tag"></i>
          <h3>دسته‌بندی وجود ندارد</h3>
          <p>هیچ دسته‌بندی در این بخش وجود ندارد.</p>
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
  name: 'DepartmentDetail',
  components: {
    Breadcrumb
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const department = ref(null)
    const categories = ref([])
    const loading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const itemsPerPage = 12

    const breadcrumbItems = computed(() => [
      { text: 'خانه', to: '/' },
      { text: 'بخش‌ها', to: '/departments' },
      { text: department.value?.name || 'بخش', to: `/departments/${route.params.slug}` }
    ])

    const fetchDepartmentData = async () => {
      loading.value = true
      error.value = null
      try {
        // Fetch department by slug
        console.log('Fetching department with slug:', route.params.slug)
        const deptResponse = await api.getDepartmentBySlug(route.params.slug)
        console.log('Department response:', deptResponse)
        console.log('Department response data:', deptResponse.data)
        
        // Handle different response structures
        let deptData = deptResponse.data
        if (deptResponse.data.results) {
          deptData = deptResponse.data.results
        }
        
        if (deptData && (Array.isArray(deptData) ? deptData.length > 0 : deptData.id)) {
          department.value = Array.isArray(deptData) ? deptData[0] : deptData
          console.log('Department found:', department.value)
          
          // Fetch categories filtered by department ID using backend API
          const catResponse = await api.getCategories({ department: department.value.id })
          console.log('Categories response for department:', catResponse)
          console.log('Categories data:', catResponse.data)
          
          let categoriesData = catResponse.data
          if (catResponse.data.results) {
            categoriesData = catResponse.data.results
          }
          
          console.log('Filtered categories for this department:', categoriesData)
          
          // Assign categories (already filtered by backend)
          if (Array.isArray(categoriesData)) {
            categories.value = categoriesData
          } else {
            categories.value = []
          }
          
          console.log('Number of categories:', categories.value.length)
        } else {
          error.value = 'بخش یافت نشد'
          console.log('Department not found')
        }
      } catch (err) {
        error.value = 'بارگذاری اطلاعات با خطا مواجه شد. لطفاً دوباره تلاش کنید.'
        console.error('Error fetching department data:', err)
        console.error('Error details:', err.response)
      } finally {
        loading.value = false
      }
    }

    const filteredCategories = computed(() => {
      if (!searchQuery.value) {
        return categories.value
      }
      const query = searchQuery.value.toLowerCase()
      return categories.value.filter(cat => 
        cat.name.toLowerCase().includes(query) ||
        (cat.description && cat.description.toLowerCase().includes(query))
      )
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredCategories.value.length / itemsPerPage)
    })

    const paginatedCategories = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return filteredCategories.value.slice(start, end)
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

    const goToCategoryDetail = (slug) => {
      router.push({ name: 'CategoryDetail', params: { slug } })
    }

    watch(() => route.params.slug, () => {
      if (route.name === 'DepartmentDetail') {
        fetchDepartmentData()
      }
    })

    onMounted(() => {
      fetchDepartmentData()
    })

    return {
      department,
      categories,
      filteredCategories,
      paginatedCategories,
      loading,
      error,
      searchQuery,
      currentPage,
      totalPages,
      breadcrumbItems,
      handleSearch,
      nextPage,
      previousPage,
      goToCategoryDetail,
      fetchDepartmentData
    }
  }
}
</script>

<style scoped>
.department-detail {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Department Header */
.department-header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 50px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  color: white;
}

.department-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  background: white;
}

.department-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.department-image .placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 4rem;
}

.department-info {
  flex: 1;
}

.department-info h1 {
  font-size: 2.5rem;
  margin: 0 0 15px 0;
}

.department-info .description {
  font-size: 1.2rem;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
}

/* Categories Section */
.categories-section {
  margin-top: 40px;
}

.categories-section h2 {
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
  .department-header {
    flex-direction: column;
    text-align: center;
  }

  .department-info h1 {
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

  .department-image {
    width: 120px;
    height: 120px;
  }
}
</style>

