<template>
  <div dir="rtl">
    <v-card elevation="0" variant="outlined">
      <v-card-title class="pa-4">مدیریت دپارتمان‌ها</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-btn color="primary" @click="openCreateDialog" prepend-icon="mdi-plus" class="mb-4">
          افزودن دپارتمان
        </v-btn>
        <v-data-table
          :headers="headers"
          :items="departments"
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
            <v-btn size="small" variant="text" @click="editDepartment(item)">
              ویرایش
            </v-btn>
            <v-btn size="small" variant="text" color="error" @click="deleteDepartment(item)">
              حذف
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>{{ editingItem ? 'ویرایش دپارتمان' : 'افزودن دپارتمان' }}</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="form.name"
              label="نام دپارتمان *"
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
          <v-btn color="primary" @click="saveDepartment" :loading="saving">ذخیره</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
const departmentStore = useDepartmentStore()

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

const departments = computed(() => departmentStore.departments || [])

const loadDepartments = async () => {
  loading.value = true
  try {
    await departmentStore.fetchDepartments()
  } catch (error) {
    console.error('Failed to load departments:', error)
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  editingItem.value = null
  resetForm()
  showDialog.value = true
}

const editDepartment = (item: any) => {
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

const saveDepartment = async () => {
  if (!formRef.value?.validate()) return

  saving.value = true
  try {
    if (editingItem.value) {
      await departmentStore.updateDepartment(editingItem.value.id, form.value)
    } else {
      await departmentStore.createDepartment(form.value)
    }
    await loadDepartments()
    closeDialog()
  } catch (error) {
    console.error('Failed to save department:', error)
  } finally {
    saving.value = false
  }
}

const deleteDepartment = async (item: any) => {
  if (confirm(`آیا مطمئن هستید که می‌خواهید دپارتمان "${item.name}" را حذف کنید؟`)) {
    try {
      await departmentStore.deleteDepartment(item.id)
      await loadDepartments()
    } catch (error) {
      console.error('Failed to delete department:', error)
    }
  }
}

onMounted(() => {
  loadDepartments()
})
</script>

