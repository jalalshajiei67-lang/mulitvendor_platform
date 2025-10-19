<!-- src/views/DepartmentList.vue -->
<template>
  <div class="department-list" dir="rtl">
    <Breadcrumb :items="breadcrumbItems" />
    <div class="list-header">
      <h1>بخش‌ها</h1>
      <div class="search-box">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="جستجوی بخش..."
          @input="handleSearch"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>در حال بارگذاری بخش‌ها...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
      <button @click="fetchDepartments" class="retry-btn">دوباره تلاش کنید</button>
    </div>

    <!-- Departments Grid -->
    <div v-else-if="filteredDepartments.length > 0">
      <div class="items-grid">
        <div 
          v-for="department in paginatedDepartments" 
          :key="department.id" 
          class="item-card"
          @click="goToDepartmentDetail(department.slug)"
        >
          <div class="circular-image">
            <img 
              v-if="department.image" 
              :src="department.image" 
              :alt="department.name"
            />
            <div v-else class="placeholder-image">
              <i class="fas fa-folder"></i>
            </div>
          </div>
          <h3 class="item-title">{{ department.name }}</h3>
        </div>
      </div>

      <!-- Description Section -->
      <div class="description-section" v-if="pageDescription">
        <h2>درباره بخش‌ها</h2>
        <p>{{ pageDescription }}</p>
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

    <!-- Empty State -->
    <div v-else class="empty-state">
      <i class="fas fa-folder-open"></i>
      <h3>بخشی یافت نشد</h3>
      <p>هیچ بخشی پیدا نشد.</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import Breadcrumb from '@/components/Breadcrumb.vue'

export default {
  name: 'DepartmentList',
  components: {
    Breadcrumb
  },
  setup() {
    const router = useRouter()
    const departments = ref([])
    const loading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const itemsPerPage = 12

    const breadcrumbItems = [
      { text: 'خانه', to: '/' },
      { text: 'بخش‌ها', to: '/departments' }
    ]

    const pageDescription = 'تمام بخش‌های موجود در فروشگاه را مرور کنید. بخش مورد نظر خود را انتخاب کنید تا دسته‌بندی‌ها و محصولات مرتبط را مشاهده کنید.'

    const fetchDepartments = async () => {
      loading.value = true
      error.value = null
      try {
        const response = await api.getDepartments()
        console.log('Full response:', response)
        console.log('Response data:', response.data)
        console.log('Type of response.data:', typeof response.data)
        console.log('Is array?', Array.isArray(response.data))
        
        // Handle different response structures
        let departmentsData = response.data
        if (response.data.results) {
          departmentsData = response.data.results
          console.log('Using paginated results:', departmentsData)
        }
        
        console.log('Departments before filter:', departmentsData)
        // Temporarily show all departments (not filtering by is_active)
        departments.value = Array.isArray(departmentsData) 
          ? departmentsData 
          : []
        console.log('Departments after filter:', departments.value)
        console.log('Number of departments:', departments.value.length)
      } catch (err) {
        error.value = 'بارگذاری بخش‌ها با خطا مواجه شد. لطفاً دوباره تلاش کنید.'
        console.error('Error fetching departments:', err)
      } finally {
        loading.value = false
      }
    }

    const filteredDepartments = computed(() => {
      if (!searchQuery.value) {
        return departments.value
      }
      const query = searchQuery.value.toLowerCase()
      return departments.value.filter(dept => 
        dept.name.toLowerCase().includes(query) ||
        (dept.description && dept.description.toLowerCase().includes(query))
      )
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredDepartments.value.length / itemsPerPage)
    })

    const paginatedDepartments = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return filteredDepartments.value.slice(start, end)
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

    const goToDepartmentDetail = (slug) => {
      router.push({ name: 'DepartmentDetail', params: { slug } })
    }

    onMounted(() => {
      fetchDepartments()
    })

    return {
      departments,
      filteredDepartments,
      paginatedDepartments,
      loading,
      error,
      searchQuery,
      currentPage,
      totalPages,
      breadcrumbItems,
      pageDescription,
      handleSearch,
      nextPage,
      previousPage,
      goToDepartmentDetail,
      fetchDepartments
    }
  }
}
</script>

<style scoped>
.department-list {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.list-header h1 {
  font-size: 2rem;
  color: #333;
  margin: 0;
}

.search-box {
  flex: 1;
  max-width: 400px;
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

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

/* Description Section */
.description-section {
  background: #f9f9f9;
  padding: 30px;
  border-radius: 10px;
  margin: 40px 0;
  text-align: center;
}

.description-section h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 15px;
}

.description-section p {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.8;
  max-width: 800px;
  margin: 0 auto;
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
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 20px;
  }

  .circular-image {
    width: 120px;
    height: 120px;
  }

  .list-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-box {
    max-width: 100%;
  }
}
</style>

