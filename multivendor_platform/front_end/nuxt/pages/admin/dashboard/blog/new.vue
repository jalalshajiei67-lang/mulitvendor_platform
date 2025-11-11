<template>
  <div dir="rtl" class="blog-form-container">
    <v-container fluid class="pa-4">
      <h1 class="text-h4 text-sm-h3 font-weight-bold mb-4 mb-sm-6">
        {{ t('createNewPost') }}
      </h1>

      <v-form @submit.prevent="submitForm" ref="formRef">
        <v-row>
          <v-col cols="12" lg="8">
            <!-- Basic Information -->
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
              <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-primary pa-4 pa-sm-5">
                <v-icon class="mr-2">mdi-information</v-icon>
                {{ t('basicInformation') }}
              </v-card-title>
              <v-card-text class="pa-4 pa-sm-5 pa-md-6">
                <v-text-field
                  v-model="form.title"
                  :label="t('postTitle') + ' *'"
                  prepend-inner-icon="mdi-format-title"
                  variant="outlined"
                  rounded="lg"
                  :rules="[v => !!v || 'عنوان پست الزامی است']"
                  required
                  class="mb-4"
                ></v-text-field>

                <v-textarea
                  v-model="form.excerpt"
                  :label="t('postExcerpt')"
                  prepend-inner-icon="mdi-text"
                  variant="outlined"
                  rounded="lg"
                  rows="3"
                  hint="این در لیست وبلاگ و پیش‌نمایش شبکه‌های اجتماعی نمایش داده می‌شود"
                  persistent-hint
                  class="mb-4"
                ></v-textarea>

                <div class="content-editor-wrapper">
                  <label class="text-body-2 mb-2 d-block">
                    <v-icon size="small" class="mr-1">mdi-text</v-icon>
                    {{ t('postContent') }} <span class="text-error">*</span>
                  </label>
                  <TiptapEditor v-model="form.content" class="content-editor" />
                  <div v-if="!contentValid && contentTouched" class="text-error text-caption mt-1">
                    محتوای پست الزامی است
                  </div>
                </div>
              </v-card-text>
            </v-card>

            <!-- Featured Image -->
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6">
              <v-card-title class="text-h6 text-sm-h5 font-weight-bold bg-accent pa-4 pa-sm-5">
                <v-icon class="mr-2">mdi-image</v-icon>
                {{ t('featuredImage') }}
              </v-card-title>
              <v-card-text class="pa-4 pa-sm-5 pa-md-6">
                <div v-if="imagePreview" class="image-preview-wrapper">
                  <v-img :src="imagePreview" max-height="300" contain class="mb-4"></v-img>
                  <v-btn color="error" variant="outlined" @click="removeImage">
                    <v-icon class="mr-2">mdi-delete</v-icon>
                    حذف تصویر
                  </v-btn>
                </div>
                <div v-else>
                  <v-file-input
                    v-model="form.featured_image"
                    :label="t('clickToUpload')"
                    prepend-inner-icon="mdi-cloud-upload"
                    variant="outlined"
                    rounded="lg"
                    accept="image/*"
                    @change="handleImageUpload"
                  ></v-file-input>
                  <small class="text-caption text-medium-emphasis">{{ t('recommendedSize') }}: 1200x630px</small>
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Sidebar -->
          <v-col cols="12" lg="4">
            <!-- Publish Settings -->
            <v-card elevation="4" rounded="lg" class="mb-4 mb-sm-6 sticky-card">
              <v-card-title class="text-subtitle-1 text-sm-h6 font-weight-bold pa-4 pa-sm-5">
                <v-icon class="mr-2">mdi-cog</v-icon>
                {{ t('publishSettings') }}
              </v-card-title>
              <v-card-text class="pa-3 pa-sm-4">
                <v-select
                  v-model="form.status"
                  :label="t('status')"
                  :items="[
                    { title: t('draft'), value: 'draft' },
                    { title: t('published'), value: 'published' },
                    { title: t('archived'), value: 'archived' }
                  ]"
                  variant="outlined"
                  rounded="lg"
                  class="mb-4"
                ></v-select>

                <v-select
                  v-model="form.category"
                  :label="t('category') + ' *'"
                  :items="categories"
                  item-title="name"
                  item-value="id"
                  variant="outlined"
                  rounded="lg"
                  :rules="[v => !!v || 'انتخاب دسته‌بندی الزامی است']"
                  required
                  class="mb-4"
                >
                  <template v-slot:append-item>
                    <v-btn color="primary" variant="text" block @click="showCreateCategory = true" class="mt-2">
                      <v-icon class="mr-2">mdi-plus</v-icon>
                      {{ t('createNewCategory') }}
                    </v-btn>
                  </template>
                </v-select>

                <v-switch
                  v-model="form.is_featured"
                  :label="t('isFeatured')"
                  color="success"
                  inset
                  hide-details
                  class="mb-4"
                ></v-switch>
              </v-card-text>

              <v-divider></v-divider>

              <!-- SEO Settings -->
              <v-card-text class="pa-3 pa-sm-4">
                <h3 class="text-subtitle-2 font-weight-bold mb-3">{{ t('seoSettings') }}</h3>
                <v-text-field
                  v-model="form.meta_title"
                  :label="t('metaTitle')"
                  variant="outlined"
                  density="compact"
                  rounded="lg"
                  hint="خالی بگذارید تا از عنوان پست استفاده شود"
                  persistent-hint
                  class="mb-3"
                ></v-text-field>
                <v-textarea
                  v-model="form.meta_description"
                  :label="t('metaDescription')"
                  variant="outlined"
                  density="compact"
                  rounded="lg"
                  rows="3"
                  hint="خالی بگذارید تا از خلاصه پست استفاده شود"
                  persistent-hint
                ></v-textarea>
              </v-card-text>

              <v-divider></v-divider>

              <!-- Actions -->
              <v-card-actions class="pa-3 pa-sm-4 flex-column ga-2 ga-sm-3">
                <v-btn
                  type="submit"
                  color="primary"
                  size="x-large"
                  prepend-icon="mdi-paper-plane"
                  block
                  variant="elevated"
                  rounded="lg"
                  :loading="submitting"
                  :disabled="submitting"
                >
                  {{ submitting ? t('saving') : t('publishPost') }}
                </v-btn>
                <v-btn
                  color="secondary"
                  size="large"
                  prepend-icon="mdi-content-save"
                  block
                  variant="outlined"
                  rounded="lg"
                  @click="saveDraft"
                  :disabled="submitting"
                >
                  {{ t('savingDraft') }}
                </v-btn>
                <v-btn
                  color="secondary"
                  size="large"
                  prepend-icon="mdi-close"
                  block
                  variant="outlined"
                  rounded="lg"
                  to="/admin/dashboard?view=blog"
                >
                  {{ t('cancel') }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-form>

      <!-- Create Category Dialog -->
      <v-dialog v-model="showCreateCategory" max-width="500px">
        <v-card>
          <v-card-title>{{ t('createNewCategory') }}</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-form ref="categoryFormRef">
              <v-text-field
                v-model="categoryForm.name"
                :label="t('categoryName') + ' *'"
                variant="outlined"
                :rules="[v => !!v || 'نام دسته‌بندی الزامی است']"
                required
                class="mb-3"
              ></v-text-field>
              <v-textarea
                v-model="categoryForm.description"
                :label="t('categoryDescription')"
                variant="outlined"
                rows="3"
                class="mb-3"
              ></v-textarea>
              <v-text-field
                v-model="categoryForm.color"
                :label="t('categoryColor')"
                type="color"
                variant="outlined"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="showCreateCategory = false">{{ t('cancel') }}</v-btn>
            <v-btn color="primary" @click="createCategory" :loading="creatingCategory">{{ t('createCategory') }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'admin'
})

