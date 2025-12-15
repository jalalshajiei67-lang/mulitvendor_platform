<template>
  <div class="contact-detail" dir="rtl">
    <v-card elevation="2" rounded="xl" v-if="contact">
      <v-card-title class="d-flex align-center justify-space-between">
        <div class="d-flex align-center gap-3">
          <v-btn
            icon="mdi-arrow-right"
            variant="text"
            @click="$emit('back')"
            class="me-2"
          ></v-btn>
          <v-avatar color="primary" size="56">
            <span class="text-white text-h5">
              {{ getInitials(contact) }}
            </span>
          </v-avatar>
          <div>
            <div class="text-h6 font-weight-bold">
              {{ getFullName(contact) }}
            </div>
            <div v-if="contact.company_name" class="text-body-2 text-medium-emphasis">
              {{ contact.company_name }}
            </div>
          </div>
        </div>
        <v-btn
          icon="mdi-pencil"
          variant="text"
          @click="$emit('edit', contact)"
        ></v-btn>
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text>
        <!-- Contact Info -->
        <v-row class="mb-4">
          <v-col cols="12" md="6">
            <div class="mb-3">
              <div class="text-caption text-medium-emphasis mb-1">شماره تلفن</div>
              <div class="text-body-1">
                <v-icon size="small" class="me-1">mdi-phone</v-icon>
                <a :href="`tel:${contact.phone}`">{{ contact.phone }}</a>
              </div>
            </div>
          </v-col>
          <v-col cols="12" v-if="contact.address">
            <div class="mb-3">
              <div class="text-caption text-medium-emphasis mb-1">آدرس</div>
              <div class="text-body-1">{{ contact.address }}</div>
            </div>
          </v-col>
          <v-col cols="12" v-if="contact.notes">
            <div class="mb-3">
              <div class="text-caption text-medium-emphasis mb-1">یادداشت</div>
              <div class="text-body-1" style="white-space: pre-line">{{ contact.notes }}</div>
            </div>
          </v-col>
        </v-row>

        <v-divider class="my-4"></v-divider>

        <!-- Tabs for Notes and Tasks -->
        <v-tabs v-model="tab" class="mb-4">
          <v-tab value="notes">
            یادداشت‌ها ({{ notes.length }})
          </v-tab>
          <v-tab value="tasks">
            یادآوری‌ها ({{ tasks.length }})
          </v-tab>
        </v-tabs>

        <v-window v-model="tab">
          <v-window-item value="notes">
            <div class="mb-4">
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="showNoteForm = true"
              >
                افزودن یادداشت
              </v-btn>
            </div>

            <div v-if="notesLoading" class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>

            <div v-else-if="notes.length > 0">
              <NoteCard
                v-for="note in notes"
                :key="note.id"
                :note="note"
                @edit="handleEditNote"
                @delete="handleDeleteNote"
              />
            </div>

            <div v-else class="text-center py-8">
              <v-icon size="64" color="grey-lighten-2">mdi-note-outline</v-icon>
              <p class="text-body-1 text-medium-emphasis mt-2">یادداشتی وجود ندارد</p>
            </div>
          </v-window-item>

          <v-window-item value="tasks">
            <div class="mb-4">
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="showTaskForm = true"
              >
                افزودن یادآوری
              </v-btn>
            </div>

            <div v-if="tasksLoading" class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>

            <div v-else-if="tasks.length > 0">
              <v-list lines="two">
                <v-list-item
                  v-for="task in tasks"
                  :key="task.id"
                  class="mb-2 rounded-lg"
                >
                  <v-list-item-title>{{ task.title }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ formatDate(task.due_date) }} - {{ task.priority_display }}
                  </v-list-item-subtitle>
                  <template v-slot:append>
                    <v-chip
                      :color="getStatusColor(task.status)"
                      size="small"
                      variant="tonal"
                    >
                      {{ task.status_display }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </div>

            <div v-else class="text-center py-8">
              <v-icon size="64" color="grey-lighten-2">mdi-checkbox-blank-outline</v-icon>
              <p class="text-body-1 text-medium-emphasis mt-2">یادآوری وجود ندارد</p>
            </div>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

    <!-- Note Form Dialog -->
    <v-dialog v-model="showNoteForm" max-width="600">
      <v-card>
        <v-card-title>
          {{ editingNote ? 'ویرایش یادداشت' : 'افزودن یادداشت' }}
        </v-card-title>
        <v-card-text>
          <v-textarea
            v-model="noteContent"
            label="محتوا"
            required
            rows="5"
            variant="outlined"
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="cancelNoteForm">انصراف</v-btn>
          <v-btn color="primary" @click="saveNote" :loading="noteSaving">ذخیره</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Task Form Dialog -->
    <v-dialog v-model="showTaskForm" max-width="600">
      <v-card>
        <v-card-title>
          {{ editingTask ? 'ویرایش یادآوری' : 'افزودن یادآوری' }}
        </v-card-title>
        <v-card-text>
          <TaskForm
            :task="editingTask"
            :contacts="[contact]"
            :loading="taskSaving"
            @submit="handleSaveTask"
            @cancel="cancelTaskForm"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import type { SellerContact, ContactNote, ContactTask } from '~/composables/useCrmApi'
import NoteCard from './NoteCard.vue'
import TaskForm from './TaskForm.vue'
import { formatDate } from '~/utils/date'

const props = defineProps<{
  contact: SellerContact
  notes: ContactNote[]
  tasks: ContactTask[]
  notesLoading?: boolean
  tasksLoading?: boolean
}>()

const emit = defineEmits<{
  back: []
  edit: [contact: SellerContact]
  noteCreated: [note: ContactNote]
  noteUpdated: [note: ContactNote]
  noteDeleted: [id: number]
  taskCreated: [task: ContactTask]
  taskUpdated: [task: ContactTask]
  taskDeleted: [id: number]
}>()

const tab = ref('notes')
const showNoteForm = ref(false)
const showTaskForm = ref(false)
const editingNote = ref<ContactNote | null>(null)
const editingTask = ref<ContactTask | null>(null)
const noteContent = ref('')
const noteSaving = ref(false)
const taskSaving = ref(false)

const getInitials = (contact: SellerContact) => {
  const first = contact.first_name?.charAt(0) || ''
  const last = contact.last_name?.charAt(0) || ''
  return (first + last).toUpperCase() || '?'
}

const getFullName = (contact: SellerContact) => {
  const parts = [contact.first_name, contact.last_name].filter(Boolean)
  return parts.join(' ') || contact.phone || 'بدون نام'
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'success'
    case 'cancelled': return 'error'
    case 'pending': return 'warning'
    default: return 'grey'
  }
}

