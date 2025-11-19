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

              <div class="mb-4">
                <label class="text-body-2 mb-2 d-block font-weight-medium">
                  <v-icon size="small" class="ml-1">mdi-text</v-icon>
                  توضیحات <span class="text-error">*</span>
                </label>
                <LazyTiptapEditor v-model="product.description" />
                <div v-if="!descriptionValid && descriptionTouched" class="text-error text-caption mt-1">
                  توضیحات الزامی است
                </div>
              </div>

              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="product.price"
                    label="قیمت (تومان)"
                    prepend-inner-icon="mdi-currency-usd"
                    variant="outlined"
                    type="number"
                    step="1"
                    min="0"
                    :rules="[v => v >= 0 || 'قیمت باید مثبت باشد']"
                    required
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
            </v-card-text>
          </v-card>

          <!-- Category Selection -->
          <v-card elevation="2" rounded="lg" class="mb-4">
            <v-card-title class="text-h6 font-weight-bold bg-secondary pa-4">
              <v-icon class="ml-2">mdi-folder-outline</v-icon>
              دسته‌بندی
            </v-card-title>
            <v-card-text class="pa-4">
              <v-select
                v-model="selectedDepartment"
                :items="departments"
                item-title="name"
                item-value="id"
                label="دپارتمان"
                prepend-inner-icon="mdi-sitemap"
                variant="outlined"
                @update:model-value="onDepartmentChange"
                class="mb-2"
              ></v-select>

              <v-select
                v-model="selectedCategory"
                :items="filteredCategories"
                item-title="name"
                item-value="id"
                label="دسته‌بندی"
                prepend-inner-icon="mdi-folder"
                variant="outlined"
                :disabled="!selectedDepartment"
                @update:model-value="onCategoryChange"
                class="mb-2"
              ></v-select>

              <v-select
                v-model="product.subcategory"
                :items="filteredSubcategories"
                item-title="name"
                item-value="id"
                label="زیردسته"
                prepend-inner-icon="mdi-folder-open"
                variant="outlined"
                :disabled="!selectedCategory"
                :rules="[v => !!v || 'زیردسته الزامی است']"
                required
              ></v-select>

              <!-- Breadcrumb Display -->
              <v-alert v-if="product.subcategory" type="info" variant="tonal" class="mt-3">
                <strong>مسیر انتخاب شده:</strong>
                <div class="mt-1">{{ getCategoryBreadcrumb() }}</div>
              </v-alert>
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
          <FormQualityScore
            class="mb-4 sticky-card"
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

              <v-divider class="my-4"></v-divider>

              <!-- Action Buttons -->
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
      :timeout="5000"
      location="top"
    >
      {{ errorMessage }}
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

const formRef = ref<any>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const product = ref({
  name: '',
  slug: '',
  description: '',
  price: 0,
  stock: 0,
  subcategory: null,
  is_active: true,
  is_featured: false
})

const departments = ref<any[]>([])
const categories = ref<any[]>([])
const subcategories = ref<any[]>([])
const filteredCategories = ref<any[]>([])
const filteredSubcategories = ref<any[]>([])
const selectedDepartment = ref<number | null>(null)
const selectedCategory = ref<number | null>(null)

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

const onDepartmentChange = () => {
  if (selectedDepartment.value) {
    filteredCategories.value = categories.value.filter(
      cat => cat.department === selectedDepartment.value
    )
    selectedCategory.value = null
    product.value.subcategory = null
    filteredSubcategories.value = []
  }
}

const onCategoryChange = () => {
  if (selectedCategory.value) {
    filteredSubcategories.value = subcategories.value.filter(
      sub => sub.category === selectedCategory.value
    )
    product.value.subcategory = null
  }
}

const getCategoryBreadcrumb = () => {
  if (!product.value.subcategory) return ''
  
  const subcategory = subcategories.value.find(s => s.id === product.value.subcategory)
  if (!subcategory) return ''
  
  const category = categories.value.find(c => c.id === subcategory.category)
  const department = departments.value.find(d => d.id === category?.department)
  
  const parts = []
  if (department) parts.push(department.name)
  if (category) parts.push(category.name)
  if (subcategory) parts.push(subcategory.name)
  
  return parts.join(' ← ')
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
  } catch (error) {
    console.error('Error fetching form data:', error)
  }
}

const saveProduct = async () => {
  descriptionTouched.value = true

  const formInstance = formRef.value
  if (!formInstance) return

  const { valid } = await formInstance.validate()
  if (!valid) return

  if (!descriptionValid.value) return

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

    if (product.value.subcategory) {
      formData.append('subcategories', String(product.value.subcategory))
    }

    if (selectedCategory.value) {
      formData.append('primary_category', String(selectedCategory.value))
    }

    uploadedImages.value.forEach(image => {
      if (image.file) {
        formData.append('images', image.file)
      }
    })

    let response
    if (props.editMode && props.productData?.id) {
      response = await productApi.updateProduct(props.productData.id, formData)
      successMessage.value = `محصول "${response.name}" با موفقیت به‌روزرسانی شد!`
    } else {
      response = await productApi.createProduct(formData)
      successMessage.value = `محصول "${response.name}" با موفقیت ایجاد شد!`
    }

    showSuccessSnackbar.value = true

    setTimeout(() => {
      emit('saved', response)
    }, 1500)
  } catch (error: any) {
    console.error('Error saving product:', error)
    errorMessage.value = error.data?.detail || 'خطا در ذخیره محصول'
    showErrorSnackbar.value = true
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  await fetchFormData()

  // If editing, populate form with existing data
  if (props.editMode && props.productData) {
    product.value = { ...props.productData }
    
    // Set selected values for dropdowns
    if (props.productData.subcategory) {
      const subcategory = subcategories.value.find(s => s.id === props.productData.subcategory)
      if (subcategory) {
        selectedCategory.value = subcategory.category
        const category = categories.value.find(c => c.id === subcategory.category)
        if (category) {
          selectedDepartment.value = category.department
          onDepartmentChange()
          onCategoryChange()
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
}

.help-list {
  list-style-position: inside;
  padding-right: 0;
}

.help-list li {
  margin-bottom: 8px;
}
</style>



