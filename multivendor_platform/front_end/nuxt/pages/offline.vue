<template>
  <v-container class="offline-container">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="text-center pa-8" elevation="4">
          <v-card-title class="text-h4 mb-4">
            <v-icon size="64" color="warning" class="mb-4">mdi-wifi-off</v-icon>
            <div class="text-h5">اتصال به اینترنت برقرار نیست</div>
          </v-card-title>

          <v-card-text>
            <p class="text-body-1 mb-4">
              به نظر می‌رسد اتصال شما به اینترنت قطع شده است. لطفاً اتصال خود را بررسی کنید و دوباره تلاش کنید.
            </p>
            <p class="text-body-2 text-medium-emphasis">
              برخی از محتواها ممکن است به صورت آفلاین در دسترس باشند.
            </p>
          </v-card-text>

          <v-card-actions class="justify-center">
            <v-btn
              color="primary"
              size="large"
              prepend-icon="mdi-refresh"
              @click="retryConnection"
              :loading="retrying"
            >
              تلاش مجدد
            </v-btn>
            <v-btn
              color="secondary"
              size="large"
              prepend-icon="mdi-home"
              @click="goHome"
              variant="outlined"
            >
              بازگشت به صفحه اصلی
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const retrying = ref(false)

const retryConnection = async () => {
  retrying.value = true
  try {
    // Check if we're back online
    if (navigator.onLine) {
      // Try to reload the page
      window.location.reload()
    } else {
      // Wait a bit and check again
      await new Promise(resolve => setTimeout(resolve, 1000))
      if (navigator.onLine) {
        window.location.reload()
      } else {
        // Show error message
        alert('هنوز اتصال به اینترنت برقرار نیست. لطفاً اتصال خود را بررسی کنید.')
      }
    }
  } catch (error) {
    console.error('Error retrying connection:', error)
  } finally {
    retrying.value = false
  }
}

const goHome = () => {
  navigateTo('/')
}

useSeoMeta({
  title: 'آفلاین - ایندکسو',
  description: 'اتصال به اینترنت برقرار نیست'
})
</script>

<style scoped>
.offline-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f5f5 0%, #e8f5e9 100%);
}
</style>

