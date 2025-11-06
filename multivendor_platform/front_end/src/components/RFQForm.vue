<template>
  <v-dialog
    v-model="dialog"
    max-width="800px"
    persistent
    scrollable
    dir="rtl"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center pa-4">
        <span class="text-h6">درخواست استعلام قیمت</span>
        <v-btn
          icon
          variant="text"
          size="small"
          @click="closeDialog"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      
      <v-divider></v-divider>
      
      <v-card-text class="pa-4">
        <v-form ref="form" v-model="valid">
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
                density="compact"
                :rules="[v => !!v || 'لطفاً یک محصول انتخاب کنید']"
                required
              ></v-select>
            </v-col>
            
            <!-- First Name -->
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.first_name"
                label="نام *"
                variant="outlined"
                density="compact"
                :rules="[v => !!v || 'نام الزامی است']"
                required
              ></v-text-field>
            </v-col>
            
            <!-- Last Name -->
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.last_name"
                label="نام خانوادگی *"
                variant="outlined"
                density="compact"
                :rules="[v => !!v || 'نام خانوادگی الزامی است']"
                required
              ></v-text-field>
            </v-col>
            
            <!-- Company Name -->
            <v-col cols="12">
              <v-text-field
                v-model="formData.company_name"
                label="نام شرکت *"
                variant="outlined"
                density="compact"
                :rules="[v => !!v || 'نام شرکت الزامی است']"
                required
              ></v-text-field>
            </v-col>
            
            <!-- Phone Number -->
            <v-col cols="12">
              <v-text-field
                v-model="formData.phone_number"
                label="شماره تماس *"
                variant="outlined"
                density="compact"
                :rules="[
                  v => !!v || 'شماره تماس الزامی است',
                  v => /^[0-9+\-\s()]+$/.test(v) || 'شماره تماس معتبر نیست'
                ]"
                required
              ></v-text-field>
            </v-col>
            
            <!-- Unique Needs -->
            <v-col cols="12">
              <v-textarea
                v-model="formData.unique_needs"
                label="نیازهای خاص شما *"
                variant="outlined"
                density="compact"
                rows="4"
                :rules="[v => !!v || 'لطفاً نیازهای خاص خود را توضیح دهید']"
                required
                hint="لطفاً نیازهای خاص، مشخصات فنی، یا هر اطلاعات دیگری که برای استعلام قیمت لازم است را وارد کنید"
                persistent-hint
              ></v-textarea>
            </v-col>
            
            <!-- Image Upload -->
            <v-col cols="12">
              <v-file-input
                v-model="imageFiles"
                label="تصاویر (حداکثر 10 تصویر)"
                variant="outlined"
                density="compact"
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
              <v-row v-if="imagePreviews.length > 0" class="mt-2">
                <v-col
                  v-for="(preview, index) in imagePreviews"
                  :key="index"
                  cols="6"
                  sm="4"
                  md="3"
                >
                  <v-card>
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
                        style="top: 4px; left: 4px;"
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
        </v-form>
      </v-card-text>
      
      <v-divider></v-divider>
      
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          variant="text"
          @click="closeDialog"
        >
          انصراف
        </v-btn>
        <v-btn
          color="primary"
          :loading="submitting"
          :disabled="!valid || submitting"
          @click="submitRFQ"
        >
          ارسال درخواست
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch, computed } from 'vue'
import api from '@/services/api'
import { useDisplay } from 'vuetify'

export default {
  name: 'RFQForm',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    productId: {
      type: Number,
      default: null
    },
    categoryId: {
      type: Number,
      default: null
    },
    products: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:modelValue', 'submitted', 'error'],
  setup(props, { emit }) {
    const { display } = useDisplay()
    const dialog = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value)
    })
    
    const form = ref(null)
    const valid = ref(false)
    const submitting = ref(false)
    const imageFiles = ref([])
    const imagePreviews = ref([])
    
    const showProductSelect = computed(() => {
      return !props.productId && props.products.length > 0
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
    
    const handleImageChange = (files) => {
      imagePreviews.value = []
      if (files && files.length > 0) {
        files.forEach(file => {
          if (file && file.type.startsWith('image/')) {
            const reader = new FileReader()
            reader.onload = (e) => {
              imagePreviews.value.push(e.target.result)
            }
            reader.readAsDataURL(file)
          }
        })
      }
    }
    
    const removeImage = (index) => {
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
        formDataToSend.append('product_id', formData.value.product_id)
        if (formData.value.category_id) {
          formDataToSend.append('category_id', formData.value.category_id)
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
        
        const response = await api.createRFQ(formDataToSend)
        
        emit('submitted', response.data)
        closeDialog()
      } catch (error) {
        console.error('RFQ submission error:', error)
        const errorMessage = error.response?.data?.error || 
                           error.response?.data?.message || 
                           'خطا در ارسال درخواست. لطفاً دوباره تلاش کنید.'
        emit('error', errorMessage)
      } finally {
        submitting.value = false
      }
    }
    
    return {
      dialog,
      form,
      valid,
      submitting,
      imageFiles,
      imagePreviews,
      showProductSelect,
      formData,
      handleImageChange,
      removeImage,
      closeDialog,
      submitRFQ,
      display
    }
  }
}
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>

