<template>
  <div class="blog-list" dir="rtl">
    <!-- Header Section -->
    <div class="blog-header">
      <v-container fluid class="pa-0">
        <v-row no-gutters justify="center" align="center" class="hero-content">
          <v-col cols="12" class="text-center pa-8 pa-md-12">
            <h1 class="text-h3 text-md-h2 text-lg-h1 font-weight-bold mb-4 text-white readable-heading">
              {{ t('blog') }}
            </h1>
            <p class="text-h6 text-md-h5 text-white opacity-90 max-width-600 mx-auto readable-text">
              {{ t('discoverInsights') }}
            </p>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Category Filter -->
    <v-container class="pa-0">
      <v-card 
        elevation="2" 
        rounded="0" 
        class="category-filter"
        color="surface"
      >
        <v-container>
          <div class="filter-tabs d-flex flex-wrap ga-2 py-4">
            <v-btn
              v-for="category in categories"
              :key="category.id"
              @click="selectCategory(category)"
              :color="getCategoryButtonColor(category)"
              :variant="selectedCategory?.id === category.id ? 'elevated' : 'outlined'"
              rounded="xl"
              size="small"
              :style="getCategoryButtonStyle(category)"
            >
              {{ category.name }}
            </v-btn>
            <v-btn
              @click="selectCategory(null)"
              :color="!selectedCategory ? 'primary' : 'default'"
              :variant="!selectedCategory ? 'elevated' : 'outlined'"
              rounded="xl"
              size="small"
              class="ms-auto"
            >
              {{ t('allPosts') }}
            </v-btn>
          </div>
        </v-container>
      </v-card>
    </v-container>

    <!-- Main Content -->
    <v-container class="py-8 py-md-12">
      <!-- Featured Posts Section -->
      <section v-if="!selectedCategory && featuredPosts.length > 0" class="mb-12">
        <h2 class="text-h4 text-md-h3 font-weight-bold mb-6 readable-heading">{{ t('featuredPosts') }}</h2>
        <v-row>
          <v-col
            v-for="post in featuredPosts.slice(0, 3)"
            :key="post.id"
            cols="12"
            md="6"
            lg="4"
          >
            <v-card
              elevation="4"
              rounded="xl"
              class="featured-card h-100"
              @click="goToPost(post.slug)"
              hover
            >
              <v-img
                v-if="post.featured_image"
                :src="post.featured_image"
                :alt="post.title"
                height="200"
                cover
              >
              </v-img>
              <div v-else class="no-image d-flex align-center justify-center" style="height: 200px;">
                <v-icon size="48" color="grey-lighten-1">mdi-image</v-icon>
              </div>
              
              <v-card-text class="pa-4 pa-md-6">
                <v-chip
                  v-if="post.category_color"
                  :style="{ backgroundColor: post.category_color, color: 'white' }"
                  size="small"
                  class="mb-3"
                >
                  {{ post.category_name }}
                </v-chip>
                
                <h3 class="text-h6 text-md-h5 font-weight-bold mb-3 readable-heading">{{ post.title }}</h3>
                <p class="text-body-2 text-medium-emphasis mb-4 excerpt-text">{{ post.excerpt }}</p>
                
                <div class="d-flex align-center flex-wrap ga-3 text-caption text-medium-emphasis meta-text">
                  <span class="d-flex align-center">
                    <v-icon size="small" class="ml-1">mdi-account</v-icon>
                    {{ post.author_name }}
                  </span>
                  <span class="d-flex align-center">
                    <v-icon size="small" class="ml-1">mdi-calendar</v-icon>
                    {{ formatDate(post.created_at) }}
                  </span>
                  <span class="d-flex align-center">
                    <v-icon size="small" class="ml-1">mdi-clock-outline</v-icon>
                    {{ post.reading_time }} {{ t('minRead') }}
                  </span>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </section>

      <!-- Posts Section -->
      <section class="posts-section">
        <div class="d-flex justify-space-between align-center mb-6 flex-column-reverse flex-md-row-reverse ga-4">
          <h2 class="text-h4 text-md-h3 font-weight-bold mb-0 readable-heading">
            {{ selectedCategory ? `${selectedCategory.name} ${t('posts')}` : t('allPosts') }}
          </h2>
          <div class="d-flex ga-2">
            <v-btn
              @click="viewMode = 'grid'"
              :color="viewMode === 'grid' ? 'primary' : 'default'"
              :variant="viewMode === 'grid' ? 'elevated' : 'outlined'"
              icon="mdi-view-grid"
              size="small"
            ></v-btn>
            <v-btn
              @click="viewMode = 'list'"
              :color="viewMode === 'list' ? 'primary' : 'default'"
              :variant="viewMode === 'list' ? 'elevated' : 'outlined'"
              icon="mdi-view-list"
              size="small"
            ></v-btn>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
            class="mb-4"
          ></v-progress-circular>
          <p class="text-body-1 text-medium-emphasis">{{ t('loadingPosts') }}</p>
        </div>

        <!-- Error State -->
        <v-card v-else-if="error" elevation="2" rounded="lg" class="pa-8 text-center">
          <v-icon size="64" color="error" class="mb-4">mdi-alert-circle</v-icon>
          <h3 class="text-h6 mb-2">{{ error }}</h3>
          <v-btn @click="fetchPosts" color="primary" class="mt-4">
            {{ t('tryAgain') }}
          </v-btn>
        </v-card>

        <!-- Posts Grid/List -->
        <v-row v-else-if="posts.length > 0" :class="{ 'posts-list': viewMode === 'list' }">
          <v-col
            v-for="post in posts"
            :key="post.id"
            :cols="viewMode === 'list' ? 12 : 12"
            :sm="viewMode === 'list' ? 12 : 6"
            :md="viewMode === 'list' ? 12 : 6"
            :lg="viewMode === 'list' ? 12 : 4"
          >
            <v-card
              v-if="viewMode === 'grid'"
              elevation="2"
              rounded="xl"
              class="post-card h-100"
              @click="goToPost(post.slug)"
              hover
            >
              <div class="post-image-wrapper position-relative">
                <v-img
                  v-if="post.featured_image"
                  :src="post.featured_image"
                  :alt="post.title"
                  height="200"
                  cover
                ></v-img>
                <div v-else class="no-image d-flex align-center justify-center" style="height: 200px;">
                  <v-icon size="48" color="grey-lighten-1">mdi-image</v-icon>
                </div>
                <v-chip
                  v-if="post.is_featured"
                  color="warning"
                  size="small"
                  class="position-absolute"
                  style="top: 12px; right: 12px;"
                >
                  <v-icon start size="small">mdi-star</v-icon>
                  {{ t('featured') }}
                </v-chip>
              </div>
              
              <v-card-text class="pa-4 pa-md-6">
                <div class="d-flex justify-space-between align-center mb-3">
                  <v-chip
                    v-if="post.category_color"
                    :style="{ backgroundColor: post.category_color, color: 'white' }"
                    size="small"
                  >
                    {{ post.category_name }}
                  </v-chip>
                  <div class="d-flex ga-3 text-caption text-medium-emphasis">
                    <span class="d-flex align-center">
                      <v-icon size="x-small" class="ml-1">mdi-eye</v-icon>
                      {{ post.view_count }}
                    </span>
                    <span class="d-flex align-center">
                      <v-icon size="x-small" class="ml-1">mdi-comment</v-icon>
                      {{ post.comment_count }}
                    </span>
                  </div>
                </div>
                
                <h3 class="text-h6 font-weight-bold mb-2 readable-heading">{{ post.title }}</h3>
                <p class="text-body-2 text-medium-emphasis mb-4 excerpt-text">{{ post.excerpt }}</p>
                
                <div class="d-flex justify-space-between align-center flex-wrap ga-2 text-caption text-medium-emphasis meta-text">
                  <div class="d-flex align-center flex-wrap ga-2">
                    <span>{{ post.author_name }}</span>
                    <span>•</span>
                    <span>{{ formatDate(post.created_at) }}</span>
                  </div>
                  <span class="d-flex align-center">
                    <v-icon size="x-small" class="ml-1">mdi-clock-outline</v-icon>
                    {{ post.reading_time }} {{ t('minRead') }}
                  </span>
                </div>
              </v-card-text>
            </v-card>

            <!-- List View Card -->
            <v-card
              v-else
              elevation="2"
              rounded="xl"
              class="post-card-list mb-4"
              @click="goToPost(post.slug)"
              hover
            >
              <v-row no-gutters>
                <v-col cols="12" sm="4" md="3">
                  <div class="post-image-wrapper position-relative h-100">
                    <v-img
                      v-if="post.featured_image"
                      :src="post.featured_image"
                      :alt="post.title"
                      height="100%"
                      min-height="200"
                      cover
                    ></v-img>
                    <div v-else class="no-image d-flex align-center justify-center h-100" style="min-height: 200px;">
                      <v-icon size="48" color="grey-lighten-1">mdi-image</v-icon>
                    </div>
                    <v-chip
                      v-if="post.is_featured"
                      color="warning"
                      size="small"
                      class="position-absolute"
                      style="top: 12px; right: 12px;"
                    >
                      <v-icon start size="small">mdi-star</v-icon>
                      {{ t('featured') }}
                    </v-chip>
                  </div>
                </v-col>
                <v-col cols="12" sm="8" md="9">
                  <v-card-text class="pa-4 pa-md-6">
                    <div class="d-flex justify-space-between align-center mb-3 flex-wrap ga-2">
                      <v-chip
                        v-if="post.category_color"
                        :style="{ backgroundColor: post.category_color, color: 'white' }"
                        size="small"
                      >
                        {{ post.category_name }}
                      </v-chip>
                      <div class="d-flex ga-3 text-caption text-medium-emphasis">
                        <span class="d-flex align-center">
                          <v-icon size="x-small" class="ml-1">mdi-eye</v-icon>
                          {{ post.view_count }}
                        </span>
                        <span class="d-flex align-center">
                          <v-icon size="x-small" class="ml-1">mdi-comment</v-icon>
                          {{ post.comment_count }}
                        </span>
                      </div>
                    </div>
                    
                    <h3 class="text-h6 text-md-h5 font-weight-bold mb-2 readable-heading">{{ post.title }}</h3>
                    <p class="text-body-2 text-medium-emphasis mb-4 excerpt-text">{{ post.excerpt }}</p>
                    
                    <div class="d-flex justify-space-between align-center flex-wrap ga-2 text-caption text-medium-emphasis meta-text">
                      <div class="d-flex align-center flex-wrap ga-2">
                        <span class="d-flex align-center">
                          <v-icon size="x-small" class="ml-1">mdi-account</v-icon>
                          {{ post.author_name }}
                        </span>
                        <span>•</span>
                        <span class="d-flex align-center">
                          <v-icon size="x-small" class="ml-1">mdi-calendar</v-icon>
                          {{ formatDate(post.created_at) }}
                        </span>
                      </div>
                      <span class="d-flex align-center">
                        <v-icon size="x-small" class="ml-1">mdi-clock-outline</v-icon>
                        {{ post.reading_time }} {{ t('minRead') }}
                      </span>
                    </div>
                  </v-card-text>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>

        <!-- Empty State -->
        <v-card v-else elevation="2" rounded="lg" class="pa-12 text-center">
          <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-newspaper-variant</v-icon>
          <h3 class="text-h6 mb-2 readable-heading">{{ t('noPostsFound') }}</h3>
          <p class="text-body-2 text-medium-emphasis readable-text">
            {{ selectedCategory ? t('noPostsInCategory') : t('noBlogPostsAvailable') }}
          </p>
        </v-card>

        <!-- Pagination -->
        <div v-if="pagination.count > 12" class="d-flex justify-center align-center flex-wrap ga-4 mt-8">
          <v-btn
            @click="loadPage(pagination.previous)"
            :disabled="!pagination.previous"
            color="primary"
            variant="elevated"
            prepend-icon="mdi-chevron-right"
          >
            {{ t('previous') }}
          </v-btn>
          
          <div class="text-body-1 font-weight-medium">
            {{ t('page') }} {{ currentPage }} {{ t('of') }} {{ totalPages }}
          </div>
          
          <v-btn
            @click="loadPage(pagination.next)"
            :disabled="!pagination.next"
            color="primary"
            variant="elevated"
            append-icon="mdi-chevron-left"
          >
            {{ t('next') }}
          </v-btn>
        </div>
      </section>
    </v-container>
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
      return date.toLocaleDateString('fa-IR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const getCategoryButtonColor = (category) => {
      if (selectedCategory.value?.id === category.id) {
        return category.color ? undefined : 'primary'
      }
      return 'default'
    }
    
    const getCategoryButtonStyle = (category) => {
      if (selectedCategory.value?.id === category.id && category.color) {
        return {
          backgroundColor: category.color,
          borderColor: category.color,
          color: 'white'
        }
      }
      return {}
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
      formatDate,
      getCategoryButtonColor,
      getCategoryButtonStyle
    }
  }
}
</script>

