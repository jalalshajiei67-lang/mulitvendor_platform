<template>
  <div class="seller-landing" dir="rtl">
    <!-- Hero Section -->
    <section class="hero-section">
      <v-container fluid class="pa-0">
        <v-row no-gutters class="align-center" style="min-height: 500px">
          <v-col cols="12" md="6" class="hero-content-col pa-8 pa-md-12">
            <div class="hero-content">
              <h1 class="text-h3 text-md-h2 font-weight-bold mb-4 text-primary">
                فروشنده شوید و کسب‌وکار خود را متحول کنید
              </h1>
              <p class="text-h6 text-md-h5 text-medium-emphasis mb-6">
                به بزرگ‌ترین پلتفرم B2B ماشین‌آلات صنعتی ایران بپیوندید
              </p>
              <p class="text-body-1 text-medium-emphasis mb-8">
                به هزاران خریدار صنعتی دسترسی پیدا کنید، فروش‌های خود را افزایش دهید و کسب‌وکار خود را به سطح جدیدی برسانید.
              </p>
              <div class="d-flex flex-column flex-sm-row gap-4">
                <v-btn
                  color="primary"
                  size="x-large"
                  rounded="lg"
                  prepend-icon="mdi-account-plus"
                  :to="registerLink"
                  class="px-8"
                >
                  ثبت‌نام به عنوان فروشنده
                </v-btn>
                <v-btn
                  color="secondary"
                  variant="outlined"
                  size="x-large"
                  rounded="lg"
                  prepend-icon="mdi-information"
                  to="/seller/pricing"
                  class="px-8"
                >
                  مشاهده تعرفه‌ها
                </v-btn>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="6" class="hero-image-col pa-0">
            <div class="hero-image-wrapper">
              <v-img
                src="/images/seller-landing/machinery-hero.jpg"
                alt="ماشین‌آلات صنعتی"
                cover
                height="500"
                class="hero-image"
              >
                <template v-slot:placeholder>
                  <div class="d-flex align-center justify-center fill-height bg-grey-lighten-4">
                    <v-icon size="80" color="grey-lighten-1">mdi-cog</v-icon>
                  </div>
                </template>
              </v-img>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Statistics Section -->
    <section class="statistics-section py-12">
      <v-container>
        <v-row>
          <v-col
            v-for="stat in statistics"
            :key="stat.label"
            cols="6"
            md="3"
            class="text-center"
          >
            <div class="stat-card pa-6">
              <v-icon :icon="stat.icon" size="48" color="primary" class="mb-4" />
              <div class="text-h3 text-md-h2 font-weight-bold text-primary mb-2">
                {{ stat.value }}
              </div>
              <div class="text-body-1 text-medium-emphasis">
                {{ stat.label }}
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Benefits Section -->
    <section class="benefits-section py-12 bg-grey-lighten-5">
      <v-container>
        <div class="text-center mb-12">
          <h2 class="text-h4 text-md-h3 font-weight-bold mb-4">
            چرا ایندکسو را انتخاب کنیم؟
          </h2>
          <p class="text-h6 text-medium-emphasis mx-auto" style="max-width: 700px">
            با پیوستن به ایندکسو، به ابزارها و امکاناتی دسترسی پیدا می‌کنید که فروش شما را به طور قابل توجهی افزایش می‌دهد
          </p>
        </div>
        <v-row>
          <v-col
            v-for="benefit in benefits"
            :key="benefit.title"
            cols="12"
            sm="6"
            md="4"
            class="mb-4"
          >
            <v-card elevation="2" rounded="xl" class="benefit-card h-100 pa-6">
              <v-icon :icon="benefit.icon" size="48" :color="benefit.color" class="mb-4" />
              <h3 class="text-h6 font-weight-bold mb-3">{{ benefit.title }}</h3>
              <p class="text-body-2 text-medium-emphasis">
                {{ benefit.description }}
              </p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Features Section -->
    <section class="features-section py-12">
      <v-container>
        <div class="text-center mb-12">
          <h2 class="text-h4 text-md-h3 font-weight-bold mb-4">
            امکانات پلتفرم برای فروشندگان
          </h2>
          <p class="text-h6 text-medium-emphasis mx-auto" style="max-width: 700px">
            ابزارهای حرفه‌ای برای مدیریت محصولات، ارتباط با مشتریان و تحلیل عملکرد
          </p>
        </div>
        <v-row align="center" class="mb-12">
          <v-col cols="12" md="6" class="order-2 order-md-1">
            <v-img
              src="/images/seller-landing/industrial-equipment.jpg"
              alt="امکانات پلتفرم"
              cover
              height="400"
              rounded="xl"
            >
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height bg-grey-lighten-4">
                  <v-icon size="80" color="grey-lighten-1">mdi-tools</v-icon>
                </div>
              </template>
            </v-img>
          </v-col>
          <v-col cols="12" md="6" class="order-1 order-md-2">
            <div class="features-list">
              <div
                v-for="feature in features.slice(0, 4)"
                :key="feature.title"
                class="feature-item mb-6 d-flex align-start"
              >
                <v-icon :icon="feature.icon" size="32" color="primary" class="ml-4 mt-1" />
                <div>
                  <h4 class="text-h6 font-weight-bold mb-2">{{ feature.title }}</h4>
                  <p class="text-body-2 text-medium-emphasis">
                    {{ feature.description }}
                  </p>
                </div>
              </div>
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="feature in features.slice(4)"
            :key="feature.title"
            cols="12"
            sm="6"
            md="4"
            class="mb-4"
          >
            <v-card elevation="1" rounded="lg" class="feature-card h-100 pa-4">
              <v-icon :icon="feature.icon" size="32" color="primary" class="mb-3" />
              <h4 class="text-h6 font-weight-bold mb-2">{{ feature.title }}</h4>
              <p class="text-body-2 text-medium-emphasis">
                {{ feature.description }}
              </p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials-section py-12 bg-grey-lighten-5">
      <v-container>
        <div class="text-center mb-12">
          <h2 class="text-h4 text-md-h3 font-weight-bold mb-4">
            نظرات فروشندگان ما
          </h2>
          <p class="text-h6 text-medium-emphasis mx-auto" style="max-width: 700px">
            شنیدن تجربه‌های واقعی فروشندگانی که با ما همکاری می‌کنند
          </p>
        </div>
        <v-row>
          <v-col
            v-for="testimonial in testimonials"
            :key="testimonial.name"
            cols="12"
            md="6"
            lg="4"
            class="mb-4"
          >
            <v-card elevation="2" rounded="xl" class="testimonial-card h-100 pa-6">
              <div class="d-flex align-center mb-4">
                <v-rating
                  :model-value="5"
                  readonly
                  size="small"
                  color="amber"
                  density="compact"
                />
              </div>
              <p class="text-body-1 text-medium-emphasis mb-6" style="font-style: italic">
                "{{ testimonial.quote }}"
              </p>
              <div class="d-flex align-center">
                <v-avatar color="primary" variant="tonal" size="48" class="ml-4">
                  <v-icon>mdi-account</v-icon>
                </v-avatar>
                <div>
                  <div class="text-body-1 font-weight-bold">{{ testimonial.name }}</div>
                  <div class="text-caption text-medium-emphasis">{{ testimonial.role }}</div>
                  <div class="text-caption text-medium-emphasis">{{ testimonial.company }}</div>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-16">
      <v-container>
        <v-card
          elevation="8"
          rounded="xl"
          color="primary"
          class="cta-card pa-8 pa-md-12 text-center"
        >
          <v-icon size="80" color="white" class="mb-6">mdi-rocket-launch</v-icon>
          <h2 class="text-h4 text-md-h3 font-weight-bold text-white mb-4">
            آماده شروع هستید؟
          </h2>
          <p class="text-h6 text-white mb-8 mx-auto" style="max-width: 600px; opacity: 0.95">
            همین امروز به پلتفرم ایندکسو بپیوندید و فروش خود را افزایش دهید
          </p>
          <div class="d-flex flex-column flex-sm-row justify-center gap-4">
            <v-btn
              color="white"
              size="x-large"
              rounded="lg"
              prepend-icon="mdi-account-plus"
              :to="registerLink"
              class="px-8 text-primary"
            >
              ثبت‌نام رایگان
            </v-btn>
            <v-btn
              color="white"
              variant="outlined"
              size="x-large"
              rounded="lg"
              prepend-icon="mdi-phone"
              to="/contact"
              class="px-8"
            >
              تماس با ما
            </v-btn>
          </div>
        </v-card>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'فروشنده شوید | ایندکسو',
  meta: [
    {
      name: 'description',
      content: 'به بزرگ‌ترین پلتفرم B2B ماشین‌آلات صنعتی ایران بپیوندید. دسترسی به هزاران خریدار صنعتی، افزایش فروش و رشد کسب‌وکار خود را با ایندکسو تجربه کنید.'
    },
    {
      property: 'og:title',
      content: 'فروشنده شوید | ایندکسو'
    },
    {
      property: 'og:description',
      content: 'به بزرگ‌ترین پلتفرم B2B ماشین‌آلات صنعتی ایران بپیوندید و فروش خود را افزایش دهید.'
    },
    {
      property: 'og:type',
      content: 'website'
    }
  ]
})

