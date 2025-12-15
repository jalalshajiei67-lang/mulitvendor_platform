<template>
  <v-form ref="formRef" @submit.prevent="handleSubmit">
    <v-text-field
      v-model="formData.name"
      label="نام و نام خانوادگی"
      required
      :rules="[rules.required]"
      variant="outlined"
      density="comfortable"
      class="mb-3"
    ></v-text-field>

    <v-text-field
      v-model="formData.company_name"
      label="نام شرکت"
      variant="outlined"
      density="comfortable"
      class="mb-3"
    ></v-text-field>

    <v-text-field
      v-model="formData.phone"
      label="شماره تلفن"
      required
      :rules="[rules.required]"
      variant="outlined"
      density="comfortable"
      class="mb-3"
    ></v-text-field>

    <v-textarea
      v-model="formData.address"
      label="آدرس"
      variant="outlined"
      density="comfortable"
      rows="3"
      class="mb-3"
    ></v-textarea>

    <v-textarea
      v-model="formData.notes"
      label="یادداشت"
      variant="outlined"
      density="comfortable"
      rows="3"
      class="mb-3"
    ></v-textarea>

    <v-card-actions class="pa-0">
      <v-spacer></v-spacer>
      <v-btn variant="text" @click="$emit('cancel')">انصراف</v-btn>
      <v-btn type="submit" color="primary" :loading="loading">ذخیره</v-btn>
    </v-card-actions>
  </v-form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { SellerContact } from '~/composables/useCrmApi'

const props = withDefaults(defineProps<{
  contact?: SellerContact | null
  loading?: boolean
}>(), {
  contact: null,
  loading: false
})

const emit = defineEmits<{
  submit: [data: Partial<SellerContact>]
  cancel: []
}>()

const formRef = ref()
const formData = ref<Partial<SellerContact> & { name?: string }>({
  name: '',
  company_name: '',
  phone: '',
  address: '',
  notes: ''
})

const rules = {
  required: (value: string) => !!value || 'این فیلد الزامی است'
}

watch(() => props.contact, (contact) => {
  if (contact) {
    const fullName = [contact.first_name, contact.last_name].filter(Boolean).join(' ')
    formData.value = {
      name: fullName,
      company_name: contact.company_name || '',
      phone: contact.phone || '',
      address: contact.address || '',
      notes: contact.notes || ''
    }
  } else {
    formData.value = {
      name: '',
      company_name: '',
      phone: '',
      address: '',
      notes: ''
    }
  }
}, { immediate: true })

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate()
  if (valid) {
    // Split name into first_name and last_name
    const nameParts = (formData.value.name || '').trim().split(/\s+/)
    const first_name = nameParts[0] || ''
    const last_name = nameParts.slice(1).join(' ') || ''
    
    const submitData: Partial<SellerContact> = {
      first_name,
      last_name,
      company_name: formData.value.company_name,
      phone: formData.value.phone,
      address: formData.value.address,
      notes: formData.value.notes
    }
    
    emit('submit', submitData)
  }
}
</script>

