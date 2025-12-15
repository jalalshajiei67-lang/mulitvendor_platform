<template>
  <div dir="rtl">
    <v-form @submit.prevent="saveProduct" ref="formRef">
      <v-row>
        <v-col cols="12" lg="8">
          <!-- Basic Information -->
          <v-card elevation="2" rounded="lg" class="mb-4">
            <v-card-title class="text-h6 font-weight-bold bg-primary pa-4">
              <v-icon class="ml-2">mdi-information</v-icon>
              اطلاعات پایه
            </v-card-title>
            <v-card-text class="pa-4">
              <v-text-field
                v-model="product.name"
                label="نام محصول"
                prepend-inner-icon="mdi-tag"
                variant="outlined"
                :rules="[v => !!v || 'نام محصول الزامی است']"
                required
                class="mb-2"
                data-tour="product-name-input"
              ></v-text-field>

              <v-text-field
                v-model="product.slug"
                label="Slug (نامک)"
                prepend-inner-icon="mdi-link-variant"
                variant="outlined"
                hint="در صورت خالی بودن، به صورت خودکار از نام محصول ایجاد می‌شود"
                persistent-hint
                class="mb-4"
              ></v-text-field>

              <div class="mb-4" data-tour="product-description-input">
                <label class="text-body-2 mb-2 d-block font-weight-medium">
                  <v-icon size="small" class="ml-1">mdi-text</v-icon>
                  توضیحات <span class="text-error">*</span>
                </label>
                <LazyTiptapEditor v-model="product.description" />
                <div v-if="!descriptionValid && descriptionTouched" class="text-error text-caption mt-1">
                  توضیحات الزami است
                </div>
              </div>

              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="formattedPrice"
                    label="قیمت (تومان)"
                    prepend-inner-icon="mdi-currency-usd"
                    variant="outlined"
                    type="text"
                    :rules="[v => {
                      const num = parsePriceValue(v)
                      return num >= 0 || 'قیمت باید مثبت باشد'
                    }]"
                    required
                    data-tour="product-price-input"
                    @input="onPriceInput"
                    @focus="onPriceFocus"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="product.stock"
                    label="موجودی انبار"
                    prepend-inner-icon="mdi-package-variant"
                    variant="outlined"
                    type="number"
                    min="0"
                    :rules="[v => v >= 0 || 'موجودی باید مثبت باشد']"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- Product Availability Status -->
              <v-select
                v-model="product.availability_status"
                :items="availabilityStatusOptions"
                item-title="label"
                item-value="value"
                label="وضعیت موجودی"
                prepend-inner-icon="mdi-package-variant-closed"
                variant="outlined"
                class="mb-4"
                :rules="[v => !!v || 'وضعیت موجودی الزامی است']"
                required
              ></v-select>

              <!-- Condition (shown only when in stock) -->
              <v-select
                v-if="product.availability_status === 'in_stock'"
                v-model="product.condition"
                :items="conditionOptions"
                item-title="label"
                item-value="value"
                label="وضعیت محصول"
                prepend-inner-icon="mdi-check-circle"
                variant="outlined"
                class="mb-4"
                :rules="[v => !!v || 'وضعیت محصول الزامی است']"
                required
              ></v-select>

              <!-- Lead Time (shown only when made to order) -->
              <v-text-field
                v-if="product.availability_status === 'made_to_order'"
                v-model.number="product.lead_time_days"
                label="زمان تحویل (روز کاری)"
                prepend-inner-icon="mdi-calendar-clock"
                variant="outlined"
                type="number"
                min="1"
                class="mb-4"
                :rules="[
                  v => !!v || 'زمان تحویل الزامی است',
                  v => v > 0 || 'زمان تحویل باید بیشتر از صفر باشد'
                ]"
                required
              ></v-text-field>

              <!-- Origin -->
              <v-select
                v-model="product.origin"
                :items="originOptions"
                item-title="label"
                item-value="value"
                label="مبدا"
                prepend-inner-icon="mdi-earth"
                variant="outlined"
                class="mb-4"
              ></v-select>
            </v-card-text>
          </v-card>

          <!-- Key Features -->
          <v-card elevation="2" rounded="lg" class="mb-4">
            <v-card-title class="text-h6 font-weight-bold bg-info pa-4">
              <v-icon class="ml-2">mdi-feature-search</v-icon>
              ویژگی‌های کلیدی
            </v-card-title>
            <v-card-text class="pa-4">
              <v-alert 
                type="info" 
                variant="tonal" 
                density="compact"
                class="mb-4"
              >
                <div class="text-body-2">
                  <v-icon size="small" class="ml-1">mdi-information</v-icon>
                  می‌توانید حداکثر ۱۰ ویژگی کلیدی برای محصول خود اضافه کنید.
                </div>
              </v-alert>

              <div v-for="(feature, index) in productFeatures" :key="index" class="mb-3">
                <v-row>
                  <v-col cols="12" sm="5">
                    <v-text-field
                      v-model="feature.name"
                      :label="`نام ویژگی ${index + 1}`"
                      placeholder="مثال: وزن، ابعاد، قدرت موتور، ظرفیت"
                      hint="نام ویژگی محصول را وارد کنید"
                      persistent-hint
                      variant="outlined"
                      density="compact"
                      :rules="[v => !!v || 'نام ویژگی الزامی است']"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="feature.value"
                      :label="`مقدار ${index + 1}`"
                      placeholder="مثال: 100 کیلوگرم، 50x30x20 سانتی‌متر، 5 اسب بخار"
                      hint="مقدار یا اندازه ویژگی را وارد کنید"
                      persistent-hint
                      variant="outlined"
                      density="compact"
                      :rules="[v => !!v || 'مقدار الزامی است']"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="1" class="d-flex align-center">
                    <v-btn
                      icon="mdi-delete"
                      variant="text"
                      color="error"
                      size="small"
                      @click="removeFeature(index)"
                      :disabled="productFeatures.length <= 1"
                    ></v-btn>
                  </v-col>
                </v-row>
              </div>

              <v-btn
                v-if="productFeatures.length < 10"
                color="primary"
                variant="outlined"
                prepend-icon="mdi-plus"
                @click="addFeature"
                block
                class="mt-2"
              >
                افزودن ویژگی
              </v-btn>
            </v-card-text>
          </v-card>

          <!-- Category Selection -->
          <v-card elevation="2" rounded="lg" class="mb-4">
            <v-card-title class="text-h6 font-weight-bold bg-secondary pa-4">
              <v-icon class="ml-2">mdi-folder-outline</v-icon>
              دسته‌بندی
            </v-card-title>
            <v-card-text class="pa-4">
              <v-alert 
                type="info" 
                variant="tonal" 
                density="compact"
                class="mb-4"
              >
                <div class="text-body-2">
                  <v-icon size="small" class="ml-1">mdi-information</v-icon>
                  اگر دسته‌بندی مناسب محصول خود را پیدا نکردید، می‌توانید درخواست ایجاد دسته‌بندی جدید دهید.
                </div>
              </v-alert>
              
              <!-- Searchable Subcategory Selector -->
              <div class="d-flex gap-2 align-center mb-2">
              <v-autocomplete
                v-model="product.subcategory"
                :items="filteredSearchableSubcategories"
                :search="subcategorySearch"
                item-title="label"
                item-value="id"
                label="جستجو و انتخاب زیردسته"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                  :rules="subcategoryRules"
                  :required="!showCategoryRequest"
                clearable
                data-tour="product-category-input"
                  class="flex-grow-1"
                @update:model-value="onSubcategorySelect"
                @update:search="onSubcategorySearch"
              >
                <template #item="{ props, item }">
                  <v-list-item v-bind="props">
                    <template #title>
                      <div class="d-flex flex-column">
                        <span class="font-weight-bold">{{ item.raw.name }}</span>
                        <span class="text-caption text-medium-emphasis">{{ item.raw.path }}</span>
                      </div>
                    </template>
                    <template #prepend>
                      <v-icon>mdi-folder-open</v-icon>
                    </template>
                  </v-list-item>
                </template>
                <template #no-data>
                  <v-list-item>
                    <v-list-item-title>
                      {{ subcategorySearch ? 'نتیجه‌ای یافت نشد' : 'شروع به تایپ کنید...' }}
                    </v-list-item-title>
                  </v-list-item>
                </template>
              </v-autocomplete>
                
                <!-- Always visible category request button -->
                <v-btn
                  v-if="!showCategoryRequest"
                  color="orange"
                  variant="outlined"
                  prepend-icon="mdi-plus-circle"
                  @click="showCategoryRequest = true"
                  class="mt-n2"
                >
                  درخواست دسته‌بندی جدید
                </v-btn>
              </div>

              <!-- Category Request Option (when search fails) -->
              <v-alert 
                v-if="subcategorySearch && subcategorySearch.length > 2 && !product.subcategory && filteredSearchableSubcategories.length === 0 && !showCategoryRequest"
                type="info" 
                variant="tonal" 
                class="mt-3"
              >
                <div class="d-flex align-center justify-space-between">
                  <div>
                    <strong class="d-block mb-1">دسته‌بندی مناسب پیدا نشد؟</strong>
                    <div class="text-body-2">می‌توانید درخواست ایجاد دسته‌بندی جدید دهید</div>
                  </div>
                  <v-btn
                    color="primary"
                    variant="outlined"
                    size="small"
                    @click="showCategoryRequest = true"
                  >
                    درخواست دسته‌بندی جدید
                  </v-btn>
                </div>
              </v-alert>

              <!-- Category Request Form (Inline) -->
              <v-card 
                v-if="showCategoryRequest" 
                elevation="1" 
                variant="outlined"
                class="mt-3"
              >
                <v-card-title class="text-subtitle-1 font-weight-bold pa-3 bg-orange-lighten-5">
                  <v-icon class="ml-2" color="orange">mdi-plus-circle</v-icon>
                  درخواست دسته‌بندی جدید
                </v-card-title>
                <v-card-text class="pa-4">
                  <v-text-field
                    v-model="categoryRequest.name"
                    label="نام دسته‌بندی پیشنهادی"
                    prepend-inner-icon="mdi-tag-plus"
                    variant="outlined"
                    :rules="[v => !!v || 'نام دسته‌بندی الزامی است']"
                    required
                    class="mb-3"
                    :disabled="requestingCategory"
                  ></v-text-field>
                  
                  <div class="d-flex gap-2">
                    <v-btn
                      @click="submitCategoryRequest"
                      color="primary"
                      :loading="requestingCategory"
                      prepend-icon="mdi-send"
                    >
                      ارسال درخواست
                    </v-btn>
                    <v-btn
                      @click="cancelCategoryRequest"
                      variant="outlined"
                      :disabled="requestingCategory"
                    >
                      انصراف
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>

              <!-- Full Path Display -->
              <v-alert 
                v-if="product.subcategory && selectedSubcategoryPath" 
                type="success" 
                variant="tonal" 
                class="mt-3"
              >
                <div class="d-flex align-center">
                  <v-icon class="ml-2">mdi-check-circle</v-icon>
                  <div>
                    <strong class="d-block mb-1">مسیر انتخاب شده:</strong>
                    <div class="text-body-2">{{ selectedSubcategoryPath }}</div>
                  </div>
                </div>
              </v-alert>

              <!-- Optional: Show Department and Category for reference -->
              <v-row v-if="product.subcategory && selectedSubcategoryPath" class="mt-2">
                <v-col cols="12" sm="6">
                  <v-text-field
                    :model-value="selectedDepartmentName"
                    label="دپارتمان"
                    prepend-inner-icon="mdi-sitemap"
                    variant="outlined"
                    readonly
                    density="compact"
                    :placeholder="selectedDepartment ? '' : 'در حال بارگذاری...'"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    :model-value="selectedCategoryName"
                    label="دسته‌بندی"
                    prepend-inner-icon="mdi-folder"
                    variant="outlined"
                    readonly
                    density="compact"
                    :placeholder="selectedCategory ? '' : 'در حال بارگذاری...'"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Product Images -->
          <v-card elevation="2" rounded="lg" class="mb-4">
            <v-card-title class="text-h6 font-weight-bold bg-info pa-4">
              <v-icon class="ml-2">mdi-image-multiple</v-icon>
              تصاویر محصول
            </v-card-title>
            <v-card-text class="pa-4">
              <!-- Image Upload Area -->
              <div
                class="image-upload-area"
                :class="{ 'drag-over': isDragOver }"
                @drop="handleDrop"
                @dragover.prevent="isDragOver = true"
                @dragleave="isDragOver = false"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept="image/*"
                  style="display: none"
                  @change="handleFileSelect"
                />
                <v-icon size="64" color="grey-lighten-1">mdi-cloud-upload</v-icon>
                <p class="text-h6 mt-2">تصاویر را اینجا رها کنید</p>
                <p class="text-caption">یا کلیک کنید تا فایل انتخاب کنید</p>
                <p class="text-caption text-grey">حداکثر 20 تصویر</p>
              </div>

              <!-- Error Message -->
              <v-alert v-if="imageError" type="error" variant="tonal" class="mt-3">
                {{ imageError }}
              </v-alert>

              <!-- Image Preview Grid -->
              <v-row v-if="uploadedImages.length > 0" class="mt-4">
                <v-col
                  v-for="(image, index) in uploadedImages"
                  :key="index"
                  cols="6"
                  sm="4"
                  md="3"
                >
                  <v-card elevation="2" class="image-preview-card">
                    <v-img
                      :src="image.preview"
                      aspect-ratio="1"
                      cover
                      class="rounded"
                    ></v-img>
                    <v-btn
                      icon
                      size="small"
                      color="error"
                      class="remove-image-btn"
                      @click.stop="removeImage(index)"
                    >
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-chip
                      v-if="index === 0"
                      size="small"
                      color="success"
                      class="main-image-badge"
                    >
                      تصویر اصلی
                    </v-chip>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" lg="4">
          <!-- Action Buttons (moved to top) -->
          <div class="action-buttons-container mb-4">
            <v-btn
              type="submit"
              color="primary"
              size="large"
              block
              :loading="submitting"
              prepend-icon="mdi-content-save"
              class="mb-2 save-button"
              elevation="3"
              data-tour="product-save-button"
            >
              {{ editMode ? 'به‌روزرسانی محصول' : 'ذخیره محصول' }}
            </v-btn>

            <v-btn
              color="grey"
              size="large"
              block
              variant="outlined"
              @click="$emit('cancel')"
              :disabled="submitting"
              class="cancel-button"
              elevation="2"
            >
              انصراف
            </v-btn>
          </div>

          <FormQualityScore
            class="mb-4"
            title="امتیاز محصول"
            caption="راهنمای قدم‌به‌قدم برای جذاب‌تر کردن محصول"
            :score="productScore"
            :metrics="productMetrics"
            :tips="productTips"
          />
          <!-- Status & Options -->
          <v-card elevation="2" rounded="lg" class="mb-4">
            <v-card-title class="text-h6 font-weight-bold bg-warning pa-4">
              <v-icon class="ml-2">mdi-cog</v-icon>
              تنظیمات
            </v-card-title>
            <v-card-text class="pa-4">
              <v-switch
                v-model="product.is_active"
                label="محصول فعال است"
                color="success"
                hide-details
                class="mb-3"
              ></v-switch>

              <v-switch
                v-model="product.is_featured"
                label="محصول ویژه"
                color="primary"
                hide-details
                class="mb-3"
              ></v-switch>


              <!-- Original Vuetify buttons (commented out for now) -->
              <!--
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="submitting"
                prepend-icon="mdi-content-save"
                class="mb-2"
              >
                {{ editMode ? 'به‌روزرسانی محصول' : 'ذخیره محصول' }}
              </v-btn>

              <v-btn
                color="grey"
                size="large"
                block
                variant="outlined"
                @click="$emit('cancel')"
                :disabled="submitting"
              >
                انصراف
              </v-btn>
              -->
            </v-card-text>
          </v-card>

          <!-- Help Card -->
          <v-card elevation="2" rounded="lg" class="help-card">
            <v-card-title class="text-subtitle-1 font-weight-bold pa-3">
              <v-icon class="ml-2" color="info">mdi-help-circle</v-icon>
              راهنما
            </v-card-title>
            <v-card-text class="pa-3">
              <ul class="text-caption help-list">
                <li>نام محصول باید واضح و توصیفی باشد</li>
                <li>قیمت را به تومان وارد کنید</li>
                <li>حداقل یک تصویر با کیفیت بالا اضافه کنید</li>
                <li>دسته‌بندی مناسب را انتخاب کنید</li>
                <li>توضیحات کامل و جامع بنویسید</li>
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-form>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="showSuccessSnackbar"
      color="success"
      :timeout="3000"
      location="top"
    >
      {{ successMessage }}
    </v-snackbar>

    <!-- Error Snackbar -->
    <v-snackbar
      v-model="showErrorSnackbar"
      color="error"
      :timeout="8000"
      location="top"
      multi-line
    >
      <div style="white-space: pre-line; max-width: 600px;">
        {{ errorMessage }}
      </div>
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="showErrorSnackbar = false"
        >
          بستن
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useProductApi } from '~/composables/useProductApi'
import { useDepartmentStore } from '~/stores/department'
import { useCategoryStore } from '~/stores/category'
import { useSubcategoryStore } from '~/stores/subcategory'
import { useGamificationStore } from '~/stores/gamification'
import { useSupplierOnboarding } from '~/composables/useSupplierOnboarding'
import { useToast } from '~/composables/useToast'
import FormQualityScore from '~/components/gamification/FormQualityScore.vue'

