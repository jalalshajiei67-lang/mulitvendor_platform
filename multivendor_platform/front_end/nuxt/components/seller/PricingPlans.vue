<template>
  <v-container class="pricing-plans" fluid dir="rtl">
    <!-- Commission Plan Activation Dialog -->
    <CommissionPlanActivation v-model="showCommissionDialog" @success="handleCommissionSuccess" />

    <!-- Plans Overview Section -->
    <div class="plans-overview mb-8">
      <div class="overview-header">
        <h3 class="overview-title">پلن‌های موجود</h3>
        <p class="overview-subtitle">انتخاب کنید که کدام پلن برای شما مناسب است</p>
      </div>

      <div class="plans-stats">
        <div class="plan-stat-card free-stat" @click="scrollToPlan('free')">
          <div class="stat-icon">
            <v-icon size="28">mdi-store</v-icon>
          </div>
          <div class="stat-content">
            <div class="stat-title">پلن رایگان</div>
            <div class="stat-description">برای شروع و تست</div>
          </div>
        </div>

        <div class="plan-stat-card premium-stat" @click="scrollToPlan('premium')">
          <div class="stat-icon">
            <v-icon size="28">mdi-crown</v-icon>
          </div>
          <div class="stat-content">
            <div class="stat-title">پلن پریمیوم</div>
            <div class="stat-description">رشد سریع فروش</div>
          </div>
        </div>

        <div class="plan-stat-card commission-stat" @click="scrollToPlan('commission')">
          <div class="stat-icon">
            <v-icon size="28">mdi-handshake-outline</v-icon>
          </div>
          <div class="stat-content">
            <div class="stat-title">پلن کمیسیونی</div>
            <div class="stat-description">فقط از فروش</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile-First Hero Section -->
    <div class="hero-section mb-6">
      <div class="hero-content">
        <div class="hero-icon">
          <v-icon size="40" color="primary">mdi-crown</v-icon>
        </div>
        <h1 class="hero-title">بدون محدودیت رشد کنید</h1>
        <p class="hero-subtitle">
          سه راهکار متفاوت برای هر نوع فروشگاه. انتخاب کنید و امروز شروع کنید.
        </p>
      </div>

      <!-- Billing Period Toggle -->
      <div class="billing-section">
        <div class="billing-label">دوره پرداخت</div>
        <div class="billing-buttons">
          <button
            v-for="period in ['monthly', 'quarterly', 'semiannual', 'yearly']"
            :key="period"
            class="billing-btn"
            :class="{ active: billingPeriod === period }"
            @click="billingPeriod = period as BillingPeriod"
          >
            <span>{{ getBillingLabel(period) }}</span>
            <span v-if="period === 'yearly'" class="discount-badge">۲۰٪</span>
          </button>
        </div>
        <p class="billing-hint">هر زمان قابل تغییر</p>
      </div>
    </div>

    <!-- Mobile-First Plans Stack -->
    <div class="plans-container">
      <!-- Free Plan -->
      <div
        ref="freePlanRef"
        class="plan-card free-plan"
        :class="{ 'plan-selected': selectedPlan === 'free' }"
      >
        <div class="plan-header">
          <div class="plan-icon">
            <v-icon>mdi-store</v-icon>
          </div>
          <div class="plan-title-group">
            <h2 class="plan-name">پلن رایگان</h2>
            <p class="plan-description">برای شروع و تست بازار</p>
          </div>
        </div>

        <div class="plan-pricing">
          <div class="price-display">
            <span class="price">۰</span>
            <span class="currency">تومان</span>
          </div>
          <span class="price-label">همیشه رایگان</span>
        </div>

        <div class="plan-highlights">
          <div class="highlight">۱ مشتری در روز</div>
          <div class="highlight">محصولات محدود</div>
        </div>

        <div class="features-section">
          <h3 class="features-title">شامل است:</h3>
          <ul class="features-list">
            <li
              v-for="(feature, idx) in freePlanFeatures.filter((f) => f.included)"
              :key="`free-${idx}`"
              class="feature-item"
            >
              <v-icon class="feature-icon" size="20">mdi-check-circle</v-icon>
              <div class="feature-content">
                <div class="feature-name">{{ feature.text }}</div>
                <div class="feature-desc">{{ feature.description }}</div>
              </div>
            </li>
          </ul>
        </div>

        <button class="plan-action-btn free-btn" @click="selectedPlan = 'free'">
          <v-icon v-if="selectedPlan === 'free'" size="20">mdi-check-circle</v-icon>
          <span>{{ selectedPlan === 'free' ? 'انتخاب شده' : 'شروع رایگان' }}</span>
        </button>
      </div>

      <!-- Premium Plan - Featured -->
      <div
        ref="premiumPlanRef"
        class="plan-card premium-plan featured"
        :class="{ 'plan-selected': selectedPlan === 'premium' }"
      >
        <div class="plan-badge">
          <v-icon size="16">mdi-star</v-icon>
          <span>پیشنهاد محبوب</span>
        </div>

        <div class="plan-header">
          <div class="plan-icon premium-icon">
            <v-icon>mdi-crown</v-icon>
          </div>
          <div class="plan-title-group">
            <h2 class="plan-name">پلن پریمیوم</h2>
            <p class="plan-description">ویژه رشد سریع</p>
          </div>
        </div>

        <div class="plan-pricing">
          <div class="price-display">
            <span class="price">{{ premiumPriceNumber }}</span>
            <span class="currency">تومان</span>
          </div>
          <span class="price-label">{{ billingCaption }}</span>
          <span v-if="billingPeriod === 'yearly'" class="savings-badge">۲۰٪ صرفه‌جویی</span>
        </div>

        <div class="plan-highlights">
          <div class="highlight">مشتری نامحدود</div>
          <div class="highlight">پشتیبانی اولویت‌دار</div>
          <div class="highlight">گزارش پیشرفته</div>
        </div>

        <div class="features-section">
          <h3 class="features-title">شامل است:</h3>
          <ul class="features-list">
            <li
              v-for="(feature, idx) in premiumPlanFeatures.filter((f) => f.included)"
              :key="`premium-${idx}`"
              class="feature-item"
            >
              <v-icon class="feature-icon premium-icon-small" size="20">mdi-check-circle</v-icon>
              <div class="feature-content">
                <div class="feature-name">{{ feature.text }}</div>
                <div class="feature-desc">{{ feature.description }}</div>
              </div>
            </li>
          </ul>
        </div>

        <button class="plan-action-btn premium-btn" @click="selectedPlan = 'premium'">
          <v-icon v-if="selectedPlan === 'premium'" size="20">mdi-check-circle</v-icon>
          <span>{{ selectedPlan === 'premium' ? 'فعال شده' : 'ارتقاء به پریمیوم' }}</span>
        </button>
      </div>

      <!-- Commission Plan -->
      <div
        ref="commissionPlanRef"
        class="plan-card commission-plan"
        :class="{
          'plan-selected': selectedPlan === 'commission',
          'plan-inactive': !commissionPlanStatus?.is_ready,
        }"
      >
        <div class="plan-badge commission-badge">
          <v-icon size="16">mdi-percent</v-icon>
          <span>بدون هزینه ثابت</span>
        </div>

        <div v-if="!commissionPlanStatus?.is_ready" class="inactive-overlay">
          <span>غیرفعال</span>
        </div>

        <div class="plan-header">
          <div class="plan-icon commission-icon">
            <v-icon>mdi-handshake-outline</v-icon>
          </div>
          <div class="plan-title-group">
            <h2 class="plan-name">پلن کمیسیونی</h2>
            <p class="plan-description">فقط کمیسیون از فروش</p>
          </div>
        </div>

        <div class="plan-pricing">
          <div class="price-display commission-prices">
            <div class="price-tier">
              <span class="price">۵٪</span>
              <span class="price-note">زیر ۱ میلیارد</span>
            </div>
            <div class="price-separator">/</div>
            <div class="price-tier">
              <span class="price">۳٪</span>
              <span class="price-note">بالای ۱ میلیارد</span>
            </div>
          </div>
          <span class="price-label">کمیسیون از فروش</span>
        </div>

        <div class="plan-highlights">
          <div class="highlight">مشتری نامحدود</div>
          <div class="highlight">محصولات نامحدود</div>
          <div class="highlight">قرارداد رسمی</div>
        </div>

        <div class="features-section">
          <h3 class="features-title">شامل است:</h3>
          <ul class="features-list">
            <li
              v-for="(feature, idx) in commissionPlanFeatures.filter((f) => f.included)"
              :key="`commission-${idx}`"
              class="feature-item"
            >
              <v-icon class="feature-icon commission-icon-small" size="20">mdi-check-circle</v-icon>
              <div class="feature-content">
                <div class="feature-name">{{ feature.text }}</div>
                <div class="feature-desc">{{ feature.description }}</div>
              </div>
            </li>
          </ul>
        </div>

        <div v-if="!commissionPlanStatus?.is_ready" class="plan-status-alert">
          <v-icon size="18">mdi-alert-circle</v-icon>
          <div>
            <div v-if="commissionPlanStatus?.is_commission_based">درخواست شما در حال بررسی است</div>
            <div v-else>نیاز به نشان طلایی برای فعال‌سازی</div>
          </div>
        </div>

        <button
          class="plan-action-btn commission-btn"
          :disabled="loadingCommissionStatus"
          @click="handleCommissionClick"
        >
          <v-icon v-if="commissionPlanStatus?.is_ready" size="20">mdi-check-circle</v-icon>
          <span>
            {{ commissionPlanStatus?.is_ready ? 'فعال شده' : 'درخواست فعال‌سازی' }}
          </span>
        </button>
      </div>
    </div>

    <!-- Quick Comparison Table -->
    <div class="comparison-section mt-8">
      <h2 class="comparison-title">مقایسه کامل امکانات</h2>
      <div class="comparison-table">
        <div class="comparison-row header-row">
          <div class="comparison-cell feature-cell">امکانات</div>
          <div class="comparison-cell">رایگان</div>
          <div class="comparison-cell">پریمیوم</div>
          <div class="comparison-cell">کمیسیونی</div>
        </div>

        <template v-for="(row, idx) in comparisonRows" :key="`cmp-${idx}`">
          <div class="comparison-row" :class="{ 'alt-row': idx % 2 === 0 }">
            <div class="comparison-cell feature-cell">
              <div class="feature-label">{{ row.label }}</div>
              <div class="feature-hint">{{ row.hint }}</div>
            </div>
            <div class="comparison-cell">
              <v-icon :color="row.free ? 'success' : 'disabled'" size="20">
                {{ row.free ? 'mdi-check' : 'mdi-close' }}
              </v-icon>
            </div>
            <div class="comparison-cell">
              <v-icon color="amber-darken-2" size="20">mdi-check</v-icon>
            </div>
            <div class="comparison-cell">
              <v-icon :color="row.commission ? 'success' : 'disabled'" size="20">
                {{ row.commission ? 'mdi-check' : 'mdi-close' }}
              </v-icon>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="cta-section mt-8">
      <div class="cta-content">
        <h2>آماده شروع هستید؟</h2>
        <p>انتخاب کنید و به رشد تجارتان کمک کنید</p>
        <button class="cta-button" @click="selectedPlan = 'premium'">
          <v-icon>mdi-rocket-launch</v-icon>
          <span>شروع امروز</span>
        </button>
      </div>
    </div>

    <!-- Old Plans Row (hidden for now, kept for backward compatibility) -->
    <v-row class="mb-4" dense style="display: none">
      <v-col cols="12" md="4">
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
                <v-list-item-title
                  :class="!feature.included ? 'text-disabled text-decoration-line-through' : ''"
                >
                  {{ feature.text }}
                </v-list-item-title>
                <v-list-item-subtitle class="d-flex align-center gap-2">
                  <span class="text-caption text-medium-emphasis">{{ feature.description }}</span>
                  <v-chip v-if="feature.badge" size="x-small" color="primary" variant="tonal">
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

      <v-col cols="12" md="4">
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
              <v-chip size="small" color="white" text-color="amber-darken-4" variant="flat"
                >مشتری نامحدود</v-chip
              >
              <v-chip size="small" color="white" text-color="amber-darken-4" variant="flat"
                >پشتیبانی اولویت‌دار</v-chip
              >
              <v-chip size="small" color="white" text-color="amber-darken-4" variant="flat"
                >گزارش ساده عملکرد</v-chip
              >
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
                <v-list-item-title
                  :class="!feature.included ? 'text-disabled text-decoration-line-through' : ''"
                >
                  {{ feature.text }}
                </v-list-item-title>
                <v-list-item-subtitle class="d-flex align-center gap-2">
                  <span class="text-caption text-medium-emphasis">{{ feature.description }}</span>
                  <v-chip v-if="feature.badge" size="x-small" color="amber" variant="tonal">
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

      <v-col cols="12" md="4">
        <v-card
          :elevation="selectedPlan === 'commission' ? 10 : 4"
          class="rounded-2xl overflow-hidden commission-card h-100"
          :class="[
            selectedPlan === 'commission' ? 'border-success' : 'border-success-light',
            !commissionPlanStatus?.is_ready && 'commission-inactive',
          ]"
          :style="!commissionPlanStatus?.is_ready ? { opacity: 0.7 } : {}"
        >
          <!-- Inactive Badge -->
          <div v-if="!commissionPlanStatus?.is_ready" class="inactive-badge">
            <v-chip
              color="warning"
              text-color="white"
              variant="flat"
              prepend-icon="mdi-alert-circle"
              size="small"
            >
              غیرفعال
            </v-chip>
          </div>

          <div class="commission-ribbon">
            <div class="d-flex align-center gap-2">
              <v-icon size="16" class="ml-1">mdi-percent</v-icon>
              <span>بدون هزینه ماهانه</span>
            </div>
            <v-chip
              color="white"
              text-color="green-darken-3"
              variant="flat"
              prepend-icon="mdi-handshake"
              size="x-small"
              class="mt-2"
            >
              قراردادی
            </v-chip>
          </div>
          <v-card-text
            class="pa-6 commission-hero"
            :class="{ 'commission-hero-inactive': !commissionPlanStatus?.is_ready }"
          >
            <div class="d-flex align-center gap-3">
              <v-avatar size="48" color="white" variant="tonal">
                <v-icon color="white">mdi-handshake-outline</v-icon>
              </v-avatar>
              <div>
                <div class="text-h6 font-weight-bold text-white">پلن کمیسیونی</div>
                <div class="text-caption text-white">فقط کمیسیون از فروش</div>
              </div>
            </div>
            <div class="d-flex flex-column gap-2 mt-4">
              <div class="text-white">
                <span class="text-h5 font-weight-bold">٪۵</span>
                <span class="text-caption mr-1">زیر ۱ میلیارد</span>
              </div>
              <div class="text-white">
                <span class="text-h5 font-weight-bold">٪۳</span>
                <span class="text-caption mr-1">بالای ۱ میلیارد</span>
              </div>
            </div>
            <div class="d-flex gap-2 flex-wrap mt-3">
              <v-chip size="small" color="white" text-color="green-darken-4" variant="flat"
                >بدون هزینه ثابت</v-chip
              >
              <v-chip size="small" color="white" text-color="green-darken-4" variant="flat"
                >مشتری نامحدود</v-chip
              >
              <v-chip size="small" color="white" text-color="green-darken-4" variant="flat"
                >قراردادی</v-chip
              >
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="pa-6">
            <v-list density="comfortable" lines="two" class="feature-list">
              <v-list-item
                v-for="(feature, idx) in commissionPlanFeatures"
                :key="`commission-${idx}`"
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
                <v-list-item-title
                  :class="!feature.included ? 'text-disabled text-decoration-line-through' : ''"
                >
                  {{ feature.text }}
                </v-list-item-title>
                <v-list-item-subtitle class="d-flex align-center gap-2">
                  <span class="text-caption text-medium-emphasis">{{ feature.description }}</span>
                  <v-chip v-if="feature.badge" size="x-small" color="success" variant="tonal">
                    {{ feature.badge }}
                  </v-chip>
                </v-list-item-subtitle>
                <template #append>
                  <v-icon :color="feature.included ? 'success' : 'grey'">
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
              :color="selectedPlan === 'commission' ? 'green-darken-2' : 'success'"
              :variant="selectedPlan === 'commission' ? 'flat' : 'elevated'"
              :prepend-icon="commissionPlanStatus?.is_ready ? 'mdi-check-circle' : 'mdi-file-sign'"
              :disabled="loadingCommissionStatus"
              @click="handleCommissionClick"
            >
              <span v-if="commissionPlanStatus?.is_ready"> ✓ فعال شده </span>
              <span
                v-else-if="
                  commissionPlanStatus?.is_commission_based && !commissionPlanStatus?.is_ready
                "
              >
                در حال بررسی
              </span>
              <span v-else> درخواست فعال‌سازی </span>
            </v-btn>

            <v-alert
              v-if="!commissionPlanStatus?.is_ready"
              type="warning"
              variant="tonal"
              density="compact"
              class="mt-3 text-caption"
            >
              <div v-if="commissionPlanStatus?.is_commission_based">
                درخواست شما در حال بررسی است. پس از تأیید ادمین، پلن فعال خواهد شد.
              </div>
              <div v-else>برای فعال‌سازی این پلن، ابتدا باید نشان طلایی را دریافت کنید.</div>
            </v-alert>

            <v-alert
              v-else
              type="success"
              variant="tonal"
              density="compact"
              class="mt-3 text-caption"
            >
              پلن کمیسیونی شما فعال است
            </v-alert>
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
              <div class="text-caption text-medium-emphasis">
                آنچه در داشبورد فروشنده دریافت می‌کنید
              </div>
            </div>
          </div>
          <v-chip
            color="primary"
            variant="tonal"
            size="small"
            prepend-icon="mdi-checkbox-marked-circle-outline"
          >
            مناسب برای تصمیم سریع
          </v-chip>
        </div>

        <div class="comparison-grid">
          <div class="comparison-header">امکانات کلیدی</div>
          <div class="comparison-header text-center">رایگان</div>
          <div class="comparison-header text-center">پریمیوم</div>
          <div class="comparison-header text-center">کمیسیونی</div>

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
            <div class="comparison-cell text-center">
              <v-icon :color="row.commission ? 'success' : 'disabled'">
                {{ row.commission ? 'mdi-check' : 'mdi-close' }}
              </v-icon>
              <div class="text-caption text-medium-emphasis mt-1">{{ row.commissionText }}</div>
            </div>
          </template>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useToast } from '~/composables/useToast'

