<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" rounded="lg">
          <v-toolbar color="primary" dark prominent>
            <v-toolbar-title class="text-h5">{{ t('auth.loginToAccount') }}</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pa-6">
            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                :label="t('auth.username')"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                rounded="lg"
                :rules="usernameRules"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                :label="t('auth.password')"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                rounded="lg"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                :rules="passwordRules"
                required
              ></v-text-field>

              <v-alert v-if="error" type="error" variant="tonal" class="mt-3">
                {{ error }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions class="pa-6 pt-0">
            <v-spacer></v-spacer>
            <v-btn 
              color="primary" 
              @click="handleLogin" 
              :loading="loading" 
              :disabled="!valid"
              size="large"
              rounded="lg"
              block
            >
              {{ t('auth.login') }}
            </v-btn>
          </v-card-actions>
          <v-divider></v-divider>
          <v-card-text class="text-center pa-4">
            {{ t('auth.dontHaveAccount') }}
            <router-link to="/register" class="text-primary font-weight-bold">{{ t('auth.registerHere') }}</router-link>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import config from '@/config'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const { t } = useI18n()
    
    const form = ref(null)
    const valid = ref(false)
    const username = ref('')
    const password = ref('')
    const showPassword = ref(false)
    const error = ref('')
    const loading = ref(false)
    
    const usernameRules = [
      v => !!v || t('auth.usernameRequired'),
    ]
    
    const passwordRules = [
      v => !!v || t('auth.passwordRequired'),
    ]
    
    const handleLogin = async () => {
      if (!form.value) return
      
      const { valid: isValid } = await form.value.validate()
      if (!isValid) return
      
      loading.value = true
      error.value = ''
      
      try {
        const response = await authStore.login({
          username: username.value,
          password: password.value
        })
        
        // Redirect based on user role
        if (response.user.is_staff) {
          // Redirect admins/superusers to Django admin panel
          window.location.href = config.djangoAdminUrl
        } else if (response.user.role === 'seller' || response.user.role === 'both') {
          router.push('/seller/dashboard')
        } else {
          router.push('/buyer/dashboard')
        }
      } catch (err) {
        error.value = authStore.error || t('auth.loginFailed')
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      valid,
      username,
      password,
      showPassword,
      error,
      loading,
      usernameRules,
      passwordRules,
      handleLogin,
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

