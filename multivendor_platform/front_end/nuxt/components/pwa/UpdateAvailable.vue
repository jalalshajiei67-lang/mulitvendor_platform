<template>
  <v-snackbar
    v-model="showUpdate"
    :timeout="-1"
    location="bottom"
    color="info"
    class="update-available-snackbar"
  >
    <div class="d-flex align-center ga-3">
      <v-icon color="white">mdi-update</v-icon>
      <div class="flex-grow-1">
        <div class="text-subtitle-1 font-weight-bold">نسخه جدید در دسترس است</div>
        <div class="text-caption">برای دریافت آخرین به‌روزرسانی‌ها، صفحه را بارگذاری مجدد کنید</div>
      </div>
      <v-btn
        color="white"
        variant="flat"
        size="small"
        @click="updateApp"
        :loading="updating"
      >
        به‌روزرسانی
      </v-btn>
      <v-btn
        icon
        variant="text"
        size="small"
        @click="dismissUpdate"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>
  </v-snackbar>
</template>

<script setup lang="ts">
const { $pwa } = useNuxtApp()

const showUpdate = ref(false)
const updating = ref(false)

const updateApp = async () => {
  updating.value = true

  try {
    if ($pwa && 'updateServiceWorker' in $pwa && typeof $pwa.updateServiceWorker === 'function') {
      await $pwa.updateServiceWorker(true)
    } else if ($pwa && 'refresh' in $pwa && typeof $pwa.refresh === 'function') {
      await $pwa.refresh()
    } else {
      // Fallback: reload the page
      if (typeof window !== 'undefined') {
        window.location.reload()
      }
    }
  } catch (error) {
    console.error('Error updating app:', error)
    // Fallback: reload the page
    if (typeof window !== 'undefined') {
      window.location.reload()
    }
  } finally {
    updating.value = false
  }
}

const dismissUpdate = () => {
  showUpdate.value = false
}

const checkForUpdates = () => {
  if (!$pwa) {
    return
  }

  // Listen for service worker updates
  if ('needRefresh' in $pwa && $pwa.needRefresh) {
    showUpdate.value = true
  }

  // Also listen for the update event
  if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      showUpdate.value = true
    })
  }
}

onMounted(() => {
  if (typeof window === 'undefined') {
    return
  }

  checkForUpdates()

  // Check periodically for updates
  const interval = setInterval(() => {
    checkForUpdates()
  }, 60000) // Check every minute

  onUnmounted(() => {
    clearInterval(interval)
  })
})

// Watch for PWA update events
watch(() => {
  if ($pwa && 'needRefresh' in $pwa) {
    return $pwa.needRefresh
  }
  return false
}, (needRefresh) => {
  if (needRefresh) {
    showUpdate.value = true
  }
})
</script>

<style scoped>
.update-available-snackbar {
  z-index: 9998;
}
</style>

