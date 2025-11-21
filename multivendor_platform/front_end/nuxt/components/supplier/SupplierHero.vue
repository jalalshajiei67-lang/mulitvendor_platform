<template>
  <div class="supplier-hero" dir="rtl" :style="heroStyle">
    <!-- Banner -->
    <div class="hero-banner">
      <v-img
        v-if="supplier.banner_image"
        :src="formatImageUrl(supplier.banner_image) || ''"
        :height="display.xs.value ? 260 : 360"
        cover
        class="hero-image"
      >
        <template #placeholder>
          <v-skeleton-loader type="image" />
        </template>
      </v-img>

      <div
        v-else
        class="default-banner"
        :style="{ height: display.xs.value ? '260px' : '360px' }"
      ></div>

      <!-- Dark gradient overlay -->
      <div class="hero-overlay">
        <v-container>
          <div class="hero-content">
            <!-- Logo + Title -->
            <div class="hero-main">
              <div class="hero-logo-wrapper">
                <v-avatar
                  :size="display.xs.value ? 90 : 120"
                  class="hero-logo elevation-6"
                  rounded="lg"
                >
                  <v-img v-if="supplier.logo" :src="supplier.logo" cover>
                    <template #placeholder>
                      <v-skeleton-loader type="avatar" />
                    </template>
                  </v-img>
                  <v-icon v-else :size="display.xs.value ? 48 : 64" color="white">
                    mdi-store
                  </v-icon>
                </v-avatar>
              </div>

              <div class="hero-text">
                <p class="hero-overline">صفحه اختصاصی تامین‌کننده</p>
                <h1 class="store-name">
                  {{ supplier.store_name }}
                </h1>
                <p v-if="supplier.slogan" class="slogan-text">
                  {{ supplier.slogan }}
                </p>

                <!-- Main CTAs -->
                <div class="hero-actions">
                  <v-btn
                    color="primary"
                    size="x-large"
                    class="hero-cta"
                    rounded="xl"
                    elevation="6"
                    @click="$emit('contact-click')"
                  >
                    <v-icon start size="26">mdi-phone</v-icon>
                    <span>تماس با فروشنده</span>
                  </v-btn>

                  <v-btn
                    variant="outlined"
                    color="white"
                    size="large"
                    class="hero-secondary"
                    rounded="xl"
                    @click="$emit('section-click', 'products')"
                  >
                    <v-icon start size="22">mdi-shopping</v-icon>
                    <span>مشاهده محصولات</span>
                  </v-btn>
                </div>
              </div>
            </div>
          </div>
        </v-container>
      </div>
    </div>

    <!-- Navigation -->
    <div class="navigation-container">
      <v-container>
        <!-- Desktop Navigation -->
        <div class="desktop-nav d-none d-md-flex">
          <button
            v-for="section in availableSections"
            :key="section.value"
            class="nav-item"
            :class="{ 'nav-item--active': activeSection === section.value }"
            type="button"
            @click="$emit('section-click', section.value)"
          >
            <v-icon size="24" class="nav-icon">{{ section.icon }}</v-icon>
            <span class="nav-label">{{ section.label }}</span>
          </button>
        </div>

        <!-- Mobile Navigation -->
        <div class="mobile-nav-selector d-md-none">
          <v-select
            :model-value="activeSection"
            :items="mobileNavItems"
            variant="solo"
            density="comfortable"
            class="mobile-nav-select"
            hide-details
            rounded="xl"
            bg-color="white"
            @update:model-value="$emit('section-click', $event)"
          >
            <template #selection="{ item }">
              <div class="d-flex align-center justify-space-between w-100">
                <div class="d-flex align-center">
                  <v-icon :color="item.raw.color" class="ms-3" size="24">
                    {{ item.raw.icon }}
                  </v-icon>
                  <span class="text-subtitle-1 font-weight-medium">
                    {{ item.title }}
                  </span>
                </div>
                <v-icon size="20">mdi-chevron-down</v-icon>
              </div>
            </template>

            <template #item="{ item, props }">
              <v-list-item
                v-bind="props"
                :prepend-icon="item.raw.icon"
                rounded="lg"
                class="text-subtitle-1"
              />
            </template>
          </v-select>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import type { Supplier } from '~/composables/useSupplierApi'
