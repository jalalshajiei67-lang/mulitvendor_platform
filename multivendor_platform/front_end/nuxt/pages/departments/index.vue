<template>
  <div class="departments-page">
    <section class="hero">
      <v-container class="py-10 text-white">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3 text-center">
          {{ t('departments') }}
        </h1>
        <p class="text-subtitle-1 opacity-85 mx-auto max-w-640 text-center">
          سازماندهی کلان محصولات و خدمات در ایندکسو؛ هر دپارتمان به نیاز خاصی پاسخ می‌دهد.
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

    <v-container class="py-8">
      <ListSkeleton
        v-if="loading"
        type="product"
        variant="grid"
        :count="6"
        :cols="12"
        :sm="6"
        :md="6"
        :lg="4"
      />

      <v-alert v-else-if="error" type="error" variant="tonal" class="mb-6">
        {{ error }}
      </v-alert>

      <v-row v-else-if="departments.length" class="ga-4">
        <v-col
          v-for="department in departments"
          :key="department.id"
          cols="12"
          md="6"
          lg="4"
        >
          <v-card
            rounded="xl"
            elevation="3"
            class="department-card"
            hover
            @click="navigateTo(`/departments/${department.slug}`)"
          >
            <v-card-text class="pa-6">
              <v-img
                v-if="formatImageUrl(department)"
                height="200"
                :src="formatImageUrl(department) || ''"
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
                <v-icon size="64" color="primary">mdi-domain</v-icon>
              </div>
              <h2 class="text-h5 font-weight-bold mb-3">{{ department.name }}</h2>
              <div class="d-flex justify-space-between align-center mt-4 text-caption text-medium-emphasis">
                <span>
                  {{ department.category_count || 0 }} دسته‌بندی
                </span>
                <v-icon>mdi-arrow-left</v-icon>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-card v-else elevation="1" rounded="xl" class="pa-10 text-center">
        <v-icon size="56" color="primary" class="mb-4">mdi-office-building</v-icon>
        <h3 class="text-h6 mb-2">{{ t('departments') }}</h3>
        <p class="text-body-2 text-medium-emphasis mb-6">
          هنوز دپارتمانی در سیستم ثبت نشده است.
        </p>
        <v-btn color="primary" @click="fetchPage">تلاش مجدد</v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { formatImageUrl } from '~/utils/imageUtils'
import ListSkeleton from '~/components/skeletons/ListSkeleton.vue'

definePageMeta({
  layout: 'default'
})

useSeoMeta({
  title: 'دپارتمان‌ها',
  description: 'لیست دپارتمان‌های ایندکسو برای ناوبری سریع در حوزه‌های مختلف محصول.',
  ogTitle: 'دپارتمان‌های ایندکسو',
  ogDescription: 'معرفی دپارتمان‌های اصلی بازار چندفروشنده ایندکسو.',
  ogType: 'website'
})

const departmentStore = useDepartmentStore()
const { departments, loading, error } = storeToRefs(departmentStore)
const t = departmentStore.t

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('departments'), disabled: true }
])

const fetchPage = async () => {
  await departmentStore.fetchDepartments({ page_size: 100 })
  return true
}

await useAsyncData('department-list-page', fetchPage)
</script>

<style scoped>
.departments-page {
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

.breadcrumbs-container {
  max-width: 1440px;
  margin: -24px auto 16px;
  padding: 0 16px;
  position: relative;
  z-index: 1;
}

.department-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.department-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 32px rgba(var(--v-theme-on-surface), 0.12);
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

