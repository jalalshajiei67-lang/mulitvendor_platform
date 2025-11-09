<template>
  <div class="categories-page">
    <section class="hero">
      <v-container class="py-10 text-center text-white">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ t('categories') }}
        </h1>
        <p class="text-subtitle-1 opacity-85 mx-auto max-w-640">
          همه دسته‌بندی‌های فعال ایندکسو را مرور کنید و مسیر خرید خود را سریع‌تر پیدا کنید.
        </p>
      </v-container>
    </section>

    <v-container class="py-8">
      <div v-if="loading" class="text-center py-14">
        <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
        <p class="text-body-1 text-medium-emphasis">{{ t('loading') }}</p>
      </div>

      <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
        {{ error }}
      </v-alert>

      <template v-else>
        <v-row v-if="categories.length" class="ga-4">
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
                <v-avatar size="48" class="mb-4 bg-primary/10 text-primary">
                  <v-icon>mdi-shape</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold mb-2">
                  {{ category.name }}
                </h2>
                <p class="text-body-2 text-medium-emphasis line-clamp-3">
                  {{ category.description || 'بدون توضیحات' }}
                </p>
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

const fetchPage = async () => {
  await categoryStore.fetchCategories({ page_size: 100 })
}

await useAsyncData('category-list-page', fetchPage)
</script>

<style scoped>
.categories-page {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, rgba(0, 197, 142, 0.25), rgba(0, 111, 82, 0.25));
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
  overflow: hidden;
}

.max-w-640 {
  max-width: 640px;
}
</style>

