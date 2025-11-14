<template>
  <v-card rounded="xl" elevation="2" class="product-card-skeleton">
    <v-skeleton-loader
      type="image"
      height="220"
      class="rounded-t-xl"
    />
    <v-card-text class="pa-5">
      <v-skeleton-loader
        type="chip"
        class="mb-3"
        width="100"
      />
      <v-skeleton-loader
        type="heading"
        class="mb-2"
      />
      <v-skeleton-loader
        type="text"
        class="mb-4"
      />
      <div class="d-flex align-center justify-space-between">
        <div class="flex-grow-1">
          <v-skeleton-loader
            type="text"
            width="60"
            class="mb-1"
          />
          <v-skeleton-loader
            type="text"
            width="120"
          />
        </div>
        <v-skeleton-loader
          type="button"
          width="80"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
// Product card skeleton loader
</script>

<style scoped>
.product-card-skeleton {
  height: 100%;
}
</style>

