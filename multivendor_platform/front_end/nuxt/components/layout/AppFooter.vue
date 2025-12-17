<template>
  <v-footer color="white" class="app-footer">
    <v-container fluid>
      <v-row class="py-8">
        <v-col cols="12" md="4">
          <div class="text-h6 font-weight-bold mb-2">ایندکسو</div>
          <p class="text-body-2 text-medium-emphasis">
            ایندکسو: خرید و فروش آسان ماشین‌آلات و تجهیزات از بهترین تولیدکنندگان کشور. بدون واسطه و با اطمینان کامل.
          </p>
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <div class="text-subtitle-1 font-weight-bold mb-3">لینک‌های سریع</div>
          <ul class="footer-links">
            <li v-for="link in quickLinks" :key="link.to">
              <NuxtLink :to="link.to">
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <div class="text-subtitle-1 font-weight-bold mb-3">خبرنامه</div>
          <p class="text-body-2 text-medium-emphasis">
            برای دریافت آخرین محصولات و تخفیف‌های ویژه، ایمیل خود را وارد کنید.
          </p>
          <v-text-field
            v-model="newsletter"
            density="comfortable"
            variant="outlined"
            placeholder="ایمیل شما"
            hide-details
            class="mt-3"
            @keyup.enter="submitNewsletter"
          >
            <template #prepend-inner>
              <v-btn
                icon="mdi-send"
                variant="text"
                size="small"
                @click="submitNewsletter"
                class="mr-2"
              />
            </template>
          </v-text-field>
        </v-col>
      </v-row>

      <v-divider />

      <div class="text-center py-4 text-caption text-medium-emphasis">
        © {{ currentYear }} تمامی حقوق این پلتفرم متعلق به ایندکسو است.
      </div>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
const newsletter = ref('')

const quickLinks = [
  { to: '/', label: 'خانه' },
  { to: '/for-buyers', label: 'ایندکسو برای خریداران' },
  { to: '/for-sellers', label: 'ایندکسو برای فروشندگان' },
  { to: '/rfq', label: 'درخواست خرید' },
  { to: '/faqs', label: 'سؤالات متداول' },
  { to: '/terms', label: 'قوانین و مقررات' }
]

const currentYear = new Date().getFullYear()

const submitNewsletter = async () => {
  if (!newsletter.value || !newsletter.value.trim()) {
    return
  }

  try {
    // TODO: Implement newsletter subscription API call
    console.log('Subscribing email:', newsletter.value)
    // Example: await $fetch('/api/newsletter/subscribe', { method: 'POST', body: { email: newsletter.value } })
    
    // Clear input after successful submission
    newsletter.value = ''
    
    // TODO: Show success message (e.g., using snackbar)
  } catch (error) {
    console.error('Newsletter subscription error:', error)
    // TODO: Show error message
  }
}
</script>

<style scoped>
.app-footer {
  border-top: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  background: rgb(var(--v-theme-surface));
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.75rem;
}

.footer-links a {
  color: rgba(var(--v-theme-on-surface), 0.7);
  transition: color 0.2s;
}

.footer-links a:hover {
  color: rgb(var(--v-theme-primary));
}
</style>

