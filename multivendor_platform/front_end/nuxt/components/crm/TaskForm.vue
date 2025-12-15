<template>
  <v-form ref="formRef" @submit.prevent="handleSubmit">
    <v-text-field
      v-model="formData.title"
      label="عنوان"
      required
      :rules="[rules.required]"
      variant="outlined"
      density="comfortable"
      class="mb-3"
    ></v-text-field>

    <v-textarea
      v-model="formData.description"
      label="توضیحات"
      variant="outlined"
      density="comfortable"
      rows="3"
      class="mb-3"
    ></v-textarea>

    <v-select
      v-model="formData.contact"
      :items="contacts"
      item-title="label"
      item-value="value"
      label="مخاطب (اختیاری)"
      variant="outlined"
      density="comfortable"
      clearable
      class="mb-3"
    ></v-select>

    <PersianDatePicker
      v-model="formData.due_date_date"
      label="تاریخ سررسید"
      required
      :rules="[rules.required]"
      class="mb-3"
    />

    <v-text-field
      v-model="formData.due_date_time"
      label="زمان سررسید"
      type="time"
      required
      :rules="[rules.required]"
      variant="outlined"
      density="comfortable"
      class="mb-3"
    ></v-text-field>

    <v-select
      v-model="formData.priority"
      :items="priorityOptions"
      label="اولویت"
      required
      :rules="[rules.required]"
      variant="outlined"
      density="comfortable"
      class="mb-3"
    ></v-select>

    <v-card-actions class="pa-0">
      <v-spacer></v-spacer>
      <v-btn variant="text" @click="$emit('cancel')">انصراف</v-btn>
      <v-btn type="submit" color="primary" :loading="loading">ذخیره</v-btn>
    </v-card-actions>
  </v-form>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { ContactTask, SellerContact } from '~/composables/useCrmApi'
import PersianDatePicker from '~/components/common/PersianDatePicker.vue'
import { toGregorian, toJalaali } from 'jalaali-js'

const props = withDefaults(defineProps<{
  task?: ContactTask | null
  contacts?: SellerContact[]
  loading?: boolean
}>(), {
  task: null,
  contacts: () => [],
  loading: false
})

const emit = defineEmits<{
  submit: [data: Partial<ContactTask>]
  cancel: []
}>()

const formRef = ref()
const formData = ref<Partial<ContactTask> & { due_date_date?: string | null; due_date_time?: string }>({
  title: '',
  description: '',
  contact: null,
  due_date_date: null,
  due_date_time: '12:00',
  priority: 'medium'
})

const priorityOptions = [
  { title: 'کم', value: 'low' },
  { title: 'متوسط', value: 'medium' },
  { title: 'زیاد', value: 'high' }
]

const contacts = computed(() => {
  return props.contacts.map(c => {
    const fullName = [c.first_name, c.last_name].filter(Boolean).join(' ') || c.phone || 'بدون نام'
    return {
      label: `${fullName}${c.company_name ? ` (${c.company_name})` : ''}`,
      value: c.id
    }
  })
})

const rules = {
  required: (value: any) => !!value || 'این فیلد الزامی است'
}

watch(() => props.task, (task) => {
  if (task && task.due_date) {
    // Parse the datetime string (ISO format)
    const date = new Date(task.due_date)
    const dateStr = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    const timeStr = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
    
    formData.value = {
      title: task.title || '',
      description: task.description || '',
      contact: task.contact || null,
      due_date_date: dateStr,
      due_date_time: timeStr,
      priority: task.priority || 'medium'
    }
  } else {
    formData.value = {
      title: '',
      description: '',
      contact: null,
      due_date_date: null,
      due_date_time: '12:00',
      priority: 'medium'
    }
  }
}, { immediate: true })

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate()
  if (valid) {
    // Combine date and time into ISO datetime string
    let due_date = ''
    if (formData.value.due_date_date && formData.value.due_date_time) {
      // Parse the date (YYYY-MM-DD format from PersianDatePicker)
      const dateParts = formData.value.due_date_date.split('-')
      const timeParts = formData.value.due_date_time.split(':')
      
      if (dateParts.length === 3 && timeParts.length === 2) {
        const year = parseInt(dateParts[0])
        const month = parseInt(dateParts[1]) - 1 // JavaScript months are 0-indexed
        const day = parseInt(dateParts[2])
        const hours = parseInt(timeParts[0])
        const minutes = parseInt(timeParts[1])
        
        const date = new Date(year, month, day, hours, minutes)
        due_date = date.toISOString()
      }
    }
    
    const submitData: Partial<ContactTask> = {
      title: formData.value.title,
      description: formData.value.description,
      contact: formData.value.contact,
      due_date: due_date,
      priority: formData.value.priority
    }
    
    emit('submit', submitData)
  }
}
</script>

