<template>
  <v-dialog
    v-model="dialog"
    max-width="900px"
    persistent
    scrollable
    dir="rtl"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center pa-4" style="background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));">
        <div class="d-flex align-center gap-3">
          <v-icon color="white">mdi-file-document-edit-outline</v-icon>
          <span class="text-h6 text-white">درخواست استعلام قیمت</span>
        </div>
        <v-btn
          icon
          variant="text"
          size="small"
          color="white"
          @click="closeDialog"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <!-- Progress Steps -->
      <v-card-subtitle class="pa-4 bg-grey-lighten-5">
        <v-stepper
          v-model="currentStep"
          alt-labels
          elevation="0"
          bg-color="transparent"
        >
          <v-stepper-header>
            <v-stepper-item
              :complete="currentStep > 1"
              :value="1"
              title="توضیحات و تصاویر"
              subtitle="نیازهای خود را شرح دهید"
            ></v-stepper-item>
            <v-divider></v-divider>
            <v-stepper-item
              :complete="currentStep > 2"
              :value="2"
              title="اطلاعات تماس"
              subtitle="اطلاعات شخصی و تماس"
            ></v-stepper-item>
          </v-stepper-header>
        </v-stepper>
      </v-card-subtitle>

      <v-divider></v-divider>

      <v-card-text class="pa-6">
        <v-form ref="form" v-model="valid">
          <!-- Step 1: Description and Images -->
          <div v-if="currentStep === 1" class="step-content">
            <div class="text-h6 mb-4 d-flex align-center gap-2">
              <v-icon color="primary">mdi-text-box-outline</v-icon>
              <span>گام اول: توضیحات و تصاویر</span>
            </div>

            <v-row>
              <!-- Unique Needs / Description -->
              <v-col cols="12">
                <v-textarea
                  v-model="formData.unique_needs"
                  label="نیازهای خاص شما *"
                  variant="outlined"
                  density="comfortable"
                  rows="6"
                  :rules="[v => !!v || 'لطفاً نیازهای خاص خود را توضیح دهید']"
                  required
                  hint="لطفاً نیازهای خاص، مشخصات فنی، یا هر اطلاعات دیگری که برای استعلام قیمت لازم است را وارد کنید"
                  persistent-hint
                  prepend-inner-icon="mdi-text"
                ></v-textarea>
              </v-col>

              <!-- Image Upload -->
              <v-col cols="12">
                <v-file-input
                  v-model="imageFiles"
                  label="تصاویر (حداکثر 10 تصویر)"
                  variant="outlined"
                  density="comfortable"
                  multiple
                  accept="image/jpeg,image/png,image/webp"
                  :rules="[
                    v => !v || v.length <= 10 || 'حداکثر 10 تصویر مجاز است'
                  ]"
                  show-size
                  prepend-icon="mdi-camera"
                  @update:model-value="handleImageChange"
                >
                  <template v-slot:selection="{ fileNames }">
                    <template v-for="(fileName, index) in fileNames" :key="fileName">
                      <v-chip
                        v-if="index < 2"
                        color="primary"
                        size="small"
                        label
                        class="me-2"
                      >
                        {{ fileName }}
                      </v-chip>
                    </template>
                    <span
                      v-if="fileNames.length > 2"
                      class="text-overline text-grey ms-2"
                    >
                      +{{ fileNames.length - 2 }} فایل دیگر
                    </span>
                  </template>
                </v-file-input>

                <!-- Image Preview -->
                <v-row v-if="imagePreviews.length > 0" class="mt-4">
                  <v-col
                    v-for="(preview, index) in imagePreviews"
                    :key="index"
                    cols="6"
                    sm="4"
                    md="3"
                  >
                    <v-card elevation="2" class="image-preview-card">
                      <v-img
                        :src="preview"
                        aspect-ratio="1"
                        cover
                        class="position-relative"
                      >
                        <v-btn
                          icon
                          size="small"
                          color="error"
                          class="position-absolute"
                          style="top: 4px; left: 4px; z-index: 1;"
                          @click="removeImage(index)"
                        >
                          <v-icon>mdi-close</v-icon>
                        </v-btn>
                      </v-img>
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </div>

          <!-- Step 2: Personal Information -->
          <div v-if="currentStep === 2" class="step-content">
            <div class="text-h6 mb-4 d-flex align-center gap-2">
              <v-icon color="primary">mdi-account-outline</v-icon>
              <span>گام دوم: اطلاعات تماس</span>
            </div>

            <v-row>
              <!-- Product Selection (if from category page) -->
              <v-col v-if="showProductSelect" cols="12">
                <v-select
                  v-model="formData.product_id"
                  :items="products"
                  item-title="name"
                  item-value="id"
                  label="انتخاب محصول *"
                  variant="outlined"
                  density="comfortable"
                  :rules="[v => !!v || 'لطفاً یک محصول انتخاب کنید']"
                  required
                  prepend-inner-icon="mdi-package-variant"
                ></v-select>
              </v-col>

              <!-- First Name -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.first_name"
                  label="نام *"
                  variant="outlined"
                  density="comfortable"
                  :rules="[v => !!v || 'نام الزامی است']"
                  required
                  prepend-inner-icon="mdi-account"
                ></v-text-field>
              </v-col>

              <!-- Last Name -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.last_name"
                  label="نام خانوادگی *"
                  variant="outlined"
                  density="comfortable"
                  :rules="[v => !!v || 'نام خانوادگی الزامی است']"
                  required
                  prepend-inner-icon="mdi-account"
                ></v-text-field>
              </v-col>

              <!-- Company Name -->
              <v-col cols="12">
                <v-text-field
                  v-model="formData.company_name"
                  label="نام شرکت *"
                  variant="outlined"
                  density="comfortable"
                  :rules="[v => !!v || 'نام شرکت الزامی است']"
                  required
                  prepend-inner-icon="mdi-office-building"
                ></v-text-field>
              </v-col>

              <!-- Phone Number -->
              <v-col cols="12">
                <v-text-field
                  v-model="formData.phone_number"
                  label="شماره تماس *"
                  variant="outlined"
                  density="comfortable"
                  :rules="[
                    v => !!v || 'شماره تماس الزامی است',
                    v => /^[0-9+\-\s()]+$/.test(v) || 'شماره تماس معتبر نیست'
                  ]"
                  required
                  prepend-inner-icon="mdi-phone"
                ></v-text-field>
              </v-col>
            </v-row>
          </div>
        </v-form>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4">
        <v-btn
          v-if="currentStep > 1"
          variant="text"
          @click="previousStep"
        >
          <v-icon class="ms-2">mdi-arrow-right</v-icon>
          مرحله قبل
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          variant="text"
          @click="closeDialog"
        >
          انصراف
        </v-btn>
        <v-btn
          v-if="currentStep < 2"
          color="primary"
          :disabled="!canProceedToNextStep"
          @click="nextStep"
        >
          مرحله بعد
          <v-icon class="me-2">mdi-arrow-left</v-icon>
        </v-btn>
        <v-btn
          v-else
          color="primary"
          :loading="submitting"
          :disabled="!valid || submitting"
          @click="submitRFQ"
        >
          <v-icon class="me-2">mdi-send</v-icon>
          ارسال درخواست
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRfqApi } from '~/composables/useRfqApi'

