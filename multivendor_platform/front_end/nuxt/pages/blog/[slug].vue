<template>
  <div v-if="post" class="blog-detail">
    <section class="hero" :style="heroStyle">
      <v-container class="py-10 py-md-14">
        <div class="text-white">
          <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0 mb-4">
            <template #divider>
              <v-icon>mdi-chevron-left</v-icon>
            </template>
          </v-breadcrumbs>
          <v-chip v-if="post.category_name" class="mb-4" size="small" color="rgba(255,255,255,0.24)">
            {{ post.category_name }}
          </v-chip>
          <h1 class="text-h3 text-md-h1 font-weight-bold mb-4 hero-heading">
            {{ post.title }}
          </h1>
          <p class="text-body-1 text-md-h5 opacity-90 hero-text">
            {{ post.excerpt }}
          </p>

          <div class="d-flex flex-wrap gap-4 mt-6 text-body-2 text-md-subtitle-2 hero-meta">
            <span class="d-flex align-center">
              <v-icon size="18" class="ml-2">mdi-account</v-icon>
              {{ post.author_name }}
            </span>
            <span class="d-flex align-center">
              <v-icon size="18" class="ml-2">mdi-calendar</v-icon>
              {{ formatDate(post.created_at) }}
            </span>
            <span class="d-flex align-center">
              <v-icon size="18" class="ml-2">mdi-clock-outline</v-icon>
              {{ post.reading_time }} {{ t('minRead') }}
            </span>
            <span class="d-flex align-center">
              <v-icon size="18" class="ml-2">mdi-eye</v-icon>
              {{ post.view_count }}
            </span>
          </div>
        </div>
      </v-container>
    </section>

    <v-container class="py-10">
      <v-row>
        <v-col cols="12" md="8">
          <v-card elevation="3" rounded="xl" class="pa-6 pa-md-10 mb-10">
            <v-img
              v-if="post.featured_image"
              :src="post.featured_image"
              :alt="post.title"
              class="rounded-xl mb-8"
              height="420"
              cover
              loading="lazy"
            >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-skeleton-loader type="image" width="100%" height="100%" />
                </div>
              </template>
            </v-img>
            <article class="content content-body" v-html="post.content" />
          </v-card>

          <section class="mb-12">
            <div class="d-flex align-center justify-space-between mb-6">
              <h2 class="text-h5 font-weight-bold readable-heading">{{ t('comments') }}</h2>
              <v-btn
                v-if="!isAuthenticated"
                color="primary"
                variant="text"
                to="/login"
              >
                {{ t('loginToComment') }}
              </v-btn>
            </div>

            <v-card v-if="isAuthenticated" elevation="2" rounded="xl" class="pa-6 mb-8">
              <v-form @submit.prevent="submitComment">
                <v-textarea
                  v-model="newComment"
                  :label="t('writeComment')"
                  rows="4"
                  variant="outlined"
                  density="comfortable"
                  auto-grow
                  required
                />
                <div class="d-flex justify-end mt-4">
                  <v-btn color="primary" :loading="commentLoading" type="submit">
                    {{ t('postComment') }}
                  </v-btn>
                </div>
              </v-form>
            </v-card>

            <v-alert v-if="!comments.length" variant="tonal" color="primary">
              {{ t('beFirstToComment') }}
            </v-alert>

            <v-list v-else lines="three" class="comment-list">
              <v-list-item
                v-for="comment in comments"
                :key="comment.id"
                class="comment-item"
              >
                <template #prepend>
                  <v-avatar color="primary" size="44">
                    <span class="text-body-2 font-weight-bold">
                      {{ comment.author_name?.[0] || 'ن' }}
                    </span>
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-medium mb-1">
                  {{ comment.author_name || 'کاربر' }}
                </v-list-item-title>
                <v-list-item-subtitle class="text-caption text-medium-emphasis mb-3 meta-text">
                  {{ formatDate(comment.created_at) }}
                </v-list-item-subtitle>
                <div class="text-body-2 comment-text">
                  {{ comment.content }}
                </div>
              </v-list-item>
            </v-list>
          </section>
        </v-col>

        <v-col cols="12" md="4">
          <v-card elevation="2" rounded="xl" class="pa-6 mb-8">
            <h3 class="text-subtitle-1 font-weight-bold mb-4 readable-heading">{{ t('recentPosts') }}</h3>
            <v-list lines="one" density="comfortable">
              <v-list-item
                v-for="item in recentPosts.slice(0, 5)"
                :key="item.id"
                @click="goToPost(item.slug)"
                class="rounded-lg"
              >
                <v-list-item-title class="font-weight-medium">
                  {{ item.title }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ formatDate(item.created_at) }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>

          <v-card
            v-if="relatedPosts.length"
            elevation="2"
            rounded="xl"
            class="pa-6"
          >
            <h3 class="text-subtitle-1 font-weight-bold mb-4 readable-heading">{{ t('relatedPosts') }}</h3>
            <v-list lines="two" density="comfortable">
              <v-list-item
                v-for="item in relatedPosts"
                :key="item.id"
                @click="goToPost(item.slug)"
                class="rounded-lg"
              >
                <v-list-item-title class="font-weight-medium">
                  {{ item.title }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ item.reading_time }} {{ t('minRead') }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>

  <BlogDetailSkeleton v-else />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const blogStore = useBlogStore()
const { currentPost, comments, recentPosts, relatedPosts } = storeToRefs(blogStore)
const t = blogStore.t

const authToken = useCookie<string | null>('authToken')
const isAuthenticated = computed(() => Boolean(authToken.value || (process.client && localStorage.getItem('authToken'))))

const post = computed(() => currentPost.value)

const newComment = ref('')
const commentLoading = ref(false)

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('blog'), to: '/blog' },
  { title: post.value?.title ?? '', disabled: true }
])

