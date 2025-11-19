<template>
  <v-container fluid class="fill-height auth-container">
    <v-row align="center" justify="center" class="ma-0">
      <v-col cols="12" sm="10" md="8" lg="6" class="pa-0">
        <v-card class="elevation-0 auth-card" rounded="xl">
          <!-- Header -->
          <v-card-text class="pa-6 pb-4 text-center">
            <h1 class="text-h4 font-weight-bold mb-2">ثبت نام در ایندکسو</h1>
            <p class="text-body-2 text-medium-emphasis">لطفاً بگویید می‌خواهید خریدار باشید یا فروشنده</p>
          </v-card-text>

          <!-- Role Selection Cards -->
          <v-card-text class="pa-6 pt-2">
            <v-row class="ma-0">
              <v-col
                v-for="role in roleOptions"
                :key="role.value"
                cols="12"
                sm="4"
                class="pa-2"
              >
                <v-card
                  :class="[
                    'role-card',
                    { 'role-card-selected': form.role === role.value },
                    { 'role-card-flash': !form.role }
                  ]"
                  :color="form.role === role.value ? 'primary' : 'surface-variant'"
                  :variant="form.role === role.value ? 'flat' : 'outlined'"
                  rounded="lg"
                  elevation="0"
                  @click="selectRole(role.value)"
                  class="cursor-pointer transition-all"
                >
                  <v-card-text class="text-center pa-4">
                    <v-icon
                      :icon="role.icon"
                      :color="form.role === role.value ? 'white' : 'primary'"
                      size="48"
                      class="mb-3"
                    />
                    <h3
                      :class="[
                        'text-h6 font-weight-bold mb-2',
                        form.role === role.value ? 'text-white' : 'text-primary'
                      ]"
                    >
                      {{ role.label }}
                    </h3>
                    <p
                      :class="[
                        'text-body-2 mb-0',
                        form.role === role.value ? 'text-white' : 'text-medium-emphasis'
                      ]"
                    >
                      {{ role.description }}
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>

          <!-- Registration Form -->
          <v-card-text class="pa-6 pt-2">
            <v-form ref="formRef" v-model="isValid" @submit.prevent="submit">
              <v-row class="ma-0">
                <!-- First Name -->
                <v-col cols="12" sm="6" class="pa-2">
                  <v-text-field
                    v-model="form.first_name"
                    label="نام *"
                    prepend-inner-icon="mdi-account-outline"
                    variant="outlined"
                    rounded="lg"
                    :rules="firstNameRules"
                    required
                    density="comfortable"
                    dir="rtl"
                  />
                </v-col>

                <!-- Last Name -->
                <v-col cols="12" sm="6" class="pa-2">
                  <v-text-field
                    v-model="form.last_name"
                    label="نام خانوادگی *"
                    prepend-inner-icon="mdi-account-outline"
                    variant="outlined"
                    rounded="lg"
                    :rules="lastNameRules"
                    required
                    density="comfortable"
                    dir="rtl"
                  />
                </v-col>

                <!-- Mobile Number (Username) -->
                <v-col cols="12" class="pa-2">
                  <v-text-field
                    v-model="form.username"
                    label="شماره موبایل *"
                    prepend-inner-icon="mdi-phone"
                    variant="outlined"
                    rounded="lg"
                    :rules="mobileRules"
                    :error="authError?.field === 'username'"
                    :error-messages="authError?.field === 'username' ? [authError.message] : []"
                    required
                    density="comfortable"
                    dir="rtl"
                    type="tel"
                    placeholder="09123456789"
                    hint="شماره موبایل شما همان نام کاربری شما خواهد بود (مثال: 09123456789)"
                    persistent-hint
                    @input="clearError"
                  />
                </v-col>

                <!-- Password -->
                <v-col cols="12" sm="6" class="pa-2">
                  <v-text-field
                    v-model="form.password"
                    label="رمز عبور *"
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
                    density="comfortable"
                    dir="rtl"
                    hint="حداقل ۶ کاراکتر"
                    persistent-hint
                    @input="clearError"
                  />
                </v-col>

                <!-- Confirm Password -->
                <v-col cols="12" sm="6" class="pa-2">
                  <v-text-field
                    v-model="confirmPassword"
                    label="تکرار رمز عبور *"
                    prepend-inner-icon="mdi-lock-check"
                    variant="outlined"
                    rounded="lg"
                    :type="showPassword ? 'text' : 'password'"
                    :rules="confirmPasswordRules"
                    required
                    density="comfortable"
                    dir="rtl"
                  />
                </v-col>
              </v-row>

              <!-- Enhanced Error Display -->
              <transition name="slide-fade">
                <v-alert
                  v-if="authError"
                  :type="getErrorColor(authError.type)"
                  variant="tonal"
                  rounded="lg"
                  class="mt-4 error-alert"
                  :icon="getErrorIcon(authError.type)"
                  closable
                  @click:close="clearError"
                >
                  <div class="error-content">
                    <div class="text-h6 font-weight-bold mb-2">{{ authError.message }}</div>
                    <div v-if="authError.hint" class="text-body-2 mt-2 hint-text">
                      {{ authError.hint }}
                    </div>
                    <div v-if="authError.action === 'login'" class="mt-3">
                      <v-btn
                        variant="text"
                        size="small"
                        color="primary"
                        prepend-icon="mdi-login"
                        to="/login"
                      >
                        ورود به حساب کاربری
                      </v-btn>
                    </div>
                    <div v-if="authError.recoverable && authError.action === 'retry'" class="mt-3">
                      <v-btn
                        variant="outlined"
                        size="small"
                        color="primary"
                        @click="retryRegister"
                        :loading="loading"
                      >
                        تلاش مجدد
                      </v-btn>
                    </div>
                  </div>
                </v-alert>
              </transition>
            </v-form>
          </v-card-text>

          <!-- Submit Button -->
          <v-card-actions class="pa-6 pt-0">
            <v-btn
              color="primary"
              block
              size="x-large"
              rounded="lg"
              :loading="loading"
              :disabled="!isValid || !form.role || loading"
              @click="submit"
              class="font-weight-bold"
            >
              <span v-if="!loading">ثبت‌نام</span>
              <span v-else>در حال ثبت‌نام...</span>
            </v-btn>
          </v-card-actions>

          <!-- Login Link -->
          <v-divider />
          <v-card-text class="text-center pa-4">
            <span class="text-body-2">قبلاً ثبت نام کرده‌اید؟</span>
            <NuxtLink to="/login" class="text-primary font-weight-bold mr-2">
              ورود
            </NuxtLink>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { getErrorIcon, getErrorColor } from '~/utils/authErrors'

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
  title: 'ثبت‌نام | ایندکسو',
  description: 'ثبت نام در ایندکسو برای خرید یا فروش ماشین‌آلات و تجهیزات. ساده و سریع.',
  ogTitle: 'ثبت‌نام در ایندکسو',
  ogDescription: 'ثبت نام در ایندکسو برای خرید یا فروش ماشین‌آلات و تجهیزات. ساده و سریع.',
  ogType: 'website'
})

