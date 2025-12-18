<template>
  <v-dialog
    v-model="dialog"
    max-width="900"
    scrollable
    persistent
    dir="rtl"
  >
    <v-card>
      <v-card-title class="d-flex align-center justify-space-between bg-primary text-white pa-4">
        <div class="d-flex align-center">
          <v-icon class="ml-2">mdi-gavel</v-icon>
          <span>درخواست مناقصه</span>
        </div>
        <v-btn
          icon
          variant="text"
          @click="closeDialog"
          class="text-white"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="pa-6">
        <v-stepper v-model="currentStep" alt-labels>
          <v-stepper-header>
            <v-stepper-item
              :complete="currentStep > 1"
              step="1"
              title="انتخاب دسته‌بندی"
            ></v-stepper-item>
            <v-stepper-item
              :complete="currentStep > 2"
              step="2"
              title="مشخصات فنی"
            ></v-stepper-item>
            <v-stepper-item
              :complete="currentStep > 3"
              step="3"
              title="تنظیمات مناقصه"
            ></v-stepper-item>
            <v-stepper-item
              :complete="currentStep > 4"
              step="4"
              title="تصاویر و مستندات"
            ></v-stepper-item>
            <v-stepper-item
              step="5"
              title="پرداخت واریز"
            ></v-stepper-item>
          </v-stepper-header>

          <v-stepper-window>
            <!-- Step 1: Subcategory Selection -->
            <v-stepper-window-item step="1">
              <div class="pa-4">
                <h3 class="text-h6 mb-4">انتخاب دسته‌بندی</h3>
                <v-autocomplete
                  v-model="formData.subcategory"
                  :items="searchableSubcategories"
                  :search="subcategorySearch"
                  item-title="label"
                  item-value="id"
                  label="جستجو و انتخاب زیردسته"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  :rules="[v => !!v || 'انتخاب زیردسته الزامی است']"
                  required
                  clearable
                  @update:model-value="onSubcategorySelect"
                >
                  <template #item="{ props, item }">
                    <v-list-item v-bind="props">
                      <template #title>
                        <div class="d-flex flex-column">
                          <span class="font-weight-bold">{{ item.raw.name }}</span>
                          <span class="text-caption text-medium-emphasis">{{ item.raw.path }}</span>
                        </div>
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </div>
            </v-stepper-window-item>

            <!-- Step 2: Technical Specs -->
            <v-stepper-window-item step="2">
              <div class="pa-4">
                <h3 class="text-h6 mb-4">مشخصات فنی</h3>
                <v-textarea
                  v-model="formData.description"
                  label="توضیحات نیاز شما"
                  prepend-inner-icon="mdi-text"
                  variant="outlined"
                  rows="4"
                  :rules="[v => !!v || 'توضیحات الزامی است']"
                  required
                  class="mb-4"
                ></v-textarea>

                <div v-if="featureTemplates.length > 0">
                  <h4 class="text-subtitle-1 mb-3">مشخصات فنی (از قالب)</h4>
                  <v-card variant="outlined" class="pa-4">
                    <div
                      v-for="template in featureTemplates"
                      :key="template.id"
                      class="mb-3"
                    >
                      <v-text-field
                        v-model="technicalSpecs[template.feature_name]"
                        :label="template.feature_name"
                        :required="template.is_required"
                        variant="outlined"
                        :rules="template.is_required ? [v => !!v || 'این فیلد الزامی است'] : []"
                      ></v-text-field>
                    </div>
                  </v-card>
                </div>
              </div>
            </v-stepper-window-item>

            <!-- Step 3: Auction Settings -->
            <v-stepper-window-item step="3">
              <div class="pa-4">
                <h3 class="text-h6 mb-4">تنظیمات مناقصه</h3>
                
                <v-select
                  v-model="formData.auction_style"
                  :items="auctionStyles"
                  label="نوع مناقصه"
                  prepend-inner-icon="mdi-format-list-bulleted"
                  variant="outlined"
                  :rules="[v => !!v || 'انتخاب نوع مناقصه الزامی است']"
                  required
                  class="mb-4"
                ></v-select>

                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.start_time"
                      label="زمان شروع"
                      type="datetime-local"
                      prepend-inner-icon="mdi-calendar-start"
                      variant="outlined"
                      :rules="[v => !!v || 'زمان شروع الزامی است']"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.end_time"
                      label="زمان پایان"
                      type="datetime-local"
                      prepend-inner-icon="mdi-calendar-end"
                      variant="outlined"
                      :rules="[v => !!v || 'زمان پایان الزامی است']"
                      required
                    ></v-text-field>
                  </v-col>
                </v-row>
              </div>
            </v-stepper-window-item>

            <!-- Step 4: Photos and Documents -->
            <v-stepper-window-item step="4">
              <div class="pa-4">
                <h3 class="text-h6 mb-4">تصاویر و مستندات</h3>
                
                <v-card variant="outlined" class="pa-4 mb-4">
                  <h4 class="text-subtitle-1 mb-3">تصاویر</h4>
                  <v-file-input
                    v-model="photoFiles"
                    label="انتخاب تصاویر"
                    prepend-icon="mdi-camera"
                    variant="outlined"
                    multiple
                    accept="image/*"
                    @change="handlePhotoUpload"
                  ></v-file-input>
                  <div v-if="uploadedPhotos.length > 0" class="mt-3">
                    <div class="d-flex flex-wrap gap-2">
                      <v-chip
                        v-for="photo in uploadedPhotos"
                        :key="photo.id"
                        closable
                        @click:close="removePhoto(photo.id)"
                      >
                        تصویر {{ photo.id }}
                      </v-chip>
                    </div>
                  </div>
                </v-card>

                <v-card variant="outlined" class="pa-4">
                  <h4 class="text-subtitle-1 mb-3">مستندات (فقط برای درخواست‌های تایید شده)</h4>
                  <v-file-input
                    v-model="documentFiles"
                    label="انتخاب فایل"
                    prepend-icon="mdi-file-document"
                    variant="outlined"
                    multiple
                    :disabled="!canUploadDocuments"
                    @change="handleDocumentUpload"
                  ></v-file-input>
                  <v-alert
                    v-if="!canUploadDocuments"
                    type="info"
                    variant="tonal"
                    density="compact"
                    class="mt-2"
                  >
                    برای آپلود مستندات باید واریز پرداخت کنید
                  </v-alert>
                  <div v-if="uploadedDocuments.length > 0" class="mt-3">
                    <div class="d-flex flex-wrap gap-2">
                      <v-chip
                        v-for="doc in uploadedDocuments"
                        :key="doc.id"
                        closable
                        @click:close="removeDocument(doc.id)"
                      >
                        {{ doc.file_name }}
                      </v-chip>
                    </div>
                  </div>
                </v-card>
              </div>
            </v-stepper-window-item>

            <!-- Step 5: Deposit Payment -->
            <v-stepper-window-item step="5">
              <div class="pa-4">
                <h3 class="text-h6 mb-4">پرداخت واریز</h3>
                
                <v-card variant="outlined" class="pa-4 mb-4">
                  <v-radio-group v-model="formData.request_type">
                    <v-radio
                      label="درخواست رایگان (فقط فرم‌ها)"
                      value="free"
                    ></v-radio>
                    <v-radio
                      label="درخواست تایید شده (با واریز ۵,۰۰۰,۰۰۰ تومان)"
                      value="verified"
                    ></v-radio>
                  </v-radio-group>
                </v-card>

                <v-alert
                  v-if="formData.request_type === 'verified'"
                  type="info"
                  variant="tonal"
                  class="mb-4"
                >
                  <div class="text-body-2">
                    با پرداخت واریز، درخواست شما به عنوان "تایید شده" نمایش داده می‌شود و می‌توانید مستندات آپلود کنید.
                  </div>
                </v-alert>

                <v-btn
                  v-if="formData.request_type === 'verified' && !depositPaid"
                  color="primary"
                  block
                  size="large"
                  @click="handleDepositPayment"
                  :loading="processingPayment"
                  prepend-icon="mdi-credit-card"
                >
                  پرداخت واریز (۵,۰۰۰,۰۰۰ تومان)
                </v-btn>

                <v-alert
                  v-if="depositPaid"
                  type="success"
                  variant="tonal"
                  class="mt-4"
                >
                  واریز با موفقیت پرداخت شد
                </v-alert>
              </div>
            </v-stepper-window-item>
          </v-stepper-window>
        </v-stepper>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          v-if="currentStep > 1"
          variant="text"
          @click="currentStep--"
        >
          قبلی
        </v-btn>
        <v-btn
          v-if="currentStep < 5"
          color="primary"
          @click="nextStep"
        >
          بعدی
        </v-btn>
        <v-btn
          v-if="currentStep === 5"
          color="primary"
          @click="submitRequest"
          :loading="submitting"
          prepend-icon="mdi-check"
        >
          ثبت درخواست
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useAuctionApi, type AuctionPhoto, type AuctionDocument } from '~/composables/useAuctionApi'
import { useProductApi } from '~/composables/useProductApi'
import { useAuthStore } from '~/stores/auth'

