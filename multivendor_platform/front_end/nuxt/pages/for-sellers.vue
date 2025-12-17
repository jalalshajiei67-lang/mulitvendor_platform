<template>
  <div class="for-sellers" dir="rtl">
    <!-- Hero Section -->
    <section class="hero-section">
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="12" md="10" lg="8" class="text-center">
            <div class="hero-badge mb-4">
              <v-chip color="primary" size="large" variant="tonal">
                <v-icon start>mdi-store</v-icon>
                پلتفرم B2B ایندکسو
              </v-chip>
            </div>
            
            <h1 class="hero-title text-h3 text-md-h2 font-weight-bold mb-4">
              فروش بیشتر، رشد سریع‌تر با ایندکسو
            </h1>
            
            <p class="hero-subtitle text-h6 text-medium-emphasis mb-8">
              به بزرگ‌ترین پلتفرم خرید و فروش ماشین‌آلات صنعتی کشور بپیوندید و کسب‌وکار خود را متحول کنید
            </p>
            
            <div class="cta-buttons">
              <v-btn
                size="x-large"
                color="primary"
                rounded="lg"
                elevation="4"
                class="px-8"
                @click="scrollToRegister"
              >
                <v-icon start>mdi-rocket-launch</v-icon>
                همین الان شروع کنید
              </v-btn>
              
              <v-btn
                size="x-large"
                variant="outlined"
                rounded="lg"
                class="px-8 mr-3"
                @click="scrollToBenefits"
              >
                مزایا را ببینید
                <v-icon end>mdi-chevron-down</v-icon>
              </v-btn>
            </div>
            
            <!-- Trust Indicators -->
            <div class="trust-indicators mt-12">
              <v-row justify="center">
                <v-col cols="6" sm="3" v-for="stat in stats" :key="stat.label">
                  <div class="stat-card">
                    <div class="stat-number text-h4 font-weight-bold text-primary">
                      {{ stat.number }}
                    </div>
                    <div class="stat-label text-body-2 text-medium-emphasis">
                      {{ stat.label }}
                    </div>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Benefits Section -->
    <section class="benefits-section py-16" ref="benefitsSection">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            چرا ایندکسو؟
          </h2>
          <p class="text-h6 text-medium-emphasis">
            مزایای عضویت در پلتفرم B2B ایندکسو
          </p>
        </div>

        <v-row>
          <v-col 
            cols="12" 
            sm="6" 
            lg="4"
            v-for="(benefit, index) in benefits" 
            :key="index"
          >
            <v-card 
              class="benefit-card h-100 pa-6" 
              elevation="2"
              rounded="lg"
              :class="{ 'featured': benefit.featured }"
            >
              <div class="benefit-icon mb-4">
                <v-avatar :color="benefit.color" size="64">
                  <v-icon size="32" color="white">{{ benefit.icon }}</v-icon>
                </v-avatar>
              </div>
              
              <h3 class="text-h6 font-weight-bold mb-3">
                {{ benefit.title }}
              </h3>
              
              <p class="text-body-2 text-medium-emphasis">
                {{ benefit.description }}
              </p>

              <v-chip 
                v-if="benefit.featured" 
                color="primary" 
                variant="flat" 
                size="small"
                class="mt-3"
              >
                محبوب‌ترین
              </v-chip>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Features Section -->
    <section class="features-section py-16 bg-surface-variant">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            امکانات ویژه برای فروشندگان
          </h2>
          <p class="text-h6 text-medium-emphasis">
            ابزارهای حرفه‌ای برای مدیریت و رشد کسب‌وکار شما
          </p>
        </div>

        <v-row>
          <v-col 
            cols="12" 
            md="6"
            v-for="(feature, index) in features" 
            :key="index"
          >
            <v-card class="feature-card pa-6" elevation="0" rounded="lg">
              <div class="d-flex align-start">
                <v-icon 
                  :color="feature.color" 
                  size="40"
                  class="ml-4"
                >
                  {{ feature.icon }}
                </v-icon>
                
                <div>
                  <h3 class="text-h6 font-weight-bold mb-2">
                    {{ feature.title }}
                  </h3>
                  
                  <p class="text-body-2 text-medium-emphasis mb-3">
                    {{ feature.description }}
                  </p>
                  
                  <ul class="feature-list">
                    <li v-for="item in feature.items" :key="item">
                      <v-icon size="small" color="success" class="ml-1">mdi-check-circle</v-icon>
                      {{ item }}
                    </li>
                  </ul>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Pricing Plans Section -->
    <section class="pricing-section py-16">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            پکیج‌های عضویت
          </h2>
          <p class="text-h6 text-medium-emphasis">
            بسته مناسب برای کسب‌وکار خود را انتخاب کنید
          </p>
        </div>

        <v-row justify="center">
          <v-col 
            cols="12" 
            sm="6" 
            md="4"
            v-for="(plan, index) in pricingPlans" 
            :key="index"
          >
            <v-card 
              class="pricing-card pa-6 h-100" 
              :elevation="plan.popular ? 8 : 2"
              rounded="lg"
              :class="{ 'popular-plan': plan.popular }"
            >
              <v-chip 
                v-if="plan.popular" 
                color="primary" 
                variant="flat"
                class="mb-4"
              >
                محبوب‌ترین
              </v-chip>
              
              <h3 class="text-h5 font-weight-bold mb-2">
                {{ plan.name }}
              </h3>
              
              <div class="price mb-4">
                <span class="text-h3 font-weight-bold">{{ plan.price }}</span>
                <span class="text-body-1 text-medium-emphasis mr-2">{{ plan.period }}</span>
              </div>
              
              <v-divider class="my-4" />
              
              <ul class="plan-features mb-6">
                <li v-for="feature in plan.features" :key="feature">
                  <v-icon size="small" color="success" class="ml-2">mdi-check</v-icon>
                  {{ feature }}
                </li>
              </ul>
              
              <v-btn 
                :color="plan.popular ? 'primary' : 'default'"
                :variant="plan.popular ? 'flat' : 'outlined'"
                block
                size="large"
                rounded="lg"
                @click="selectPlan(plan)"
              >
                {{ plan.buttonText }}
              </v-btn>
            </v-card>
          </v-col>
        </v-row>

        <div class="text-center mt-8">
          <p class="text-body-1 text-medium-emphasis">
            نیاز به مشاوره دارید؟ 
            <NuxtLink to="/contact" class="text-primary font-weight-bold">
              با ما تماس بگیرید
            </NuxtLink>
          </p>
        </div>
      </v-container>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section py-16 bg-surface-variant">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            چطور شروع کنم؟
          </h2>
          <p class="text-h6 text-medium-emphasis">
            تنها در ۳ مرحله ساده، فروش خود را شروع کنید
          </p>
        </div>

        <v-row class="steps-container">
          <v-col 
            cols="12" 
            md="4"
            v-for="(step, index) in steps" 
            :key="index"
          >
            <div class="step-card text-center">
              <div class="step-number mb-4">
                <v-avatar color="primary" size="72">
                  <span class="text-h4 font-weight-bold">{{ index + 1 }}</span>
                </v-avatar>
              </div>
              
              <v-icon :color="step.color" size="48" class="mb-4">
                {{ step.icon }}
              </v-icon>
              
              <h3 class="text-h6 font-weight-bold mb-3">
                {{ step.title }}
              </h3>
              
              <p class="text-body-2 text-medium-emphasis">
                {{ step.description }}
              </p>
            </div>
            
            <div 
              v-if="index < steps.length - 1" 
              class="step-arrow d-none d-md-block"
            >
              <v-icon color="primary" size="32">mdi-arrow-left</v-icon>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials-section py-16">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            فروشندگان ما چه می‌گویند؟
          </h2>
          <p class="text-h6 text-medium-emphasis">
            تجربه واقعی شرکا و تولیدکنندگان در ایندکسو
          </p>
        </div>

        <v-row>
          <v-col 
            cols="12" 
            md="4"
            v-for="(testimonial, index) in testimonials" 
            :key="index"
          >
            <v-card class="testimonial-card pa-6 h-100" elevation="2" rounded="lg">
              <v-icon color="primary" size="32" class="mb-4">mdi-format-quote-close</v-icon>
              
              <p class="text-body-1 mb-6">
                {{ testimonial.quote }}
              </p>
              
              <div class="d-flex align-center">
                <v-avatar color="primary" size="48" class="ml-3">
                  <span class="text-h6">{{ testimonial.initial }}</span>
                </v-avatar>
                
                <div>
                  <div class="font-weight-bold">{{ testimonial.name }}</div>
                  <div class="text-body-2 text-medium-emphasis">{{ testimonial.company }}</div>
                </div>
              </div>
              
              <v-rating
                :model-value="testimonial.rating"
                color="warning"
                half-increments
                readonly
                density="compact"
                class="mt-3"
              />
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section py-16 bg-surface-variant">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            سؤالات متداول
          </h2>
          <p class="text-h6 text-medium-emphasis">
            پاسخ سؤالات رایج فروشندگان
          </p>
        </div>

        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <v-expansion-panels variant="accordion">
              <v-expansion-panel
                v-for="(faq, index) in faqs"
                :key="index"
                rounded="lg"
                class="mb-3"
              >
                <v-expansion-panel-title class="text-h6 font-weight-medium">
                  {{ faq.question }}
                </v-expansion-panel-title>
                <v-expansion-panel-text class="text-body-1">
                  {{ faq.answer }}
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>

            <div class="text-center mt-8">
              <NuxtLink to="/faqs" class="text-primary font-weight-bold text-h6">
                مشاهده تمام سؤالات
                <v-icon>mdi-arrow-left</v-icon>
              </NuxtLink>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-16" ref="registerSection">
      <v-container>
        <v-card 
          class="cta-card pa-8 pa-md-12" 
          color="primary"
          elevation="12"
          rounded="xl"
        >
          <v-row align="center" justify="center">
            <v-col cols="12" md="8" class="text-center">
              <h2 class="text-h3 text-md-h2 font-weight-bold mb-4 text-white">
                آماده شروع هستید؟
              </h2>
              
              <p class="text-h6 mb-8 text-white opacity-90">
                همین امروز به جمع فروشندگان موفق ایندکسو بپیوندید و فروش خود را چند برابر کنید
              </p>
              
              <div class="cta-actions">
                <v-btn
                  size="x-large"
                  color="white"
                  rounded="lg"
                  elevation="4"
                  class="px-8"
                  @click="goToRegister"
                >
                  <v-icon start>mdi-account-plus</v-icon>
                  ثبت‌نام رایگان
                </v-btn>
                
                <v-btn
                  size="x-large"
                  variant="outlined"
                  color="white"
                  rounded="lg"
                  class="px-8 mr-3"
                  @click="goToContact"
                >
                  تماس با فروش
                  <v-icon end>mdi-phone</v-icon>
                </v-btn>
              </div>
              
              <p class="text-body-1 mt-6 text-white opacity-75">
                <v-icon color="white" size="small" class="ml-1">mdi-check-circle</v-icon>
                بدون نیاز به پرداخت هزینه
                <span class="mx-2">•</span>
                <v-icon color="white" size="small" class="ml-1">mdi-check-circle</v-icon>
                راه‌اندازی در کمتر از ۵ دقیقه
              </p>
            </v-col>
          </v-row>
        </v-card>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
