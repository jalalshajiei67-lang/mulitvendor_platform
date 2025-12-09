<template>
  <v-snackbar
    v-model="showPrompt"
    :timeout="-1"
    location="bottom"
    color="primary"
    class="install-prompt-snackbar"
  >
    <div class="d-flex align-center ga-3">
      <v-icon color="white">mdi-download</v-icon>
      <div class="flex-grow-1">
        <div class="text-subtitle-1 font-weight-bold">ایندکسو را نصب کنید</div>
        <div class="text-caption">برای دسترسی سریع‌تر و تجربه بهتر</div>
      </div>
      <v-btn
        color="white"
        variant="flat"
        size="small"
        @click="installApp"
        :loading="installing"
      >
        نصب
      </v-btn>
      <v-btn
        icon
        variant="text"
        size="small"
        @click="dismissPrompt"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>
  </v-snackbar>
</template>

<script setup lang="ts">
interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

const { $pwa } = useNuxtApp()

const showPrompt = ref(false)
const installing = ref(false)
const deferredPrompt = ref<BeforeInstallPromptEvent | null>(null)

const installApp = async () => {
  if (!deferredPrompt.value) {
    return
  }

  installing.value = true

  try {
    // Show the install prompt
    deferredPrompt.value.prompt()

    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.value.userChoice

    if (outcome === 'accepted') {
      console.log('User accepted the install prompt')
    } else {
      console.log('User dismissed the install prompt')
    }
  } catch (error) {
    console.error('Error installing app:', error)
  } finally {
    deferredPrompt.value = null
    showPrompt.value = false
    installing.value = false
  }
}

const dismissPrompt = () => {
  showPrompt.value = false
  // Store dismissal in localStorage to avoid showing again for a while
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('pwa-install-dismissed', Date.now().toString())
  }
}

const checkIfDismissed = () => {
  if (typeof window === 'undefined' || !window.localStorage) {
    return false
  }
  const dismissed = localStorage.getItem('pwa-install-dismissed')
  if (dismissed) {
    const dismissedTime = parseInt(dismissed, 10)
    const daysSinceDismissed = (Date.now() - dismissedTime) / (1000 * 60 * 60 * 24)
    // Show again after 7 days
    return daysSinceDismissed < 7
  }
  return false
}

const handleBeforeInstallPrompt = (e: Event) => {
  // Prevent the mini-infobar from appearing
  e.preventDefault()
  
  // Check if user has dismissed recently
  if (checkIfDismissed()) {
    return
  }

  // Store the event so it can be triggered later
  deferredPrompt.value = e as BeforeInstallPromptEvent
  
  // Show our custom prompt
  showPrompt.value = true
}

const checkIfInstalled = () => {
  // Check if app is already installed
  if (window.matchMedia('(display-mode: standalone)').matches) {
    return true
  }
  // Check if running in standalone mode (iOS)
  if ((window.navigator as any).standalone) {
    return true
  }
  return false
}

onMounted(() => {
  // Only run on client side
  if (typeof window === 'undefined') {
    return
  }

  // Don't show if already installed
  if (checkIfInstalled()) {
    return
  }

  // Listen for the beforeinstallprompt event
  window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)

  // Also check PWA module's install prompt if available
  if ($pwa && 'installPrompt' in $pwa && $pwa.installPrompt) {
    deferredPrompt.value = $pwa.installPrompt as BeforeInstallPromptEvent
    if (!checkIfDismissed()) {
      showPrompt.value = true
    }
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
  }
})
</script>

<style scoped>
.install-prompt-snackbar {
  z-index: 9999;
}
</style>