interface Props {
  productData?: any
  editMode?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  editMode: false
})

const emit = defineEmits(['saved', 'cancel'])

const productApi = useProductApi()
const departmentStore = useDepartmentStore()
const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()
const gamificationStore = useGamificationStore()
const { markActionCompleted } = useSupplierOnboarding()
const { showToast } = useToast()

const formRef = ref<any>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const product = ref<{
  name: string
  slug: string
  description: string
  price: number
  stock: number
  subcategory: number | null
  is_active: boolean
  is_featured: boolean
  availability_status: string
  condition: string
  origin: string
  lead_time_days: number | null
}>({
  name: '',
  slug: '',
  description: '',
  price: 0,
  stock: 0,
  subcategory: null,
  is_active: true,
  is_featured: false,
  availability_status: '',
  condition: '',
  origin: '',
  lead_time_days: null
})

const productFeatures = ref<Array<{ name: string; value: string }>>([{ name: '', value: '' }])

const availabilityStatusOptions = [
  { label: 'موجود در انبار', value: 'in_stock' },
  { label: 'سفارشی', value: 'made_to_order' }
]

const conditionOptions = [
  { label: 'نو', value: 'new' },
  { label: 'دست دوم', value: 'used' }
]

const originOptions = [
  { label: 'ساخت ایران', value: 'iran' },
  { label: 'وارداتی', value: 'imported' }
]