const heroStyle = computed(() => {
  if (post.value?.category_color) {
    return {
      background: `linear-gradient(135deg, ${post.value.category_color}, rgba(0,0,0,0.45))`
    }
  }
  
  // Use fallback colors if CSS variables aren't available
  // The CSS will handle the gradient with CSS variables
  return {}
})

const formatDate = (value: string) =>
  new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(new Date(value))

const fetchPage = async () => {
  await blogStore.fetchPost(slug.value)
  await Promise.all([
    blogStore.fetchRecentPosts(),
    blogStore.fetchRelatedPosts(slug.value),
    blogStore.fetchComments(slug.value)
  ])
}

await useAsyncData(`blog-detail-${slug.value}`, fetchPage)

watch(
  () => route.params.slug,
  async (next, prev) => {
    if (next !== prev) {
      await fetchPage()
    }
  }
)

const submitComment = async () => {
  if (!newComment.value.trim()) {
    return
  }

  commentLoading.value = true
  try {
    await blogStore.createComment(slug.value, { content: newComment.value })
    newComment.value = ''
    await blogStore.fetchComments(slug.value)
  } catch (error) {
    console.error('Error submitting comment:', error)
  } finally {
    commentLoading.value = false
  }
}

const goToPost = (targetSlug: string) => {
  navigateTo(`/blog/${targetSlug}`)
}

useSeoMeta({
  title: () => post.value?.meta_title ?? post.value?.title ?? 'وبلاگ',
  description: () => post.value?.meta_description ?? post.value?.excerpt ?? '',
  ogTitle: () => post.value?.meta_title ?? post.value?.title ?? '',
  ogDescription: () => post.value?.meta_description ?? post.value?.excerpt ?? '',
  ogType: 'article',
  ogImage: () => post.value?.featured_image ?? ''
})
</script>

<style scoped>
.hero {
  color: rgba(var(--v-theme-on-primary), 0.98);
  border-radius: 24px;
  margin: 16px auto 36px;
  max-width: 1440px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.12);
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(255, 255, 255, 0.28), transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.hero .v-container {
  position: relative;
  z-index: 1;
}

/* Hero-specific text styling - ensure white text is visible */
.hero-heading {
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: rgba(255, 255, 255, 0.98) !important;
}

.hero-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(255, 255, 255, 0.9) !important;
}

.hero-meta {
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85) !important;
  font-size: 0.875rem;
}

.hero-meta .v-icon {
  color: rgba(255, 255, 255, 0.85) !important;
}

/* Ensure breadcrumbs are visible in hero */
.hero :deep(.v-breadcrumbs) {
  color: rgba(255, 255, 255, 0.9) !important;
}

.hero :deep(.v-breadcrumbs .v-breadcrumbs-item) {
  color: rgba(255, 255, 255, 0.9) !important;
}

