<template>
  <div class="supplier-portfolio" dir="rtl">
    <v-container>
      <!-- Header -->
      <div class="section-header mb-6">
        <h2 class="text-h4 font-weight-bold">نمونه کارها</h2>
        <p class="text-body-1 text-medium-emphasis mt-2">
          پروژه‌ها و نمونه کارهای موفق ما
        </p>
      </div>

      <!-- Category Filter -->
      <div v-if="categories.length > 0" class="category-filter mb-6">
        <v-chip-group
          v-model="selectedCategory"
          selected-class="text-primary"
          mandatory
        >
          <v-chip value="all" variant="outlined">همه</v-chip>
          <v-chip
            v-for="category in categories"
            :key="category"
            :value="category"
            variant="outlined"
          >
            {{ category }}
          </v-chip>
        </v-chip-group>
      </div>

      <!-- Loading State -->
      <v-row v-if="loading" justify="center" class="my-8">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-row>

      <!-- Portfolio Grid -->
      <v-row v-else-if="filteredItems.length > 0" class="portfolio-grid">
        <v-col
          v-for="item in filteredItems"
          :key="item.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="portfolio-card"
            :class="{ 'featured-card': item.is_featured }"
            elevation="4"
            hover
            @click="openLightbox(item)"
          >
            <v-badge
              v-if="item.is_featured"
              content="ویژه"
              color="amber"
              floating
              class="featured-badge"
            >
              <v-img
                :src="formatImageUrl(item.image)"
                :height="display.xs.value ? 200 : 250"
                cover
                class="portfolio-image"
              >
                <template v-slot:placeholder>
                  <v-skeleton-loader type="image" />
                </template>
                <div class="image-overlay">
                  <v-icon size="large" color="white">mdi-magnify-plus</v-icon>
                </div>
              </v-img>
            </v-badge>
            <v-img
              v-else
              :src="formatImageUrl(item.image)"
              :height="display.xs.value ? 200 : 250"
              cover
              class="portfolio-image"
            >
              <template v-slot:placeholder>
                <v-skeleton-loader type="image" />
              </template>
              <div class="image-overlay">
                <v-icon size="large" color="white">mdi-magnify-plus</v-icon>
              </div>
            </v-img>

            <v-card-text class="pa-3">
              <h3 class="text-subtitle-1 font-weight-bold mb-1">
                {{ item.title }}
              </h3>
              <p class="text-caption text-medium-emphasis line-clamp-2">
                {{ item.description }}
              </p>
              <div class="mt-2 d-flex align-center text-caption">
                <v-icon size="x-small" class="me-1">mdi-calendar</v-icon>
                {{ formatDate(item.project_date) }}
              </div>
              <v-chip
                v-if="item.category"
                size="x-small"
                variant="tonal"
                color="primary"
                class="mt-2"
              >
                {{ item.category }}
              </v-chip>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Empty State -->
      <v-row v-else justify="center" class="my-8">
        <v-col cols="12" class="text-center">
          <v-icon size="80" color="grey-lighten-2">mdi-folder-open</v-icon>
          <h3 class="text-h6 mt-3">نمونه کاری یافت نشد</h3>
          <p class="text-body-2 text-medium-emphasis">
            هنوز هیچ پروژه‌ای به نمایش گذاشته نشده است
          </p>
        </v-col>
      </v-row>
    </v-container>

    <!-- Lightbox Dialog -->
    <v-dialog v-model="lightboxOpen" max-width="900">
      <v-card v-if="selectedItem">
        <v-card-title class="d-flex justify-space-between align-center">
          <span class="text-h6">{{ selectedItem.title }}</span>
          <v-btn icon="mdi-close" variant="text" @click="lightboxOpen = false"></v-btn>
        </v-card-title>
        <v-img
          :src="formatImageUrl(selectedItem.image)"
          max-height="500"
          contain
        ></v-img>
        <v-card-text>
          <p class="text-body-1 mb-3">{{ selectedItem.description }}</p>
          <v-chip v-if="selectedItem.category" size="small" variant="tonal" color="primary" class="me-2">
            {{ selectedItem.category }}
          </v-chip>
          <v-chip v-if="selectedItem.client_name" size="small" variant="tonal" color="secondary">
            <v-icon start size="small">mdi-account</v-icon>
            {{ selectedItem.client_name }}
          </v-chip>
          <div v-if="selectedItem.project_date" class="mt-3 text-caption text-medium-emphasis">
            <v-icon size="small" class="me-1">mdi-calendar</v-icon>
            {{ formatDate(selectedItem.project_date) }}
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useDisplay } from 'vuetify'
import type { SupplierPortfolioItem } from '~/composables/useSupplierPortfolioApi'
import { formatImageUrl } from '~/utils/imageUtils'

interface Props {
  items: SupplierPortfolioItem[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const display = useDisplay()
const selectedCategory = ref('all')
const lightboxOpen = ref(false)
const selectedItem = ref<SupplierPortfolioItem | null>(null)

const categories = computed(() => {
  const cats = new Set(props.items.map(item => item.category).filter(Boolean))
  return Array.from(cats) as string[]
})

const filteredItems = computed(() => {
  if (selectedCategory.value === 'all') {
    return props.items
  }
  return props.items.filter(item => item.category === selectedCategory.value)
})

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long'
  }).format(date)
}

const openLightbox = (item: SupplierPortfolioItem) => {
  selectedItem.value = item
  lightboxOpen.value = true
}
</script>

<style scoped>
.section-header {
  text-align: center;
}

.category-filter {
  display: flex;
  justify-content: center;
}

.portfolio-grid {
  margin: -8px;
}

.portfolio-grid > .v-col {
  padding: 8px;
}

.portfolio-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
}

.portfolio-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15) !important;
}

.featured-card {
  border: 2px solid rgb(var(--v-theme-amber));
}

.portfolio-image {
  position: relative;
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.portfolio-card:hover .image-overlay {
  opacity: 1;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