// Onboarding tour action tracking (one-time markers)
const completedActions = ref<Record<string, boolean>>({})
const markOnce = (actionId: string) => {
  if (completedActions.value[actionId]) return
  markActionCompleted(actionId)
  completedActions.value[actionId] = true
}

watch(() => product.value.name, (val) => {
  if (val && val.trim().length > 0) {
    markOnce('product-name-input')
  }
})

watch(() => product.value.description, (val) => {
  if (val && val.trim().length > 0) {
    markOnce('product-description-input')
  }
})

watch(() => product.value.price, (val) => {
  if (val !== null && val !== undefined && val > 0) {
    markOnce('product-price-input')
  }
})

watch(() => product.value.subcategory, (val) => {
  if (val) {
    markOnce('product-category-input')
  }
})

const awardProductSection = async (): Promise<number> => {
  try {
    const { useApiFetch } = await import('~/composables/useApiFetch')
    const resp = await useApiFetch<{ points?: number }>('gamification/award-section/', {
      method: 'POST',
      body: { section: 'product' }
    })
    await gamificationStore.fetchScores()
    return resp?.points || 0
  } catch (e) {
    console.warn('Failed to award product section points', e)
    return 0
  }
}

const addFeature = () => {
  if (productFeatures.value.length < 10) {
    productFeatures.value.push({ name: '', value: '' })
  }
}

