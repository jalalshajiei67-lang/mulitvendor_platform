<template>
  <div class="for-buyers" dir="rtl">
    <!-- Hero Section -->
    <section class="hero-section">
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="12" md="10" lg="8" class="text-center">
            <div class="hero-badge mb-4">
              <v-chip color="primary" size="large" variant="tonal">
                <v-icon start>mdi-shopping</v-icon>
                پلتفرم B2B ایندکسو
              </v-chip>
            </div>
            
            <h1 class="hero-title text-h3 text-md-h2 font-weight-bold mb-4">
              خرید مطمئن ماشین‌آلات از بهترین تولیدکنندگان
            </h1>
            
            <p class="hero-subtitle text-h6 text-medium-emphasis mb-8">
              دسترسی مستقیم به هزاران تولیدکننده معتبر صنعتی در یک پلتفرم
            </p>
            
            <div class="cta-buttons">
              <v-btn
                size="x-large"
                color="primary"
                rounded="lg"
                elevation="4"
                class="px-8"
                @click="goToBrowse"
              >
                <v-icon start>mdi-view-grid</v-icon>
                مشاهده محصولات
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
            چرا از ایندکسو خرید کنیم؟
          </h2>
          <p class="text-h6 text-medium-emphasis">
            مزایای خرید از پلتفرم B2B ایندکسو
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
                برجسته
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
            امکانات ویژه برای خریداران
          </h2>
          <p class="text-h6 text-medium-emphasis">
            ابزارهای هوشمند برای خرید بهتر و سریع‌تر
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

    <!-- Categories Section -->
    <section class="categories-section py-16">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            دسته‌بندی محصولات
          </h2>
          <p class="text-h6 text-medium-emphasis">
            هر آنچه برای صنعت و تولید نیاز دارید
          </p>
        </div>

        <v-row>
          <v-col 
            cols="6" 
            sm="4"
            md="3"
            v-for="(category, index) in categories" 
            :key="index"
          >
            <v-card 
              class="category-card pa-6 h-100 text-center" 
              elevation="2"
              rounded="lg"
              @click="goToCategory(category.slug)"
            >
              <v-icon 
                :color="category.color" 
                size="48"
                class="mb-3"
              >
                {{ category.icon }}
              </v-icon>
              
              <h3 class="text-body-1 font-weight-bold">
                {{ category.title }}
              </h3>
              
              <p class="text-caption text-medium-emphasis mt-2">
                {{ category.count }}+ محصول
              </p>
            </v-card>
          </v-col>
        </v-row>

        <div class="text-center mt-8">
          <v-btn
            color="primary"
            variant="outlined"
            size="large"
            rounded="lg"
            @click="goToCategories"
          >
            مشاهده تمام دسته‌بندی‌ها
            <v-icon end>mdi-arrow-left</v-icon>
          </v-btn>
        </div>
      </v-container>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section py-16 bg-surface-variant">
      <v-container>
        <div class="section-header text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            چطور از ایندکسو خرید کنم؟
          </h2>
          <p class="text-h6 text-medium-emphasis">
            تنها در ۴ مرحله ساده، خرید خود را انجام دهید
          </p>
        </div>

        <v-row class="steps-container">
          <v-col 
            cols="12" 
            sm="6"
            md="3"
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
            خریداران ما چه می‌گویند؟
          </h2>
          <p class="text-h6 text-medium-emphasis">
            تجربه واقعی خریداران و کارخانجات
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
            پاسخ سؤالات رایج خریداران
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

    <!-- Request Quote Section -->
    <section class="request-quote-section py-16">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6">
            <div class="request-quote-content">
              <v-chip color="primary" variant="tonal" class="mb-4">
                <v-icon start>mdi-file-document-edit</v-icon>
                درخواست خرید (RFQ)
              </v-chip>
              
              <h2 class="text-h3 font-weight-bold mb-4">
                محصول مورد نظر را پیدا نکردید؟
              </h2>
              
              <p class="text-h6 text-medium-emphasis mb-6">
                درخواست خرید خود را ثبت کنید تا تولیدکنندگان با بهترین قیمت به شما پیشنهاد بدهند
              </p>
              
              <ul class="feature-list mb-6">
                <li>
                  <v-icon color="success" class="ml-2">mdi-check-circle</v-icon>
                  دریافت پیشنهاد از چندین تولیدکننده
                </li>
                <li>
                  <v-icon color="success" class="ml-2">mdi-check-circle</v-icon>
                  مقایسه قیمت‌ها و انتخاب بهترین
                </li>
                <li>
                  <v-icon color="success" class="ml-2">mdi-check-circle</v-icon>
                  صرفه‌جویی در زمان و هزینه
                </li>
                <li>
                  <v-icon color="success" class="ml-2">mdi-check-circle</v-icon>
                  مشاوره رایگان
                </li>
              </ul>
              
              <v-btn
                color="primary"
                size="x-large"
                rounded="lg"
                elevation="4"
                @click="goToRFQ"
              >
                <v-icon start>mdi-file-plus</v-icon>
                ثبت درخواست خرید
              </v-btn>
            </div>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card class="rfq-demo-card pa-6" elevation="8" rounded="lg">
              <div class="demo-icon text-center mb-4">
                <v-avatar color="primary" size="80">
                  <v-icon size="40" color="white">mdi-file-document-multiple</v-icon>
                </v-avatar>
              </div>
              
              <h3 class="text-h6 font-weight-bold text-center mb-4">
                نمونه درخواست خرید
              </h3>
              
              <div class="demo-content">
                <div class="demo-field mb-3">
                  <div class="text-caption text-medium-emphasis">عنوان درخواست</div>
                  <div class="text-body-1 font-weight-medium">خرید دستگاه تراش CNC</div>
                </div>
                
                <div class="demo-field mb-3">
                  <div class="text-caption text-medium-emphasis">دسته‌بندی</div>
                  <div class="text-body-1 font-weight-medium">ماشین‌آلات فلزکاری</div>
                </div>
                
                <div class="demo-field mb-3">
                  <div class="text-caption text-medium-emphasis">تعداد</div>
                  <div class="text-body-1 font-weight-medium">۲ دستگاه</div>
                </div>
                
                <div class="demo-field">
                  <div class="text-caption text-medium-emphasis">پیشنهادات دریافتی</div>
                  <div class="text-body-1 font-weight-bold text-success">۸ پیشنهاد</div>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-16 bg-surface-variant">
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
                آماده خرید هستید؟
              </h2>
              
              <p class="text-h6 mb-8 text-white opacity-90">
                همین الان شروع کنید و به بهترین تولیدکنندگان دسترسی پیدا کنید
              </p>
              
              <div class="cta-actions">
                <v-btn
                  size="x-large"
                  color="white"
                  rounded="lg"
                  elevation="4"
                  class="px-8"
                  @click="goToBrowse"
                >
                  <v-icon start>mdi-view-grid</v-icon>
                  مشاهده محصولات
                </v-btn>
                
                <v-btn
                  size="x-large"
                  variant="outlined"
                  color="white"
                  rounded="lg"
                  class="px-8 mr-3"
                  @click="goToRFQ"
                >
                  ثبت درخواست خرید
                  <v-icon end>mdi-file-plus</v-icon>
                </v-btn>
              </div>
              
              <p class="text-body-1 mt-6 text-white opacity-75">
                <v-icon color="white" size="small" class="ml-1">mdi-check-circle</v-icon>
                بدون نیاز به ثبت‌نام برای مشاهده
                <span class="mx-2">•</span>
                <v-icon color="white" size="small" class="ml-1">mdi-check-circle</v-icon>
                پشتیبانی رایگان
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
  title: 'ایندکسو برای خریداران - خرید مطمئن ماشین‌آلات صنعتی',
  meta: [
    {
      name: 'description',
      content: 'دسترسی مستقیم به هزاران تولیدکننده معتبر ماشین‌آلات صنعتی. مقایسه قیمت، خرید مطمئن و ارسال سریع در سراسر کشور'
    },
    {
      property: 'og:title',
      content: 'ایندکسو برای خریداران - خرید مطمئن ماشین‌آلات'
    },
    {
      property: 'og:description',
      content: 'خرید مستقیم از تولیدکننده با بهترین قیمت. مقایسه، انتخاب و خرید آسان ماشین‌آلات صنعتی'
    }
  ]
})

