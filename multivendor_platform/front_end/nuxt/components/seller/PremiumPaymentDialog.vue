<template>
  <v-dialog v-model="localDialog" max-width="600" persistent>
    <v-card rounded="lg">
      <v-card-title class="d-flex align-center justify-space-between pa-4 bg-amber-lighten-5">
        <div class="d-flex align-center gap-2">
          <v-icon color="amber-darken-2" size="28">mdi-crown</v-icon>
          <span class="text-h6 font-weight-bold">ارتقاء به پلن پریمیوم</span>
        </div>
        <v-btn
          icon
          variant="text"
          size="small"
          @click="close"
          :disabled="loading"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="pa-6">
        <!-- Billing Period Selection -->
        <div class="mb-6">
          <h3 class="text-subtitle-1 font-weight-bold mb-3">دوره پرداخت را انتخاب کنید:</h3>
          
          <v-radio-group v-model="billingPeriod" color="amber-darken-2">
            <v-radio
              value="monthly"
              class="billing-option"
            >
              <template #label>
                <div class="d-flex align-center justify-space-between flex-grow-1">
                  <span>ماهانه</span>
                  <span class="font-weight-bold">۱٫۵ میلیون تومان</span>
                </div>
              </template>
            </v-radio>
            
            <v-radio
              value="quarterly"
              class="billing-option"
            >
              <template #label>
                <div class="d-flex align-center justify-space-between flex-grow-1">
                  <span>سه‌ماهه</span>
                  <span class="font-weight-bold">۴٫۵ میلیون تومان</span>
                </div>
              </template>
            </v-radio>
            
            <v-radio
              value="semiannual"
              class="billing-option"
            >
              <template #label>
                <div class="d-flex align-center justify-space-between flex-grow-1">
                  <span>شش‌ماهه</span>
                  <span class="font-weight-bold">۹ میلیون تومان</span>
                </div>
              </template>
            </v-radio>
            
            <v-radio
              value="yearly"
              class="billing-option"
            >
              <template #label>
                <div class="d-flex align-center justify-space-between flex-grow-1 ">
                  <span>سالانه</span>
                  <div class="d-flex align-center gap-2">
                    <v-chip color="green" size="x-small" variant="flat">۲۰٪ تخفیف</v-chip>
                    <span class="font-weight-bold">۱۴٫۴ میلیون تومان</span>
                  </div>
                </div>
              </template>
            </v-radio>
          </v-radio-group>
        </div>

        <!-- Features Summary -->
        <v-card color="amber-lighten-5" variant="flat" class="mb-4">
          <v-card-text class="pa-4">
            <h4 class="text-subtitle-2 font-weight-bold mb-3">امکانات پلن پریمیوم:</h4>
            <v-list density="compact" bg-color="transparent">
              <v-list-item
                v-for="(feature, idx) in premiumFeatures"
                :key="idx"
                class="px-0"
              >
                <template #prepend>
                  <v-icon size="20" color="amber-darken-2">mdi-check-circle</v-icon>
                </template>
                <v-list-item-title class="text-body-2">
                  {{ feature }}
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Discount Code Input -->
        <v-card color="grey-lighten-5" variant="flat" class="mb-4">
          <v-card-text class="pa-4">
            <div class="d-flex align-center gap-2 flex-wrap">
              <v-text-field
                v-model="localDiscountCode"
                label="کد تخفیف"
                placeholder="کد تخفیف خود را وارد کنید"
                variant="outlined"
                density="compact"
                hide-details
                class="flex-grow-1"
                prepend-inner-icon="mdi-tag-outline"
                @keyup.enter="applyDiscountCode"
              >
                <template v-slot:append-inner>
                  <v-btn
                    color="primary"
                    variant="text"
                    size="small"
                    @click="applyDiscountCode"
                    :loading="validatingDiscount"
                    :disabled="!localDiscountCode || validatingDiscount"
                  >
                    اعمال
                  </v-btn>
                </template>
              </v-text-field>
            </div>
            <div v-if="discountError" class="text-caption text-error mt-2">
              {{ discountError }}
            </div>
            <div v-if="appliedDiscount" class="text-caption text-success mt-2 d-flex align-center gap-1">
              <v-icon size="16">mdi-check-circle</v-icon>
              کد تخفیف اعمال شد: {{ appliedDiscount.code }} ({{ discountAmountDisplay }})
            </div>
          </v-card-text>
        </v-card>

        <!-- Price Display -->
        <v-card color="amber" variant="flat" class="mb-4">
          <v-card-text class="pa-4">
            <div v-if="appliedDiscount" class="mb-2">
              <div class="d-flex align-center justify-space-between text-white mb-1">
                <span class="text-body-2">مبلغ اصلی:</span>
                <span class="text-body-2 text-decoration-line-through">{{ basePriceDisplay }}</span>
              </div>
              <div class="d-flex align-center justify-space-between text-white mb-1">
                <span class="text-body-2">تخفیف:</span>
                <span class="text-body-2 font-weight-bold">-{{ discountAmountDisplay }}</span>
              </div>
              <v-divider color="white" class="my-2"></v-divider>
            </div>
            <div class="d-flex align-center justify-space-between">
              <span class="text-subtitle-1 font-weight-medium text-white">مبلغ قابل پرداخت:</span>
              <span class="text-h5 font-weight-bold text-white">{{ finalPriceDisplay }}</span>
            </div>
          </v-card-text>
        </v-card>

        <!-- Error Message -->
        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-4"
          closable
          @click:close="error = null"
        >
          {{ error }}
        </v-alert>

        <!-- Payment Gateway Info -->
        <div class="text-center text-caption text-medium-emphasis">
          <v-icon size="16" class="me-1">mdi-shield-check</v-icon>
          پرداخت امن از طریق درگاه زیبال
        </div>
      </v-card-text>

      <v-divider />

      <v-card-actions class="pa-4">
        <v-btn
          variant="text"
          @click="close"
          :disabled="loading"
        >
          انصراف
        </v-btn>
        <v-spacer />
        <v-btn
          color="amber-darken-2"
          variant="flat"
          size="large"
          @click="handlePayment"
          :loading="loading"
          :disabled="loading"
        >
          <v-icon start>mdi-credit-card</v-icon>
          پرداخت و فعال‌سازی
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { usePaymentApi } from '~/composables/usePaymentApi'
import { useConfetti } from '~/composables/useConfetti'

