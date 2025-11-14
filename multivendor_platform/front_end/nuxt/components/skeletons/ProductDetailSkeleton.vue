<template>
  <div class="product-detail-skeleton">
    <!-- Hero Section Skeleton -->
    <section class="hero-skeleton">
      <v-container class="py-8">
        <v-skeleton-loader
          type="text"
          width="200"
          class="mb-4"
        />
        <v-skeleton-loader
          type="heading"
          class="mb-3"
        />
        <v-skeleton-loader
          type="text"
          width="80%"
        />
      </v-container>
    </section>

    <v-container class="py-8">
      <v-row>
        <!-- Image Section -->
        <v-col cols="12" md="6">
          <v-sheet elevation="3" rounded="xl" class="pa-4">
            <v-skeleton-loader
              type="image"
              height="420"
              class="rounded-lg mb-4"
            />
            <v-skeleton-loader
              type="image"
              height="80"
              class="rounded-lg"
            />
          </v-sheet>
        </v-col>

        <!-- Info Section -->
        <v-col cols="12" md="6">
          <v-card elevation="3" rounded="xl" class="pa-6 mb-6">
            <div class="d-flex gap-3 mb-4">
              <v-skeleton-loader
                type="chip"
                width="100"
              />
              <v-skeleton-loader
                type="chip"
                width="100"
              />
            </div>
            <v-skeleton-loader
              type="text"
              width="80"
              class="mb-2"
            />
            <v-skeleton-loader
              type="heading"
              class="mb-6"
            />
            <v-skeleton-loader
              type="button"
              height="48"
            />
          </v-card>

          <v-card elevation="1" rounded="xl" class="pa-6">
            <v-skeleton-loader
              type="heading"
              width="200"
              class="mb-4"
            />
            <v-skeleton-loader
              type="list-item-two-line"
              class="mb-2"
            />
            <v-skeleton-loader
              type="list-item-two-line"
              class="mb-2"
            />
            <v-skeleton-loader
              type="list-item-two-line"
            />
          </v-card>
        </v-col>
      </v-row>

      <!-- Description Section -->
      <v-row class="mt-8">
        <v-col cols="12" md="8">
          <v-card elevation="1" rounded="xl" class="pa-6">
            <v-skeleton-loader
              type="heading"
              width="200"
              class="mb-4"
            />
            <v-skeleton-loader
              type="paragraph"
              class="mb-2"
            />
            <v-skeleton-loader
              type="paragraph"
              class="mb-2"
            />
            <v-skeleton-loader
              type="paragraph"
            />
          </v-card>
        </v-col>

        <!-- Related Products -->
        <v-col cols="12" md="4">
          <v-card elevation="1" rounded="xl" class="pa-6">
            <v-skeleton-loader
              type="heading"
              width="150"
              class="mb-4"
            />
            <v-skeleton-loader
              type="list-item-avatar-two-line"
              class="mb-2"
            />
            <v-skeleton-loader
              type="list-item-avatar-two-line"
              class="mb-2"
            />
            <v-skeleton-loader
              type="list-item-avatar-two-line"
            />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
// Product detail skeleton loader
</script>

<style scoped>
.product-detail-skeleton {
  min-height: 100vh;
}

.hero-skeleton {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.2), rgba(var(--v-theme-secondary), 0.2));
  border-radius: 24px;
  margin-top: 12px;
  margin-bottom: 32px;
}
</style>