// Refs
const benefitsSection = ref<HTMLElement | null>(null)

// Stats Data
const stats = [
  { number: '+۱۰۰۰', label: 'تولیدکننده' },
  { number: '+۱۵۰۰۰', label: 'محصول' },
  { number: '+۵۰۰۰', label: 'خریدار راضی' },
  { number: '۲۴/۷', label: 'پشتیبانی' }
]

// Benefits Data
const benefits = [
  {
    icon: 'mdi-shield-check',
    title: 'خرید مطمئن و ایمن',
    description: 'تمام تولیدکنندگان احراز هویت شده‌اند و می‌توانید با اطمینان خرید کنید. گارانتی اصالت محصولات.',
    color: 'success',
    featured: true
  },
  {
    icon: 'mdi-cash-multiple',
    title: 'بهترین قیمت بازار',
    description: 'با خرید مستقیم از تولیدکننده، بدون واسطه و با کمترین قیمت، صرفه‌جویی قابل توجهی داشته باشید.',
    color: 'primary',
    featured: false
  },
  {
    icon: 'mdi-compare',
    title: 'مقایسه آسان محصولات',
    description: 'امکان مقایسه قیمت، مشخصات فنی و نظرات سایر خریداران برای انتخاب بهترین گزینه.',
    color: 'info',
    featured: false
  },
  {
    icon: 'mdi-account-group',
    title: 'دسترسی به هزاران تولیدکننده',
    description: 'در یک پلتفرم به بیش از ۱۰۰۰ تولیدکننده معتبر دسترسی داشته باشید و بهترین را انتخاب کنید.',
    color: 'purple',
    featured: false
  },
  {
    icon: 'mdi-headset',
    title: 'مشاوره تخصصی رایگان',
    description: 'تیم کارشناسان ما آماده است تا در انتخاب بهترین محصول و بهترین قیمت به شما مشاوره دهند.',
    color: 'orange',
    featured: false
  },
  {
    icon: 'mdi-truck-fast',
    title: 'ارسال سریع',
    description: 'پیگیری آنلاین سفارش و ارسال سریع به سراسر کشور با بسته‌بندی مطمئن و استاندارد.',
    color: 'teal',
    featured: false
  }
]

