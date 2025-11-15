<template>
  <div class="loading-spinner" :class="{ 'full-screen': fullScreen }">
    <ClientOnly>
      <Vue3Lottie
        :animationLink="animationUrl"
        :height="size"
        :width="size"
        :speed="speed"
        :loop="loop"
        :autoPlay="true"
        class="lottie-animation"
      />
      <template #fallback>
        <v-progress-circular
          indeterminate
          color="primary"
          :size="size"
          class="mb-4"
        ></v-progress-circular>
      </template>
    </ClientOnly>
    <p v-if="message" class="text-body-1 text-medium-emphasis mt-4">
      {{ message }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { Vue3Lottie } from 'vue3-lottie'
import 'vue3-lottie/dist/style.css'

interface Props {
  message?: string
  size?: number | string
  speed?: number
  loop?: boolean
  fullScreen?: boolean
  animationUrl?: string
}

withDefaults(defineProps<Props>(), {
  message: 'در حال بارگذاری...',
  size: 200,
  speed: 1,
  loop: true,
  fullScreen: false,
  animationUrl: '/animations/loading.lottie'
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.loading-spinner.full-screen {
  min-height: 100vh;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(255, 255, 255, 0.95);
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.lottie-animation {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* RTL Support */
[dir="rtl"] .loading-spinner {
  direction: rtl;
}

/* Dark mode support */
.v-theme--dark .loading-spinner.full-screen {
  background-color: rgba(18, 18, 18, 0.95);
}

/* Mobile-first responsive design */
@media (max-width: 768px) {
  .loading-spinner {
    padding: 1.5rem;
  }
  
  .lottie-animation {
    max-width: 100%;
    height: auto;
  }
}
</style>

