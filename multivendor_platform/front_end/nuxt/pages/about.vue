<template>
  <div class="about" dir="rtl">
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h3 text-center mb-8">درباره ما</h1>
          <div class="about-content">
            <p class="text-body-1 mb-4">
              پلتفرم چندفروشنده‌ای ایندکسو با هدف تسهیل ارتباط بین خریداران و فروشندگان ماشین‌آلات صنعتی ایجاد شده است.
            </p>
            <p class="text-body-1 mb-4">
              ما با استفاده از تکنولوژی‌های پیشرفته، بستری امن و کارآمد برای معاملات فراهم کرده‌ایم که هم برای خریداران و هم برای فروشندگان فرصت‌های جدیدی برای رشد و توسعه کسب‌وکارها ایجاد می‌کند.
            </p>
            <p class="text-body-1">
              امروز ایندکسو به عنوان یک محصول تحول‌آفرین در صنعت، راه‌حل‌های جامعی برای ارتباط بهتر، معاملات سریع‌تر و دسترسی آسان‌تر به محصولات و خدمات ارائه می‌دهد.
            </p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'درباره ما',
  meta: [
    {
      name: 'description',
      content: 'آشنایی با ماموریت و چشم‌انداز ایندکسو در تحول خرید و فروش تجهیزات صنعتی.'
    }
  ]
})
</script>

<style scoped>
.about {
  min-height: 100vh;
  padding: 80px 0;
}

.about-content {
  max-width: 900px;
  margin: 0 auto;
  text-align: justify;
  line-height: 2;
}
</style>