// Features Data
const features = [
  {
    icon: 'mdi-magnify',
    title: 'جستجوی هوشمند',
    description: 'سیستم جستجوی پیشرفته برای پیدا کردن دقیق محصول',
    color: 'primary',
    items: [
      'فیلترهای پیشرفته (قیمت، برند، ویژگی‌ها)',
      'جستجوی متنی و تصویری',
      'پیشنهادات هوشمند',
      'ذخیره محصولات مورد علاقه'
    ]
  },
  {
    icon: 'mdi-file-document-edit',
    title: 'درخواست خرید (RFQ)',
    description: 'ثبت درخواست و دریافت پیشنهاد از چندین تولیدکننده',
    color: 'success',
    items: [
      'ثبت درخواست در کمتر از ۲ دقیقه',
      'دریافت پیشنهادات قیمت',
      'مقایسه پیشنهادات',
      'مذاکره مستقیم با تولیدکننده'
    ]
  },
  {
    icon: 'mdi-chat',
    title: 'ارتباط مستقیم',
    description: 'چت آنلاین با تولیدکنندگان',
    color: 'info',
    items: [
      'چت زنده با فروشندگان',
      'پرسش و پاسخ فنی',
      'دریافت کاتالوگ و بروشور',
      'درخواست بازدید از کارخانه'
    ]
  },
  {
    icon: 'mdi-star',
    title: 'نظرات و امتیازدهی',
    description: 'تجربه واقعی خریداران قبلی',
    color: 'warning',
    items: [
      'امتیاز و نظرات تأیید شده',
      'رتبه‌بندی تولیدکنندگان',
      'گزارش تجربه خرید',
      'پرسش و پاسخ محصولات'
    ]
  }
]

// Categories Data
const categories = [
  { title: 'ماشین‌آلات صنعتی', icon: 'mdi-factory', color: 'primary', count: '2500', slug: 'machinery' },
  { title: 'تجهیزات فلزکاری', icon: 'mdi-hammer-wrench', color: 'orange', count: '1800', slug: 'metalworking' },
  { title: 'دستگاه‌های CNC', icon: 'mdi-robot-industrial', color: 'purple', count: '950', slug: 'cnc' },
  { title: 'تجهیزات بسته‌بندی', icon: 'mdi-package-variant', color: 'success', count: '1200', slug: 'packaging' },
  { title: 'پمپ و کمپرسور', icon: 'mdi-pump', color: 'info', count: '890', slug: 'pumps' },
  { title: 'ابزار برقی', icon: 'mdi-lightning-bolt', color: 'warning', count: '1500', slug: 'power-tools' },
  { title: 'تجهیزات جوشکاری', icon: 'mdi-fire', color: 'red', count: '670', slug: 'welding' },
  { title: 'سایر تجهیزات', icon: 'mdi-cog', color: 'grey', count: '3200', slug: 'other' }
]

// Steps Data
const steps = [
  {
    icon: 'mdi-magnify',
    title: 'جستجو کنید',
    description: 'محصول مورد نظر خود را با جستجو یا مرور دسته‌بندی‌ها پیدا کنید.',
    color: 'primary'
  },
  {
    icon: 'mdi-compare',
    title: 'مقایسه و انتخاب',
    description: 'قیمت‌ها، مشخصات و نظرات را مقایسه کنید و بهترین را انتخاب کنید.',
    color: 'info'
  },
  {
    icon: 'mdi-chat',
    title: 'ارتباط با فروشنده',
    description: 'از طریق چت یا تلفن با تولیدکننده در ارتباط باشید و سؤالات خود را بپرسید.',
    color: 'success'
  },
  {
    icon: 'mdi-cart-check',
    title: 'خرید کنید',
    description: 'سفارش خود را ثبت کنید و محصول را با ارسال سریع دریافت کنید.',
    color: 'warning'
  }
]