const removeFeature = (index: number) => {
  if (productFeatures.value.length > 1) {
    productFeatures.value.splice(index, 1)
  }
}

const departments = ref<any[]>([])
const categories = ref<any[]>([])
const subcategories = ref<any[]>([])
const filteredCategories = ref<any[]>([])
const filteredSubcategories = ref<any[]>([])
const selectedDepartment = ref<number | null>(null)
const selectedCategory = ref<number | null>(null)
const subcategorySearch = ref('')
const searchableSubcategories = ref<Array<{ id: number; name: string; label: string; path: string; category: number; department: number }>>([])
const showCategoryRequest = ref(false)
const categoryRequest = ref({ name: '' })
const requestingCategory = ref(false)

const uploadedImages = ref<any[]>([])
const existingImageCount = ref(props.productData?.images?.length ?? 0)
const isDragOver = ref(false)
const imageError = ref('')
const descriptionTouched = ref(false)
const submitting = ref(false)
const showSuccessSnackbar = ref(false)
const showErrorSnackbar = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Price formatting functions
const formatPrice = (value: number | string): string => {
  if (!value && value !== 0) return '00,000'
  const numValue = typeof value === 'string' ? parsePriceValue(value) : value
  if (isNaN(numValue) || numValue === 0) return '00,000'
  return numValue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const parsePriceValue = (value: string | number): number => {
  if (typeof value === 'number') return value
  if (!value || value === '00,000') return 0
  const cleaned = value.toString().replace(/,/g, '').trim()
  const num = parseInt(cleaned, 10)
  return isNaN(num) ? 0 : num
}

// Formatted price computed property
const formattedPrice = computed({
  get: () => formatPrice(product.value.price),
  set: (val: string) => {
    product.value.price = parsePriceValue(val)
  }
})

const onPriceFocus = (event: Event) => {
  const target = event.target as HTMLInputElement
  // If the value is "00,000" or empty, select all so user can start typing
  if (target.value === '00,000' || !target.value) {
    target.select()
  }
}

const onPriceInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  let value = target.value
  const cursorPosition = target.selectionStart || 0
  
  // Remove all non-digit characters
  const cleaned = value.replace(/\D/g, '')
  
  // If empty or just zeros, set to 0
  if (!cleaned || cleaned === '0' || cleaned === '00' || cleaned === '000' || cleaned === '0000' || cleaned === '00000') {
    product.value.price = 0
    target.value = '00,000'
    target.setSelectionRange(0, 0)
    return
  }
  
  // If the number is less than 6 digits, multiply by 100000 to add 5 zeros
  // For example: "32" becomes "3200000" (3,200,000)
  let numericValue: number
  if (cleaned.length <= 5) {
    // User is typing the main number, append 5 zeros
    numericValue = parseInt(cleaned, 10) * 100000
  } else {
    // User has typed more than 5 digits, use as is
    numericValue = parseInt(cleaned, 10)
  }
  
  product.value.price = numericValue
  
  // Format the display value with commas
  const formatted = formatPrice(numericValue)
  
  // Update the input value
  if (target.value !== formatted) {
    target.value = formatted
    // Try to maintain cursor position intelligently
    const digitsBeforeCursor = value.substring(0, cursorPosition).replace(/\D/g, '').length
    let newPosition = 0
    let digitCount = 0
    for (let i = 0; i < formatted.length; i++) {
      if (/\d/.test(formatted[i])) {
        digitCount++
        if (digitCount === digitsBeforeCursor) {
          newPosition = i + 1
          break
        }
      }
    }
    target.setSelectionRange(newPosition, newPosition)
  }
}

const descriptionValid = computed(() => {
  if (!product.value.description) return false
  const textOnly = product.value.description.replace(/<[^>]*>/g, '').trim()
  return textOnly.length > 0
})

const cleanDescription = computed(() => (product.value.description || '').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim())
const descriptionWords = computed(() => (cleanDescription.value ? cleanDescription.value.split(' ').filter(Boolean).length : 0))
const totalImageCount = computed(() => existingImageCount.value + uploadedImages.value.length)

