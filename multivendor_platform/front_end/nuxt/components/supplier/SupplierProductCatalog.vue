<template>
  <div class="supplier-product-catalog" dir="rtl">
    <v-container>
      <!-- Header with Search and Sort -->
      <div class="catalog-header mb-8">
        <div class="section-header mb-4">
          <h2 class="text-h4 font-weight-bold mb-2">محصولات</h2>
          <p class="text-body-1 text-medium-emphasis">
            مشاهده و خرید محصولات ما
          </p>
        </div>
        <v-card elevation="3" class="filter-card" rounded="lg">
          <v-card-text class="pa-4 pa-md-6">
            <v-row align="center" no-gutters>
              <v-col cols="12" md="7" class="mb-4 mb-md-0 pr-md-4">
                <v-text-field
                  v-model="searchQuery"
                  label="جستجوی محصولات"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  clearable
                  density="comfortable"
                  hide-details
                  class="search-field"
                  rounded="lg"
                >
                  <template v-slot:prepend-inner>
                    <v-icon color="primary" class="me-2">mdi-magnify</v-icon>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" md="5">
                <v-select
                  v-model="sortBy"
                  :items="sortOptions"
                  label="مرتب‌سازی"
                  prepend-inner-icon="mdi-sort"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                  class="sort-field"
                  rounded="lg"
                >
                  <template v-slot:prepend-inner>
                    <v-icon color="primary" class="me-2">mdi-sort</v-icon>
                  </template>
                </v-select>
              </v-col>
            </v-row>
            <v-chip
              v-if="searchQuery"
              color="primary"
              variant="tonal"
              class="mt-4"
              closable
              @click:close="searchQuery = ''"
            >
              نتایج جستجو: "{{ searchQuery }}"
            </v-chip>
          </v-card-text>
        </v-card>
      </div>

      <!-- Loading State -->
      <v-row v-if="loading" justify="center" class="my-8">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-row>

      <!-- Products Grid -->
      <v-row v-else-if="filteredProducts.length > 0" class="product-grid">
        <v-col
          v-for="product in filteredProducts"
          :key="product.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="product-card"
            elevation="4"
            hover
            @click="navigateTo(`/products/${product.slug || product.id}`)"
            @mouseenter="startImageRotation(product.id)"
            @mouseleave="stopImageRotation(product.id)"
          >
            <div class="image-gallery-container">
              <!-- Image Gallery -->
              <div class="image-gallery" :class="{ 'multiple-images': getProductImages(product).length > 1 }">
                <transition-group name="image-fade" tag="div" class="image-stack">
                  <v-img
                    v-for="(image, index) in getProductImages(product)"
                    :key="`${product.id}-${index}`"
                    :src="formatImageUrl(image)"
                    :height="display.xs.value ? 200 : 250"
                    cover
                    class="gallery-image"
                    :class="{ active: activeImageIndex[product.id] === index }"
                    :style="{ zIndex: activeImageIndex[product.id] === index ? 2 : 1 }"
                  >
                    <template v-slot:placeholder>
                      <v-skeleton-loader v-if="index === 0" type="image" />
                    </template>
                  </v-img>
                </transition-group>

                <!-- Timeline Progress Indicator -->
                <div
                  v-if="getProductImages(product).length > 1"
                  class="timeline-progress"
                >
                  <div class="timeline-bar">
                    <div
                      v-for="(image, index) in getProductImages(product)"
                      :key="`progress-${product.id}-${index}`"
                      class="timeline-segment"
                      :class="{
                        active: activeImageIndex[product.id] === index,
                        completed: index < activeImageIndex[product.id]
                      }"
                    >
                      <div
                        class="timeline-fill"
                        :style="{
                          width: activeImageIndex[product.id] === index ? progressWidths[product.id] + '%' : '100%'
                        }"
                      ></div>
                    </div>
                  </div>

                  <!-- Image Indicators -->
                  <div class="image-indicators">
                    <span
                      v-for="(image, index) in getProductImages(product)"
                      :key="`indicator-${product.id}-${index}`"
                      class="image-dot"
                      :class="{
                        active: activeImageIndex[product.id] === index,
                        completed: index < activeImageIndex[product.id]
                      }"
                    ></span>
                  </div>
                </div>
              </div>

              <!-- Featured Badge -->
              <v-chip
                v-if="product.is_featured"
                color="amber"
                size="small"
                class="product-badge"
              >
                ویژه
              </v-chip>

              <!-- Stock Status -->
              <v-chip
                v-if="product.stock <= 0"
                color="error"
                size="small"
                class="stock-badge"
              >
                ناموجود
              </v-chip>

              <!-- Gallery Navigation -->
              <div
                v-if="getProductImages(product).length > 1"
                class="gallery-nav"
              >
                <v-btn
                  icon="mdi-chevron-right"
                  size="small"
                  variant="text"
                  color="white"
                  class="nav-btn prev-btn"
                  @click.stop="previousImage(product.id)"
                ></v-btn>
                <v-btn
                  icon="mdi-chevron-left"
                  size="small"
                  variant="text"
                  color="white"
                  class="nav-btn next-btn"
                  @click.stop="nextImage(product.id)"
                ></v-btn>
              </div>
            </div>

            <v-card-text class="pa-4 product-content">
              <!-- Product Title -->
              <h3 class="product-title text-h6 font-weight-bold mb-2 line-clamp-2">
                {{ product.name }}
              </h3>

              <!-- Product Description (if available) -->
              <p v-if="product.description" class="product-description text-caption text-medium-emphasis mb-3 line-clamp-2">
                {{ stripHtml(product.description) }}
              </p>

              <!-- Price Section -->
              <div class="price-section mb-3">
                <div class="price-container">
                  <span class="price text-h5 font-weight-black text-primary">
                    {{ formatPrice(product.price) }}
                  </span>
                  <span class="currency text-caption text-medium-emphasis">تومان</span>
                </div>
                <v-chip
                  v-if="product.discount_percentage"
                  color="error"
                  size="small"
                  variant="elevated"
                  class="discount-badge"
                >
                  {{ product.discount_percentage }}% تخفیف
                </v-chip>
              </div>

              <!-- Product Meta -->
              <div class="product-meta d-flex align-center justify-space-between mb-3">
                <div class="rating-section d-flex align-center">
                  <div class="rating-stars">
                    <v-rating
                      :model-value="product.rating || 0"
                      readonly
                      density="compact"
                      color="amber"
                      size="small"
                      class="me-1"
                    ></v-rating>
                  </div>
                  <span class="rating-text text-caption text-medium-emphasis">
                    ({{ product.review_count || 0 }})
                  </span>
                </div>
                <div class="stock-info">
                  <v-chip
                    :color="product.stock > 10 ? 'success' : product.stock > 0 ? 'warning' : 'error'"
                    size="small"
                    variant="tonal"
                  >
                    <v-icon start size="x-small">mdi-package-variant</v-icon>
                    {{ product.stock > 10 ? 'موجود' : product.stock > 0 ? `فقط ${product.stock}` : 'ناموجود' }}
                  </v-chip>
                </div>
              </div>

              <!-- Product Tags/Categories -->
              <div v-if="product.category_name" class="product-tags mb-3">
                <v-chip
                  size="x-small"
                  variant="outlined"
                  color="primary"
                  class="category-chip"
                >
                  <v-icon start size="x-small">mdi-tag</v-icon>
                  {{ product.category_name }}
                </v-chip>
              </div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>

            <v-card-actions class="px-4 py-3 action-buttons">
              <div class="action-left">
                <v-btn
                  color="primary"
                  variant="text"
                  size="small"
                  class="details-btn"
                  @click.stop="navigateTo(`/products/${product.slug || product.id}`)"
                >
                  <v-icon start size="small">mdi-eye</v-icon>
                  جزئیات
                </v-btn>
              </div>

              <div class="action-right">
                <v-btn
                  v-if="product.stock > 0"
                  color="primary"
                  variant="flat"
                  size="small"
                  class="add-to-cart-btn"
                  @click.stop="$emit('add-to-cart', product)"
                >
                  <v-icon start size="small">mdi-cart-plus</v-icon>
                  افزودن
                </v-btn>
                <v-btn
                  v-else
                  color="grey"
                  variant="text"
                  size="small"
                  disabled
                  class="notify-btn"
                >
                  <v-icon start size="small">mdi-bell-outline</v-icon>
                  اطلاع‌رسانی
                </v-btn>
              </div>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Empty State -->
      <v-row v-else justify="center" class="my-8">
        <v-col cols="12" class="text-center">
          <v-icon size="80" color="grey-lighten-2">mdi-package-variant-closed</v-icon>
          <h3 class="text-h6 mt-3">محصولی یافت نشد</h3>
          <p class="text-body-2 text-medium-emphasis">
            {{ searchQuery ? 'نتیجه‌ای برای جستجوی شما یافت نشد' : 'هنوز محصولی ثبت نشده است' }}
          </p>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { useDisplay } from 'vuetify'
