<template>
  <div dir="rtl">
    <!-- Summary Cards -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="3">
        <v-card class="summary-card" elevation="0" variant="outlined">
          <v-card-text class="text-center pa-4">
            <div class="text-h5 font-weight-bold mb-1">{{ categories.length }}</div>
            <div class="text-caption text-grey">کل دسته‌بندی‌ها</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="summary-card" elevation="0" variant="outlined">
          <v-card-text class="text-center pa-4">
            <div class="text-h5 font-weight-bold text-success mb-1">
              {{ categories.filter(c => c.is_active).length }}
            </div>
            <div class="text-caption text-grey">فعال</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="summary-card" elevation="0" variant="outlined">
          <v-card-text class="text-center pa-4">
            <div class="text-h5 font-weight-bold text-warning mb-1">
              {{ categories.filter(c => !c.is_active).length }}
            </div>
            <div class="text-caption text-grey">غیرفعال</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filters and Actions -->
    <v-card class="mb-4" elevation="0" variant="outlined">
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="filters.search"
              label="جستجو"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              clearable
              @update:model-value="loadCategories"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.is_active"
              label="وضعیت"
              :items="statusFilterOptions"
              clearable
              density="compact"
              variant="outlined"
              @update:model-value="loadCategories"
            ></v-select>
          </v-col>
          <v-col cols="12" md="5">
            <v-btn
              color="primary"
              @click="openCreateDialog"
              prepend-icon="mdi-plus"
            >
              افزودن دسته‌بندی
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Categories Table -->
    <v-card elevation="0" variant="outlined">
      <v-card-title class="pa-4">لیست دسته‌بندی‌ها</v-card-title>
      <v-divider></v-divider>
      <v-data-table
        :headers="headers"
        :items="categories"
        :loading="loading"
        item-value="id"
        class="categories-table"
      >
        <template v-slot:item.name="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="40" class="mr-2" rounded v-if="item.image_url">
              <v-img :src="item.image_url" cover></v-img>
            </v-avatar>
            <strong>{{ item.name }}</strong>
          </div>
        </template>
        <template v-slot:item.is_active="{ item }">
          <v-chip size="small" :color="item.is_active ? 'success' : 'warning'">
            {{ item.is_active ? 'فعال' : 'غیرفعال' }}
          </v-chip>
        </template>
        <template v-slot:item.sort_order="{ item }">
          {{ item.sort_order }}
        </template>
        <template v-slot:item.created_at="{ item }">
          {{ formatDate(item.created_at) }}
        </template>
        <template v-slot:item.actions="{ item }">
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn icon size="small" variant="text" v-bind="props">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
                <v-list-item @click="editCategory(item)">
                <template v-slot:prepend>
                  <v-icon>mdi-pencil</v-icon>
                </template>
                <v-list-item-title>ویرایش</v-list-item-title>
              </v-list-item>
              <v-list-item @click="deleteCategory(item)">
                <template v-slot:prepend>
                  <v-icon color="error">mdi-delete</v-icon>
                </template>
                <v-list-item-title>حذف</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="showDialog" max-width="900px" scrollable>
      <v-card>
        <v-card-title>{{ editingItem ? 'ویرایش دسته‌بندی' : 'افزودن دسته‌بندی' }}</v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-form ref="formRef" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.name"
                  label="نام دسته‌بندی *"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'نام الزامی است']"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.slug"
                  label="Slug"
                  variant="outlined"
                  density="compact"
                  hint="به صورت خودکار از نام ایجاد می‌شود"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <label class="text-body-2 mb-2 d-block">توضیحات</label>
                <TiptapEditor v-model="form.description" />
              </v-col>
              <v-col cols="12" md="6">
                <v-file-input
                  v-model="form.imageFile"
                  label="تصویر"
                  accept="image/*"
                  variant="outlined"
                  density="compact"
                  prepend-icon="mdi-image"
                  @change="handleImageChange"
                ></v-file-input>
                <v-img
                  v-if="form.image_url || imagePreview"
                  :src="imagePreview || form.image_url"
                  max-height="150"
                  class="mt-2"
                  contain
                ></v-img>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.image_alt_text"
                  label="Alt Text برای تصویر"
                  variant="outlined"
                  density="compact"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.sort_order"
                  label="ترتیب نمایش"
                  type="number"
                  variant="outlined"
                  density="compact"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-switch
                  v-model="form.is_active"
                  label="فعال"
                  color="success"
                ></v-switch>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="form.departments"
                  :items="departments"
                  item-title="name"
                  item-value="id"
                  label="دپارتمان‌ها"
                  multiple
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>

              <!-- SEO Section -->
              <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-4">تنظیمات SEO</h3>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.meta_title"
                  label="Meta Title"
                  variant="outlined"
                  density="compact"
                  hint="حداکثر 60 کاراکتر"
                  :counter="60"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="form.meta_description"
                  label="Meta Description"
                  variant="outlined"
                  density="compact"
                  rows="3"
                  hint="حداکثر 160 کاراکتر"
                  :counter="160"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="form.canonical_url"
                  label="Canonical URL"
                  variant="outlined"
                  density="compact"
                  type="url"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-file-input
                  v-model="form.og_imageFile"
                  label="Open Graph Image"
                  accept="image/*"
                  variant="outlined"
                  density="compact"
                  prepend-icon="mdi-image"
                  @change="handleOgImageChange"
                ></v-file-input>
                <v-img
                  v-if="form.og_image_url || ogImagePreview"
                  :src="ogImagePreview || form.og_image_url"
                  max-height="150"
                  class="mt-2"
                  contain
                ></v-img>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">انصراف</v-btn>
          <v-btn color="primary" @click="saveCategory" :loading="saving">ذخیره</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import TiptapEditor from '@/components/TiptapEditor.vue'

