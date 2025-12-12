<template>
  <v-card elevation="1" rounded="xl" class="text-center pa-8 empty-state-card">
    <v-icon :size="iconSize" :color="iconColor" class="mb-4">{{ icon }}</v-icon>
    <h3 class="text-h6 mb-2">{{ title }}</h3>
    <p class="text-body-2 text-medium-emphasis mb-6">{{ description }}</p>
    
    <!-- Gamification Context -->
    <div v-if="gamificationContext" class="gamification-context mb-4">
      <v-card
        :color="gamificationContext.color || 'primary'"
        variant="tonal"
        rounded="lg"
        class="pa-4 mb-4"
      >
        <div class="d-flex align-center justify-center gap-2 mb-2">
          <v-icon :color="gamificationContext.color || 'primary'">mdi-star-circle</v-icon>
          <span class="font-weight-bold">{{ gamificationContext.message }}</span>
        </div>
        <p v-if="gamificationContext.subtitle" class="text-caption text-medium-emphasis">
          {{ gamificationContext.subtitle }}
        </p>
      </v-card>
    </div>
    
    <v-btn
      v-if="actionLabel"
      :color="actionColor"
      size="large"
      :prepend-icon="actionIcon"
      @click="$emit('action')"
    >
      {{ actionLabel }}
    </v-btn>
  </v-card>
</template>

<script setup lang="ts">
interface GamificationContext {
  message: string
  subtitle?: string
  color?: string
  points?: number
}

const props = withDefaults(defineProps<{
  icon?: string
  iconSize?: number | string
  iconColor?: string
  title: string
  description: string
  actionLabel?: string
  actionIcon?: string
  actionColor?: string
  gamificationContext?: GamificationContext
}>(), {
  icon: 'mdi-information-outline',
  iconSize: 56,
  iconColor: 'primary',
  actionLabel: '',
  actionIcon: '',
  actionColor: 'primary',
})

defineEmits<{
  action: []
}>()
</script>

<style scoped>
.empty-state-card {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.gamification-context {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}
</style>



