<template>
  <v-card rounded="xl" elevation="2" class="setup-progress-widget" variant="tonal" color="primary">
    <v-card-text class="pa-6">
      <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
        <div>
          <p class="text-caption text-medium-emphasis mb-1">پیشرفت راه‌اندازی</p>
          <h3 class="text-h6 font-weight-bold">راه‌اندازی فروشگاه</h3>
          <p class="text-body-2 text-medium-emphasis">
            {{ stepsCompleted }} از {{ totalSteps }} مرحله انجام شده
          </p>
        </div>
        <v-avatar size="64" color="white" variant="flat">
          <v-icon size="36" color="primary">mdi-rocket-launch</v-icon>
        </v-avatar>
      </div>

      <v-progress-linear
        :model-value="progressPercent"
        height="12"
        rounded
        color="primary"
        class="mb-3"
      />
      <div class="d-flex justify-space-between text-caption text-medium-emphasis mb-4">
        <span>شروع</span>
        <span>{{ Math.round(progressPercent) }}%</span>
        <span>کامل</span>
      </div>

      <v-alert type="info" variant="tonal" rounded="lg" class="mb-4">
        <div class="d-flex align-center gap-2">
          <v-icon color="primary">mdi-information</v-icon>
          <span class="text-body-2">برای ادامه راه‌اندازی، راهنمای تعاملی را از سر بگیرید.</span>
        </div>
      </v-alert>

      <v-btn color="primary" block size="large" prepend-icon="mdi-play-circle" @click="$emit('resume')">
        ادامه راه‌اندازی
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  progressPercent: number
  stepsCompleted: number
  totalSteps: number
}>()

defineEmits<{
  resume: []
}>()
</script>

<style scoped>
.setup-progress-widget {
  min-height: 260px;
}
</style>

