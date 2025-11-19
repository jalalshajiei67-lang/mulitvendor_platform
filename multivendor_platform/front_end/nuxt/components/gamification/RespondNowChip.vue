<template>
  <v-chip
    class="respond-now-chip"
    :color="color"
    variant="elevated"
    size="large"
    pill
    @click="$emit('click')"
  >
    <v-icon start>mdi-flash</v-icon>
    {{ label }}
  </v-chip>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = withDefaults(defineProps<{ minutesRemaining?: number; color?: string }>(), {
  minutesRemaining: 30,
  color: 'error'
})

const label = computed(() => {
  if (!props.minutesRemaining) return 'همین حالا پاسخ دهید'
  return `برای پاسخ سریع ${props.minutesRemaining} دقیقه فرصت دارید`
})
</script>

<style scoped>
.respond-now-chip {
  cursor: pointer;
  font-weight: 600;
}
</style>
