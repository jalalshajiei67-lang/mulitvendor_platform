<template>
  <v-dialog v-model="dialog" max-width="800" persistent dir="rtl">
    <v-card class="rounded-xl">
      <v-card-title class="d-flex align-center justify-space-between pa-6 bg-success-lighten-5">
        <div class="d-flex align-center gap-3">
          <v-avatar color="success" size="48">
            <v-icon color="white">mdi-file-sign</v-icon>
          </v-avatar>
          <div>
            <div class="text-h6 font-weight-bold">فعال‌سازی پلن کمیسیونی</div>
            <div class="text-caption text-medium-emphasis">ثبت درخواست و آپلود مدارک</div>
          </div>
        </div>
        <v-btn icon="mdi-close" variant="text" @click="close"></v-btn>
      </v-card-title>

      <v-card-text class="pa-6">
        <!-- Stepper -->
        <v-stepper v-model="currentStep" alt-labels class="elevation-0 mb-4">
          <v-stepper-header>
            <v-stepper-item
              :complete="currentStep > 1"
              :value="1"
              title="بررسی اطلاعات"
              icon="mdi-account-check"
            ></v-stepper-item>
            <v-divider></v-divider>
            <v-stepper-item
              :complete="currentStep > 2"
              :value="2"
              title="قبول شرایط"
              icon="mdi-file-document-check"
            ></v-stepper-item>
            <v-divider></v-divider>
            <v-stepper-item
              :complete="currentStep > 3"
              :value="3"
              title="آپلود قرارداد"
              icon="mdi-file-upload"
            ></v-stepper-item>
            <v-divider></v-divider>
            <v-stepper-item
              :value="4"
              title="ضمانت‌نامه بانکی"
              icon="mdi-bank"
            ></v-stepper-item>
          </v-stepper-header>
        </v-stepper>

        <!-- Step 1: Profile Check -->
        <div v-if="currentStep === 1" class="step-content">
          <!-- Gold Tier Requirement Alert -->
          <v-alert
            v-if="gamificationTier && !gamificationTier.has_gold_tier"
            type="warning"
            variant="tonal"
            class="mb-4"
            border="start"
            border-color="warning"
          >
            <div class="d-flex align-center gap-3">
              <v-avatar color="warning" size="48">
                <v-icon color="white">mdi-trophy</v-icon>
              </v-avatar>
              <div class="flex-grow-1">
                <div class="text-subtitle-2 font-weight-bold mb-1">نیاز به نشان طلایی (Gold)</div>
                <div class="text-body-2 mb-2">
                  برای فعال‌سازی پلن کمیسیونی، باید نشان طلایی را دریافت کنید.
                </div>
                <div class="text-caption text-medium-emphasis">
                  وضعیت فعلی: <strong>{{ getTierName(gamificationTier.current_tier) }}</strong> 
                  (امتیاز: {{ gamificationTier.current_points }}, اعتبار: {{ gamificationTier.current_reputation.toFixed(1) }})
                </div>
                <div class="text-caption text-medium-emphasis mt-1">
                  نیاز به: <strong>نشان طلایی</strong> (حداقل ۵۰۰ امتیاز و ۶۰ اعتبار)
                </div>
              </div>
            </div>
          </v-alert>

          <v-alert
            v-else-if="gamificationTier && gamificationTier.has_gold_tier"
            type="success"
            variant="tonal"
            class="mb-4"
          >
            <div class="d-flex align-center gap-2">
              <v-icon color="success">mdi-trophy</v-icon>
              <div>
                <div class="text-subtitle-2 font-weight-bold">✓ نشان طلایی دریافت شده</div>
                <div class="text-body-2">شما نشان طلایی را دریافت کرده‌اید و می‌توانید پلن کمیسیونی را فعال کنید.</div>
              </div>
            </div>
          </v-alert>

          <v-alert
            v-if="missingRequirements.length > 0 && missingRequirements.filter(r => r !== 'gold_tier').length > 0"
            type="warning"
            variant="tonal"
            class="mb-4"
          >
            <div class="text-subtitle-2 font-weight-bold mb-2">اطلاعات ناقص</div>
            <div class="text-body-2">لطفاً ابتدا اطلاعات زیر را در پروفایل خود تکمیل کنید:</div>
            <v-list density="compact" class="bg-transparent mt-2">
              <v-list-item v-for="req in missingRequirements.filter(r => r !== 'gold_tier')" :key="req">
                <template #prepend>
                  <v-icon color="warning">mdi-alert-circle</v-icon>
                </template>
                <v-list-item-title>{{ translateRequirement(req) }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-alert>

          <v-alert 
            v-if="missingRequirements.length === 0 || (missingRequirements.length === 1 && missingRequirements[0] === 'gold_tier')"
            type="success" 
            variant="tonal" 
            class="mb-4"
          >
            <div class="text-subtitle-2 font-weight-bold mb-2">✓ اطلاعات کامل است</div>
            <div class="text-body-2">تمام اطلاعات پروفایل شما تکمیل شده است.</div>
          </v-alert>

          <v-card variant="outlined" class="rounded-lg">
            <v-card-text>
              <div class="text-subtitle-2 font-weight-bold mb-3">شرایط پلن کمیسیونی:</div>
              <v-list density="compact">
                <v-list-item>
                  <template #prepend>
                    <v-icon color="success">mdi-check-circle</v-icon>
                  </template>
                  <v-list-item-title>بدون هزینه ثابت ماهانه</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <template #prepend>
                    <v-icon color="success">mdi-check-circle</v-icon>
                  </template>
                  <v-list-item-title>کمیسیون ٪۵ برای فروش زیر ۱ میلیارد تومان</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <template #prepend>
                    <v-icon color="success">mdi-check-circle</v-icon>
                  </template>
                  <v-list-item-title>کمیسیون ٪۳ برای فروش بالای ۱ میلیارد تومان</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <template #prepend>
                    <v-icon color="info">mdi-information</v-icon>
                  </template>
                  <v-list-item-title>مشتریان و محصولات نامحدود</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <template #prepend>
                    <v-icon color="warning">mdi-trophy</v-icon>
                  </template>
                  <v-list-item-title class="font-weight-bold">نیاز به دریافت نشان طلایی (Gold) از سیستم گیمیفیکیشن</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <template #prepend>
                    <v-icon color="warning">mdi-file-sign</v-icon>
                  </template>
                  <v-list-item-title class="font-weight-bold">نیاز به امضای قرارداد و ارائه ضمانت‌نامه بانکی</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </div>

        <!-- Step 2: Terms & Conditions -->
        <div v-if="currentStep === 2" class="step-content">
          <v-card variant="outlined" class="rounded-lg mb-4">
            <v-card-text>
              <div class="text-subtitle-2 font-weight-bold mb-3">شرایط و ضوابط پلن کمیسیونی</div>
              <div class="terms-content">
                <p class="mb-3">با فعال‌سازی پلن کمیسیونی، شما موارد زیر را می‌پذیرید:</p>
                <ol class="pr-4">
                  <li class="mb-2">کمیسیون از هر فروش به صورت خودکار محاسبه و کسر می‌شود</li>
                  <li class="mb-2">تسویه‌حساب فروش بعد از کسر کمیسیون انجام خواهد شد</li>
                  <li class="mb-2">قرارداد رسمی امضا شده و ضمانت‌نامه بانکی الزامی است</li>
                  <li class="mb-2">تغییر پلن به اشتراکی یا رایگان با هماهنگی قبلی امکان‌پذیر است</li>
                  <li class="mb-2">فعال‌سازی نهایی پس از تأیید ادمین انجام می‌شود</li>
                  <li class="mb-2">کمیسیون از مبلغ کل سفارش (بدون هزینه حمل و مالیات) محاسبه می‌شود</li>
                  <li class="mb-2">ضمانت‌نامه بانکی باید معتبر و دارای تاریخ انقضا مشخص باشد</li>
                </ol>
              </div>
            </v-card-text>
          </v-card>

          <v-checkbox
            v-model="termsAccepted"
            color="success"
            hide-details
          >
            <template #label>
              <span class="text-body-2">
                شرایط و ضوابط را مطالعه کرده‌ام و 
                <strong class="text-success">قبول دارم</strong>
              </span>
            </template>
          </v-checkbox>
        </div>

        <!-- Step 3: Contract Upload -->
        <div v-if="currentStep === 3" class="step-content">
          <v-alert type="info" variant="tonal" class="mb-4">
            <div class="text-subtitle-2 font-weight-bold mb-2">دانلود و امضای قرارداد</div>
            <div class="text-body-2 mb-3">
              لطفاً قرارداد را دانلود، امضا و اسکن کنید و سپس فایل امضا شده را آپلود نمایید.
            </div>
            <v-btn
              color="info"
              variant="tonal"
              prepend-icon="mdi-download"
              @click="downloadContract"
            >
              دانلود قرارداد
            </v-btn>
          </v-alert>

          <v-file-input
            v-model="contractFile"
            label="آپلود قرارداد امضا شده"
            prepend-icon="mdi-paperclip"
            accept=".pdf,.jpg,.jpeg,.png"
            variant="outlined"
            color="success"
            :rules="[validateContractFile]"
            hint="فرمت‌های مجاز: PDF, JPG, PNG (حداکثر ۱۰ مگابایت)"
            persistent-hint
            class="mb-2"
            @update:model-value="validateContractFile"
          >
            <template #selection="{ fileNames }">
              <v-chip color="success" label>
                <v-icon start>mdi-file-check</v-icon>
                {{ fileNames[0] }}
              </v-chip>
            </template>
          </v-file-input>

          <v-alert v-if="contractFile" type="success" variant="tonal" density="compact">
            <v-icon start>mdi-check-circle</v-icon>
            فایل قرارداد آماده آپلود است
          </v-alert>
        </div>

        <!-- Step 4: Bank Guarantee -->
        <div v-if="currentStep === 4" class="step-content">
          <v-alert type="info" variant="tonal" class="mb-4">
            <div class="text-subtitle-2 font-weight-bold mb-2">ضمانت‌نامه بانکی</div>
            <div class="text-body-2">
              لطفاً ضمانت‌نامه بانکی معتبر خود را آپلود کنید. این سند باید توسط بانک صادر شده باشد.
            </div>
          </v-alert>

          <v-text-field
            v-model="guaranteeAmount"
            label="مبلغ ضمانت‌نامه (تومان)"
            variant="outlined"
            type="number"
            prepend-inner-icon="mdi-currency-usd"
            color="success"
            :rules="[v => !!v || 'مبلغ ضمانت‌نامه الزامی است']"
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="guaranteeExpiry"
            label="تاریخ انقضا"
            variant="outlined"
            type="date"
            prepend-inner-icon="mdi-calendar"
            color="success"
            :rules="[validateExpiryDate]"
            class="mb-4"
            :min="new Date().toISOString().split('T')[0]"
          ></v-text-field>

          <v-file-input
            v-model="guaranteeFile"
            label="آپلود ضمانت‌نامه بانکی"
            prepend-icon="mdi-bank"
            accept=".pdf,.jpg,.jpeg,.png"
            variant="outlined"
            color="success"
            :rules="[validateGuaranteeFile]"
            hint="فرمت‌های مجاز: PDF, JPG, PNG (حداکثر ۱۰ مگابایت)"
            persistent-hint
            @update:model-value="validateGuaranteeFile"
          >
            <template #selection="{ fileNames }">
              <v-chip color="success" label>
                <v-icon start>mdi-file-check</v-icon>
                {{ fileNames[0] }}
              </v-chip>
            </template>
          </v-file-input>

          <v-alert v-if="guaranteeFile" type="success" variant="tonal" density="compact" class="mt-3">
            <v-icon start>mdi-check-circle</v-icon>
            فایل ضمانت‌نامه آماده آپلود است
          </v-alert>
        </div>

        <!-- Error/Success Messages -->
        <v-alert v-if="errorMessage" type="error" variant="tonal" class="mt-4">
          {{ errorMessage }}
        </v-alert>

        <v-alert v-if="successMessage" type="success" variant="tonal" class="mt-4">
          {{ successMessage }}
        </v-alert>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          v-if="currentStep > 1"
          variant="text"
          @click="previousStep"
          :disabled="loading"
        >
          قبلی
        </v-btn>
        <v-btn
          v-if="currentStep < 4"
          color="success"
          variant="flat"
          @click="nextStep"
          :disabled="!canProceed"
          :loading="loading"
        >
          بعدی
        </v-btn>
        <v-btn
          v-if="currentStep === 4"
          color="success"
          variant="flat"
          @click="submitActivation"
          :disabled="!canSubmit"
          :loading="loading"
        >
          ثبت نهایی درخواست
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'success': []
}>()

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const currentStep = ref(1)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Step 1
const missingRequirements = ref<string[]>([])
const canActivate = ref(false)
const gamificationTier = ref<{
  current_tier: string
  current_points: number
  current_reputation: number
  has_gold_tier: boolean
} | null>(null)