// Link to register page (can be enhanced to pre-select seller role via query param or state)
const registerLink = '/register'

const statistics = [
  {
    icon: 'mdi-account-group',
    value: '۱۰۰۰+',
    label: 'فروشنده فعال'
  },
  {
    icon: 'mdi-shopping',
    value: '۵۰۰۰+',
    label: 'خریدار صنعتی'
  },
  {
    icon: 'mdi-package-variant',
    value: '۵۰۰۰۰+',
    label: 'محصول فعال'
  },
  {
    icon: 'mdi-chart-line',
    value: '۹۵٪',
    label: 'رضایت فروشندگان'
  }
]

const benefits = [
  {
    icon: 'mdi-account-search',
    color: 'primary',
    title: 'دسترسی به خریداران صنعتی',
    description: 'با هزاران خریدار صنعتی و تولیدکننده در ارتباط باشید و فرصت‌های فروش جدید را کشف کنید.'
  },
  {
    icon: 'mdi-chart-timeline-variant',
    color: 'success',
    title: 'تحلیل عملکرد فروش',
    description: 'با داشبورد تحلیلی پیشرفته، عملکرد محصولات و فروش خود را در زمان واقعی رصد کنید.'
  },
  {
    icon: 'mdi-shield-check',
    color: 'info',
    title: 'امنیت معاملات',
    description: 'پلتفرم امن و قابل اعتماد برای انجام معاملات B2B با تضمین پرداخت و تحویل.'
  },
  {
    icon: 'mdi-tools',
    color: 'warning',
    title: 'ابزارهای مدیریت فروش',
    description: 'سیستم مدیریت ارتباط با مشتریان (CRM)، مدیریت محصولات و مدیریت سفارشات در یک پلتفرم.'
  },
  {
    icon: 'mdi-web',
    color: 'purple',
    title: 'نمایشگاه آنلاین اختصاصی',
    description: 'صفحه اختصاصی برای نمایش محصولات، نمونه‌کارها و اطلاعات شرکت شما به خریداران.'
  },
  {
    icon: 'mdi-headset',
    color: 'orange',
    title: 'پشتیبانی اختصاصی',
    description: 'تیم پشتیبانی حرفه‌ای برای کمک به شما در استفاده از پلتفرم و افزایش فروش.'
  }
]