const props = defineProps<{
  modelValue: boolean
  productId?: number
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'success': []
  'error': [message: string]
}>()

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const auctionApi = useAuctionApi()
const productApi = useProductApi()
const authStore = useAuthStore()

const currentStep = ref(1)
const submitting = ref(false)
const processingPayment = ref(false)
const subcategorySearch = ref('')
const searchableSubcategories = ref<any[]>([])
const featureTemplates = ref<any[]>([])
const photoFiles = ref<File[]>([])
const documentFiles = ref<File[]>([])
const uploadedPhotos = ref<AuctionPhoto[]>([])
const uploadedDocuments = ref<AuctionDocument[]>([])
const depositPaid = ref(false)

const formData = ref({
  subcategory: null as number | null,
  description: '',
  technical_specs: {} as Record<string, any>,
  auction_style: 'sealed' as 'sealed' | 'live_reverse',
  start_time: '',
  end_time: '',
  request_type: 'free' as 'free' | 'verified',
})

const technicalSpecs = ref<Record<string, string>>({})

const auctionStyles = [
  { title: 'مناقصه پاکتی', value: 'sealed' },
  { title: 'مناقصه زنده معکوس', value: 'live_reverse' },
]

const canUploadDocuments = computed(() => {
  return depositPaid.value || formData.value.request_type === 'verified'
})

