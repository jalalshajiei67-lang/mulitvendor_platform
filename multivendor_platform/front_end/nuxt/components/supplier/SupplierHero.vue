<template>
  <div class="supplier-hero" :style="heroStyle">
    <!-- Banner Image with Overlay -->
    <div class="hero-banner">
      <v-img
        v-if="supplier.banner_image"
        :src="formatImageUrl(supplier.banner_image)"
        :height="display.xs.value ? 350 : 450"
        cover
        class="hero-image animate-in"
      >
        <template v-slot:placeholder>
          <v-skeleton-loader type="image" />
        </template>
      </v-img>
      <div v-else class="default-banner animate-in" :style="{ height: display.xs.value ? '350px' : '450px' }"></div>
      <div class="hero-overlay animate-in"></div>

      <!-- Floating Elements -->
      <div class="floating-elements">
        <div class="floating-shape shape-1"></div>
        <div class="floating-shape shape-2"></div>
        <div class="floating-shape shape-3"></div>
      </div>
    </div>

    <!-- Hero Content -->
    <v-container class="hero-content">
      <v-row align="center" justify="center">
        <!-- Logo -->
        <v-col cols="12" md="4" class="text-center logo-section">
          <div class="logo-container animate-in" :class="{ 'animate-delay-1': true }">
            <v-avatar
              :size="display.xs.value ? 140 : 200"
              class="hero-logo elevation-12"
              rounded="lg"
            >
              <v-img
                v-if="supplier.logo"
                :src="formatImageUrl(supplier.logo)"
                cover
              >
                <template v-slot:placeholder>
                  <v-skeleton-loader type="avatar" />
                </template>
              </v-img>
              <v-icon v-else :size="display.xs.value ? 70 : 100" color="white">
                mdi-store
              </v-icon>
            </v-avatar>

            <!-- Trust Indicators -->
            <div class="trust-indicators mt-4">
              <v-chip
                v-if="supplier.is_verified"
                color="success"
                size="small"
                variant="elevated"
                class="me-2 mb-2"
              >
                <v-icon start size="small">mdi-check-decagram</v-icon>
                تایید شده
              </v-chip>
              <v-chip
                v-if="supplier.is_featured"
                color="amber"
                size="small"
                variant="elevated"
                class="mb-2"
              >
                <v-icon start size="small">mdi-star</v-icon>
                ویژه
              </v-chip>
            </div>
          </div>
        </v-col>

        <!-- Store Info -->
        <v-col cols="12" md="8">
          <div class="store-info animate-in animate-delay-2">
            <div class="store-header">
              <h1 class="store-name text-h3 text-md-h1 font-weight-black mb-3">
                {{ supplier.store_name }}
              </h1>
              <div v-if="supplier.slogan" class="slogan-badge">
                <v-chip
                  variant="elevated"
                  size="large"
                  class="slogan-chip"
                >
                  <v-icon start>mdi-lightbulb-on</v-icon>
                  {{ supplier.slogan }}
                </v-chip>
              </div>
            </div>

            <p v-if="supplier.description" class="store-description text-body-1 mb-6">
              {{ supplier.description }}
            </p>

            <!-- Key Metrics -->
            <v-row class="metrics mt-6" dense justify="center" justify-md="start">
              <v-col cols="6" sm="3" v-if="supplier.year_established">
                <v-card class="metric-card metric-card-1 pa-4 pa-md-5 text-center animate-in animate-delay-3" elevation="0" rounded="xl">
                  <div class="metric-icon-container mb-3">
                    <v-icon size="x-large" class="metric-icon">mdi-calendar-star</v-icon>
                  </div>
                  <div class="metric-value text-h4 text-md-h3 font-weight-black">
                    {{ yearsOfExperience }}
                  </div>
                  <div class="metric-label text-caption text-sm-body-2 font-weight-medium">سال تجربه</div>
                </v-card>
              </v-col>
              <v-col cols="6" sm="3" v-if="supplier.employee_count">
                <v-card class="metric-card metric-card-2 pa-4 pa-md-5 text-center animate-in animate-delay-4" elevation="0" rounded="xl">
                  <div class="metric-icon-container mb-3">
                    <v-icon size="x-large" class="metric-icon">mdi-account-group</v-icon>
                  </div>
                  <div class="metric-value text-h4 text-md-h3 font-weight-black">
                    {{ supplier.employee_count }}
                  </div>
                  <div class="metric-label text-caption text-sm-body-2 font-weight-medium">کارمند</div>
                </v-card>
              </v-col>
              <v-col cols="6" sm="3">
                <v-card class="metric-card metric-card-3 pa-4 pa-md-5 text-center animate-in animate-delay-5" elevation="0" rounded="xl">
                  <div class="metric-icon-container mb-3">
                    <v-icon size="x-large" class="metric-icon">mdi-star</v-icon>
                  </div>
                  <div class="metric-value text-h4 text-md-h3 font-weight-black">
                    {{ supplier.rating_average || 0 }}
                  </div>
                  <div class="metric-label text-caption text-sm-body-2 font-weight-medium">امتیاز</div>
                </v-card>
              </v-col>
              <v-col cols="6" sm="3">
                <v-card class="metric-card metric-card-4 pa-4 pa-md-5 text-center animate-in animate-delay-6" elevation="0" rounded="xl">
                  <div class="metric-icon-container mb-3">
                    <v-icon size="x-large" class="metric-icon">mdi-package-variant</v-icon>
                  </div>
                  <div class="metric-value text-h4 text-md-h3 font-weight-black">
                    {{ supplier.product_count || 0 }}
                  </div>
                  <div class="metric-label text-caption text-sm-body-2 font-weight-medium">محصول</div>
                </v-card>
              </v-col>
            </v-row>

            <!-- Enhanced Action Buttons -->
            <div class="action-buttons mt-8 animate-in animate-delay-7">
              <v-btn
                size="x-large"
                prepend-icon="mdi-email"
                @click="$emit('contact-click')"
                class="primary-cta me-3 mb-3 pulse-animation"
                elevation="0"
                rounded="lg"
              >
                <span class="cta-text">تماس با ما</span>
                <v-icon end class="cta-arrow">mdi-chevron-left</v-icon>
              </v-btn>
              <v-btn
                v-if="supplier.website"
                variant="outlined"
                size="x-large"
                prepend-icon="mdi-web"
                :href="supplier.website"
                target="_blank"
                class="secondary-cta mb-3"
                elevation="0"
                rounded="lg"
              >
                بازدید از وب‌سایت
              </v-btn>

              <!-- Social Media Quick Links -->
              <div v-if="supplier.social_media" class="social-quick-links mt-4">
                <span class="social-label text-caption mb-2 d-block">ما را دنبال کنید:</span>
                <div class="social-buttons">
                  <v-btn
                    v-if="supplier.social_media.instagram"
                    icon="mdi-instagram"
                    size="small"
                    variant="text"
                    color="white"
                    :href="supplier.social_media.instagram"
                    target="_blank"
                    class="social-btn"
                  ></v-btn>
                  <v-btn
                    v-if="supplier.social_media.telegram"
                    icon="mdi-telegram"
                    size="small"
                    variant="text"
                    color="white"
                    :href="supplier.social_media.telegram"
                    target="_blank"
                    class="social-btn"
                  ></v-btn>
                  <v-btn
                    v-if="supplier.social_media.whatsapp"
                    icon="mdi-whatsapp"
                    size="small"
                    variant="text"
                    color="white"
                    :href="supplier.social_media.whatsapp"
                    target="_blank"
                    class="social-btn"
                  ></v-btn>
                </div>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import { toJalaali } from 'jalaali-js'