import { formatImageUrl } from '~/utils/imageUtils'

interface Product {
  id: number
  name: string
  slug?: string
  price: number
  stock: number
  image?: string
  images?: any[]
  rating?: number
  is_featured?: boolean
  description?: string
}

interface Props {
  products: Product[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

defineEmits(['add-to-cart'])

const display = useDisplay()
const searchQuery = ref('')
const sortBy = ref('default')

// Image gallery reactive data
const activeImageIndex = ref<Record<number, number>>({})
const progressWidths = ref<Record<number, number>>({})
const rotationIntervals = ref<Record<number, NodeJS.Timeout>>({})
const IMAGE_ROTATION_DURATION = 3000 // 3 seconds per image

const sortOptions = [
  { title: 'پیش‌فرض', value: 'default' },
  { title: 'جدیدترین', value: 'newest' },
  { title: 'ارزان‌ترین', value: 'price_asc' },
  { title: 'گران‌ترین', value: 'price_desc' },
  { title: 'پرفروش‌ترین', value: 'popular' }
]

const filteredProducts = computed(() => {
  let filtered = [...props.products]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(product =>
      product.name.toLowerCase().includes(query)
    )
  }

  // Sort
  switch (sortBy.value) {
    case 'newest':
      filtered.sort((a, b) => b.id - a.id)
      break
    case 'price_asc':
      filtered.sort((a, b) => a.price - b.price)
      break
    case 'price_desc':
      filtered.sort((a, b) => b.price - a.price)
      break
    case 'popular':
      filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0))
      break
  }

