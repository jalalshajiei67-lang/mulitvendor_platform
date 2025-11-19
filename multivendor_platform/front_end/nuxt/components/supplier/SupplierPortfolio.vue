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
      <div v-if="categories.length > 0" class="category-filter mb-8">
        <v-card elevation="3" class="filter-card" rounded="lg">
          <v-card-text class="pa-4">
            <v-chip-group
              v-model="selectedCategory"
              selected-class="bg-primary text-white"
              mandatory
              class="filter-chips"
            >
              <v-chip
                value="all"
                variant="outlined"
                class="filter-chip"
                prepend-icon="mdi-view-grid"
                size="large"
              >
                همه پروژه‌ها
              </v-chip>
              <v-chip
                v-for="category in categories"
                :key="category"
                :value="category"
                variant="outlined"
                class="filter-chip"
                :prepend-icon="getCategoryIcon(category)"
                size="large"
              >
                {{ category }}
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>
      </div>

      <!-- Loading State -->
      <v-row v-if="loading" justify="center" class="my-8">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-row>

      <!-- Portfolio Grid -->
      <v-row v-else-if="filteredItems.length > 0" class="portfolio-grid">
        <v-col
          v-for="(item, index) in filteredItems"
          :key="item.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          class="portfolio-col"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <v-card
            class="portfolio-card animate-in"
            :class="{ 'featured-card': item.is_featured }"
            elevation="4"
            hover
            @click="openLightbox(item)"
          >
            <!-- Image Container -->
            <div class="image-container">
              <v-badge
                v-if="item.is_featured"
                content="ویژه"
                color="amber"
                floating
                class="featured-badge"
              >
                <v-img
                  :src="formatImageUrl(item.image)"
                  :height="display.xs.value ? 220 : 280"
                  cover
                  class="portfolio-image"
                >
                  <template v-slot:placeholder>
                    <v-skeleton-loader type="image" />
                  </template>

                  <!-- Image Overlay with Actions -->
                  <div class="image-overlay">
                    <div class="overlay-content">
                      <v-btn
                        icon="mdi-magnify-plus"
                        size="large"
                        color="white"
                        variant="text"
                        class="zoom-btn"
                        @click.stop="openLightbox(item)"
                      ></v-btn>
                      <div class="overlay-info">
                        <v-chip
                          v-if="item.category"
                          size="small"
                          color="white"
                          variant="elevated"
                          class="category-overlay-chip"
                        >
                          {{ item.category }}
                        </v-chip>
                      </div>
                    </div>
                  </div>
                </v-img>
              </v-badge>

              <!-- Project Date Badge -->
              <v-chip
                v-if="item.project_date"
                size="small"
                color="rgba(0,0,0,0.7)"
                text-color="white"
                variant="elevated"
                class="date-badge"
              >
                <v-icon start size="x-small">mdi-calendar</v-icon>
                {{ formatDate(item.project_date) }}
              </v-chip>
            </div>

            <!-- Card Content -->
            <v-card-text class="pa-4 portfolio-content">
              <div class="content-header">
                <h3 class="portfolio-title text-h6 font-weight-bold mb-2 line-clamp-2">
                  {{ item.title }}
                </h3>
                <v-btn
                  icon="mdi-magnify-plus"
                  size="small"
                  variant="text"
                  color="primary"
                  class="expand-btn"
                  @click.stop="openLightbox(item)"
                ></v-btn>
              </div>

              <p class="portfolio-description text-body-2 text-medium-emphasis mb-3 line-clamp-3">
                {{ item.description }}
              </p>

              <!-- Project Meta -->
              <div class="project-meta">
                <div class="meta-row">
                  <v-icon size="small" color="primary" class="me-1">mdi-calendar</v-icon>
                  <span class="text-caption">{{ formatDate(item.project_date) }}</span>
                </div>
                <div v-if="item.client_name" class="meta-row">
                  <v-icon size="small" color="secondary" class="me-1">mdi-account</v-icon>
                  <span class="text-caption">{{ item.client_name }}</span>
                </div>
              </div>

              <!-- Tags -->
              <div v-if="item.category" class="portfolio-tags mt-3">
                <v-chip
                  size="x-small"
                  variant="tonal"
                  color="primary"
                  class="category-chip"
                >
                  <v-icon start size="x-small">{{ getCategoryIcon(item.category) }}</v-icon>
                  {{ item.category }}
                </v-chip>
              </div>
            </v-card-text>

            <!-- Hover Effect Indicator -->
            <div class="hover-indicator">
              <v-icon color="primary">mdi-eye</v-icon>
              <span class="text-caption ms-1">مشاهده پروژه</span>
            </div>
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

