<template>
  <div class="chat-guest-auth" dir="rtl">
    <div class="auth-content">
      <!-- Header -->
      <div class="auth-header">
        <div class="header-icon-wrapper">
          <v-icon size="40" color="white">mdi-chat-processing-outline</v-icon>
        </div>
        <h3 class="text-h5 font-weight-bold mb-2 mt-4">ورود به گفتگو</h3>
        <p class="text-body-1 text-medium-emphasis">
          برای شروع گفتگو، لطفاً اطلاعات خود را وارد کنید
        </p>
      </div>

      <!-- Step 1: Name and Mobile Input -->
      <v-fade-transition>
        <div v-if="!otpRequested" class="auth-form">
          <v-text-field
            v-model="fullName"
            label="نام و نام خانوادگی"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-account-outline"
            :error="!!errors.fullName"
            :error-messages="errors.fullName"
            :disabled="loading"
            class="form-field"
            rounded="lg"
            bg-color="white"
            @input="clearError('fullName')"
          />

          <v-text-field
            v-model="mobile"
            label="شماره موبایل"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-phone-outline"
            :error="!!errors.mobile"
            :error-messages="errors.mobile"
            :disabled="loading"
            type="tel"
            maxlength="11"
            class="form-field"
            rounded="lg"
            bg-color="white"
            @input="handleMobileInput"
          />

          <v-btn
            color="primary"
            block
            size="large"
            rounded="lg"
            elevation="2"
            :loading="loading"
            :disabled="!isFormValid || loading"
            class="submit-btn"
            @click="requestOtp"
          >
            <v-icon start size="20">mdi-send</v-icon>
            ارسال کد تأیید
          </v-btn>
        </div>
      </v-fade-transition>

      <!-- Step 2: OTP Verification -->
      <v-fade-transition>
        <div v-if="otpRequested" class="otp-section">
          <div class="otp-header text-center mb-6">
            <div class="otp-icon-wrapper mb-3">
              <v-icon size="48" color="primary">mdi-message-text-lock-outline</v-icon>
            </div>
            <p class="text-h6 font-weight-bold mb-2">
              کد تأیید ارسال شد
            </p>
            <p class="text-body-1 text-medium-emphasis mb-1">
              کد تأیید به شماره <strong class="phone-number">{{ formattedMobile }}</strong> ارسال شد
            </p>
            <p class="text-body-2 text-medium-emphasis mb-3">
              لطفاً کد 6 رقمی را وارد کنید
            </p>
            <v-chip
              v-if="attemptsRemaining > 0"
              size="small"
              variant="tonal"
              color="info"
              class="attempts-chip"
            >
              <v-icon start size="16">mdi-information-outline</v-icon>
              تعداد تلاش‌های باقی‌مانده: {{ attemptsRemaining }}
            </v-chip>
          </div>

          <!-- OTP Input Fields -->
          <div class="otp-inputs d-flex justify-center gap-3 mb-5">
            <v-text-field
              v-for="(digit, index) in otpDigits"
              :key="index"
              v-model="otpDigits[index]"
              :ref="el => inputRefs[index] = el"
              type="text"
              inputmode="numeric"
              maxlength="1"
              variant="outlined"
              class="otp-digit"
              hide-details
              density="comfortable"
              bg-color="white"
              rounded="lg"
              :disabled="loading || attemptsRemaining === 0"
              @input="handleOtpInput(index, $event)"
              @keydown="handleOtpKeydown(index, $event)"
              @paste="handleOtpPaste"
            />
          </div>

          <!-- Error Message -->
          <transition name="slide-fade">
            <v-alert
              v-if="error"
              type="error"
              variant="tonal"
              class="mb-4"
              closable
              @click:close="error = ''"
              rounded="lg"
            >
              {{ error }}
            </v-alert>
          </transition>

          <!-- Success Message (for dev mode) -->
          <transition name="slide-fade">
            <v-alert
              v-if="devModeCode && isDev"
              type="info"
              variant="tonal"
              class="mb-4"
              rounded="lg"
            >
              <div class="d-flex align-center">
                <v-icon class="ml-2">mdi-information</v-icon>
                <div>
                  <div class="font-weight-bold">حالت توسعه</div>
                  <div class="text-body-2">کد تأیید: <strong>{{ devModeCode }}</strong></div>
                </div>
              </div>
            </v-alert>
          </transition>

          <!-- Attempts Exceeded -->
          <v-alert
            v-if="attemptsRemaining === 0"
            type="error"
            variant="tonal"
            class="mb-4"
            rounded="lg"
          >
            <div class="text-body-1 font-weight-medium">
              تعداد تلاش‌های شما به پایان رسید
            </div>
            <div class="text-body-2 mt-2">
              لطفاً دکمه "شروع مجدد" را بزنید و دوباره تلاش کنید
            </div>
          </v-alert>

          <!-- Resend Timer -->
          <div class="text-center mb-5">
            <v-btn
              v-if="canResend"
              variant="text"
              color="primary"
              size="large"
              :disabled="loading || attemptsRemaining === 0"
              @click="resendOtp"
              :loading="resending"
              class="resend-btn"
            >
              <v-icon start>mdi-refresh</v-icon>
              ارسال مجدد کد
            </v-btn>
            <div v-else class="resend-timer">
              <v-icon size="16" class="ml-1">mdi-clock-outline</v-icon>
              <span>ارسال مجدد کد در {{ countdown }} ثانیه</span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="d-flex gap-3">
            <v-btn
              variant="outlined"
              block
              size="large"
              rounded="lg"
              :disabled="loading"
              @click="resetForm"
              class="back-btn"
            >
              <v-icon start>mdi-arrow-right</v-icon>
              بازگشت
            </v-btn>
            <v-btn
              color="primary"
              block
              size="large"
              rounded="lg"
              elevation="2"
              :loading="loading"
              :disabled="!isOtpComplete || loading || attemptsRemaining === 0"
              @click="verifyOtp"
              class="verify-btn"
            >
              <v-icon start v-if="!loading">mdi-check-circle-outline</v-icon>
              <span v-if="!loading">تأیید</span>
              <span v-else>در حال تأیید...</span>
            </v-btn>
          </div>
        </div>
      </v-fade-transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useChatStore } from '~/stores/chat'