interface Props {
  modelValue: boolean
  productId?: number | null
  categoryId?: number | null
  products?: Array<{ id: number; name: string }>
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  productId: null,
  categoryId: null,
  products: () => []
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  submitted: [data: any]
  error: [message: string]
}>()

const rfqApi = useRfqApi()

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const form = ref<any>(null)
const valid = ref(false)
const submitting = ref(false)
const currentStep = ref(1)
const imageFiles = ref<File[]>([])
const imagePreviews = ref<string[]>([])

const showProductSelect = computed(() => {
  return !props.productId && props.products.length > 0
})

const canProceedToNextStep = computed(() => {
  if (currentStep.value === 1) {
    // Step 1 validation: description is required
    return !!formData.value.unique_needs && formData.value.unique_needs.trim().length > 0
  }
  return false
})

const formData = ref({
  product_id: props.productId || null,
  category_id: props.categoryId || null,
  first_name: '',
  last_name: '',
  company_name: '',
  phone_number: '',
  unique_needs: ''
})

// Watch for productId changes
watch(() => props.productId, (newId) => {
  if (newId) {
    formData.value.product_id = newId
  }
})

// Watch for categoryId changes
watch(() => props.categoryId, (newId) => {
  if (newId) {
    formData.value.category_id = newId
  }
})

