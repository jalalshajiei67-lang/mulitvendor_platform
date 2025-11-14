<template>
  <div class="categories-page">
    <section class="hero">
      <v-container class="py-10 text-white">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0 mb-4">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3 text-center">
          {{ t('categories') }}
        </h1>
        <p class="text-subtitle-1 opacity-85 mx-auto max-w-640 text-center">
          همه دسته‌بندی‌های فعال ایندکسو را مرور کنید و مسیر خرید خود را سریع‌تر پیدا کنید.
        </p>
      </v-container>
    </section>

    <v-container class="py-8">
      <ListSkeleton
        v-if="loading"
        type="product"
        variant="grid"
        :count="8"
        :cols="12"
        :sm="6"
        :md="4"
        :lg="3"
      />

      <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
        {{ error }}
      </v-alert>

      <template v-else>
        <v-row v-if="categories.length" class="g-4">
          <v-col
            v-for="category in categories"
            :key="category.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card
              rounded="xl"
              elevation="2"
              class="category-card"
              hover
              @click="navigateTo(`/categories/${category.slug}`)"
            >
              <v-card-text class="pa-6">
              <v-img
                v-if="formatImageUrl(category)"
                height="200"
                :src="formatImageUrl(category) || ''"
                cover
                class="mb-4 rounded-lg"
                loading="lazy"
              >
                <template v-slot:placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <v-skeleton-loader type="image" width="100%" height="100%" />
                  </div>
                </template>
              </v-img>
              <div v-else class="d-flex align-center justify-center mb-4" style="height: 200px; background: rgba(var(--v-theme-primary), 0.1); border-radius: 8px;">
                <v-icon size="64" color="primary">mdi-shape</v-icon>
              </div>
                <h2 class="text-h6 font-weight-bold mb-2">
                  {{ category.name }}
                </h2>
                <v-chip
                  v-if="category.department_name"
                  size="small"
                  color="secondary"
                  variant="tonal"
                  class="mt-4"
                >
                  {{ category.department_name }}
                </v-chip>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else elevation="1" rounded="xl" class="pa-10 text-center">
          <v-icon size="56" color="primary" class="mb-4">mdi-folder-outline</v-icon>
          <h3 class="text-h6 mb-2">{{ t('categories') }}</h3>
          <p class="text-body-2 text-medium-emphasis mb-6">
            هنوز دسته‌بندی فعالی وجود ندارد. لطفاً بعداً دوباره بررسی کنید.
          </p>
          <v-btn color="primary" @click="fetchPage">{{ t('tryDifferentFilters') }}</v-btn>
        </v-card>
      </template>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { formatImageUrl } from '~/utils/imageUtils'

definePageMeta({
  layout: 'default'
})

useSeoMeta({
  title: 'دسته‌بندی‌ها',
  description: 'فهرست همه دسته‌بندی‌های ایندکسو برای کشف سریع محصولات و تأمین‌کنندگان.',
  ogTitle: 'دسته‌بندی‌های ایندکسو',
  ogDescription: 'مرور دسته‌بندی‌های فعال بازار چندفروشنده ایندکسو.',
  ogType: 'website'
})

const categoryStore = useCategoryStore()
const { categories, loading, error } = storeToRefs(categoryStore)
const t = categoryStore.t

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('categories'), disabled: true }
])

const fetchPage = async () => {
  await categoryStore.fetchCategories({ page_size: 100 })
  return true
}

await useAsyncData('category-list-page', fetchPage)
</script>

<style scoped>
.categories-page {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.25), rgba(var(--v-theme-secondary), 0.25));
  border-radius: 24px;
  margin-top: 12px;
  margin-bottom: 32px;
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

.category-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.category-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-clamp: 3;
  overflow: hidden;
}

.max-w-640 {
  max-width: 640px;
}
</style>