const authStore = useAuthStore()
const router = useRouter()

const formRef = ref()
const isValid = ref(false)
const showPassword = ref(false)
const confirmPassword = ref('')
const loading = computed(() => authStore.loading)
const authError = computed(() => authStore.authError)

const form = reactive({
  username: '',
  first_name: '',
  last_name: '',
  password: '',
  role: null as string | null
})

const roleOptions = [
  {
    label: 'خریدار',
    value: 'buyer',
    icon: 'mdi-cart',
    description: 'می‌خواهم محصولات و ماشین‌آلات بخرم'
  },
  {
    label: 'فروشنده',
    value: 'seller',
    icon: 'mdi-store',
    description: 'می‌خواهم محصولات و ماشین‌آلات خود را بفروشم'
  },
  {
    label: 'خریدار و فروشنده',
    value: 'both',
    icon: 'mdi-account-multiple',
    description: 'هم می‌خواهم بخرم و هم بفروشم'
  }
]

const selectRole = (role: string) => {
  form.role = role
  // Clear any previous errors
  clearError()
}

const clearError = () => {
  authStore.clearError()
}

const retryRegister = async () => {
  await submit()
}

// Validation rules
const firstNameRules = [
  (value: string) => Boolean(value?.trim()) || 'نام الزامی است',
  (value: string) => (value?.trim()?.length >= 2) || 'نام باید حداقل ۲ کاراکتر باشد'
]

const lastNameRules = [
  (value: string) => Boolean(value?.trim()) || 'نام خانوادگی الزامی است',
  (value: string) => (value?.trim()?.length >= 2) || 'نام خانوادگی باید حداقل ۲ کاراکتر باشد'
]