// SEO and Meta
useHead({
  title: 'ایندکسو برای فروشندگان - پلتفرم B2B فروش ماشین‌آلات صنعتی',
  meta: [
    {
      name: 'description',
      content: 'به بزرگ‌ترین پلتفرم B2B خرید و فروش ماشین‌آلات صنعتی بپیوندید. فروش بیشتر، دسترسی به هزاران خریدار، مدیریت آسان محصولات و پشتیبانی ۲۴/۷'
    },
    {
      property: 'og:title',
      content: 'ایندکسو برای فروشندگان - رشد کسب‌وکار شما'
    },
    {
      property: 'og:description',
      content: 'با ایندکسو فروش خود را متحول کنید. دسترسی به هزاران خریدار صنعتی در سراسر کشور'
    }
  ]
})

// Refs
const benefitsSection = ref<HTMLElement | null>(null)
const registerSection = ref<HTMLElement | null>(null)

// Stats Data
const stats = [
  { number: '+۱۰۰۰', label: 'فروشنده فعال' },
  { number: '+۵۰۰۰', label: 'خریدار' },
  { number: '+۱۵۰۰۰', label: 'محصول' },
  { number: '۹۸٪', label: 'رضایت مشتریان' }
]

// Benefits Data
const benefits = [
  {
    icon: 'mdi-account-group',
    title: 'دسترسی به هزاران خریدار',
    description: 'به شبکه گسترده خریداران صنعتی و تولیدکنندگان در سراسر کشور دسترسی پیدا کنید و فروش خود را افزایش دهید.',
    color: 'primary',
    featured: true
  },
  {
    icon: 'mdi-chart-line',
    title: 'افزایش فروش تا ۳ برابر',
    description: 'با استفاده از ابزارهای بازاریابی و نمایش بهینه محصولات، فروش خود را به طور متوسط تا ۳ برابر افزایش دهید.',
    color: 'success',
    featured: false
  },
  {
    icon: 'mdi-clock-fast',
    title: 'مدیریت آسان و سریع',
    description: 'پنل کاربری قدرتمند برای مدیریت محصولات، سفارشات، پیام‌ها و گزارش‌های فروش در یک محیط یکپارچه.',
    color: 'info',
    featured: false
  },
  {
    icon: 'mdi-shield-check',
    title: 'امنیت و اعتبار',
    description: 'با نشان‌های تأیید، رتبه‌بندی فروشندگان و سیستم احراز هویت، اعتماد مشتریان را جلب کنید.',
    color: 'warning',
    featured: false
  },
  {
    icon: 'mdi-headset',
    title: 'پشتیبانی مداوم',
    description: 'تیم پشتیبانی ما همیشه آماده است تا در مسیر فروش و رشد کسب‌وکار شما همراهتان باشد.',
    color: 'purple',
    featured: false
  },
  {
    icon: 'mdi-cash-multiple',
    title: 'بدون هزینه راه‌اندازی',
    description: 'بدون نیاز به سرمایه اولیه، کسب‌وکار خود را شروع کنید. فقط در صورت فروش، کمیسیون پرداخت می‌کنید.',
    color: 'teal',
    featured: false
  }
]

