<template>
  <div class="about" dir="rtl">
    <section class="hero">
      <v-container class="py-10 text-center text-white">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-3">درباره ایندکسو</h1>
        <p class="text-subtitle-1 opacity-90 mx-auto max-w-720">
          داستان تحول‌آفرین ما در اتصال خریداران و فروشندگان ماشین‌آلات صنعتی.
        </p>
      </v-container>
    </section>

    <v-container class="py-10">
      <v-row justify="center">
        <v-col cols="12" md="10" lg="8">
          <v-card class="about-card" elevation="2" rounded="xl">
            <v-card-text class="pa-8 pa-md-10">
              <p class="text-body-1 mb-6">
                پلتفرم چندفروشنده‌ای ایندکسو با هدف تسهیل ارتباط بین خریداران و فروشندگان ماشین‌آلات صنعتی ایجاد شده است.
              </p>
              <p class="text-body-1 mb-6">
                ما با استفاده از تکنولوژی‌های پیشرفته، بستری امن و کارآمد برای معاملات فراهم کرده‌ایم که هم برای خریداران و هم برای فروشندگان فرصت‌های جدیدی برای رشد و توسعه کسب‌وکارها ایجاد می‌کند.
              </p>
              <p class="text-body-1">
                امروز ایندکسو به عنوان یک محصول تحول‌آفرین در صنعت، راه‌حل‌های جامعی برای ارتباط بهتر، معاملات سریع‌تر و دسترسی آسان‌تر به محصولات و خدمات ارائه می‌دهد.
              </p>
            </v-card-text>
          </v-card>
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
  background-color: rgba(var(--v-theme-surface), 0.97);
  color: rgba(var(--v-theme-on-surface), 0.92);
}

.hero {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.22), rgba(var(--v-theme-secondary), 0.26));
  border-radius: 24px;
  margin: 16px auto 36px;
  max-width: 1440px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(var(--v-theme-on-surface), 0.12);
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(var(--v-theme-surface), 0.28), transparent 60%);
  pointer-events: none;
}

.max-w-720 {
  max-width: 720px;
}

.about-card {
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-theme-primary), 0.08);
}
</style>

