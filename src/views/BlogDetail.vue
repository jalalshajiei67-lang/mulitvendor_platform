<template>
  <div class="blog-detail" dir="rtl">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>{{ t('loadingPost') }}</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <i class="fas fa-exclamation-triangle"></i>
      <h2>{{ t('postNotFound') }}</h2>
      <p>{{ error }}</p>
      <button @click="$router.push('/blog')" class="back-btn">
        <i class="fas fa-arrow-right"></i>
        {{ t('backToBlog') }}
      </button>
    </div>

    <!-- Post Content -->
    <article v-else-if="post" class="post-article">
      <!-- Post Header -->
      <header class="post-header">
        <div class="container">
          <!-- Breadcrumb -->
          <nav class="breadcrumb">
            <router-link to="/blog" class="breadcrumb-link">{{ t('blog') }}</router-link>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">{{ post.category_name }}</span>
          </nav>

          <!-- Post Meta -->
          <div class="post-meta">
            <div class="category-badge" :style="{ backgroundColor: post.category_color }">
              {{ post.category_name }}
            </div>
            <div class="post-stats">
              <span class="views">
                <i class="fas fa-eye"></i>
                {{ post.view_count }} {{ t('views') }}
              </span>
              <span class="comments">
                <i class="fas fa-comment"></i>
                {{ post.comment_count }} {{ t('comments') }}
              </span>
              <span class="reading-time">
                <i class="fas fa-clock"></i>
                {{ post.reading_time }} {{ t('minRead') }}
              </span>
            </div>
          </div>

          <!-- Post Title -->
          <h1 class="post-title">{{ post.title }}</h1>

          <!-- Post Excerpt -->
          <p v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</p>

          <!-- Author Info -->
          <div class="author-info">
            <div class="author-avatar">
              <i class="fas fa-user"></i>
            </div>
            <div class="author-details">
              <span class="author-name">{{ post.author_name }}</span>
              <span class="post-date">{{ formatDate(post.published_at || post.created_at) }}</span>
            </div>
            <div class="post-actions">
              <button class="action-btn" @click="sharePost">
                <i class="fas fa-share"></i>
                {{ t('share') }}
              </button>
              <button v-if="isAuthor" class="action-btn edit-btn" @click="editPost">
                <i class="fas fa-edit"></i>
                {{ t('edit') }}
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Featured Image -->
      <div v-if="post.featured_image" class="featured-image">
        <img :src="post.featured_image" :alt="post.title" />
      </div>

      <!-- Post Content -->
      <div class="post-content">
        <div class="container">
          <div class="content-wrapper">
            <div class="main-content">
              <div class="content-body" v-html="formatContent(post.content)"></div>
              
              <!-- Post Tags (if any) -->
              <div v-if="post.tags && post.tags.length > 0" class="post-tags">
                <h4>{{ t('tags') }}:</h4>
                <div class="tags">
                  <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
                </div>
              </div>
            </div>

            <!-- Sidebar -->
            <aside class="sidebar">
              <!-- Related Posts -->
              <div v-if="relatedPosts.length > 0" class="sidebar-section">
                <h3>{{ t('relatedPosts') }}</h3>
                <div class="related-posts">
                  <div 
                    v-for="relatedPost in relatedPosts" 
                    :key="relatedPost.id"
                    class="related-post"
                    @click="goToPost(relatedPost.slug)"
                  >
                    <div class="related-image">
                      <img 
                        v-if="relatedPost.featured_image" 
                        :src="relatedPost.featured_image" 
                        :alt="relatedPost.title"
                      />
                      <div v-else class="no-image">
                        <i class="fas fa-image"></i>
                      </div>
                    </div>
                    <div class="related-content">
                      <h4 class="related-title">{{ relatedPost.title }}</h4>
                      <span class="related-date">{{ formatDate(relatedPost.created_at) }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Popular Posts -->
              <div v-if="popularPosts.length > 0" class="sidebar-section">
                <h3>{{ t('popularPosts') }}</h3>
                <div class="popular-posts">
                  <div 
                    v-for="popularPost in popularPosts.slice(0, 5)" 
                    :key="popularPost.id"
                    class="popular-post"
                    @click="goToPost(popularPost.slug)"
                  >
                    <div class="popular-image">
                      <img 
                        v-if="popularPost.featured_image" 
                        :src="popularPost.featured_image" 
                        :alt="popularPost.title"
                      />
                      <div v-else class="no-image">
                        <i class="fas fa-image"></i>
                      </div>
                    </div>
                    <div class="popular-content">
                      <h4 class="popular-title">{{ popularPost.title }}</h4>
                      <div class="popular-meta">
                        <span class="popular-views">{{ popularPost.view_count }} {{ t('views') }}</span>
                        <span class="popular-date">{{ formatDate(popularPost.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </div>

      <!-- Comments Section -->
      <section class="comments-section">
        <div class="container">
          <div class="comments-wrapper">
            <h3 class="comments-title">
              {{ t('comments') }} ({{ post.comment_count }})
            </h3>

            <!-- Comment Form -->
            <div v-if="isAuthenticated" class="comment-form">
              <h4>{{ t('leaveComment') }}</h4>
              <form @submit.prevent="submitComment">
                <div class="form-group">
                  <textarea 
                    v-model="commentForm.content"
                    :placeholder="t('writeComment')"
                    rows="4"
                    required
                  ></textarea>
                </div>
                <button type="submit" class="submit-btn" :disabled="submittingComment">
                  <i v-if="submittingComment" class="fas fa-spinner fa-spin"></i>
                  <i v-else class="fas fa-paper-plane"></i>
                  {{ submittingComment ? t('postingComment') : t('postComment') }}
                </button>
              </form>
            </div>

            <!-- Login Prompt -->
            <div v-else class="login-prompt">
              <p>{{ t('loginToComment') }}</p>
            </div>

            <!-- Comments List -->
            <div v-if="comments.length > 0" class="comments-list">
              <div 
                v-for="comment in comments" 
                :key="comment.id"
                class="comment"
                :class="{ 'comment-reply': comment.parent }"
              >
                <div class="comment-avatar">
                  <i class="fas fa-user"></i>
                </div>
                <div class="comment-content">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.author_name }}</span>
                    <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                  </div>
                  <div class="comment-body">{{ comment.content }}</div>
                  <div class="comment-actions">
                    <button 
                      v-if="isAuthenticated" 
                      @click="replyToComment(comment)"
                      class="reply-btn"
                    >
                      <i class="fas fa-reply"></i>
                      {{ t('reply') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- No Comments -->
            <div v-else class="no-comments">
              <i class="fas fa-comments"></i>
              <p>{{ t('beFirstToComment') }}</p>
            </div>
          </div>
        </div>
      </section>
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
      return date.toLocaleDateString('en-US', {
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
  background-color: #f8f9fa;
  direction: rtl;
  text-align: right;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
  color: #6c757d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.back-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-direction: row-reverse;
}

.post-article {
  background: white;
}

.post-header {
  padding: 2rem 0;
  border-bottom: 1px solid #e9ecef;
}

.breadcrumb {
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.breadcrumb-link {
  color: #007bff;
  text-decoration: none;
}

.breadcrumb-link:hover {
  text-decoration: underline;
}

.breadcrumb-separator {
  margin: 0 0.5rem;
  color: #6c757d;
}

.breadcrumb-current {
  color: #6c757d;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
  flex-direction: row-reverse;
}

.category-badge {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.post-stats {
  display: flex;
  gap: 1.5rem;
  font-size: 0.9rem;
  color: #6c757d;
  flex-direction: row-reverse;
}

.post-title {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.post-excerpt {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-direction: row-reverse;
}

.author-avatar {
  width: 50px;
  height: 50px;
  background-color: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
  font-size: 1.2rem;
}

.author-details {
  flex: 1;
}

.author-name {
  display: block;
  font-weight: 600;
  color: #2c3e50;
}

.post-date {
  display: block;
  font-size: 0.9rem;
  color: #6c757d;
}

.post-actions {
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.action-btn {
  background: none;
  border: 1px solid #dee2e6;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  flex-direction: row-reverse;
}

.action-btn:hover {
  background-color: #f8f9fa;
}

.edit-btn {
  border-color: #28a745;
  color: #28a745;
}

.edit-btn:hover {
  background-color: #28a745;
  color: white;
}

.featured-image {
  height: 400px;
  overflow: hidden;
}

.featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-content {
  padding: 3rem 0;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 3rem;
}

.main-content {
  min-width: 0;
}

.content-body {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.post-tags {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.post-tags h4 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.tag {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.9rem;
}

.sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.sidebar-section {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sidebar-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.2rem;
}

.related-posts, .popular-posts {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.related-post, .popular-post {
  display: flex;
  gap: 1rem;
  cursor: pointer;
  transition: opacity 0.3s ease;
  flex-direction: row-reverse;
}

.related-post:hover, .popular-post:hover {
  opacity: 0.8;
}

.related-image, .popular-image {
  width: 60px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}

.related-image img, .popular-image img {
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
}

.related-content, .popular-content {
  flex: 1;
  min-width: 0;
}

.related-title, .popular-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #2c3e50;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-date, .popular-meta {
  font-size: 0.8rem;
  color: #6c757d;
}

.popular-meta {
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.comments-section {
  background: white;
  padding: 3rem 0;
  border-top: 1px solid #e9ecef;
}

.comments-title {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.comment-form {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.comment-form h4 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-family: inherit;
  resize: vertical;
}

.submit-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-direction: row-reverse;
}

.submit-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.login-prompt {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment {
  display: flex;
  gap: 1rem;
  flex-direction: row-reverse;
}

.comment-reply {
  margin-right: 3rem;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  background-color: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  flex-direction: row-reverse;
}

.comment-author {
  font-weight: 600;
  color: #2c3e50;
}

.comment-date {
  font-size: 0.9rem;
  color: #6c757d;
}

.comment-body {
  margin-bottom: 0.5rem;
  line-height: 1.6;
  color: #495057;
}

.comment-actions {
  display: flex;
  gap: 1rem;
  flex-direction: row-reverse;
}

.reply-btn {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex-direction: row-reverse;
}

.reply-btn:hover {
  text-decoration: underline;
}

.no-comments {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
}

.no-comments i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

@media (max-width: 768px) {
  .post-title {
    font-size: 2rem;
  }
  
  .content-wrapper {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .sidebar {
    position: static;
  }
  
  .post-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .post-stats {
    flex-wrap: wrap;
  }
  
  .post-stats {
    flex-wrap: wrap;
  }
  
  .comment-reply {
    margin-right: 1rem;
  }
}
</style>