// Features Data
const features = [
  {
    icon: 'mdi-store-cog',
    title: 'پنل فروشندگی حرفه‌ای',
    description: 'داشبورد کامل برای مدیریت کسب‌وکار آنلاین',
    color: 'primary',
    items: [
      'مدیریت محصولات و موجودی',
      'پیگیری سفارشات و فاکتورها',
      'گزارش‌های فروش تحلیلی',
      'مدیریت پیام‌ها و درخواست‌های خرید'
    ]
  },
  {
    icon: 'mdi-bullhorn',
    title: 'ابزارهای بازاریابی',
    description: 'محصولات خود را به بهترین شکل نمایش دهید',
    color: 'success',
    items: [
      'تبلیغات هدفمند',
      'سئو و بهینه‌سازی محصولات',
      'نمایش در صفحه اول',
      'پیشنهادات ویژه و تخفیف‌ها'
    ]
  },
  {
    icon: 'mdi-web',
    title: 'مینی‌سایت اختصاصی',
    description: 'رزومه آنلاین شرکت شما',
    color: 'info',
    items: [
      'طراحی اختصاصی برای برند شما',
      'کاتالوگ محصولات و پروژه‌های اجرا شده',
      'معرفی تیم و گواهینامه‌ها',
      'لینک اشتراک‌گذاری در شبکه‌های اجتماعی'
    ]
  },
  {
    icon: 'mdi-chart-box',
    title: 'تحلیل و گزارش‌گیری',
    description: 'آمار دقیق برای تصمیم‌گیری بهتر',
    color: 'warning',
    items: [
      'آمار بازدید و تعاملات',
      'گزارش فروش و درآمد',
      'تحلیل رفتار مشتریان',
      'پیشنهادات بهبود فروش'
    ]
  }
]

