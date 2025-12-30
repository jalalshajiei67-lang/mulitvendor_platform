<template>
  <div class="countdown-timer">
    <v-chip
      v-if="!isExpired"
      color="primary"
      variant="tonal"
      size="large"
      class="countdown-chip"
    >
      <v-icon start>mdi-clock-outline</v-icon>
      <span v-if="timeRemaining">
        {{ timeRemaining.days }} روز : {{ timeRemaining.hours }} ساعت : {{ timeRemaining.minutes }} دقیقه
      </span>
      <span v-else>در حال محاسبه...</span>
    </v-chip>
    <v-chip
      v-else
      color="error"
      variant="tonal"
      size="large"
      class="countdown-chip"
    >
      <v-icon start>mdi-clock-alert-outline</v-icon>
      به پایان رسیده
    </v-chip>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Props {
  deadline: string  // ISO datetime string
}

const props = defineProps<Props>()

const now = ref(new Date())
let intervalId: NodeJS.Timeout | null = null

const deadlineDate = computed(() => new Date(props.deadline))

const timeRemaining = computed(() => {
  const diff = deadlineDate.value.getTime() - now.value.getTime()
  
  if (diff <= 0) {
    return null
  }
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  return { days, hours, minutes }
})

const isExpired = computed(() => {
  return deadlineDate.value.getTime() <= now.value.getTime()
})

const updateTime = () => {
  now.value = new Date()
}

onMounted(() => {
  updateTime()
  // Update every 10 seconds
  intervalId = setInterval(updateTime, 10000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.countdown-timer {
  display: flex;
  justify-content: center;
}

.countdown-chip {
  font-weight: 600;
}
</style>

