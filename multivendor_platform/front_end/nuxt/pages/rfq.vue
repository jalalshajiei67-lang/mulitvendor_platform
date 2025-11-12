<template>
  <v-container class="rfq-page">
    <v-row class="page-hero align-center mb-6 mb-md-10" justify="center">
      <v-col cols="12" md="10" lg="8">
        <h1 class="text-h4 text-sm-h3 font-weight-bold mb-4">
          درخواست استعلام قیمت
        </h1>
        <p class="text-body-2 text-sm-body-1 hero-subtitle">
          فرم درخواست استعلام قیمت را تکمیل کنید تا در کوتاه‌ترین زمان با مناسب‌ترین تامین‌کنندگان ارتباط برقرار کنید.
        </p>

        <div class="hero-actions d-flex flex-column flex-sm-row align-stretch mt-6">
          <v-btn
            color="primary"
            size="large"
            class="hero-primary mb-3 mb-sm-0 me-sm-4"
            @click="openForm"
          >
            ارسال درخواست
          </v-btn>
          <v-btn
            variant="tonal"
            color="primary"
            size="large"
            class="hero-secondary"
            @click="scrollToDetails"
          >
            مزایا و مراحل
          </v-btn>
        </div>

        <v-row class="mt-6 hero-highlights" dense>
          <v-col
            v-for="item in heroHighlights"
            :key="item.title"
            cols="12"
            sm="4"
            class="d-flex"
          >
            <v-sheet class="hero-highlight flex-grow-1" color="primary" variant="tonal">
              <div class="text-body-2 text-medium-emphasis mb-1">
                {{ item.title }}
              </div>
              <div class="text-subtitle-1 font-weight-bold">
                {{ item.description }}
              </div>
            </v-sheet>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="12" md="10" lg="9">
        <v-alert
          v-if="successMessage"
          type="success"
          variant="tonal"
          class="mb-4"
          border="start"
          closable
          @click:close="clearSuccess"
        >
          {{ successMessage }}
        </v-alert>

        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          class="mb-4"
          border="start"
          closable
          @click:close="clearError"
        >
          {{ errorMessage }}
        </v-alert>

        <v-card class="rfq-card" elevation="4" rounded="xl">
          <v-card-title class="d-flex align-center justify-space-between pa-4 pa-md-6">
            <div>
              <h2 class="text-h5 text-md-h4 font-weight-bold mb-2">
                اطلاعات موردنیاز برای استعلام دقیق
              </h2>
              <p class="text-body-2 text-medium-emphasis mb-0">
                با چند گام ساده، نیاز خود را با ما در میان بگذارید تا کارشناسان، مناسب‌ترین تامین‌کنندگان را معرفی کنند.
              </p>
            </div>
            <v-avatar size="56" class="d-none d-md-flex card-icon" variant="tonal" color="primary">
              <v-icon>mdi-file-document-edit-outline</v-icon>
            </v-avatar>
          </v-card-title>

          <v-divider />

          <div ref="detailSectionRef">
            <v-card-text class="pa-4 pa-md-6">
              <v-alert
                v-if="loadingProducts"
                variant="tonal"
                type="info"
                class="mb-4"
                icon="mdi-refresh"
              >
                در حال آماده‌سازی فهرست محصولات برای انتخاب شما هستیم...
              </v-alert>

              <v-alert
                v-else-if="products.length === 0"
                variant="tonal"
                type="warning"
                class="mb-4"
                icon="mdi-package-variant"
              >
                در حال حاضر هیچ محصولی برای انتخاب در دسترس نیست. لطفاً بعداً دوباره تلاش کنید یا نیاز خود را در بخش توضیحات فرم بنویسید.
              </v-alert>

              <v-row>
                <v-col
                  v-for="feature in featureCards"
                  :key="feature.title"
                  cols="12"
                  md="6"
                  class="mb-4"
                >
                  <v-sheet class="feature-card h-100" color="primary" variant="tonal">
                    <v-icon size="32" class="mb-4">{{ feature.icon }}</v-icon>
                    <h3 class="text-subtitle-1 font-weight-bold mb-2">
                      {{ feature.title }}
                    </h3>
                    <p class="text-body-2 text-medium-emphasis">
                      {{ feature.description }}
                    </p>
                  </v-sheet>
                </v-col>
              </v-row>
            </v-card-text>

            <v-divider />
          </div>

          <v-card-actions class="pa-4 pa-md-6 justify-end flex-wrap gap-4">
            <div class="text-caption text-medium-emphasis me-auto">
              اطلاعات شما با دقت و محرمانگی بررسی می‌شود.
            </div>
            <v-btn color="primary" size="large" @click="openForm">
              شروع ثبت درخواست
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-12">
      <v-col cols="12" md="10" lg="9">
        <section class="process-section">
          <h2 class="text-h5 text-md-h4 font-weight-bold mb-3">
            مراحل بررسی و پاسخ‌دهی
          </h2>
          <p class="text-body-2 text-medium-emphasis mb-6">
            پس از ارسال فرم، تیم پشتیبانی ما همه جزئیات را بررسی می‌کند و شما را در هر مرحله همراهی خواهد کرد.
          </p>

          <v-row dense>
            <v-col
              v-for="(step, index) in processSteps"
              :key="step.title"
              cols="12"
              md="4"
              class="d-flex"
            >
              <v-card class="process-card flex-grow-1" variant="tonal" color="primary">
                <div class="process-index">
                  {{ index + 1 }}
                </div>
                <h3 class="text-subtitle-1 font-weight-bold mb-2">
                  {{ step.title }}
                </h3>
                <p class="text-body-2 text-medium-emphasis">
                  {{ step.description }}
                </p>
              </v-card>
            </v-col>
          </v-row>
        </section>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-12">
      <v-col cols="12" md="10" lg="9">
        <section class="support-section">
          <h2 class="text-h5 text-md-h4 font-weight-bold mb-3">
            راه‌های ارتباطی تیم پشتیبانی
          </h2>
          <p class="text-body-2 text-medium-emphasis mb-6">
            اگر پیش از ارسال فرم نیاز به راهنمایی دارید، از طریق یکی از روش‌های زیر با ما در ارتباط باشید.
          </p>

          <v-row dense>
            <v-col
              v-for="support in supportOptions"
              :key="support.title"
              cols="12"
              md="4"
            >
              <v-card class="support-card" variant="tonal" :color="support.color">
                <v-icon size="32" class="mb-3">{{ support.icon }}</v-icon>
                <h3 class="text-subtitle-1 font-weight-bold mb-2">
                  {{ support.title }}
                </h3>
                <p class="text-body-2">
                  {{ support.description }}
                </p>
                <span class="text-caption text-medium-emphasis">
                  {{ support.subtitle }}
                </span>
              </v-card>
            </v-col>
          </v-row>
        </section>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-12 mb-16">
      <v-col cols="12" md="10" lg="9">
        <section class="faq-section">
          <h2 class="text-h5 text-md-h4 font-weight-bold mb-3">
            پرسش‌های متداول
          </h2>
          <p class="text-body-2 text-medium-emphasis mb-6">
            پاسخ سریع به سوالاتی که معمولاً پیش از ارسال درخواست استعلام مطرح می‌شوند.
          </p>

          <v-expansion-panels variant="accordion">
            <v-expansion-panel
              v-for="faq in faqs"
              :key="faq.question"
            >
              <v-expansion-panel-title class="faq-title">
                {{ faq.question }}
              </v-expansion-panel-title>
              <v-expansion-panel-text class="faq-text">
                {{ faq.answer }}
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </section>
      </v-col>
    </v-row>

    <RFQForm
      v-model="showForm"
      :products="products"
      @submitted="handleRFQSubmitted"
      @error="handleRFQError"
    />
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useProductApi } from '~/composables/useProductApi'