<style scoped>
.blog-list {
  min-height: 100vh;
  background-color: #F5F5F5;
  direction: rtl;
}

.blog-header {
  background: linear-gradient(135deg, #1565C0 0%, #0277BD 100%);
  padding: 4rem 0;
}

.max-width-600 {
  max-width: 600px;
}

.category-filter {
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.filter-tabs {
  overflow-x: auto;
  padding: 0.5rem 0;
}

.filter-tabs::-webkit-scrollbar {
  height: 4px;
}

.filter-tabs::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.filter-tabs::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 2px;
}

.featured-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.featured-card:hover {
  transform: translateY(-8px);
}

.post-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-4px);
}

.post-card-list {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card-list:hover {
  transform: translateX(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}

.post-image-wrapper {
  overflow: hidden;
  border-radius: 12px 12px 0 0;
}

.posts-list .post-image-wrapper {
  border-radius: 12px 0 0 12px;
}

.no-image {
  background-color: #f5f5f5;
}

/* Typography improvements */
.readable-heading {
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: rgba(var(--v-theme-on-surface), 0.96);
}

.readable-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.meta-text {
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.72);
  font-size: 0.875rem;
}

.excerpt-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

/* Card text improvements */
.post-card h3,
.post-card-list h3,
.featured-card h3 {
  line-height: 1.4;
}

.post-card p,
.post-card-list p,
.featured-card p {
  line-height: 1.75;
}

/* Mobile Responsive */
@media (max-width: 959px) {
  .blog-header {
    padding: 2rem 0;
  }
  
  .post-card-list :deep(.v-row) {
    flex-direction: column;
  }
  
  .posts-list .post-image-wrapper {
    border-radius: 12px 12px 0 0;
  }
}
</style>