.hero :deep(.v-breadcrumbs .v-icon) {
  color: rgba(255, 255, 255, 0.7) !important;
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

/* Content body styling */
.content-body {
  max-width: 100%;
  line-height: 1.8;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
}

.blog-detail .content-body :deep(img) {
  max-width: 100%;
  border-radius: 16px;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  box-shadow: 0 4px 12px rgba(var(--v-theme-on-surface), 0.1);
}

.blog-detail .content-body :deep(h1),
.blog-detail .content-body :deep(h2),
.blog-detail .content-body :deep(h3),
.blog-detail .content-body :deep(h4),
.blog-detail .content-body :deep(h5),
.blog-detail .content-body :deep(h6) {
  font-weight: 700;
  line-height: 1.3;
  color: rgba(var(--v-theme-on-surface), 0.96);
  margin-bottom: 0;
}

/* Medium.com-inspired heading spacing */
.blog-detail .content-body :deep(h1) {
  font-size: 2.5rem;
  margin-top: 3rem;
  margin-bottom: 1.5rem;
}

.blog-detail .content-body :deep(h1:first-child) {
  margin-top: 0;
}

.blog-detail .content-body :deep(h2) {
  font-size: 2rem;
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
}

.blog-detail .content-body :deep(h3) {
  font-size: 1.75rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.blog-detail .content-body :deep(h4) {
  font-size: 1.5rem;
  margin-top: 1.75rem;
  margin-bottom: 0.875rem;
}

.blog-detail .content-body :deep(h5) {
  font-size: 1.25rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.blog-detail .content-body :deep(h6) {
  font-size: 1.125rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

/* Medium.com-inspired paragraph spacing */
.blog-detail .content-body :deep(p) {
  line-height: 1.8;
  margin-top: 0;
  margin-bottom: 1.75rem;
  color: rgba(var(--v-theme-on-surface), 0.87);
  font-size: 1.05rem;
  text-align: justify;
  max-width: 65ch;
}

/* First paragraph after heading has less top margin */
.blog-detail .content-body :deep(h1 + p),
.blog-detail .content-body :deep(h2 + p),
.blog-detail .content-body :deep(h3 + p),
.blog-detail .content-body :deep(h4 + p),
.blog-detail .content-body :deep(h5 + p),
.blog-detail .content-body :deep(h6 + p) {
  margin-top: 0.5rem;
}

.blog-detail .content-body :deep(ul),
.blog-detail .content-body :deep(ol) {
  margin-top: 1.5rem;
  margin-bottom: 1.75rem;
  padding-right: 2rem;
  line-height: 1.8;
}

.blog-detail .content-body :deep(li) {
  margin-bottom: 0.875rem;
  line-height: 1.8;
}

.blog-detail .content-body :deep(li:last-child) {
  margin-bottom: 0;
}

.blog-detail .content-body :deep(blockquote) {
  border-right: 4px solid rgba(var(--v-theme-primary), 0.5);
  padding-right: 1.5rem;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), 0.75);
  line-height: 1.8;
}

.blog-detail .content-body :deep(blockquote p) {
  margin-bottom: 1rem;
}

.blog-detail .content-body :deep(blockquote p:last-child) {
  margin-bottom: 0;
}

.blog-detail .content-body :deep(a) {
  color: rgb(var(--v-theme-primary));
  text-decoration: underline;
  transition: opacity 0.2s ease;
}

.blog-detail .content-body :deep(a:hover) {
  opacity: 0.8;
}

.blog-detail .content-body :deep(code) {
  background-color: rgba(var(--v-theme-on-surface), 0.08);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Courier New', monospace;
}

.blog-detail .content-body :deep(pre) {
  background-color: rgba(var(--v-theme-on-surface), 0.05);
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-top: 1.75rem;
  margin-bottom: 1.75rem;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
}

.blog-detail .content-body :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

/* Comments styling */
.comment-list {
  background-color: transparent;
}

.comment-item {
  border-radius: 16px;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  margin-bottom: 16px;
  padding: 1rem;
}

.comment-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  color: rgba(var(--v-theme-on-surface), 0.87);
  margin-top: 0.5rem;
}

/* Sidebar text improvements */
.v-list-item-title {
  line-height: 1.5;
  font-weight: 500;
}

.v-list-item-subtitle {
  line-height: 1.4;
  color: rgba(var(--v-theme-on-surface), 0.68);
}
</style>