import { formatImageUrl } from '~/utils/imageUtils'

interface Props {
  supplier: Supplier
  availableSections: Array<{ value: string; label: string; icon: string }>
  mobileNavItems: Array<{ title: string; value: string; icon: string; color: string }>
  activeSection: string
}

const props = defineProps<Props>()
const display = useDisplay()

defineEmits(['contact-click', 'section-click'])

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
</script>

<style scoped>
.supplier-hero {
  position: relative;
  margin-bottom: 1.5rem;
  --brand-color-primary: rgb(var(--v-theme-primary));
  --brand-color-secondary: rgb(var(--v-theme-secondary));
  overflow: hidden;
}

/* Banner */
.hero-banner {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.hero-image {
  filter: brightness(0.8);
}

.default-banner {
  background: linear-gradient(
    135deg,
    var(--brand-color-primary),
    var(--brand-color-secondary)
  );
  width: 100%;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(0, 0, 0, 0.4) 0%,
    rgba(0, 0, 0, 0.85) 100%
  );
  display: flex;
  align-items: flex-end;
  padding-bottom: 1.5rem;
}

/* Content */
.hero-content {
  display: flex;
  justify-content: flex-start;
}

.hero-main {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  padding: 1.5rem;
  border-radius: 24px;
  background: rgba(15, 23, 42, 0.9);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.6);
  max-width: 900px;
}

.hero-logo-wrapper {
  flex-shrink: 0;
}

.hero-logo {
  border: 4px solid rgba(255, 255, 255, 0.45);
  background: white;
}

.hero-text {
  color: white;
  text-align: right;
}

.hero-overline {
  font-size: 0.9rem;
  opacity: 0.85;
  margin-bottom: 0.25rem;
}

.store-name {
  color: white;
  margin: 0 0 0.5rem;
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1.4;
}

.slogan-text {
  font-size: 1.1rem;
  font-weight: 500;
  opacity: 0.9;
  margin-bottom: 1.25rem;
}

/* Actions */
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.hero-cta {
  font-size: 1rem;
  font-weight: 700;
  padding-inline: 1.6rem !important;
}

.hero-secondary {
  font-size: 0.95rem;
  border-width: 2px;
}

/* Navigation */
.navigation-container {
  position: sticky;
  top: 0;
  z-index: 20;
  background: white;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.08);
}

.desktop-nav {
  display: flex;
  justify-content: center;
  gap: 0.25rem;
  padding-block: 0.75rem;
}

.nav-item {
  border: none;
  background: transparent;
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.98rem;
  font-weight: 600;
  color: #4b5563;
  transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
}

.nav-item--active {
  background: rgba(var(--v-theme-primary), 0.08);
  color: rgb(var(--v-theme-primary));
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
}

.nav-item:hover {
  background: rgba(15, 23, 42, 0.04);
}

.nav-icon {
  margin-left: 0.25rem;
}

.nav-label {
  white-space: nowrap;
}

/* Mobile */
.mobile-nav-selector {
  padding: 0.75rem 0 0.9rem;
}

.mobile-nav-select :deep(.v-field) {
  min-height: 60px;
  font-size: 1rem;
}

.mobile-nav-select :deep(.v-field__input) {
  padding-inline: 1rem;
}

/* Responsive */
@media (max-width: 960px) {
  .hero-overlay {
    align-items: flex-end;
    padding-bottom: 1.25rem;
  }

  .hero-main {
    flex-direction: column;
    align-items: flex-start;
    max-width: 100%;
    padding: 1.25rem 1.5rem;
  }

  .hero-text {
    text-align: right;
  }

  .store-name {
    font-size: 1.8rem;
  }

  .slogan-text {
    font-size: 1rem;
  }
}

@media (max-width: 600px) {
  .store-name {
    font-size: 1.5rem;
  }

  .hero-main {
    border-radius: 18px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .hero-cta,
  .hero-secondary {
    justify-content: center;
    width: 100%;
  }
}
</style>
