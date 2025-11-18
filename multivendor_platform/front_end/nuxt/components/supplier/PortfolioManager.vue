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
                  :src="formatImageUrl(item.image)"
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
                :src="formatImageUrl(item.image)"
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
                <v-text-field
                  v-model="formData.project_date"
                  label="تاریخ پروژه"
                  prepend-icon="mdi-calendar"
                  type="date"
                  variant="outlined"
                ></v-text-field>
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
                <div class="mb-2 text-subtitle-2 font-weight-bold">تصویر پروژه *</div>
                <div v-if="imagePreview" class="mb-3">
                  <v-img :src="imagePreview" height="200" cover class="rounded">
                    <v-btn
                      icon="mdi-close"
                      size="small"
                      color="error"
                      class="ma-2"
                      @click="removeImage"
                    ></v-btn>
                  </v-img>
                </div>
                <v-file-input
                  v-model="imageFile"
                  label="انتخاب تصویر"
                  prepend-icon="mdi-camera"
                  accept="image/*"
                  variant="outlined"
                  @change="onImageChange"
                  :rules="[v => !!editingItem || !!imageFile.length || 'تصویر الزامی است']"
                ></v-file-input>
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
import { ref, onMounted } from 'vue'
import { useSupplierPortfolioApi, type SupplierPortfolioItem } from '~/composables/useSupplierPortfolioApi'
import { formatImageUrl } from '~/utils/imageUtils'

const portfolioApi = useSupplierPortfolioApi()

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
const imagePreview = ref<string>('')

const formData = ref({
  title: '',
  description: '',
  category: '',
  client_name: '',
  project_date: '',
  sort_order: 0,
  is_featured: false
})

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
      imagePreview.value = formatImageUrl(item.image)
    }
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
    imagePreview.value = ''
    imageFile.value = []
  }
  formDialog.value = true
}

const closeForm = () => {
  formDialog.value = false
  editingItem.value = null
  imagePreview.value = ''
  imageFile.value = []
  formRef.value?.reset()
}

const onImageChange = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (files && files[0]) {
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(files[0])
  }
}

const removeImage = () => {
  imageFile.value = []
  imagePreview.value = ''
}

const saveItem = async () => {
  if (!formValid.value) return

  saving.value = true

  try {
    const data: any = {
      ...formData.value
    }

    if (imageFile.value.length > 0) {
      data.image = imageFile.value[0]
    }

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
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

