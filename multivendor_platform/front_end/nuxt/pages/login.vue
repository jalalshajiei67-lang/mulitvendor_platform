<template>
  <v-container fluid class="fill-height auth-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark prominent>
            <v-toolbar-title class="text-h5">ورود به حساب کاربری</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pa-6">
            <v-form ref="formRef" v-model="isValid" @submit.prevent="submit">
              <v-text-field
                v-model="username"
                label="نام کاربری"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                rounded="lg"
                :rules="usernameRules"
                required
              />

              <v-text-field
                v-model="password"
                label="رمز عبور"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                rounded="lg"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                :rules="passwordRules"
                required
              />

              <v-alert v-if="error" type="error" variant="tonal" class="mt-3">
                {{ error }}
              </v-alert>
            </v-form>
          </v-card-text>

          <v-card-actions class="pa-6 pt-0">
            <v-btn
              color="primary"
              block
              size="large"
              rounded="lg"
              :loading="loading"
              :disabled="!isValid"
              @click="submit"
            >
              ورود
            </v-btn>
          </v-card-actions>

          <v-divider />

          <v-card-text class="text-center pa-4">
            حساب کاربری ندارید؟
            <NuxtLink to="/register" class="text-primary font-weight-bold">ثبت‌نام کنید</NuxtLink>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: [
    function redirectIfAuthenticated() {
      const authStore = useAuthStore()
      if (authStore.isAuthenticated) {
        return navigateTo('/')
      }
    }
  ]
})

useSeoMeta({
  title: 'ورود | ایندکسو',
  description: 'ورود به حساب کاربری ایندکسو برای دسترسی به پنل کاربران و فروشندگان.',
  ogTitle: 'ورود به ایندکسو',
  ogDescription: 'برای مدیریت سفارش‌ها و محصولات وارد حساب کاربری خود شوید.',
  ogType: 'website'
})

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const formRef = ref()
const isValid = ref(false)
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref<string | null>(null)
const loading = computed(() => authStore.loading)

const usernameRules = [(value: string) => Boolean(value) || 'نام کاربری الزامی است']
const passwordRules = [(value: string) => Boolean(value) || 'رمز عبور الزامی است']

const submit = async () => {
  if (!formRef.value) return

  const result = await formRef.value.validate()
  if (!result.valid) return

  error.value = null

  try {
    const response = await authStore.login({
      username: username.value,
      password: password.value
    })

    const redirect = (route.query.redirect as string) || '/'
    if (response?.user?.is_staff || response?.user?.is_superuser) {
      return router.push('/admin/dashboard')
    }
    if (response?.user?.role === 'seller' || response?.user?.role === 'both') {
      return router.push('/seller/dashboard')
    }
    if (response?.user?.role === 'buyer') {
      return router.push(redirect)
    }

    router.push(redirect)
  } catch (err: any) {
    console.error('Login failed', err)
    error.value =
      authStore.error ??
      err?.data?.error ??
      'خطا در ورود. لطفاً اطلاعات خود را بررسی کنید.'
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.auth-container {
  direction: rtl;
  text-align: right;
}

:deep(.v-field__input) {
  text-align: right;
}

:deep(.v-field__append-inner) {
  margin-inline-start: 0;
  margin-inline-end: 8px;
}
</style>

