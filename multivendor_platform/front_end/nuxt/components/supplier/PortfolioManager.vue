<template>
  <div class="portfolio-manager" dir="rtl">
    <v-card elevation="2">
      <v-card-title class="text-h5 font-weight-bold d-flex align-center justify-space-between">
        <div>
          <v-icon color="primary" class="me-2">mdi-briefcase</v-icon>
          مدیریت نمونه کارها
        </div>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="openForm()"
        >
          افزودن نمونه کار
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Loading State -->
        <v-row v-if="loading" justify="center" class="my-8">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-row>

        <!-- Portfolio List -->
        <v-row v-else-if="items.length > 0">
          <v-col
            v-for="item in items"
            :key="item.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card class="portfolio-item-card" elevation="3">
              <v-badge
                v-if="item.is_featured"
                content="ویژه"
                color="amber"
                floating
              >
                <v-img
                  :src="getImageUrl(item.image) || ''"
                  height="200"
                  cover
                >
                  <template v-slot:placeholder>
                    <v-skeleton-loader type="image" />
                  </template>
                </v-img>
              </v-badge>
              <v-img
                v-else
                :src="getImageUrl(item.image) || ''"
                height="200"
                cover
              >
                <template v-slot:placeholder>
                  <v-skeleton-loader type="image" />
                </template>
              </v-img>

              <v-card-text>
                <h3 class="text-subtitle-1 font-weight-bold mb-1">
                  {{ item.title }}
                </h3>
                <p class="text-caption text-medium-emphasis line-clamp-2 mb-2">
                  {{ item.description }}
                </p>
                <div class="d-flex align-center justify-space-between">
                  <v-chip v-if="item.category" size="x-small" variant="tonal" color="primary">
                    {{ item.category }}
                  </v-chip>
                  <v-chip size="x-small" variant="outlined">
                    ترتیب: {{ item.sort_order || 0 }}
                  </v-chip>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="openForm(item)"
                ></v-btn>
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="confirmDelete(item)"
                ></v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  :icon="item.is_featured ? 'mdi-star' : 'mdi-star-outline'"
                  size="small"
                  variant="text"
                  :color="item.is_featured ? 'amber' : 'grey'"
                  @click="toggleFeatured(item)"
                ></v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- Empty State -->
        <v-row v-else justify="center" class="my-8">
          <v-col cols="12" class="text-center">
            <v-icon size="80" color="grey-lighten-2">mdi-folder-open</v-icon>
            <h3 class="text-h6 mt-3">هنوز نمونه کاری اضافه نشده</h3>
            <p class="text-body-2 text-medium-emphasis mb-4">
              نمونه کارها و پروژه‌های موفق خود را به نمایش بگذارید
            </p>
            <v-btn color="primary" prepend-icon="mdi-plus" @click="openForm()">
              افزودن اولین نمونه کار
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Form Dialog -->
    <v-dialog v-model="formDialog" max-width="800" persistent>
      <v-card>
        <v-card-title class="text-h6 font-weight-bold">
          {{ editingItem ? 'ویرایش نمونه کار' : 'افزودن نمونه کار' }}
        </v-card-title>

        <v-card-text>
          <v-form ref="formRef" v-model="formValid">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.title"
                  label="عنوان پروژه *"
                  prepend-icon="mdi-text"
                  variant="outlined"
                  :rules="[v => !!v || 'عنوان الزامی است']"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="formData.description"
                  label="توضیحات *"
                  prepend-icon="mdi-text-long"
                  variant="outlined"
                  rows="4"
                  :rules="[v => !!v || 'توضیحات الزامی است']"
                  required
                ></v-textarea>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.category"
                  label="دسته‌بندی"
                  prepend-icon="mdi-tag"
                  variant="outlined"
                  placeholder="مثال: صنعتی، تجاری، ..."
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.client_name"
                  label="نام کارفرما"
                  prepend-icon="mdi-account"
                  variant="outlined"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <PersianDatePicker
                  v-model="formData.project_date"
                  label="تاریخ پروژه"
                  prepend-icon="mdi-calendar"
                  variant="outlined"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="formData.sort_order"
                  label="ترتیب نمایش"
                  prepend-icon="mdi-sort"
                  type="number"
                  variant="outlined"
                  hint="عدد کمتر = نمایش زودتر"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-checkbox
                  v-model="formData.is_featured"
                  label="نمایش به عنوان پروژه ویژه"
                  color="primary"
                  hide-details
                ></v-checkbox>
              </v-col>

              <v-col cols="12">
                <div class="mb-2 text-subtitle-2 font-weight-bold">تصاویر پروژه *</div>
                
                <!-- Image Gallery Preview -->
                <div v-if="imagePreviews.length > 0" class="mb-3">
                  <v-row dense>
                    <v-col
                      v-for="(preview, index) in imagePreviews"
                      :key="index"
                      cols="6"
                      sm="4"
                      md="3"
                    >
                      <div class="image-preview-wrapper position-relative">
                        <v-img
                          :src="preview.url"
                          height="150"
                          cover
                          class="rounded"
                        >
                          <template v-slot:placeholder>
                            <v-skeleton-loader type="image" />
                          </template>
                        </v-img>
                        <v-btn
                          icon="mdi-close"
                          size="small"
                          color="error"
                          variant="flat"
                          class="remove-image-btn"
                          @click="removeImageAtIndex(index)"
                        ></v-btn>
                        <v-chip
                          v-if="index === 0"
                          size="x-small"
                          color="primary"
                          class="primary-image-badge"
                        >
                          اصلی
                        </v-chip>
                      </div>
                    </v-col>
                  </v-row>
                  <v-alert
                    v-if="imagePreviews.length > 1"
                    type="info"
                    variant="tonal"
                    density="compact"
                    class="mt-2"
                  >
                    اولین تصویر به عنوان تصویر اصلی نمایش داده می‌شود
                  </v-alert>
                </div>

                <!-- Existing Image Preview (when editing) -->
                <div v-else-if="existingImagePreview" class="mb-3">
                  <v-img
                    :src="existingImagePreview"
                    height="200"
                    cover
                    class="rounded"
                  >
                    <template v-slot:placeholder>
                      <v-skeleton-loader type="image" />
                    </template>
                  </v-img>
                  <v-btn
                    icon="mdi-close"
                    size="small"
                    color="error"
                    variant="flat"
                    class="mt-2"
                    @click="removeExistingImage"
                  >
                    حذف تصویر موجود
                  </v-btn>
                </div>

                <v-file-input
                  v-model="imageFile"
                  label="انتخاب تصاویر (می‌توانید چند تصویر انتخاب کنید)"
                  prepend-icon="mdi-image-multiple"
                  accept="image/*"
                  variant="outlined"
                  multiple
                  chips
                  show-size
                  @update:model-value="onImageChange"
                  :rules="imageValidationRules"
                  hide-details="auto"
                >
                  <template v-slot:selection="{ fileNames }">
                    <template v-for="(fileName, index) in fileNames" :key="fileName">
                      <v-chip
                        size="small"
                        color="primary"
                        class="me-2"
                      >
                        {{ fileName }}
                      </v-chip>
                    </template>
                  </template>
                </v-file-input>
                <div class="text-caption text-medium-emphasis mt-1">
                  می‌توانید حداکثر 10 تصویر انتخاب کنید
                </div>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-btn color="primary" :loading="saving" :disabled="!formValid" @click="saveItem">
            {{ editingItem ? 'به‌روزرسانی' : 'ذخیره' }}
          </v-btn>
          <v-btn variant="text" @click="closeForm">انصراف</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">حذف نمونه کار</v-card-title>
        <v-card-text>
          آیا مطمئن هستید که می‌خواهید این نمونه کار را حذف کنید؟
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" :loading="deleting" @click="deleteItem">حذف</v-btn>
          <v-btn variant="text" @click="deleteDialog = false">انصراف</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed, nextTick } from 'vue'
