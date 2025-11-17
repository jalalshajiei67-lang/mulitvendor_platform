<template>
  <div class="subcategories-page">
    <section class="hero">
      <v-container class="py-10 text-white">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0 mb-4">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3 text-center">
          {{ t('subcategories') }}
        </h1>
        <p class="text-subtitle-1 opacity-85 mx-auto max-w-640 text-center">
          زیردسته‌های دقیق‌تر برای هدایت شما به محصولات تخصصی در ایندکسو.
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
        <v-row v-if="subcategories.length" class="g-4">
          <v-col
            v-for="subcategory in subcategories"
            :key="subcategory.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card
              rounded="xl"
              elevation="2"
              class="subcategory-card"
              hover
              @click="navigateTo(`/subcategories/${subcategory.slug}`)"
            >
              <v-card-text class="pa-6">
                <v-img
                  v-if="formatImageUrl(subcategory)"
                  height="200"
                  :src="formatImageUrl(subcategory)"
                  cover
                  class="mb-4 rounded-lg"
                />
                <div v-else class="d-flex align-center justify-center mb-4" style="height: 200px; background: rgba(var(--v-theme-primary), 0.1); border-radius: 8px;">
                  <v-icon size="64" color="primary">mdi-layers-triple</v-icon>
                </div>
                <h2 class="text-h6 font-weight-bold mb-2">
                  {{ subcategory.name }}
                </h2>
                <v-chip
                  v-if="subcategory.category_name"
                  size="small"
                  color="secondary"
                  variant="tonal"
                  class="mt-4"
                >
                  {{ subcategory.category_name }}
                </v-chip>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else elevation="1" rounded="xl" class="pa-10 text-center">
          <v-icon size="56" color="primary" class="mb-4">mdi-layers</v-icon>
          <h3 class="text-h6 mb-2">{{ t('subcategories') }}</h3>
          <p class="text-body-2 text-medium-emphasis mb-6">
            هنوز زیردسته‌ای در سیستم ثبت نشده است.
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
  title: 'زیردسته‌ها',
  description: 'زیردسته‌های موجود در ایندکسو را برای یافتن محصولات تخصصی بررسی کنید.',
  ogTitle: 'زیردسته‌های ایندکسو',
  ogDescription: 'مروری سریع بر زیردسته‌های بازار چندفروشنده ایندکسو.',
  ogType: 'website'
})

const subcategoryStore = useSubcategoryStore()
const { subcategories, loading, error } = storeToRefs(subcategoryStore)
const t = subcategoryStore.t

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('subcategories'), disabled: true }
])

const fetchPage = async () => {
  await subcategoryStore.fetchSubcategories({ page_size: 100 })
  return true
}

await useAsyncData('subcategory-list-page', fetchPage)
</script>

<style scoped>
.subcategories-page {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.85), rgba(var(--v-theme-secondary), 0.9));
  color: rgba(var(--v-theme-on-primary), 0.98);
  border-radius: 24px;
  margin: 16px auto 36px;
  max-width: 1440px;
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

.subcategory-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.subcategory-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(var(--v-theme-on-surface), 0.12);
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

