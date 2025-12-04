<template>
  <div class="error-page" dir="rtl">
    <!-- Background Decorative Elements -->
    <div class="background-decoration">
      <div class="decoration-circle decoration-circle-1"></div>
      <div class="decoration-circle decoration-circle-2"></div>
    </div>

    <v-container fluid class="fill-height">
      <v-row justify="center" align="center" class="fill-height">
        <v-col cols="12" sm="10" md="8" lg="6" xl="5">
          <v-card
            elevation="4"
            rounded="xl"
            class="error-card pa-6 pa-sm-8 pa-md-10"
            color="surface"
          >
            <!-- Friendly Icon -->
            <div class="icon-container mb-6">
              <v-icon
                :size="display.xs.value ? 100 : 120"
                color="primary"
                class="friendly-icon"
              >
                mdi-map-marker-off
              </v-icon>
            </div>

            <!-- Main Message -->
            <div class="text-center mb-6">
              <h1 class="error-title text-h4 text-sm-h3 font-weight-bold mb-4">
                متأسفانه این صفحه پیدا نشد
              </h1>
              <p class="error-message text-body-1 text-sm-h6 mb-2">
                به نظر می‌رسد صفحه‌ای که دنبال آن هستید وجود ندارد یا آدرس آن تغییر کرده است.
              </p>
              <p class="error-subtitle text-body-2 text-medium-emphasis">
                نگران نباشید! می‌توانید از طریق دکمه‌های زیر به بخش‌های مختلف سایت دسترسی پیدا کنید.
              </p>
            </div>

            <!-- Helpful Actions -->
            <v-row class="actions-row mb-6" justify="center">
              <v-col cols="12" sm="6" md="6" class="pa-2">
                <v-btn
                  color="primary"
                  size="x-large"
                  block
                  rounded="lg"
                  elevation="2"
                  prepend-icon="mdi-home"
                  class="action-btn font-weight-bold"
                  @click="goHome"
                >
                  <span class="btn-text">بازگشت به صفحه اصلی</span>
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="6" class="pa-2">
                <v-btn
                  color="secondary"
                  size="x-large"
                  block
                  rounded="lg"
                  elevation="2"
                  variant="tonal"
                  prepend-icon="mdi-magnify"
                  class="action-btn font-weight-bold"
                  @click="goToSearch"
                >
                  <span class="btn-text">جستجوی محصولات</span>
                </v-btn>
              </v-col>
            </v-row>

            <!-- Additional Help Options -->
            <v-expansion-panels variant="accordion" class="help-panels mb-6">
              <v-expansion-panel elevation="1" rounded="lg">
                <v-expansion-panel-title class="text-body-1 font-weight-medium">
                  <v-icon class="ml-2" size="24">mdi-lightbulb-on</v-icon>
                  راهنمای بیشتر
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div class="help-content">
                    <p class="text-body-2 mb-3">
                      <strong>چند راهکار مفید:</strong>
                    </p>
                    <ul class="help-list text-body-2">
                      <li>می‌توانید از صفحه اصلی شروع کنید و محصول مورد نظر خود را جستجو کنید</li>
                      <li>یا از طریق دسته‌بندی‌های محصولات، دستگاه مورد نظر خود را پیدا کنید</li>
                      <li>اگر مشکل ادامه دارد، با تیم پشتیبانی ما تماس بگیرید</li>
                    </ul>
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'

const display = useDisplay()

useHead({
  title: 'صفحه مورد نظر یافت نشد - ایندکسو',
  meta: [
    {
      name: 'description',
      content: 'صفحه مورد نظر یافت نشد. می‌توانید از صفحه اصلی یا جستجوی محصولات استفاده کنید.'
    },
    {
      name: 'robots',
      content: 'noindex, nofollow'
    }
  ]
})

const goHome = () => {
  navigateTo('/')
}

const goToSearch = () => {
  navigateTo('/products')
}
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.03) 0%, rgba(var(--v-theme-secondary), 0.03) 100%);
  position: relative;
  overflow: hidden;
  padding: 16px;
}

.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08) 0%, rgba(var(--v-theme-secondary), 0.08) 100%);
  opacity: 0.5;
  animation: float 6s ease-in-out infinite;
}

.decoration-circle-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -150px;
  animation-delay: 0s;
}

.decoration-circle-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -100px;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(20px, 20px) scale(1.1);
  }
}

.error-card {
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.friendly-icon {
  animation: bounce 2s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(var(--v-theme-primary), 0.3));
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.error-title {
  color: rgba(var(--v-theme-on-surface), 0.96);
  line-height: 1.3;
}

.error-message {
  color: rgba(var(--v-theme-on-surface), 0.87);
  line-height: 1.8;
  max-width: 600px;
  margin: 0 auto;
}

.error-subtitle {
  color: rgba(var(--v-theme-on-surface), 0.72);
  line-height: 1.7;
  margin-top: 8px;
}

.actions-row {
  margin-top: 24px;
}

.action-btn {
  min-height: 56px;
  padding: 16px 24px;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(var(--v-theme-primary), 0.3) !important;
}

.btn-text {
  font-size: 1rem;
}

.help-panels {
  margin-top: 24px;
}

.help-content {
  text-align: right;
  padding: 8px;
}

.help-list {
  list-style: none;
  padding-right: 20px;
  line-height: 2;
}

.help-list li {
  position: relative;
  padding-right: 24px;
  margin-bottom: 12px;
}

.help-list li::before {
  content: '✓';
  position: absolute;
  right: 0;
  top: 0;
  color: rgb(var(--v-theme-primary));
  font-weight: bold;
  font-size: 1.2rem;
}

/* Mobile Optimizations */
@media (max-width: 600px) {
  .error-page {
    padding: 8px;
  }

  .error-card {
    padding: 24px 16px !important;
  }

  .action-btn {
    min-height: 52px;
    font-size: 1rem;
  }

  .btn-text {
    font-size: 0.95rem;
  }

  .error-title {
    font-size: 1.5rem !important;
  }

  .error-message {
    font-size: 0.95rem !important;
  }

  .help-list {
    padding-right: 16px;
    line-height: 1.8;
  }

  .help-list li {
    margin-bottom: 8px;
  }
}

/* Tablet Optimizations */
@media (min-width: 600px) and (max-width: 960px) {
  .error-card {
    padding: 40px 32px !important;
  }
}

/* Large Screen Enhancements */
@media (min-width: 1280px) {
  .error-card {
    padding: 64px 48px !important;
  }

  .error-title {
    font-size: 2.5rem !important;
  }

  .error-message {
    font-size: 1.2rem !important;
  }
}

/* Accessibility: Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  .friendly-icon,
  .decoration-circle,
  .error-card {
    animation: none;
  }

  .action-btn:hover {
    transform: none;
  }
}

/* High Contrast Mode Support */
@media (prefers-contrast: high) {
  .error-card {
    border: 2px solid rgba(var(--v-theme-on-surface), 0.3);
  }

  .action-btn {
    border: 2px solid rgba(var(--v-theme-primary), 0.5);
  }
}
</style>

