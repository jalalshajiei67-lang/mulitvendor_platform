<template>
  <v-dialog
    v-model="show"
    persistent
    max-width="500"
    transition="scale-transition"
  >
    <v-card rounded="xl" elevation="8" class="celebration-card">
      <v-card-text class="pa-8 text-center">
        <!-- Success Icon -->
        <v-avatar
          color="success"
          size="120"
          class="mb-4 celebration-avatar"
        >
          <v-icon size="60" color="white">mdi-check-circle</v-icon>
        </v-avatar>

        <!-- Celebration Message -->
        <h2 class="text-h4 font-weight-bold mb-3">
          آفرین! تمام شد
        </h2>

        <p class="text-h6 text-medium-emphasis mb-6">
          {{ message }}
        </p>

        <!-- Points Badge -->
        <v-chip
          color="primary"
          size="x-large"
          variant="flat"
          class="px-6 mb-6"
        >
          <v-icon start size="28">mdi-star</v-icon>
          <span class="text-h5 font-weight-bold">
            +{{ points }} امتیاز
          </span>
        </v-chip>

        <!-- Close Button -->
        <v-btn
          color="primary"
          size="large"
          block
          rounded="lg"
          elevation="2"
          @click="handleClose"
        >
          <span class="text-h6">ادامه</span>
        </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { watch, ref } from 'vue'
import confetti from 'canvas-confetti'

const props = defineProps<{
  show: boolean
  points: number
  message: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const show = ref(props.show)

// Watch for show prop changes
watch(() => props.show, (newVal) => {
  show.value = newVal
  if (newVal) {
    triggerConfetti()
    // Auto-close after 3 seconds
    setTimeout(() => {
      handleClose()
    }, 3000)
  }
})

const triggerConfetti = () => {
  const duration = 2000
  const animationEnd = Date.now() + duration
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 }

  function randomInRange(min: number, max: number) {
    return Math.random() * (max - min) + min
  }

  const interval: any = setInterval(() => {
    const timeLeft = animationEnd - Date.now()

    if (timeLeft <= 0) {
      return clearInterval(interval)
    }

    const particleCount = 50 * (timeLeft / duration)

    // Confetti burst from multiple origins
    confetti({
      ...defaults,
      particleCount,
      origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 }
    })
    confetti({
      ...defaults,
      particleCount,
      origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 }
    })
  }, 250)
}

const handleClose = () => {
  show.value = false
  emit('close')
}
</script>

<style scoped>
.celebration-card {
  position: relative;
  overflow: hidden;
}

.celebration-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, 
    rgb(var(--v-theme-error)),
    rgb(var(--v-theme-warning)),
    rgb(var(--v-theme-success)),
    rgb(var(--v-theme-info)),
    rgb(var(--v-theme-primary))
  );
}

.celebration-avatar {
  animation: bounce 0.6s ease-in-out;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  25% {
    transform: translateY(-20px) scale(1.1);
  }
  50% {
    transform: translateY(0) scale(0.95);
  }
  75% {
    transform: translateY(-10px) scale(1.05);
  }
}

/* RTL support */
:dir(rtl) .celebration-card {
  direction: rtl;
}
</style>

