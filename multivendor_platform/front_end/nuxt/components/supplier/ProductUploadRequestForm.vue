<template>
  <div dir="rtl" class="product-upload-request-form">
    <v-card elevation="2" class="pa-6">
      <v-card-title class="text-h6 mb-4 d-flex align-center">
        <v-icon class="ml-2" color="primary">mdi-upload</v-icon>
        درخواست بارگذاری محصول
      </v-card-title>

      <v-card-text>
        <v-alert
          type="info"
          variant="tonal"
          color="primary"
          class="mb-6"
          border="start"
          elevation="0"
        >
          <div class="font-weight-bold mb-2">۳ محصول رایگان برای شما!</div>
          <div class="text-body-2">
            با ارسال درخواست، تیم ما ۳ محصول را به صورت رایگان برای شما بارگذاری خواهد کرد.
            لطفاً آدرس وب‌سایت خود را وارد کنید تا بتوانیم محصولات شما را بررسی کنیم.
          </div>
        </v-alert>

        <v-form ref="formRef" v-model="valid" @submit.prevent="submitRequest">
          <v-text-field
            v-model="website"
            label="آدرس وب‌سایت"
            placeholder="https://example.com"
            prepend-inner-icon="mdi-web"
            :rules="websiteRules"
            :disabled="submitted || loading"
            required
            variant="outlined"
            class="mb-4"
          ></v-text-field>

          <v-btn
            type="submit"
            color="primary"
            size="large"
            :loading="loading"
            :disabled="submitted || !valid"
            block
            prepend-icon="mdi-send"
          >
            {{ submitted ? 'درخواست ارسال شد' : 'ارسال درخواست' }}
          </v-btn>
        </v-form>

        <v-alert
          v-if="submitted"
          type="success"
          variant="tonal"
          color="success"
          class="mt-4"
          border="start"
          elevation="0"
        >
          <div class="font-weight-bold mb-1">درخواست شما با موفقیت ثبت شد!</div>
          <div class="text-body-2">
            درخواست شما در حال بررسی است. پس از بررسی، ۳ محصول به صورت رایگان برای شما اضافه خواهد شد.
            شما می‌توانید وضعیت درخواست خود را در این بخش مشاهده کنید.
          </div>
        </v-alert>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApiFetch } from '~/composables/useApiFetch'
import { useToast } from '~/composables/useToast'

const { showToast } = useToast()

const formRef = ref<any>(null)
const valid = ref(false)
const website = ref('')
const loading = ref(false)
const submitted = ref(false)

const websiteRules = [
  (v: string) => !!v || 'آدرس وب‌سایت الزامی است',
  (v: string) => {
    if (!v) return true
    const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
    return urlPattern.test(v) || 'آدرس وب‌سایت معتبر نیست'
  }
]

const submitRequest = async () => {
  if (!valid.value || loading.value || submitted.value) return

  loading.value = true
  try {
    // Ensure URL has protocol
    let websiteUrl = website.value.trim()
    if (!websiteUrl.startsWith('http://') && !websiteUrl.startsWith('https://')) {
      websiteUrl = 'https://' + websiteUrl
    }

    await useApiFetch('product-upload-requests/', {
      method: 'POST',
      body: {
        website: websiteUrl
      }
    })

    submitted.value = true
    showToast({
      message: 'درخواست شما با موفقیت ثبت شد. ۳ محصول به صورت رایگان برای شما اضافه خواهد شد.',
      color: 'success'
    })
  } catch (error: any) {
    console.error('Error submitting product upload request:', error)
    const errorMessage = error?.data?.website?.[0] || 
                        error?.data?.detail || 
                        error?.message || 
                        'خطا در ارسال درخواست. لطفاً دوباره تلاش کنید.'
    showToast({
      message: errorMessage,
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}

// Check if user already has a request
const checkExistingRequest = async () => {
  try {
    const response = await useApiFetch('product-upload-requests/')
    const requests = Array.isArray(response) ? response : response.results || []
    const pendingOrCompleted = requests.find((req: any) => 
      req.status === 'pending' || req.status === 'completed'
    )
    
    if (pendingOrCompleted) {
      submitted.value = true
      if (pendingOrCompleted.status === 'completed') {
        website.value = pendingOrCompleted.website
      }
    }
  } catch (error) {
    console.error('Error checking existing request:', error)
  }
}

// Check on mount
onMounted(() => {
  checkExistingRequest()
})
</script>

<style scoped>
.product-upload-request-form {
  max-width: 600px;
  margin: 0 auto;
}
</style>

