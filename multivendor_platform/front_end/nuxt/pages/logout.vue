<template>
  <v-container class="py-16 text-center">
    <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
    <p class="text-body-1 text-medium-emphasis">در حال خروج از حساب کاربری...</p>
  </v-container>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

await authStore.logout()

const redirect = (route.query.redirect as string) || '/'
router.replace(redirect)
</script>

