<template>
  <div class="blog-list" dir="rtl">
    <!-- Header Section -->
    <div class="blog-header">
      <div class="container">
        <h1 class="blog-title">{{ t('blog') }}</h1>
        <p class="blog-subtitle">{{ t('discoverInsights') }}</p>
      </div>
    </div>

    <!-- Category Filter -->
    <div class="category-filter">
      <div class="container">
        <div class="filter-tabs">
          <button 
            @click="selectCategory(null)"
            :class="['filter-tab', { active: !selectedCategory }]"
          >
            {{ t('allPosts') }}
          </button>
          <button 
            v-for="category in categories" 
            :key="category.id"
            @click="selectCategory(category)"
            :class="['filter-tab', { active: selectedCategory?.id === category.id }]"
            :style="{ borderColor: category.color }"
          >
            {{ category.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container">
      <div class="blog-content">
        <!-- Featured Posts Section -->
        <section v-if="!selectedCategory && featuredPosts.length > 0" class="featured-section">
          <h2 class="section-title">{{ t('featuredPosts') }}</h2>
          <div class="featured-grid">
            <div 
              v-for="post in featuredPosts.slice(0, 3)" 
              :key="post.id"
              class="featured-card"
              @click="goToPost(post.slug)"
            >
              <div class="featured-image">
                <img 
                  v-if="post.featured_image" 
                  :src="post.featured_image" 
                  :alt="post.title"
                />
                <div v-else class="no-image">
                  <i class="fas fa-image"></i>
                </div>
              </div>
              <div class="featured-content">
                <div class="category-badge" :style="{ backgroundColor: post.category_color }">
                  {{ post.category_name }}
                </div>
                <h3 class="featured-title">{{ post.title }}</h3>
                <p class="featured-excerpt">{{ post.excerpt }}</p>
                <div class="featured-meta">
                  <span class="author">{{ post.author_name }}</span>
                  <span class="date">{{ formatDate(post.created_at) }}</span>
                  <span class="reading-time">{{ post.reading_time }} {{ t('minRead') }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Posts Grid -->
        <section class="posts-section">
          <div class="section-header">
            <h2 class="section-title">
              {{ selectedCategory ? `${selectedCategory.name} ${t('posts')}` : t('allPosts') }}
            </h2>
            <div class="view-options">
              <button 
                @click="viewMode = 'grid'"
                :class="['view-btn', { active: viewMode === 'grid' }]"
                :title="t('gridView')"
              >
                <i class="fas fa-th"></i>
              </button>
              <button 
                @click="viewMode = 'list'"
                :class="['view-btn', { active: viewMode === 'list' }]"
                :title="t('listView')"
              >
                <i class="fas fa-list"></i>
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>{{ t('loadingPosts') }}</p>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="error-state">
            <i class="fas fa-exclamation-triangle"></i>
            <p>{{ error }}</p>
            <button @click="fetchPosts" class="retry-btn">{{ t('tryAgain') }}</button>
          </div>

          <!-- Posts Grid/List -->
          <div v-else-if="posts.length > 0" :class="['posts-container', viewMode]">
            <article 
              v-for="post in posts" 
              :key="post.id"
              class="post-card"
              @click="goToPost(post.slug)"
            >
              <div class="post-image">
                <img 
                  v-if="post.featured_image" 
                  :src="post.featured_image" 
                  :alt="post.title"
                />
                <div v-else class="no-image">
                  <i class="fas fa-image"></i>
                </div>
                <div v-if="post.is_featured" class="featured-badge">
                  <i class="fas fa-star"></i>
                </div>
              </div>
              
              <div class="post-content">
                <div class="post-meta">
                  <div class="category-badge" :style="{ backgroundColor: post.category_color }">
                    {{ post.category_name }}
                  </div>
                  <div class="post-stats">
                    <span class="views">
                      <i class="fas fa-eye"></i>
                      {{ post.view_count }}
                    </span>
                    <span class="comments">
                      <i class="fas fa-comment"></i>
                      {{ post.comment_count }}
                    </span>
                  </div>
                </div>
                
                <h3 class="post-title">{{ post.title }}</h3>
                <p class="post-excerpt">{{ post.excerpt }}</p>
                
                  <div class="post-footer">
                    <div class="author-info">
                      <span class="author">{{ post.author_name }}</span>
                      <span class="date">{{ formatDate(post.created_at) }}</span>
                    </div>
                    <span class="reading-time">{{ post.reading_time }} {{ t('minRead') }}</span>
                  </div>
              </div>
            </article>
          </div>

          <!-- Empty State -->
          <div v-else class="empty-state">
            <i class="fas fa-newspaper"></i>
            <h3>{{ t('noPostsFound') }}</h3>
            <p>{{ selectedCategory ? t('noPostsInCategory') : t('noBlogPostsAvailable') }}</p>
          </div>

          <!-- Pagination -->
          <div v-if="pagination.count > 12" class="pagination">
            <button 
              @click="loadPage(pagination.previous)"
              :disabled="!pagination.previous"
              class="pagination-btn"
            >
              <i class="fas fa-chevron-right"></i>
              {{ t('previous') }}
            </button>
            
            <div class="pagination-info">
              {{ t('page') }} {{ currentPage }} {{ t('of') }} {{ totalPages }}
            </div>
            
            <button 
              @click="loadPage(pagination.next)"
              :disabled="!pagination.next"
              class="pagination-btn"
            >
              {{ t('next') }}
              <i class="fas fa-chevron-left"></i>
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useBlogStore } from '@/stores/blog'

export default {
  name: 'BlogList',
  setup() {
    const router = useRouter()
    const blogStore = useBlogStore()
    
    const selectedCategory = ref(null)
    const viewMode = ref('grid')
    const currentPage = ref(1)
    
    const posts = computed(() => blogStore.posts)
    const categories = computed(() => blogStore.categories)
    const featuredPosts = computed(() => blogStore.featuredPosts)
    const loading = computed(() => blogStore.loading)
    const error = computed(() => blogStore.error)
    const pagination = computed(() => blogStore.pagination)
    const t = computed(() => blogStore.t)
    
    const totalPages = computed(() => {
      return Math.ceil(pagination.value.count / 12)
    })
    
    const fetchPosts = async () => {
      const params = {
        page: currentPage.value,
        page_size: 12
      }
      
      if (selectedCategory.value) {
        await blogStore.fetchCategoryPosts(selectedCategory.value.slug)
      } else {
        await blogStore.fetchPosts(params)
      }
    }
    
    const fetchCategories = async () => {
      await blogStore.fetchCategories()
    }
    
    const fetchFeaturedPosts = async () => {
      await blogStore.fetchFeaturedPosts()
    }
    
    const selectCategory = async (category) => {
      selectedCategory.value = category
      currentPage.value = 1
      await fetchPosts()
    }
    
    const loadPage = async (url) => {
      if (!url) return
      
      const urlObj = new URL(url)
      const page = urlObj.searchParams.get('page')
      currentPage.value = parseInt(page) || 1
      
      await fetchPosts()
    }
    
    const goToPost = (slug) => {
      router.push({ name: 'BlogDetail', params: { slug } })
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    onMounted(async () => {
      await Promise.all([
        fetchCategories(),
        fetchPosts(),
        fetchFeaturedPosts()
      ])
    })
    
    watch(selectedCategory, () => {
      currentPage.value = 1
    })
    
    return {
      posts,
      categories,
      featuredPosts,
      loading,
      error,
      pagination,
      selectedCategory,
      viewMode,
      currentPage,
      totalPages,
      t,
      fetchPosts,
      selectCategory,
      loadPage,
      goToPost,
      formatDate
    }
  }
}
</script>

<style scoped>
.blog-list {
  min-height: 100vh;
  background-color: #f8f9fa;
  direction: rtl;
  text-align: right;
}

.blog-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.blog-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.blog-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

.category-filter {
  background: white;
  border-bottom: 1px solid #e9ecef;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.filter-tabs {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 0.5rem 0;
  flex-direction: row-reverse;
}

.filter-tab {
  background: none;
  border: 2px solid transparent;
  border-radius: 25px;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.filter-tab:hover {
  background-color: #f8f9fa;
}

.filter-tab.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.blog-content {
  padding: 2rem 0;
}

.section-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.featured-section {
  margin-bottom: 4rem;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.featured-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.featured-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.featured-image {
  height: 200px;
  overflow: hidden;
}

.featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  color: #6c757d;
  font-size: 2rem;
}

.featured-content {
  padding: 1.5rem;
}

.category-badge {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.featured-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #2c3e50;
  line-height: 1.4;
}

.featured-excerpt {
  color: #6c757d;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.featured-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #6c757d;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-direction: row-reverse;
}

.view-options {
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.view-btn {
  background: none;
  border: 1px solid #dee2e6;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn:hover {
  background-color: #f8f9fa;
}

.view-btn.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.posts-container.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.posts-container.list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.post-image {
  height: 200px;
  overflow: hidden;
  position: relative;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.featured-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: #ffc107;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.post-content {
  padding: 1.5rem;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.post-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #6c757d;
}

.post-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #2c3e50;
  line-height: 1.4;
}

.post-excerpt {
  color: #6c757d;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #6c757d;
  flex-direction: row-reverse;
}

.author-info {
  display: flex;
  gap: 1rem;
  flex-direction: row-reverse;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6c757d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.retry-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 3rem;
  flex-direction: row-reverse;
}

.pagination-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s ease;
  flex-direction: row-reverse;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.pagination-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.pagination-info {
  font-weight: 500;
  color: #2c3e50;
}

@media (max-width: 768px) {
  .blog-title {
    font-size: 2rem;
  }
  
  .featured-grid {
    grid-template-columns: 1fr;
  }
  
  .posts-container.grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .view-options {
    flex-direction: row;
  }
  
  .pagination {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