const authStore = useAuthStore()
const chatStore = useChatStore()

// Development mode check
const isDev = import.meta.env.DEV

// Form state
const fullName = ref('')
const mobile = ref('')
const otpRequested = ref(false)
const otpDigits = ref<string[]>(['', '', '', '', '', ''])
const inputRefs = ref<(HTMLElement | null)[]>([])
const loading = ref(false)
const resending = ref(false)
const error = ref('')
const errors = ref<{ fullName?: string; mobile?: string }>({})
const devModeCode = ref<string | null>(null)

// OTP state
const canResend = ref(false)
const countdown = ref(120)
let countdownTimer: NodeJS.Timeout | null = null

// Attempt tracking
const MAX_ATTEMPTS = 3
const attemptsRemaining = ref(MAX_ATTEMPTS)

const formattedMobile = computed(() => {
  if (!mobile.value) return ''
  // Format: 0912 345 6789
  const cleaned = mobile.value.replace(/\D/g, '')
  if (cleaned.length === 11) {
    return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 7)} ${cleaned.slice(7)}`
  }
  return mobile.value
})

const isFormValid = computed(() => {
  return fullName.value.trim().length >= 2 && isValidMobile(mobile.value)
})

const isOtpComplete = computed(() => {
  return otpDigits.value.every(digit => digit !== '')
})

const otpCode = computed(() => {
  return otpDigits.value.join('')
})

const isValidMobile = (phone: string): boolean => {
  const cleaned = phone.replace(/\D/g, '')
  // Iranian mobile: 09XXXXXXXXX (11 digits starting with 09)
  return cleaned.length === 11 && cleaned.startsWith('09')
}

const handleMobileInput = () => {
  // Only allow digits
  mobile.value = mobile.value.replace(/\D/g, '')
  // Limit to 11 digits
  if (mobile.value.length > 11) {
    mobile.value = mobile.value.slice(0, 11)
  }
  clearError('mobile')
}

const clearError = (field?: string) => {
  if (field) {
    errors.value[field] = undefined
  } else {
    errors.value = {}
  }
  error.value = ''
}

const validateForm = (): boolean => {
  errors.value = {}

  if (!fullName.value.trim()) {
    errors.value.fullName = 'نام و نام خانوادگی الزامی است'
    return false
  }

  if (fullName.value.trim().length < 2) {
    errors.value.fullName = 'نام باید حداقل 2 کاراکتر باشد'
    return false
  }

  if (!mobile.value) {
    errors.value.mobile = 'شماره موبایل الزامی است'
    return false
  }

  if (!isValidMobile(mobile.value)) {
    errors.value.mobile = 'شماره موبایل باید 11 رقم و با 09 شروع شود'
    return false
  }

  return true
}

const requestOtp = async () => {
  if (!validateForm()) {
    return
  }

  try {
    loading.value = true
    error.value = ''
    clearError()

    const response = await authStore.requestOtpLogin(mobile.value)

    // Check if OTP code is returned (dev mode only)
    if (response.otp_code && isDev) {
      devModeCode.value = response.otp_code
      // Auto-fill in dev mode
      const code = response.otp_code
      for (let i = 0; i < 6; i++) {
        otpDigits.value[i] = code[i] || ''
      }
      // Focus last input
      setTimeout(() => {
        if (inputRefs.value[5]) {
          (inputRefs.value[5] as any).focus()
        }
      }, 100)
    }

    otpRequested.value = true
    attemptsRemaining.value = MAX_ATTEMPTS
    startCountdown()
  } catch (err: any) {
    const errorMessage = err.data?.error || err.message || 'خطا در ارسال کد تأیید'
    const helpfulMessage = err.data?.helpful_message || err.data?.hint || ''
    
    error.value = helpfulMessage 
      ? `${errorMessage}\n\n${helpfulMessage}`
      : errorMessage
  } finally {
    loading.value = false
  }
}

const verifyOtp = async () => {
  if (!isOtpComplete.value) {
    error.value = 'لطفاً کد 6 رقمی را کامل وارد کنید'
    return
  }

  if (attemptsRemaining.value === 0) {
    error.value = 'تعداد تلاش‌های شما به پایان رسید. لطفاً دوباره شروع کنید.'
    return
  }

  try {
    loading.value = true
    error.value = ''

    // Split full name into first and last name
    const nameParts = fullName.value.trim().split(/\s+/)
    const firstName = nameParts[0] || ''
    const lastName = nameParts.slice(1).join(' ') || ''

    const response = await authStore.verifyOtpLogin(mobile.value, otpCode.value, firstName, lastName)

    if (response.success && response.token && response.user) {
      // User is now logged in
      // Reinitialize chat with authenticated user
      await chatStore.initializeChat()

      // If there's a pending chat request, start it
      if (chatStore.pendingChatRequest) {
        try {
          await chatStore.startPendingChat()
          console.log('Pending chat started successfully after authentication')
        } catch (error) {
          console.error('Failed to start pending chat:', error)
        }
      }

      // Success - component will be hidden by parent
      return
    }

    // If verification didn't return user, it might be because user doesn't exist
    // We need to handle this in backend, but for now show error
    error.value = 'خطا در تأیید کد. لطفاً دوباره تلاش کنید.'
    attemptsRemaining.value--
  } catch (err: any) {
    attemptsRemaining.value--
    
    const errorMessage = err.data?.error || err.message || 'کد تأیید نامعتبر است'
    const helpfulMessage = err.data?.helpful_message || err.data?.hint || ''
    
    error.value = helpfulMessage 
      ? `${errorMessage}\n\n${helpfulMessage}`
      : errorMessage

    // Clear OTP on error
    otpDigits.value = ['', '', '', '', '', '']
    if (inputRefs.value[0]) {
      (inputRefs.value[0] as any).focus()
    }
  } finally {
    loading.value = false
  }
}

const resendOtp = async () => {
  await requestOtp()
  otpDigits.value = ['', '', '', '', '', '']
  error.value = ''
  attemptsRemaining.value = MAX_ATTEMPTS
}

const resetForm = () => {
  otpRequested.value = false
  otpDigits.value = ['', '', '', '', '', '']
  error.value = ''
  errors.value = {}
  devModeCode.value = null
  attemptsRemaining.value = MAX_ATTEMPTS
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
  canResend.value = false
}

const handleOtpInput = (index: number, event: Event) => {
  const target = event.target as HTMLInputElement
  const value = target.value.replace(/\D/g, '') // Only digits
  
  if (value) {
    otpDigits.value[index] = value.slice(-1) // Take only last character
    
    // Move to next input
    if (index < 5 && inputRefs.value[index + 1]) {
      (inputRefs.value[index + 1] as any).focus()
    }
  } else {
    otpDigits.value[index] = ''
  }
  
  error.value = ''
}

const handleOtpKeydown = (index: number, event: KeyboardEvent) => {
  // Handle backspace
  if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
    (inputRefs.value[index - 1] as any)?.focus()
  }
  
  // Handle arrow keys
  if (event.key === 'ArrowLeft' && index > 0) {
    (inputRefs.value[index - 1] as any).focus()
  }
  if (event.key === 'ArrowRight' && index < 5) {
    (inputRefs.value[index + 1] as any).focus()
  }
}

const handleOtpPaste = (event: ClipboardEvent) => {
  event.preventDefault()
  const pastedData = event.clipboardData?.getData('text') || ''
  const digits = pastedData.replace(/\D/g, '').slice(0, 6)
  
  for (let i = 0; i < 6; i++) {
    otpDigits.value[i] = digits[i] || ''
  }
  
  // Focus last filled input or last input
  const lastFilledIndex = Math.min(digits.length - 1, 5)
  if (inputRefs.value[lastFilledIndex]) {
    (inputRefs.value[lastFilledIndex] as any).focus()
  }
}

const startCountdown = () => {
  canResend.value = false
  countdown.value = 120
  
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
  
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      canResend.value = true
      if (countdownTimer) {
        clearInterval(countdownTimer)
        countdownTimer = null
      }
    }
  }, 1000)
}

onMounted(() => {
  // Focus first input
  setTimeout(() => {
    const firstInput = document.querySelector('.auth-form .v-text-field input')
    if (firstInput) {
      (firstInput as HTMLElement).focus()
    }
  }, 100)
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
.chat-guest-auth {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100%;
}

.auth-content {
  width: 100%;
  max-width: 420px;
  animation: fadeInUp 0.4s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 0 8px;
}

.header-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  margin-bottom: 16px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
  }
}

.auth-header h3 {
  color: #1a237e;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.auth-form {
  width: 100%;
}

.form-field {
  margin-bottom: 20px;
}

.form-field :deep(.v-field) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.form-field :deep(.v-field:hover) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.form-field :deep(.v-field--focused) {
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.2);
}

.submit-btn {
  margin-top: 8px;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-transform: none;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(25, 118, 210, 0.3) !important;
}

.otp-section {
  width: 100%;
}

.otp-header {
  padding: 0 8px;
}

.otp-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  animation: fadeInScale 0.5s ease-out;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.phone-number {
  color: #1976d2;
  font-weight: 600;
}

.attempts-chip {
  font-weight: 500;
}

.otp-inputs {
  direction: ltr;
  padding: 8px 0;
}

.otp-digit {
  width: 56px;
  max-width: 56px;
  flex-shrink: 0;
}

.otp-digit :deep(.v-field) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.otp-digit :deep(.v-field--focused) {
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.3);
  transform: translateY(-2px);
}

.otp-digit :deep(.v-field__input) {
  text-align: center;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #1976d2;
}

.resend-btn {
  font-weight: 500;
  text-transform: none;
}

.resend-timer {
  display: inline-flex;
  align-items: center;
  padding: 12px 20px;
  background-color: rgba(0, 0, 0, 0.04);
  border-radius: 24px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 0.875rem;
  font-weight: 500;
}

.back-btn,
.verify-btn {
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.02em;
}

.verify-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(25, 118, 210, 0.3) !important;
}

.back-btn:hover:not(:disabled) {
  transform: translateY(-1px);
}

.slide-fade-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from {
  transform: translateY(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Mobile Responsive */
@media (max-width: 600px) {
  .chat-guest-auth {
    padding: 24px 16px;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  }
  
  .auth-content {
    max-width: 100%;
  }
  
  .auth-header {
    margin-bottom: 32px;
  }
  
  .header-icon-wrapper {
    width: 72px;
    height: 72px;
  }
  
  .auth-header h3 {
    font-size: 1.375rem;
  }
  
  .otp-icon-wrapper {
    width: 80px;
    height: 80px;
  }
  
  .otp-icon-wrapper .v-icon {
    font-size: 40px !important;
  }
  
  .otp-digit {
    width: 48px;
    max-width: 48px;
  }
  
  .otp-digit :deep(.v-field__input) {
    font-size: 1.5rem;
  }
  
  .form-field {
    margin-bottom: 16px;
  }
  
  .resend-timer {
    padding: 10px 16px;
    font-size: 0.8125rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .chat-guest-auth {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  }
  
  .auth-header h3 {
    color: #e3f2fd;
  }
  
  .resend-timer {
    background-color: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.7);
  }
}
</style>