type PlanType = 'free' | 'premium' | 'commission' | null
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
  commission: boolean
  commissionText: string
}

const selectedPlan = ref<PlanType>('free')
const billingPeriod = ref<BillingPeriod>('monthly')
const showCommissionDialog = ref(false)
const commissionPlanStatus = ref<any>(null)
const loadingCommissionStatus = ref(false)

// Refs for plan cards
const freePlanRef = ref<HTMLDivElement | null>(null)
const premiumPlanRef = ref<HTMLDivElement | null>(null)
const commissionPlanRef = ref<HTMLDivElement | null>(null)

const { showToast } = useToast()

function scrollToPlan(planType: PlanType) {
  let element: HTMLDivElement | null | undefined = null

  if (planType === 'free') {
    element = freePlanRef.value
  } else if (planType === 'premium') {
    element = premiumPlanRef.value
  } else if (planType === 'commission') {
    element = commissionPlanRef.value
  }

  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }
}

function handleCommissionClick() {
  if (selectedPlan.value === 'commission') {
    selectedPlan.value = null
  } else {
    showCommissionDialog.value = true
  }
}

function handleCommissionSuccess() {
  selectedPlan.value = 'commission'
  showToast({
    message: 'درخواست فعال‌سازی پلن کمیسیونی با موفقیت ثبت شد',
    color: 'success',
  })
  loadCommissionStatus()
}

