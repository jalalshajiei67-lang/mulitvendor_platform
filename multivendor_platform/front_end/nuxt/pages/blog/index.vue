<template>
  <div class="blog-list">
    <section class="hero">
      <v-container class="py-12 text-white">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-4 text-center readable-heading">
          {{ t('blog') }}
        </h1>
        <p class="text-subtitle-1 text-md-h5 opacity-90 mx-auto max-w-600 text-center readable-text">
          {{ t('discoverInsights') }}
        </p>
      </v-container>
    </section>

    <v-container class="breadcrumbs-container">
      <v-breadcrumbs :items="breadcrumbs" class="pa-0">
        <template #divider>
          <v-icon>mdi-chevron-left</v-icon>
        </template>
      </v-breadcrumbs>
    </v-container>

    <v-container class="py-6">
      <v-card elevation="2" rounded="xl" class="mb-8">
        <v-container class="py-4 d-flex flex-wrap gap-3 align-center">
          <v-btn
            v-for="category in categories"
            :key="category.id"
            :variant="selectedCategory?.id === category.id ? 'elevated' : 'outlined'"
            :color="selectedCategory?.id === category.id ? 'primary' : 'default'"
            rounded="xl"
            size="small"
            @click="selectCategory(category)"
          >
            {{ category.name }}
          </v-btn>
          <v-btn
            class="ms-auto"
            :variant="!selectedCategory ? 'elevated' : 'outlined'"
            :color="!selectedCategory ? 'primary' : 'default'"
            rounded="xl"
            size="small"
            @click="selectCategory(null)"
          >
            {{ t('allPosts') }}
          </v-btn>
        </v-container>
      </v-card>

      <section v-if="!selectedCategory && featuredPosts.length" class="mb-12">
        <header class="d-flex justify-space-between align-center mb-5">
          <h2 class="text-h4 font-weight-bold mb-0 readable-heading">{{ t('featuredPosts') }}</h2>
          <v-btn variant="text" color="primary" @click="goToFirstFeatured">
            {{ t('view') }}
            <v-icon class="mr-2">mdi-arrow-left</v-icon>
          </v-btn>
        </header>
        <v-row>
          <v-col
            v-for="post in featuredPosts"
            :key="post.id"
            cols="12"
            md="4"
          >
            <BlogCard :post="post" variant="featured" />
          </v-col>
        </v-row>
      </section>

      <section>
        <header class="d-flex flex-column flex-md-row-reverse justify-space-between align-center gap-4 mb-6">
          <h2 class="text-h4 font-weight-bold mb-0 readable-heading">
            {{ selectedCategory ? `${selectedCategory.name} ${t('posts')}` : t('allPosts') }}
          </h2>
          <div class="d-flex gap-2">
            <v-btn
              icon="mdi-view-grid"
              size="small"
              :variant="viewMode === 'grid' ? 'elevated' : 'outlined'"
              :color="viewMode === 'grid' ? 'primary' : undefined"
              @click="viewMode = 'grid'"
            />
            <v-btn
              icon="mdi-view-list"
              size="small"
              :variant="viewMode === 'list' ? 'elevated' : 'outlined'"
              :color="viewMode === 'list' ? 'primary' : undefined"
              @click="viewMode = 'list'"
            />
          </div>
        </header>

        <ListSkeleton
          v-if="loading"
          type="blog"
          :variant="viewMode"
          :count="viewMode === 'grid' ? 6 : 3"
          :cols="viewMode === 'grid' ? 12 : 12"
          :sm="viewMode === 'grid' ? 6 : 12"
          :md="viewMode === 'grid' ? 4 : 12"
          :lg="viewMode === 'grid' ? 4 : 12"
        />

        <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
          {{ error }}
        </v-alert>

        <div v-else>
          <v-row v-if="posts.length" :class="{ 'flex-column': viewMode === 'list' }" class="gap-4">
            <template v-for="post in posts" :key="post.id">
              <v-col
                v-if="viewMode === 'grid'"
                cols="12"
                sm="6"
                lg="4"
              >
                <BlogCard :post="post" />
              </v-col>
              <v-col v-else cols="12">
                <BlogCard :post="post" variant="list" />
              </v-col>
            </template>
          </v-row>

          <v-card v-else elevation="1" rounded="xl" class="pa-10 text-center">
            <v-icon size="56" color="primary" class="mb-4">mdi-notebook</v-icon>
            <h3 class="text-h6 mb-2 readable-heading">{{ t('noBlogPostsAvailable') }}</h3>
            <p class="text-body-2 text-medium-emphasis mb-6 readable-text">
              {{ t('discoverInsights') }}
            </p>
            <v-btn color="primary" @click="fetchInitial">
              {{ t('tryAgain') }}
            </v-btn>
          </v-card>

          <div v-if="pagination.count > posts.length" class="d-flex justify-center mt-8">
            <v-pagination
              v-model="page"
              :length="pageCount"
              :total-visible="5"
              @update:model-value="onPageChange"
            />
          </div>
        </div>
      </section>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import ListSkeleton from '~/components/skeletons/ListSkeleton.vue'

