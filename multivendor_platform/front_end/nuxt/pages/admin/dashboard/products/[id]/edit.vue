<template>
  <div dir="rtl" class="product-form-container">
    <v-container fluid class="pa-4">
      <v-breadcrumbs :items="breadcrumbItems" class="px-2 py-1" divider="/" dir="rtl">
        <template v-slot:prepend>
          <v-icon size="small" class="mr-2">mdi-home</v-icon>
        </template>
      </v-breadcrumbs>

      <h1 class="text-h4 text-sm-h3 font-weight-bold mb-4 mb-sm-6">
        {{ t('editProduct') }}
      </h1>

      <v-row v-if="loading" justify="center" class="my-16">
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <p class="text-h6 mt-4">{{ t('loading') }}</p>
        </v-col>
      </v-row>

      <v-form v-if="!loading" @submit.prevent="saveProduct" ref="formRef">
        <v-alert v-if="error" type="error" variant="tonal" prominent closable class="mb-4" @click:close="clearError">
          {{ error }}
        </v-alert>

        <v-row>
          <v-col cols="12" lg="8">
            <!-- Basic Information -->
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
              <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-primary pa-4 pa-sm-5">
                <v-icon class="mr-2">mdi-information</v-icon>
                اطلاعات پایه
              </v-card-title>
              <v-card-text class="pa-4 pa-sm-5 pa-md-6">
                <v-text-field
                  v-model="product.name"
                  :label="t('productName')"
                  prepend-inner-icon="mdi-tag"
                  variant="outlined"
                  rounded="lg"
                  :rules="[v => !!v || 'نام محصول الزامی است']"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="product.slug"
                  label="Slug (نامک)"
                  prepend-inner-icon="mdi-link-variant"
                  variant="outlined"
                  rounded="lg"
                ></v-text-field>

                <div class="description-editor-wrapper">
                  <label class="text-body-2 mb-2 d-block">
                    <v-icon size="small" class="mr-1">mdi-text</v-icon>
                    {{ t('description') }} <span class="text-error">*</span>
                  </label>
                  <LazyTiptapEditor v-model="product.description" class="description-editor" />
                  <div v-if="!descriptionValid && descriptionTouched" class="text-error text-caption mt-1">
                    توضیحات الزامی است
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="formattedPrice"
                      :label="t('price') + ' (تومان)'"
                      prepend-inner-icon="mdi-currency-usd"
                      variant="outlined"
                      rounded="lg"
                      type="text"
                      :rules="[v => {
                        const num = parsePriceValue(v)
                        return num >= 0 || 'قیمت باید مثبت باشد'
                      }]"
                      required
                      @input="onPriceInput"
                      @focus="onPriceFocus"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model.number="product.stock"
                      :label="t('stock')"
                      prepend-inner-icon="mdi-package-variant"
                      variant="outlined"
                      rounded="lg"
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
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
              <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-secondary pa-4 pa-sm-5">
                <v-icon class="mr-2">mdi-shape</v-icon>
                دسته‌بندی محصول
              </v-card-title>
              <v-card-text class="pa-4 pa-sm-5 pa-md-6">
                <v-select
                  v-model="selectedDepartment"
                  :items="departments"
                  item-title="name"
                  item-value="id"
                  label="بخش (برای فیلتر)"
                  prepend-inner-icon="mdi-filter"
                  variant="outlined"
                  rounded="lg"
                  clearable
                  class="mb-4"
                  @update:model-value="onDepartmentChange"
                ></v-select>

                <v-select
                  v-model="selectedCategory"
                  :items="filteredCategories"
                  item-title="name"
                  item-value="id"
                  label="دسته‌بندی (برای فیلتر)"
                  prepend-inner-icon="mdi-filter"
                  variant="outlined"
                  rounded="lg"
                  clearable
                  class="mb-4"
                  :disabled="!selectedDepartment && categories.length === 0"
                  @update:model-value="onCategoryChange"
                ></v-select>

                <v-select
                  v-model="product.subcategory"
                  :items="filteredSubcategories"
                  item-title="name"
                  item-value="id"
                  label="زیردسته *"
                  prepend-inner-icon="mdi-check-circle"
                  variant="outlined"
                  rounded="lg"
                  :rules="[
                    v => !!v || 'انتخاب زیردسته الزامی است',
                    v => !v || !isNaN(Number(v)) || 'زیردسته انتخاب شده معتبر نیست'
                  ]"
                  required
                  @update:model-value="onSubcategoryChange"
                ></v-select>
              </v-card-text>
            </v-card>

            <!-- Product Images -->
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
              <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-accent pa-4 pa-sm-5">
                <v-icon class="mr-2">mdi-image-multiple</v-icon>
                تصاویر محصول (حداکثر 20 تصویر)
              </v-card-title>
              <v-card-text class="pa-3 pa-sm-4 pa-md-6">
                <div
                  class="image-upload-zone"
                  :class="{ 'drag-over': isDragOver, 'has-images': uploadedImages.length > 0 }"
                  @drop="handleDrop"
                  @dragover.prevent="isDragOver = true"
                  @dragleave="isDragOver = false"
                  @click="triggerFileInput"
                >
                  <v-row v-if="uploadedImages.length > 0" dense class="pa-1 pa-sm-2">
                    <v-col v-for="(image, index) in uploadedImages" :key="index" cols="6" sm="6" lg="3">
                      <v-card elevation="2" rounded="lg" class="image-item" :class="{ 'primary-image': index === 0 }">
                        <v-img :src="image.preview" aspect-ratio="1" cover>
                          <div class="image-overlay">
                            <v-btn icon="mdi-delete" color="error" size="small" @click.stop="removeImage(index)"></v-btn>
                          </div>
                          <v-chip v-if="index === 0" color="success" size="small" class="primary-badge" prepend-icon="mdi-star">
                            اصلی
                          </v-chip>
                        </v-img>
                      </v-card>
                    </v-col>
                    <v-col v-if="uploadedImages.length < 20" cols="6" sm="6" lg="3">
                      <v-card elevation="2" rounded="lg" class="add-more-card" @click.stop="triggerFileInput">
                        <div class="d-flex flex-column align-center justify-center fill-height">
                          <v-icon size="48" color="primary">mdi-plus</v-icon>
                          <span class="text-body-2 mt-2">افزودن بیشتر</span>
                        </div>
                      </v-card>
                    </v-col>
                  </v-row>
                  <div v-else class="text-center pa-6 pa-sm-8">
                    <v-icon size="64" color="primary">mdi-cloud-upload</v-icon>
                    <p class="text-subtitle-1 mt-3 mt-sm-4">تصاویر را اینجا بکشید یا کلیک کنید</p>
                  </div>
                </div>

                <input ref="fileInput" type="file" multiple @change="handleFileSelect" accept="image/*" style="display: none" />

                <v-alert v-if="imageError" type="error" variant="tonal" density="compact" class="mt-4">
                  {{ imageError }}
                </v-alert>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Sidebar -->
          <v-col cols="12" lg="4">
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6 sticky-card">
              <v-card-title class="text-subtitle-1 text-sm-h6 font-weight-bold pa-4 pa-sm-5">
                <v-icon class="mr-2">mdi-cog</v-icon>
                تنظیمات
              </v-card-title>
              <v-card-text class="pa-3 pa-sm-4">
                <v-switch v-model="product.is_active" :label="t('productIsActive')" color="success" inset hide-details></v-switch>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions class="pa-3 pa-sm-4 flex-column ga-2 ga-sm-3">
                <v-btn
                  type="submit"
                  color="primary"
                  size="x-large"
                  prepend-icon="mdi-content-save"
                  block
                  variant="elevated"
                  rounded="lg"
                  :loading="submitting"
                  :disabled="submitting"
                >
                  {{ submitting ? t('saving') : t('saveProduct') }}
                </v-btn>
                <v-btn color="secondary" size="large" prepend-icon="mdi-close" block variant="outlined" rounded="lg" to="/admin/dashboard?view=products">
                  {{ t('cancel') }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-form>

      <v-snackbar v-model="showSuccessSnackbar" :timeout="3000" color="success" location="top" rounded="pill">
        <div class="d-flex align-center">
          <v-icon class="mr-2">mdi-check-circle</v-icon>
          <span>{{ successMessage }}</span>
        </div>
      </v-snackbar>
    </v-container>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const departmentStore = useDepartmentStore()
const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()

const productId = computed(() => route.params.id as string)
const formRef = ref()
const submitting = ref(false)
const uploadedImages = ref<any[]>([])
const isDragOver = ref(false)
const imageError = ref('')
const fileInput = ref<HTMLInputElement | null>(null)
const descriptionTouched = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')

const departments = ref<any[]>([])
const categories = ref<any[]>([])
const subcategories = ref<any[]>([])
const selectedDepartment = ref<number | string | null>(null)
const selectedCategory = ref<number | string | null>(null)
const filteredCategories = ref<any[]>([])
const filteredSubcategories = ref<any[]>([])

const product = ref({
  name: '',
  slug: '',
  subcategory: '',
  description: '',
  price: 0,
  stock: 0,
  is_active: true,
  meta_title: '',
  meta_description: '',
  image_alt_text: '',
  canonical_url: ''
})

const loading = computed(() => productStore.loading)
const error = computed(() => productStore.error)
const t = computed(() => productStore.t)

const descriptionValid = computed(() => {
  if (!product.value.description) return false
  const description = product.value.description.trim()
  if (!description || description === '<p></p>' || description === '<p><br></p>') {
    return false
  }
  if (process.client) {
    try {
      const tempDiv = document.createElement('div')
      tempDiv.innerHTML = description
      const textContent = tempDiv.textContent || tempDiv.innerText || ''
      return textContent.trim().length > 0
    } catch (e) {
      const textOnly = description.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
      return textOnly.length > 0
    }
  }
  const textOnly = description.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
  return textOnly.length > 0
})

watch(() => product.value.description, () => {
  descriptionTouched.value = true
})

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

const breadcrumbItems = computed(() => [
  { title: t.value('home'), to: '/', disabled: false },
  { title: 'پنل مدیریت', to: '/admin/dashboard', disabled: false },
  { title: t.value('editProduct'), disabled: true }
])

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
    filteredCategories.value = categories.value.filter(cat =>
      cat.departments && cat.departments.some((d: any) => d.id === parseInt(String(selectedDepartment.value)))
    )
  } else {
    filteredCategories.value = categories.value
  }

  if (selectedCategory.value && !filteredCategories.value.find(c => c.id === parseInt(String(selectedCategory.value)))) {
    selectedCategory.value = null
  }

  filterSubcategories()
}

