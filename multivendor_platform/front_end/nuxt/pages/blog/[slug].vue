<template>
  <div v-if="post" class="blog-detail">
    <section class="hero" :style="heroStyle">
      <v-container class="py-10 py-md-14">
        <div class="text-white">
          <v-chip v-if="post.category_name" class="mb-4" size="small" color="rgba(255,255,255,0.24)">
            {{ post.category_name }}
          </v-chip>
          <h1 class="text-h3 text-md-h1 font-weight-bold mb-4">
            {{ post.title }}
          </h1>
          <p class="text-body-1 text-md-h5 opacity-90">
            {{ post.excerpt }}
          </p>

          <div class="d-flex flex-wrap gap-4 mt-6 text-body-2 text-md-subtitle-2">
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
            />
            <article class="content" v-html="post.content" />
          </v-card>

          <section class="mb-12">
            <div class="d-flex align-center justify-space-between mb-6">
              <h2 class="text-h5 font-weight-bold">{{ t('comments') }}</h2>
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
                <v-list-item-subtitle class="text-caption text-medium-emphasis mb-3">
                  {{ formatDate(comment.created_at) }}
                </v-list-item-subtitle>
                <div class="text-body-2">
                  {{ comment.content }}
                </div>
              </v-list-item>
            </v-list>
          </section>
        </v-col>

        <v-col cols="12" md="4">
          <v-card elevation="2" rounded="xl" class="pa-6 mb-8">
            <h3 class="text-subtitle-1 font-weight-bold mb-4">{{ t('recentPosts') }}</h3>
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
            <h3 class="text-subtitle-1 font-weight-bold mb-4">{{ t('relatedPosts') }}</h3>
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

  <v-container v-else class="py-16 text-center">
    <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
    <p class="text-body-1 text-medium-emphasis">{{ t('loadingPost') }}</p>
  </v-container>
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

const heroStyle = computed(() => {
  const gradient = post.value?.category_color
    ? `linear-gradient(135deg, ${post.value.category_color}, rgba(0,0,0,0.45))`
    : 'linear-gradient(135deg, rgba(0, 197, 142, 0.9), rgba(0, 111, 82, 0.9))'

  return {
    background: gradient
  }
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
  color: white;
}

.blog-detail .content :deep(img) {
  max-width: 100%;
  border-radius: 16px;
  margin: 2rem 0;
}

.blog-detail .content :deep(h2),
.blog-detail .content :deep(h3),
.blog-detail .content :deep(h4) {
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.blog-detail .content :deep(p) {
  line-height: 2.2;
  margin-bottom: 1rem;
  color: #424242;
  font-size: 1.05rem;
}

.comment-list {
  background-color: transparent;
}

.comment-item {
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 16px;
}
</style>

