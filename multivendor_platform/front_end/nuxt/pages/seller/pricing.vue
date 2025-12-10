<template>
  <v-container fluid dir="rtl" class="pa-4 pa-md-8">
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