// Pricing Plans Data
const pricingPlans = [
  {
    name: 'پایه',
    price: 'رایگان',
    period: '',
    popular: false,
    features: [
      'حداکثر ۲۰ محصول',
      'پنل فروشندگی پایه',
      'پشتیبانی فقط آنلاین',
      'گزارش‌های ساده'
    ],
    buttonText: 'شروع رایگان'
  },
  {
    name: 'حرفه‌ای',
    price: '1٫500٫000',
    period: 'تومان / ماه',
    popular: true,
    features: [
      'محصولات نامحدود',
      'پنل پیشرفته فروشندگی',
      'پشتیبانی اختصاصی بی وقفه',
      'کمیسیون شناور',
      'مینی‌سایت اختصاصی',
      'ابزارهای بازاریابی پیشرفته',
      'تحلیل و گزارش‌های تفصیلی',
      'نمایش در صفحه اول'
    ],
    buttonText: 'انتخاب پکیج حرفه‌ای'
  },
  {
    name: 'سازمانی',
    price: 'تماس بگیرید',
    period: '',
    popular: false,
    features: [
      'تمام امکانات حرفه‌ای',
      'مدیر حساب اختصاصی',
      'کمیسیون قابل مذاکره',
      'API اختصاصی',
      'آموزش و مشاوره',
      'قراردادهای سازمانی',
      'امکانات سفارشی'
    ],
    buttonText: 'تماس با فروش'
  }
]