// Step 2
const termsAccepted = ref(false)

// Step 3
const contractFile = ref<File[] | null>(null)

// Step 4
const guaranteeFile = ref<File[] | null>(null)
const guaranteeAmount = ref('')
const guaranteeExpiry = ref('')

const canProceed = computed(() => {
  if (currentStep.value === 1) {
    // Can proceed only if all requirements are met (including gold tier)
    return missingRequirements.value.length === 0
  }
  if (currentStep.value === 2) {
    return termsAccepted.value
  }
  if (currentStep.value === 3) {
    return contractFile.value && contractFile.value.length > 0
  }
  return false
})

const canSubmit = computed(() => {
  return (
    guaranteeFile.value &&
    guaranteeFile.value.length > 0 &&
    guaranteeAmount.value &&
    guaranteeExpiry.value
  )
})

function translateRequirement(req: string): string {
  const translations: Record<string, string> = {
    store_name: 'نام فروشگاه',
    contact_email: 'ایمیل تماس',
    contact_phone: 'تلفن تماس',
    address: 'آدرس',
    phone: 'شماره تلفن',
    vendor_profile: 'پروفایل فروشنده',
    user_profile: 'پروفایل کاربری',
    gold_tier: 'نشان طلایی'
  }
  return translations[req] || req
}