const productMetrics = computed(() => [
  {
    key: 'name',
    label: 'نام محصول',
    tip: 'نام را بین ۱۰ تا ۶۰ کاراکتر نگه دارید و مدل دستگاه را ذکر کنید.',
    weight: 0.15,
    passed: product.value.name.length >= 10 && product.value.name.length <= 60
  },
  {
    key: 'description',
    label: 'توضیحات',
    tip: 'حداقل ۱۵۰ کلمه درباره ویژگی‌ها و خدمات پس از فروش بنویسید.',
    weight: 0.25,
    passed: descriptionWords.value >= 150
  },
  {
    key: 'images',
    label: 'تصاویر',
    tip: 'سه تصویر واضح از زوایای مختلف دستگاه آپلود کنید.',
    weight: 0.2,
    passed: totalImageCount.value >= 3
  },
  {
    key: 'pricing',
    label: 'قیمت و موجودی',
    tip: 'قیمت و وضعیت موجودی را مشخص کنید.',
    weight: 0.1,
    passed: product.value.price > 0 && product.value.stock >= 0
  },
  {
    key: 'category',
    label: 'دسته‌بندی',
    tip: 'زیر دسته دقیق را انتخاب کنید تا مشتری راحت‌تر شما را پیدا کند.',
    weight: 0.1,
    passed: Boolean(product.value.subcategory)
  },
  {
    key: 'attributes',
    label: 'ویژگی‌ها و برچسب‌ها',
    tip: 'برچسب‌هایی مثل توان موتور یا ظرفیت تولید را وارد کنید.',
    weight: 0.05,
    passed: true // Placeholder until attributes UI متصل شود
  },
  {
    key: 'seo',
    label: 'سئو',
    tip: 'نامک و توضیح کوتاه را تکمیل کنید.',
    weight: 0.1,
    passed: Boolean(product.value.slug && product.value.slug.length > 3 && product.value.description)
  },
  {
    key: 'status',
    label: 'وضعیت نمایش',
    tip: 'محصول را در حالت فعال قرار دهید تا در لیست‌ها دیده شود.',
    weight: 0.05,
    passed: product.value.is_active
  }
])

const productScore = computed(() => {
  const metrics = productMetrics.value
  const totalWeight = metrics.reduce((sum, metric) => sum + metric.weight, 0)
  const earned = metrics.reduce((sum, metric) => sum + (metric.passed ? metric.weight : 0), 0)
  return totalWeight ? Math.round((earned / totalWeight) * 100) : 0
})

const productTips = computed(() => productMetrics.value.filter(metric => !metric.passed).map(metric => metric.tip))

watch(productScore, (score) => {
  gamificationStore.updateLocalScore('product', {
    title: 'product',
    score,
    metrics: productMetrics.value,
    tips: productTips.value
  })
}, { immediate: true })

watch(() => product.value.description, () => {
  descriptionTouched.value = true
})

watch(() => props.productData, (value) => {
  existingImageCount.value = value?.images?.length ?? 0
})

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = Array.from(target.files || [])
  addImages(files)
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = false
  const files = Array.from(event.dataTransfer?.files || [])
  addImages(files)
}

const addImages = (files: File[]) => {
  imageError.value = ''
  const imageFiles = files.filter(file => file.type.startsWith('image/'))

  if (imageFiles.length === 0) {
    imageError.value = 'فقط فایل‌های تصویری مجاز هستند'
    return
  }

  if (uploadedImages.value.length + imageFiles.length > 20) {
    imageError.value = 'حداکثر 20 تصویر مجاز است'
    return
  }

  imageFiles.forEach(file => {
    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImages.value.push({
        file: file,
        preview: e.target?.result
      })
    }
    reader.readAsDataURL(file)
  })
}

const removeImage = (index: number) => {
  uploadedImages.value.splice(index, 1)
}

// Build searchable subcategories with full path
const buildSearchableSubcategories = () => {
  const searchable: Array<{ id: number; name: string; label: string; path: string; category: number; department: number }> = []
  
  subcategories.value.forEach(sub => {
    // Handle both 'category' (singular) and 'categories' (plural/array)
    let categoryId: number | null = null
    let category: any = null
    
    // Check if subcategory has 'categories' array (ManyToMany)
    if (sub.categories && Array.isArray(sub.categories) && sub.categories.length > 0) {
      // Use first category from the array
      const firstCategory = sub.categories[0]
      categoryId = typeof firstCategory === 'object' ? firstCategory?.id : firstCategory
      category = categories.value.find(c => c.id === categoryId)
    } 
    // Fallback to 'category' (singular) field
    else if (sub.category) {
      categoryId = typeof sub.category === 'object' ? sub.category?.id : sub.category
      category = categories.value.find(c => c.id === categoryId)
    }
    
    // Get department - handle both object and ID
    let departmentId: number | null = null
    let department: any = null
    
    if (category) {
      // Handle both 'department' (singular) and 'departments' (array)
      if (category.departments && Array.isArray(category.departments) && category.departments.length > 0) {
        const firstDept = category.departments[0]
        departmentId = typeof firstDept === 'object' ? firstDept?.id : firstDept
        department = departments.value.find(d => d.id === departmentId)
      } else if (category.department) {
        departmentId = typeof category.department === 'object' ? category.department?.id : category.department
        department = departments.value.find(d => d.id === departmentId)
      }
    }
    
    // Also check if subcategory has departments directly
    if (!department && sub.departments && Array.isArray(sub.departments) && sub.departments.length > 0) {
      const firstDept = sub.departments[0]
      departmentId = typeof firstDept === 'object' ? firstDept?.id : firstDept
      department = departments.value.find(d => d.id === departmentId)
    }
    
    // Build path
    const pathParts: string[] = []
    if (department) pathParts.push(department.name)
    if (category) pathParts.push(category.name)
    pathParts.push(sub.name)
    const path = pathParts.join(' ← ')
    
    // Only add if we have valid category and department
    if (categoryId && departmentId) {
      searchable.push({
        id: sub.id,
        name: sub.name,
        label: sub.name,
        path: path,
        category: categoryId,
        department: departmentId
      })
    } else {
      // Still add but with null values - will be handled in selection
      searchable.push({
        id: sub.id,
        name: sub.name,
        label: sub.name,
        path: path,
        category: categoryId || 0,
        department: departmentId || 0
      })
    }
  })
  
  searchableSubcategories.value = searchable
}

const subcategoryRules = computed(() => {
  if (showCategoryRequest.value) {
    return [] // No validation when category request is shown
  }
  return [(v: any) => !!v || 'زیردسته الزامی است']
})

