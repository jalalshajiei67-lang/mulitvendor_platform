<template>
  <v-card
    :elevation="variant === 'featured' ? 4 : 2"
    rounded="xl"
    class="blog-card-skeleton"
  >
    <v-skeleton-loader
      type="image"
      :height="variant === 'list' ? 200 : 200"
      class="rounded-t-xl"
    />
    <v-card-text :class="variant === 'list' ? 'pa-6' : 'pa-5'">
      <div class="d-flex gap-3 mb-3">
        <v-skeleton-loader
          type="text"
          width="80"
        />
        <v-skeleton-loader
          type="text"
          width="100"
        />
        <v-skeleton-loader
          type="text"
          width="60"
        />
      </div>
      <v-skeleton-loader
        type="heading"
        class="mb-3"
      />
      <v-skeleton-loader
        type="text"
        class="mb-2"
      />
      <v-skeleton-loader
        type="text"
        width="80%"
        class="mb-4"
      />
      <v-divider class="my-4" />
      <div class="d-flex align-center justify-space-between">
        <v-skeleton-loader
          type="chip"
          width="100"
        />
        <v-skeleton-loader
          type="button"
          width="80"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  variant?: 'grid' | 'list' | 'featured'
}>()
</script>

<style scoped>
.blog-card-skeleton {
  height: 100%;
}
</style>

