<template>
  <v-container fluid class="fill-height auth-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark prominent>
            <v-toolbar-title class="text-h5">ورود به حساب کاربری</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pa-6">
            <!-- Login Method Toggle -->
            <div class="d-flex justify-center mb-4">
              <v-btn-toggle
                v-model="loginMethod"
                mandatory
                variant="outlined"
                density="compact"
                rounded="lg"
              >
                <v-btn value="password">
                  <v-icon class="ml-2">mdi-lock</v-icon>
                  رمز عبور
                </v-btn>
                <v-btn value="otp">
                  <v-icon class="ml-2">mdi-shield-check</v-icon>
                  کد تأیید
                </v-btn>
              </v-btn-toggle>
            </div>

            <!-- Password Login Form -->
            <v-form v-if="loginMethod === 'password'" ref="formRef" v-model="isValid" @submit.prevent="submit">
              <v-text-field
                v-model="username"
                label="شماره موبایل"
                prepend-inner-icon="mdi-phone"
                variant="outlined"
                rounded="lg"
                :rules="usernameRules"
                :error="authError?.field === 'username'"
                :error-messages="authError?.field === 'username' ? [authError.message] : []"
                required
                @input="clearError"
                hint="شماره موبایل خود را وارد کنید"
                persistent-hint
              />

              <v-text-field
                v-model="password"
                label="رمز عبور"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                rounded="lg"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                :rules="passwordRules"
                :error="authError?.field === 'password'"
                :error-messages="authError?.field === 'password' ? [authError.message] : []"
                required
                @input="clearError"
                class="mt-2"
              />

              <!-- Forgot Password Link -->
              <div class="text-left mt-2">
                <NuxtLink to="/password-reset" class="text-primary text-body-2">
                  <v-icon size="small" class="ml-1">mdi-lock-reset</v-icon>
                  رمز عبور را فراموش کرده‌اید؟
                </NuxtLink>
              </div>
            </v-form>

            <!-- OTP Login Form -->
            <div v-else>
              <v-text-field
                v-if="!showOtpVerification"
                v-model="otpPhone"
                label="شماره موبایل"
                prepend-inner-icon="mdi-phone"
                variant="outlined"
                rounded="lg"
                :rules="phoneRules"
                :error="authError?.field === 'phone'"
                :error-messages="authError?.field === 'phone' ? [authError.message] : []"
                required
                @input="clearError"
                hint="شماره موبایل خود را وارد کنید (مثال: 09123456789)"
                persistent-hint
                class="mb-4"
              />

              <!-- OTP Verification Component -->
              <div v-if="showOtpVerification">
                <AuthOtpVerification
                  :phone="otpPhone"
                  purpose="login"
                  @verified="handleOtpVerified"
                  @error="handleOtpError"
                  @resend="handleOtpResend"
                />
              </div>
            </div>

              <!-- Enhanced Error Display -->
              <transition name="slide-fade">
                <v-alert
                  v-if="authError"
                  :type="getErrorColor(authError.type)"
                  variant="tonal"
                  class="mt-4 error-alert"
                  :icon="getErrorIcon(authError.type)"
                  closable
                  @click:close="clearError"
                  rounded="lg"
                >
                  <div class="error-content">
                    <div class="text-h6 font-weight-bold mb-2">{{ authError.message }}</div>
                    <div v-if="authError.hint" class="text-body-2 mt-2 hint-text">
                      {{ authError.hint }}
                    </div>
                    <div v-if="authError.action === 'forgot_password'" class="mt-3">
                      <v-btn
                        variant="text"
                        size="small"
                        color="primary"
                        prepend-icon="mdi-lock-reset"
                        @click="router.push('/password-reset')"
                      >
                        بازیابی رمز عبور
                      </v-btn>
                    </div>
                    <div v-if="authError.recoverable && authError.action === 'retry'" class="mt-3">
                      <v-btn
                        variant="outlined"
                        size="small"
                        color="primary"
                        @click="retryLogin"
                        :loading="loading"
                      >
                        تلاش مجدد
                      </v-btn>
                    </div>
                  </div>
                </v-alert>
              </transition>
          </v-card-text>

          <v-card-actions v-if="loginMethod === 'password'" class="pa-6 pt-0">
            <v-btn
              color="primary"
              block
              size="large"
              rounded="lg"
              :loading="loading"
              :disabled="!isValid || loading"
              @click="submit"
            >
              <span v-if="!loading">ورود</span>
              <span v-else>در حال ورود...</span>
            </v-btn>
          </v-card-actions>

          <v-card-actions v-else-if="!showOtpVerification" class="pa-6 pt-0">
            <v-btn
              color="primary"
              block
              size="large"
              rounded="lg"
              :loading="loading"
              :disabled="!otpPhone || !isPhoneValid || loading"
              @click="requestOtp"
            >
              <span v-if="!loading">ارسال کد تأیید</span>
              <span v-else>در حال ارسال...</span>
            </v-btn>
          </v-card-actions>

          <v-divider />

          <v-card-text class="text-center pa-4">
            حساب کاربری ندارید؟
            <NuxtLink to="/register" class="text-primary font-weight-bold">ثبت‌نام کنید</NuxtLink>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { getErrorIcon, getErrorColor } from '~/utils/authErrors'
