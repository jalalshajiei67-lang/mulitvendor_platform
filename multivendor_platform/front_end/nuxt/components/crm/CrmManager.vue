<template>
  <div class="crm-manager" dir="rtl">
    <v-row>
      <!-- Contacts List -->
      <v-col cols="12" md="4" v-if="!selectedContact">
        <ContactList
          :contacts="contacts"
          :loading="contactsLoading"
          @select="handleSelectContact"
          @create="showContactForm = true"
          @search="handleSearch"
        />
      </v-col>

      <!-- Tasks List -->
      <v-col cols="12" md="4" v-if="!selectedContact && !showContactForm && !showTaskForm">
        <TaskList
          :tasks="tasks"
          :loading="tasksLoading"
          @create="showTaskForm = true"
          @edit="handleEditTask"
          @delete="handleDeleteTask"
          @complete="handleCompleteTask"
          @cancel="handleCancelTask"
        />
      </v-col>

      <!-- Contact Detail or Forms -->
      <v-col cols="12" :md="selectedContact ? 12 : 4">
        <!-- Contact Detail -->
        <ContactDetail
          v-if="selectedContact && !showContactForm && !showTaskForm"
          :contact="selectedContact"
          :notes="contactNotes"
          :tasks="contactTasks"
          :notes-loading="notesLoading"
          :tasks-loading="tasksLoading"
          @back="handleBackToMain"
          @edit="handleEditContact"
          @note-created="handleCreateNote"
          @note-updated="handleUpdateNote"
          @note-deleted="handleDeleteNote"
          @task-created="handleCreateTask"
          @task-updated="handleUpdateTask"
          @task-deleted="handleDeleteTask"
        />

        <!-- Contact Form -->
        <v-card v-else-if="showContactForm" elevation="2" rounded="xl">
          <v-card-title>
            {{ editingContact ? 'ویرایش مخاطب' : 'افزودن مخاطب' }}
          </v-card-title>
          <v-card-text>
            <ContactForm
              :contact="editingContact"
              :loading="contactSaving"
              @submit="handleSaveContact"
              @cancel="cancelContactForm"
            />
          </v-card-text>
        </v-card>

        <!-- Task Form -->
        <v-card v-else-if="showTaskForm" elevation="2" rounded="xl">
          <v-card-title>
            {{ editingTask ? 'ویرایش یادآوری' : 'افزودن یادآوری' }}
          </v-card-title>
          <v-card-text>
            <TaskForm
              :task="editingTask"
              :contacts="contacts"
              :loading="taskSaving"
              @submit="handleSaveTask"
              @cancel="cancelTaskForm"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useCrmApi, type SellerContact, type ContactNote, type ContactTask } from '~/composables/useCrmApi'
import ContactList from './ContactList.vue'
import ContactDetail from './ContactDetail.vue'
import ContactForm from './ContactForm.vue'
import TaskList from './TaskList.vue'
import TaskForm from './TaskForm.vue'

const crmApi = useCrmApi()

// State
const contacts = ref<SellerContact[]>([])
const tasks = ref<ContactTask[]>([])
const selectedContact = ref<SellerContact | null>(null)
const contactNotes = ref<ContactNote[]>([])
const contactTasks = ref<ContactTask[]>([])

// Loading states
const contactsLoading = ref(false)
const tasksLoading = ref(false)
const notesLoading = ref(false)
const contactSaving = ref(false)
const taskSaving = ref(false)

// UI states
const showContactForm = ref(false)
const showTaskForm = ref(false)
const editingContact = ref<SellerContact | null>(null)
const editingTask = ref<ContactTask | null>(null)

// Snackbar
const snackbar = ref(false)
const snackbarColor = ref('success')
const snackbarMessage = ref('')

// Load data
const loadContacts = async (search?: string) => {
  contactsLoading.value = true
  try {
    contacts.value = await crmApi.getContacts(search)
  } catch (error) {
    showSnackbar('خطا در بارگذاری مخاطبین', 'error')
  } finally {
    contactsLoading.value = false
  }
}

const loadTasks = async () => {
  tasksLoading.value = true
  try {
    tasks.value = await crmApi.getTasks()
  } catch (error) {
    showSnackbar('خطا در بارگذاری یادآوری‌ها', 'error')
  } finally {
    tasksLoading.value = false
  }
}

const loadContactNotes = async (contactId: number) => {
  notesLoading.value = true
  try {
    contactNotes.value = await crmApi.getContactNotes(contactId)
  } catch (error) {
    showSnackbar('خطا در بارگذاری یادداشت‌ها', 'error')
  } finally {
    notesLoading.value = false
  }
}

const loadContactTasks = async (contactId: number) => {
  try {
    const allTasks = await crmApi.getTasks({ contact: contactId })
    contactTasks.value = allTasks
  } catch (error) {
    showSnackbar('خطا در بارگذاری یادآوری‌ها', 'error')
  }
}

// Contact handlers
const handleSelectContact = async (contact: SellerContact) => {
  selectedContact.value = contact
  await Promise.all([
    loadContactNotes(contact.id),
    loadContactTasks(contact.id)
  ])
}

