<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <div class="text-h4 font-weight-bold mb-6">سؤالات متداول</div>
        
        <v-expansion-panels variant="accordion">
          <v-expansion-panel
            v-for="(faq, index) in faqs"
            :key="index"
          >
            <v-expansion-panel-title>
              {{ faq.question }}
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              {{ faq.answer }}
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
useSeoMeta({
  title: 'سؤالات متداول',
  description: 'پاسخ به سؤالات متداول درباره پلتفرم ایندکسو'
})

const faqs = [
  {
    question: 'چگونه می‌توانم در ایندکسو ثبت‌نام کنم؟',
    answer: 'برای ثبت‌نام در ایندکسو، روی دکمه "ثبت‌نام" در بالای صفحه کلیک کرده و فرم را پر کنید. می‌توانید به عنوان خریدار یا فروشنده ثبت‌نام کنید.'
  },
  {
    question: 'آیا استفاده از پلتفرم رایگان است؟',
    answer: 'بله، ثبت‌نام و مرور محصولات در پلتفرم کاملاً رایگان است. برای فروشندگان، کمیسیون بر اساس فروش محاسبه می‌شود.'
  },
  {
    question: 'چگونه می‌توانم محصول خود را در پلتفرم ثبت کنم؟',
    answer: 'پس از ثبت‌نام به عنوان فروشنده و تأیید حساب کاربری، می‌توانید از پنل فروشنده خود محصولات را اضافه کنید.'
  },
  {
    question: 'روش‌های پرداخت چیست؟',
    answer: 'پلتفرم ایندکسو از درگاه‌های پرداخت معتبر ایرانی پشتیبانی می‌کند و پرداخت‌ها کاملاً امن هستند.'
  },
  {
    question: 'چگونه می‌توانم با پشتیبانی تماس بگیرم؟',
    answer: 'می‌توانید از صفحه "تماس با ما" با پشتیبانی ایندکسو در ارتباط باشید یا ایمیل خود را در فرم ارسال کنید.'
  }
]
</script>