const props = defineProps<{
  modelValue: boolean
  discountCode?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'success': []
}>()

const paymentApi = usePaymentApi()
const { triggerConfetti } = useConfetti()

const localDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const billingPeriod = ref<'monthly' | 'quarterly' | 'semiannual' | 'yearly'>('monthly')
const loading = ref(false)
const error = ref<string | null>(null)
const localDiscountCode = ref(props.discountCode || '')
const validatingDiscount = ref(false)
const discountError = ref('')
const appliedDiscount = ref<any>(null)

const premiumFeatures = [
  'مشتریان نامحدود',
  'نمایش در فهرست شرکت‌های گواهی‌شده',
  'دستیار شخصی اختصاصی',
  'گزارش ساده عملکرد',
  'محصولات نامحدود',
  'اولویت در پشتیبانی',
]

const basePrices = {
  monthly: 1_500_000,
  quarterly: 4_500_000,
  semiannual: 9_000_000,
  yearly: 14_400_000,
}

const basePriceDisplay = computed(() => {
  const price = basePrices[billingPeriod.value]
  return `${(price / 1_000_000).toFixed(1).replace(/\.0$/, '')} میلیون تومان`
})

const discountAmountDisplay = computed(() => {
  if (!appliedDiscount.value) return ''
  const discount = appliedDiscount.value.discount_amount_toman || 0
  if (appliedDiscount.value.discount_type === 'percentage') {
    return `${appliedDiscount.value.discount_value}%`
  }
  return `${(discount / 1_000_000).toFixed(1).replace(/\.0$/, '')} میلیون تومان`
})

const finalPriceDisplay = computed(() => {
  const basePrice = basePrices[billingPeriod.value]
  let finalPrice = basePrice
  
  if (appliedDiscount.value) {
    // Use nullish coalescing to handle 0 correctly (0 is valid, only null/undefined should fallback)
    finalPrice = appliedDiscount.value.final_amount_toman ?? basePrice
  }
  
  // Handle zero price display
  if (finalPrice === 0) {
    return 'رایگان'
  }
  
  return `${(finalPrice / 1_000_000).toFixed(1).replace(/\.0$/, '')} میلیون تومان`
})

const priceDisplay = computed(() => finalPriceDisplay.value)

async function applyDiscountCode() {
  if (!localDiscountCode.value.trim()) {
    discountError.value = 'لطفاً کد تخفیف را وارد کنید'
    return
  }

  validatingDiscount.value = true
  discountError.value = ''
  appliedDiscount.value = null

  try {
    const { usePaymentApi } = await import('~/composables/usePaymentApi')
    const paymentApi = usePaymentApi()
    const response = await paymentApi.validateDiscountCode(
      localDiscountCode.value.trim().toUpperCase(),
      billingPeriod.value
    )

    if (response.valid) {
      appliedDiscount.value = response
      discountError.value = ''
      // Trigger confetti animation
      triggerConfetti()
    } else {
      discountError.value = response.error || 'کد تخفیف معتبر نیست'
      appliedDiscount.value = null
    }
  } catch (error: any) {
    discountError.value = error?.data?.error || 'خطا در بررسی کد تخفیف'
    appliedDiscount.value = null
  } finally {
    validatingDiscount.value = false
  }
}

// Watch billing period changes to re-validate discount
watch(billingPeriod, () => {
  if (appliedDiscount.value && localDiscountCode.value) {
    applyDiscountCode()
  }
})

// Initialize discount code from props
watch(() => props.discountCode, (newCode) => {
  if (newCode) {
    localDiscountCode.value = newCode
    applyDiscountCode()
  }
}, { immediate: true })

async function handlePayment() {
  loading.value = true
  error.value = null

  try {
    const discountCodeToSend = appliedDiscount.value ? localDiscountCode.value.trim().toUpperCase() : undefined
    const response = await paymentApi.requestPremiumPayment(billingPeriod.value, discountCodeToSend)

    if (response.success && response.payment_url) {
      // Redirect to Zibal payment gateway
      window.location.href = response.payment_url
    } else {
      error.value = response.error || 'خطا در درخواست پرداخت. لطفاً دوباره تلاش کنید.'
    }
  } catch (err: any) {
    console.error('Payment error:', err)
    error.value = 'خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.'
  } finally {
    loading.value = false
  }
}

function close() {
  if (!loading.value) {
    localDialog.value = false
    error.value = null
  }
}
</script>

<style scoped>
.billing-option {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  transition: all 0.2s;
}

.billing-option:hover {
  background: rgba(255, 193, 7, 0.05);
  border-color: rgba(255, 193, 7, 0.5);
}

:deep(.v-selection-control__input) {
  margin-right: 8px !important;
}

:deep(.v-label) {
  width: 100%;
  opacity: 1 !important;
}
</style>

