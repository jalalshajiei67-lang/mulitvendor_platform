<template>
  <div class="contact-list" dir="rtl">
    <v-card elevation="2" rounded="xl">
      <v-card-title class="d-flex align-center justify-space-between">
        <div class="d-flex align-center gap-3">
          <v-icon color="primary">mdi-account-group</v-icon>
          <span class="text-h6 font-weight-bold">لیست مخاطبین</span>
        </div>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="$emit('create')"
        >
          افزودن مخاطب
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Search -->
        <v-text-field
          v-model="searchQuery"
          prepend-inner-icon="mdi-magnify"
          label="جستجو (نام، تلفن)"
          variant="outlined"
          density="comfortable"
          clearable
          class="mb-4"
          @update:model-value="handleSearch"
        ></v-text-field>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <!-- Contacts List -->
        <v-list v-else-if="contacts.length > 0" lines="three">
          <v-list-item
            v-for="contact in contacts"
            :key="contact.id"
            @click="$emit('select', contact)"
            class="mb-2 rounded-lg"
          >
            <template v-slot:prepend>
              <v-avatar color="primary" size="48">
                <span class="text-white text-h6">
                  {{ getInitials(contact) }}
                </span>
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold">
              {{ getFullName(contact) }}
            </v-list-item-title>

            <v-list-item-subtitle>
              <div v-if="contact.company_name" class="mb-1">
                <v-icon size="small" class="me-1">mdi-office-building</v-icon>
                {{ contact.company_name }}
              </div>
              <div>
                <v-icon size="small" class="me-1">mdi-phone</v-icon>
                {{ contact.phone }}
              </div>
            </v-list-item-subtitle>

            <template v-slot:append>
              <div class="d-flex flex-column align-end gap-1">
                <v-chip size="small" color="info" variant="tonal">
                  {{ contact.notes_count || 0 }} یادداشت
                </v-chip>
                <v-chip size="small" color="warning" variant="tonal">
                  {{ contact.tasks_count || 0 }} یادآوری
                </v-chip>
              </div>
            </template>
          </v-list-item>
        </v-list>

        <!-- Empty State -->
        <div v-else class="text-center py-8">
          <v-icon size="80" color="grey-lighten-2">mdi-account-off</v-icon>
          <h3 class="text-h6 mt-3">مخاطبی وجود ندارد</h3>
          <p class="text-body-2 text-medium-emphasis mb-4">
            برای شروع، یک مخاطب جدید اضافه کنید
          </p>
          <v-btn color="primary" prepend-icon="mdi-plus" @click="$emit('create')">
            افزودن مخاطب
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { SellerContact } from '~/composables/useCrmApi'

defineProps<{
  contacts: SellerContact[]
  loading?: boolean
}>()

const emit = defineEmits<{
  select: [contact: SellerContact]
  create: []
  search: [query: string]
}>()

const searchQuery = ref('')

const getInitials = (contact: SellerContact) => {
  const first = contact.first_name?.charAt(0) || ''
  const last = contact.last_name?.charAt(0) || ''
  return (first + last).toUpperCase() || '?'
}

const getFullName = (contact: SellerContact) => {
  const parts = [contact.first_name, contact.last_name].filter(Boolean)
  return parts.join(' ') || contact.phone || 'بدون نام'
}

const handleSearch = (value: string) => {
  emit('search', value || '')
}

watch(searchQuery, (value) => {
  if (!value) {
    emit('search', '')
  }
})
</script>

<style scoped>
.contact-list {
  width: 100%;
}
</style>