function getTierName(tier: string): string {
  const tierNames: Record<string, string> = {
    inactive: 'غیرفعال',
    bronze: 'برنزی',
    silver: 'نقره‌ای',
    gold: 'طلایی',
    diamond: 'الماس'
  }
  return tierNames[tier] || tier
}

function validateContractFile(files: File[] | null): string | true {
  if (!files || files.length === 0) {
    return 'آپلود قرارداد الزامی است'
  }
  
  const file = files[0]
  const maxSize = 10 * 1024 * 1024 // 10MB
  const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
  const allowedExtensions = ['.pdf', '.jpg', '.jpeg', '.png']
  
  // Check file size
  if (file.size > maxSize) {
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2)
    return `حجم فایل باید کمتر از ۱۰ مگابایت باشد. حجم فایل شما: ${sizeMB} مگابایت`
  }
  
  // Check file type
  const fileName = file.name.toLowerCase()
  const isValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext))
  const isValidType = allowedTypes.includes(file.type)
  
  if (!isValidExtension && !isValidType) {
    return 'فرمت فایل مجاز نیست. فرمت‌های مجاز: PDF, JPG, PNG'
  }
  
  return true
}

function validateGuaranteeFile(files: File[] | null): string | true {
  if (!files || files.length === 0) {
    return 'آپلود ضمانت‌نامه الزامی است'
  }
  
  const file = files[0]
  const maxSize = 10 * 1024 * 1024 // 10MB
  const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
  const allowedExtensions = ['.pdf', '.jpg', '.jpeg', '.png']
  
  // Check file size
  if (file.size > maxSize) {
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2)
    return `حجم فایل باید کمتر از ۱۰ مگابایت باشد. حجم فایل شما: ${sizeMB} مگابایت`
  }
  
  // Check file type
  const fileName = file.name.toLowerCase()
  const isValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext))
  const isValidType = allowedTypes.includes(file.type)
  
  if (!isValidExtension && !isValidType) {
    return 'فرمت فایل مجاز نیست. فرمت‌های مجاز: PDF, JPG, PNG'
  }
  
  return true
}

