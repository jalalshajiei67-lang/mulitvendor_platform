<template>
  <v-container class="pricing-plans" fluid dir="rtl">
    <!-- Hero block for dashboard context -->
    <v-card class="hero-card rounded-2xl mb-6" elevation="0">
      <v-card-text class="py-6 px-4 px-md-8 d-flex flex-column flex-md-row align-center justify-space-between gap-4">
        <div>
          <div class="d-flex align-center gap-3 mb-2">
            <v-avatar size="42" color="primary" variant="tonal">
              <v-icon color="primary">mdi-crown</v-icon>
            </v-avatar>
            <div>
              <h1 class="text-h6 text-md-h5 font-weight-bold mb-1">پلن‌های عضویت و رشد فروش</h1>
              <p class="text-body-2 text-md-body-1 text-medium-emphasis mb-0">
                بدون نیاز به مهارت فنی یا اصطلاحات پیچیده؛ با راهنمای ساده امروز مشتری‌های بیشتری بگیرید.
              </p>
            </div>
          </div>
          <div class="d-flex flex-wrap gap-2 mt-2">
            <v-chip size="small" variant="tonal" class="pill-tag">
              نمایش اولویت‌دار در نتایج
            </v-chip>
            <v-chip size="small" variant="tonal" class="pill-tag">
              دستیار اختصاصی
            </v-chip>
            <v-chip size="small" variant="tonal" class="pill-tag">
              مشتری نامحدود
            </v-chip>
          </div>
        </div>
        <div class="d-flex flex-column align-end gap-4 align-self-start align-self-md-center">
          <div class="d-flex align-center gap-3 flex-wrap billing-row">
            <span class="text-body-2 text-medium-emphasis">دوره پرداخت</span>
            <v-btn-toggle v-model="billingPeriod" color="primary" density="comfortable" rounded="lg" mandatory class="billing-toggle">
              <v-btn value="monthly" variant="elevated">ماهانه</v-btn>
              <v-btn value="quarterly" variant="tonal">۳ ماهه</v-btn>
              <v-btn value="semiannual" variant="tonal">۶ ماهه</v-btn>
              <v-btn value="yearly" variant="tonal">
                سالانه
                <v-chip size="x-small" class="ml-2" color="success" variant="flat">۲۰٪ تخفیف</v-chip>
              </v-btn>
            </v-btn-toggle>
            <div class="text-caption text-medium-emphasis pr-1 ">هر زمان قابل تغییر</div>
          </div>
          <v-btn
            color="primary"
            variant="flat"
            height="44"
            rounded="lg"
            prepend-icon="mdi-rocket-launch"
            class="text-subtitle-2 upgrade-btn"
            @click="selectedPlan = 'premium'"
            style="margin-left: 38px;"
          >
            ارتقاء ساده به پریمیوم
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <v-row class="mb-4" dense>
      <v-col cols="12" md="6">
        <v-card
          :elevation="selectedPlan === 'free' ? 8 : 2"
          class="rounded-2xl h-100"
          :class="selectedPlan === 'free' ? 'border-primary' : 'border-muted'"
        >
          <v-card-text class="bg-surface-light pa-6">
            <div class="d-flex align-center justify-space-between mb-3">
              <div class="d-flex align-center gap-3">
                <v-avatar size="48" color="grey-lighten-3">
                  <v-icon color="grey-darken-3">mdi-store</v-icon>
                </v-avatar>
                <div>
                  <div class="text-h6 font-weight-bold">پلن رایگان</div>
                  <div class="text-caption text-medium-emphasis">برای شروع و تست بازار</div>
                </div>
              </div>
              <v-chip color="grey" variant="flat" size="small" prepend-icon="mdi-clock-outline">
                همیشه رایگان
              </v-chip>
            </div>
            <div class="d-flex align-center justify-space-between flex-wrap gap-3">
              <div class="d-flex align-end gap-2">
                <span class="text-h3 font-weight-bold">۰</span>
                <span class="text-body-1 text-medium-emphasis">تومان</span>
              </div>
              <div class="d-flex gap-2 flex-wrap">
                <v-chip size="small" variant="tonal" color="primary">۱ مشتری در روز</v-chip>
                <v-chip size="small" variant="tonal" color="primary">محصولات محدود</v-chip>
              </div>
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="pa-6">
            <v-list density="comfortable" lines="two" class="feature-list">
              <v-list-item
                v-for="(feature, idx) in freePlanFeatures"
                :key="`free-${idx}`"
                class="rounded-lg mb-2"
              >
                <template #prepend>
                  <v-avatar
                    size="32"
                    :color="feature.included ? 'green-lighten-4' : 'red-lighten-4'"
                  >
                    <v-icon :color="feature.included ? 'green-darken-2' : 'red-darken-2'">
                      {{ feature.included ? 'mdi-check' : 'mdi-close' }}
                    </v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title :class="!feature.included ? 'text-disabled text-decoration-line-through' : ''">
                  {{ feature.text }}
                </v-list-item-title>
                <v-list-item-subtitle class="d-flex align-center gap-2">
                  <span class="text-caption text-medium-emphasis">{{ feature.description }}</span>
                  <v-chip
                    v-if="feature.badge"
                    size="x-small"
                    color="primary"
                    variant="tonal"
                  >
                    {{ feature.badge }}
                  </v-chip>
                </v-list-item-subtitle>
                <template #append>
                  <v-icon :color="feature.included ? 'primary' : 'grey'">
                    {{ feature.icon }}
                  </v-icon>
                </template>
              </v-list-item>
            </v-list>

            <v-btn
              block
              rounded="lg"
              height="48"
              class="plan-action-btn"
              :color="selectedPlan === 'free' ? 'primary' : 'surface'"
              :variant="selectedPlan === 'free' ? 'flat' : 'tonal'"
              @click="selectedPlan = 'free'"
            >
              {{ selectedPlan === 'free' ? '✓ انتخاب شده' : 'شروع رایگان' }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card
          :elevation="selectedPlan === 'premium' ? 10 : 4"
          class="rounded-2xl overflow-hidden premium-card h-100"
          :class="selectedPlan === 'premium' ? 'border-amber' : 'border-amber-light'"
        >
          <div class="premium-ribbon">
            <div class="d-flex align-center gap-2">
              <v-icon size="16" class="ml-1">mdi-star</v-icon>
              <span>پیشنهاد ویژه</span>
            </div>
            <v-chip
              color="white"
              text-color="amber-darken-3"
              variant="flat"
              prepend-icon="mdi-lightning-bolt"
              size="x-small"
              class="mt-2"
            >
              فعال‌سازی فوری
            </v-chip>
          </div>
          <v-card-text class="pa-6 premium-hero">
            <div class="d-flex align-center gap-3">
              <v-avatar size="48" color="white" variant="tonal">
                <v-icon color="white">mdi-crown</v-icon>
              </v-avatar>
              <div>
                <div class="text-h6 font-weight-bold text-white">پلن پریمیوم</div>
                <div class="text-caption text-white">ویژه رشد سریع و دیده‌شدن</div>
              </div>
            </div>
            <div class="d-flex align-center gap-3 mt-4 flex-wrap">
              <div>
                <div class="text-h4 font-weight-bold text-white">{{ premiumPriceDisplay }}</div>
                <div class="text-caption text-white mt-1">
                  {{ billingCaption }}
                </div>
              </div>
              <v-chip
                color="white"
                text-color="amber-darken-3"
                variant="outlined"
                size="small"
                prepend-icon="mdi-discount-percent"
                v-if="billingPeriod === 'yearly'"
              >
                ۲۰٪ ارزان‌تر
              </v-chip>
            </div>
            <div class="d-flex gap-2 flex-wrap mt-3">
              <v-chip size="small" color="white" text-color="amber-darken-4" variant="flat">مشتری نامحدود</v-chip>
              <v-chip size="small" color="white" text-color="amber-darken-4" variant="flat">پشتیبانی اولویت‌دار</v-chip>
              <v-chip size="small" color="white" text-color="amber-darken-4" variant="flat">گزارش ساده عملکرد</v-chip>
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="pa-6">
            <v-list density="comfortable" lines="two" class="feature-list">
              <v-list-item
                v-for="(feature, idx) in premiumPlanFeatures"
                :key="`premium-${idx}`"
                class="rounded-lg mb-2"
              >
                <template #prepend>
                  <v-avatar
                    size="32"
                    :color="feature.included ? 'amber-lighten-4' : 'red-lighten-4'"
                  >
                    <v-icon :color="feature.included ? 'amber-darken-2' : 'red-darken-2'">
                      {{ feature.included ? 'mdi-check' : 'mdi-close' }}
                    </v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title :class="!feature.included ? 'text-disabled text-decoration-line-through' : ''">
                  {{ feature.text }}
                </v-list-item-title>
                <v-list-item-subtitle class="d-flex align-center gap-2">
                  <span class="text-caption text-medium-emphasis">{{ feature.description }}</span>
                  <v-chip
                    v-if="feature.badge"
                    size="x-small"
                    color="amber"
                    variant="tonal"
                  >
                    {{ feature.badge }}
                  </v-chip>
                </v-list-item-subtitle>
                <template #append>
                  <v-icon :color="feature.included ? 'amber-darken-2' : 'grey'">
                    {{ feature.icon }}
                  </v-icon>
                </template>
              </v-list-item>
            </v-list>

            <v-btn
              block
              rounded="lg"
              height="48"
              class="plan-action-btn"
              :color="selectedPlan === 'premium' ? 'amber-darken-2' : 'amber'"
              :variant="selectedPlan === 'premium' ? 'flat' : 'elevated'"
              prepend-icon="mdi-rocket-launch"
              @click="selectedPlan = 'premium'"
            >
              {{ selectedPlan === 'premium' ? '✓ فعال شده' : 'ارتقاء به پریمیوم' }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Comparison section for dashboard -->
    <v-card class="rounded-2xl mt-2" elevation="0">
      <v-card-text class="pa-4 pa-md-6">
        <div class="d-flex align-center justify-space-between mb-4 flex-wrap gap-2">
          <div class="d-flex align-center gap-2">
            <v-icon color="primary">mdi-compare</v-icon>
            <div>
              <div class="text-subtitle-1 font-weight-bold">مقایسه سریع امکانات</div>
              <div class="text-caption text-medium-emphasis">آنچه در داشبورد فروشنده دریافت می‌کنید</div>
            </div>
          </div>
          <v-chip color="primary" variant="tonal" size="small" prepend-icon="mdi-checkbox-marked-circle-outline">
            مناسب برای تصمیم سریع
          </v-chip>
        </div>

        <div class="comparison-grid">
          <div class="comparison-header">امکانات کلیدی</div>
          <div class="comparison-header text-center">پلن رایگان</div>
          <div class="comparison-header text-center">پلن پریمیوم</div>

          <template v-for="(row, idx) in comparisonRows" :key="`cmp-${idx}`">
            <div class="comparison-label">
              <div class="text-body-2 font-weight-medium">{{ row.label }}</div>
              <div class="text-caption text-medium-emphasis">{{ row.hint }}</div>
            </div>
            <div class="comparison-cell text-center">
              <v-icon :color="row.free ? 'success' : 'disabled'">
                {{ row.free ? 'mdi-check' : 'mdi-close' }}
              </v-icon>
              <div class="text-caption text-medium-emphasis mt-1">{{ row.freeText }}</div>
            </div>
            <div class="comparison-cell text-center">
              <v-icon color="amber-darken-2">mdi-check</v-icon>
              <div class="text-caption text-medium-emphasis mt-1">{{ row.premiumText }}</div>
            </div>
          </template>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type PlanType = 'free' | 'premium' | null
type BillingPeriod = 'monthly' | 'quarterly' | 'semiannual' | 'yearly'

interface Feature {
  text: string
  icon: string
  included: boolean
  description?: string
  badge?: string
}

interface ComparisonRow {
  label: string
  hint: string
  free: boolean
  freeText: string
  premiumText: string
}

const selectedPlan = ref<PlanType>('free')
const billingPeriod = ref<BillingPeriod>('monthly')

const freePlanFeatures: Feature[] = [
  {
    text: 'ایجاد یک فروشگاه مینی رایگان',
    icon: 'mdi-store',
    included: true,
    description: 'با تمام امکانات پایه'
  },
  {
    text: 'ابزارهای تبلیغاتی کامل',
    icon: 'mdi-account-group',
    included: true,
    description: 'معرفی ساده تیم و نمونه کار'
  },
  {
    text: 'دریافت تأییدیه از همکاران',
    icon: 'mdi-award',
    included: true,
    description: 'دعوت همکاران برای تأیید شما'
  },
  {
    text: 'نظرات و بررسی مشتریان قبلی',
    icon: 'mdi-message-text',
    included: true,
    description: 'نظر کوتاه از مشتریان قبلی'
  },
  {
    text: 'فهرست محصولات',
    icon: 'mdi-package-variant',
    included: true,
    description: 'چند محصول اصلی با عکس واضح',
    badge: 'محدود'
  },
  {
    text: 'نمایش در فهرست شرکت‌های گواهی‌شده',
    icon: 'mdi-shield-check',
    included: false,
    description: 'فقط برای کاربران پریمیوم'
  },
  {
    text: 'یک مشتری در روز',
    icon: 'mdi-clock-outline',
    included: true,
    description: 'روزانه یک پیام از خریداران',
    badge: 'محدودیت روزانه'
  },
  {
    text: 'دسترسی به یک دسته اولویت بالا',
    icon: 'mdi-star',
    included: true,
    description: 'برای محصولات غیر استاندارد'
  },
  {
    text: 'دستیار شخصی اختصاصی',
    icon: 'mdi-account-cog',
    included: false
  },
  {
    text: 'داشبورد تحلیلی پیشرفته',
    icon: 'mdi-chart-bar',
    included: false
  },
  {
    text: 'مشتریان نامحدود با فیلتر',
    icon: 'mdi-filter',
    included: false
  }
]

const premiumPlanFeatures: Feature[] = [
  {
    text: 'تمام امکانات پلن رایگان',
    icon: 'mdi-gift',
    included: true,
    description: 'بدون هیچ محدودیتی'
  },
  {
    text: 'مشتریان نامحدود',
    icon: 'mdi-trending-up',
    included: true,
    description: 'پیام‌های بیشتر با فیلتر ساده',
    badge: 'نامحدود'
  },
  {
    text: 'نمایش در فهرست شرکت‌های گواهی‌شده',
    icon: 'mdi-shield-check',
    included: true,
    description: 'دید عمومی و اعتبار بالا'
  },
  {
    text: 'دستیار شخصی اختصاصی',
    icon: 'mdi-account-cog',
    included: true,
    description: 'مدیریت وظایف از راه دور'
  },
  {
    text: 'گزارش ساده عملکرد',
    icon: 'mdi-chart-bar',
    included: true,
    description: 'گزارش خوانا از بازدید و پیام‌ها'
  },
  {
    text: 'فیلتر مشتریان',
    icon: 'mdi-filter',
    included: true,
    description: 'بر اساس دسته، شهر و نیاز'
  },
  {
    text: 'محصولات نامحدود',
    icon: 'mdi-package-variant',
    included: true,
    description: 'بدون محدودیت تعداد'
  },
  {
    text: 'تأییدیه‌های نامحدود',
    icon: 'mdi-award',
    included: true,
    description: 'دعوت همکاران بدون محدودیت'
  },
  {
    text: 'اولویت در پشتیبانی',
    icon: 'mdi-lightning-bolt',
    included: true,
    description: 'پاسخ سریع تلفنی و پیام'
  }
]

const comparisonRows: ComparisonRow[] = [
  {
    label: 'پیام خریداران',
    hint: 'تعداد پیام‌هایی که دریافت می‌کنید',
    free: true,
    freeText: '۱ پیام عمومی در روز',
    premiumText: 'نامحدود با فیلتر دقیق'
  },
  {
    label: 'نمایش در نتایج',
    hint: 'جایگاه شما در لیست و جست‌وجو',
    free: false,
    freeText: 'نمایش عادی',
    premiumText: 'نمایش بالاتر با نشان پریمیوم'
  },
  {
    label: 'گزارش‌ها',
    hint: 'گزارش ساده از بازدید و پیام‌ها',
    free: false,
    freeText: 'نمای کلی ساده',
    premiumText: 'گزارش کامل و خوانا'
  },
  {
    label: 'تعداد محصولات',
    hint: 'حداکثر محصولات فعال',
    free: true,
    freeText: 'محدود',
    premiumText: 'نامحدود'
  },
  {
    label: 'پشتیبانی',
    hint: 'زمان پاسخ و کانال ارتباط',
    free: true,
    freeText: 'پشتیبانی عادی',
    premiumText: 'اولویت‌دار + دستیار اختصاصی'
  }
]

const premiumPriceDisplay = computed(() => {
  const monthly = 1_500_000
  const prices: Record<BillingPeriod, number> = {
    monthly,
    quarterly: monthly * 3,
    semiannual: monthly * 6,
    yearly: Math.round(monthly * 12 * 0.8)
  }
  const value = prices[billingPeriod.value]
  return `${value.toLocaleString('fa-IR')} تومان`
})

const billingCaption = computed(() => {
  switch (billingPeriod.value) {
    case 'monthly':
      return 'پرداخت ماهانه'
    case 'quarterly':
      return 'پرداخت سه‌ماهه'
    case 'semiannual':
      return 'پرداخت شش‌ماهه'
    case 'yearly':
      return 'پرداخت سالانه با تخفیف'
    default:
      return 'پرداخت'
  }
})
</script>

<style scoped>
.pricing-plans {
  max-width: 1200px;
}

.billing-row {
  row-gap: 10px;
}

.billing-toggle .v-btn {
  margin-inline: 2px;
}

.upgrade-btn {
  margin-top: 4px;
}

.plan-action-btn {
  margin-top: 20px;
}

.pill-tag {
  margin: 1px;
  background: rgba(0, 0, 0, 0.05);
  color: #37474f;
}

.hero-card {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(245, 158, 11, 0.08));
  border: 1px solid rgba(59, 130, 246, 0.12);
}

.premium-card {
  position: relative;
}

.premium-hero {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.premium-ribbon {
  position: absolute;
  top: 16px;
  left: 16px;
  background: linear-gradient(90deg, #f59e0b, #d97706);
  color: white;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.feature-list {
  max-height: 520px;
  overflow: hidden;
  padding-bottom: 12px;
}

.feature-list :deep(.v-list-item:last-child) {
  margin-bottom: 12px;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr 0.8fr;
  gap: 12px;
  align-items: stretch;
}

.comparison-header {
  background: rgba(0, 0, 0, 0.04);
  padding: 12px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.95rem;
}

.comparison-label,
.comparison-cell {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 12px;
  padding: 12px;
}

.border-primary {
  border: 2px solid rgba(33, 150, 243, 0.35);
}

.border-muted {
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.border-amber {
  border: 2px solid rgba(245, 158, 11, 0.45);
}

.border-amber-light {
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.max-w-600 {
  max-width: 600px;
}

@media (max-width: 960px) {
  .feature-list {
    max-height: none;
  }

  .comparison-grid {
    grid-template-columns: 1fr;
  }

  .comparison-header {
    text-align: center;
  }
}
</style>

