<template>
  <v-app>
    <NuxtLoadingIndicator color="primary" />
    <ToastContainer />
    <NuxtPage />
  </v-app>
</template>

<script setup lang="ts">
import ToastContainer from '~/components/common/ToastContainer.vue'
</script>

<style>
/* Page transition animations */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* View transition support */
@view-transition {
  navigation: auto;
}

::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}
</style>