const onCategoryChange = () => {
  filterSubcategories()
}

const onSubcategoryChange = (value: any) => {
  // Ensure the value is always a number (ID)
  if (value !== null && value !== undefined && value !== '') {
    const numValue = Number(value)
    if (!isNaN(numValue)) {
      product.value.subcategory = numValue
    } else {
      // Invalid value, reset it
      product.value.subcategory = ''
    }
  }
}

const filterSubcategories = () => {
  let filtered = subcategories.value

  if (selectedDepartment.value) {
    filtered = filtered.filter(sub =>
      sub.departments && sub.departments.some((d: any) => d.id === parseInt(String(selectedDepartment.value)))
    )
  }

  if (selectedCategory.value) {
    filtered = filtered.filter(sub =>
      sub.categories && sub.categories.some((c: any) => c.id === parseInt(String(selectedCategory.value)))
    )
  }

  filteredSubcategories.value = filtered

  if (product.value.subcategory && !filtered.find(s => s.id === parseInt(String(product.value.subcategory)))) {
    product.value.subcategory = ''
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
  } catch (error) {
    console.error('Error fetching form data:', error)
  }
}

const loadProduct = async () => {
  try {
    await productStore.fetchProduct(productId.value)

    if (productStore.currentProduct) {
      const p = productStore.currentProduct
      product.value = {
        name: p.name || '',
        slug: p.slug || '',
        subcategory: '',
        description: p.description || '',
        price: p.price || 0,
        stock: p.stock || 0,
        is_active: p.is_active !== undefined ? p.is_active : true,
        meta_title: p.meta_title || '',
        meta_description: p.meta_description || '',
        image_alt_text: p.image_alt_text || '',
        canonical_url: p.canonical_url || ''
      }

      // Handle subcategories
      let subcategoryId = null
      if (p.subcategories && Array.isArray(p.subcategories) && p.subcategories.length > 0) {
        subcategoryId = p.subcategories[0]
      } else if (p.subcategory) {
        subcategoryId = p.subcategory
      }

      if (subcategoryId) {
        product.value.subcategory = subcategoryId
        const sub = subcategories.value.find(s => s.id === parseInt(String(subcategoryId)))
        if (sub) {
          if (sub.departments && sub.departments.length > 0) {
            selectedDepartment.value = sub.departments[0].id
            onDepartmentChange()
          }
          if (sub.categories && sub.categories.length > 0) {
            selectedCategory.value = sub.categories[0].id
            onCategoryChange()
          }
        }
      }

      if (p.images && p.images.length > 0) {
        uploadedImages.value = p.images.map((img: any) => ({
          file: null,
          preview: img.image_url || img.image,
          id: img.id,
          is_primary: img.is_primary
        }))
      }
    }
  } catch (error) {
    console.error('Error loading product:', error)
  }
}

