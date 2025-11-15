<template>
  <v-container fluid dir="rtl" class="supplier-list-container">
    <!-- Breadcrumbs -->
    <Breadcrumb :items="breadcrumbItems" />

    <!-- Header Section -->
    <v-row class="page-hero align-center mb-4 mb-md-6" align="center">
      <v-col cols="12" md="6">
        <h1 class="text-h4 text-sm-h3 font-weight-bold readable-heading">
          تامین‌کنندگان
        </h1>
        <p class="text-body-2 text-sm-body-1 text-medium-emphasis mt-2 readable-text">
          لیست تامین‌کنندگان و فروشندگان معتبر
        </p>
      </v-col>
    </v-row>

    <!-- Search Section -->
    <v-card elevation="2" rounded="lg" class="filter-card mb-4 mb-md-6">
      <v-card-text class="pa-3 pa-md-4">
        <v-row dense>
          <v-col cols="12" sm="6" md="6">
            <v-text-field
              v-model="searchQuery"
              label="جستجو در تامین‌کنندگان"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              clearable
              rounded="lg"
              @update:model-value="filterSuppliers"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="6">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              item-title="text"
              item-value="value"
              label="مرتب‌سازی"
              prepend-inner-icon="mdi-sort"
              variant="outlined"
              rounded="lg"
              @update:model-value="filterSuppliers"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <ListSkeleton
      v-if="loading"
      type="supplier"
      variant="grid"
      :count="8"
      :cols="12"
      :sm="6"
      :md="4"
      :lg="3"
    />

    <!-- Error State -->
    <v-alert
      v-else-if="error"
      type="error"
      variant="tonal"
      prominent
      class="my-4"
    >
      <v-row align="center">
        <v-col>
          <div class="text-h6">{{ error }}</div>
          <v-btn
            color="error"
            variant="text"
            prepend-icon="mdi-refresh"
            @click="fetchSuppliers"
            class="mt-2"
          >
            تلاش مجدد
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Suppliers Grid -->
    <v-row v-else-if="filteredSuppliers.length > 0" class="supplier-grid">
      <v-col
        v-for="supplier in filteredSuppliers"
        :key="supplier.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card
          elevation="4"
          rounded="lg"
          hover
          class="supplier-card h-100"
          @click="goToSupplierDetail(supplier.id)"
        >
          <!-- Supplier Logo -->
          <v-img
            :src="getSupplierLogo(supplier)"
            :height="display.xs.value ? 200 : 250"
            cover
            class="cursor-pointer"
            loading="lazy"
          >
            <template v-slot:placeholder>
              <div class="d-flex align-center justify-center fill-height">
                <v-skeleton-loader type="image" width="100%" height="100%" />
              </div>
            </template>
          </v-img>

          <v-card-text class="pa-3 pa-sm-4 pb-2">
            <!-- Supplier Name -->
            <h3 class="text-subtitle-1 text-sm-h6 font-weight-bold mb-2 readable-heading">
              {{ supplier.store_name }}
            </h3>

            <!-- Description -->
            <p class="text-caption text-sm-body-2 text-medium-emphasis mb-2 description-text" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
              {{ supplier.description || 'بدون توضیحات' }}
            </p>

            <!-- Rating and Product Count -->
            <div class="d-flex justify-space-between align-center mt-2 mt-sm-3 meta-text">
              <div class="d-flex align-center">
                <v-icon color="amber" size="small" class="me-1">mdi-star</v-icon>
                <span class="text-body-2 font-weight-bold">{{ supplier.rating_average || 0 }}</span>
              </div>
              <div class="text-caption text-sm-body-2 text-medium-emphasis">
                <v-icon size="small" class="me-1">mdi-package-variant</v-icon>
                {{ supplier.product_count || 0 }} محصول
              </div>
            </div>

            <!-- Contact Info -->
            <div v-if="supplier.contact_phone" class="mt-2">
              <v-chip size="x-small" variant="tonal" color="primary">
                <v-icon start size="x-small">mdi-phone</v-icon>
                {{ supplier.contact_phone }}
              </v-chip>
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <!-- Action Buttons -->
          <v-card-actions class="px-3 px-sm-4 py-2 py-sm-3">
            <v-btn
              color="primary"
              variant="text"
              prepend-icon="mdi-eye"
              :size="display.xs.value ? 'x-small' : 'small'"
              @click.stop="goToSupplierDetail(supplier.id)"
            >
              مشاهده جزئیات
            </v-btn>

            <v-spacer></v-spacer>

            <v-btn
              v-if="supplier.website"
              color="secondary"
              variant="text"
              icon="mdi-web"
              :size="display.xs.value ? 'x-small' : 'small'"
              :href="supplier.website"
              target="_blank"
              @click.stop
            ></v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <v-row v-else justify="center" class="my-8 my-md-16">
      <v-col cols="12" class="text-center px-4">
        <v-icon :size="display.xs.value ? 80 : 120" color="grey-lighten-2">mdi-store-off</v-icon>
        <h3 class="text-h6 text-sm-h5 font-weight-bold mt-3 mt-sm-4 readable-heading">تامین‌کننده‌ای یافت نشد</h3>
        <p class="text-body-2 text-sm-body-1 text-medium-emphasis mt-2 readable-text">هیچ تامین‌کننده‌ای در حال حاضر موجود نیست</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
import { useSupplierApi, type Supplier } from '~/composables/useSupplierApi'
import { formatImageUrl } from '~/utils/imageUtils'

useHead({
  title: 'تامین‌کنندگان',
  meta: [
    {
      name: 'description',
      content: 'لیست تامین‌کنندگان و فروشندگان معتبر ماشین‌آلات صنعتی'
    }
  ]
})