import { useSupplierPortfolioApi, type SupplierPortfolioItem } from '~/composables/useSupplierPortfolioApi'
import { formatImageUrl } from '~/utils/imageUtils'
import PersianDatePicker from '~/components/common/PersianDatePicker.vue'

const portfolioApi = useSupplierPortfolioApi()

// Helper function to get image URL (handles both string and File types)
const getImageUrl = (image: string | File | undefined): string | null => {
  if (!image) return null
  if (typeof image === 'string') {
    return formatImageUrl(image)
  }
  // If it's a File, create object URL for preview
  if (image instanceof File) {
    return URL.createObjectURL(image)
  }
  return null
}

const items = ref<SupplierPortfolioItem[]>([])
const loading = ref(false)
const formDialog = ref(false)
const deleteDialog = ref(false)
const formRef = ref()
const formValid = ref(false)
const saving = ref(false)
const deleting = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const editingItem = ref<SupplierPortfolioItem | null>(null)
const itemToDelete = ref<SupplierPortfolioItem | null>(null)
const imageFile = ref<File[]>([])
const imagePreviews = ref<Array<{ url: string; file: File }>>([])
const existingImagePreview = ref<string>('')
const isUpdatingImages = ref(false) // Flag to prevent recursive updates

const formData = ref({
  title: '',
  description: '',
  category: '',
  client_name: '',
  project_date: '',
  sort_order: 0,
  is_featured: false
})