onMounted(async () => {
  await loadSubcategories()
})

const loadSubcategories = async () => {
  try {
    const response = await productApi.getSubcategories()
    if (response && (response as any).results) {
      const subs = (response as any).results
      searchableSubcategories.value = subs.map((sub: any) => ({
        id: sub.id,
        name: sub.name,
        label: sub.name,
        path: sub.name, // Simplified for now
      }))
    }
  } catch (error) {
    console.error('Error loading subcategories:', error)
  }
}

const onSubcategorySelect = async (subcategoryId: number | null) => {
  if (!subcategoryId) {
    featureTemplates.value = []
    technicalSpecs.value = {}
    return
  }

  try {
    const response = await productApi.getSubcategoryFeatureTemplates(subcategoryId)
    if (response && (response as any).results) {
      featureTemplates.value = (response as any).results
      technicalSpecs.value = {}
      featureTemplates.value.forEach((template: any) => {
        technicalSpecs.value[template.feature_name] = ''
      })
    } else {
      featureTemplates.value = []
      technicalSpecs.value = {}
    }
  } catch (error) {
    console.error('Error loading feature templates:', error)
    featureTemplates.value = []
  }
}

const handlePhotoUpload = async (files: File[] | null) => {
  if (!files || files.length === 0) return

  for (const file of files) {
    try {
      const photo = await auctionApi.uploadPhoto(file)
      uploadedPhotos.value.push(photo)
    } catch (error) {
      console.error('Error uploading photo:', error)
      emit('error', 'خطا در آپلود تصویر')
    }
  }
  photoFiles.value = []
}