const saveProduct = async () => {
  descriptionTouched.value = true

  const formInstance = formRef.value
  if (!formInstance) {
    return
  }

  const { valid } = await formInstance.validate()
  if (!valid) return

  if (!descriptionValid.value) {
    return
  }

  submitting.value = true

  try {
    const formData = new FormData()

    Object.keys(product.value).forEach(key => {
      if (['subcategory'].includes(key)) {
        return
      }
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
      } else {
        throw new Error('زیردسته انتخاب شده معتبر نیست')
      }
    }

    if (selectedCategory.value) {
      formData.append('primary_category', String(selectedCategory.value))
    }

    uploadedImages.value.forEach(image => {
      if (image.file) {
        formData.append('images', image.file)
      }
    })

    const response = await productStore.updateProduct(productId.value, formData)
    successMessage.value = `محصول "${response.name}" با موفقیت به‌روزرسانی شد!`
    showSuccessSnackbar.value = true

    setTimeout(() => {
      router.push('/admin/dashboard?view=products')
    }, 1500)
  } catch (error: any) {
    console.error('Error saving product:', error)
    alert('خطا در ذخیره محصول: ' + (error?.data?.detail || error?.message || 'خطای نامشخص'))
  } finally {
    submitting.value = false
  }
}

const clearError = () => {
  productStore.error = null
}

