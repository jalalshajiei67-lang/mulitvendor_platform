<template>
  <v-container fluid dir="rtl" class="pricing-page pa-4 pa-md-8">
    <PricingPlans />
  </v-container>
</template>

<script setup lang="ts">
import PricingPlans from '~/components/seller/PricingPlans.vue'

definePageMeta({
  middleware: 'authenticated',
  layout: 'dashboard'
})
</script>

<style scoped>
.pricing-page {
  padding-top: 140px !important;
}

@media (max-width: 960px) {
  .pricing-page {
    padding-top: 120px !important;
  }
}

@media (max-width: 600px) {
  .pricing-page {
    padding-top: 112px !important;
  }
}
</style>