async function loadCommissionStatus() {
  loadingCommissionStatus.value = true
  try {
    const { $api } = useNuxtApp() as any
    const response = await $api('/api/users/seller/commission/status/')
    commissionPlanStatus.value = response

    // Auto-select commission plan if it's active
    if (response.is_ready) {
      selectedPlan.value = 'commission'
    }
  } catch (error: any) {
    console.error('Error loading commission status:', error)
    commissionPlanStatus.value = null
  } finally {
    loadingCommissionStatus.value = false
  }
}

// Load commission status on mount
onMounted(() => {
  loadCommissionStatus()
})

const freePlanFeatures: Feature[] = [
  {
    text: 'ایجاد یک فروشگاه مینی رایگان',
    icon: 'mdi-store',
    included: true,
    description: 'با تمام امکانات پایه',
  },
  {
    text: 'ابزارهای تبلیغاتی کامل',
    icon: 'mdi-account-group',
    included: true,
    description: 'معرفی ساده تیم و نمونه کار',
  },
  {
    text: 'دریافت تأییدیه از همکاران',
    icon: 'mdi-award',
    included: true,
    description: 'دعوت همکاران برای تأیید شما',
  },
  {
    text: 'نظرات و بررسی مشتریان قبلی',
    icon: 'mdi-message-text',
    included: true,
    description: 'نظر کوتاه از مشتریان قبلی',
  },
  {
    text: 'فهرست محصولات',
    icon: 'mdi-package-variant',
    included: true,
    description: 'چند محصول اصلی با عکس واضح',
    badge: 'محدود',
  },
  {
    text: 'نمایش در فهرست شرکت‌های گواهی‌شده',
    icon: 'mdi-shield-check',
    included: false,
    description: 'فقط برای کاربران پریمیوم',
  },
  {
    text: 'یک مشتری در روز',
    icon: 'mdi-clock-outline',
    included: true,
    description: 'روزانه یک پیام از خریداران',
    badge: 'محدودیت روزانه',
  },
  {
    text: 'دسترسی به یک دسته اولویت بالا',
    icon: 'mdi-star',
    included: true,
    description: 'برای محصولات غیر استاندارد',
  },
  {
    text: 'دستیار شخصی اختصاصی',
    icon: 'mdi-account-cog',
    included: false,
  },
  {
    text: 'داشبورد تحلیلی پیشرفته',
    icon: 'mdi-chart-bar',
    included: false,
  },
  {
    text: 'مشتریان نامحدود با فیلتر',
    icon: 'mdi-filter',
    included: false,
  },
]