  return filtered
})

const getProductImages = (product: Product) => {
  const images = []

  // Add main image first
  if (product.image) {
    images.push(product.image)
  }

  // Add additional images
  if (product.images && product.images.length > 0) {
    product.images.forEach(img => {
      const imgUrl = typeof img === 'string' ? img : img.image
      if (imgUrl && !images.includes(imgUrl)) {
        images.push(imgUrl)
      }
    })
  }

  // Fallback to placeholder if no images
  if (images.length === 0) {
    images.push('https://via.placeholder.com/250x250?text=No+Image')
  }

  return images
}

const getProductImage = (product: Product) => {
  return getProductImages(product)[0]
}

// Image gallery methods
const startImageRotation = (productId: number) => {
  const images = getProductImages(filteredProducts.value.find(p => p.id === productId))
  if (images.length <= 1) return

  // Initialize if not exists
  if (!(productId in activeImageIndex.value)) {
    activeImageIndex.value[productId] = 0
    progressWidths.value[productId] = 0
  }

  stopImageRotation(productId) // Clear any existing interval

  const rotateImage = () => {
    const currentIndex = activeImageIndex.value[productId] || 0
    const nextIndex = (currentIndex + 1) % images.length

    activeImageIndex.value[productId] = nextIndex
    progressWidths.value[productId] = 0

    // Start progress animation for next image
    let progress = 0
    const progressInterval = setInterval(() => {
      progress += 100 / (IMAGE_ROTATION_DURATION / 50) // Update every 50ms
      if (progress >= 100) {
        progress = 100
        clearInterval(progressInterval)
      }
      progressWidths.value[productId] = progress
    }, 50)
  }

  // Start progress animation for current image
  let progress = 0
  const progressInterval = setInterval(() => {
    progress += 100 / (IMAGE_ROTATION_DURATION / 50)
    if (progress >= 100) {
      progress = 100
      clearInterval(progressInterval)
      rotateImage()
    }
    progressWidths.value[productId] = progress
  }, 50)

  rotationIntervals.value[productId] = progressInterval
}