function validateExpiryDate(date: string | null): string | true {
  if (!date) {
    return 'تاریخ انقضا الزامی است'
  }
  
  const expiryDate = new Date(date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  if (expiryDate < today) {
    return 'تاریخ انقضا نمی‌تواند در گذشته باشد'
  }
  
  return true
}

async function checkProfileStatus() {
  loading.value = true
  errorMessage.value = ''
  
  try {
    const { $api } = useNuxtApp()
    const response = await $api('/api/users/seller/commission/status/')
    
    canActivate.value = response.can_activate
    missingRequirements.value = response.missing_requirements || []
    gamificationTier.value = response.gamification_tier || null
  } catch (error: any) {
    if (error.response) {
      const errorData = error.response.data
      errorMessage.value = errorData.message || errorData.error || 'خطا در بررسی وضعیت'
    } else if (error.request) {
      errorMessage.value = 'خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید.'
    } else {
      errorMessage.value = 'خطا در بررسی وضعیت. لطفاً دوباره تلاش کنید.'
    }
  } finally {
    loading.value = false
  }
}

function downloadContract() {
  // TODO: Implement contract download
  window.open('/static/commission-contract-template.pdf', '_blank')
}

function nextStep() {
  if (currentStep.value === 2 && termsAccepted.value) {
    // Activate plan when accepting terms
    activateCommissionPlan()
  } else {
    currentStep.value++
  }
}

function previousStep() {
  currentStep.value--
}

async function activateCommissionPlan() {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  
  try {
    const { $api } = useNuxtApp()
    const response = await $api('/api/users/seller/commission/activate/', {
      method: 'POST',
      body: { terms_accepted: true }
    })
    
    if (response.success) {
      successMessage.value = response.message || 'درخواست فعال‌سازی با موفقیت ثبت شد'
      currentStep.value++
      // Refresh status to get updated info
      await checkProfileStatus()
    }
  } catch (error: any) {
    // Handle different error types
    if (error.response) {
      // Server responded with error
      const errorData = error.response.data
      
      // Check if plan is already activated
      if (error.response.status === 400 && errorData.error === 'Commission plan already activated') {
        errorMessage.value = errorData.message || 'پلن کمیسیونی شما قبلاً فعال شده است'
        // Refresh status and close dialog
        await checkProfileStatus()
        setTimeout(() => {
          emit('success')
          close()
        }, 2000)
        return
      }
      
      // Check if activation is in progress
      if (error.response.status === 400 && errorData.error === 'Activation already in progress') {
        errorMessage.value = errorData.message || 'درخواست فعال‌سازی شما در حال بررسی است'
        currentStep.value = 3 // Move to contract upload step
        await checkProfileStatus()
        return
      }
      
      // Show the detailed error message from backend (includes gold tier info)
      errorMessage.value = errorData.message || errorData.error || 'خطا در فعال‌سازی پلن'
      
      // Refresh status to update tier info if it's a validation error
      if (error.response.status === 400) {
        await checkProfileStatus()
      }
    } else if (error.request) {
      // Request was made but no response received
      errorMessage.value = 'خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید و دوباره تلاش کنید.'
    } else {
      // Something else happened
      errorMessage.value = 'خطای غیرمنتظره رخ داد. لطفاً دوباره تلاش کنید.'
    }
  } finally {
    loading.value = false
  }
}

async function submitActivation() {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  
  try {
    const { $api } = useNuxtApp()
    
    // Upload contract
    if (contractFile.value && contractFile.value.length > 0) {
      try {
        const contractFormData = new FormData()
        contractFormData.append('contract_document', contractFile.value[0])
        
        const contractResponse = await $api('/api/users/seller/commission/upload-contract/', {
          method: 'POST',
          body: contractFormData
        })
        
        if (contractResponse.success) {
          successMessage.value = contractResponse.message || 'قرارداد با موفقیت آپلود شد'
        }
      } catch (error: any) {
        if (error.response) {
          const errorData = error.response.data
          errorMessage.value = errorData.message || errorData.error || 'خطا در آپلود قرارداد'
        } else {
          errorMessage.value = 'خطا در آپلود قرارداد. لطفاً دوباره تلاش کنید.'
        }
        return // Stop if contract upload fails
      }
    }
    
    // Upload bank guarantee
    if (guaranteeFile.value && guaranteeFile.value.length > 0) {
      try {
        const guaranteeFormData = new FormData()
        guaranteeFormData.append('bank_guarantee_document', guaranteeFile.value[0])
        guaranteeFormData.append('bank_guarantee_amount', guaranteeAmount.value)
        guaranteeFormData.append('bank_guarantee_expiry', guaranteeExpiry.value)
        
        const guaranteeResponse = await $api('/api/users/seller/commission/upload-guarantee/', {
          method: 'POST',
          body: guaranteeFormData
        })
        
        if (guaranteeResponse.success) {
          successMessage.value = 'درخواست شما با موفقیت ثبت شد. پس از بررسی و تأیید ادمین، پلن شما فعال خواهد شد.'
          
          setTimeout(() => {
            emit('success')
            close()
          }, 2000)
        }
      } catch (error: any) {
        if (error.response) {
          const errorData = error.response.data
          errorMessage.value = errorData.message || errorData.error || 'خطا در آپلود ضمانت‌نامه'
        } else if (error.request) {
          errorMessage.value = 'خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید.'
        } else {
          errorMessage.value = 'خطا در آپلود ضمانت‌نامه. لطفاً دوباره تلاش کنید.'
        }
      }
    } else {
      errorMessage.value = 'لطفاً فایل ضمانت‌نامه را آپلود کنید'
    }
  } catch (error: any) {
    if (error.response) {
      const errorData = error.response.data
      errorMessage.value = errorData.message || errorData.error || 'خطا در ثبت درخواست'
    } else if (error.request) {
      errorMessage.value = 'خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید.'
    } else {
      errorMessage.value = 'خطای غیرمنتظره رخ داد. لطفاً دوباره تلاش کنید.'
    }
  } finally {
    loading.value = false
  }
}

function close() {
  dialog.value = false
  currentStep.value = 1
  termsAccepted.value = false
  contractFile.value = null
  guaranteeFile.value = null
  guaranteeAmount.value = ''
  guaranteeExpiry.value = ''
  errorMessage.value = ''
  successMessage.value = ''
  gamificationTier.value = null
}

watch(dialog, (newValue) => {
  if (newValue) {
    checkProfileStatus()
  }
})
</script>

<style scoped>
.step-content {
  min-height: 300px;
}

.terms-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 16px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
}

.terms-content ol {
  line-height: 1.8;
}
</style>
