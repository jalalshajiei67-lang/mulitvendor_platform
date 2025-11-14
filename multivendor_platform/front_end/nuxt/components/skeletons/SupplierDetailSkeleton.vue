<template>
  <div class="supplier-detail-skeleton">
    <!-- Header Section -->
    <v-container fluid class="py-8">
      <v-skeleton-loader
        type="text"
        width="200"
        class="mb-4"
      />
      <v-row>
        <v-col cols="12" md="4">
          <v-skeleton-loader
            type="image"
            height="300"
            class="rounded-lg"
          />
        </v-col>
        <v-col cols="12" md="8">
          <v-skeleton-loader
            type="heading"
            class="mb-4"
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
            type="button"
            width="150"
          />
        </v-col>
      </v-row>
    </v-container>

    <!-- Content Sections -->
    <v-container class="py-8">
      <v-row>
        <v-col cols="12" md="8">
          <v-card elevation="1" rounded="xl" class="pa-6 mb-6">
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
            />
          </v-card>

          <!-- Products Grid -->
          <v-card elevation="1" rounded="xl" class="pa-6">
            <v-skeleton-loader
              type="heading"
              width="200"
              class="mb-4"
            />
            <v-row>
              <v-col
                v-for="i in 6"
                :key="i"
                cols="6"
                sm="4"
                md="3"
              >
                <v-skeleton-loader
                  type="image"
                  height="200"
                  class="rounded-lg"
                />
              </v-col>
            </v-row>
          </v-card>
        </v-col>

        <!-- Sidebar -->
        <v-col cols="12" md="4">
          <v-card elevation="1" rounded="xl" class="pa-6 mb-6">
            <v-skeleton-loader
              type="heading"
              width="150"
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

          <!-- Reviews -->
          <v-card elevation="1" rounded="xl" class="pa-6">
            <v-skeleton-loader
              type="heading"
              width="150"
              class="mb-4"
            />
            <v-skeleton-loader
              type="list-item-avatar-three-line"
              class="mb-2"
            />
            <v-skeleton-loader
              type="list-item-avatar-three-line"
              class="mb-2"
            />
            <v-skeleton-loader
              type="list-item-avatar-three-line"
            />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
// Supplier detail skeleton loader
</script>

<style scoped>
.supplier-detail-skeleton {
  min-height: 100vh;
}
</style>

