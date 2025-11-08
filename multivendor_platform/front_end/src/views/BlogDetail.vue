<template>
  <div class="blog-detail" dir="rtl">
    <!-- Loading State -->
    <v-container v-if="loading" class="py-12">
      <div class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
          class="mb-4"
        ></v-progress-circular>
        <p class="text-body-1 text-medium-emphasis">{{ t('loadingPost') }}</p>
      </div>
    </v-container>

    <!-- Error State -->
    <v-container v-else-if="error" class="py-12">
      <v-card elevation="2" rounded="lg" class="pa-8 text-center">
        <v-icon size="64" color="error" class="mb-4">mdi-alert-circle</v-icon>
        <h2 class="text-h5 mb-2">{{ t('postNotFound') }}</h2>
        <p class="text-body-1 text-medium-emphasis mb-4">{{ error }}</p>
        <v-btn @click="$router.push('/blog')" color="primary" prepend-icon="mdi-arrow-right">
          {{ t('backToBlog') }}
        </v-btn>
      </v-card>
    </v-container>

    <!-- Post Content -->
    <article v-else-if="post">
      <!-- Post Header -->
      <header class="post-header">
        <v-container>
          <!-- Breadcrumb -->
          <v-breadcrumbs
            :items="[
              { title: t('blog'), to: '/blog', disabled: false },
              { title: post.category_name, disabled: true }
            ]"
            class="pa-0 mb-4"
            divider="/"
          >
          </v-breadcrumbs>

          <!-- Post Meta -->
          <div class="d-flex justify-space-between align-center flex-wrap ga-4 mb-6">
            <v-chip
              v-if="post.category_color"
              :style="{ backgroundColor: post.category_color, color: 'white' }"
              size="large"
              class="font-weight-bold"
            >
              {{ post.category_name }}
            </v-chip>
            <div class="d-flex align-center flex-wrap ga-4 text-body-2 text-medium-emphasis">
              <span class="d-flex align-center">
                <v-icon size="small" class="ml-1">mdi-eye</v-icon>
                {{ post.view_count }} {{ t('views') }}
              </span>
              <span class="d-flex align-center">
                <v-icon size="small" class="ml-1">mdi-comment</v-icon>
                {{ post.comment_count }} {{ t('comments') }}
              </span>
              <span class="d-flex align-center">
                <v-icon size="small" class="ml-1">mdi-clock-outline</v-icon>
                {{ post.reading_time }} {{ t('minRead') }}
              </span>
            </div>
          </div>

          <!-- Post Title -->
          <h1 class="text-h4 text-md-h3 text-lg-h2 font-weight-bold mb-4">{{ post.title }}</h1>

          <!-- Post Excerpt -->
          <p v-if="post.excerpt" class="text-h6 text-md-h5 text-medium-emphasis mb-6">
            {{ post.excerpt }}
          </p>

          <!-- Author Info -->
          <div class="d-flex justify-space-between align-center flex-wrap ga-4 mb-4">
            <div class="d-flex align-center ga-3">
              <v-avatar color="primary" size="50">
                <v-icon color="white">mdi-account</v-icon>
              </v-avatar>
              <div>
                <div class="text-subtitle-1 font-weight-bold">{{ post.author_name }}</div>
                <div class="text-caption text-medium-emphasis">
                  {{ formatDate(post.published_at || post.created_at) }}
                </div>
              </div>
            </div>
            <div class="d-flex ga-2">
              <v-btn
                @click="sharePost"
                color="primary"
                variant="outlined"
                prepend-icon="mdi-share-variant"
              >
                {{ t('share') }}
              </v-btn>
              <v-btn
                v-if="isAuthor"
                @click="editPost"
                color="success"
                variant="outlined"
                prepend-icon="mdi-pencil"
              >
                {{ t('edit') }}
              </v-btn>
            </div>
          </div>
        </v-container>
      </header>

      <!-- Featured Image -->
      <div v-if="post.featured_image" class="featured-image-wrapper">
        <v-img
          :src="post.featured_image"
          :alt="post.title"
          height="400"
          cover
          class="featured-image"
        ></v-img>
      </div>

      <!-- Post Content -->
      <v-container class="py-8 py-md-12">
        <v-row>
          <!-- Main Content -->
          <v-col cols="12" lg="8">
            <v-card elevation="2" rounded="xl" class="pa-6 pa-md-8 mb-6">
              <div class="content-body" v-html="formatContent(post.content)"></div>
              
              <!-- Post Tags -->
              <div v-if="post.tags && post.tags.length > 0" class="mt-8 pt-6 border-t">
                <h4 class="text-h6 font-weight-bold mb-4">{{ t('tags') }}:</h4>
                <div class="d-flex flex-wrap ga-2">
                  <v-chip
                    v-for="tag in post.tags"
                    :key="tag"
                    color="primary"
                    variant="tonal"
                    size="small"
                  >
                    {{ tag }}
                  </v-chip>
                </div>
              </div>
            </v-card>

            <!-- Comments Section -->
            <v-card elevation="2" rounded="xl" class="pa-6 pa-md-8">
              <h3 class="text-h5 font-weight-bold mb-6">
                {{ t('comments') }} ({{ post.comment_count }})
              </h3>

              <!-- Comment Form -->
              <v-card
                v-if="isAuthenticated"
                variant="tonal"
                color="primary"
                class="pa-4 pa-md-6 mb-6"
              >
                <h4 class="text-h6 font-weight-bold mb-4">{{ t('leaveComment') }}</h4>
                <form @submit.prevent="submitComment">
                  <v-textarea
                    v-model="commentForm.content"
                    :placeholder="t('writeComment')"
                    rows="4"
                    variant="outlined"
                    required
                    class="mb-4"
                  ></v-textarea>
                  <v-btn
                    type="submit"
                    color="primary"
                    :loading="submittingComment"
                    :disabled="submittingComment"
                    prepend-icon="mdi-send"
                  >
                    {{ submittingComment ? t('postingComment') : t('postComment') }}
                  </v-btn>
                </form>
              </v-card>

              <!-- Login Prompt -->
              <v-alert
                v-else
                type="info"
                variant="tonal"
                class="mb-6"
              >
                {{ t('loginToComment') }}
              </v-alert>

              <!-- Comments List -->
              <div v-if="comments.length > 0" class="comments-list">
                <div
                  v-for="comment in comments"
                  :key="comment.id"
                  class="comment mb-6"
                  :class="{ 'comment-reply': comment.parent }"
                >
                  <div class="d-flex ga-4">
                    <v-avatar color="primary" size="40">
                      <v-icon color="white" size="small">mdi-account</v-icon>
                    </v-avatar>
                    <div class="flex-grow-1">
                      <div class="d-flex justify-space-between align-center mb-2 flex-wrap ga-2">
                        <span class="text-subtitle-2 font-weight-bold">{{ comment.author_name }}</span>
                        <span class="text-caption text-medium-emphasis">
                          {{ formatDate(comment.created_at) }}
                        </span>
                      </div>
                      <div class="text-body-2 mb-2">{{ comment.content }}</div>
                      <v-btn
                        v-if="isAuthenticated"
                        @click="replyToComment(comment)"
                        color="primary"
                        variant="text"
                        size="small"
                        prepend-icon="mdi-reply"
                      >
                        {{ t('reply') }}
                      </v-btn>
                    </div>
                  </div>
                </div>
              </div>

              <!-- No Comments -->
              <div v-else class="text-center py-12">
                <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-comment-outline</v-icon>
                <p class="text-body-1 text-medium-emphasis">{{ t('beFirstToComment') }}</p>
              </div>
            </v-card>
          </v-col>

          <!-- Sidebar -->
          <v-col cols="12" lg="4">
            <div class="sidebar">
              <!-- Related Posts -->
              <v-card
                v-if="relatedPosts.length > 0"
                elevation="2"
                rounded="xl"
                class="pa-4 pa-md-6 mb-6"
              >
                <h3 class="text-h6 font-weight-bold mb-4">{{ t('relatedPosts') }}</h3>
                <div class="related-posts">
                  <div
                    v-for="relatedPost in relatedPosts"
                    :key="relatedPost.id"
                    class="related-post mb-4"
                    @click="goToPost(relatedPost.slug)"
                  >
                    <div class="d-flex ga-3 cursor-pointer">
                      <v-avatar
                        rounded="lg"
                        size="60"
                        class="flex-shrink-0"
                      >
                        <v-img
                          v-if="relatedPost.featured_image"
                          :src="relatedPost.featured_image"
                          :alt="relatedPost.title"
                          cover
                        ></v-img>
                        <v-icon v-else>mdi-image</v-icon>
                      </v-avatar>
                      <div class="flex-grow-1 min-width-0">
                        <h4 class="text-subtitle-2 font-weight-bold mb-1 line-clamp-2">
                          {{ relatedPost.title }}
                        </h4>
                        <span class="text-caption text-medium-emphasis">
                          {{ formatDate(relatedPost.created_at) }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </v-card>

              <!-- Popular Posts -->
              <v-card
                v-if="popularPosts.length > 0"
                elevation="2"
                rounded="xl"
                class="pa-4 pa-md-6"
              >
                <h3 class="text-h6 font-weight-bold mb-4">{{ t('popularPosts') }}</h3>
                <div class="popular-posts">
                  <div
                    v-for="popularPost in popularPosts.slice(0, 5)"
                    :key="popularPost.id"
                    class="popular-post mb-4"
                    @click="goToPost(popularPost.slug)"
                  >
                    <div class="d-flex ga-3 cursor-pointer">
                      <v-avatar
                        rounded="lg"
                        size="60"
                        class="flex-shrink-0"
                      >
                        <v-img
                          v-if="popularPost.featured_image"
                          :src="popularPost.featured_image"
                          :alt="popularPost.title"
                          cover
                        ></v-img>
                        <v-icon v-else>mdi-image</v-icon>
                      </v-avatar>
                      <div class="flex-grow-1 min-width-0">
                        <h4 class="text-subtitle-2 font-weight-bold mb-1 line-clamp-2">
                          {{ popularPost.title }}
                        </h4>
                        <div class="d-flex align-center flex-wrap ga-2 text-caption text-medium-emphasis">
                          <span class="d-flex align-center">
                            <v-icon size="x-small" class="ml-1">mdi-eye</v-icon>
                            {{ popularPost.view_count }} {{ t('views') }}
                          </span>
                          <span>•</span>
                          <span>{{ formatDate(popularPost.created_at) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </v-card>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </article>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBlogStore } from '@/stores/blog'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'BlogDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const blogStore = useBlogStore()
    const authStore = useAuthStore()
    
    const commentForm = ref({
      content: '',
      parent: null
    })
    const submittingComment = ref(false)
    
    const post = computed(() => blogStore.currentPost)
    const comments = computed(() => blogStore.comments)
    const relatedPosts = computed(() => blogStore.relatedPosts || [])
    const popularPosts = computed(() => blogStore.popularPosts)
    const loading = computed(() => blogStore.loading)
    const error = computed(() => blogStore.error)
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const t = computed(() => blogStore.t)
    
    const isAuthor = computed(() => {
      return post.value && authStore.user && post.value.author === authStore.user.id
    })
    
    const fetchPost = async () => {
      const slug = route.params.slug
      await blogStore.fetchPost(slug)
    }
    
    const fetchComments = async () => {
      const slug = route.params.slug
      await blogStore.fetchComments(slug)
    }
    
    const fetchRelatedPosts = async () => {
      const slug = route.params.slug
      try {
        await blogStore.fetchRelatedPosts(slug)
      } catch (error) {
        console.error('Error fetching related posts:', error)
      }
    }
    
    const fetchPopularPosts = async () => {
      try {
        await blogStore.fetchPopularPosts()
      } catch (error) {
        console.error('Error fetching popular posts:', error)
      }
    }
    
    const submitComment = async () => {
      if (!commentForm.value.content.trim()) return
      
      submittingComment.value = true
      try {
        const slug = route.params.slug
        await blogStore.createComment(slug, commentForm.value)
        commentForm.value.content = ''
        commentForm.value.parent = null
        await fetchComments()
      } catch (error) {
        console.error('Error submitting comment:', error)
      } finally {
        submittingComment.value = false
      }
    }
    
    const replyToComment = (comment) => {
      commentForm.value.parent = comment.id
      commentForm.value.content = `@${comment.author_name} `
    }
    
    const sharePost = () => {
      if (navigator.share) {
        navigator.share({
          title: post.value.title,
          text: post.value.excerpt,
          url: window.location.href
        })
      } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href)
        alert(t.value('linkCopied'))
      }
    }
    
    const editPost = () => {
      router.push({ name: 'EditBlogPost', params: { slug: route.params.slug } })
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
    
    const formatContent = (content) => {
      // Simple formatting - in a real app, you might want to use a markdown parser
      return content.replace(/\n/g, '<br>')
    }
    
    onMounted(async () => {
      await Promise.all([
        fetchPost(),
        fetchComments(),
        fetchRelatedPosts(),
        fetchPopularPosts()
      ])
    })
    
    watch(() => route.params.slug, () => {
      fetchPost()
      fetchComments()
      fetchRelatedPosts()
    })
    
    return {
      post,
      comments,
      relatedPosts,
      popularPosts,
      loading,
      error,
      isAuthenticated,
      isAuthor,
      commentForm,
      submittingComment,
      t,
      submitComment,
      replyToComment,
      sharePost,
      editPost,
      goToPost,
      formatDate,
      formatContent
    }
  }
}
</script>