interface ProductOption {
  id: number
  name: string
}

const showForm = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const loadingProducts = ref(false)
const products = ref<ProductOption[]>([])
const detailSectionRef = ref<HTMLElement | null>(null)

const heroHighlights = [
  {
    title: 'تامین‌کنندگان فعال',
    description: 'بیش از ۱۲۰ شریک تجاری تاییدشده'
  },
  {
    title: 'پاسخ‌گویی سریع',
    description: 'میانگین پاسخ کمتر از ۲۴ ساعت'
  },
  {
    title: 'پوشش کشوری',
    description: 'سرویس‌دهی در سراسر ایران'
  }
]

const featureCards = [
  {
    icon: 'mdi-account-tie-voice',
    title: 'کارشناسان تخصصی هر حوزه',
    description: 'درخواست شما به کارشناس همان گروه محصول ارجاع می‌شود تا با شناخت کامل بازار پاسخ دقیق ارائه شود.'
  },
  {
    icon: 'mdi-shield-check',
    title: 'تامین‌کنندگان تأییدشده',
    description: 'همه تامین‌کنندگان پس از ارزیابی کیفی و بررسی سوابق همکاری، در پلتفرم فعال شده‌اند.'
  },
  {
    icon: 'mdi-tray-arrow-up',
    title: 'آپلود مستندات فنی',
    description: 'می‌توانید نقشه‌ها، تصاویر یا فایل‌های مرتبط را ضمیمه کنید تا پیشنهاد دقیق‌تری دریافت نمایید.'
  },
  {
    icon: 'mdi-account-clock',
    title: 'پیگیری لحظه‌ای وضعیت',
    description: 'پس از ارسال درخواست، اطلاع‌رسانی وضعیت از طریق پیامک و داشبورد کاربری انجام می‌شود.'
  }
]