const display = useDisplay()
const supplierApi = useSupplierApi()

const suppliers = ref<Supplier[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const sortBy = ref('store_name')

const breadcrumbItems = computed(() => [
  { text: 'خانه', to: '/' },
  { text: 'تامین‌کنندگان', to: null }
])

const sortOptions = computed(() => [
  { text: 'نام (الف تا ی)', value: 'store_name' },
  { text: 'نام (ی تا الف)', value: '-store_name' },
  { text: 'بیشترین امتیاز', value: '-rating_average' },
  { text: 'بیشترین محصولات', value: '-product_count' },
  { text: 'جدیدترین', value: '-created_at' },
  { text: 'قدیمی‌ترین', value: 'created_at' }
])

const filteredSuppliers = computed(() => {
  let filtered = [...suppliers.value]

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(supplier =>
      supplier.store_name.toLowerCase().includes(query) ||
      (supplier.description && supplier.description.toLowerCase().includes(query)) ||
      (supplier.contact_email && supplier.contact_email.toLowerCase().includes(query))
    )
  }

  // Sort
  if (sortBy.value) {
    const isDescending = sortBy.value.startsWith('-')
    const sortKey = isDescending ? sortBy.value.substring(1) : sortBy.value

    filtered.sort((a, b) => {
      let aValue: any = a[sortKey as keyof Supplier] || 0
      let bValue: any = b[sortKey as keyof Supplier] || 0

      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase()
        bValue = bValue.toLowerCase()
      }

      if (isDescending) {
        return bValue > aValue ? 1 : -1
      } else {
        return aValue > bValue ? 1 : -1
      }
    })
  }

  return filtered
})

const getSupplierLogo = (supplier: Supplier) => {
  if (supplier.logo) {
    const formattedUrl = formatImageUrl(supplier.logo)
    if (formattedUrl) return formattedUrl
  }
  return 'https://via.placeholder.com/250x250?text=No+Logo'
}

const fetchSuppliers = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await supplierApi.getSuppliers()
    suppliers.value = response
  } catch (err: any) {
    console.error('Error fetching suppliers:', err)
    error.value = 'خطا در بارگذاری تامین‌کنندگان. لطفاً دوباره تلاش کنید.'
  } finally {
    loading.value = false
  }
}

const filterSuppliers = () => {
  // Filtering is handled by computed property
}

const goToSupplierDetail = (supplierId: number) => {
  navigateTo(`/suppliers/${supplierId}`)
}

onMounted(() => {
  fetchSuppliers()
})
</script>

<style scoped>
.supplier-list-container {
  min-height: 100vh;
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
  padding-bottom: 80px;
  max-width: 100%;
  padding-left: 16px;
  padding-right: 16px;
}

@media (min-width: 960px) {
  .supplier-list-container {
    max-width: 100%;
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (min-width: 1280px) {
  .supplier-list-container {
    max-width: 1600px;
    margin: 0 auto;
    padding-left: 32px;
    padding-right: 32px;
  }
}

@media (min-width: 1920px) {
  .supplier-list-container {
    max-width: 1800px;
    margin: 0 auto;
    padding-left: 40px;
    padding-right: 40px;
  }
}

.page-hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.22), rgba(var(--v-theme-secondary), 0.28));
  border-radius: 24px;
  padding: 48px 32px;
  margin-top: 12px;
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
}

.page-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.28), transparent 60%);
  pointer-events: none;
}

.page-hero h1 {
  color: rgba(var(--v-theme-on-primary), 0.98);
}

.page-hero p {
  color: rgba(var(--v-theme-on-primary), 0.9);
}

.filter-card {
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.08);
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
}

.filter-card :deep(.v-field__input) {
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.filter-card :deep(.v-field__label) {
  color: rgba(var(--v-theme-on-surface), 0.72);
}

.filter-card :deep(.v-field__input::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.56);
}

.supplier-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  background: rgb(var(--v-theme-surface));
  display: flex;
  flex-direction: column;
}

.supplier-card :deep(.v-card-text) {
  flex: 1;
}

.supplier-card h3 {
  color: rgba(var(--v-theme-on-surface), 0.96);
}

.supplier-card p {
  color: rgba(var(--v-theme-on-surface), 0.68);
}

.supplier-card :deep(.v-card-actions) {
  background-color: rgba(var(--v-theme-primary), 0.04);
}

.supplier-card :deep(.v-chip) {
  background-color: rgba(var(--v-theme-primary), 0.12);
  color: rgb(var(--v-theme-primary));
  font-weight: 600;
}

.supplier-card :deep(.v-icon) {
  color: rgba(var(--v-theme-on-surface), 0.7);
}

.supplier-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 22px 45px rgba(15, 23, 42, 0.12) !important;
  border-color: rgba(var(--v-theme-primary), 0.2);
}

@media (max-width: 600px) {
  .supplier-card:hover {
    transform: translateY(-4px);
  }
}

.cursor-pointer {
  cursor: pointer;
}

.h-100 {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.supplier-grid {
  margin: -8px;
}

.supplier-grid > .v-col {
  padding: 8px;
}

@media (min-width: 600px) {
  .supplier-grid {
    margin: -12px;
  }

  .supplier-grid > .v-col {
    padding: 12px;
  }
}

/* Typography improvements */
.readable-heading {
  line-height: 1.4;
  letter-spacing: -0.01em;
  color: rgba(var(--v-theme-on-surface), 0.96);
}

.readable-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.meta-text {
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.72);
  font-size: 0.875rem;
}

.description-text {
  line-height: 1.75;
  word-spacing: 0.1em;
  letter-spacing: 0.01em;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.supplier-card h3 {
  line-height: 1.4;
}

.supplier-card p {
  line-height: 1.75;
}
</style>

