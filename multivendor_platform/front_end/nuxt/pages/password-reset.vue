<template>
  <v-container fluid class="fill-height auth-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5">
        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark prominent>
            <v-toolbar-title class="text-h5">بازیابی رمز عبور</v-toolbar-title>
          </v-toolbar>
          
          <v-card-text class="pa-6">
            <!-- Step 1: Request OTP -->
            <div v-if="step === 1">
              <div class="text-center mb-6">
                <v-icon size="64" color="primary" class="mb-4">mdi-lock-reset</v-icon>
                <p class="text-h6 mb-2">بازیابی رمز عبور</p>
                <p class="text-body-2 text-medium-emphasis">
                  شماره موبایل خود را وارد کنید تا کد تأیید برای شما ارسال شود
                </p>
              </div>

              <v-form ref="phoneFormRef" v-model="phoneFormValid" @submit.prevent="requestOtp">
                <v-text-field
                  v-model="phone"
                  label="شماره موبایل"
                  prepend-inner-icon="mdi-phone"
                  variant="outlined"
                  rounded="lg"
                  :rules="phoneRules"
                  :error="!!error"
                  :error-messages="error ? [error] : []"
                  required
                  @input="clearError"
                  hint="شماره موبایل خود را وارد کنید (مثال: 09123456789)"
                  persistent-hint
                />

                <v-alert
                  v-if="error"
                  type="error"
                  variant="tonal"
                  class="mt-4"
                  closable
                  @click:close="clearError"
                  rounded="lg"
                  icon="mdi-alert-circle"
                >
                  <div class="error-message">
                    <div class="text-body-1 font-weight-medium mb-2">{{ error.split('\n\n')[0] }}</div>
                    <div v-if="error.includes('\n\n')" class="text-body-2 mt-2" style="opacity: 0.9;">
                      {{ error.split('\n\n')[1] }}
                    </div>
                  </div>
                </v-alert>
              </v-form>
            </div>

            <!-- Step 2: Verify OTP -->
            <div v-if="step === 2">
              <AuthOtpVerification
                :phone="phone"
                purpose="password_reset"
                @verified="handleOtpVerified"
                @error="handleOtpError"
                @resend="handleOtpResend"
              />
            </div>

            <!-- Step 3: Set New Password -->
            <div v-if="step === 3">
              <div class="text-center mb-6">
                <v-icon size="64" color="success" class="mb-4">mdi-check-circle</v-icon>
                <p class="text-h6 mb-2">کد تأیید شد</p>
                <p class="text-body-2 text-medium-emphasis">
                  رمز عبور جدید خود را وارد کنید
                </p>
              </div>

              <v-form ref="passwordFormRef" v-model="passwordFormValid" @submit.prevent="resetPassword">
                <v-text-field
                  v-model="newPassword"
                  label="رمز عبور جدید"
                  prepend-inner-icon="mdi-lock"
                  variant="outlined"
                  rounded="lg"
                  :type="showPassword ? 'text' : 'password'"
                  :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append-inner="showPassword = !showPassword"
                  :rules="passwordRules"
                  required
                  class="mb-4"
                />

                <v-text-field
                  v-model="confirmPassword"
                  label="تکرار رمز عبور"
                  prepend-inner-icon="mdi-lock-check"
                  variant="outlined"
                  rounded="lg"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append-inner="showConfirmPassword = !showConfirmPassword"
                  :rules="confirmPasswordRules"
                  required
                />

                <v-alert
                  v-if="error"
                  type="error"
                  variant="tonal"
                  class="mt-4"
                  closable
                  @click:close="clearError"
                  rounded="lg"
                  icon="mdi-alert-circle"
                >
                  <div class="error-message">
                    <div class="text-body-1 font-weight-medium mb-2">{{ error.split('\n\n')[0] }}</div>
                    <div v-if="error.includes('\n\n')" class="text-body-2 mt-2" style="opacity: 0.9;">
                      {{ error.split('\n\n')[1] }}
                    </div>
                  </div>
                </v-alert>
              </v-form>
            </div>
          </v-card-text>

          <v-card-actions class="pa-6 pt-0">
            <!-- Step 1: Request OTP Button -->
            <v-btn
              v-if="step === 1"
              color="primary"
              block
              size="large"
              rounded="lg"
              :loading="loading"
              :disabled="!phoneFormValid || loading"
              @click="requestOtp"
            >
              <span v-if="!loading">ارسال کد تأیید</span>
              <span v-else>در حال ارسال...</span>
            </v-btn>

            <!-- Step 3: Reset Password Button -->
            <v-btn
              v-if="step === 3"
              color="primary"
              block
              size="large"
              rounded="lg"
              :loading="loading"
              :disabled="!passwordFormValid || loading"
              @click="resetPassword"
            >
              <span v-if="!loading">تغییر رمز عبور</span>
              <span v-else>در حال تغییر...</span>
            </v-btn>
          </v-card-actions>

          <v-divider />

          <v-card-text class="text-center pa-4">
            <NuxtLink to="/login" class="text-primary font-weight-bold">
              <v-icon class="ml-2">mdi-arrow-right</v-icon>
              بازگشت به صفحه ورود
            </NuxtLink>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: [
    function redirectIfAuthenticated() {
      const authStore = useAuthStore()
      if (authStore.isAuthenticated) {
        return navigateTo('/')
      }
    }
  ]
})