const commissionPlanFeatures: Feature[] = [
  {
    text: 'بدون هزینه ثابت ماهانه',
    icon: 'mdi-cash-remove',
    included: true,
    description: 'فقط از فروش کمیسیون',
    badge: 'صرفه‌جویی',
  },
  {
    text: 'مشتریان نامحدود',
    icon: 'mdi-account-multiple',
    included: true,
    description: 'دریافت پیام نامحدود',
  },
  {
    text: 'محصولات نامحدود',
    icon: 'mdi-package-variant',
    included: true,
    description: 'بدون محدودیت تعداد',
  },
  {
    text: 'نمایش در مارکت‌پلیس',
    icon: 'mdi-storefront',
    included: true,
    description: 'دسترسی کامل به بازار',
  },
  {
    text: 'کمیسیون پلکانی',
    icon: 'mdi-chart-line',
    included: true,
    description: '٪۵ زیر ۱ میلیارد، ٪۳ بالای آن',
    badge: 'منصفانه',
  },
  {
    text: 'قرارداد رسمی',
    icon: 'mdi-file-sign',
    included: true,
    description: 'امضای قرارداد و ضمانت‌نامه',
    badge: 'ضروری',
  },
  {
    text: 'پشتیبانی عادی',
    icon: 'mdi-headset',
    included: true,
    description: 'پشتیبانی استاندارد',
  },
  {
    text: 'تسویه قراردادی',
    icon: 'mdi-calendar-clock',
    included: true,
    description: 'پرداخت بعد از کسر کمیسیون',
  },
  {
    text: 'دستیار شخصی اختصاصی',
    icon: 'mdi-account-cog',
    included: false,
    description: 'فقط پلن پریمیوم',
  },
]

