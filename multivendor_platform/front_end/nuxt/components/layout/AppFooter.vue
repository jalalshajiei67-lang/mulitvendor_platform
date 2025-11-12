<template>
  <v-footer color="white" class="app-footer">
    <v-container fluid>
      <v-row class="py-8">
        <v-col cols="12" md="4">
          <div class="text-h6 font-weight-bold mb-2">ایندکسو</div>
          <p class="text-body-2 text-medium-emphasis">
            پلتفرم جامع خرید و فروش B2B با تمرکز بر تجربه کاربری فارسی، چندفروشندگی و سئوی پیشرفته.
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
            برای دریافت جدیدترین محصولات و تخفیف‌ها ایمیل خود را وارد کنید.
          </p>
          <v-text-field
            v-model="newsletter"
            density="comfortable"
            variant="outlined"
            placeholder="ایمیل شما"
            append-inner-icon="mdi-send"
            hide-details
            class="mt-3"
          />
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
  { to: '/rfq', label: 'درخواست خرید' },
  { to: '/faqs', label: 'سؤالات متداول' },
  { to: '/terms', label: 'قوانین و مقررات' }
]

const currentYear = new Date().getFullYear()
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