useSeoMeta({
  title: 'بازیابی رمز عبور | ایندکسو',
  description: 'بازیابی رمز عبور حساب کاربری ایندکسو با استفاده از کد تأیید ارسالی به شماره موبایل.',
  ogTitle: 'بازیابی رمز عبور',
  ogDescription: 'رمز عبور خود را با استفاده از کد تأیید بازیابی کنید.',
  ogType: 'website'
})

const authStore = useAuthStore()
const router = useRouter()

const step = ref(1) // 1: Request OTP, 2: Verify OTP, 3: Set Password
const phone = ref('')
const verifiedOtpCode = ref('') // Store verified OTP code for password reset
const newPassword = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const phoneFormRef = ref()
const passwordFormRef = ref()
const phoneFormValid = ref(false)
const passwordFormValid = ref(false)
const loading = computed(() => authStore.loading)
const error = ref('')

const phoneRules = [
  (value: string) => Boolean(value?.trim()) || 'لطفاً شماره موبایل خود را وارد کنید',
  (value: string) => {
    if (!value) return true
    const cleaned = value.replace(/[\s\-()]/g, '')
    if (!/^09\d{9}$/.test(cleaned)) {
      return 'شماره موبایل باید 11 رقم و با 09 شروع شود. مثال: 09123456789'
    }
    return true
  }
]

const passwordRules = [
  (value: string) => Boolean(value) || 'لطفاً رمز عبور جدید را وارد کنید',
  (value: string) => (value?.length >= 6) || 'رمز عبور باید حداقل ۶ کاراکتر باشد. لطفاً رمز عبور قوی‌تری انتخاب کنید'
]

const confirmPasswordRules = [
  (value: string) => Boolean(value) || 'لطفاً رمز عبور را دوباره وارد کنید',
  (value: string) => value === newPassword.value || 'رمز عبور و تکرار آن باید یکسان باشند. لطفاً دقت کنید'
]

const clearError = () => {
  error.value = ''
  authStore.clearError()
}

const requestOtp = async () => {
  if (!phoneFormRef.value) return

  const result = await phoneFormRef.value.validate()
  if (!result.valid) return

  clearError()

  try {
    await authStore.requestPasswordResetOtp(phone.value)
    step.value = 2
  } catch (err: any) {
    const errorMessage = err.data?.error || err.message || 'خطا در ارسال کد تأیید'
    const helpfulMessage = err.data?.helpful_message || err.data?.hint || ''
    
    error.value = helpfulMessage 
      ? `${errorMessage}\n\n${helpfulMessage}`
      : errorMessage
  }
}

const handleOtpVerified = (data: any) => {
  // Store the OTP code that was verified (we'll need it for password reset)
  // Note: For password_reset, we need to send the code again with the new password
  // The backend will verify it again as part of the password reset process
  if (data.otp_code) {
    verifiedOtpCode.value = data.otp_code
  }
  step.value = 3
  clearError()
}

const handleOtpError = (message: string) => {
  error.value = message
}

const handleOtpResend = async () => {
  await requestOtp()
}

const resetPassword = async () => {
  if (!passwordFormRef.value) return

  const result = await passwordFormRef.value.validate()
  if (!result.valid) return

  clearError()

  try {
    // Call password reset API endpoint
    const response = await useApiFetch('auth/password-reset/', {
      method: 'POST',
      body: {
        phone: phone.value,
        code: verifiedOtpCode.value,
        new_password: newPassword.value
      }
    })

    if (response.success) {
      // Show success message and redirect to login
      router.push({
        path: '/login',
        query: { message: 'رمز عبور شما با موفقیت تغییر یافت. اکنون می‌توانید با رمز عبور جدید وارد شوید.' }
      })
    }
  } catch (err: any) {
    const errorMessage = err.data?.error || err.message || 'خطا در تغییر رمز عبور'
    const helpfulMessage = err.data?.helpful_message || err.data?.hint || ''
    
    error.value = helpfulMessage 
      ? `${errorMessage}\n\n${helpfulMessage}`
      : errorMessage
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.auth-container {
  direction: rtl;
  text-align: right;
}

:deep(.v-field__input) {
  text-align: right;
}
</style>