const mobileRules = [
  (value: string) => Boolean(value?.trim()) || 'شماره موبایل الزامی است',
  (value: string) => {
    // Remove spaces, dashes, and parentheses for validation
    const cleaned = value?.replace(/[\s\-()]/g, '') || ''
    // Check if it starts with a valid Iranian mobile prefix
    // Accept: 09XXXXXXXXX, +98XXXXXXXXXX, 0098XXXXXXXXXX, 98XXXXXXXXXX, 9XXXXXXXXX
    const mobileRegex = /^(\+98|0098|98|0)?9\d{9}$/
    if (!mobileRegex.test(cleaned)) {
      return 'شماره موبایل درست نیست. لطفاً شماره را صحیح وارد کنید (مثال: 09123456789)'
    }
    // Check minimum length (should be at least 10 digits after cleaning)
    const digitsOnly = cleaned.replace(/\D/g, '')
    if (digitsOnly.length < 10 || digitsOnly.length > 13) {
      return 'شماره موبایل باید ۱۱ رقم باشد (مثال: 09123456789)'
    }
    return true
  }
]

const passwordRules = [
  (value: string) => Boolean(value) || 'رمز عبور الزامی است',
  (value: string) => (value?.length >= 6) || 'رمز عبور باید حداقل ۶ کاراکتر باشد',
  (value: string) => {
    if (!value || value.length < 6) return true
    // Check for at least one letter and one number for better security
    const hasLetter = /[a-zA-Z\u0600-\u06FF]/.test(value)
    const hasNumber = /\d/.test(value)
    if (!hasLetter || !hasNumber) {
      return 'رمز عبور باید شامل حروف و اعداد باشد'
    }
    return true
  }
]

const confirmPasswordRules = [
  (value: string) => Boolean(value) || 'تکرار رمز عبور الزامی است',
  (value: string) => value === form.password || 'رمز عبور مطابقت ندارد'
]

const submit = async () => {
  if (!formRef.value) return

  const result = await formRef.value.validate()
  if (!result.valid) return

  if (!form.role) {
    return
  }

  clearError()

  try {
    // Prepare payload - mobile number is username
    // Backend will normalize the mobile number format
    const payload = {
      username: form.username.trim(), // Backend will clean and normalize
      first_name: form.first_name.trim(),
      last_name: form.last_name.trim(),
      password: form.password,
      role: form.role
    }

    const response = await authStore.register(payload)

    if (response?.user?.is_staff || response?.user?.is_superuser) {
      return router.push('/admin/dashboard')
    }
    if (response?.user?.role === 'seller' || response?.user?.role === 'both') {
      return router.push('/seller/dashboard')
    }

    router.push('/buyer/dashboard')
  } catch (err: any) {
    console.error('Registration failed', err)
    // Error is already handled by the auth store
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  padding: 16px;
}

.auth-container {
  direction: rtl;
  text-align: right;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-card {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
}

.role-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.role-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.role-card-selected {
  border-color: rgb(var(--v-theme-primary)) !important;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3) !important;
  animation: none !important;
}

.role-card-flash {
  animation: flash-pulse 2s ease-in-out infinite;
}

@keyframes flash-pulse {
  0%, 100% {
    border-color: transparent;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transform: scale(1);
  }
  50% {
    border-color: rgb(var(--v-theme-primary));
    box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.4);
    transform: scale(1.02);
  }
}

.cursor-pointer {
  cursor: pointer;
}

.transition-all {
  transition: all 0.3s ease;
}

:deep(.v-field__input) {
  text-align: right;
  direction: rtl;
}

:deep(.v-field__prepend-inner) {
  padding-left: 12px;
  padding-right: 0;
}

:deep(.v-field__append-inner) {
  padding-right: 12px;
  padding-left: 0;
}

:deep(.v-label) {
  right: 0;
  left: auto;
}

/* Mobile optimizations */
@media (max-width: 600px) {
  .fill-height {
    padding: 8px;
  }

  .auth-card {
    border-radius: 16px !important;
  }

  .role-card {
    min-height: 140px;
  }

  :deep(.v-card-text) {
    padding: 16px !important;
  }
}

/* RTL support for icons */
:deep(.v-icon) {
  direction: ltr;
}

/* Focus styles */
:deep(.v-field--focused) {
  border-color: rgb(var(--v-theme-primary)) !important;
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