const premiumPlanFeatures: Feature[] = [
  {
    text: 'تمام امکانات پلن رایگان',
    icon: 'mdi-gift',
    included: true,
    description: 'بدون هیچ محدودیتی',
  },
  {
    text: 'مشتریان نامحدود',
    icon: 'mdi-trending-up',
    included: true,
    description: 'پیام‌های بیشتر با فیلتر ساده',
    badge: 'نامحدود',
  },
  {
    text: 'نمایش در فهرست شرکت‌های گواهی‌شده',
    icon: 'mdi-shield-check',
    included: true,
    description: 'دید عمومی و اعتبار بالا',
  },
  {
    text: 'دستیار شخصی اختصاصی',
    icon: 'mdi-account-cog',
    included: true,
    description: 'مدیریت وظایف از راه دور',
  },
  {
    text: 'گزارش ساده عملکرد',
    icon: 'mdi-chart-bar',
    included: true,
    description: 'گزارش خوانا از بازدید و پیام‌ها',
  },
  {
    text: 'فیلتر مشتریان',
    icon: 'mdi-filter',
    included: true,
    description: 'بر اساس دسته، شهر و نیاز',
  },
  {
    text: 'محصولات نامحدود',
    icon: 'mdi-package-variant',
    included: true,
    description: 'بدون محدودیت تعداد',
  },
  {
    text: 'تأییدیه‌های نامحدود',
    icon: 'mdi-award',
    included: true,
    description: 'دعوت همکاران بدون محدودیت',
  },
  {
    text: 'اولویت در پشتیبانی',
    icon: 'mdi-lightning-bolt',
    included: true,
    description: 'پاسخ سریع تلفنی و پیام',
  },
]