const router = useRouter()
const blogStore = useBlogStore()

const formRef = ref()
const categoryFormRef = ref()
const submitting = ref(false)
const creatingCategory = ref(false)
const showCreateCategory = ref(false)
const imagePreview = ref<string | null>(null)
const contentTouched = ref(false)

const form = ref({
  title: '',
  excerpt: '',
  content: '',
  category: '',
  status: 'draft',
  is_featured: false,
  meta_title: '',
  meta_description: '',
  featured_image: null as File | null
})

const categoryForm = ref({
  name: '',
  description: '',
  color: '#007bff'
})

const categories = computed(() => blogStore.categories || [])
const t = computed(() => blogStore.t)

const contentValid = computed(() => {
  if (!form.value.content) return false
  const content = form.value.content.trim()
  if (!content || content === '<p></p>' || content === '<p><br></p>') {
    return false
  }
  if (process.client) {
    try {
      const tempDiv = document.createElement('div')
      tempDiv.innerHTML = content
      const textContent = tempDiv.textContent || tempDiv.innerText || ''
      return textContent.trim().length > 0
    } catch (e) {
      const textOnly = content.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
      return textOnly.length > 0
    }
  }
  const textOnly = content.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim()
  return textOnly.length > 0
})

watch(() => form.value.content, () => {
  contentTouched.value = true
})

