<template>
  <div class="departments-page">
    <section class="hero">
      <v-container class="py-10 text-center text-white">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ t('departments') }}
        </h1>
        <p class="text-subtitle-1 opacity-85 mx-auto max-w-640">
          سازماندهی کلان محصولات و خدمات در ایندکسو؛ هر دپارتمان به نیاز خاصی پاسخ می‌دهد.
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
              <v-avatar size="56" class="mb-4 bg-secondary/10 text-secondary">
                <v-icon>mdi-domain</v-icon>
              </v-avatar>
              <h2 class="text-h5 font-weight-bold mb-3">{{ department.name }}</h2>
              <p class="text-body-2 text-medium-emphasis line-clamp-3">
                {{ department.description_plain || 'بدون توضیحات' }}
              </p>
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
  background: linear-gradient(135deg, rgba(var(--v-theme-secondary), 0.3), rgba(var(--v-theme-primary), 0.3));
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

