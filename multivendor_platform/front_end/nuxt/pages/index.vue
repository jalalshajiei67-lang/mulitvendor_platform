<template>
  <section class="hero">
    <v-container class="py-12">
      <v-row align="center">
        <v-col cols="12" md="6" class="text-section">
          <h1 class="text-h3 text-md-h2 font-weight-bold mb-4">
            پلتفرم چندفروشنده برای کسب‌وکارهای حرفه‌ای
          </h1>
          <p class="text-body-1 text-medium-emphasis mb-6">
            ایندکسو با ارائه تجربه فارسی، قابلیت‌های سئو محور و زیرساخت B2B به شما کمک می‌کند فروشندگان و خریداران را در یک پلتفرم امن به هم متصل کنید.
          </p>
          <div class="d-flex flex-column flex-sm-row gap-3">
            <v-btn color="primary" size="large">
              شروع خرید
            </v-btn>
            <v-btn color="secondary" variant="outlined" size="large" to="/suppliers">
              ثبت به عنوان تأمین‌کننده
            </v-btn>
          </div>
        </v-col>

        <v-col cols="12" md="6" class="text-center">
          <v-img
            src="/hero-abstract.svg"
            alt="نمایی از داشبورد چندفروشنده"
            max-width="420"
            class="mx-auto hero-image"
          />
        </v-col>
      </v-row>
    </v-container>
  </section>

  <section class="features">
    <v-container class="py-12">
      <v-row>
        <v-col v-for="feature in features" :key="feature.title" cols="12" md="4">
          <v-sheet class="pa-6 feature-card" elevation="1">
            <v-icon size="36" color="primary" class="mb-4">{{ feature.icon }}</v-icon>
            <h2 class="text-h5 font-weight-bold mb-3">{{ feature.title }}</h2>
            <p class="text-body-2 text-medium-emphasis">{{ feature.description }}</p>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  title: 'خانه'
})

useSeoMeta({
  title: 'خانه',
  ogTitle: 'ایندکسو | پلتفرم چندفروشنده',
  description:
    'ایندکسو پلتفرمی برای اتصال خریداران و فروشندگان در بازار B2B است که بر تجربه فارسی و سئو تمرکز دارد.',
  ogDescription:
    'با ایندکسو فروشگاه چندفروشنده خود را بسازید، مدیریت کنید و مشتریان بیشتری جذب کنید.',
  ogImage: '/favicon.ico',
  ogType: 'website'
})

const features = [
  {
    icon: 'mdi-domain',
    title: 'زیرساخت قدرتمند B2B',
    description: 'مدیریت فروشندگان، قراردادها و فرایندهای مالی پیچیده با انعطاف کامل.'
  },
  {
    icon: 'mdi-earth',
    title: 'سئوی پیشرفته',
    description: 'رندر سمت سرور، مدیریت تگ‌های متا و ساختار URL سازگار با موتورهای جستجو.'
  },
  {
    icon: 'mdi-cellphone-link',
    title: 'اول موبایل و RTL',
    description: 'تجربه کاربری فارسی و واکنش‌گرا برای کاربران موبایل و دسکتاپ.'
  }
]
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, rgba(0, 197, 142, 0.12), rgba(0, 111, 82, 0.12));
}

.text-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-image :deep(img) {
  filter: drop-shadow(0 12px 40px rgba(0, 0, 0, 0.08));
}

.features {
  background-color: #ffffff;
}

.feature-card {
  border-radius: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.06);
}

@media (max-width: 960px) {
  .hero {
    text-align: center;
  }

  .text-section {
    align-items: center;
  }
}
</style>

