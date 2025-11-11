<template>
  <div dir="rtl">
    <v-card elevation="0" variant="outlined">
      <v-card-title class="pa-4">مدیریت زیردسته‌ها</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-btn color="primary" @click="openCreateDialog" prepend-icon="mdi-plus" class="mb-4">
          افزودن زیردسته
        </v-btn>
        <v-data-table
          :headers="headers"
          :items="subcategories"
          :loading="loading"
          item-value="id"
        >
          <template v-slot:item.name="{ item }">
            <strong>{{ item.name }}</strong>
          </template>
          <template v-slot:item.is_active="{ item }">
            <v-chip size="small" :color="item.is_active ? 'success' : 'warning'">
              {{ item.is_active ? 'فعال' : 'غیرفعال' }}
            </v-chip>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-btn size="small" variant="text" @click="editSubcategory(item)">
              ویرایش
            </v-btn>
            <v-btn size="small" variant="text" color="error" @click="deleteSubcategory(item)">
              حذف
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>{{ editingItem ? 'ویرایش زیردسته' : 'افزودن زیردسته' }}</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="form.name"
              label="نام زیردسته *"
              variant="outlined"
              :rules="[v => !!v || 'نام الزامی است']"
            ></v-text-field>
            <v-text-field
              v-model="form.slug"
              label="Slug"
              variant="outlined"
            ></v-text-field>
            <v-textarea
              v-model="form.description"
              label="توضیحات"
              variant="outlined"
              rows="3"
            ></v-textarea>
            <v-switch
              v-model="form.is_active"
              label="فعال"
              color="success"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="closeDialog">انصراف</v-btn>
          <v-btn color="primary" @click="saveSubcategory" :loading="saving">ذخیره</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
const subcategoryStore = useSubcategoryStore()

const loading = ref(false)
const saving = ref(false)
const showDialog = ref(false)
const editingItem = ref<any>(null)
const formRef = ref()

const form = ref({
  name: '',
  slug: '',
  description: '',
  is_active: true
})

const headers = [
  { title: 'نام', key: 'name' },
  { title: 'وضعیت', key: 'is_active' },
  { title: 'عملیات', key: 'actions' }
]

const subcategories = computed(() => subcategoryStore.subcategories || [])

const loadSubcategories = async () => {
  loading.value = true
  try {
    await subcategoryStore.fetchSubcategories()
  } catch (error) {
    console.error('Failed to load subcategories:', error)
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  editingItem.value = null
  resetForm()
  showDialog.value = true
}

const editSubcategory = (item: any) => {
  editingItem.value = item
  form.value = {
    name: item.name || '',
    slug: item.slug || '',
    description: item.description || '',
    is_active: item.is_active !== undefined ? item.is_active : true
  }
  showDialog.value = true
}

const resetForm = () => {
  form.value = {
    name: '',
    slug: '',
    description: '',
    is_active: true
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingItem.value = null
  resetForm()
}

const saveSubcategory = async () => {
  if (!formRef.value?.validate()) return

  saving.value = true
  try {
    if (editingItem.value) {
      await subcategoryStore.updateSubcategory(editingItem.value.id, form.value)
    } else {
      await subcategoryStore.createSubcategory(form.value)
    }
    await loadSubcategories()
    closeDialog()
  } catch (error) {
    console.error('Failed to save subcategory:', error)
  } finally {
    saving.value = false
  }
}

const deleteSubcategory = async (item: any) => {
  if (confirm(`آیا مطمئن هستید که می‌خواهید زیردسته "${item.name}" را حذف کنید؟`)) {
    try {
      await subcategoryStore.deleteSubcategory(item.id)
      await loadSubcategories()
    } catch (error) {
      console.error('Failed to delete subcategory:', error)
    }
  }
}

onMounted(() => {
  loadSubcategories()
})
</script>

