<template>
  <v-container class="payment-result-page" dir="rtl">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <!-- Loading State -->
        <v-card v-if="loading" class="pa-8 text-center" rounded="lg">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
            width="6"
          />
          <p class="text-subtitle-1 mt-4">در حال بررسی نتیجه پرداخت...</p>
        </v-card>

        <!-- Success State -->
        <v-card v-else-if="status === 'success'" class="pa-6" rounded="lg">
          <div class="text-center mb-6">
            <v-avatar size="80" color="green-lighten-4" class="mb-4">
              <v-icon size="48" color="green">mdi-check-circle</v-icon>
            </v-avatar>
            <h1 class="text-h5 font-weight-bold mb-2">پرداخت موفق!</h1>
            <p class="text-subtitle-1 text-medium-emphasis">
              اشتراک پریمیوم شما با موفقیت فعال شد
            </p>
          </div>

          <v-divider class="my-4" />

          <v-list bg-color="transparent">
            <v-list-item v-if="trackId">
              <template #prepend>
                <v-icon>mdi-identifier</v-icon>
              </template>
              <v-list-item-title>کد پیگیری</v-list-item-title>
              <v-list-item-subtitle>{{ trackId }}</v-list-item-subtitle>
            </v-list-item>
            
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-calendar-check</v-icon>
              </template>
              <v-list-item-title>وضعیت</v-list-item-title>
              <v-list-item-subtitle class="text-green">پرداخت شده و تایید شده</v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <v-alert type="info" variant="tonal" class="my-4">
            <div class="d-flex align-center gap-2">
              <v-icon>mdi-information</v-icon>
              <div>
                فاکتور پرداخت از طریق ایمیل برای شما ارسال می‌شود و در تاریخچه پرداخت‌ها قابل مشاهده است.
              </div>
            </div>
          </v-alert>

          <div class="d-flex gap-2">
            <v-btn
              color="primary"
              variant="flat"
              block
              size="large"
              @click="navigateTo('/seller/dashboard')"
            >
              <v-icon start>mdi-view-dashboard</v-icon>
              بازگشت به داشبورد
            </v-btn>
            <v-btn
              color="grey-lighten-1"
              variant="flat"
              @click="navigateTo('/seller/payment-history')"
            >
              <v-icon>mdi-history</v-icon>
            </v-btn>
          </div>
        </v-card>

        <!-- Failure State -->
        <v-card v-else-if="status === 'failed'" class="pa-6" rounded="lg">
          <div class="text-center mb-6">
            <v-avatar size="80" color="red-lighten-4" class="mb-4">
              <v-icon size="48" color="red">mdi-close-circle</v-icon>
            </v-avatar>
            <h1 class="text-h5 font-weight-bold mb-2">پرداخت ناموفق</h1>
            <p class="text-subtitle-1 text-medium-emphasis">
              متأسفانه پرداخت شما با خطا مواجه شد
            </p>
          </div>

          <v-alert type="error" variant="tonal" class="mb-4">
            {{ errorMessage }}
          </v-alert>

          <div class="d-flex flex-column gap-2">
            <v-btn
              color="primary"
              variant="flat"
              size="large"
              @click="retry"
            >
              <v-icon start>mdi-refresh</v-icon>
              تلاش مجدد
            </v-btn>
            <v-btn
              color="grey"
              variant="text"
              @click="navigateTo('/seller/dashboard')"
            >
              بازگشت به داشبورد
            </v-btn>
          </div>
        </v-card>

        <!-- Cancelled State -->
        <v-card v-else-if="status === 'cancelled'" class="pa-6" rounded="lg">
          <div class="text-center mb-6">
            <v-avatar size="80" color="orange-lighten-4" class="mb-4">
              <v-icon size="48" color="orange">mdi-cancel</v-icon>
            </v-avatar>
            <h1 class="text-h5 font-weight-bold mb-2">پرداخت لغو شد</h1>
            <p class="text-subtitle-1 text-medium-emphasis">
              شما پرداخت را لغو کردید
            </p>
          </div>

          <v-alert type="warning" variant="tonal" class="mb-4">
            هیچ مبلغی از حساب شما کسر نشده است.
          </v-alert>

          <div class="d-flex flex-column gap-2">
            <v-btn
              color="primary"
              variant="flat"
              size="large"
              @click="retry"
            >
              <v-icon start>mdi-arrow-right</v-icon>
              بازگشت به صفحه پرداخت
            </v-btn>
            <v-btn
              color="grey"
              variant="text"
              @click="navigateTo('/seller/dashboard')"
            >
              بازگشت به داشبورد
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const status = ref<'success' | 'failed' | 'cancelled' | null>(null)
const trackId = ref<string | null>(null)
const errorMessage = ref('خطای نامشخص در پرداخت')
const loading = ref(true)

onMounted(() => {
  // Get status from query params
  const statusParam = route.query.status as string
  const trackIdParam = route.query.track_id as string
  const errorParam = route.query.error as string

  trackId.value = trackIdParam || null

  if (statusParam === 'success') {
    status.value = 'success'
  } else if (statusParam === 'cancelled') {
    status.value = 'cancelled'
  } else if (statusParam === 'failed') {
    status.value = 'failed'
    
    // Map error codes to Persian messages
    const errorMessages: Record<string, string> = {
      invalid_callback: 'اطلاعات دریافتی از درگاه نامعتبر است',
      payment_not_found: 'پرداخت یافت نشد',
      verification_failed: 'تایید پرداخت با خطا مواجه شد',
      system_error: 'خطای سیستمی رخ داده است',
    }
    
    errorMessage.value = errorMessages[errorParam] || 'خطای نامشخص در پرداخت'
  } else {
    // Unknown status, redirect to dashboard
    setTimeout(() => {
      navigateTo('/seller/dashboard')
    }, 2000)
  }

  loading.value = false
})

function retry() {
  navigateTo('/seller/dashboard')
}
</script>

<style scoped>
.payment-result-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

