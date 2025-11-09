<template>
  <div v-if="department" class="department-detail">
    <section class="hero">
      <v-container class="py-10 text-white">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ department.name }}
        </h1>
        <p class="text-subtitle-1 opacity-90 max-w-720">
          {{ department.description || 'بدون توضیحات تکمیلی برای این دپارتمان.' }}
        </p>
      </v-container>
    </section>

    <v-container class="py-8">
      <section class="mb-12">
        <header class="d-flex align-center justify-space-between mb-4">
          <h2 class="text-h5 font-weight-bold">دسته‌بندی‌های این دپارتمان</h2>
          <v-btn variant="text" color="primary" @click="refreshCategories">
            بروزرسانی
            <v-icon class="mr-2">mdi-refresh</v-icon>
          </v-btn>
        </header>

        <div v-if="catLoading.value" class="text-center py-10">
          <v-progress-circular indeterminate color="primary" size="56" class="mb-4" />
          <p class="text-body-1 text-medium-emphasis">در حال دریافت دسته‌بندی‌ها...</p>
        </div>

        <v-alert v-else-if="catError.value" type="error" variant="tonal">
          {{ catError.value }}
        </v-alert>

        <v-row v-else-if="categories.length" class="ga-4">
          <v-col
            v-for="category in categories"
            :key="category.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card rounded="xl" elevation="2" class="category-card" hover>
              <v-card-text class="pa-6">
                <h3 class="text-h6 font-weight-bold mb-2">{{ category.name }}</h3>
                <p class="text-body-2 text-medium-emphasis line-clamp-3">
                  {{ category.description || 'بدون توضیحات' }}
                </p>
                <v-btn
                  variant="text"
                  color="primary"
                  class="mt-4"
                  @click="navigateTo(`/categories/${category.slug}`)"
                >
                  مشاهده دسته‌بندی
                  <v-icon class="mr-2">mdi-arrow-left</v-icon>
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else elevation="1" rounded="xl" class="pa-8 text-center">
          <v-icon size="48" color="primary" class="mb-3">mdi-folder-outline</v-icon>
          <h3 class="text-subtitle-1 mb-2">دسته‌بندی‌ای یافت نشد</h3>
          <p class="text-body-2 text-medium-emphasis">
            برای این دپارتمان هنوز دسته‌بندی‌ای ثبت نشده است.
          </p>
        </v-card>
      </section>
    </v-container>
  </div>

  <v-container v-else class="py-16 text-center">
    <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
    <p class="text-body-1 text-medium-emphasis">در حال بارگذاری دپارتمان...</p>
  </v-container>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const departmentStore = useDepartmentStore()
const categoryStore = useCategoryStore()

const { currentDepartment } = storeToRefs(departmentStore)
const { categories, loading: catLoading, error: catError } = storeToRefs(categoryStore)
const t = departmentStore.t

const department = computed(() => currentDepartment.value)

const breadcrumbs = computed(() => [
  { title: t('home'), to: '/' },
  { title: t('departments'), to: '/departments' },
  { title: department.value?.name ?? '', disabled: true }
])

const loadDepartment = async () => {
  try {
    await departmentStore.fetchDepartmentBySlug(slug.value)
  } catch (error) {
    await departmentStore.fetchDepartment(slug.value)
  }
}

const refreshCategories = async () => {
  if (!department.value) return
  await categoryStore.fetchCategories({
    department: department.value.id,
    page_size: 100
  })
}

await useAsyncData(`department-detail-${slug.value}`, async () => {
  await loadDepartment()
  await refreshCategories()
})

watch(
  () => route.params.slug,
  async (next, prev) => {
    if (next !== prev) {
      await loadDepartment()
      await refreshCategories()
    }
  }
)

useSeoMeta({
  title: () => department.value?.meta_title ?? department.value?.name ?? 'دپارتمان',
  description: () =>
    department.value?.meta_description ?? department.value?.description ?? '',
  ogTitle: () => department.value?.meta_title ?? department.value?.name ?? '',
  ogDescription: () =>
    department.value?.meta_description ?? department.value?.description ?? '',
  ogType: 'website'
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, rgba(0, 111, 82, 0.9), rgba(0, 197, 142, 0.9));
  color: white;
}

.category-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
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

.max-w-720 {
  max-width: 720px;
}
</style>

