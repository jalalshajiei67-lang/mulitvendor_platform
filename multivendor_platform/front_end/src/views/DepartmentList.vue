<!-- src/views/DepartmentList.vue -->
<template>
  <div class="department-list" dir="rtl">
    <Breadcrumb :items="breadcrumbItems" />
    <div class="list-header">
      <h1>بخش‌ها</h1>
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
    <div v-else-if="departments.length > 0">
      <div class="items-grid">
        <div 
          v-for="department in paginatedDepartments" 
          :key="department.id" 
          class="item-card"
          @click="goToDepartmentDetail(department.slug)"
        >
          <div class="circular-image">
            <img 
              v-if="department.image || department.image_url" 
              :src="formatImageUrl(department)" 
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
      <div class="department-description-section" v-if="pageDescription">
        <div class="description-content">
          <h2>درباره بخش‌ها</h2>
          <div class="description rich-text-content" v-html="pageDescription"></div>
        </div>
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
import { formatImageUrl } from '@/utils/imageUtils'

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

    const totalPages = computed(() => {
      return Math.ceil(departments.value.length / itemsPerPage)
    })

    const paginatedDepartments = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return departments.value.slice(start, end)
    })

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
      paginatedDepartments,
      loading,
      error,
      currentPage,
      totalPages,
      breadcrumbItems,
      pageDescription,
      nextPage,
      previousPage,
      goToDepartmentDetail,
      fetchDepartments,
      formatImageUrl
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
  margin-bottom: 30px;
}

.list-header h1 {
  font-size: 2rem;
  color: #333;
  margin: 0;
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
.department-description-section {
  margin: 50px 0;
  padding: 0;
}

.description-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.description-content::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

.description-content h2 {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 20px;
  font-weight: 700;
  position: relative;
  z-index: 1;
}

.description-content .description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.95);
  line-height: 2;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* Rich text content styling for HTML descriptions */
.rich-text-content {
  text-align: right;
  direction: rtl;
}

.rich-text-content :deep(p) {
  margin-bottom: 1.2em;
  line-height: 1.8;
  text-align: justify;
}

.rich-text-content :deep(h1),
.rich-text-content :deep(h2),
.rich-text-content :deep(h3),
.rich-text-content :deep(h4),
.rich-text-content :deep(h5),
.rich-text-content :deep(h6) {
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  font-weight: 700;
  line-height: 1.4;
}

.rich-text-content :deep(h1) {
  font-size: 2em;
}

.rich-text-content :deep(h2) {
  font-size: 1.75em;
}

.rich-text-content :deep(h3) {
  font-size: 1.5em;
}

.rich-text-content :deep(ul),
.rich-text-content :deep(ol) {
  margin: 1em 0;
  padding-right: 2em;
  line-height: 1.8;
}

.rich-text-content :deep(li) {
  margin-bottom: 0.5em;
}

.rich-text-content :deep(a) {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: underline;
  transition: color 0.3s ease;
}

.rich-text-content :deep(a:hover) {
  color: #fff;
}

.rich-text-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1.5em 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.rich-text-content :deep(blockquote) {
  border-right: 4px solid rgba(255, 255, 255, 0.5);
  padding-right: 1.5em;
  margin: 1.5em 0;
  font-style: italic;
  opacity: 0.9;
}

.rich-text-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
}

.rich-text-content :deep(table th),
.rich-text-content :deep(table td) {
  padding: 0.75em;
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-align: right;
}

.rich-text-content :deep(table th) {
  background-color: rgba(255, 255, 255, 0.1);
  font-weight: 700;
}

.rich-text-content :deep(strong),
.rich-text-content :deep(b) {
  font-weight: 700;
}

.rich-text-content :deep(em),
.rich-text-content :deep(i) {
  font-style: italic;
}

.rich-text-content :deep(code) {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.rich-text-content :deep(pre) {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1em;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5em 0;
}

.rich-text-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
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

  .description-content {
    padding: 25px 20px;
  }

  .description-content h2 {
    font-size: 1.4rem;
    margin-bottom: 15px;
  }

  .description-content .description {
    font-size: 1rem;
    line-height: 1.8;
  }
}
</style>

