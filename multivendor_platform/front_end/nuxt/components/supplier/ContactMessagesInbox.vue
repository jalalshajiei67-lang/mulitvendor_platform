<template>
  <div class="contact-messages-inbox" dir="rtl">
    <v-card elevation="2">
      <v-card-title class="text-h5 font-weight-bold d-flex align-center justify-space-between">
        <div>
          <v-icon color="primary" class="me-2">mdi-email-inbox</v-icon>
          صندوق پیام‌ها
          <v-badge v-if="unreadCount > 0" :content="unreadCount" color="error" inline class="ms-2"></v-badge>
        </div>
        <v-btn-group density="compact">
          <v-btn
            :variant="filter === 'all' ? 'flat' : 'outlined'"
            size="small"
            @click="filter = 'all'"
          >
            همه ({{ messages.length }})
          </v-btn>
          <v-btn
            :variant="filter === 'unread' ? 'flat' : 'outlined'"
            size="small"
            @click="filter = 'unread'"
          >
            خوانده نشده ({{ unreadCount }})
          </v-btn>
        </v-btn-group>
      </v-card-title>

      <v-card-text class="pa-0">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <!-- Messages List -->
        <v-list v-else-if="filteredMessages.length > 0" lines="three">
          <template v-for="(message, index) in filteredMessages" :key="message.id">
            <v-list-item
              :class="{'message-unread': !message.is_read}"
              @click="openMessage(message)"
            >
              <template v-slot:prepend>
                <v-avatar :color="message.is_read ? 'grey-lighten-1' : 'primary'">
                  <v-icon color="white">{{ message.is_read ? 'mdi-email-open' : 'mdi-email' }}</v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-bold">
                {{ message.sender_name }}
              </v-list-item-title>
              
              <v-list-item-subtitle class="mb-1">
                <v-icon size="x-small" class="me-1">mdi-email</v-icon>
                {{ message.sender_email }}
                <span v-if="message.sender_phone" class="ms-2">
                  <v-icon size="x-small" class="me-1">mdi-phone</v-icon>
                  {{ message.sender_phone }}
                </span>
              </v-list-item-subtitle>

              <v-list-item-subtitle class="font-weight-medium">
                {{ message.subject }}
              </v-list-item-subtitle>

              <template v-slot:append>
                <div class="text-caption text-medium-emphasis">
                  {{ formatDate(message.created_at) }}
                </div>
              </template>
            </v-list-item>

            <v-divider v-if="index < filteredMessages.length - 1"></v-divider>
          </template>
        </v-list>

        <!-- Empty State -->
        <div v-else class="text-center py-8">
          <v-icon size="80" color="grey-lighten-2">mdi-email-off</v-icon>
          <h3 class="text-h6 mt-3">پیامی وجود ندارد</h3>
          <p class="text-body-2 text-medium-emphasis">
            {{ filter === 'unread' ? 'همه پیام‌ها خوانده شده‌اند' : 'هنوز پیامی دریافت نشده است' }}
          </p>
        </div>
      </v-card-text>
    </v-card>

    <!-- Message Detail Dialog -->
    <v-dialog v-model="messageDialog" max-width="700">
      <v-card v-if="selectedMessage">
        <v-card-title class="d-flex align-center justify-space-between">
          <span class="text-h6">{{ selectedMessage.subject }}</span>
          <v-btn
            icon="mdi-close"
            variant="text"
            @click="messageDialog = false"
          ></v-btn>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text>
          <!-- Sender Info -->
          <v-card class="mb-4" variant="outlined">
            <v-card-text class="pa-3">
              <div class="d-flex align-center mb-2">
                <v-avatar color="primary" size="40" class="me-2">
                  <span class="text-white">{{ selectedMessage.sender_name.charAt(0).toUpperCase() }}</span>
                </v-avatar>
                <div>
                  <div class="font-weight-bold">{{ selectedMessage.sender_name }}</div>
                  <div class="text-caption text-medium-emphasis">
                    {{ formatDate(selectedMessage.created_at) }}
                  </div>
                </div>
              </div>
              <v-divider class="my-2"></v-divider>
              <div class="text-body-2">
                <div class="mb-1">
                  <v-icon size="small" class="me-1">mdi-email</v-icon>
                  <a :href="`mailto:${selectedMessage.sender_email}`">{{ selectedMessage.sender_email }}</a>
                </div>
                <div v-if="selectedMessage.sender_phone">
                  <v-icon size="small" class="me-1">mdi-phone</v-icon>
                  <a :href="`tel:${selectedMessage.sender_phone}`">{{ selectedMessage.sender_phone }}</a>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Message Content -->
          <div class="message-content">
            <p style="white-space: pre-line; line-height: 1.8;">{{ selectedMessage.message }}</p>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="primary"
            prepend-icon="mdi-reply"
            :href="`mailto:${selectedMessage.sender_email}?subject=Re: ${selectedMessage.subject}`"
          >
            پاسخ
          </v-btn>
          <v-btn
            v-if="selectedMessage.is_read"
            variant="outlined"
            prepend-icon="mdi-email"
            @click="markAsUnread(selectedMessage)"
          >
            علامت به عنوان خوانده نشده
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            icon="mdi-delete"
            variant="text"
            color="error"
            @click="confirmDelete(selectedMessage)"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">حذف پیام</v-card-title>
        <v-card-text>
          آیا مطمئن هستید که می‌خواهید این پیام را حذف کنید؟
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" :loading="deleting" @click="deleteMessage">حذف</v-btn>
          <v-btn variant="text" @click="deleteDialog = false">انصراف</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSupplierContactApi, type SupplierContactMessage } from '~/composables/useSupplierContactApi'

