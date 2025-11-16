<template>
  <v-card ref="cardElement" rounded="xl" elevation="2" class="product-card" hover @click="openProduct">
    <div class="image-wrapper">
      <v-img
        v-if="hasGallery && currentImage"
        :src="currentImage"
        :alt="product.name"
        height="220"
        cover
        loading="lazy"
      >
        <template v-slot:placeholder>
          <div class="d-flex align-center justify-center fill-height">
            <v-skeleton-loader type="image" width="100%" height="100%" />
          </div>
        </template>
      </v-img>
      <div v-else class="no-image">
        <v-icon size="48" color="grey-lighten-1">mdi-cube-outline</v-icon>
      </div>

      <div v-if="hasMultipleImages" class="gallery-nav">
        <v-btn
          size="small"
          variant="tonal"
          class="gallery-arrow gallery-arrow-left"
          color="primary"
          elevation="2"
          :icon="prevArrowIcon"
          aria-label="قبلی"
          @click.stop="prevImage"
        />
        <v-btn
          size="small"
          variant="tonal"
          class="gallery-arrow gallery-arrow-right"
          color="primary"
          elevation="2"
          :icon="nextArrowIcon"
          aria-label="بعدی"
          @click.stop="nextImage"
        />
      </div>

      <!-- Timeline Progress Indicator -->
      <div v-if="hasMultipleImages" class="gallery-timeline">
        <div
          v-for="(image, index) in galleryImages"
          :key="index"
          class="timeline-segment"
        >
          <div
            class="timeline-fill"
            :style="{ width: getSegmentProgress(index) + '%' }"
          ></div>
        </div>
      </div>

      <v-chip
        v-if="product.is_featured"
        size="small"
        color="accent"
        class="badge"
      >
        {{ t('featured') }}
      </v-chip>
    </div>

    <v-card-text class="pa-5">
      <v-chip
        v-if="product.category_name"
        size="small"
        class="mb-3"
        color="primary"
        variant="tonal"
      >
        {{ product.category_name }}
      </v-chip>

      <h3 class="text-h6 font-weight-bold mb-2 line-clamp-2">
        {{ product.name }}
      </h3>
      <p class="text-body-2 text-medium-emphasis line-clamp-2 mb-4">
        {{ product.short_description }}
      </p>

      <div class="d-flex align-center justify-space-between">
        <v-btn color="primary" variant="tonal" prepend-icon="mdi-arrow-right">
          {{ t('view') }}
        </v-btn>
        <div class="text-right">
          <div class="text-caption text-medium-emphasis">{{ t('price') }}</div>
          <div class="text-h6 font-weight-bold">
            {{ product.price ? formatPrice(product.price) : t('contactForPrice') }}
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps<{
  product: Record<string, any>
}>()

const productStore = useProductStore()
const t = productStore.t

// Timeline auto-advance configuration
const SLIDE_DURATION = 4000 // 4 seconds per image
const PROGRESS_INTERVAL = 50 // Update progress every 50ms
const progress = ref(0)
let progressTimer: ReturnType<typeof setInterval> | null = null
let autoAdvanceTimer: ReturnType<typeof setTimeout> | null = null

// Intersection Observer for viewport visibility
const cardElement = ref<HTMLElement | null>(null)
const isVisible = ref(false)
let observer: IntersectionObserver | null = null

const galleryImages = computed(() => {
  const images: string[] = []

  const primary = props.product.primary_image ?? props.product.image
  if (primary) {
    images.push(primary)
  }

  const gallery = Array.isArray(props.product.images) ? props.product.images : []
  gallery.forEach((image) => {
    const url = image?.image_url ?? image?.image
    if (url && !images.includes(url)) {
      images.push(url)
    }
  })

  return images
})

const currentImageIndex = ref(0)

const currentImage = computed(() => galleryImages.value[currentImageIndex.value] ?? galleryImages.value[0] ?? null)

const hasGallery = computed(() => galleryImages.value.length > 0)
const hasMultipleImages = computed(() => galleryImages.value.length > 1)

const isRtl = computed(() => {
  if (typeof window !== 'undefined' && window.document.documentElement) {
    return window.document.documentElement.dir === 'rtl'
  }
  return true
})

const prevArrowIcon = computed(() => (isRtl.value ? 'mdi-chevron-right' : 'mdi-chevron-left'))
const nextArrowIcon = computed(() => (isRtl.value ? 'mdi-chevron-left' : 'mdi-chevron-right'))

const resetImageIndex = (length: number) => {
  if (length === 0) {
    currentImageIndex.value = 0
    return
  }

  if (currentImageIndex.value >= length) {
    currentImageIndex.value = 0
  }
}