const comparisonRows: ComparisonRow[] = [
  {
    label: 'هزینه ماهانه',
    hint: 'هزینه ثابت برای استفاده',
    free: true,
    freeText: 'رایگان',
    premiumText: '۱٫۵ میلیون تومان',
    commission: true,
    commissionText: 'رایگان (فقط کمیسیون)',
  },
  {
    label: 'کمیسیون فروش',
    hint: 'درصد کسری از فروش',
    free: true,
    freeText: 'ندارد',
    premiumText: 'ندارد',
    commission: true,
    commissionText: '٪۳-۵ از فروش',
  },
  {
    label: 'پیام خریداران',
    hint: 'تعداد پیام‌هایی که دریافت می‌کنید',
    free: true,
    freeText: '۱ پیام عمومی در روز',
    premiumText: 'نامحدود با فیلتر دقیق',
    commission: true,
    commissionText: 'نامحدود',
  },
  {
    label: 'نمایش در نتایج',
    hint: 'جایگاه شما در لیست و جست‌وجو',
    free: false,
    freeText: 'نمایش عادی',
    premiumText: 'نمایش بالاتر با نشان پریمیوم',
    commission: true,
    commissionText: 'نمایش عادی',
  },
  {
    label: 'گزارش‌ها',
    hint: 'گزارش ساده از بازدید و پیام‌ها',
    free: false,
    freeText: 'نمای کلی ساده',
    premiumText: 'گزارش کامل و خوانا',
    commission: false,
    commissionText: 'نمای کلی ساده',
  },
  {
    label: 'تعداد محصولات',
    hint: 'حداکثر محصولات فعال',
    free: true,
    freeText: 'محدود',
    premiumText: 'نامحدود',
    commission: true,
    commissionText: 'نامحدود',
  },
  {
    label: 'پشتیبانی',
    hint: 'زمان پاسخ و کانال ارتباط',
    free: true,
    freeText: 'پشتیبانی عادی',
    premiumText: 'اولویت‌دار + دستیار اختصاصی',
    commission: true,
    commissionText: 'پشتیبانی عادی',
  },
  {
    label: 'نیازمندی‌ها',
    hint: 'شرایط لازم برای فعال‌سازی',
    free: true,
    freeText: 'بدون شرط',
    premiumText: 'پرداخت ماهانه',
    commission: true,
    commissionText: 'قرارداد + ضمانت‌نامه',
  },
]

const premiumPriceDisplay = computed(() => {
  const monthly = 1_500_000
  const prices: Record<BillingPeriod, number> = {
    monthly,
    quarterly: monthly * 3,
    semiannual: monthly * 6,
    yearly: Math.round(monthly * 12 * 0.8),
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

const premiumPriceNumber = computed(() => {
  const monthly = 1_500_000
  const prices: Record<BillingPeriod, number> = {
    monthly,
    quarterly: monthly * 3,
    semiannual: monthly * 6,
    yearly: Math.round(monthly * 12 * 0.8),
  }
  const value = prices[billingPeriod.value]
  return (value / 1_000_000).toFixed(1).replace(/\.0$/, '')
})

function getBillingLabel(period: string): string {
  const labels: Record<string, string> = {
    monthly: 'ماهانه',
    quarterly: '۳ ماهه',
    semiannual: '۶ ماهه',
    yearly: 'سالانه',
  }
  return labels[period] || period
}
</script>

<style scoped>
:root {
  --color-primary: #3b82f6;
  --color-amber: #f59e0b;
  --color-success: #10b981;
  --color-bg: #ffffff;
  --color-surface: #f9fafb;
  --color-border: #e5e7eb;
  --color-text: #111827;
  --color-text-light: #6b7280;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
}

* {
  box-sizing: border-box;
}

.pricing-plans {
  padding: 0;
  max-width: 100%;
}

/* Plans Overview Section */
.plans-overview {
  padding: 0 16px;
}

.overview-header {
  text-align: center;
  margin-bottom: 24px;
}

.overview-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px 0;
}

.overview-subtitle {
  font-size: 14px;
  color: var(--color-text-light);
  margin: 0;
}

.plans-stats {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.plan-stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
  cursor: pointer;
}

.plan-stat-card:active {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.plan-stat-card.free-stat {
  border-left: 4px solid #2563eb;
}

.plan-stat-card.free-stat .stat-icon {
  color: #2563eb;
}

.plan-stat-card.premium-stat {
  border-left: 4px solid #d97706;
  background: linear-gradient(135deg, rgba(217, 119, 6, 0.02), transparent);
}

.plan-stat-card.premium-stat .stat-icon {
  color: #d97706;
}

.plan-stat-card.commission-stat {
  border-left: 4px solid #059669;
  background: linear-gradient(135deg, rgba(5, 150, 105, 0.02), transparent);
}

.plan-stat-card.commission-stat .stat-icon {
  color: #059669;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  min-width: 48px;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 50%;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.2;
}

.stat-description {
  font-size: 12px;
  color: var(--color-text-light);
  margin-top: 2px;
}

/* Tablet Styles for Plans Overview */
@media (min-width: 768px) {
  .plans-overview {
    padding: 0;
  }

  .overview-header {
    margin-bottom: 28px;
  }

  .overview-title {
    font-size: 26px;
  }

  .overview-subtitle {
    font-size: 16px;
  }

  .plans-stats {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }

  .plan-stat-card {
    flex-direction: column;
    text-align: center;
    gap: 12px;
    padding: 20px;
  }

  .plan-stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  }

  .plan-stat-card.free-stat {
    border-left: none;
    border-top: 4px solid #2563eb;
  }

  .plan-stat-card.premium-stat {
    border-left: none;
    border-top: 4px solid #d97706;
  }

  .plan-stat-card.commission-stat {
    border-left: none;
    border-top: 4px solid #059669;
  }

  .stat-icon {
    width: 56px;
    height: 56px;
  }

  .stat-title {
    font-size: 15px;
  }

  .stat-description {
    font-size: 13px;
  }
}

/* Desktop Styles for Plans Overview */
@media (min-width: 1024px) {
  .overview-title {
    font-size: 28px;
  }

  .overview-subtitle {
    font-size: 16px;
    max-width: 500px;
    margin: 8px auto 0;
  }

  .plans-stats {
    gap: 20px;
  }

  .plan-stat-card {
    padding: 24px;
  }

  .stat-icon {
    width: 60px;
    height: 60px;
  }

  .stat-title {
    font-size: 16px;
  }

  .stat-description {
    font-size: 14px;
  }
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: 24px 16px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(245, 158, 11, 0.05));
  border-radius: var(--radius-lg);
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.hero-content {
  margin-bottom: 32px;
}

.hero-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 50%;
  margin-bottom: 16px;
}

.hero-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 16px 0 12px 0;
  line-height: 1.3;
}

