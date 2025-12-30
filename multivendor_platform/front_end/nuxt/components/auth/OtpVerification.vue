<template>
  <div class="otp-verification" dir="rtl">
    <v-card class="elevation-12" rounded="lg">
      <v-card-title class="text-h5 text-center pa-4">
        <v-icon class="ml-2">mdi-shield-check</v-icon>
        تأیید کد
      </v-card-title>
      
      <v-card-text class="pa-6">
        <div class="text-center mb-6">
          <p class="text-body-1 mb-2">
            کد تأیید به شماره <strong>{{ phone }}</strong> ارسال شد
          </p>
          <p class="text-body-2 text-medium-emphasis">
            لطفاً کد 6 رقمی را وارد کنید
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
            @input="handleInput(index, $event)"
            @keydown="handleKeydown(index, $event)"
            @paste="handlePaste"
            :disabled="loading"
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
            :icon="'mdi-alert-circle'"
          >
            <div class="error-message">
              <div class="text-body-1 font-weight-medium mb-2">{{ error.split('\n\n')[0] }}</div>
              <div v-if="error.includes('\n\n')" class="text-body-2 mt-2" style="opacity: 0.9;">
                {{ error.split('\n\n')[1] }}
              </div>
            </div>
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

        <!-- Spam Folder Reminder Message -->
        <transition name="slide-fade">
          <v-alert
            v-if="showSpamMessage"
            type="warning"
            variant="tonal"
            class="mb-4"
            rounded="lg"
            closable
            @click:close="showSpamMessage = false"
            :icon="'mdi-alert'"
          >
            <div class="d-flex align-center">
              <div>
                <div class="text-body-1 font-weight-medium">
                  اگر کد تأیید را دریافت نکرده‌اید، لطفاً پوشه پیام‌های هرزنامه (Spam) خود را بررسی کنید.
                </div>
              </div>
            </div>
          </v-alert>
        </transition>

        <!-- Resend Timer -->
        <div class="text-center mb-4">
          <v-btn
            v-if="canResend"
            variant="text"
            color="primary"
            :disabled="loading"
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
      </v-card-text>

      <v-card-actions class="pa-6 pt-0">
        <v-btn
          color="primary"
          block
          size="large"
          rounded="lg"
          :loading="loading"
          :disabled="!isOtpComplete || loading"
          @click="verifyOtp"
        >
          <span v-if="!loading">تأیید</span>
          <span v-else>در حال تأیید...</span>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useOtpApi, type OtpPurpose } from '~/composables/useOtpApi'

interface Props {
  phone: string
  purpose: OtpPurpose
  username?: string
  onVerified?: (data: any) => void
  onResend?: () => void
}

const props = withDefaults(defineProps<Props>(), {
  username: undefined,
  onVerified: undefined,
  onResend: undefined
})

const emit = defineEmits<{
  verified: [data: any]
  error: [message: string]
}>()

const otpApi = useOtpApi()
const otpDigits = ref<string[]>(['', '', '', '', '', ''])
const inputRefs = ref<(HTMLElement | null)[]>([])
const loading = ref(false)
const error = ref('')
const resending = ref(false)
const canResend = ref(false)
const countdown = ref(120) // 2 minutes
const devModeCode = ref<string | null>(null)
const showSpamMessage = ref(false)
const isVerified = ref(false)
let countdownTimer: NodeJS.Timeout | null = null
let spamMessageTimer: NodeJS.Timeout | null = null

const isOtpComplete = computed(() => {
  return otpDigits.value.every(digit => digit !== '')
})

const otpCode = computed(() => {
  return otpDigits.value.join('')
})

// Request OTP on mount
onMounted(async () => {
  await requestOtp()
  startCountdown()
  startSpamMessageTimer()
})

// Cleanup timer on unmount
watch(() => props.phone, () => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
  if (spamMessageTimer) {
    clearTimeout(spamMessageTimer)
  }
  otpDigits.value = ['', '', '', '', '', '']
  error.value = ''
  devModeCode.value = null
  showSpamMessage.value = false
  isVerified.value = false
  requestOtp()
  startCountdown()
  startSpamMessageTimer()
})

const requestOtp = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await otpApi.requestOtp({
      phone: props.phone,
      username: props.username,
      purpose: props.purpose
    })
    
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
  } catch (err: any) {
    const errorMessage = err.data?.error || err.message || 'خطا در ارسال کد تأیید'
    const helpfulMessage = err.data?.helpful_message || err.data?.hint || ''
    
    error.value = helpfulMessage 
      ? `${errorMessage}\n\n${helpfulMessage}`
      : errorMessage
    
    emit('error', error.value)
  } finally {
    loading.value = false
  }
}

const verifyOtp = async () => {
  if (!isOtpComplete.value) {
    error.value = 'لطفاً کد 6 رقمی را کامل وارد کنید'
    return
  }

  try {
    loading.value = true
    error.value = ''
    
    const response = await otpApi.verifyOtp({
      phone: props.phone,
      username: props.username,
      code: otpCode.value,
      purpose: props.purpose
    })
    
    if (response.success) {
      // Mark as verified and hide spam message
      isVerified.value = true
      showSpamMessage.value = false
      if (spamMessageTimer) {
        clearTimeout(spamMessageTimer)
        spamMessageTimer = null
      }
      
      // Include the OTP code in the response for password reset flow
      const responseWithCode = {
        ...response,
        otp_code: otpCode.value
      }
      if (props.onVerified) {
        props.onVerified(responseWithCode)
      }
      emit('verified', responseWithCode)
    }
  } catch (err: any) {
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
    emit('error', error.value)
  } finally {
    loading.value = false
  }
}

const resendOtp = async () => {
  if (props.onResend) {
    props.onResend()
  }
  // Reset spam message and timer when resending
  showSpamMessage.value = false
  isVerified.value = false
  if (spamMessageTimer) {
    clearTimeout(spamMessageTimer)
  }
  await requestOtp()
  startCountdown()
  startSpamMessageTimer()
}

const handleInput = (index: number, event: Event) => {
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

const handleKeydown = (index: number, event: KeyboardEvent) => {
  // Handle backspace
  if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
    (inputRefs.value[index - 1] as any)?.focus()
  }
  
  // Handle arrow keys
  if (event.key === 'ArrowLeft' && index > 0) {
    (inputRefs.value[index - 1] as any)?.focus()
  }
  if (event.key === 'ArrowRight' && index < 5) {
    (inputRefs.value[index + 1] as any)?.focus()
  }
}

const handlePaste = (event: ClipboardEvent) => {
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

const startSpamMessageTimer = () => {
  // Clear existing timer if any
  if (spamMessageTimer) {
    clearTimeout(spamMessageTimer)
  }
  
  // Reset spam message flag
  showSpamMessage.value = false
  
  // Show spam message after 1 minute (60 seconds) if not verified
  spamMessageTimer = setTimeout(() => {
    if (!isVerified.value) {
      showSpamMessage.value = true
    }
  }, 60000) // 60 seconds = 1 minute
}

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
  if (spamMessageTimer) {
    clearTimeout(spamMessageTimer)
  }
})
</script>

<style scoped>
.otp-verification {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
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

.error-message {
  line-height: 1.8;
}

.error-message .text-body-1 {
  font-size: 15px;
}

.error-message .text-body-2 {
  font-size: 14px;
  line-height: 1.6;
}
</style>

