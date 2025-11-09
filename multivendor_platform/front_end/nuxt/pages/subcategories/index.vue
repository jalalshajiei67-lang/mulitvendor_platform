<template>
  <div class="subcategories-page">
    <section class="hero">
      <v-container class="py-10 text-center text-white">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ t('subcategories') }}
        </h1>
        <p class="text-subtitle-1 opacity-85 mx-auto max-w-640">
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
        <v-row v-if="subcategories.length" class="ga-4">
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
                <v-avatar size="48" class="mb-4 bg-primary/10 text-primary">
                  <v-icon>mdi-layers-triple</v-icon>
                </v-avatar>
                <h2 class="text-h6 font-weight-bold mb-2">
                  {{ subcategory.name }}
                </h2>
                <p class="text-body-2 text-medium-emphasis line-clamp-3">
                  {{ subcategory.description || 'بدون توضیحات' }}
                </p>
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

const fetchPage = async () => {
  await subcategoryStore.fetchSubcategories({ page_size: 100 })
}

await useAsyncData('subcategory-list-page', fetchPage)
</script>

<style scoped>
.subcategories-page {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, rgba(0, 197, 142, 0.25), rgba(0, 111, 82, 0.25));
}

.subcategory-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.subcategory-card:hover {
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

