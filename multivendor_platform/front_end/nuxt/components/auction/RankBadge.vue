<template>
  <v-chip
    :color="rankColor"
    :variant="variant"
    :size="size"
    class="rank-badge"
  >
    <v-icon v-if="showIcon" start>{{ rankIcon }}</v-icon>
    رتبه {{ rank }}
  </v-chip>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  rank: number | null
  variant?: 'flat' | 'tonal' | 'outlined' | 'text'
  size?: 'small' | 'default' | 'large'
  showIcon?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'tonal',
  size: 'default',
  showIcon: true
})

const rankColor = computed(() => {
  if (!props.rank) return 'grey'
  
  if (props.rank === 1) return 'success'  // Green for 1st
  if (props.rank === 2 || props.rank === 3) return 'warning'  // Amber for 2nd/3rd
  return 'error'  // Red for >3rd
})

const rankIcon = computed(() => {
  if (!props.rank) return 'mdi-help-circle'
  
  if (props.rank === 1) return 'mdi-trophy'
  if (props.rank === 2) return 'mdi-medal'
  if (props.rank === 3) return 'mdi-medal-outline'
  return 'mdi-numeric-' + props.rank
})
</script>

<style scoped>
.rank-badge {
  font-weight: 600;
}
</style>

