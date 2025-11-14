<template>
  <div dir="rtl" class="blog-form-container">
    <v-container fluid class="pa-4">
      <h1 class="text-h4 text-sm-h3 font-weight-bold mb-4 mb-sm-6">
        {{ t('editPost') }}
      </h1>

      <v-row v-if="loading" justify="center" class="my-16">
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <p class="text-h6 mt-4">{{ t('loading') }}</p>
        </v-col>
      </v-row>

      <v-form v-if="!loading" @submit.prevent="submitForm" ref="formRef">
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
                  <LazyTiptapEditor v-model="form.content" class="content-editor" />
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
                ></v-select>

                <!-- Subcategory Selection -->
                <v-autocomplete
                  v-model="form.linked_subcategory_ids"
                  label="زیردسته‌ها"
                  :items="subcategories"
                  item-title="name"
                  item-value="id"
                  variant="outlined"
                  rounded="lg"
                  multiple
                  chips
                  closable-chips
                  :loading="loadingSubcategories"
                  class="mb-4"
                  hint="انتخاب زیردسته‌ها برای مرتبط کردن پست با دسته‌های فرعی"
                  persistent-hint
                >
                  <template v-slot:prepend-item>
                    <v-list-item
                      title="همه زیردسته‌ها"
                      @click="selectAllSubcategories"
                    >
                      <template v-slot:prepend>
                        <v-checkbox
                          :model-value="allSubcategoriesSelected"
                          @update:model-value="toggleAllSubcategories"
                        ></v-checkbox>
                      </template>
                    </v-list-item>
                    <v-divider></v-divider>
                  </template>
                  <template v-slot:no-data>
                    <v-list-item>
                      <v-list-item-title>هیچ زیردسته‌ای یافت نشد</v-list-item-title>
                    </v-list-item>
                  </template>
                </v-autocomplete>

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
                  prepend-icon="mdi-content-save"
                  block
                  variant="elevated"
                  rounded="lg"
                  :loading="submitting"
                  :disabled="submitting"
                >
                  {{ submitting ? t('saving') : t('updatePost') }}
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
const blogStore = useBlogStore()
const subcategoryStore = useSubcategoryStore()

const slug = computed(() => route.params.slug as string)
const formRef = ref()
const submitting = ref(false)
const imagePreview = ref<string | null>(null)
const contentTouched = ref(false)
const loadingSubcategories = ref(false)

const form = ref({
  title: '',
  excerpt: '',
  content: '',
  category: '',
  linked_subcategory_ids: [] as number[],
  status: 'draft',
  is_featured: false,
  meta_title: '',
  meta_description: '',
  featured_image: null as File | null
})

const loading = computed(() => blogStore.loading)
const categories = computed(() => blogStore.categories || [])
const subcategories = computed(() => subcategoryStore.subcategories || [])
const t = computed(() => blogStore.t)

const allSubcategoriesSelected = computed(() => {
  return subcategories.value.length > 0 &&
         form.value.linked_subcategory_ids.length === subcategories.value.length
})

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

const selectAllSubcategories = () => {
  form.value.linked_subcategory_ids = subcategories.value.map(s => s.id)
}

const toggleAllSubcategories = (value: boolean) => {
  if (value) {
    selectAllSubcategories()
  } else {
    form.value.linked_subcategory_ids = []
  }
}

const loadPost = async () => {
  try {
    await blogStore.fetchPost(slug.value)
    const post = blogStore.currentPost
    if (post) {
      form.value = {
        title: post.title || '',
        excerpt: post.excerpt || '',
        content: post.content || '',
        category: post.category || '',
        linked_subcategory_ids: post.linked_subcategory_ids || [],
        status: post.status || 'draft',
        is_featured: post.is_featured || false,
        meta_title: post.meta_title || '',
        meta_description: post.meta_description || '',
        featured_image: null
      }

      if (post.featured_image) {
        imagePreview.value = post.featured_image
      }
    }
  } catch (error) {
    console.error('Error loading post:', error)
    router.push('/admin/dashboard?view=blog')
  }
}

const submitForm = async () => {
  contentTouched.value = true

  const formInstance = formRef.value
  if (!formInstance) {
    return
  }

  const { valid } = await formInstance.validate()
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
        } else if (key === 'linked_subcategory_ids') {
          // Handle array of subcategory IDs
          const subcategoryIds = value as number[]
          subcategoryIds.forEach(id => {
            formData.append('linked_subcategory_ids', String(id))
          })
        } else {
          formData.append(key, String(value))
        }
      }
    })

    await blogStore.updatePost(slug.value, formData)
    router.push('/admin/dashboard?view=blog')
  } catch (error: any) {
    console.error('Error submitting form:', error)
    alert('خطا در ارسال فرم: ' + (error?.data?.detail || error?.message || 'خطای نامشخص'))
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  loadingSubcategories.value = true
  try {
    await Promise.all([
      blogStore.fetchCategories(),
      subcategoryStore.fetchSubcategories({ page_size: 1000 }),
      loadPost()
    ])
  } finally {
    loadingSubcategories.value = false
  }
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

