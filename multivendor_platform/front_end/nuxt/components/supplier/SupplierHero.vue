<template>
  <div class="supplier-hero" :style="heroStyle">
    <!-- Banner Image with Overlay -->
    <div class="hero-banner">
      <v-img
        v-if="supplier.banner_image"
        :src="formatImageUrl(supplier.banner_image) || ''"
        :height="display.xs.value ? 300 : 400"
        cover
        class="hero-image"
      >
        <template v-slot:placeholder>
          <v-skeleton-loader type="image" />
        </template>
      </v-img>
      <div v-else class="default-banner" :style="{ height: display.xs.value ? '300px' : '400px' }"></div>
      <div class="hero-overlay">
        <!-- Store Header in Center of Overlay -->
        <div class="overlay-store-header">
          <h1 class="store-name">
            {{ supplier.store_name }}
          </h1>
          <div v-if="supplier.slogan" class="slogan-text">
            {{ supplier.slogan }}
          </div>
        </div>
      </div>
    </div>

    <!-- Simplified Navigation Bar -->
    <div class="navigation-container">
      <v-container>
        <!-- Desktop Navigation -->
        <div class="desktop-nav d-none d-md-flex">
          <v-btn
            v-for="section in availableSections"
            :key="section.value"
            :variant="activeSection === section.value ? 'flat' : 'text'"
            :color="activeSection === section.value ? 'primary' : 'grey-darken-2'"
            size="large"
            class="nav-btn px-6"
            rounded="lg"
            @click="$emit('section-click', section.value)"
          >
            <v-icon start size="28">{{ section.icon }}</v-icon>
            <span class="text-h6">{{ section.label }}</span>
          </v-btn>
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
            <template v-slot:selection="{ item }">
              <div class="d-flex align-center">
                <v-icon :color="item.raw.color" class="me-3" size="28">{{ item.raw.icon }}</v-icon>
                <span class="text-h6 font-weight-medium">{{ item.title }}</span>
              </div>
            </template>
            <template v-slot:item="{ item, props }">
              <v-list-item 
                v-bind="props"
                :prepend-icon="item.raw.icon"
                rounded="lg"
                class="text-h6"
              >
              </v-list-item>
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
  margin-bottom: 2rem;
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
    to bottom,
    rgba(0, 0, 0, 0.5) 0%,
    rgba(0, 0, 0, 0.7) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

/* Store Header in Overlay */
.overlay-store-header {
  text-align: center;
  padding: 3rem 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.overlay-store-header .store-name {
  color: white;
  line-height: 1.3;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
  margin-bottom: 1rem;
  font-size: 3.5rem;
  font-weight: 800;
}

@media (max-width: 960px) {
  .overlay-store-header .store-name {
    font-size: 2.5rem;
  }
}

@media (max-width: 600px) {
  .overlay-store-header .store-name {
    font-size: 2rem;
  }
}

.slogan-text {
  color: white;
  font-size: 1.5rem;
  font-weight: 500;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.8);
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  display: inline-block;
}

@media (max-width: 600px) {
  .slogan-text {
    font-size: 1.1rem;
  }
}


/* Navigation Styles */
.navigation-container {
  position: relative;
  z-index: 10;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.desktop-nav {
  width: 100%;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.nav-btn {
  font-size: 1.125rem !important;
  padding: 1rem 2rem !important;
  min-height: 56px;
  font-weight: 600 !important;
  letter-spacing: 0.5px;
}

/* Mobile Navigation */
.mobile-nav-selector {
  padding: 1.5rem;
}

.mobile-nav-select {
  font-size: 1.125rem;
}

.mobile-nav-select :deep(.v-field) {
  min-height: 64px;
  font-size: 1.125rem;
}

.mobile-nav-select :deep(.v-field__input) {
  padding: 1rem;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .slogan-text {
    font-size: 1rem;
    padding: 0.5rem 0.75rem;
  }
  
  .nav-btn {
    font-size: 1rem !important;
    min-height: 48px;
  }
}
</style>

