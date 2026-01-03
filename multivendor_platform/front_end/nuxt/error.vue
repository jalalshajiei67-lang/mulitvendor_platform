<template>
  <!-- Don't show default error page for 404s - redirect to custom 404 page instead -->
  <div v-if="!is404" class="error-page" dir="rtl">
    <v-container fluid>
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" sm="8" md="6" lg="4" class="text-center">
          <v-card elevation="0" class="pa-8">
            <v-icon
              :size="display.xs.value ? 80 : 120"
              color="error"
              class="mb-4"
            >
              mdi-alert-circle
            </v-icon>
            <h1 class="text-h4 mb-4">خطایی رخ داد</h1>
            <p class="text-body-1 text-medium-emphasis mb-6">
              {{ sanitizedError.message || 'متأسفانه خطایی در سیستم رخ داده است. لطفاً دوباره تلاش کنید.' }}
            </p>
            <v-row justify="center" class="gap-2">
              <v-btn
                color="primary"
                size="large"
                prepend-icon="mdi-refresh"
                @click="handleError"
              >
                تلاش مجدد
              </v-btn>
              <v-btn
                color="secondary"
                size="large"
                prepend-icon="mdi-home"
                variant="outlined"
                @click="goHome"
              >
                بازگشت به صفحه اصلی
              </v-btn>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
  <!-- Show loading state while redirecting 404s -->
  <div v-else class="error-page" dir="rtl">
    <v-container fluid class="fill-height">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <p class="mt-4 text-body-1">در حال انتقال...</p>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'

const props = defineProps<{
  error: {
    statusCode?: number
    statusMessage?: string
    message?: string
    data?: any
    [key: string]: any
  }
}>()

const display = useDisplay()

// Redirect 404 errors to the custom 404 page
// This prevents the default error page from showing for 404s
const statusCode = props.error?.statusCode
const is404 = computed(() => statusCode === 404)

// Handle 404 redirect on both server and client
if (statusCode === 404) {
  if (process.server) {
    // On server side, navigate immediately
    navigateTo('/404', { redirectCode: 404, replace: true }).catch(() => {
      // Ignore navigation errors
    })
  } else {
    // On client side, redirect when component mounts
    onMounted(() => {
      const route = useRoute()
      // Only redirect if we're not already on the 404 page to avoid loops
      if (route.path !== '/404') {
        clearError({ redirect: '/404' })
      }
    })
  }
}

// Sanitize error object to ensure it's serializable and doesn't break Pinia hydration
// This prevents "hasOwnProperty is not a function" errors
const sanitizedError = computed(() => {
  const error = props.error
  if (!error) return { message: 'خطایی رخ داده است' }
  
  // If we somehow got here with a 404 (shouldn't happen due to redirect above),
  // show a loading message
  if (error.statusCode === 404) {
    return { message: 'در حال انتقال...' }
  }
  
  // Create a clean error object with proper prototype
  const clean: Record<string, any> = {
    statusCode: error.statusCode,
    statusMessage: error.statusMessage,
    message: error.message
  }
  
  // Safely copy other properties if they exist and are serializable
  if (error.data && typeof error.data === 'object') {
    try {
      // Only include simple serializable properties
      if (error.data.path) clean.path = String(error.data.path)
      if (error.data.url) clean.url = String(error.data.url)
    } catch (e) {
      // Ignore non-serializable properties
    }
  }
  
  return clean
})

useHead({
  title: `خطا ${sanitizedError.value.statusCode || ''}`,
  meta: [
    {
      name: 'description',
      content: sanitizedError.value.message || sanitizedError.value.statusMessage || 'خطایی در سیستم رخ داده است'
    },
    {
      name: 'robots',
      content: 'noindex, nofollow'
    }
  ]
})

const handleError = () => {
  clearError({ redirect: '/' })
}

const goHome = () => {
  navigateTo('/')
}
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

