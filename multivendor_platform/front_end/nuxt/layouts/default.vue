<template>
  <v-layout class="app-shell d-flex flex-column">
    <AppHeader />
    <v-main class="main-content flex-grow-1">
      <slot />
    </v-main>
    <AppFooter />
    
    <!-- Chat Widget - Available site-wide -->
    <ChatWidget />
    
    <!-- PWA Components -->
    <PwaInstallPrompt />
    <PwaUpdateAvailable />
  </v-layout>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ChatWidget from '@/components/chat/ChatWidget.vue'
import PwaInstallPrompt from '@/components/pwa/InstallPrompt.vue'
import PwaUpdateAvailable from '@/components/pwa/UpdateAvailable.vue'

useSeoMeta({
  title: 'صفحه اصلی',
  ogLocale: 'fa_IR'
})
</script>
<style scoped>
.app-shell {
  min-height: 100vh;
  background-color: rgb(var(--v-theme-background));
}
</style>

