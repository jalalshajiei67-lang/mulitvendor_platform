<template>
  <div dir="rtl" class="product-form-container">
    <v-container fluid class="pa-4">
      <v-breadcrumbs :items="breadcrumbItems" class="px-2 py-1" divider="/" dir="rtl">
        <template v-slot:prepend>
          <v-icon size="small" class="mr-2">mdi-home</v-icon>
        </template>
      </v-breadcrumbs>

      <h1 class="text-h4 text-sm-h3 font-weight-bold mb-4 mb-sm-6">
        {{ t('addNewProduct') }}
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
                  hint="در صورت خالی بودن، به صورت خودکار از نام محصول ایجاد می‌شود"
                  persistent-hint
                ></v-text-field>

                <div class="description-editor-wrapper">
                  <label class="text-body-2 mb-2 d-block">
                    <v-icon size="small" class="mr-1">mdi-text</v-icon>
                    {{ t('description') }} <span class="text-error">*</span>
                  </label>
                  <TiptapEditor v-model="product.description" class="description-editor" />
                  <div v-if="!descriptionValid && descriptionTouched" class="text-error text-caption mt-1">
                    توضیحات الزامی است
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model.number="product.price"
                      :label="t('price') + ' (تومان)'"
                      prepend-inner-icon="mdi-currency-usd"
                      variant="outlined"
                      rounded="lg"
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
                  :rules="[v => !!v || 'انتخاب زیردسته الزامی است']"
                  required
                ></v-select>

                <v-alert v-if="product.subcategory && selectedSubcategoryObject" type="success" variant="tonal" class="mt-4">
                  <v-icon class="mr-2">mdi-route</v-icon>
                  <strong>مسیر انتخاب شده:</strong>
                  <div class="mt-2 font-weight-bold">{{ getSelectedFullPath() }}</div>
                </v-alert>
              </v-card-text>
            </v-card>

            <!-- SEO Settings -->
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
              <v-expansion-panels v-model="seoPanel" variant="accordion" multiple>
                <v-expansion-panel>
                  <v-expansion-panel-title class="text-h6 text-sm-h5 font-weight-bold">
                    <v-icon class="mr-2">mdi-search-web</v-icon>
                    تنظیمات SEO
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-card-text class="pa-4 pa-sm-5 pa-md-6">
                      <v-text-field
                        v-model="product.meta_title"
                        label="عنوان متا (Meta Title)"
                        variant="outlined"
                        rounded="lg"
                        :counter="60"
                        maxlength="60"
                        class="mb-4"
                      ></v-text-field>
                      <v-textarea
                        v-model="product.meta_description"
                        label="توضیحات متا (Meta Description)"
                        variant="outlined"
                        rounded="lg"
                        rows="3"
                        :counter="160"
                        maxlength="160"
                        class="mb-4"
                      ></v-textarea>
                      <v-text-field
                        v-model="product.image_alt_text"
                        label="متن جایگزین تصویر"
                        variant="outlined"
                        rounded="lg"
                        class="mb-4"
                      ></v-text-field>
                      <v-text-field
                        v-model="product.canonical_url"
                        label="آدرس کانونیکال"
                        variant="outlined"
                        rounded="lg"
                        type="url"
                        class="mb-4"
                      ></v-text-field>
                    </v-card-text>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
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
                  <div v-if="uploadedImages.length === 0" class="text-center pa-6 pa-sm-8">
                    <v-icon size="64" color="primary">mdi-cloud-upload</v-icon>
                    <p class="text-subtitle-1 mt-3 mt-sm-4">تصاویر را اینجا بکشید یا کلیک کنید</p>
                  </div>

                  <v-row v-else dense class="pa-1 pa-sm-2">
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
const authStore = useAuthStore()
const productStore = useProductStore()
const departmentStore = useDepartmentStore()
const categoryStore = useCategoryStore()
const subcategoryStore = useSubcategoryStore()
const { mdAndDown } = useDisplay()

const formRef = ref()
const submitting = ref(false)
const uploadedImages = ref<any[]>([])
const isDragOver = ref(false)
const imageError = ref('')
const fileInput = ref<HTMLInputElement | null>(null)
const descriptionTouched = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')
const seoPanel = ref<number[]>([])

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

const selectedSubcategoryObject = computed(() => {
  if (!product.value.subcategory) return null
  return subcategories.value.find(sub => sub.id === parseInt(String(product.value.subcategory)))
})

const breadcrumbItems = computed(() => [
  { title: t.value('home'), to: '/', disabled: false },
  { title: 'پنل مدیریت', to: '/admin/dashboard', disabled: false },
  { title: t.value('addNewProduct'), disabled: true }
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

const getSelectedFullPath = () => {
  if (!selectedSubcategoryObject.value) return ''
  const parts: string[] = []
  if (selectedSubcategoryObject.value.departments && selectedSubcategoryObject.value.departments.length > 0) {
    parts.push(selectedSubcategoryObject.value.departments[0].name)
  }
  if (selectedSubcategoryObject.value.categories && selectedSubcategoryObject.value.categories.length > 0) {
    parts.push(selectedSubcategoryObject.value.categories[0].name)
  }
  parts.push(selectedSubcategoryObject.value.name)
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

  const { valid } = await formRef.value?.validate()
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

    const response = await productStore.createProduct(formData)
    successMessage.value = `محصول "${response.name}" با موفقیت ایجاد شد!`
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