const features = [
  {
    icon: 'mdi-view-dashboard',
    title: 'داشبورد مدیریتی',
    description: 'داشبورد جامع برای مدیریت تمام جنبه‌های کسب‌وکار شما از یک مکان'
  },
  {
    icon: 'mdi-package-variant-closed',
    title: 'مدیریت محصولات',
    description: 'افزودن، ویرایش و مدیریت محصولات با جزئیات کامل و تصاویر با کیفیت'
  },
  {
    icon: 'mdi-account-supervisor',
    title: 'سیستم CRM',
    description: 'مدیریت ارتباط با مشتریان، ردیابی فرصت‌های فروش و مدیریت لیدها'
  },
  {
    icon: 'mdi-chat-processing',
    title: 'سیستم چت',
    description: 'ارتباط مستقیم با خریداران از طریق سیستم چت یکپارچه پلتفرم'
  },
  {
    icon: 'mdi-file-document-multiple',
    title: 'مدیریت سفارشات',
    description: 'پیگیری و مدیریت تمام سفارشات از مرحله ثبت تا تحویل'
  },
  {
    icon: 'mdi-chart-box',
    title: 'گزارش‌گیری و آمار',
    description: 'گزارش‌های تفصیلی از فروش، بازدید محصولات و عملکرد کلی'
  },
  {
    icon: 'mdi-cash-multiple',
    title: 'مدیریت پرداخت‌ها',
    description: 'پیگیری پرداخت‌ها، فاکتورها و تاریخچه مالی در یک مکان'
  },
  {
    icon: 'mdi-star-circle',
    title: 'سیستم امتیازدهی',
    description: 'سیستم گیمیفیکیشن برای بهبود عملکرد و افزایش اعتبار فروشنده'
  },
  {
    icon: 'mdi-bullhorn',
    title: 'تبلیغات و بازاریابی',
    description: 'امکانات تبلیغاتی برای افزایش دیده شدن محصولات و فروش بیشتر'
  }
]

