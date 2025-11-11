<template>
  <div class="loading-spinner" :class="{ 'full-screen': fullScreen }">
    <v-progress-circular
      indeterminate
      :color="color"
      :size="size"
      :width="width"
      class="mb-4"
    ></v-progress-circular>
    <p v-if="message" class="text-body-1 text-medium-emphasis">
      {{ message }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message?: string
  color?: string
  size?: number | string
  width?: number | string
  fullScreen?: boolean
}

withDefaults(defineProps<Props>(), {
  message: 'در حال بارگذاری...',
  color: 'primary',
  size: 64,
  width: 4,
  fullScreen: false
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
}
</style>