const handleBackToMain = () => {
  selectedContact.value = null
  contactNotes.value = []
  contactTasks.value = []
}

const handleSearch = (query: string) => {
  loadContacts(query)
}

const handleEditContact = (contact: SellerContact) => {
  editingContact.value = contact
  showContactForm.value = true
}

const handleSaveContact = async (data: Partial<SellerContact>) => {
  contactSaving.value = true
  try {
    if (editingContact.value) {
      await crmApi.updateContact(editingContact.value.id, data)
      showSnackbar('مخاطب با موفقیت به‌روزرسانی شد', 'success')
    } else {
      await crmApi.createContact(data)
      showSnackbar('مخاطب با موفقیت ایجاد شد', 'success')
    }
    await loadContacts()
    cancelContactForm()
  } catch (error) {
    showSnackbar('خطا در ذخیره مخاطب', 'error')
  } finally {
    contactSaving.value = false
  }
}

const cancelContactForm = () => {
  showContactForm.value = false
  editingContact.value = null
}

// Note handlers
const handleCreateNote = async (note: ContactNote) => {
  try {
    if (selectedContact.value) {
      await crmApi.createNote(selectedContact.value.id, note.content)
      showSnackbar('یادداشت با موفقیت ایجاد شد', 'success')
      await loadContactNotes(selectedContact.value.id)
    }
  } catch (error) {
    showSnackbar('خطا در ایجاد یادداشت', 'error')
  }
}

const handleUpdateNote = async (note: ContactNote) => {
  try {
    await crmApi.updateNote(note.id, note.content)
    showSnackbar('یادداشت با موفقیت به‌روزرسانی شد', 'success')
    if (selectedContact.value) {
      await loadContactNotes(selectedContact.value.id)
    }
  } catch (error) {
    showSnackbar('خطا در به‌روزرسانی یادداشت', 'error')
  }
}

const handleDeleteNote = async (id: number) => {
  try {
    await crmApi.deleteNote(id)
    showSnackbar('یادداشت با موفقیت حذف شد', 'success')
    if (selectedContact.value) {
      await loadContactNotes(selectedContact.value.id)
    }
  } catch (error) {
    showSnackbar('خطا در حذف یادداشت', 'error')
  }
}

// Task handlers
const handleEditTask = (task: ContactTask) => {
  editingTask.value = task
  showTaskForm.value = true
}

const handleSaveTask = async (data: Partial<ContactTask>) => {
  taskSaving.value = true
  try {
    if (editingTask.value) {
      await crmApi.updateTask(editingTask.value.id, data)
      showSnackbar('یادآوری با موفقیت به‌روزرسانی شد', 'success')
    } else {
      await crmApi.createTask(data)
      showSnackbar('یادآوری با موفقیت ایجاد شد', 'success')
    }
    await loadTasks()
    if (selectedContact.value) {
      await loadContactTasks(selectedContact.value.id)
    }
    cancelTaskForm()
  } catch (error) {
    showSnackbar('خطا در ذخیره یادآوری', 'error')
  } finally {
    taskSaving.value = false
  }
}

const handleDeleteTask = async (task: ContactTask) => {
  try {
    await crmApi.deleteTask(task.id)
    showSnackbar('یادآوری با موفقیت حذف شد', 'success')
    await loadTasks()
    if (selectedContact.value) {
      await loadContactTasks(selectedContact.value.id)
    }
  } catch (error) {
    showSnackbar('خطا در حذف یادآوری', 'error')
  }
}

const handleCompleteTask = async (task: ContactTask) => {
  try {
    await crmApi.completeTask(task.id)
    showSnackbar('یادآوری به عنوان تکمیل شده علامت‌گذاری شد', 'success')
    await loadTasks()
    if (selectedContact.value) {
      await loadContactTasks(selectedContact.value.id)
    }
  } catch (error) {
    showSnackbar('خطا در تکمیل یادآوری', 'error')
  }
}

const handleCancelTask = async (task: ContactTask) => {
  try {
    await crmApi.cancelTask(task.id)
    showSnackbar('یادآوری لغو شد', 'success')
    await loadTasks()
    if (selectedContact.value) {
      await loadContactTasks(selectedContact.value.id)
    }
  } catch (error) {
    showSnackbar('خطا در لغو یادآوری', 'error')
  }
}

const handleCreateTask = async (task: ContactTask) => {
  await handleSaveTask(task)
}

const handleUpdateTask = async (task: ContactTask) => {
  await handleSaveTask(task)
}

const cancelTaskForm = () => {
  showTaskForm.value = false
  editingTask.value = null
}

// Watch for contact selection changes
watch(selectedContact, (newContact) => {
  if (!newContact) {
    contactNotes.value = []
    contactTasks.value = []
  }
})

// Utility
const showSnackbar = (message: string, color: string = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

// Initialize
onMounted(async () => {
  await Promise.all([
    loadContacts(),
    loadTasks()
  ])
})
</script>

<style scoped>
.crm-manager {
  width: 100%;
}
</style>