watch(
  () => galleryImages.value,
  (images) => {
    resetImageIndex(images.length)
  },
  { immediate: true }
)

const nextImage = () => {
  if (!hasGallery.value) {
    return
  }

  const length = galleryImages.value.length
  currentImageIndex.value = (currentImageIndex.value + 1) % length
  resetProgress()
}

// Timeline auto-advance logic
const startAutoAdvance = () => {
  // Only run on client side and when card is visible
  if (typeof window === 'undefined' || !hasMultipleImages.value || !isVisible.value) {
    return
  }

  stopAutoAdvance()

  // Start progress animation
  progressTimer = window.setInterval(() => {
    progress.value += (PROGRESS_INTERVAL / SLIDE_DURATION) * 100
    if (progress.value >= 100) {
      progress.value = 100
    }
  }, PROGRESS_INTERVAL)

  // Auto-advance to next image
  autoAdvanceTimer = window.setTimeout(() => {
    nextImage()
  }, SLIDE_DURATION)
}

const stopAutoAdvance = () => {
  if (progressTimer) {
    window.clearInterval(progressTimer)
    progressTimer = null
  }
  if (autoAdvanceTimer) {
    window.clearTimeout(autoAdvanceTimer)
    autoAdvanceTimer = null
  }
}

const resetProgress = () => {
  progress.value = 0
  startAutoAdvance()
}

const prevImage = () => {
  if (!hasGallery.value) {
    return
  }

  const length = galleryImages.value.length
  currentImageIndex.value = (currentImageIndex.value - 1 + length) % length
  resetProgress()
}

const getSegmentProgress = (index: number): number => {
  if (index < currentImageIndex.value) {
    return 100 // Completed segments
  } else if (index === currentImageIndex.value) {
    return progress.value // Current segment with progress
  } else {
    return 0 // Future segments
  }
}

// Lifecycle hooks - only run on client
onMounted(async () => {
  // Wait for DOM to be ready
  await nextTick()
  
  // Set up Intersection Observer for viewport visibility
  if (typeof window !== 'undefined' && cardElement.value) {
    // Access the actual DOM element from the Vue component
    const element = (cardElement.value as any)?.$el || cardElement.value
    
    if (element && element instanceof Element) {
      observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            isVisible.value = entry.isIntersecting
            
            if (entry.isIntersecting && hasMultipleImages.value) {
              // Card entered viewport - start animation
              startAutoAdvance()
            } else {
              // Card left viewport - stop animation
              stopAutoAdvance()
            }
          })
        },
        {
          threshold: 0.5, // Trigger when 50% of card is visible
          rootMargin: '50px' // Start slightly before entering viewport
        }
      )
      
      observer.observe(element)
    }
  }

  // Watch for gallery changes only on client
  watch(
    () => hasMultipleImages.value,
    (hasMultiple) => {
      if (hasMultiple && isVisible.value) {
        startAutoAdvance()
      } else {
        stopAutoAdvance()
      }
    }
  )
})

onBeforeUnmount(() => {
  // Clean up observer
  if (observer) {
    observer.disconnect()
    observer = null
  }
  
  stopAutoAdvance()
})

const formatPrice = (value: number | string) => {
  const amount = Number(value)
  if (Number.isNaN(amount)) {
    return value
  }

  return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان'
}

const openProduct = () => {
  navigateTo(`/products/${props.product.slug ?? props.product.id}`)
}
</script>

<style scoped>
.product-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(var(--v-theme-on-surface), 0.12);
}

.image-wrapper {
  position: relative;
  border-top-left-radius: inherit;
  border-top-right-radius: inherit;
  overflow: hidden;
}

.no-image {
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(var(--v-theme-on-surface), 0.06);
}

.badge {
  position: absolute;
  top: 14px;
  right: 14px;
}

.gallery-nav {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  pointer-events: none;
  z-index: 2;
}

.gallery-arrow {
  pointer-events: auto;
  width: 38px;
  height: 38px;
  min-width: 38px;
  border-radius: 50%;
  background-color: rgba(var(--v-theme-surface), 0.92);
  color: rgba(var(--v-theme-on-surface), 0.95);
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.18);
}

.gallery-arrow:hover {
  background-color: rgba(var(--v-theme-surface), 0.98);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

/* Timeline Progress Indicator */
.gallery-timeline {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 4px;
  padding: 8px 12px;
  z-index: 3;
  pointer-events: none;
}

.timeline-segment {
  flex: 1;
  height: 3px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  overflow: hidden;
}

.timeline-fill {
  height: 100%;
  background-color: rgba(255, 255, 255, 0.95);
  transition: width 0.05s linear;
  border-radius: 2px;
}
</style>