const handleImageChange = (files: File[] | null) => {
  imagePreviews.value = []
  if (files && files.length > 0) {
    files.forEach(file => {
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          if (e.target?.result) {
            imagePreviews.value.push(e.target.result as string)
          }
        }
        reader.readAsDataURL(file)
      }
    })
  }
}

const removeImage = (index: number) => {
  imageFiles.value.splice(index, 1)
  imagePreviews.value.splice(index, 1)
}

const closeDialog = () => {
  dialog.value = false
  resetForm()
}

const resetForm = () => {
  if (form.value) {
    form.value.reset()
  }
  currentStep.value = 1
  formData.value = {
    product_id: props.productId || null,
    category_id: props.categoryId || null,
    first_name: '',
    last_name: '',
    company_name: '',
    phone_number: '',
    unique_needs: ''
  }
  imageFiles.value = []
  imagePreviews.value = []
}

const nextStep = () => {
  if (currentStep.value < 2 && canProceedToNextStep.value) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const submitRFQ = async () => {
  if (!form.value || !form.value.validate()) {
    return
  }

  // Validate product selection if needed
  if (!formData.value.product_id) {
    emit('error', 'لطفاً یک محصول انتخاب کنید')
    return
  }

  submitting.value = true

  try {
    // Create FormData for multipart/form-data
    const formDataToSend = new FormData()
    formDataToSend.append('product_id', formData.value.product_id.toString())
    if (formData.value.category_id) {
      formDataToSend.append('category_id', formData.value.category_id.toString())
    }
    formDataToSend.append('first_name', formData.value.first_name)
    formDataToSend.append('last_name', formData.value.last_name)
    formDataToSend.append('company_name', formData.value.company_name)
    formDataToSend.append('phone_number', formData.value.phone_number)
    formDataToSend.append('unique_needs', formData.value.unique_needs)

    // Append images
    if (imageFiles.value && imageFiles.value.length > 0) {
      imageFiles.value.forEach((file, index) => {
        if (file && file instanceof File) {
          formDataToSend.append(`images[${index}]`, file)
        }
      })
    }

    const response = await rfqApi.createRFQ(formDataToSend)

    emit('submitted', response)
    closeDialog()
  } catch (error: any) {
    console.error('RFQ submission error:', error)
    let errorMessage = 'خطا در ارسال درخواست. لطفاً دوباره تلاش کنید.'
    
    if (error?.data) {
      // Handle different error response formats
      if (typeof error.data === 'string') {
        errorMessage = error.data
      } else if (error.data.error) {
        errorMessage = error.data.error
      } else if (error.data.message) {
        errorMessage = error.data.message
      } else if (error.data.detail) {
        errorMessage = error.data.detail
      } else if (typeof error.data === 'object') {
        // Handle validation errors
        const firstError = Object.values(error.data)[0]
        if (Array.isArray(firstError)) {
          errorMessage = firstError[0]
        } else if (typeof firstError === 'string') {
          errorMessage = firstError
        }
      }
    } else if (error?.message) {
      errorMessage = error.message
    }
    
    emit('error', errorMessage)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.step-content {
  min-height: 400px;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.image-preview-card {
  transition: transform 0.2s ease;
}

.image-preview-card:hover {
  transform: scale(1.05);
}

:deep(.v-field__input) {
  color: rgba(var(--v-theme-on-surface), 0.92);
}

:deep(.v-field__label) {
  color: rgba(var(--v-theme-on-surface), 0.72);
}

:deep(.v-field__input::placeholder) {
  color: rgba(var(--v-theme-on-surface), 0.56);
}

:deep(.v-stepper-header) {
  padding: 0;
}

:deep(.v-stepper-item__title) {
  font-size: 0.875rem;
  font-weight: 600;
}

:deep(.v-stepper-item__subtitle) {
  font-size: 0.75rem;
  opacity: 0.7;
}
</style>