import type { Supplier } from '~/composables/useSupplierApi'
import { formatImageUrl } from '~/utils/imageUtils'

interface Props {
  supplier: Supplier
}

const props = defineProps<Props>()
const display = useDisplay()

defineEmits(['contact-click'])

const heroStyle = computed(() => {
  const styles: any = {}
  
  if (props.supplier.brand_color_primary) {
    styles['--brand-color-primary'] = props.supplier.brand_color_primary
  }
  
  if (props.supplier.brand_color_secondary) {
    styles['--brand-color-secondary'] = props.supplier.brand_color_secondary
  }
  
  return styles
})

// Calculate years of experience based on Hijri/Jalaali calendar
const yearsOfExperience = computed(() => {
  if (!props.supplier.year_established) return 0
  
  // Get current Jalaali (Hijri) year
  const currentJalaali = toJalaali(new Date())
  const currentYear = currentJalaali.jy
  
  // Calculate difference (both are in Jalaali/Hijri calendar)
  const years = currentYear - props.supplier.year_established
  
  return years > 0 ? years : 0
})
</script>

<style scoped>
.supplier-hero {
  position: relative;
  margin-bottom: 3rem;
  --brand-color-primary: rgb(var(--v-theme-primary));
  --brand-color-secondary: rgb(var(--v-theme-secondary));
  overflow: hidden;
}