onMounted(async () => {
  await fetchFormData()
  await loadProduct()
})
</script>

<style scoped>
.image-upload-zone {
  border: 2px dashed rgb(var(--v-theme-primary));
  border-radius: 16px;
  min-height: 200px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: rgba(var(--v-theme-surface), 1);
}

.image-upload-zone:hover {
  border-color: rgb(var(--v-theme-secondary));
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.image-upload-zone.drag-over {
  border-color: rgb(var(--v-theme-success));
  background-color: rgba(var(--v-theme-success), 0.1);
  transform: scale(1.02);
}

.image-upload-zone.has-images {
  min-height: auto;
  border-style: solid;
}

.image-item {
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.image-item:hover {
  transform: scale(1.05);
}

.image-item.primary-image {
  border: 3px solid rgb(var(--v-theme-success));
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-item:hover .image-overlay {
  opacity: 1;
}

.primary-badge {
  position: absolute;
  top: 8px;
  left: 8px;
}

.add-more-card {
  aspect-ratio: 1;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px dashed rgb(var(--v-theme-primary));
}

.add-more-card:hover {
  border-color: rgb(var(--v-theme-secondary));
  background-color: rgba(var(--v-theme-primary), 0.05);
  transform: scale(1.05);
}

.sticky-card {
  position: sticky;
  top: 80px;
}

.description-editor-wrapper {
  margin-bottom: 16px;
}

.description-editor-wrapper label {
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.description-editor {
  margin-top: 8px;
}
</style>

