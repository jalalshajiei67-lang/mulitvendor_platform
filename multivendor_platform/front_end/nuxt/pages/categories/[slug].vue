<template>
  <div v-if="category" class="category-detail">
    <section class="hero">
      <v-container class="py-10">
        <v-breadcrumbs :items="breadcrumbs" class="text-white pa-0">
          <template #divider>
            <v-icon>mdi-chevron-left</v-icon>
          </template>
        </v-breadcrumbs>
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">
          {{ category.name }}
        </h1>
      </v-container>
    </section>

    <v-container class="py-8">
      <v-row class="mb-6" v-if="category.department_name">
        <v-col cols="12" md="4">
          <v-card elevation="2" rounded="xl" class="pa-6">
            <h2 class="text-subtitle-1 font-weight-bold mb-2">دپارتمان مرتبط</h2>
            <p class="text-body-2 text-medium-emphasis mb-4">
              {{ category.department_name }}
            </p>
            <v-btn
              v-if="category.department_slug"
              color="primary"
              variant="tonal"
              @click="navigateTo(`/departments/${category.department_slug}`)"
            >
              مشاهده دپارتمان
              <v-icon class="mr-2">mdi-arrow-left</v-icon>
            </v-btn>
          </v-card>
        </v-col>
      </v-row>

      <section class="mb-12">
        <header class="d-flex align-center justify-space-between mb-4">
          <h2 class="text-h5 font-weight-bold">زیردسته‌های مرتبط</h2>
          <v-btn variant="text" color="primary" @click="refreshSubcategories">
            بروزرسانی
            <v-icon class="mr-2">mdi-refresh</v-icon>
          </v-btn>
        </header>

        <div v-if="subLoading" class="text-center py-10">
          <v-progress-circular indeterminate color="primary" size="56" class="mb-4" />
          <p class="text-body-1 text-medium-emphasis">در حال دریافت زیردسته‌ها...</p>
        </div>

        <v-alert v-else-if="subError" type="error" variant="tonal">
          {{ subError }}
        </v-alert>

        <v-row v-else-if="subcategories.length" class="ga-4">
          <v-col
            v-for="sub in subcategories"
            :key="sub.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card 
              rounded="xl" 
              elevation="2" 
              class="subcategory-card h-100" 
              hover
              @click="navigateTo(`/subcategories/${sub.slug}`)"
            >
              <v-card-text class="pa-6">
                <h3 class="text-h6 font-weight-bold mb-2">{{ sub.name }}</h3>
                <p class="text-body-2 text-medium-emphasis line-clamp-3">
                  {{ sub.description_plain || 'بدون توضیحات' }}
                </p>
                <div class="d-flex align-center justify-space-between mt-4">
                  <span class="text-primary text-body-2 font-weight-medium">
                    مشاهده محصولات
                  </span>
                  <v-icon color="primary">mdi-arrow-left</v-icon>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else elevation="1" rounded="xl" class="pa-8 text-center">
          <v-icon size="48" color="primary" class="mb-3">mdi-layers-triple-outline</v-icon>
          <h3 class="text-subtitle-1 mb-2">زیردسته‌ای یافت نشد</h3>
          <p class="text-body-2 text-medium-emphasis">
            برای این دسته هنوز زیردسته‌ای ثبت نشده است.
          </p>
        </v-card>
      </section>

      <v-card elevation="4" rounded="xl" class="description-card">
        <v-card-title class="d-flex align-center gap-3">
          <v-avatar size="48" class="description-icon" variant="tonal" color="primary">
            <v-icon>mdi-text-box-edit-outline</v-icon>
          </v-avatar>
          <div>
            <h2 class="text-h6 text-md-h5 font-weight-bold mb-1">
              درباره {{ category.name }}
            </h2>
            <p class="text-body-2 text-medium-emphasis mb-0">
              توضیحاتی کوتاه درباره این دسته‌بندی و کاربردهای آن
            </p>
          </div>
        </v-card-title>
        <v-card-text class="description-text">
          <div
            v-html="category.description_html"
            class="text-body-1"
            data-testid="category-description"
          />
        </v-card-text>
      </v-card>
    </v-container>
  </div>

  <v-container v-else class="py-16 text-center">
    <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
    <p class="text-body-1 text-medium-emphasis">در حال بارگذاری دسته‌بندی...</p>
  </v-container>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()

const { currentCategory } = storeToRefs(categoryStore)
const { subcategories, loading: subLoading, error: subError } = storeToRefs(subcategoryStore)
const t = categoryStore.t

const category = computed(() => currentCategory.value)

type BreadcrumbItem = {
  title: string
  to?: string
  disabled?: boolean
}

const breadcrumbs = computed((): BreadcrumbItem[] => [
  { title: t('home'), to: '/' },
  { title: t('categories'), to: '/categories' },
  { title: category.value?.name ?? '', disabled: true }
])

const loadCategory = async () => {
  await categoryStore.fetchCategoryBySlug(slug.value)
}

const refreshSubcategories = async () => {
  if (!category.value) return
  await subcategoryStore.fetchSubcategories({
    category: category.value.id,
    page_size: 100
  })
}

await useAsyncData(`category-detail-${slug.value}`, async () => {
  await loadCategory()
  await refreshSubcategories()
  return true
})

watch(
  () => route.params.slug,
  async (next, prev) => {
    if (next !== prev) {
      await loadCategory()
      await refreshSubcategories()
    }
  }
)

useSeoMeta({
  title: () => category.value?.meta_title ?? category.value?.name ?? 'دسته‌بندی',
  description: () =>
    category.value?.meta_description ?? category.value?.description ?? '',
  ogTitle: () => category.value?.meta_title ?? category.value?.name ?? '',
  ogDescription: () =>
    category.value?.meta_description ?? category.value?.description ?? '',
  ogType: 'website'
})
</script>

<style scoped>
.category-detail {
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

.subcategory-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  background: rgb(var(--v-theme-surface));
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

.subcategory-card :deep(.text-medium-emphasis) {
  color: rgba(var(--v-theme-on-surface), 0.68) !important;
}

.description-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.08);
  margin-top: 16px;
}

.description-icon :deep(.v-icon) {
  color: rgb(var(--v-theme-primary));
}

.description-text {
  line-height: 2;
}
</style>

