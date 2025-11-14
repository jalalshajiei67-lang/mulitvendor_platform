<template>
  <v-card
    elevation="4"
    rounded="lg"
    class="supplier-card-skeleton h-100"
  >
    <v-skeleton-loader
      type="image"
      height="250"
      class="rounded-t-lg"
    />
    <v-card-text class="pa-3 pa-sm-4 pb-2">
      <v-skeleton-loader
        type="heading"
        class="mb-2"
      />
      <v-skeleton-loader
        type="text"
        class="mb-2"
      />
      <v-skeleton-loader
        type="text"
        width="70%"
        class="mb-3"
      />
      <div class="d-flex justify-space-between align-center mt-2 mt-sm-3">
        <v-skeleton-loader
          type="text"
          width="60"
        />
        <v-skeleton-loader
          type="text"
          width="80"
        />
      </div>
      <v-skeleton-loader
        type="chip"
        width="100"
        class="mt-2"
      />
    </v-card-text>
    <v-divider />
    <v-card-actions class="px-3 px-sm-4 py-2 py-sm-3">
      <v-skeleton-loader
        type="button"
        width="120"
      />
      <v-spacer />
      <v-skeleton-loader
        type="button"
        width="40"
      />
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
// Supplier card skeleton loader
</script>

<style scoped>
.supplier-card-skeleton {
  display: flex;
  flex-direction: column;
}

.h-100 {
  height: 100%;
}
</style>