import type { AuthError } from '~/utils/authErrors'

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
  title: 'ورود | ایندکسو',
  description: 'ورود به حساب کاربری ایندکسو برای دسترسی به پنل کاربران و فروشندگان.',
  ogTitle: 'ورود به ایندکسو',
  ogDescription: 'برای مدیریت سفارش‌ها و محصولات وارد حساب کاربری خود شوید.',
  ogType: 'website'
})

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const formRef = ref()
const isValid = ref(false)
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loginMethod = ref<'password' | 'otp'>('password')
const otpPhone = ref('')
const showOtpVerification = ref(false)
const loading = computed(() => authStore.loading)
const authError = computed(() => authStore.authError)

const usernameRules = [
  (value: string) => Boolean(value?.trim()) || 'لطفاً شماره موبایل خود را وارد کنید',
  (value: string) => {
    if (!value) return true
    const cleaned = value.replace(/[\s\-()]/g, '')
    if (cleaned.length < 10) {
      return 'شماره موبایل باید حداقل ۱۰ رقم باشد. لطفاً شماره را کامل وارد کنید'
    }
    return true
  }
]
const passwordRules = [
  (value: string) => Boolean(value) || 'لطفاً رمز عبور خود را وارد کنید',
  (value: string) => (value?.length >= 6) || 'رمز عبور باید حداقل ۶ کاراکتر باشد. لطفاً رمز عبور خود را بررسی کنید'
]

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

const isPhoneValid = computed(() => {
  if (!otpPhone.value) return false
  const cleaned = otpPhone.value.replace(/[\s\-()]/g, '')
  return /^09\d{9}$/.test(cleaned)
})

const clearError = () => {
  authStore.clearError()
}

const retryLogin = async () => {
  await submit()
}

const submit = async () => {
  if (!formRef.value) return

  const result = await formRef.value.validate()
  if (!result.valid) return

  clearError()

  try {
    console.log('[LOGIN] Starting login...')
    const response = await authStore.login({
      username: username.value.trim(),
      password: password.value
    })
    
    console.log('[LOGIN] Login response:', response)

    const redirect = (route.query.redirect as string) || null
    if (response?.user?.is_staff || response?.user?.is_superuser) {
      console.log('[LOGIN] Admin user, redirecting to admin dashboard')
      return router.push('/admin/dashboard')
    }
    if (response?.user?.role === 'seller' || response?.user?.role === 'both') {
      console.log('[LOGIN] Seller user, redirecting to seller dashboard')
      return router.push(redirect || '/seller/dashboard')
    }
    if (response?.user?.role === 'buyer') {
      console.log('[LOGIN] Buyer user, redirecting to home')
      return router.push(redirect || '/')
    }

    console.log('[LOGIN] No role match, redirecting to home')
    router.push(redirect || '/')
  } catch (err: any) {
    console.error('[LOGIN] Login failed with error:', err)
    // Error is already handled by the auth store
  }
}

const requestOtp = async () => {
  if (!isPhoneValid.value) {
    // Error will be shown by form validation
    return
  }

  clearError()

  try {
    const response = await authStore.requestOtpLogin(otpPhone.value)
    
    // Always show OTP verification component on success
    if (response && response.success !== false) {
      showOtpVerification.value = true
    }
  } catch (err: any) {
    // Error is already handled by the auth store
    showOtpVerification.value = false
  }
}

const handleOtpVerified = async (data: any) => {
  if (data.token && data.user) {
    const redirect = (route.query.redirect as string) || null
    if (data.user.is_staff || data.user.is_superuser) {
      return router.push('/admin/dashboard')
    }
    if (data.user.role === 'seller' || data.user.role === 'both') {
      return router.push(redirect || '/seller/dashboard')
    }
    if (data.user.role === 'buyer') {
      return router.push(redirect || '/')
    }
    router.push(redirect || '/')
  }
}

const handleOtpError = (message: string) => {
  console.error('OTP verification error:', message)
}

const handleOtpResend = async () => {
  await requestOtp()
}

// Reset OTP form when switching methods
watch(loginMethod, () => {
  showOtpVerification.value = false
  otpPhone.value = ''
  clearError()
})
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

:deep(.v-field__append-inner) {
  margin-inline-start: 0;
  margin-inline-end: 8px;
}

.error-alert {
  font-size: 16px;
  line-height: 1.6;
}

.error-content {
  width: 100%;
}

.hint-text {
  opacity: 0.9;
  font-size: 14px;
}

/* Slide fade animation for error */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Focus styles for better visibility */
:deep(.v-field--focused) {
  border-color: rgb(var(--v-theme-primary)) !important;
}

/* Error field highlighting */
:deep(.v-field--error) {
  animation: shake 0.3s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
</style>