.hero-banner {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.default-banner {
  background: linear-gradient(135deg, var(--brand-color-primary), var(--brand-color-secondary));
  width: 100%;
  position: relative;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.4) 0%,
    rgba(0, 0, 0, 0.6) 50%,
    rgba(0, 0, 0, 0.8) 100%
  );
}

.hero-content {
  position: relative;
  margin-top: -100px;
  z-index: 10;
  padding: 2rem 0;
}

@media (max-width: 960px) {
  .hero-content {
    margin-top: -80px;
    padding: 1.5rem 0;
  }
}

@media (max-width: 600px) {
  .hero-content {
    margin-top: -60px;
    padding: 1rem 0;
  }
}

/* Floating Elements */
.floating-elements {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 60px;
  height: 60px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* Logo Section */
.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-logo {
  border: 5px solid rgba(255, 255, 255, 0.9);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.hero-logo:hover {
  transform: scale(1.05) rotate(2deg);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
}

/* Trust Indicators */
.trust-indicators {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
}

/* Store Info */
.store-info {
  color: white;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
  text-align: center;
}

@media (min-width: 960px) {
  .store-info {
    text-align: right;
  }
}

.store-header {
  margin-bottom: 1.5rem;
}

.store-name {
  color: white;
  line-height: 1.1;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8);
  margin-bottom: 1rem;
  font-size: 2.5rem !important;
}

@media (max-width: 600px) {
  .store-name {
    font-size: 1.8rem !important;
  }
}

.slogan-badge {
  display: flex;
  justify-content: center;
}

@media (min-width: 960px) {
  .slogan-badge {
    justify-content: flex-start;
  }
}

.slogan-chip {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.15)) !important;
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  font-style: italic;
  font-weight: 600;
  color: white !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.slogan-chip:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.25)) !important;
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.store-description {
  color: rgba(255, 255, 255, 0.95);
  max-width: 700px;
  line-height: 1.6;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
  margin: 0 auto;
}

@media (min-width: 960px) {
  .store-description {
    margin: 0;
  }
}

/* Metrics */
.metrics {
  margin-top: 2rem;
  gap: 12px;
}

.metric-card {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: none !important;
}

/* Gradient backgrounds for each metric card */
.metric-card-1 {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(139, 92, 246, 0.25)) !important;
  backdrop-filter: blur(30px);
  border: 2px solid rgba(99, 102, 241, 0.4) !important;
}

.metric-card-2 {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.25), rgba(219, 39, 119, 0.25)) !important;
  backdrop-filter: blur(30px);
  border: 2px solid rgba(236, 72, 153, 0.4) !important;
}

.metric-card-3 {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.25), rgba(245, 158, 11, 0.25)) !important;
  backdrop-filter: blur(30px);
  border: 2px solid rgba(251, 191, 36, 0.4) !important;
}

.metric-card-4 {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.25), rgba(22, 163, 74, 0.25)) !important;
  backdrop-filter: blur(30px);
  border: 2px solid rgba(34, 197, 94, 0.4) !important;
}

.metric-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: 1;
}

.metric-card::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: 1;
}

.metric-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.metric-card-1:hover {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.4)) !important;
  border-color: rgba(99, 102, 241, 0.6) !important;
}

.metric-card-2:hover {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.4), rgba(219, 39, 119, 0.4)) !important;
  border-color: rgba(236, 72, 153, 0.6) !important;
}

.metric-card-3:hover {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.4), rgba(245, 158, 11, 0.4)) !important;
  border-color: rgba(251, 191, 36, 0.6) !important;
}

.metric-card-4:hover {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.4), rgba(22, 163, 74, 0.4)) !important;
  border-color: rgba(34, 197, 94, 0.6) !important;
}

.metric-card:hover::before,
.metric-card:hover::after {
  opacity: 1;
}

.metric-icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  margin: 0 auto;
  transition: all 0.4s ease;
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.metric-card-1 .metric-icon-container {
  background: rgba(99, 102, 241, 0.3);
  border-color: rgba(99, 102, 241, 0.5);
}

