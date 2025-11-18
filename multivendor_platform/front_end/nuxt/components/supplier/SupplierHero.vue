<template>
  <div class="supplier-hero" :style="heroStyle">
    <!-- Banner Image with Overlay -->
    <div class="hero-banner">
      <v-img
        v-if="supplier.banner_image"
        :src="formatImageUrl(supplier.banner_image)"
        :height="display.xs.value ? 300 : 400"
        cover
        class="hero-image"
      >
        <template v-slot:placeholder>
          <v-skeleton-loader type="image" />
        </template>
      </v-img>
      <div v-else class="default-banner" :style="{ height: display.xs.value ? '300px' : '400px' }"></div>
      <div class="hero-overlay"></div>
    </div>

    <!-- Hero Content -->
    <v-container class="hero-content">
      <v-row align="center" justify="center">
        <!-- Logo -->
        <v-col cols="12" md="3" class="text-center">
          <v-avatar
            :size="display.xs.value ? 120 : 180"
            class="hero-logo elevation-8"
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
            <v-icon v-else :size="display.xs.value ? 60 : 90" color="white">
              mdi-store
            </v-icon>
          </v-avatar>
        </v-col>

        <!-- Store Info -->
        <v-col cols="12" md="9">
          <div class="store-info">
            <h1 class="store-name text-h3 text-md-h2 font-weight-bold mb-2">
              {{ supplier.store_name }}
            </h1>
            <p v-if="supplier.slogan" class="store-slogan text-h6 text-md-h5 mb-4">
              {{ supplier.slogan }}
            </p>
            <p v-if="supplier.description" class="store-description text-body-1 mb-4">
              {{ supplier.description }}
            </p>

            <!-- Key Metrics -->
            <v-row class="metrics mt-4" dense>
              <v-col cols="6" sm="3" v-if="supplier.year_established">
                <v-card class="metric-card pa-3 text-center" elevation="2">
                  <v-icon color="primary" size="large">mdi-calendar-star</v-icon>
                  <div class="metric-value text-h6 font-weight-bold mt-2">
                    {{ new Date().getFullYear() - supplier.year_established }}
                  </div>
                  <div class="metric-label text-caption">سال تجربه</div>
                </v-card>
              </v-col>
              <v-col cols="6" sm="3" v-if="supplier.employee_count">
                <v-card class="metric-card pa-3 text-center" elevation="2">
                  <v-icon color="primary" size="large">mdi-account-group</v-icon>
                  <div class="metric-value text-h6 font-weight-bold mt-2">
                    {{ supplier.employee_count }}
                  </div>
                  <div class="metric-label text-caption">کارمند</div>
                </v-card>
              </v-col>
              <v-col cols="6" sm="3">
                <v-card class="metric-card pa-3 text-center" elevation="2">
                  <v-icon color="amber" size="large">mdi-star</v-icon>
                  <div class="metric-value text-h6 font-weight-bold mt-2">
                    {{ supplier.rating_average || 0 }}
                  </div>
                  <div class="metric-label text-caption">امتیاز</div>
                </v-card>
              </v-col>
              <v-col cols="6" sm="3">
                <v-card class="metric-card pa-3 text-center" elevation="2">
                  <v-icon color="primary" size="large">mdi-package-variant</v-icon>
                  <div class="metric-value text-h6 font-weight-bold mt-2">
                    {{ supplier.product_count || 0 }}
                  </div>
                  <div class="metric-label text-caption">محصول</div>
                </v-card>
              </v-col>
            </v-row>

            <!-- Action Buttons -->
            <div class="action-buttons mt-6">
              <v-btn
                color="primary"
                size="large"
                prepend-icon="mdi-email"
                @click="$emit('contact-click')"
                class="me-2 mb-2"
              >
                تماس با ما
              </v-btn>
              <v-btn
                v-if="supplier.website"
                color="secondary"
                variant="outlined"
                size="large"
                prepend-icon="mdi-web"
                :href="supplier.website"
                target="_blank"
                class="mb-2"
              >
                وب‌سایت
              </v-btn>
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
</script>

<style scoped>
.supplier-hero {
  position: relative;
  margin-bottom: 2rem;
  --brand-color-primary: rgb(var(--v-theme-primary));
  --brand-color-secondary: rgb(var(--v-theme-secondary));
}

.hero-banner {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.default-banner {
  background: linear-gradient(135deg, var(--brand-color-primary), var(--brand-color-secondary));
  width: 100%;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.6));
}

.hero-content {
  position: relative;
  margin-top: -80px;
  z-index: 10;
}

@media (max-width: 960px) {
  .hero-content {
    margin-top: -60px;
  }
}

.hero-logo {
  border: 4px solid white;
  background-color: white;
}

.store-info {
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.store-name {
  color: white;
  line-height: 1.2;
}

.store-slogan {
  color: rgba(255, 255, 255, 0.95);
  font-style: italic;
}

.store-description {
  color: rgba(255, 255, 255, 0.9);
  max-width: 800px;
}

.metric-card {
  background-color: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
}

.metric-value {
  color: var(--brand-color-primary);
}

.metric-label {
  color: rgba(var(--v-theme-on-surface), 0.7);
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

@media (max-width: 600px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .v-btn {
    width: 100%;
  }
}
</style>

