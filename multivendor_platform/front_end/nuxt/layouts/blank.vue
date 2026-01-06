<template>
  <v-layout class="blank-layout">
    <slot />
  </v-layout>
</template>

<script setup lang="ts">
useSeoMeta({
  title: 'صفحه اصلی',
  ogLocale: 'fa_IR'
})
</script>

<style scoped>
.blank-layout {
  min-height: 100vh;
  width: 100%;
}
</style>