.metric-card-2 .metric-icon-container {
  background: rgba(236, 72, 153, 0.3);
  border-color: rgba(236, 72, 153, 0.5);
}

.metric-card-3 .metric-icon-container {
  background: rgba(251, 191, 36, 0.3);
  border-color: rgba(251, 191, 36, 0.5);
}

.metric-card-4 .metric-icon-container {
  background: rgba(34, 197, 94, 0.3);
  border-color: rgba(34, 197, 94, 0.5);
}

.metric-card:hover .metric-icon-container {
  transform: scale(1.2) rotate(10deg);
  background: rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.6);
}

.metric-icon {
  color: white !important;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.4));
  z-index: 2;
  position: relative;
}

.metric-value {
  color: white;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
  margin-bottom: 0.5rem;
  position: relative;
  z-index: 2;
}

.metric-label {
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  z-index: 2;
  font-size: 0.75rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

@media (min-width: 960px) {
  .action-buttons {
    flex-direction: row;
    align-items: flex-start;
  }
}

.primary-cta {
  background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899) !important;
  background-size: 200% 200% !important;
  border: none !important;
  position: relative;
  overflow: hidden;
  min-width: 200px;
  color: white !important;
  font-weight: 700;
  letter-spacing: 0.5px;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.primary-cta::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), transparent);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: 1;
}

.primary-cta::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
  z-index: 0;
}

.primary-cta:hover::before {
  opacity: 1;
}

.primary-cta:hover::after {
  width: 300px;
  height: 300px;
}

.primary-cta:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(99, 102, 241, 0.6);
  background-position: 100% 0% !important;
}

.primary-cta :deep(.v-btn__content) {
  position: relative;
  z-index: 2;
}

.cta-text {
  font-weight: 700;
  letter-spacing: 0.5px;
  font-size: 1.1rem;
}

.cta-arrow {
  transition: transform 0.3s ease;
}

.primary-cta:hover .cta-arrow {
  transform: translateX(-6px);
}

.secondary-cta {
  background: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.4) !important;
  color: white !important;
  min-width: 180px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.secondary-cta:hover {
  background: rgba(255, 255, 255, 0.25) !important;
  border-color: rgba(255, 255, 255, 0.7) !important;
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}

/* Social Quick Links */
.social-quick-links {
  text-align: center;
}

@media (min-width: 960px) {
  .social-quick-links {
    text-align: right;
  }
}

.social-label {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.social-buttons {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

@media (min-width: 960px) {
  .social-buttons {
    justify-content: flex-start;
  }
}

.social-btn {
  transition: all 0.3s ease;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.social-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

/* Pulse Animation */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.6);
  }
  70% {
    box-shadow: 0 0 0 15px rgba(99, 102, 241, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(99, 102, 241, 0);
  }
}

.pulse-animation {
  animation: pulse 2.5s infinite;
}

/* Animation Classes */
.animate-in {
  opacity: 0;
  transform: translateY(30px);
  animation: slideInUp 0.8s ease-out forwards;
}

.animate-delay-1 {
  animation-delay: 0.1s;
}

.animate-delay-2 {
  animation-delay: 0.2s;
}

.animate-delay-3 {
  animation-delay: 0.3s;
}

.animate-delay-4 {
  animation-delay: 0.4s;
}

.animate-delay-5 {
  animation-delay: 0.5s;
}

.animate-delay-6 {
  animation-delay: 0.6s;
}

.animate-delay-7 {
  animation-delay: 0.7s;
}

@keyframes slideInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Glass Card Utility */
.glass-card {
  background: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .metrics {
    margin-top: 1.5rem;
    gap: 8px;
  }

  .metric-card {
    padding: 1rem !important;
  }

  .metric-icon-container {
    width: 56px;
    height: 56px;
  }

  .metric-icon {
    font-size: 1.5rem !important;
  }

  .metric-value {
    font-size: 1.25rem !important;
  }

  .metric-label {
    font-size: 0.7rem !important;
  }

  .action-buttons {
    width: 100%;
  }

  .primary-cta,
  .secondary-cta {
    width: 100%;
    min-width: unset;
    font-size: 0.95rem !important;
  }

  .cta-text {
    font-size: 1rem !important;
  }

  .social-buttons {
    justify-content: center;
  }

  .slogan-chip {
    font-size: 0.9rem !important;
  }
}
</style>

