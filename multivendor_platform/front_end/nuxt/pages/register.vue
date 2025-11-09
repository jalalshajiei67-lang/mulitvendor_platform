<template>
  <v-container fluid class="fill-height auth-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="10" md="7">
        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark prominent>
            <v-toolbar-title class="text-h5">ایجاد حساب کاربری</v-toolbar-title>
          </v-toolbar>

          <v-card-text class="pa-6">
            <v-form ref="formRef" v-model="isValid" @submit.prevent="submit">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.username"
                    label="نام کاربری *"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    rounded="lg"
                    :rules="usernameRules"
                    required
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.email"
                    label="ایمیل *"
                    prepend-inner-icon="mdi-email"
                    variant="outlined"
                    rounded="lg"
                    type="email"
                    :rules="emailRules"
                    required
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.first_name"
                    label="نام"
                    prepend-inner-icon="mdi-account-outline"
                    variant="outlined"
                    rounded="lg"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.last_name"
                    label="نام خانوادگی"
                    prepend-inner-icon="mdi-account-outline"
                    variant="outlined"
                    rounded="lg"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.password"
                    label="رمز عبور *"
                    prepend-inner-icon="mdi-lock"
                    variant="outlined"
                    rounded="lg"
                    :type="showPassword ? 'text' : 'password'"
                    :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append-inner="showPassword = !showPassword"
                    :rules="passwordRules"
                    required
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="confirmPassword"
                    label="تکرار رمز عبور *"
                    prepend-inner-icon="mdi-lock-check"
                    variant="outlined"
                    rounded="lg"
                    :type="showPassword ? 'text' : 'password'"
                    :rules="confirmPasswordRules"
                    required
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.phone"
                    label="شماره تماس"
                    prepend-inner-icon="mdi-phone"
                    variant="outlined"
                    rounded="lg"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="form.role"
                    label="نقش کاربری *"
                    prepend-inner-icon="mdi-account-group"
                    variant="outlined"
                    rounded="lg"
                    :items="roleOptions"
                    item-title="label"
                    item-value="value"
                    :rules="roleRules"
                    required
                  />
                </v-col>
              </v-row>

              <v-text-field
                v-model="form.address"
                label="آدرس"
                prepend-inner-icon="mdi-map-marker"
                variant="outlined"
                rounded="lg"
              />

              <v-expand-transition>
                <div v-if="form.role === 'seller' || form.role === 'both'">
                  <v-divider class="my-4" />
                  <h3 class="text-h6 mb-3">اطلاعات فروشگاه</h3>
                  <v-text-field
                    v-model="form.store_name"
                    label="نام فروشگاه *"
                    prepend-inner-icon="mdi-store"
                    variant="outlined"
                    rounded="lg"
                    :rules="storeNameRules"
                  />
                  <v-textarea
                    v-model="form.store_description"
                    label="توضیحات فروشگاه"
                    prepend-inner-icon="mdi-text"
                    variant="outlined"
                    rounded="lg"
                    rows="3"
                  />
                </div>
              </v-expand-transition>

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
              ثبت‌نام
            </v-btn>
          </v-card-actions>

          <v-divider />

          <v-card-text class="text-center pa-4">
            از قبل حساب دارید؟
            <NuxtLink to="/login" class="text-primary font-weight-bold">ورود</NuxtLink>
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
  title: 'ثبت‌نام | ایندکسو',
  description: 'ایجاد حساب کاربری جدید در ایندکسو برای خرید یا فروش محصولات.',
  ogTitle: 'ثبت‌نام در ایندکسو',
  ogDescription: 'با ثبت‌نام در ایندکسو به امکانات خرید و فروش چندفروشنده دسترسی پیدا کنید.',
  ogType: 'website'
})

const authStore = useAuthStore()
const router = useRouter()

const formRef = ref()
const isValid = ref(false)
const showPassword = ref(false)
const confirmPassword = ref('')
const error = ref<string | null>(null)
const loading = computed(() => authStore.loading)

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  phone: '',
  role: null as string | null,
  address: '',
  store_name: '',
  store_description: ''
})

const roleOptions = [
  { label: 'خریدار', value: 'buyer' },
  { label: 'فروشنده', value: 'seller' },
  { label: 'خریدار و فروشنده', value: 'both' }
]

const usernameRules = [(value: string) => Boolean(value) || 'نام کاربری الزامی است']
const emailRules = [
  (value: string) => Boolean(value) || 'ایمیل الزامی است',
  (value: string) => /.+@.+\..+/.test(value) || 'ایمیل معتبر نیست'
]
const passwordRules = [(value: string) => Boolean(value) || 'رمز عبور الزامی است']
const confirmPasswordRules = [
  (value: string) => Boolean(value) || 'تکرار رمز عبور الزامی است',
  (value: string) => value === form.password || 'رمز عبور مطابقت ندارد'
]
const roleRules = [(value: string) => Boolean(value) || 'انتخاب نقش کاربری الزامی است']
const storeNameRules = [
  (value: string) => (form.role === 'seller' || form.role === 'both' ? Boolean(value) : true) || 'نام فروشگاه الزامی است'
]

const submit = async () => {
  if (!formRef.value) return

  const result = await formRef.value.validate()
  if (!result.valid) return

  error.value = null

  try {
    const payload = { ...form, confirmPassword: undefined }
    const response = await authStore.register(payload)

    if (response?.user?.is_staff || response?.user?.is_superuser) {
      return router.push('/admin/dashboard')
    }
    if (response?.user?.role === 'seller' || response?.user?.role === 'both') {
      return router.push('/seller/dashboard')
    }

    router.push('/buyer/dashboard')
  } catch (err: any) {
    console.error('Registration failed', err)
    error.value =
      authStore.error ??
      err?.data?.error ??
      'خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.'
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
</style>