// Steps Data
const steps = [
  {
    icon: 'mdi-account-plus',
    title: 'ثبت‌نام کنید',
    description: 'در کمتر از ۲ دقیقه حساب کاربری خود را ایجاد کنید و به پنل فروشندگی دسترسی پیدا کنید.',
    color: 'primary'
  },
  {
    icon: 'mdi-package-variant-plus',
    title: 'محصولات اضافه کنید',
    description: 'محصولات خود را با عکس، توضیحات و قیمت به راحتی در پلتفرم ثبت کنید.',
    color: 'success'
  },
  {
    icon: 'mdi-rocket-launch',
    title: 'شروع به فروش کنید',
    description: 'محصولات شما برای هزاران خریدار نمایش داده می‌شود و سفارشات را از پنل خود مدیریت کنید.',
    color: 'warning'
  }
]

// Testimonials Data
const testimonials = [
  {
    quote: 'بعد از عضویت در ایندکسو، فروش ما 2 برابر شد. دسترسی به خریداران صنعتی واقعاً تفاوت ایجاد کرده.',
    name: 'محمد رضایی',
    company: 'شرکت ماشین‌سازی پارس',
    initial: 'م',
    rating: 5
  },
  {
    quote: 'پنل فروشندگی خیلی کاربردی و راحته. همه چیز رو از یک جا مدیریت می‌کنم و تیم پشتیبانی هم عالیه.',
    name: 'زهرا احمدی',
    company: 'تجهیزات صنعتی آریا',
    initial: 'ز',
    rating: 5
  },
  {
    quote: 'قبلاً برای پیدا کردن مشتری خیلی وقت می‌گذاشتم. الان مشتریا خودشون به من پیام می‌دن و سفارش می‌دن.',
    name: 'علی کریمی',
    company: 'ماشین‌آلات کیان',
    initial: 'ع',
    rating: 4.5
  }
]

// FAQ Data
const faqs = [
  {
    question: 'آیا ثبت‌نام در ایندکسو رایگان است؟',
    answer: 'بله، ثبت‌نام و شروع فروش در ایندکسو کاملاً رایگان است. شما می‌توانید با پکیج رایگان شروع کنید و در صورت نیاز به امکانات بیشتر، به پکیج‌های پولی ارتقا دهید.'
  },
  {
    question: 'کمیسیون ایندکسو چقدر است؟',
    answer: 'کمیسیون بسته به پکیجی که انتخاب می‌کنید متفاوت است. پکیج رایگان بدون هزینه پکیج حرفه‌ای دارای پرداخت ماهیانه  و پکیج سازمانی بدون هزینه ثابت و شامل کمیسیون از فروش می شود..'
  },
  {
    question: 'چند وقت طول می‌کشد تا محصولاتم تأیید شوند؟',
    answer: 'پس از ثبت محصولات، تیم ما در کمتر از ۲۴ ساعت آن‌ها را بررسی و تأیید می‌کند. در صورت نیاز به اصلاحات، از طریق پنل به شما اطلاع می‌دهیم.'
  },
  {
    question: 'آیا می‌توانم محصولات خود را در چند دسته مختلف ثبت کنم؟',
    answer: 'بله، شما می‌توانید محصولات خود را در تمام دسته‌بندی‌های مرتبط ثبت کنید تا بیشتر دیده شوند.'
  },
  {
    question: 'پشتیبانی چگونه است؟',
    answer: 'ما پشتیبانی از طریق چت آنلاین، ایمیل و تلفن ارائه می‌دهیم. در پکیج حرفه‌ای و بالاتر، پشتیبانی ۲۴/۷ در دسترس است.'
  }
]