definePageMeta({
  layout: 'default',
  middleware: []
})

useSeoMeta({
  title: 'وبلاگ',
  description: 'آخرین مقالات و تحلیل‌های تخصصی ایندکسو را بررسی کنید.',
  ogTitle: 'وبلاگ ایندکسو',
  ogDescription: 'مطالب آموزشی، خبرها و تحلیل‌های حوزه B2B و چندفروشندگی.',
  ogType: 'website'
})

const blogStore = useBlogStore()
const { posts, categories, featuredPosts, pagination, loading, error } = storeToRefs(blogStore)
const t = blogStore.t

const route = useRoute()
const router = useRouter()

const selectedCategory = ref<any | null>(null)
const viewMode = ref<'grid' | 'list'>('grid')
const page = ref(1)
const pageSize = 12

const pageCount = computed(() => Math.max(1, Math.ceil((pagination.value.count || posts.value.length || 1) / pageSize)))

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('blog'), disabled: true }
])

const applyRouteCategory = async () => {
  const slug = route.query.category
  page.value = 1
  if (typeof slug === 'string' && categories.value.length) {
    const category = categories.value.find((item: any) => item.slug === slug) ?? null
    selectedCategory.value = category
    await blogStore.fetchPosts({
      page: 1,
      page_size: pageSize,
      ...(category ? { category: category.id } : {})
    })
  } else {
    selectedCategory.value = null
    await blogStore.fetchPosts({ page: 1, page_size: pageSize })
  }
}

const fetchInitial = async () => {
  await blogStore.fetchCategories()
  await applyRouteCategory()
  await blogStore.fetchFeaturedPosts()
  return {
    categories: categories.value,
    posts: posts.value,
    featuredPosts: featuredPosts.value
  }
}

await useAsyncData('blog-list-page', fetchInitial)

const onPageChange = async (value: number) => {
  page.value = value
  await blogStore.fetchPosts({ page: value, page_size: pageSize, category: selectedCategory.value?.id })
}

const selectCategory = async (category: any | null) => {
  selectedCategory.value = category
  page.value = 1
  await blogStore.fetchPosts({
    page: 1,
    page_size: pageSize,
    ...(category ? { category: category.id } : {})
  })
  router.replace({
    path: '/blog',
    query: (category?.slug ? { category: category.slug } : {})
  })
}

const goToFirstFeatured = () => {
  if (featuredPosts.value.length) {
    navigateTo(`/blog/${featuredPosts.value[0].slug}`)
  }
}

watch(
  () => route.query.category,
  async () => {
    await applyRouteCategory()
  }
)
</script>

<style scoped>
.blog-list {
  min-height: 100vh;
}

/* Shared container width matching v-container */
.hero,
.breadcrumbs-container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 600px) {
  .hero,
  .breadcrumbs-container {
    max-width: 600px;
  }
}

@media (min-width: 960px) {
  .hero,
  .breadcrumbs-container {
    max-width: 960px;
  }
}

@media (min-width: 1280px) {
  .hero,
  .breadcrumbs-container {
    max-width: 1200px;
  }
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.85), rgba(var(--v-theme-secondary), 0.9));
  color: rgba(var(--v-theme-on-primary), 0.98);
  border-radius: 24px;
  margin-top: 16px;
  margin-bottom: 36px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.28), transparent 60%);
  pointer-events: none;
}

.breadcrumbs-container {
  margin-top: -24px;
  margin-bottom: 16px;
  padding: 0 16px;
  position: relative;
  z-index: 1;
}

.max-w-600 {
  max-width: 600px;
}

/* Typography improvements for readability */
.readable-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.readable-heading {
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: rgba(var(--v-theme-on-surface), 0.96);
}

.readable-heading h1,
.readable-heading h2,
.readable-heading h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
}

/* Section spacing */
section {
  margin-bottom: 2rem;
}

section header {
  margin-bottom: 1.5rem;
}

/* Empty state text */
.v-card .readable-text {
  max-width: 65ch;
  margin: 0 auto;
  text-align: center;
}
</style>