// Image validation rules
const imageValidationRules = computed(() => [
  (v: File[] | null) => {
    // If editing, image is optional (can keep existing image)
    if (editingItem.value && (existingImagePreview.value || imagePreviews.value.length > 0)) {
      return true
    }
    // If creating new, at least one image is required
    if (!v || !Array.isArray(v) || v.length === 0) {
      return 'حداقل یک تصویر الزامی است'
    }
    // Check maximum number of images
    if (v.length > 10) {
      return 'حداکثر 10 تصویر می‌توانید انتخاب کنید'
    }
    return true
  }
])

const loadItems = async () => {
  loading.value = true
  try {
    items.value = await portfolioApi.getPortfolioItems()
  } catch (error) {
    console.error('Error loading portfolio items:', error)
  } finally {
    loading.value = false
  }
}

const openForm = (item?: SupplierPortfolioItem) => {
  if (item) {
    editingItem.value = item
    formData.value = {
      title: item.title,
      description: item.description,
      category: item.category || '',
      client_name: item.client_name || '',
      project_date: item.project_date || '',
      sort_order: item.sort_order || 0,
      is_featured: item.is_featured || false
    }
    if (item.image) {
      const imageUrl = getImageUrl(item.image)
      existingImagePreview.value = imageUrl || ''
    } else {
      existingImagePreview.value = ''
    }
    imagePreviews.value = []
    imageFile.value = []
  } else {
    editingItem.value = null
    formData.value = {
      title: '',
      description: '',
      category: '',
      client_name: '',
      project_date: '',
      sort_order: 0,
      is_featured: false
    }
    existingImagePreview.value = ''
    imagePreviews.value = []
    imageFile.value = []
  }
  formDialog.value = true
}

const closeForm = () => {
  formDialog.value = false
  editingItem.value = null
  existingImagePreview.value = ''
  imagePreviews.value = []
  imageFile.value = []
  // Clean up object URLs
  imagePreviews.value.forEach(preview => {
    if (preview.url.startsWith('blob:')) {
      URL.revokeObjectURL(preview.url)
    }
  })
  formRef.value?.reset()
}

const onImageChange = async (files: File | File[] | null) => {
  // Prevent recursive updates
  if (isUpdatingImages.value) {
    return
  }

  isUpdatingImages.value = true

  try {
    // Clean up previous preview URLs
    imagePreviews.value.forEach(preview => {
      if (preview.url.startsWith('blob:')) {
        URL.revokeObjectURL(preview.url)
      }
    })

    // Normalize to array
    const fileArray = Array.isArray(files) ? files : files ? [files] : []
    
    // Limit to 10 images
    const limitedFiles = fileArray.slice(0, 10)
    
    // Create previews for all selected images
    imagePreviews.value = []
    
    for (const file of limitedFiles) {
      if (file instanceof File) {
        const url = URL.createObjectURL(file)
        imagePreviews.value.push({ url, file })
      }
    }

    // Only update imageFile if it's different to prevent recursion
    const currentFiles = imageFile.value
    const filesChanged = 
      currentFiles.length !== limitedFiles.length ||
      currentFiles.some((file, index) => file !== limitedFiles[index])
    
    if (filesChanged) {
      imageFile.value = limitedFiles
    }

    // Trigger validation after files are selected
    await nextTick()
    if (formRef.value) {
      formRef.value.validate()
    }
  } finally {
    isUpdatingImages.value = false
  }
}

