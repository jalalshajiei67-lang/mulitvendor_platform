<template>
  <v-container fluid class="error-page" dir="rtl">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4" class="text-center">
        <v-card elevation="0" class="pa-8">
          <div class="error-code text-h1 font-weight-bold text-primary mb-4">
            404
          </div>
          <h1 class="text-h4 mb-4">صفحه مورد نظر یافت نشد</h1>
          <p class="text-body-1 text-medium-emphasis mb-6">
            متأسفانه صفحه‌ای که به دنبال آن هستید وجود ندارد یا حذف شده است.
          </p>
          <v-btn
            color="primary"
            size="large"
            prepend-icon="mdi-home"
            @click="goHome"
          >
            بازگشت به صفحه اصلی
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
useHead({
  title: '404 - صفحه یافت نشد',
  meta: [
    {
      name: 'description',
      content: 'صفحه مورد نظر یافت نشد'
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
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-code {
  font-size: 8rem;
  line-height: 1;
  opacity: 0.8;
}

@media (max-width: 600px) {
  .error-code {
    font-size: 5rem;
  }
}
</style>

