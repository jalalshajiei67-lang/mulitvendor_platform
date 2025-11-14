<template>
  <v-card :elevation="variant === 'featured' ? 4 : 2" rounded="xl" class="blog-card" hover @click="goToPost">
    <div class="image-wrapper">
      <v-img
        v-if="post.featured_image"
        :src="post.featured_image"
        :alt="post.title"
        height="200"
        cover
        loading="lazy"
      >
        <template v-slot:placeholder>
          <div class="d-flex align-center justify-center fill-height">
            <v-skeleton-loader type="image" width="100%" height="100%" />
          </div>
        </template>
      </v-img>
      <div v-else class="no-image">
        <v-icon size="48" color="grey-lighten-1">mdi-image-broken</v-icon>
      </div>
      <v-chip
        v-if="post.is_featured && variant !== 'list'"
        color="accent"
        size="small"
        class="badge"
      >
        {{ t('featured') }}
      </v-chip>
    </div>

    <v-card-text :class="variant === 'list' ? 'pa-6' : 'pa-5'">
      <div class="d-flex gap-3 align-center mb-3 text-caption text-medium-emphasis flex-wrap">
        <span class="d-flex align-center">
          <v-icon size="16" class="ml-1">mdi-account</v-icon>
          {{ post.author_name }}
        </span>
        <span class="d-flex align-center">
          <v-icon size="16" class="ml-1">mdi-calendar</v-icon>
          {{ formatDate(post.created_at) }}
        </span>
        <span class="d-flex align-center">
          <v-icon size="16" class="ml-1">mdi-clock-outline</v-icon>
          {{ post.reading_time }} {{ t('minRead') }}
        </span>
      </div>

      <h3 class="text-h6 text-md-h5 font-weight-bold mb-3">
        {{ post.title }}
      </h3>
      <p class="text-body-2 text-medium-emphasis line-clamp-3">
        {{ post.excerpt }}
      </p>

      <v-divider class="my-4" />

      <div class="d-flex align-center justify-space-between">
        <v-chip
          v-if="post.category_name"
          :style="chipStyle"
          size="small"
          class="font-weight-medium"
        >
          {{ post.category_name }}
        </v-chip>
        <v-btn variant="text" color="primary" @click.stop="goToPost">
          {{ t('view') }}
          <v-icon class="mr-2">mdi-arrow-left</v-icon>
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps<{
  post: Record<string, any>
  variant?: 'grid' | 'list' | 'featured'
}>()

const blogStore = useBlogStore()
const t = blogStore.t

const chipStyle = computed(() => {
  if (!props.post.category_color) {
    return {
      backgroundColor: 'rgba(var(--v-theme-on-surface), 0.04)'
    }
  }

  return {
    backgroundColor: props.post.category_color,
    color: '#fff'
  }
})

const goToPost = () => {
  navigateTo(`/blog/${props.post.slug}`)
}

const formatDate = (value: string) =>
  new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(new Date(value))
</script>

<style scoped>
.blog-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.blog-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(var(--v-theme-on-surface), 0.12);
}

.image-wrapper {
  position: relative;
  overflow: hidden;
  border-top-left-radius: inherit;
  border-top-right-radius: inherit;
}

.no-image {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(var(--v-theme-on-surface), 0.06);
}

.badge {
  position: absolute;
  top: 16px;
  right: 16px;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