const onSubcategorySearch = (value: string) => {
  subcategorySearch.value = value
  // Hide category request form if user starts searching again
  if (value && showCategoryRequest.value) {
    showCategoryRequest.value = false
  }
}

const onSubcategorySelect = (subcategoryId: number | null) => {
  if (!subcategoryId) {
    selectedDepartment.value = null
    selectedCategory.value = null
    return
  }
  
  const subcategory = searchableSubcategories.value.find(s => s.id === subcategoryId)
  if (subcategory) {
    // Set category and department from the searchable subcategory
    selectedCategory.value = subcategory.category || null
    selectedDepartment.value = subcategory.department || null
    
    // Debug logging
    console.log('Subcategory selected:', {
      subcategoryId,
      category: subcategory.category,
      department: subcategory.department,
      path: subcategory.path
    })
  } else {
    console.warn('Subcategory not found in searchable list:', subcategoryId)
  }
}

const selectedSubcategoryPath = computed(() => {
  if (!product.value.subcategory) return null
  const sub = searchableSubcategories.value.find(s => s.id === product.value.subcategory)
  return sub?.path || null
})

const selectedDepartmentName = computed(() => {
  if (!selectedDepartment.value || selectedDepartment.value === 0) return ''
  const dept = departments.value.find(d => d.id === selectedDepartment.value)
  return dept?.name || ''
})

const selectedCategoryName = computed(() => {
  if (!selectedCategory.value || selectedCategory.value === 0) return ''
  const cat = categories.value.find(c => c.id === selectedCategory.value)
  return cat?.name || ''
})

// Filter searchable subcategories based on search term
const filteredSearchableSubcategories = computed(() => {
  if (!subcategorySearch.value) {
    return searchableSubcategories.value
  }
  
  const searchLower = subcategorySearch.value.toLowerCase()
  return searchableSubcategories.value.filter(sub => {
    return (
      sub.name.toLowerCase().includes(searchLower) ||
      sub.path.toLowerCase().includes(searchLower)
    )
  })
})

const onDepartmentChange = () => {
  if (selectedDepartment.value) {
    filteredCategories.value = categories.value.filter(cat => {
      const deptId = typeof cat.department === 'object' ? cat.department?.id : cat.department
      return deptId === selectedDepartment.value
    })
    selectedCategory.value = null
    product.value.subcategory = null
    filteredSubcategories.value = []
  }
}

const onCategoryChange = () => {
  if (selectedCategory.value) {
    filteredSubcategories.value = subcategories.value.filter(sub => {
      const catId = typeof sub.category === 'object' ? sub.category?.id : sub.category
      return catId === selectedCategory.value
    })
    product.value.subcategory = null
  }
}

const fetchFormData = async () => {
  try {
    await Promise.all([
      departmentStore.fetchDepartments(),
      categoryStore.fetchCategories(),
      subcategoryStore.fetchSubcategories()
    ])

    departments.value = departmentStore.departments
    categories.value = categoryStore.categories
    subcategories.value = subcategoryStore.subcategories

    filteredCategories.value = categories.value
    filteredSubcategories.value = subcategories.value
    
    // Build searchable subcategories after data is loaded
    buildSearchableSubcategories()
  } catch (error) {
    console.error('Error fetching form data:', error)
  }
}

const submitCategoryRequest = async () => {
  if (!categoryRequest.value.name || !categoryRequest.value.name.trim()) {
    errorMessage.value = 'نام دسته‌بندی الزامی است'
    showErrorSnackbar.value = true
    return
  }

  // Validate product form first
  descriptionTouched.value = true
  const formInstance = formRef.value
  if (!formInstance) return

  const { valid } = await formInstance.validate()
  if (!valid) {
    errorMessage.value = 'لطفاً تمام فیلدهای الزامی محصول را پر کنید'
    showErrorSnackbar.value = true
    return
  }

  if (!descriptionValid.value) {
    errorMessage.value = 'توضیحات محصول الزامی است'
    showErrorSnackbar.value = true
    return
  }

  requestingCategory.value = true

  try {
    const { useApiFetch } = await import('~/composables/useApiFetch')
    
    // First create the category request
    const requestResponse = await useApiFetch('/category-requests/', {
      method: 'POST',
      body: {
        requested_name: categoryRequest.value.name.trim()
      }
    })

    console.log('Category request response:', requestResponse)

    if (requestResponse && (requestResponse as any).id) {
      // Now save the product with the category request linked
      await saveProductWithRequest((requestResponse as any).id)
    } else {
      console.error('Invalid response from category request:', requestResponse)
      throw new Error('درخواست دسته‌بندی ایجاد نشد. لطفاً دوباره تلاش کنید.')
    }
  } catch (error: any) {
    console.error('Error submitting category request:', error)
    const { formatErrorMessage } = await import('~/utils/apiErrors')
    errorMessage.value = formatErrorMessage(error) || 'خطا در ایجاد درخواست دسته‌بندی'
    showErrorSnackbar.value = true
  } finally {
    requestingCategory.value = false
  }
}

const cancelCategoryRequest = () => {
  categoryRequest.value.name = ''
  showCategoryRequest.value = false
  subcategorySearch.value = ''
}