// Methods
const scrollToBenefits = () => {
  benefitsSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const scrollToRegister = () => {
  registerSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const selectPlan = (plan: any) => {
  if (plan.name === 'سازمانی') {
    navigateTo('/contact')
  } else {
    navigateTo('/register')
  }
}

const goToRegister = () => {
  navigateTo('/register')
}

const goToContact = () => {
  navigateTo('/contact')
}
</script>

<style scoped>
.for-sellers {
  min-height: 100vh;
  background: rgb(var(--v-theme-background));
}

/* Hero Section */
.hero-section {
  padding: 80px 0 60px;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-secondary)) 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.hero-badge {
  animation: fadeInDown 0.6s ease-out;
}

.hero-title {
  color: white;
  line-height: 1.3;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.hero-subtitle {
  color: rgba(255, 255, 255, 0.9);
  animation: fadeInUp 0.6s ease-out 0.4s both;
}

.cta-buttons {
  animation: fadeInUp 0.6s ease-out 0.6s both;
}

.trust-indicators {
  animation: fadeInUp 0.6s ease-out 0.8s both;
}

.stat-card {
  padding: 20px;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.stat-number {
  color: white;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
}

/* Benefits Section */
.benefits-section {
  background: rgb(var(--v-theme-background));
}

.benefit-card {
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.benefit-card:hover {
  transform: translateY(-8px);
  border-color: rgb(var(--v-theme-primary));
}

.benefit-card.featured {
  border-color: rgb(var(--v-theme-primary));
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05) 0%, transparent 100%);
}

/* Features Section */
.feature-card {
  background: white;
  transition: all 0.3s ease;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.feature-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  padding: 8px 0;
  display: flex;
  align-items: center;
}

/* Pricing Section */
.pricing-card {
  border: 2px solid rgba(var(--v-theme-on-surface), 0.08);
  transition: all 0.3s ease;
}

.pricing-card:hover {
  transform: translateY(-8px);
}

.popular-plan {
  border-color: rgb(var(--v-theme-primary));
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05) 0%, transparent 100%);
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.plan-features li {
  padding: 12px 0;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.plan-features li:last-child {
  border-bottom: none;
}

/* Steps Section */
.steps-container {
  position: relative;
}

.step-card {
  padding: 30px 20px;
}

.step-arrow {
  position: absolute;
  top: 50%;
  left: -16px;
  transform: translateY(-50%);
}

/* Testimonials Section */
.testimonial-card {
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-4px);
}

/* CTA Section */
.cta-section {
  background: rgb(var(--v-theme-background));
}

.cta-card {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-secondary)) 100%);
}

/* Animations */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile Responsive */
@media (max-width: 960px) {
  .hero-section {
    padding: 60px 0 40px;
  }

  .hero-title {
    font-size: 2rem !important;
  }

  .hero-subtitle {
    font-size: 1.1rem !important;
  }

  .cta-buttons .v-btn {
    display: block;
    width: 100%;
    margin: 8px 0 !important;
  }

  .section-header h2 {
    font-size: 1.8rem !important;
  }

  .benefit-card,
  .feature-card,
  .pricing-card,
  .testimonial-card {
    margin-bottom: 16px;
  }

  .step-arrow {
    display: none !important;
  }
}

/* RTL Adjustments */
[dir="rtl"] .cta-buttons .v-btn {
  margin-right: 0;
  margin-left: 12px;
}

[dir="rtl"] .cta-buttons .v-btn:first-child {
  margin-left: 0;
}
</style>

