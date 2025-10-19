<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="10" md="6">
        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark prominent>
            <v-toolbar-title class="text-h5">{{ t('auth.createAccount') }}</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pa-6">
            <v-form ref="form" v-model="valid" @submit.prevent="handleRegister">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.username"
                    :label="t('auth.username') + ' *'"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    rounded="lg"
                    :rules="usernameRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.email"
                    :label="t('auth.email') + ' *'"
                    prepend-inner-icon="mdi-email"
                    variant="outlined"
                    rounded="lg"
                    type="email"
                    :rules="emailRules"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.first_name"
                    :label="t('auth.firstName')"
                    prepend-inner-icon="mdi-account-outline"
                    variant="outlined"
                    rounded="lg"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.last_name"
                    :label="t('auth.lastName')"
                    prepend-inner-icon="mdi-account-outline"
                    variant="outlined"
                    rounded="lg"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.password"
                    :label="t('auth.password') + ' *'"
                    prepend-inner-icon="mdi-lock"
                    variant="outlined"
                    rounded="lg"
                    :type="showPassword ? 'text' : 'password'"
                    :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append-inner="showPassword = !showPassword"
                    :rules="passwordRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="confirmPassword"
                    :label="t('auth.confirmPassword') + ' *'"
                    prepend-inner-icon="mdi-lock-check"
                    variant="outlined"
                    rounded="lg"
                    :type="showPassword ? 'text' : 'password'"
                    :rules="confirmPasswordRules"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="formData.phone"
                    :label="t('auth.phoneNumber')"
                    prepend-inner-icon="mdi-phone"
                    variant="outlined"
                    rounded="lg"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="formData.role"
                    :label="t('auth.selectRole') + ' *'"
                    prepend-inner-icon="mdi-account-group"
                    variant="outlined"
                    rounded="lg"
                    :items="roleOptions"
                    item-title="text"
                    item-value="value"
                    :rules="roleRules"
                    required
                  ></v-select>
                </v-col>
              </v-row>

              <v-text-field
                v-model="formData.address"
                label="آدرس"
                prepend-inner-icon="mdi-map-marker"
                variant="outlined"
                rounded="lg"
              ></v-text-field>

              <!-- Seller-specific fields -->
              <v-expand-transition>
                <div v-if="formData.role === 'seller' || formData.role === 'both'">
                  <v-divider class="my-4"></v-divider>
                  <h3 class="text-h6 mb-3">اطلاعات فروشگاه</h3>
                  <v-text-field
                    v-model="formData.store_name"
                    label="نام فروشگاه *"
                    prepend-inner-icon="mdi-store"
                    variant="outlined"
                    rounded="lg"
                    :rules="storeNameRules"
                  ></v-text-field>
                  <v-textarea
                    v-model="formData.store_description"
                    label="توضیحات فروشگاه"
                    prepend-inner-icon="mdi-text"
                    variant="outlined"
                    rounded="lg"
                    rows="3"
                  ></v-textarea>
                </div>
              </v-expand-transition>

              <v-alert v-if="error" type="error" variant="tonal" class="mt-3">
                {{ error }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions class="pa-6 pt-0">
            <v-spacer></v-spacer>
            <v-btn 
              color="primary" 
              @click="handleRegister" 
              :loading="loading" 
              :disabled="!valid"
              size="large"
              rounded="lg"
              block
            >
              {{ t('auth.register') }}
            </v-btn>
          </v-card-actions>
          <v-divider></v-divider>
          <v-card-text class="text-center pa-4">
            {{ t('auth.alreadyHaveAccount') }}
            <router-link to="/login" class="text-primary font-weight-bold">{{ t('auth.loginHere') }}</router-link>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const { t } = useI18n()
    
    const form = ref(null)
    const valid = ref(false)
    const showPassword = ref(false)
    const confirmPassword = ref('')
    const error = ref('')
    const loading = ref(false)
    
    const formData = ref({
      username: '',
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      role: 'buyer',
      phone: '',
      address: '',
      store_name: '',
      store_description: ''
    })
    
    const roleOptions = [
      { text: t('auth.buyer'), value: 'buyer' },
      { text: t('auth.seller'), value: 'seller' },
      { text: t('auth.both'), value: 'both' }
    ]
    
    const usernameRules = [
      v => !!v || t('auth.usernameRequired'),
      v => v.length >= 3 || 'نام کاربری باید حداقل 3 کاراکتر باشد'
    ]
    
    const emailRules = [
      v => !!v || t('auth.emailRequired'),
      v => /.+@.+\..+/.test(v) || t('auth.invalidEmail')
    ]
    
    const passwordRules = [
      v => !!v || t('auth.passwordRequired'),
      v => v.length >= 6 || 'رمز عبور باید حداقل 6 کاراکتر باشد'
    ]
    
    const confirmPasswordRules = [
      v => !!v || 'لطفاً رمز عبور خود را تایید کنید',
      v => v === formData.value.password || t('auth.passwordMismatch')
    ]
    
    const roleRules = [
      v => !!v || 'لطفاً یک نقش انتخاب کنید'
    ]
    
    const storeNameRules = computed(() => {
      if (formData.value.role === 'seller' || formData.value.role === 'both') {
        return [v => !!v || 'نام فروشگاه برای فروشندگان الزامی است']
      }
      return []
    })
    
    const handleRegister = async () => {
      if (!form.value) return
      
      const { valid: isValid } = await form.value.validate()
      if (!isValid) return
      
      loading.value = true
      error.value = ''
      
      try {
        const response = await authStore.register(formData.value)
        
        // Redirect based on user role
        if (response.user.role === 'seller' || response.user.role === 'both') {
          router.push('/seller/dashboard')
        } else {
          router.push('/buyer/dashboard')
        }
      } catch (err) {
        if (err.response?.data) {
          // Handle validation errors
          const errors = err.response.data
          if (typeof errors === 'object') {
            error.value = Object.values(errors).flat().join(', ')
          } else {
            error.value = authStore.error || t('auth.registerFailed')
          }
        } else {
          error.value = authStore.error || t('auth.registerFailed')
        }
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      valid,
      formData,
      confirmPassword,
      showPassword,
      error,
      loading,
      roleOptions,
      usernameRules,
      emailRules,
      passwordRules,
      confirmPasswordRules,
      roleRules,
      storeNameRules,
      handleRegister,
      t
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>