const contactApi = useSupplierContactApi()

const messages = ref<SupplierContactMessage[]>([])
const loading = ref(false)
const filter = ref<'all' | 'unread'>('all')
const messageDialog = ref(false)
const deleteDialog = ref(false)
const selectedMessage = ref<SupplierContactMessage | null>(null)
const messageToDelete = ref<SupplierContactMessage | null>(null)
const deleting = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const unreadCount = computed(() => {
  return messages.value.filter(m => !m.is_read).length
})

const filteredMessages = computed(() => {
  if (filter.value === 'unread') {
    return messages.value.filter(m => !m.is_read)
  }
  return messages.value
})

const loadMessages = async () => {
  loading.value = true
  try {
    messages.value = await contactApi.getContactMessages()
  } catch (error) {
    console.error('Error loading messages:', error)
  } finally {
    loading.value = false
  }
}

const openMessage = async (message: SupplierContactMessage) => {
  selectedMessage.value = message
  messageDialog.value = true

  // Mark as read if not already
  if (!message.is_read) {
    try {
      await contactApi.markMessageRead(message.id!)
      message.is_read = true
    } catch (error) {
      console.error('Error marking message as read:', error)
    }
  }
}

const markAsUnread = async (message: SupplierContactMessage) => {
  try {
    await contactApi.markMessageUnread(message.id!)
    message.is_read = false
    snackbarMessage.value = 'پیام به عنوان خوانده نشده علامت‌گذاری شد'
    snackbarColor.value = 'success'
    snackbar.value = true
    messageDialog.value = false
  } catch (error) {
    console.error('Error marking message as unread:', error)
  }
}

const confirmDelete = (message: SupplierContactMessage) => {
  messageToDelete.value = message
  deleteDialog.value = true
}

const deleteMessage = async () => {
  if (!messageToDelete.value) return

  deleting.value = true

  try {
    await contactApi.deleteContactMessage(messageToDelete.value.id!)
    snackbarMessage.value = 'پیام با موفقیت حذف شد'
    snackbarColor.value = 'success'
    snackbar.value = true
    deleteDialog.value = false
    messageDialog.value = false
    await loadMessages()
  } catch (error) {
    console.error('Error deleting message:', error)
    snackbarMessage.value = 'خطا در حذف پیام'
    snackbarColor.value = 'error'
    snackbar.value = true
  } finally {
    deleting.value = false
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return 'امروز ' + new Intl.DateTimeFormat('fa-IR', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  } else if (diffDays === 1) {
    return 'دیروز'
  } else if (diffDays < 7) {
    return `${diffDays} روز پیش`
  } else {
    return new Intl.DateTimeFormat('fa-IR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date)
  }
}

onMounted(() => {
  loadMessages()
})
</script>

<style scoped>
.message-unread {
  background-color: rgba(var(--v-theme-primary), 0.05);
  font-weight: 500;
}

.message-content {
  background-color: rgba(var(--v-theme-surface), 0.5);
  border-radius: 8px;
  padding: 16px;
  border-left: 3px solid rgb(var(--v-theme-primary));
}
</style>