const processSteps = [
  {
    title: 'ارسال فرم استعلام',
    description: 'فرم را تکمیل و نیازهای خود را توضیح دهید تا درخواست شما ثبت شود.'
  },
  {
    title: 'هماهنگی با کارشناس',
    description: 'کارشناس مربوطه ظرف کمتر از یک روز کاری با شما تماس می‌گیرد و جزئیات را نهایی می‌کند.'
  },
  {
    title: 'معرفی تامین‌کنندگان منتخب',
    description: 'پس از جمع‌آوری پیشنهادها، بهترین گزینه‌ها همراه با شرایط همکاری برای شما ارسال می‌شوند.'
  }
]

const supportOptions = [
  {
    icon: 'mdi-phone-in-talk',
    title: 'تماس تلفنی',
    description: 'شماره ۰۲۱-۹۱۰۱۲۳۴۵ برای پاسخ‌گویی در ساعات اداری',
    subtitle: 'پشتیبانی تلفنی',
    color: 'primary'
  },
  {
    icon: 'mdi-message-text',
    title: 'گفت‌وگوی آنلاین',
    description: 'از طریق بخش چت آنلاین در پایین صفحه با ما صحبت کنید.',
    subtitle: 'چت آنلاین ۷×۲۴',
    color: 'secondary'
  },
  {
    icon: 'mdi-email-fast',
    title: 'ارسال ایمیل',
    description: 'ایمیل خود را به آدرس rfq@indexo.ir بفرستید تا در اولین فرصت پاسخ دهیم.',
    subtitle: 'پاسخ‌گویی کمتر از یک روز کاری',
    color: 'accent'
  }
]

const faqs = [
  {
    question: 'برای ارسال درخواست استعلام چه اطلاعاتی لازم است؟',
    answer: 'نام و نام خانوادگی، نام شرکت، شماره تماس، محصول مورد نظر و توضیح دقیق نیازها برای پردازش درخواست کافی است.'
  },
  {
    question: 'پس از ثبت درخواست چه مدت طول می‌کشد تا پاسخ دریافت کنم؟',
    answer: 'به طور میانگین ظرف کمتر از ۲۴ ساعت کاری با شما تماس گرفته می‌شود و فرآیند معرفی تامین‌کننده آغاز خواهد شد.'
  },
  {
    question: 'آیا ارسال درخواست هزینه دارد؟',
    answer: 'خیر، ثبت درخواست استعلام قیمت در پلتفرم ما کاملاً رایگان است و تنها پس از عقد قرارداد هزینه خدمات دریافت می‌شود.'
  },
  {
    question: 'آیا می‌توانم چند محصول را در یک فرم درخواست کنم؟',
    answer: 'بله، کافی است در بخش توضیحات نیازهای خود را به تفکیک بنویسید یا فایل مشخصات محصولات را بارگذاری کنید.'
  }
]

const productApi = useProductApi()

const loadProducts = async () => {
  loadingProducts.value = true
  try {
    const response = await productApi.getProducts({ page_size: 100, ordering: '-created_at' })
    const items = Array.isArray(response?.results) ? response.results : []
    products.value = items
      .filter((product: any) => product?.id && (product?.title || product?.name))
      .map((product: any) => ({
        id: Number(product.id),
        name: product.title ?? product.name ?? `محصول ${product.id}`
      }))
  } catch (error) {
    console.error('RFQ: failed to load products', error)
    errorMessage.value = 'خطا در بارگذاری فهرست محصولات. لطفاً بعداً دوباره تلاش کنید.'
  } finally {
    loadingProducts.value = false
  }
}

const openForm = () => {
  errorMessage.value = ''
  successMessage.value = ''
  showForm.value = true
}

