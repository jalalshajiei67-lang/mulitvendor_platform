<template>
  <div class="chat-guest-auth" dir="rtl">
    <div class="auth-content">
      <!-- Header -->
      <div class="auth-header">
        <v-icon color="primary" size="32" class="mb-2">mdi-chat-outline</v-icon>
        <h3 class="text-h6 font-weight-bold mb-1">ورود به گفتگو</h3>
        <p class="text-body-2 text-medium-emphasis">
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
            prepend-inner-icon="mdi-account"
            :error="!!errors.fullName"
            :error-messages="errors.fullName"
            :disabled="loading"
            class="mb-3"
            @input="clearError('fullName')"
          />

          <v-text-field
            v-model="mobile"
            label="شماره موبایل"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-phone"
            :error="!!errors.mobile"
            :error-messages="errors.mobile"
            :disabled="loading"
            type="tel"
            maxlength="11"
            class="mb-4"
            @input="handleMobileInput"
          />

          <v-btn
            color="primary"
            block
            size="large"
            rounded="lg"
            :loading="loading"
            :disabled="!isFormValid || loading"
            @click="requestOtp"
          >
            <v-icon class="ml-2">mdi-send</v-icon>
            ارسال کد تأیید
          </v-btn>
        </div>
      </v-fade-transition>

      <!-- Step 2: OTP Verification -->
      <v-fade-transition>
        <div v-if="otpRequested" class="otp-section">
          <div class="text-center mb-4">
            <p class="text-body-1 mb-2">
              کد تأیید به شماره <strong>{{ formattedMobile }}</strong> ارسال شد
            </p>
            <p class="text-body-2 text-medium-emphasis">
              لطفاً کد 6 رقمی را وارد کنید
            </p>
            <p v-if="attemptsRemaining > 0" class="text-caption text-medium-emphasis mt-2">
              تعداد تلاش‌های باقی‌مانده: {{ attemptsRemaining }}
            </p>
          </div>

          <!-- OTP Input Fields -->
          <div class="otp-inputs d-flex justify-center gap-2 mb-4">
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
              v-if="devModeCode && process.env.NODE_ENV === 'development'"
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
          <div class="text-center mb-4">
            <v-btn
              v-if="canResend"
              variant="text"
              color="primary"
              :disabled="loading || attemptsRemaining === 0"
              @click="resendOtp"
              :loading="resending"
            >
              <v-icon class="ml-2">mdi-refresh</v-icon>
              ارسال مجدد کد
            </v-btn>
            <div v-else class="text-body-2 text-medium-emphasis">
              ارسال مجدد کد در {{ countdown }} ثانیه
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="d-flex gap-2">
            <v-btn
              variant="outlined"
              block
              :disabled="loading"
              @click="resetForm"
            >
              بازگشت
            </v-btn>
            <v-btn
              color="primary"
              block
              size="large"
              rounded="lg"
              :loading="loading"
              :disabled="!isOtpComplete || loading || attemptsRemaining === 0"
              @click="verifyOtp"
            >
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
    if (response.otp_code && process.env.NODE_ENV === 'development') {
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
  padding: 24px;
  background-color: #fafafa;
}

.auth-content {
  width: 100%;
  max-width: 400px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-form {
  width: 100%;
}

.otp-section {
  width: 100%;
}

.otp-inputs {
  direction: ltr; /* Inputs are LTR for better UX */
}

.otp-digit {
  width: 50px;
  max-width: 50px;
}

.otp-digit :deep(.v-field__input) {
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 0.1em;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

@media (max-width: 600px) {
  .chat-guest-auth {
    padding: 16px;
  }
  
  .auth-header h3 {
    font-size: 1.25rem;
  }
}
</style>