.hero-subtitle {
  font-size: 16px;
  color: var(--color-text-light);
  line-height: 1.5;
  margin: 0;
}

/* Billing Section */
.billing-section {
  text-align: center;
}

.billing-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 12px;
}

.billing-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 12px;
}

.billing-btn {
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  background: var(--color-bg);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
  transition: all 0.2s ease;
  position: relative;
  white-space: nowrap;
}

.billing-btn:active,
.billing-btn.active {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.billing-btn:hover:not(.active) {
  border-color: var(--color-primary);
}

.discount-badge {
  display: inline-block;
  background: #10b981;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  margin-right: 4px;
  font-weight: 700;
}

.billing-hint {
  font-size: 12px;
  color: var(--color-text-light);
  margin: 0;
}

/* Plans Container */
.plans-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 24px 0;
}

/* Plan Card */
.plan-card {
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.plan-card:active,
.plan-selected {
  border-color: var(--color-primary);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.12);
  transform: translateY(-2px);
}

.plan-card.featured {
  border: 2px solid var(--color-amber);
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.02), rgba(245, 158, 11, 0.04));
}

.plan-card.featured.plan-selected {
  border-color: var(--color-amber);
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.12);
}

.plan-card.commission-plan.plan-selected {
  border-color: var(--color-success);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.12);
}

/* Plan Badge */
.plan-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.plan-badge.commission-badge {
  background: rgba(16, 185, 129, 0.1);
  color: var(--color-success);
}

.plan-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
  margin-top: 32px;
}

.plan-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  min-width: 48px;
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  border-radius: 50%;
  font-size: 24px;
}

.plan-icon.premium-icon {
  background: rgba(245, 158, 11, 0.1);
  color: var(--color-amber);
}

.plan-icon.commission-icon {
  background: rgba(16, 185, 129, 0.1);
  color: var(--color-success);
}

.plan-title-group {
  flex: 1;
}

.plan-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 4px 0;
}

.plan-description {
  font-size: 13px;
  color: var(--color-text-light);
  margin: 0;
}

/* Plan Pricing */
.plan-pricing {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
}

.price-display {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 8px;
}

.price-display.commission-prices {
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.price-tier {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.price {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text);
  line-height: 1;
}

.currency {
  font-size: 14px;
  color: var(--color-text-light);
  font-weight: 500;
}

.price-note {
  font-size: 12px;
  color: var(--color-text-light);
  margin-top: 4px;
}

.price-separator {
  font-size: 24px;
  color: var(--color-border);
}

.price-label {
  font-size: 13px;
  color: var(--color-text-light);
  display: block;
}

.savings-badge {
  display: inline-block;
  background: #10b981;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  margin-top: 8px;
}

/* Plan Highlights */
.plan-highlights {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
}

.highlight {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  padding-right: 28px;
  position: relative;
  display: flex;
  align-items: center;
}

.highlight::before {
  content: '✓';
  position: absolute;
  right: 0;
  color: var(--color-success);
  font-weight: 700;
  margin-left: 8px;
}

/* Features Section */
.features-section {
  flex: 1;
  margin-bottom: 20px;
}

.features-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 12px 0;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.feature-icon {
  color: var(--color-primary);
  margin-top: 2px;
  flex-shrink: 0;
}

.feature-icon.premium-icon-small {
  color: var(--color-amber);
}

.feature-icon.commission-icon-small {
  color: var(--color-success);
}

.feature-content {
  flex: 1;
}

.feature-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
  line-height: 1.4;
}