const saveProductWithRequest = async (categoryRequestId: number) => {
  descriptionTouched.value = true

  // Validate form fields
  const formInstance = formRef.value
  if (formInstance) {
    const { valid } = await formInstance.validate()
    if (!valid) {
      errorMessage.value = 'لطفاً تمام فیلدهای الزامی را پر کنید'
      showErrorSnackbar.value = true
      return
    }
  }

  // Validate description
  if (!descriptionValid.value) {
    errorMessage.value = 'توضیحات محصول الزامی است'
    showErrorSnackbar.value = true
    return
  }

  // Validate availability status and related fields
  const missingFields: string[] = []
  
  if (!product.value.availability_status) {
    missingFields.push('وضعیت موجودی')
  } else {
    if (product.value.availability_status === 'in_stock' && !product.value.condition) {
      missingFields.push('وضعیت محصول (نو یا دست دوم)')
    }
    if (product.value.availability_status === 'made_to_order' && !product.value.lead_time_days) {
      missingFields.push('زمان تحویل')
    }
  }

  // Validate features (if any are partially filled)
  const incompleteFeatures = productFeatures.value.filter(f => (f.name && !f.value) || (!f.name && f.value))
  if (incompleteFeatures.length > 0) {
    missingFields.push('ویژگی‌های کلیدی (نام و مقدار باید هر دو پر شوند)')
  }

  if (missingFields.length > 0) {
    errorMessage.value = `لطفاً فیلدهای زیر را پر کنید:\n• ${missingFields.join('\n• ')}`
    showErrorSnackbar.value = true
    return
  }

  submitting.value = true

  try {
    const formData = new FormData()

    Object.keys(product.value).forEach(key => {
      if (['subcategory'].includes(key)) return
      const value = product.value[key as keyof typeof product.value]
      if (value !== null && value !== undefined && value !== '') {
        formData.append(key, String(value))
      }
    })

    // Don't require subcategory if we have a category request
    // Handle subcategories (ManyToMany field - needs to be integer)
    if (product.value.subcategory) {
      const subcategoryId = Number(product.value.subcategory)
      if (!isNaN(subcategoryId)) {
        formData.append('subcategories', String(subcategoryId))
      }
    }

    if (selectedCategory.value) {
      formData.append('primary_category', String(selectedCategory.value))
    }

    // Add features
    const validFeatures = productFeatures.value.filter(f => f.name && f.value)
    if (validFeatures.length > 0) {
      formData.append('features', JSON.stringify(validFeatures))
    }

    // Link to category request
    formData.append('category_request_id', String(categoryRequestId))

    const response: any = await productApi.createProduct(formData)
    successMessage.value = `محصول "${(response as any)?.name || 'محصول'}" با موفقیت ایجاد شد! درخواست دسته‌بندی "${categoryRequest.value.name}" در حال بررسی است.`
    showSuccessSnackbar.value = true
    markOnce('product-save-button')
    const awarded = await awardProductSection()
    if (awarded > 0) {
      successMessage.value += ` (+${awarded} امتیاز)`
      showToast({
        message: `+${awarded} امتیاز برای تکمیل محصول`,
        color: 'success'
      })
    }
    
    // Reset category request form
    categoryRequest.value.name = ''
    showCategoryRequest.value = false

    setTimeout(() => {
      emit('saved', response)
    }, 1500)
  } catch (error: any) {
    console.error('Error saving product:', error)
    const { formatErrorMessage } = await import('~/utils/apiErrors')
    let formattedError = formatErrorMessage(error)
    
    // If error contains field-specific errors, format them nicely
    if (error?.response?.data) {
      const errorData = error.response.data
      const fieldErrors: string[] = []
      
      // Check for field-specific errors
      Object.keys(errorData).forEach(field => {
        if (Array.isArray(errorData[field])) {
          fieldErrors.push(`${getFieldLabel(field)}: ${errorData[field].join(', ')}`)
        } else if (typeof errorData[field] === 'string') {
          fieldErrors.push(`${getFieldLabel(field)}: ${errorData[field]}`)
        } else if (typeof errorData[field] === 'object') {
          // Handle nested errors
          Object.keys(errorData[field]).forEach(subField => {
            if (Array.isArray(errorData[field][subField])) {
              fieldErrors.push(`${getFieldLabel(field)} - ${getFieldLabel(subField)}: ${errorData[field][subField].join(', ')}`)
            }
          })
        }
      })
      
      if (fieldErrors.length > 0) {
        formattedError = `خطا در ذخیره محصول:\n• ${fieldErrors.join('\n• ')}`
      }
    }
    
    errorMessage.value = formattedError
    showErrorSnackbar.value = true
  } finally {
    submitting.value = false
  }
}

const saveProduct = async () => {
  descriptionTouched.value = true

  const formInstance = formRef.value
  if (!formInstance) return

  // Validate form fields
  const { valid } = await formInstance.validate()
  if (!valid) {
    errorMessage.value = 'لطفاً تمام فیلدهای الزامی را پر کنید'
    showErrorSnackbar.value = true
    return
  }

  // Validate description
  if (!descriptionValid.value) {
    errorMessage.value = 'توضیحات محصول الزامی است'
    showErrorSnackbar.value = true
    return
  }

  // Validate availability status and related fields
  const missingFields: string[] = []
  
  if (!product.value.availability_status) {
    missingFields.push('وضعیت موجودی')
  } else {
    if (product.value.availability_status === 'in_stock' && !product.value.condition) {
      missingFields.push('وضعیت محصول (نو یا دست دوم)')
    }
    if (product.value.availability_status === 'made_to_order' && !product.value.lead_time_days) {
      missingFields.push('زمان تحویل')
    }
  }

  // Validate features (if any are partially filled)
  const incompleteFeatures = productFeatures.value.filter(f => (f.name && !f.value) || (!f.name && f.value))
  if (incompleteFeatures.length > 0) {
    missingFields.push('ویژگی‌های کلیدی (نام و مقدار باید هر دو پر شوند)')
  }

  if (missingFields.length > 0) {
    errorMessage.value = `لطفاً فیلدهای زیر را پر کنید:\n• ${missingFields.join('\n• ')}`
    showErrorSnackbar.value = true
    return
  }

  submitting.value = true

  try {
    const formData = new FormData()

    Object.keys(product.value).forEach(key => {
      if (['subcategory'].includes(key)) return
      const value = product.value[key as keyof typeof product.value]
      if (value !== null && value !== undefined && value !== '') {
        formData.append(key, String(value))
      }
    })

    // Handle subcategories (ManyToMany field - needs to be integer)
    if (product.value.subcategory) {
      const subcategoryId = Number(product.value.subcategory)
      if (!isNaN(subcategoryId)) {
        formData.append('subcategories', String(subcategoryId))
      }
    }

    if (selectedCategory.value) {
      formData.append('primary_category', String(selectedCategory.value))
    }

    // Add features
    const validFeatures = productFeatures.value.filter(f => f.name && f.value)
    if (validFeatures.length > 0) {
      formData.append('features', JSON.stringify(validFeatures))
    }

    // If category request was submitted, link it to the product
    // This will be handled in the backend when product is created

    uploadedImages.value.forEach(image => {
      if (image.file) {
        formData.append('images', image.file)
      }
    })

    let response: any
    if (props.editMode && props.productData?.id) {
      response = await productApi.updateProduct(props.productData.id, formData)
      successMessage.value = `محصول "${response?.name || 'محصول'}" با موفقیت به‌روزرسانی شد!`
    } else {
      response = await productApi.createProduct(formData)
      successMessage.value = `محصول "${response?.name || 'محصول'}" با موفقیت ایجاد شد!`
    }

    showSuccessSnackbar.value = true
    markOnce('product-save-button')
    const awarded = await awardProductSection()
    if (awarded > 0) {
      successMessage.value += ` (+${awarded} امتیاز)`
      showToast({
        message: `+${awarded} امتیاز برای تکمیل محصول`,
        color: 'success'
      })
    }

    setTimeout(() => {
      emit('saved', response)
    }, 1500)
  } catch (error: any) {
    console.error('Error saving product:', error)
    
    // Import and use the error formatting utility
    const { formatErrorMessage } = await import('~/utils/apiErrors')
    let formattedError = formatErrorMessage(error)
    
    // If error contains field-specific errors, format them nicely
    if (error?.response?.data) {
      const errorData = error.response.data
      const fieldErrors: string[] = []
      
      // Check for field-specific errors
      Object.keys(errorData).forEach(field => {
        const fieldValue = errorData[field as keyof typeof errorData]
        if (Array.isArray(fieldValue)) {
          fieldErrors.push(`${getFieldLabel(field)}: ${fieldValue.join(', ')}`)
        } else if (typeof fieldValue === 'string') {
          fieldErrors.push(`${getFieldLabel(field)}: ${fieldValue}`)
        } else if (typeof fieldValue === 'object' && fieldValue !== null) {
          // Handle nested errors
          Object.keys(fieldValue).forEach(subField => {
            const subFieldValue = (fieldValue as Record<string, any>)[subField]
            if (Array.isArray(subFieldValue)) {
              fieldErrors.push(`${getFieldLabel(field)} - ${getFieldLabel(subField)}: ${subFieldValue.join(', ')}`)
            }
          })
        }
      })
      
      if (fieldErrors.length > 0) {
        formattedError = `خطا در ذخیره محصول:\n• ${fieldErrors.join('\n• ')}`
      }
    }
    
    errorMessage.value = formattedError
    showErrorSnackbar.value = true
  } finally {
    submitting.value = false
  }
}

