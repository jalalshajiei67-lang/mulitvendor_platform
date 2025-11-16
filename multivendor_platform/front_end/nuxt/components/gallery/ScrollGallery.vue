<template>
  <div class="scroll-gallery" dir="rtl">
    <div class="gallery-header" role="status" :aria-label="`تصویر فعال ${safeActiveIndex + 1}`">
      <span class="gallery-title">گالری تصاویر محصول</span>
      <span class="gallery-mode" :class="{ 'is-paused': !isAutoActive }">
        {{ isAutoActive ? 'همگام با اسکرول' : 'کنترل دستی فعال است' }}
      </span>
    </div>

    <div class="main-image" :class="{ 'no-motion': prefersReducedMotion }">
      <Transition name="fade" :duration="prefersReducedMotion ? 0 : 250">
        <v-img
          v-if="activeImage"
          :key="activeImage.src"
          :src="activeImage.src"
          :alt="activeImage.alt"
          cover
          class="hero-image"
          :aspect-ratio="4 / 3"
          loading="lazy"
        >
          <template #placeholder>
            <div class="skeleton" aria-hidden="true"></div>
          </template>
        </v-img>
      </Transition>
    </div>

    <div class="progress" aria-hidden="true">
      <div class="progress-track">
        <div
          class="progress-bar"
          :class="{ 'no-motion': prefersReducedMotion }"
          :style="{ width: progressWidth }"
        ></div>
        <div
          v-for="(image, index) in normalizedImages"
          :key="image.src + index"
          class="progress-stop"
          :style="{ right: `${(index / Math.max(normalizedImages.length - 1, 1)) * 100}%` }"
        ></div>
      </div>
      <div class="progress-label">
        تصویر {{ safeActiveIndex + 1 }} از {{ normalizedImages.length }}
      </div>
    </div>

    <div class="thumbnail-row" role="tablist" aria-label="تصاویر محصولات">
      <button
        v-for="(image, index) in normalizedImages"
        :key="image.src + index"
        type="button"
        class="thumbnail"
        :class="{ active: index === safeActiveIndex }"
        :aria-label="`نمایش تصویر ${index + 1}`"
        :aria-pressed="index === safeActiveIndex"
        role="tab"
        @click="onSelect(index)"
      >
        <img :src="image.src" :alt="image.alt" loading="lazy" />
        <span class="thumb-indicator">{{ index + 1 }}</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { usePrefersReducedMotion } from '@/composables/usePrefersReducedMotion'

type GalleryImage = { src: string; alt?: string; productId?: number }

type Props = {
  images: Array<string | GalleryImage>
  activeIndex: number
  isAutoActive?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'manual-select', index: number): void
}>()

const prefersReducedMotion = usePrefersReducedMotion()

const normalizedImages = computed<GalleryImage[]>(() =>
  props.images.map((item, idx) => {
    if (typeof item === 'string') {
      return { src: item, alt: `تصویر محصول ${idx + 1}` }
    }

    return {
      src: item.src,
      alt: item.alt || `تصویر محصول ${idx + 1}`,
      productId: item.productId
    }
  })
)

const safeActiveIndex = computed(() =>
  Math.min(Math.max(props.activeIndex ?? 0, 0), Math.max(normalizedImages.value.length - 1, 0))
)

const activeImage = computed(() => normalizedImages.value[safeActiveIndex.value])

const progressWidth = computed(() => {
  if (!normalizedImages.value.length) return '0%'

  const percent = ((safeActiveIndex.value + 1) / normalizedImages.value.length) * 100
  return `${percent}%`
})

const preloadImages = () => {
  if (prefersReducedMotion.value) return

  normalizedImages.value.forEach((image) => {
    const preload = new Image()
    preload.src = image.src
  })
}

const onSelect = (index: number) => {
  emit('manual-select', index)
}

onMounted(preloadImages)
</script>

<style scoped>
.scroll-gallery {
  position: sticky;
  top: 72px;
  z-index: 2;
  background: rgba(var(--v-theme-surface), 0.98);
  border-radius: 16px;
  box-shadow: 0 16px 32px rgba(var(--v-theme-on-surface), 0.08);
  padding: 12px;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
}

.gallery-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 12px;
  color: rgba(var(--v-theme-on-surface), 0.86);
}

.gallery-title {
  font-weight: 700;
  font-size: 14px;
}

.gallery-mode {
  font-size: 12px;
  color: rgba(var(--v-theme-on-surface), 0.65);
}

.gallery-mode.is-paused {
  color: rgba(var(--v-theme-warning), 0.9);
}

.main-image {
  border-radius: 14px;
  overflow: hidden;
  position: relative;
  background: rgba(var(--v-theme-on-surface), 0.04);
}

.main-image.no-motion .fade-enter-active,
.main-image.no-motion .fade-leave-active {
  transition: none;
}

.hero-image {
  width: 100%;
  height: 100%;
}

.skeleton {
  width: 100%;
  padding-top: 75%;
  background: linear-gradient(
    90deg,
    rgba(var(--v-theme-on-surface), 0.04),
    rgba(var(--v-theme-on-surface), 0.08),
    rgba(var(--v-theme-on-surface), 0.04)
  );
}

.thumbnail-row {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  margin-top: 12px;
  padding-inline: 4px;
  scrollbar-width: thin;
  direction: rtl;
}

.thumbnail-row::-webkit-scrollbar {
  height: 6px;
}

.thumbnail-row::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.2);
  border-radius: 999px;
}

.thumbnail {
  position: relative;
  border: 1px solid rgba(var(--v-theme-primary), 0.16);
  border-radius: 12px;
  padding: 4px;
  background: rgba(var(--v-theme-surface), 0.96);
  min-width: 72px;
  min-height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.thumbnail.active {
  border-color: rgba(var(--v-theme-primary), 0.6);
  box-shadow: 0 8px 16px rgba(var(--v-theme-primary), 0.12);
}

.thumbnail:focus-visible {
  outline: 2px solid rgba(var(--v-theme-primary), 0.7);
  outline-offset: 2px;
}

.thumb-indicator {
  position: absolute;
  top: 6px;
  left: 6px;
  background: rgba(var(--v-theme-surface), 0.9);
  color: rgba(var(--v-theme-on-surface), 0.8);
  border-radius: 8px;
  padding: 2px 6px;
  font-size: 11px;
  font-weight: 700;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.progress {
  margin-top: 10px;
}

.progress-track {
  position: relative;
  height: 6px;
  background: rgba(var(--v-theme-on-surface), 0.08);
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar {
  position: absolute;
  inset: 0 0 0 auto;
  background: linear-gradient(90deg, rgba(var(--v-theme-primary), 0.7), rgba(var(--v-theme-secondary), 0.6));
  transition: width 0.35s ease;
}

.progress-bar.no-motion {
  transition: none;
}

.progress-stop {
  position: absolute;
  top: 0;
  transform: translateX(50%);
  width: 1px;
  height: 100%;
  background: rgba(var(--v-theme-on-surface), 0.18);
}

.progress-label {
  margin-top: 6px;
  font-size: 12px;
  color: rgba(var(--v-theme-on-surface), 0.72);
  text-align: right;
}

@media (min-width: 960px) {
  .scroll-gallery {
    position: relative;
    top: 0;
  }

  .gallery-title {
    font-size: 15px;
  }
}
</style>
