<template>
  <v-container class="pricing-plans" fluid dir="rtl">
    <div class="text-center mb-8">
      <h1 class="text-h5 text-md-h4 font-weight-bold mb-3">
        پلن مناسب خود را انتخاب کنید
      </h1>
      <p class="text-body-2 text-md-body-1 text-medium-emphasis mx-auto max-w-600">
        با پلن رایگان شروع کنید و با ارتقاء به پریمیوم، به امکانات پیشرفته و مشتریان نا محدود دسترسی پیدا کنید
      </p>
    </div>

    <v-row class="mb-4" dense>
      <v-col cols="12" md="6">
        <v-card
          :elevation="selectedPlan === 'free' ? 8 : 4"
          class="rounded-xl"
          :class="selectedPlan === 'free' ? 'border-primary' : 'border-muted'"
        >
          <v-card-text class="bg-surface-light pa-6">
            <div class="d-flex align-center gap-3 mb-3">
              <v-avatar size="48" color="grey-lighten-3">
                <v-icon color="grey-darken-3">mdi-store</v-icon>
              </v-avatar>
              <div>
                <div class="text-h6 font-weight-bold">پلن رایگان</div>
                <div class="text-caption text-medium-emphasis">برای شروع کسب‌وکار</div>
              </div>
            </div>
            <div class="d-flex align-end gap-2">
              <span class="text-h3 font-weight-bold">۰</span>
              <span class="text-body-1 text-medium-emphasis">تومان</span>
            </div>
            <div class="text-caption text-medium-emphasis mt-1">برای همیشه رایگان</div>
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
              class="mt-4"
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
          :elevation="selectedPlan === 'premium' ? 10 : 6"
          class="rounded-xl overflow-hidden premium-card"
          :class="selectedPlan === 'premium' ? 'border-amber' : 'border-amber-light'"
        >
          <div class="premium-ribbon">
            <v-icon size="16" class="ml-1">mdi-star</v-icon>
            پیشنهاد ویژه
          </div>
          <v-card-text class="pa-6 premium-hero">
            <div class="d-flex align-center gap-3 mb-3">
              <v-avatar size="48" color="white" variant="tonal">
                <v-icon color="white">mdi-crown</v-icon>
              </v-avatar>
              <div>
                <div class="text-h6 font-weight-bold text-white">پلن پریمیوم</div>
                <div class="text-caption text-white">برای کسب‌وکارهای حرفه‌ای</div>
              </div>
            </div>
            <div class="text-h4 font-weight-bold text-white">۱ میلیون و ۵۰۰ هزار تومان</div>
            <div class="text-caption text-white mt-1">یک ماه</div>
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
              class="mt-4"
              :color="selectedPlan === 'premium' ? 'amber-darken-2' : 'amber'"
              :variant="selectedPlan === 'premium' ? 'flat' : 'elevated'"
              @click="selectedPlan = 'premium'"
            >
              {{ selectedPlan === 'premium' ? '✓ انتخاب شده' : 'ارتقاء به پریمیوم' }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'

type PlanType = 'free' | 'premium' | null

interface Feature {
  text: string
  icon: string
  included: boolean
  description?: string
  badge?: string
}

const selectedPlan = ref<PlanType>('free')

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
    description: 'معرفی تیم، دستاوردها و تصاویر نمایشگاهی'
  },
  {
    text: 'دریافت تأییدیه از همکاران',
    icon: 'mdi-award',
    included: true,
    description: 'دعوت از همکاران خارج از پلتفرم'
  },
  {
    text: 'نظرات و بررسی مشتریان قبلی',
    icon: 'mdi-message-text',
    included: true,
    description: 'دعوت مشتریان قبلی برای امتیازدهی'
  },
  {
    text: 'فهرست محصولات',
    icon: 'mdi-package-variant',
    included: true,
    description: 'تصاویر تمیز بدون واترمارک یا لوگو',
    badge: 'محدود'
  },
  {
    text: 'نمایش در فهرست شرکت‌های گواهی‌شده',
    icon: 'mdi-shield-check',
    included: false,
    description: 'فقط برای کاربران پریمیوم'
  },
  {
    text: 'یک سرنخ مشتری در روز',
    icon: 'mdi-clock-outline',
    included: true,
    description: 'از استخر عمومی سرنخ‌های مشتری',
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
    text: 'سرنخ‌های نامحدود با فیلتر',
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
    text: 'سرنخ‌های مشتری نامحدود',
    icon: 'mdi-trending-up',
    included: true,
    description: 'با فیلتر دسته‌بندی و تطابق نیش',
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
    text: 'داشبورد تحلیلی کامل',
    icon: 'mdi-chart-bar',
    included: true,
    description: 'آمار عملکرد، سرنخ‌ها و تعاملات'
  },
  {
    text: 'فیلتر پیشرفته سرنخ‌ها',
    icon: 'mdi-filter',
    included: true,
    description: 'بر اساس دسته، موقعیت و نیاز'
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
    description: 'پاسخ سریع‌تر به درخواست‌ها'
  }
]
</script>

<style scoped>
.pricing-plans {
  max-width: 1200px;
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
}
</style>

