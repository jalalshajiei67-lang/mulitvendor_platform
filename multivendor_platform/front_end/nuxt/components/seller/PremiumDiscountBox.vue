<template>
  <v-card
    v-if="!isDismissed"
    elevation="2"
    rounded="xl"
    class="premium-discount-box"
    :class="{ 'mobile-layout': isMobile }"
  >
    <v-card-text class="pa-4 pa-md-6">
      <div class="d-flex align-center justify-space-between flex-wrap gap-3">
        <!-- Left Content -->
        <div class="discount-content flex-grow-1">
          <div class="d-flex align-center gap-3 mb-2">
            <v-avatar
              size="48"
              color="amber-darken-2"
              variant="flat"
              class="rounded-lg"
            >
              <v-icon color="white" size="28">mdi-crown</v-icon>
            </v-avatar>
            <div class="flex-grow-1">
              <div class="d-flex align-center gap-2 mb-1 flex-wrap">
                <h3 class="text-h6 font-weight-bold text-high-emphasis mb-0">
                  تخفیف ویژه ارتقاء به پریمیوم
                </h3>
                <v-chip
                  color="error"
                  size="small"
                  variant="flat"
                  class="discount-badge"
                >
                  <v-icon start size="16">mdi-lightning-bolt</v-icon>
                  محدود
                </v-chip>
              </div>
              <p class="text-body-2 text-medium-emphasis mb-0">
                با پلن پریمیوم، مشتریان نامحدود دریافت کنید و فروش خود را افزایش دهید
              </p>
            </div>
          </div>

          <!-- Benefits List -->
          <div class="benefits-list mt-3">
            <div
              v-for="(benefit, idx) in keyBenefits"
              :key="idx"
              class="benefit-item"
            >
              <v-icon size="18" color="success" class="me-2">mdi-check-circle</v-icon>
              <span class="text-body-2">{{ benefit }}</span>
            </div>
          </div>

          <!-- Discount Code Input -->
          <div class="discount-code-section mt-4">
            <div class="d-flex align-center gap-2 flex-wrap">
              <v-text-field
                v-model="discountCode"
                label="کد تخفیف"
                placeholder="کد تخفیف خود را وارد کنید"
                variant="outlined"
                density="compact"
                hide-details
                class="discount-code-input"
                prepend-inner-icon="mdi-tag-outline"
                @keyup.enter="validateDiscountCode"
              >
                <template v-slot:append-inner>
                  <v-btn
                    color="primary"
                    variant="text"
                    size="small"
                    @click="validateDiscountCode"
                    :loading="validatingCode"
                    :disabled="!discountCode || validatingCode"
                  >
                    اعمال
                  </v-btn>
                </template>
              </v-text-field>
            </div>
            <div v-if="discountError" class="text-caption text-error mt-1">
              {{ discountError }}
            </div>
            <div v-if="discountApplied" class="text-caption text-success mt-1 d-flex align-center gap-1">
              <v-icon size="16">mdi-check-circle</v-icon>
              کد تخفیف اعمال شد: {{ discountInfo?.code }}
            </div>
          </div>
        </div>

        <!-- Right Action -->
        <div class="discount-action d-flex flex-column align-center gap-2">
          <v-btn
            color="amber-darken-2"
            variant="flat"
            size="large"
            rounded="lg"
            elevation="2"
            @click="handleUpgrade"
            class="upgrade-btn"
            :class="{ 'w-100': isMobile }"
          >
            <v-icon start>mdi-rocket-launch</v-icon>
            ارتقاء به پریمیوم
          </v-btn>
          <div class="text-center">
            <div class="text-caption text-medium-emphasis">
              <v-icon size="14" class="me-1">mdi-tag</v-icon>
              تخفیف ویژه برای پرداخت سالانه
            </div>
          </div>
        </div>
      </div>
    </v-card-text>

    <!-- Dismiss Button -->
    <v-btn
      icon
      variant="text"
      size="small"
      class="dismiss-btn"
      @click="dismiss"
    >
      <v-icon size="20">mdi-close</v-icon>
    </v-btn>
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
import { useConfetti } from '~/composables/useConfetti'