<style scoped>
.blog-detail {
  min-height: 100vh;
  background-color: #F5F5F5;
  direction: rtl;
}

.post-header {
  background: white;
  padding: 2rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.featured-image-wrapper {
  width: 100%;
  overflow: hidden;
}

.featured-image {
  width: 100%;
}

.content-body {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #212121;
}

.content-body :deep(p) {
  margin-bottom: 1.5rem;
}

.content-body :deep(h1),
.content-body :deep(h2),
.content-body :deep(h3),
.content-body :deep(h4),
.content-body :deep(h5),
.content-body :deep(h6) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #212121;
}

.content-body :deep(ul),
.content-body :deep(ol) {
  margin-bottom: 1.5rem;
  padding-right: 2rem;
}

.content-body :deep(li) {
  margin-bottom: 0.5rem;
}

.content-body :deep(blockquote) {
  border-right: 4px solid #1565C0;
  padding-right: 1rem;
  margin: 1.5rem 0;
  font-style: italic;
  color: #666;
}

.content-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.content-body :deep(pre) {
  background-color: #f5f7fa;
  padding: 1em;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5rem 0;
  border: 1px solid #e0e0e0;
}

.content-body :deep(code) {
  background-color: #f5f7fa;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}

.content-body :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

.sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.related-post,
.popular-post {
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.related-post:hover,
.popular-post:hover {
  opacity: 0.8;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.min-width-0 {
  min-width: 0;
}

.comment-reply {
  margin-right: 3rem;
}

.border-t {
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}

.cursor-pointer {
  cursor: pointer;
}

/* Mobile Responsive */
@media (max-width: 959px) {
  .post-header {
    padding: 1.5rem 0;
  }
  
  .sidebar {
    position: static;
  }
  
  .comment-reply {
    margin-right: 1rem;
  }
  
  .featured-image-wrapper {
    height: 250px;
  }
}
</style>