const handleImageUpload = (files: File[] | null) => {
  if (files && files.length > 0) {
    form.value.featured_image = files[0]
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(files[0])
  }
}

const removeImage = () => {
  form.value.featured_image = null
  imagePreview.value = null
}

const saveDraft = async () => {
  form.value.status = 'draft'
  await submitForm()
}

const submitForm = async () => {
  contentTouched.value = true

  const { valid } = await formRef.value?.validate()
  if (!valid) return

  if (!contentValid.value) {
    return
  }

  submitting.value = true

  try {
    const formData = new FormData()

    Object.keys(form.value).forEach(key => {
      if (key === 'featured_image') {
        if (form.value.featured_image) {
          formData.append(key, form.value.featured_image)
        }
        return
      }
      const value = form.value[key as keyof typeof form.value]
      if (value !== null && value !== undefined && value !== '') {
        if (key === 'category') {
          formData.append(key, String(parseInt(String(value))))
        } else if (key === 'is_featured') {
          formData.append(key, value ? 'true' : 'false')
        } else {
          formData.append(key, String(value))
        }
      }
    })

    await blogStore.createPost(formData)
    router.push('/admin/dashboard?view=blog')
  } catch (error: any) {
    console.error('Error submitting form:', error)
    alert('خطا در ارسال فرم: ' + (error?.data?.detail || error?.message || 'خطای نامشخص'))
  } finally {
    submitting.value = false
  }
}

const createCategory = async () => {
  const { valid } = await categoryFormRef.value?.validate()
  if (!valid) return

  creatingCategory.value = true
  try {
    const newCategory = await blogStore.createCategory(categoryForm.value)
    form.value.category = newCategory.id
    showCreateCategory.value = false
    categoryForm.value = {
      name: '',
      description: '',
      color: '#007bff'
    }
  } catch (error: any) {
    console.error('Error creating category:', error)
    alert('خطا در ایجاد دسته‌بندی: ' + (error?.data?.detail || error?.message || 'خطای نامشخص'))
  } finally {
    creatingCategory.value = false
  }
}

onMounted(async () => {
  await blogStore.fetchCategories()
})
</script>

<style scoped>
.blog-form-container {
  min-height: 100vh;
}

.content-editor-wrapper {
  margin-bottom: 16px;
}

.content-editor-wrapper label {
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.content-editor {
  margin-top: 8px;
}

.image-preview-wrapper {
  text-align: center;
}

.sticky-card {
  position: sticky;
  top: 80px;
}
</style>