const getCategoryIcon = (category: string) => {
  const iconMap: Record<string, string> = {
    'طراحی وب': 'mdi-web',
    'طراحی گرافیک': 'mdi-palette',
    'برنامه‌نویسی': 'mdi-code-tags',
    'موبایل': 'mdi-cellphone',
    'بازاریابی': 'mdi-bullhorn',
    'مشاوره': 'mdi-account-tie',
    'آموزش': 'mdi-school',
    'فروش': 'mdi-shopping',
    'ساخت': 'mdi-hammer-wrench',
    'خدمات': 'mdi-account-wrench'
  }
  return iconMap[category] || 'mdi-folder'
}
</script>

<style scoped>
.section-header {
  text-align: center;
}

/* Category Filter */
.category-filter {
  display: flex;
  justify-content: center;
}

.filter-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.95)) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(var(--v-theme-outline), 0.1);
  width: 100%;
}

.filter-chips {
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.filter-chip {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 12px;
  font-weight: 500;
  height: 40px;
}

.filter-chip:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 16px rgba(var(--v-theme-primary), 0.2);
}

.filter-chip.v-chip--selected {
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
  transform: translateY(-2px);
}

/* Portfolio Grid */
.portfolio-grid {
  margin: -12px;
}

.portfolio-grid > .v-col {
  padding: 12px;
}

.portfolio-col {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Portfolio Card */
.portfolio-card {
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  height: 100%;
  background: white;
  border: 1px solid rgba(var(--v-theme-outline), 0.1);
}

.portfolio-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1), rgba(var(--v-theme-secondary, var(--v-theme-primary)), 0.1));
  border-radius: 22px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.portfolio-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.18) !important;
  border-color: rgba(var(--v-theme-primary), 0.3);
}

.portfolio-card:hover::before {
  opacity: 1;
}

.featured-card {
  border: 3px solid rgb(var(--v-theme-amber));
  position: relative;
}

.featured-card::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  background: linear-gradient(135deg, rgb(var(--v-theme-amber)), rgb(var(--v-theme-orange)));
  border-radius: 19px;
  z-index: -1;
  opacity: 0.3;
}

/* Image Container */
.image-container {
  position: relative;
  overflow: hidden;
}

.portfolio-image {
  position: relative;
  transition: transform 0.4s ease;
}

.portfolio-card:hover .portfolio-image {
  transform: scale(1.05);
}

/* Image Overlay */
.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0.5) 50%,
    rgba(0, 0, 0, 0.7) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.4s ease;
  backdrop-filter: blur(2px);
}

.portfolio-card:hover .image-overlay {
  opacity: 1;
}

.overlay-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.zoom-btn {
  background: rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.zoom-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  transform: scale(1.1);
}

.overlay-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.category-overlay-chip {
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Date Badge */
.date-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 2;
}

.featured-badge {
  z-index: 3;
  backdrop-filter: blur(10px);
}

/* Portfolio Content */
.portfolio-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
  backdrop-filter: blur(10px);
  position: relative;
}

.content-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 8px;
}

.portfolio-title {
  color: rgba(var(--v-theme-on-surface), 0.9);
  line-height: 1.4;
  flex: 1;
  margin-right: 8px;
  transition: color 0.3s ease;
}

.portfolio-card:hover .portfolio-title {
  color: rgb(var(--v-theme-primary));
}

.expand-btn {
  flex-shrink: 0;
  opacity: 0.7;
  transition: all 0.3s ease;
}

.portfolio-card:hover .expand-btn {
  opacity: 1;
  transform: scale(1.1);
}

.portfolio-description {
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

/* Project Meta */
.project-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Portfolio Tags */
.portfolio-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.category-chip {
  transition: all 0.3s ease;
}

.category-chip:hover {
  transform: scale(1.05);
}

/* Hover Indicator */
.hover-indicator {
  position: absolute;
  bottom: 16px;
  right: 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 8px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(var(--v-theme-outline), 0.2);
}

.portfolio-card:hover .hover-indicator {
  opacity: 1;
  transform: translateY(0);
}

/* Line Clamping */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animations */
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  animation: slideInUp 0.6s ease-out forwards;
}

@keyframes slideInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile optimizations */
@media (max-width: 960px) {
  .portfolio-grid {
    margin: -8px;
  }

  .portfolio-grid > .v-col {
    padding: 8px;
  }

  .portfolio-card:hover {
    transform: translateY(-8px) scale(1.01);
  }

  .image-overlay {
    opacity: 1;
    background: rgba(0, 0, 0, 0.4);
  }

  .hover-indicator {
    display: none;
  }
}

@media (max-width: 600px) {
  .category-filter {
    padding: 0.5rem;
  }

  .filter-chips {
    flex-wrap: wrap;
    justify-content: center;
  }

  .portfolio-content {
    padding: 12px !important;
  }

  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .portfolio-title {
    margin-right: 0;
  }
}
</style>

