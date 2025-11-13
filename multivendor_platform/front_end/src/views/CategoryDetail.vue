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
            v-if="category.image || category.image_url" 
            :src="formatImageUrl(category)" 
            :alt="category.name"
          />
          <div v-else class="placeholder-image">
            <i class="fas fa-tag"></i>
          </div>
        </div>
        <div class="category-info">
          <h1>{{ category.name }}</h1>
        </div>
      </div>

      <!-- Subcategories Section -->
      <div class="subcategories-section">
        <h2>زیردسته‌های این دسته‌بندی</h2>

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
                v-if="subcategory.image || subcategory.image_url" 
                :src="formatImageUrl(subcategory)" 
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

        <!-- Description Section -->
        <div class="department-description-section" v-if="category.description">
          <div class="description-content">
            <h2>درباره این دسته‌بندی</h2>
          <div class="description rich-text-content" v-html="safeCategoryDescription"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@unhead/vue'
import api from '@/services/api'
import Breadcrumb from '@/components/Breadcrumb.vue'
import { formatImageUrl } from '@/utils/imageUtils'
import { prepareSchemaScripts, generateBreadcrumbSchema } from '@/composables/useSchema'

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
    const currentPage = ref(1)
    const itemsPerPage = 12

    const decodeHtmlEntities = (input) => {
      if (!input) {
        return ''
      }

      return input
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
        .replace(/&#(\d+);/g, (_, dec) => String.fromCharCode(parseInt(dec, 10)))
        .replace(/&nbsp;/g, ' ')
    }

    const stripDangerousContent = (input) =>
      input
        .replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, '')
        .replace(/on\w+\s*=\s*(['"]).*?\1/gi, '')
        .replace(/javascript:/gi, '')

    const stripHtmlTags = (input) => input.replace(/<\/?[^>]+(>|$)/g, '')

    const getSafeHtml = (input) => stripDangerousContent(decodeHtmlEntities(input || ''))

    const getSafeText = (input) => stripHtmlTags(getSafeHtml(input)).replace(/\s+/g, ' ').trim()

    const safeCategoryDescription = computed(() =>
      category.value?.description ? getSafeHtml(category.value.description) : ''
    )

    const sanitizeForMeta = (value) => {
      if (!value) {
        return ''
      }

      const text = getSafeText(value)
      return text.length > 160 ? `${text.slice(0, 157)}...` : text
    }

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

    // Setup useHead at the top with reactive data
    useHead(() => {
      if (!category.value) {
        return {
          title: 'دسته‌بندی',
          meta: []
        }
      }

      const baseUrl = typeof window !== 'undefined' && window.location?.origin
        ? window.location.origin
        : import.meta.env.VITE_SITE_URL || ''

      const schemas = []

      // Use schema_markup from database if available
      if (category.value.schema_markup) {
        try {
          const parsedSchema = typeof category.value.schema_markup === 'string'
            ? JSON.parse(category.value.schema_markup)
            : category.value.schema_markup
          
          if (Array.isArray(parsedSchema)) {
            schemas.push(...parsedSchema)
          } else {
            schemas.push(parsedSchema)
          }

          // Add BreadcrumbList schema only if schema_markup exists
          if (breadcrumbItems.value.length > 0 && baseUrl) {
            const breadcrumbSchema = generateBreadcrumbSchema(
              breadcrumbItems.value.map(item => ({
                name: item.text,
                url: item.to ? `${baseUrl}${item.to}` : undefined
              })),
              baseUrl
            )
            if (breadcrumbSchema) {
              schemas.push(breadcrumbSchema)
            }
          }
        } catch (error) {
          console.warn('Error parsing schema_markup:', error)
        }
      }

      // Prepare script tags for schemas
      const scriptTags = schemas.length > 0 ? prepareSchemaScripts(schemas) : []

      const metaDescriptionSource = category.value.meta_description || category.value.description
      const metaDescription = sanitizeForMeta(metaDescriptionSource)

      return {
        title: category.value.meta_title || category.value.name,
        meta: [
          {
            name: 'description',
            content: metaDescription
          }
        ],
        ...(scriptTags.length > 0 && { script: scriptTags })
      }
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
          
          // Fetch subcategories filtered by category ID using backend API
          const subResponse = await api.getSubcategories({ category: category.value.id })
          console.log('Subcategories response for category:', subResponse)
          console.log('Subcategories data:', subResponse.data)
          
          let subcategoriesData = subResponse.data
          if (subResponse.data.results) {
            subcategoriesData = subResponse.data.results
          }
          
          console.log('Filtered subcategories for this category:', subcategoriesData)
          
          // Assign subcategories (already filtered by backend)
          if (Array.isArray(subcategoriesData)) {
            subcategories.value = subcategoriesData
          } else {
            subcategories.value = []
          }
          
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

    const totalPages = computed(() => {
      return Math.ceil(subcategories.value.length / itemsPerPage)
    })

    const paginatedSubcategories = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return subcategories.value.slice(start, end)
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
      paginatedSubcategories,
      loading,
      error,
      currentPage,
      totalPages,
      breadcrumbItems,
      nextPage,
      previousPage,
      goToSubcategoryDetail,
      safeCategoryDescription,
      fetchCategoryData,
      formatImageUrl
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
  background: linear-gradient(135deg, #1565C0 0%, #0277BD 100%);
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
  color: #212121;
  margin-bottom: 30px;
  text-align: center;
}

/* Description Section */
.department-description-section {
  margin: 50px 0;
  padding: 0;
}

.description-content {
  background: linear-gradient(135deg, #1565C0 0%, #0277BD 100%);
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
  color: rgba(255, 255, 255, 0.95);
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
  background: linear-gradient(135deg, #FF6F00 0%, #FF8F00 100%);
  color: white;
  font-size: 3rem;
}

.item-title {
  font-size: 1.1rem;
  color: #212121;
  text-align: center;
  margin: 0;
  font-weight: 600;
  transition: color 0.3s ease;
}

.item-card:hover .item-title {
  color: #1565C0;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1565C0;
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
  background: #1565C0;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.retry-btn:hover {
  background: #0D47A1;
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
  color: #212121;
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
  background: #1565C0;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.pagination button:hover:not(:disabled) {
  background: #0D47A1;
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