const removeImageAtIndex = async (index: number) => {
  if (isUpdatingImages.value) {
    return
  }

  isUpdatingImages.value = true

  try {
    // Clean up the object URL
    if (imagePreviews.value[index]?.url.startsWith('blob:')) {
      URL.revokeObjectURL(imagePreviews.value[index].url)
    }
    
    // Remove from previews and files
    imagePreviews.value.splice(index, 1)
    imageFile.value.splice(index, 1)

    // Trigger validation after removing image
    await nextTick()
    if (formRef.value) {
      formRef.value.validate()
    }
  } finally {
    isUpdatingImages.value = false
  }
}

const removeExistingImage = async () => {
  existingImagePreview.value = ''
  // Trigger validation
  await nextTick()
  if (formRef.value) {
    formRef.value.validate()
  }
}

// Note: We don't need a watcher here because @update:model-value
// on the v-file-input already calls onImageChange directly

const saveItem = async () => {
  if (!formValid.value) return

  saving.value = true

  try {
    const data: any = {
      ...formData.value
    }

    // Use the first image as the main image (backend currently supports single image)
    // If new images are selected, use the first one
    // Otherwise, if editing and no new images, keep existing
    if (imageFile.value && imageFile.value.length > 0) {
      data.image = imageFile.value[0]
    }
    // Note: If we want to support multiple images in the future,
    // we can send additional images as image_1, image_2, etc.

    if (editingItem.value) {
      await portfolioApi.updatePortfolioItem(editingItem.value.id!, data)
      snackbarMessage.value = 'نمونه کار با موفقیت به‌روزرسانی شد'
    } else {
      await portfolioApi.createPortfolioItem(data)
      snackbarMessage.value = 'نمونه کار با موفقیت اضافه شد'
    }

    snackbarColor.value = 'success'
    snackbar.value = true
    closeForm()
    await loadItems()
  } catch (error) {
    console.error('Error saving portfolio item:', error)
    snackbarMessage.value = 'خطا در ذخیره نمونه کار'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    saving.value = false
  }
}

const confirmDelete = (item: SupplierPortfolioItem) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const deleteItem = async () => {
  if (!itemToDelete.value) return

  deleting.value = true

  try {
    await portfolioApi.deletePortfolioItem(itemToDelete.value.id!)
    snackbarMessage.value = 'نمونه کار با موفقیت حذف شد'
    snackbarColor.value = 'success'
    snackbar.value = true
    deleteDialog.value = false
    await loadItems()
  } catch (error) {
    console.error('Error deleting portfolio item:', error)
    snackbarMessage.value = 'خطا در حذف نمونه کار'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    deleting.value = false
  }
}

const toggleFeatured = async (item: SupplierPortfolioItem) => {
  try {
    await portfolioApi.updatePortfolioItem(item.id!, {
      is_featured: !item.is_featured
    })
    await loadItems()
    snackbarMessage.value = 'وضعیت ویژه تغییر کرد'
    snackbarColor.value = 'success'
    snackbar.value = true
  } catch (error) {
    console.error('Error toggling featured:', error)
  }
}

onMounted(() => {
  loadItems()
})
</script>

<style scoped>
.portfolio-item-card {
  transition: transform 0.3s ease;
}

.portfolio-item-card:hover {
  transform: translateY(-4px);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.image-preview-wrapper {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid rgba(var(--v-theme-surface-variant), 0.3);
  transition: all 0.3s ease;
}

.image-preview-wrapper:hover {
  border-color: rgb(var(--v-theme-primary));
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.remove-image-btn {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 2;
  opacity: 0.9;
}

.remove-image-btn:hover {
  opacity: 1;
}

.primary-image-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  z-index: 2;
}
</style>

