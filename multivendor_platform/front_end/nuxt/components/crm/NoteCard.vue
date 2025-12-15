<template>
  <v-card elevation="1" rounded="lg" class="mb-3">
    <v-card-text class="pa-4">
      <div class="d-flex align-start justify-space-between">
        <div class="flex-grow-1">
          <p class="text-body-1 mb-2" style="white-space: pre-line">{{ note.content }}</p>
          <div class="text-caption text-medium-emphasis">
            {{ formatDate(note.created_at) }}
          </div>
        </div>
        <v-menu location="bottom end">
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi-dots-vertical" variant="text" size="small" v-bind="props"></v-btn>
          </template>
          <v-list>
            <v-list-item @click="$emit('edit', note)">
              <template v-slot:prepend>
                <v-icon>mdi-pencil</v-icon>
              </template>
              <v-list-item-title>ویرایش</v-list-item-title>
            </v-list-item>
            <v-list-item @click="$emit('delete', note)">
              <template v-slot:prepend>
                <v-icon color="error">mdi-delete</v-icon>
              </template>
              <v-list-item-title>حذف</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import type { ContactNote } from '~/composables/useCrmApi'
import { formatDate } from '~/utils/date'

defineProps<{
  note: ContactNote
}>()

defineEmits<{
  edit: [note: ContactNote]
  delete: [note: ContactNote]
}>()
</script>

