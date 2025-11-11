<template>
  <v-container fluid class="error-page" dir="rtl">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4" class="text-center">
        <v-card elevation="0" class="pa-8">
          <v-icon
            :size="display.xs.value ? 80 : 120"
            color="error"
            class="mb-4"
          >
            mdi-alert-circle
          </v-icon>
          <h1 class="text-h4 mb-4">خطایی رخ داد</h1>
          <p class="text-body-1 text-medium-emphasis mb-6">
            {{ error.message || 'متأسفانه خطایی در سیستم رخ داده است. لطفاً دوباره تلاش کنید.' }}
          </p>
          <v-row justify="center" class="gap-2">
            <v-btn
              color="primary"
              size="large"
              prepend-icon="mdi-refresh"
              @click="handleError"
            >
              تلاش مجدد
            </v-btn>
            <v-btn
              color="secondary"
              size="large"
              prepend-icon="mdi-home"
              variant="outlined"
              @click="goHome"
            >
              بازگشت به صفحه اصلی
            </v-btn>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'

const props = defineProps<{
  error: {
    statusCode?: number
    statusMessage?: string
    message?: string
  }
}>()

const display = useDisplay()

useHead({
  title: `خطا ${props.error.statusCode || ''}`,
  meta: [
    {
      name: 'description',
      content: props.error.statusMessage || 'خطایی در سیستم رخ داده است'
    },
    {
      name: 'robots',
      content: 'noindex, nofollow'
    }
  ]
})

const handleError = () => {
  clearError({ redirect: '/' })
}

const goHome = () => {
  navigateTo('/')
}
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