const getFieldLabel = (field: string): string => {
  const labels: Record<string, string> = {
    'name': 'نام محصول',
    'description': 'توضیحات',
    'price': 'قیمت',
    'stock': 'موجودی',
    'availability_status': 'وضعیت موجودی',
    'condition': 'وضعیت محصول',
    'origin': 'مبدا',
    'lead_time_days': 'زمان تحویل',
    'features': 'ویژگی‌های کلیدی',
    'subcategories': 'دسته‌بندی',
    'primary_category': 'دسته‌بندی اصلی',
    'images': 'تصاویر'
  }
  return labels[field] || field
}

onMounted(async () => {
  await fetchFormData()

  // If editing, populate form with existing data
  if (props.editMode && props.productData) {
    product.value = { ...props.productData }
    
    // Populate features
    if (props.productData.features && Array.isArray(props.productData.features)) {
      productFeatures.value = props.productData.features.map((f: any) => ({
        name: f.name || '',
        value: f.value || ''
      }))
      if (productFeatures.value.length === 0) {
        productFeatures.value = [{ name: '', value: '' }]
      }
    }
    
    // Set selected values for dropdowns
    // Handle subcategory - could be from subcategory field or subcategories array
    let subcategoryId: number | null = null
    if (props.productData.subcategory) {
      subcategoryId = typeof props.productData.subcategory === 'number' 
        ? props.productData.subcategory 
        : Number(props.productData.subcategory)
    } else if (props.productData.subcategories && Array.isArray(props.productData.subcategories) && props.productData.subcategories.length > 0) {
      // If subcategories array exists, use the first one
      const firstSub = props.productData.subcategories[0]
      subcategoryId = typeof firstSub === 'object' ? firstSub.id : (typeof firstSub === 'number' ? firstSub : Number(firstSub))
    }
    
    if (subcategoryId && !isNaN(subcategoryId)) {
      product.value.subcategory = subcategoryId as number
      // Find subcategory in searchable list
      const sub = searchableSubcategories.value.find(s => s.id === subcategoryId)
      if (sub) {
        selectedCategory.value = sub.category
        selectedDepartment.value = sub.department
      } else {
        // Fallback: find in subcategories array
        const subcategory = subcategories.value.find(s => s.id === subcategoryId)
        if (subcategory) {
          const categoryId = typeof subcategory.category === 'object' ? subcategory.category?.id : subcategory.category
          selectedCategory.value = categoryId
          const category = categories.value.find(c => c.id === categoryId)
          if (category) {
            const deptId = typeof category.department === 'object' ? category.department?.id : category.department
            selectedDepartment.value = deptId
          }
        }
      }
    }
  }
})
</script>

<style scoped>
.image-upload-area {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #f5f5f5;
}

.image-upload-area:hover,
.image-upload-area.drag-over {
  border-color: #1976d2;
  background: #e3f2fd;
}

.image-preview-card {
  position: relative;
  overflow: hidden;
}

.remove-image-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 2;
}

.main-image-badge {
  position: absolute;
  bottom: 8px;
  left: 8px;
  z-index: 2;
}

.sticky-card {
  position: sticky;
  top: 80px;
  z-index: 1;
}

.help-list {
  list-style-position: inside;
  padding-right: 0;
}

.help-list li {
  margin-bottom: 8px;
}

/* Action buttons container styling */
.action-buttons-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

/* Force button visibility and proper alignment */
.save-button,
.cancel-button {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  min-height: 56px !important;
  position: relative !important;
  z-index: 10 !important;
  width: 100% !important;
}

.save-button .v-btn__content,
.cancel-button .v-btn__content {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-weight: 500 !important;
  text-align: center !important;
  width: 100% !important;
}

/* Ensure button text and icon are properly aligned */
.save-button .v-btn__prepend,
.cancel-button .v-btn__prepend {
  margin-inline-end: 8px !important;
}

.save-button .v-btn__content,
.cancel-button .v-btn__content {
  flex: 1 1 auto !important;
  justify-content: center !important;
  text-align: center !important;
}
</style>