const handleDocumentUpload = async (files: File[] | null) => {
  if (!files || files.length === 0 || !canUploadDocuments.value) return

  for (const file of files) {
    try {
      const doc = await auctionApi.uploadDocument(file, file.name)
      uploadedDocuments.value.push(doc)
    } catch (error) {
      console.error('Error uploading document:', error)
      emit('error', 'خطا در آپلود مستند')
    }
  }
  documentFiles.value = []
}

const removePhoto = (photoId: number) => {
  uploadedPhotos.value = uploadedPhotos.value.filter(p => p.id !== photoId)
}

const removeDocument = (docId: number) => {
  uploadedDocuments.value = uploadedDocuments.value.filter(d => d.id !== docId)
}

const handleDepositPayment = async () => {
  // First, create the auction as draft
  if (!formData.value.subcategory || !formData.value.description) {
    emit('error', 'لطفا تمام فیلدهای الزامی را پر کنید')
    return
  }

  processingPayment.value = true
  try {
    // Create auction first
    formData.value.technical_specs = technicalSpecs.value
    const auctionData = {
      product: props.productId || null,
      subcategory: formData.value.subcategory,
      request_type: 'verified', // Set to verified for deposit payment
      auction_style: formData.value.auction_style,
      start_time: formData.value.start_time,
      end_time: formData.value.end_time,
      description: formData.value.description,
      technical_specs: formData.value.technical_specs,
      photo_ids: uploadedPhotos.value.map(p => p.id),
      document_ids: uploadedDocuments.value.map(d => d.id),
    }

    const createdAuction = await auctionApi.createAuctionRequest(auctionData)
    
    // Now request deposit payment
    const paymentData = await auctionApi.requestDepositPayment(createdAuction.id)
    if (paymentData.payment_url) {
      window.location.href = paymentData.payment_url
    }
  } catch (error: any) {
    console.error('Error requesting deposit payment:', error)
    emit('error', error.message || 'خطا در درخواست پرداخت')
    processingPayment.value = false
  }
}

const nextStep = () => {
  // Basic validation
  if (currentStep.value === 1 && !formData.value.subcategory) {
    emit('error', 'لطفا زیردسته را انتخاب کنید')
    return
  }
  if (currentStep.value === 2 && !formData.value.description) {
    emit('error', 'لطفا توضیحات را وارد کنید')
    return
  }
  if (currentStep.value === 3 && (!formData.value.start_time || !formData.value.end_time)) {
    emit('error', 'لطفا زمان شروع و پایان را وارد کنید')
    return
  }
  currentStep.value++
}

const submitRequest = async () => {
  submitting.value = true
  try {
    // Prepare technical specs
    formData.value.technical_specs = technicalSpecs.value

    // If verified type and deposit not paid, redirect to payment
    if (formData.value.request_type === 'verified' && !depositPaid.value) {
      await handleDepositPayment()
      return // Payment will redirect, so don't close dialog yet
    }

    // Create auction request
    const auctionData = {
      product: props.productId || null,
      subcategory: formData.value.subcategory,
      request_type: formData.value.request_type,
      auction_style: formData.value.auction_style,
      start_time: formData.value.start_time,
      end_time: formData.value.end_time,
      description: formData.value.description,
      technical_specs: formData.value.technical_specs,
      photo_ids: uploadedPhotos.value.map(p => p.id),
      document_ids: uploadedDocuments.value.map(d => d.id),
    }

    await auctionApi.createAuctionRequest(auctionData)
    
    emit('success')
    closeDialog()
  } catch (error: any) {
    console.error('Error creating auction request:', error)
    emit('error', error.message || 'خطا در ثبت درخواست')
  } finally {
    submitting.value = false
  }
}

const closeDialog = () => {
  dialog.value = false
  // Reset form
  currentStep.value = 1
  formData.value = {
    subcategory: null,
    description: '',
    technical_specs: {},
    auction_style: 'sealed',
    start_time: '',
    end_time: '',
    request_type: 'free',
  }
  technicalSpecs.value = {}
  uploadedPhotos.value = []
  uploadedDocuments.value = []
  depositPaid.value = false
}
</script>

<style scoped>
.v-stepper {
  box-shadow: none;
}
</style>