const scrollToDetails = () => {
  if (detailSectionRef.value) {
    detailSectionRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const handleRFQSubmitted = () => {
  successMessage.value = 'درخواست شما با موفقیت ثبت شد. همکاران ما به‌زودی با شما تماس خواهند گرفت.'
  errorMessage.value = ''
  showForm.value = false
}

const handleRFQError = (message: string) => {
  errorMessage.value = message || 'خطا در ثبت درخواست. لطفاً دوباره تلاش کنید.'
  successMessage.value = ''
}

const clearSuccess = () => {
  successMessage.value = ''
}

const clearError = () => {
  errorMessage.value = ''
}

onMounted(() => {
  loadProducts()
})

useSeoMeta({
  title: 'درخواست قیمت (RFQ)',
  description: 'فرم درخواست قیمت برای محصولات مورد نظر خود را پر کنید'
})
</script>

<style scoped>
.rfq-page {
  min-height: 100vh;
  padding: 64px 16px 80px;
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.page-hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.22), rgba(var(--v-theme-secondary), 0.28));
  border-radius: 24px;
  padding: 48px 32px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
  margin: 0 auto 40px;
  max-width: 1100px;
}

.page-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.24), transparent 60%);
  pointer-events: none;
}

.page-hero h1,
.page-hero p {
  color: rgba(var(--v-theme-on-primary), 0.95);
}

.hero-subtitle {
  max-width: 620px;
  line-height: 1.9;
}

.hero-actions {
  gap: 16px;
}

.hero-primary,
.hero-secondary {
  min-width: 180px;
  font-weight: 600;
}

.hero-highlights {
  margin-top: 32px;
}

.hero-highlight {
  padding: 20px;
  border-radius: 18px;
  background: rgba(var(--v-theme-surface), 0.08);
  backdrop-filter: blur(6px);
  box-shadow: 0 12px 24px rgba(var(--v-theme-on-surface), 0.12);
}

.rfq-card {
  background: rgb(var(--v-theme-surface));
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.08);
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
}

.card-icon :deep(.v-icon) {
  color: rgb(var(--v-theme-primary));
}

.feature-card {
  padding: 24px;
  border-radius: 22px;
  background-color: rgba(var(--v-theme-surface), 0.75);
  backdrop-filter: blur(6px);
  box-shadow: 0 16px 32px rgba(var(--v-theme-on-surface), 0.08);
}

.feature-card :deep(.v-icon) {
  color: rgb(var(--v-theme-primary));
}

.process-section {
  background: rgb(var(--v-theme-surface));
  border-radius: 24px;
  padding: 40px 32px;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.06);
  border: 1px solid rgba(var(--v-theme-primary), 0.06);
}

.process-card {
  padding: 28px 24px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: rgba(var(--v-theme-surface), 0.75);
  backdrop-filter: blur(6px);
}

.process-index {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.125rem;
  color: rgb(var(--v-theme-primary));
  background-color: rgba(var(--v-theme-primary), 0.15);
}

.support-card {
  height: 100%;
  padding: 28px 24px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: rgba(var(--v-theme-surface), 0.85);
  box-shadow: 0 16px 32px rgba(var(--v-theme-on-surface), 0.08);
}

.support-card :deep(.v-icon) {
  color: rgb(var(--v-theme-on-primary));
}

.faq-section {
  background: rgb(var(--v-theme-surface));
  border-radius: 24px;
  padding: 40px 32px;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.06);
  border: 1px solid rgba(var(--v-theme-primary), 0.06);
}

.faq-title {
  font-weight: 600;
  color: rgba(var(--v-theme-on-surface), 0.9);
}

.faq-text {
  line-height: 1.9;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

@media (max-width: 1280px) {
  .page-hero {
    padding: 40px 28px;
  }
}

@media (max-width: 960px) {
  .page-hero {
    padding: 32px 20px;
    text-align: center;
  }

  .hero-actions {
    align-items: stretch;
  }

  .hero-highlights {
    margin-top: 24px;
  }

  .rfq-page {
    padding: 48px 12px 64px;
  }

  .rfq-card {
    border-radius: 20px;
  }

  .process-section,
  .faq-section {
    padding: 32px 20px;
  }
}

@media (max-width: 600px) {
  .hero-primary,
  .hero-secondary {
    width: 100%;
  }

  .feature-card,
  .process-card,
  .support-card {
    padding: 20px;
  }
}
</style>