// Testimonials Data
const testimonials = [
  {
    quote: 'با ایندکسو خیلی راحت تونستم چند تا تولیدکننده رو مقایسه کنم و بهترین قیمت رو پیدا کردم. ۳۰٪ صرفه‌جویی داشتم.',
    name: 'حسین محمدی',
    company: 'کارخانه قطعات خودرو البرز',
    initial: 'ح',
    rating: 5
  },
  {
    quote: 'خیلی سریع محصول مورد نظرم رو پیدا کردم. چت با فروشنده‌ها خیلی راحت بود و همه سؤالاتم جواب داده شد.',
    name: 'فاطمه رضایی',
    company: 'شرکت بسته‌بندی پارسیان',
    initial: 'ف',
    rating: 5
  },
  {
    quote: 'اولین باری بود که آنلاین ماشین‌آلات خریدم. خیلی ساده و مطمئن بود. حتماً دوباره خرید می‌کنم.',
    name: 'رضا کریمی',
    company: 'کارگاه فلزکاری میلاد',
    initial: 'ر',
    rating: 4.5
  }
]

// FAQ Data
const faqs = [
  {
    question: 'آیا برای مشاهده محصولات و قیمت‌ها باید ثبت‌نام کنم؟',
    answer: 'خیر، شما می‌توانید بدون ثبت‌نام تمام محصولات و قیمت‌ها را مشاهده کنید. فقط برای ثبت سفارش یا ارتباط با فروشندگان نیاز به ثبت‌نام دارید.'
  },
  {
    question: 'آیا تولید کنندگان مستقیم محصولات در اینجا حضور دارند یا واسطه؟',
    answer: 'تمام فروشندگان ایندکسو تولیدکنندگان مستقیم یا نمایندگی‌های رسمی معتبر هستند که احراز هویت شده‌اند. شما مستقیم از تولیدکننده خرید می‌کنید.'
  },
  {
    question: 'چگونه می‌توانم از کیفیت محصول اطمینان حاصل کنم؟',
    answer: 'می‌توانید نظرات و امتیازات سایر خریداران را بخوانید، گواهینامه‌ها و مجوزهای تولیدکننده را مشاهده کنید و در صورت نیاز از کارخانه بازدید کنید.'
  },
  {
    question: 'آیا امکان بازگشت کالا وجود دارد؟',
    answer: 'بله، طبق قوانین پلتفرم، در صورت عدم تطابق محصول با توضیحات یا وجود نقص، می‌توانید محصول را مرجوع کنید. شرایط دقیق در صفحه هر محصول ذکر شده است.'
  },
  {
    question: '(برای محصولات کوچک)  چقدر طول می‌کشد تا محصول ارسال شود؟',
    answer: 'زمان ارسال بسته به نوع محصول و موقعیت جغرافیایی متفاوت است. معمولاً محصولات آماده در کمتر از ۷ روز ارسال می‌شوند. محصولات سفارشی ممکن است زمان بیشتری نیاز داشته باشند.'
  }
]

// Methods
const scrollToBenefits = () => {
  benefitsSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const goToBrowse = () => {
  navigateTo('/products')
}

const goToCategories = () => {
  navigateTo('/categories')
}

const goToCategory = (slug: string) => {
  navigateTo(`/categories/${slug}`)
}

const goToRFQ = () => {
  navigateTo('/rfq')
}
</script>

<style scoped>
.for-buyers {
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
  border-color: rgb(var(--v-theme-success));
  background: linear-gradient(135deg, rgba(var(--v-theme-success), 0.05) 0%, transparent 100%);
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

/* Categories Section */
.category-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.category-card:hover {
  transform: translateY(-4px);
  border-color: rgb(var(--v-theme-primary));
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

/* Request Quote Section */
.request-quote-content {
  padding: 20px 0;
}

.rfq-demo-card {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.05) 0%, transparent 100%);
}

.demo-field {
  padding: 12px;
  border-radius: 8px;
  background: rgba(var(--v-theme-on-surface), 0.03);
}

/* CTA Section */
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
  .category-card,
  .testimonial-card {
    margin-bottom: 16px;
  }

  .step-arrow {
    display: none !important;
  }

  .request-quote-content {
    margin-bottom: 30px;
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