const handleEditNote = (note: ContactNote) => {
  editingNote.value = note
  noteContent.value = note.content
  showNoteForm.value = true
}

const handleDeleteNote = (note: ContactNote) => {
  emit('noteDeleted', note.id)
}

const cancelNoteForm = () => {
  showNoteForm.value = false
  editingNote.value = null
  noteContent.value = ''
}

const saveNote = async () => {
  if (!noteContent.value.trim()) return
  
  noteSaving.value = true
  try {
    if (editingNote.value) {
      emit('noteUpdated', { ...editingNote.value, content: noteContent.value } as ContactNote)
    } else {
      emit('noteCreated', {
        id: 0,
        contact: props.contact.id,
        seller: 0,
        content: noteContent.value,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      } as ContactNote)
    }
    cancelNoteForm()
  } finally {
    noteSaving.value = false
  }
}

const handleSaveTask = (taskData: Partial<ContactTask>) => {
  taskSaving.value = true
  try {
    const task = {
      ...taskData,
      contact: props.contact.id,
      id: editingTask.value?.id || 0,
      seller: 0,
      created_at: editingTask.value?.created_at || new Date().toISOString(),
      updated_at: new Date().toISOString()
    } as ContactTask
    
    if (editingTask.value) {
      emit('taskUpdated', task)
    } else {
      emit('taskCreated', task)
    }
    cancelTaskForm()
  } finally {
    taskSaving.value = false
  }
}

const cancelTaskForm = () => {
  showTaskForm.value = false
  editingTask.value = null
}
</script>

<style scoped>
.contact-detail {
  width: 100%;
}
</style>

