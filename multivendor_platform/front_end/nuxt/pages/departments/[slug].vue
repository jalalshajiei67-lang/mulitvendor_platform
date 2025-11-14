<template>
  <div v-if="department" class="department-detail">
    <section class="hero">
      <v-container class="py-10">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ department.name }}
        </h1>
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

        <div v-if="catLoading" class="text-center py-10">
          <v-progress-circular indeterminate color="primary" size="56" class="mb-4" />
          <p class="text-body-1 text-medium-emphasis">در حال دریافت دسته‌بندی‌ها...</p>
        </div>

        <v-alert v-else-if="catError" type="error" variant="tonal">
          {{ catError }}
        </v-alert>

        <v-row v-else-if="categories.length" class="ga-4">
          <v-col
            v-for="category in categories"
            :key="category.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card 
              rounded="xl" 
              elevation="2" 
              class="category-card" 
              hover
              @click="navigateTo(`/categories/${category.slug}`)"
            >
              <v-card-text class="pa-6">
                <h3 class="text-h6 font-weight-bold mb-2">{{ category.name }}</h3>
                <div class="d-flex align-center justify-space-between mt-4">
                  <span class="text-primary text-body-2 font-weight-medium">
                    مشاهده دسته‌بندی
                  </span>
                  <v-icon color="primary">mdi-arrow-left</v-icon>
                </div>
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

      <v-card elevation="4" rounded="xl" class="description-card">
        <v-card-title class="d-flex align-center gap-3">
          <v-avatar size="48" class="description-icon" variant="tonal" color="primary">
            <v-icon>mdi-text-account</v-icon>
          </v-avatar>
          <div>
            <h2 class="text-h6 text-md-h5 font-weight-bold mb-1">
              درباره {{ department.name }}
            </h2>
            <p class="text-body-2 text-medium-emphasis mb-0">
              مروری کوتاه بر نقش این دپارتمان در ساختار ایندکسو
            </p>
          </div>
        </v-card-title>
        <v-card-text class="description-text">
          <div
            v-html="department.description_html"
            class="text-body-1"
            data-testid="department-description"
          />
        </v-card-text>
      </v-card>
    </v-container>
  </div>

  <ProductDetailSkeleton v-else />
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
  return true
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
.department-detail {
  min-height: 100vh;
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.24), rgba(var(--v-theme-secondary), 0.28));
  color: rgba(var(--v-theme-on-primary), 0.96);
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.24), transparent 60%);
  pointer-events: none;
}

.category-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  background: rgb(var(--v-theme-surface));
}

.category-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(var(--v-theme-on-surface), 0.12);
}

.category-card :deep(.text-medium-emphasis) {
  color: rgba(var(--v-theme-on-surface), 0.68) !important;
}

.category-card :deep(.text-primary) {
  color: rgb(var(--v-theme-primary)) !important;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.description-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.08);
  margin-top: 16px;
}

.description-text {
  line-height: 2;
}

.description-icon :deep(.v-icon) {
  color: rgb(var(--v-theme-primary));
}
</style>

