<template>
  <v-app class="app-shell">
    <AppHeader />
    <v-main class="py-6">
      <slot />
    </v-main>
    <AppFooter />
  </v-app>
</template>

<script setup lang="ts">
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