const emit = defineEmits<{
  'upgrade': [discountCode?: string]
}>()

const { mobile } = useDisplay()
const isMobile = computed(() => mobile.value)
const { triggerConfetti } = useConfetti()

const isDismissed = ref(false)
const DISMISS_KEY = 'premium_discount_dismissed'
const discountCode = ref('')
const validatingCode = ref(false)
const discountError = ref('')
const discountApplied = ref(false)
const discountInfo = ref<any>(null)

const keyBenefits = [
  'مشتریان نامحدود',
  'محصولات نامحدود',
  'نمایش در فهرست گواهی‌شده',
  'پشتیبانی اولویت‌دار',
]

onMounted(() => {
  // Check if user has dismissed this box before
  if (typeof window !== 'undefined') {
    const dismissed = localStorage.getItem(DISMISS_KEY)
    if (dismissed === 'true') {
      isDismissed.value = true
    }
  }
})

function dismiss() {
  isDismissed.value = true
  if (typeof window !== 'undefined') {
    localStorage.setItem(DISMISS_KEY, 'true')
  }
}

async function validateDiscountCode() {
  if (!discountCode.value.trim()) {
    discountError.value = 'لطفاً کد تخفیف را وارد کنید'
    return
  }

  validatingCode.value = true
  discountError.value = ''
  discountApplied.value = false

  try {
    const { usePaymentApi } = await import('~/composables/usePaymentApi')
    const paymentApi = usePaymentApi()
    const response = await paymentApi.validateDiscountCode(
      discountCode.value.trim().toUpperCase(),
      'monthly' // Default, will be updated in payment dialog
    )

    if (response.valid) {
      discountApplied.value = true
      discountInfo.value = response
      discountError.value = ''
      // Trigger confetti animation
      triggerConfetti()
    } else {
      discountError.value = response.error || 'کد تخفیف معتبر نیست'
      discountApplied.value = false
    }
  } catch (error: any) {
    discountError.value = error?.data?.error || 'خطا در بررسی کد تخفیف'
    discountApplied.value = false
  } finally {
    validatingCode.value = false
  }
}

function handleUpgrade() {
  emit('upgrade', discountApplied.value ? discountCode.value.trim().toUpperCase() : undefined)
}
</script>

<style scoped>
.premium-discount-box {
  position: relative;
  background: linear-gradient(135deg, rgba(245, 124, 0, 0.05) 0%, rgba(255, 193, 7, 0.08) 100%);
  border: 2px solid rgba(245, 124, 0, 0.2);
  transition: all 0.3s ease;
}

.premium-discount-box:hover {
  border-color: rgba(245, 124, 0, 0.4);
  box-shadow: 0 8px 24px rgba(245, 124, 0, 0.15);
  transform: translateY(-2px);
}

.discount-content {
  min-width: 0;
}

.discount-badge {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.benefits-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.benefit-item {
  display: flex;
  align-items: center;
  flex: 1 1 auto;
  min-width: 140px;
}

.discount-action {
  min-width: 180px;
}

.upgrade-btn {
  white-space: nowrap;
  font-weight: 600;
}

.dismiss-btn {
  position: absolute;
  top: 8px;
  left: 8px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.dismiss-btn:hover {
  opacity: 1;
}

/* Mobile Layout */
@media (max-width: 960px) {
  .premium-discount-box.mobile-layout .discount-content {
    width: 100%;
  }

  .premium-discount-box.mobile-layout .discount-action {
    width: 100%;
    min-width: unset;
  }

  .premium-discount-box.mobile-layout .benefits-list {
    flex-direction: column;
    gap: 8px;
  }

  .premium-discount-box.mobile-layout .benefit-item {
    min-width: unset;
  }
}

.discount-code-section {
  padding: 12px;
  background: rgba(76, 175, 80, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.discount-code-input {
  max-width: 300px;
}

/* RTL Adjustments */
[dir='rtl'] .dismiss-btn {
  right: 8px;
  left: auto;
}
</style>

