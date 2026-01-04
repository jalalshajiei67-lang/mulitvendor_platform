<template>
  <div dir="rtl" class="education-post-list">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
      <p class="text-body-2 text-medium-emphasis mt-4">در حال بارگذاری...</p>
    </div>

    <!-- Error State -->
    <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
    </v-alert>

    <!-- Posts List -->
    <div v-else-if="posts.length > 0" class="posts-container">
      <div
        v-for="(post, index) in posts"
        :key="post.id"
        class="post-item"
        :class="{ 'post-item-last': index === posts.length - 1 }"
        @click="openPost(post)"
      >
        <div class="post-content">
          <h3 class="post-title">{{ post.title }}</h3>
          
          <div class="post-meta">
            <span class="meta-item">
              <v-icon size="14" class="ml-1">mdi-account</v-icon>
              {{ post.author_name }}
            </span>
            <span class="meta-separator">|</span>
            <span class="meta-item">
              <v-icon size="14" class="ml-1">mdi-calendar</v-icon>
              {{ formatDate(post.created_at) }}
            </span>
            <span class="meta-separator">|</span>
            <span class="meta-item">
              <v-icon size="14" class="ml-1">mdi-eye</v-icon>
              {{ post.view_count }}
            </span>
            <span v-if="post.comment_count > 0" class="meta-separator">|</span>
            <span v-if="post.comment_count > 0" class="meta-item">
              <v-icon size="14" class="ml-1">mdi-comment-outline</v-icon>
              {{ post.comment_count }}
            </span>
            <span class="meta-separator">|</span>
            <span class="meta-item">
              <v-icon size="14" class="ml-1">mdi-clock-outline</v-icon>
              {{ post.reading_time }} دقیقه
            </span>
          </div>

          <p v-if="post.excerpt" class="post-excerpt">{{ stripHtml(post.excerpt) }}</p>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pageCount > 1" class="pagination-container mt-6">
        <v-pagination
          v-model="currentPage"
          :length="pageCount"
          :total-visible="7"
          @update:model-value="handlePageChange"
        ></v-pagination>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state text-center py-12">
      <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-book-open-variant</v-icon>
      <h3 class="text-h6 mb-2">مطلبی یافت نشد</h3>
      <p class="text-body-2 text-medium-emphasis">هنوز محتوای آموزشی برای نمایش وجود ندارد.</p>
    </div>

    <!-- Post Detail Dialog -->
    <EducationPostDetail
      v-model="selectedPost"
      :post-slug="selectedPostSlug"
      @close="selectedPostSlug = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useEducationApi, type EducationPost, type PaginatedResponse } from '~/composables/useEducationApi'
import EducationPostDetail from './EducationPostDetail.vue'

interface Props {
  type: 'seller' | 'buyer'
}

const props = defineProps<Props>()

const educationApi = useEducationApi()
const posts = ref<EducationPost[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)
const selectedPostSlug = ref<string | null>(null)
const selectedPost = ref(false)

const pageCount = computed(() => {
  return Math.ceil(totalCount.value / pageSize.value)
})

const fetchPosts = async () => {
  loading.value = true
  error.value = null
  
  try {
    let response: PaginatedResponse<EducationPost>
    
    if (props.type === 'seller') {
      response = await educationApi.getSellerEducationPosts(currentPage.value, pageSize.value)
    } else {
      response = await educationApi.getBuyerEducationPosts(currentPage.value, pageSize.value)
    }
    
    posts.value = response.results || []
    totalCount.value = response.count || 0
  } catch (err: any) {
    console.error('Error fetching education posts:', err)
    error.value = err?.data?.detail || err?.message || 'خطا در بارگذاری مطالب آموزشی'
    posts.value = []
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchPosts()
  // Scroll to top on page change
  if (process.client) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const openPost = (post: EducationPost) => {
  selectedPostSlug.value = post.slug
  selectedPost.value = true
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const stripHtml = (html: string) => {
  if (!html) return ''
  const tmp = document.createElement('DIV')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

onMounted(() => {
  fetchPosts()
})

watch(() => props.type, () => {
  currentPage.value = 1
  fetchPosts()
})
</script>

<style scoped>
.education-post-list {
  width: 100%;
}

.posts-container {
  width: 100%;
}

.post-item {
  padding: 16px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.post-item:hover {
  background-color: rgba(var(--v-theme-on-surface), 0.02);
}

.post-item-last {
  border-bottom: none;
}

.post-content {
  width: 100%;
}

.post-title {
  font-size: 16px;
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface));
  margin-bottom: 8px;
  line-height: 1.5;
}

.post-title:hover {
  color: rgb(var(--v-theme-primary));
}

.post-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 12px;
  color: rgb(var(--v-theme-on-surface-variant));
  margin-bottom: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-separator {
  color: rgb(var(--v-theme-on-surface-variant));
  opacity: 0.5;
}

.post-excerpt {
  font-size: 14px;
  color: rgb(var(--v-theme-on-surface-variant));
  line-height: 1.6;
  margin-top: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination-container {
  display: flex;
  justify-content: center;
}

.empty-state {
  padding: 48px 16px;
}

@media (max-width: 600px) {
  .post-item {
    padding: 12px;
  }
  
  .post-title {
    font-size: 15px;
  }
  
  .post-meta {
    font-size: 11px;
    gap: 6px;
  }
  
  .post-excerpt {
    font-size: 13px;
  }
}
</style>