.feature-desc {
  font-size: 12px;
  color: var(--color-text-light);
  margin-top: 2px;
}

/* Plan Action Button */
.plan-action-btn {
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: inherit;
}

.free-btn {
  background: #2563eb;
  color: white;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
}

.free-btn:active {
  background: #1d4ed8;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
  transform: scale(0.98);
}

.free-btn:hover {
  background: #1d4ed8;
}

.premium-btn {
  background: #d97706;
  color: white;
  box-shadow: 0 2px 8px rgba(217, 119, 6, 0.2);
}

.premium-btn:active {
  background: #b45309;
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
  transform: scale(0.98);
}

.premium-btn:hover {
  background: #b45309;
}

.commission-btn {
  background: #059669;
  color: white;
  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.2);
}

.commission-btn:active {
  background: #047857;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
  transform: scale(0.98);
}

.commission-btn:hover {
  background: #047857;
}

.commission-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Inactive Plan */
.plan-inactive {
  opacity: 0.7;
}

.inactive-overlay {
  position: absolute;
  top: 50%;
  right: 50%;
  transform: translateX(50%) translateY(-50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  z-index: 1;
}

.plan-status-alert {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: var(--radius-md);
  padding: 12px;
  margin-bottom: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  color: #b45309;
  font-size: 13px;
}

.plan-status-alert svg {
  margin-top: 2px;
  flex-shrink: 0;
}

/* Comparison Section */
.comparison-section {
  margin-top: 48px;
  padding: 0 16px;
}

.comparison-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text);
  text-align: center;
  margin: 0 0 24px 0;
}

.comparison-table {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.comparison-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 0;
  border-bottom: 1px solid var(--color-border);
}

.comparison-row:last-child {
  border-bottom: none;
}

.comparison-row.alt-row {
  background: rgba(0, 0, 0, 0.02);
}

.comparison-row.header-row {
  background: rgba(59, 130, 246, 0.08);
  font-weight: 700;
}

.comparison-cell {
  padding: 16px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  text-align: center;
  border-right: 1px solid var(--color-border);
}

.comparison-cell:first-child {
  border-right: none;
  text-align: right;
}

.comparison-cell.feature-cell {
  grid-column: 1;
  text-align: right;
  justify-content: flex-start;
}

.feature-label {
  font-weight: 600;
  color: var(--color-text);
  font-size: 14px;
}

.feature-hint {
  font-size: 12px;
  color: var(--color-text-light);
  margin-top: 2px;
}

/* CTA Section */
.cta-section {
  text-align: center;
  padding: 40px 24px;
  background: linear-gradient(135deg, var(--color-primary), rgba(59, 130, 246, 0.8));
  border-radius: var(--radius-lg);
  color: white;
  margin: 0 16px 40px 16px;
}

.cta-content h2 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.cta-content p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 20px 0;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: white;
  color: var(--color-primary);
  border: none;
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cta-button:active {
  transform: scale(0.98);
}

/* Tablet Styles (md and up) */
@media (min-width: 768px) {
  .hero-section {
    padding: 32px 40px;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .plans-container {
    display: grid;
    grid-template-columns: 1fr 1.1fr 1fr;
    gap: 24px;
  }

  .plan-card {
    padding: 32px;
  }

  .comparison-table {
    border-radius: var(--radius-lg);
  }

  .comparison-row {
    grid-template-columns: 2fr 1fr 1fr 1fr;
  }

  .comparison-cell {
    padding: 20px 16px;
    border-right: 1px solid var(--color-border);
  }

  .comparison-cell:first-child {
    border-right: 1px solid var(--color-border);
  }

  .comparison-section {
    padding: 0;
  }

  .cta-section {
    margin: 0 0 40px 0;
  }
}

/* Desktop Styles (lg and up) */
@media (min-width: 1024px) {
  .pricing-plans {
    max-width: 1280px;
    margin: 0 auto;
  }

  .hero-section {
    padding: 48px 60px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 20px;
    max-width: 600px;
    margin: 0 auto;
  }

  .billing-buttons {
    gap: 12px;
  }

  .billing-btn {
    padding: 10px 16px;
  }

  .plans-container {
    gap: 28px;
  }

  .plan-card {
    padding: 36px;
  }

  .plan-card:hover {
    border-color: var(--color-primary);
    box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
    transform: translateY(-4px);
  }

  .plan-card.featured:hover {
    box-shadow: 0 12px 32px rgba(245, 158, 11, 0.15);
  }

  .plan-card.commission-plan:hover {
    box-shadow: 0 12px 32px rgba(16, 185, 129, 0.15);
  }

  .comparison-row {
    grid-template-columns: 2.5fr 1fr 1fr 1fr;
  }

  .comparison-cell {
    padding: 20px;
  }
}

/* RTL Adjustments */
[dir='rtl'] .plan-badge {
  left: 12px;
  right: auto;
}

[dir='rtl'] .inactive-overlay {
  right: auto;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
}

[dir='rtl'] .comparison-cell {
  border-right: none;
  border-left: 1px solid var(--color-border);
}

[dir='rtl'] .comparison-cell:first-child {
  border-left: none;
  border-right: 1px solid var(--color-border);
}
</style>