export default {
  name: 'CategoryManagement',
  components: {
    TiptapEditor
  },
  setup() {
    const categories = ref([])
    const departments = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const showDialog = ref(false)
    const editingItem = ref(null)
    const formRef = ref(null)
    const formValid = ref(false)
    const imagePreview = ref(null)
    const ogImagePreview = ref(null)

    const filters = ref({
      search: null,
      is_active: null
    })

    const form = ref({
      name: '',
      slug: '',
      description: '',
      image: null,
      imageFile: null,
      image_url: null,
      image_alt_text: '',
      og_image: null,
      og_imageFile: null,
      og_image_url: null,
      meta_title: '',
      meta_description: '',
      canonical_url: '',
      sort_order: 0,
      is_active: true,
      departments: []
    })

    const headers = [
      { title: 'نام', key: 'name', align: 'start' },
      { title: 'وضعیت', key: 'is_active', align: 'center' },
      { title: 'ترتیب', key: 'sort_order', align: 'center' },
      { title: 'تاریخ ایجاد', key: 'created_at', align: 'start' },
      { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
    ]

    const statusFilterOptions = [
      { title: 'فعال', value: 'true' },
      { title: 'غیرفعال', value: 'false' }
    ]

    const loadCategories = async () => {
      loading.value = true
      try {
        const params = {}
        if (filters.value.search) params.search = filters.value.search
        if (filters.value.is_active !== null) params.is_active = filters.value.is_active
        if (filters.value.department) params.department = filters.value.department

        const response = await api.getAdminCategories(params)
        categories.value = response.data
      } catch (error) {
        console.error('Failed to load categories:', error)
      } finally {
        loading.value = false
      }
    }

    const loadDepartments = async () => {
      try {
        const response = await api.getAdminDepartments()
        departments.value = response.data
      } catch (error) {
        console.error('Failed to load departments:', error)
      }
    }

    const openCreateDialog = () => {
      editingItem.value = null
      resetForm()
      showDialog.value = true
    }

    const editCategory = async (item) => {
      editingItem.value = item
      try {
        const response = await api.getAdminCategoryDetail(item.id)
        const data = response.data
        form.value = {
          name: data.name || '',
          slug: data.slug || '',
          description: data.description || '',
          image: null,
          imageFile: null,
          image_url: data.image_url || null,
          image_alt_text: data.image_alt_text || '',
          og_image: null,
          og_imageFile: null,
          og_image_url: data.og_image_url || null,
          meta_title: data.meta_title || '',
          meta_description: data.meta_description || '',
          canonical_url: data.canonical_url || '',
          sort_order: data.sort_order || 0,
          is_active: data.is_active !== undefined ? data.is_active : true,
          departments: data.departments ? data.departments.map(d => d.id) : []
        }
        showDialog.value = true
      } catch (error) {
        console.error('Failed to load category:', error)
      }
    }

    const resetForm = () => {
      form.value = {
        name: '',
        slug: '',
        description: '',
        image: null,
        imageFile: null,
        image_url: null,
        image_alt_text: '',
        og_image: null,
        og_imageFile: null,
        og_image_url: null,
        meta_title: '',
        meta_description: '',
      canonical_url: '',
      sort_order: 0,
      is_active: true,
      departments: []
      }
      imagePreview.value = null
      ogImagePreview.value = null
    }

    const closeDialog = () => {
      showDialog.value = false
      editingItem.value = null
      resetForm()
    }

    const handleImageChange = (file) => {
      if (file && file.length > 0) {
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file[0])
      } else {
        imagePreview.value = null
      }
    }

    const handleOgImageChange = (file) => {
      if (file && file.length > 0) {
        const reader = new FileReader()
        reader.onload = (e) => {
          ogImagePreview.value = e.target.result
        }
        reader.readAsDataURL(file[0])
      } else {
        ogImagePreview.value = null
      }
    }

    const saveCategory = async () => {
      if (!formRef.value?.validate()) return

      saving.value = true
      try {
        const formData = new FormData()
        formData.append('name', form.value.name)
        if (form.value.slug) formData.append('slug', form.value.slug)
        if (form.value.description) formData.append('description', form.value.description)
        if (form.value.imageFile && form.value.imageFile.length > 0) {
          formData.append('image', form.value.imageFile[0])
        }
        if (form.value.image_alt_text) formData.append('image_alt_text', form.value.image_alt_text)
        if (form.value.og_imageFile && form.value.og_imageFile.length > 0) {
          formData.append('og_image', form.value.og_imageFile[0])
        }
        if (form.value.meta_title) formData.append('meta_title', form.value.meta_title)
        if (form.value.meta_description) formData.append('meta_description', form.value.meta_description)
        if (form.value.canonical_url) formData.append('canonical_url', form.value.canonical_url)
        formData.append('sort_order', form.value.sort_order)
        formData.append('is_active', form.value.is_active)
        if (form.value.departments && form.value.departments.length > 0) {
          form.value.departments.forEach(deptId => {
            formData.append('departments', deptId)
          })
        }

        if (editingItem.value) {
          await api.adminUpdateCategory(editingItem.value.id, formData)
        } else {
          await api.adminCreateCategory(formData)
        }

        closeDialog()
        await loadCategories()
      } catch (error) {
        console.error('Failed to save category:', error)
      } finally {
        saving.value = false
      }
    }

    const deleteCategory = async (item) => {
      if (confirm(`آیا مطمئن هستید که می‌خواهید دسته‌بندی "${item.name}" را حذف کنید؟`)) {
        try {
          await api.adminDeleteCategory(item.id)
          await loadCategories()
        } catch (error) {
          console.error('Failed to delete category:', error)
        }
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('fa-IR')
    }

    onMounted(() => {
      loadCategories()
      loadDepartments()
    })

    return {
      categories,
      departments,
      loading,
      saving,
      showDialog,
      editingItem,
      formRef,
      formValid,
      form,
      filters,
      headers,
      statusFilterOptions,
      imagePreview,
      ogImagePreview,
      loadCategories,
      loadDepartments,
      openCreateDialog,
      editCategory,
      closeDialog,
      saveCategory,
      deleteCategory,
      handleImageChange,
      handleOgImageChange,
      formatDate
    }
  }
}
</script>

<style scoped>
.categories-table {
  direction: rtl;
}
</style>

