<template>
  <v-layout class="app-shell d-flex flex-column">
    <AppHeader />
    <v-main class="main-content flex-grow-1">
      <slot />
    </v-main>
    <AppFooter />
  </v-layout>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

useSeoMeta({
  title: 'صفحه اصلی',
  ogLocale: 'fa_IR'
})
</script>
<style scoped>
.app-shell {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>