const testimonials = [
  {
    name: 'محمد احمدی',
    role: 'مدیر فروش',
    company: 'کارخانه تولید ماشین‌آلات صنعتی پارس',
    quote: 'از زمانی که به پلتفرم ایندکسو پیوستیم، فروش ما ۳۰۰ درصد افزایش یافته است. دسترسی به خریداران صنعتی واقعی و سیستم مدیریتی عالی باعث شد بتوانیم کسب‌وکار خود را به سطح جدیدی برسانیم.'
  },
  {
    name: 'زهرا کریمی',
    role: 'مدیر عامل',
    company: 'شرکت تجهیزات تولیدی نوآور',
    quote: 'پلتفرم ایندکسو نه تنها فروش ما را افزایش داده، بلکه اعتبار برند ما را نیز بالا برده است. سیستم CRM و ابزارهای تحلیلی به ما کمک کرده تا بهتر با مشتریان ارتباط برقرار کنیم و خدمات بهتری ارائه دهیم.'
  },
  {
    name: 'علی رضایی',
    role: 'مدیر بازاریابی',
    company: 'گروه صنعتی تکنولوژی پیشرفته',
    quote: 'بهترین تصمیمی که در سال گذشته گرفتیم، پیوستن به ایندکسو بود. پشتیبانی عالی، رابط کاربری ساده و دسترسی به مشتریان هدف واقعاً معجزه کرد. به تمام تولیدکنندگان ماشین‌آلات صنعتی توصیه می‌کنم.'
  }
]
</script>

<style scoped>
.seller-landing {
  background-color: rgb(var(--v-theme-surface));
}

.hero-section {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05), rgba(var(--v-theme-secondary), 0.08));
  border-radius: 0 0 24px 24px;
  margin-bottom: 32px;
}

.hero-content-col {
  display: flex;
  align-items: center;
}

.hero-image-col {
  display: flex;
  align-items: stretch;
}

.hero-image-wrapper {
  width: 100%;
  height: 100%;
  border-radius: 0 0 24px 0;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.statistics-section {
  background-color: rgb(var(--v-theme-surface));
}

.stat-card {
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
  border-radius: 16px;
  background-color: rgb(var(--v-theme-surface));
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.15);
}

.benefit-card {
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
}

.benefit-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.feature-card {
  transition: transform 0.2s;
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
}

.feature-card:hover {
  transform: translateY(-2px);
}

.testimonial-card {
  background-color: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.testimonial-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.cta-section {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1), rgba(var(--v-theme-secondary), 0.15));
}

.cta-card {
  position: relative;
  overflow: hidden;
}

.cta-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

@media (max-width: 960px) {
  .hero-section {
    border-radius: 0;
  }
  
  .hero-image-wrapper {
    border-radius: 0;
  }
  
  .hero-content {
    text-align: center;
  }
}

@media (max-width: 600px) {
  .hero-section [style*="min-height"] {
    min-height: 400px !important;
  }
  
  .stat-card {
    padding: 24px !important;
  }
}
</style>