const stopImageRotation = (productId: number) => {
  if (rotationIntervals.value[productId]) {
    clearInterval(rotationIntervals.value[productId])
    delete rotationIntervals.value[productId]
  }
  // Reset progress
  progressWidths.value[productId] = 0
}

const nextImage = (productId: number) => {
  const images = getProductImages(filteredProducts.value.find(p => p.id === productId))
  if (images.length <= 1) return

  const currentIndex = activeImageIndex.value[productId] || 0
  activeImageIndex.value[productId] = (currentIndex + 1) % images.length
  progressWidths.value[productId] = 0

  // Restart rotation
  stopImageRotation(productId)
  startImageRotation(productId)
}

const previousImage = (productId: number) => {
  const images = getProductImages(filteredProducts.value.find(p => p.id === productId))
  if (images.length <= 1) return

  const currentIndex = activeImageIndex.value[productId] || 0
  activeImageIndex.value[productId] = currentIndex === 0 ? images.length - 1 : currentIndex - 1
  progressWidths.value[productId] = 0

  // Restart rotation
  stopImageRotation(productId)
  startImageRotation(productId)
}

// Cleanup intervals on unmount
onUnmounted(() => {
  Object.keys(rotationIntervals.value).forEach(productId => {
    stopImageRotation(Number(productId))
  })
})

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('fa-IR').format(price)
}

// Helper function to strip HTML tags and get plain text (SSR-safe)
const stripHtml = (html: string): string => {
  if (!html) return ''
  // Remove HTML tags using regex (works in both SSR and client)
  const text = html
    .replace(/<[^>]*>/g, '') // Remove HTML tags
    .replace(/&nbsp;/g, ' ') // Replace &nbsp; with space
    .replace(/&amp;/g, '&') // Replace &amp; with &
    .replace(/&lt;/g, '<') // Replace &lt; with <
    .replace(/&gt;/g, '>') // Replace &gt; with >
    .replace(/&quot;/g, '"') // Replace &quot; with "
    .replace(/&#39;/g, "'") // Replace &#39; with '
    .replace(/&zwnj;/g, '\u200C') // Replace &zwnj; with zero-width non-joiner
    .replace(/\s+/g, ' ') // Replace multiple spaces with single space
    .trim() // Remove leading/trailing whitespace
  return text
}
</script>

<style scoped>
.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

.catalog-header {
  margin-bottom: 2rem;
}

.filter-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.95)) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(var(--v-theme-outline), 0.1);
}

.search-field :deep(.v-field),
.sort-field :deep(.v-field) {
  transition: all 0.3s ease;
}

.search-field :deep(.v-field:hover),
.sort-field :deep(.v-field:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.1);
}

.search-field :deep(.v-field--focused),
.sort-field :deep(.v-field--focused) {
  box-shadow: 0 6px 16px rgba(var(--v-theme-primary), 0.15);
}

.product-grid {
  margin: -8px;
}

.product-grid > .v-col {
  padding: 8px;
}

.product-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15) !important;
}

/* Image Gallery Styles */
.image-gallery-container {
  position: relative;
  overflow: hidden;
  border-radius: 12px 12px 0 0;
}

.image-gallery {
  position: relative;
  width: 100%;
  height: 250px;
}

@media (max-width: 600px) {
  .image-gallery {
    height: 200px;
  }
}

.image-stack {
  position: relative;
  width: 100%;
  height: 100%;
}

