<template>
  <div class="blog-detail-skeleton">
    <!-- Hero Section Skeleton -->
    <section class="hero-skeleton">
      <v-container class="py-10 py-md-14">
        <v-skeleton-loader
          type="text"
          width="200"
          class="mb-4"
        />
        <v-skeleton-loader
          type="chip"
          width="100"
          class="mb-4"
        />
        <v-skeleton-loader
          type="heading"
          class="mb-4"
        />
        <v-skeleton-loader
          type="text"
          width="80%"
          class="mb-6"
        />
        <div class="d-flex flex-wrap gap-4">
          <v-skeleton-loader
            type="text"
            width="100"
          />
          <v-skeleton-loader
            type="text"
            width="120"
          />
          <v-skeleton-loader
            type="text"
            width="80"
          />
          <v-skeleton-loader
            type="text"
            width="60"
          />
        </div>
      </v-container>
    </section>

    <v-container class="py-10">
      <v-row>
        <!-- Main Content -->
        <v-col cols="12" md="8">
          <v-card elevation="3" rounded="xl" class="pa-6 pa-md-10 mb-10">
            <v-skeleton-loader
              type="image"
              height="420"
              class="rounded-xl mb-8"
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
              class="mb-2"
            />
            <v-skeleton-loader
              type="paragraph"
            />
          </v-card>

          <!-- Comments Section -->
          <section class="mb-12">
            <v-skeleton-loader
              type="heading"
              width="150"
              class="mb-6"
            />
            <v-card elevation="2" rounded="xl" class="pa-6 mb-8">
              <v-skeleton-loader
                type="text"
                height="100"
                class="mb-4"
              />
              <v-skeleton-loader
                type="button"
                width="120"
              />
            </v-card>
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
          </section>
        </v-col>

        <!-- Sidebar -->
        <v-col cols="12" md="4">
          <v-card elevation="2" rounded="xl" class="pa-6 mb-8">
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
              class="mb-2"
            />
            <v-skeleton-loader
              type="list-item-two-line"
            />
          </v-card>

          <v-card elevation="2" rounded="xl" class="pa-6">
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
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
// Blog detail skeleton loader
</script>

<style scoped>
.blog-detail-skeleton {
  min-height: 100vh;
}

.hero-skeleton {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.22), rgba(var(--v-theme-secondary), 0.26));
  border-radius: 24px;
  margin: 16px auto 36px;
  max-width: 1440px;
}
</style>