.gallery-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.gallery-image.active {
  opacity: 1;
}

.image-fade-enter-active,
.image-fade-leave-active {
  transition: opacity 0.5s ease;
}

.image-fade-enter-from,
.image-fade-leave-to {
  opacity: 0;
}

/* Timeline Progress Indicator */
.timeline-progress {
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
  z-index: 3;
}

.timeline-bar {
  display: flex;
  gap: 2px;
  margin-bottom: 8px;
}

.timeline-segment {
  flex: 1;
  height: 3px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.timeline-segment.active {
  background: rgba(255, 255, 255, 0.6);
}

.timeline-segment.completed {
  background: rgba(76, 175, 80, 0.8);
}

.timeline-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #81c784);
  border-radius: 2px;
  transition: width 0.1s linear;
  box-shadow: 0 0 6px rgba(76, 175, 80, 0.6);
}

.timeline-segment.completed .timeline-fill {
  background: rgba(76, 175, 80, 0.9);
}

/* Image Indicators */
.image-indicators {
  display: flex;
  justify-content: center;
  gap: 6px;
}

.image-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  transition: all 0.3s ease;
}

.image-dot.active {
  background: white;
  transform: scale(1.2);
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

.image-dot.completed {
  background: #4caf50;
}

/* Gallery Navigation */
.gallery-nav {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  padding: 0 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 4;
}

.product-card:hover .gallery-nav {
  opacity: 1;
}

.nav-btn {
  background: rgba(0, 0, 0, 0.5) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: rgba(0, 0, 0, 0.7) !important;
  transform: scale(1.1);
}

.product-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 5;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.stock-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 5;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Enhanced Product Content */
.product-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.9));
  backdrop-filter: blur(10px);
}

.product-title {
  color: rgba(var(--v-theme-on-surface), 0.9);
  line-height: 1.4;
  transition: color 0.3s ease;
}

.product-card:hover .product-title {
  color: rgb(var(--v-theme-primary));
}

.product-description {
  line-height: 1.5;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

/* Price Section */
.price-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.price-container {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-primary-variant, var(--v-theme-primary))));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.25rem !important;
  line-height: 1.2;
}

.currency {
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-weight: 500;
}

.discount-badge {
  animation: pulse-discount 2s infinite;
}

@keyframes pulse-discount {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
  }
}

/* Product Meta */
.product-meta {
  padding: 8px 0;
}

.rating-section {
  gap: 4px;
}

.rating-stars {
  transition: transform 0.3s ease;
}

.product-card:hover .rating-stars {
  transform: scale(1.1);
}

.rating-text {
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.stock-info {
  font-size: 0.75rem;
}

/* Product Tags */
.product-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.category-chip {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  border-color: rgba(var(--v-theme-primary), 0.3);
}

/* Action Buttons */
.action-buttons {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.action-left {
  flex: 1;
}

.action-right {
  flex-shrink: 0;
}

.details-btn {
  transition: all 0.3s ease;
  border-radius: 8px;
}

.details-btn:hover {
  background: rgba(var(--v-theme-primary), 0.1) !important;
  transform: translateX(-2px);
}

.add-to-cart-btn {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-primary-variant, var(--v-theme-primary)))) !important;
  color: white !important;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
}

.add-to-cart-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(var(--v-theme-primary), 0.4);
}

.notify-btn {
  border-radius: 8px;
}

/* Enhanced hover animations */
.product-card {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: visible;
}

.product-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1), rgba(var(--v-theme-secondary, var(--v-theme-primary)), 0.1));
  border-radius: 14px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.product-card:hover::before {
  opacity: 1;
}

.product-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
}

/* Mobile optimizations */
@media (max-width: 600px) {
  .product-content {
    padding: 12px !important;
  }

  .price-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .product-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .action-buttons {
    flex-direction: column;
    gap: 8px;
    padding: 12px !important;
  }

  .action-left,
  .action-right {
    width: 100%;
  }

  .details-btn,
  .add-to-cart-btn,
  .notify-btn {
    width: 100%;
  }
}
</style>

