<template>
  <v-container fluid class="vendor-chats-page">
    <!-- Header -->
    <v-row>
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h1 class="text-h4 mb-2">چت‌های من</h1>
            <p class="text-grey">مدیریت پیام‌های مشتریان</p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-refresh"
            @click="fetchRooms"
            :loading="loading"
          >
            بروزرسانی
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <!-- Chat Queue -->
      <v-col cols="12" md="4">
        <v-card height="700" elevation="3" class="chat-list-card">
          <!-- Header with search -->
          <v-card-title class="chat-list-header">
            <div class="w-100">
              <div class="d-flex align-center justify-space-between mb-3">
                <span class="text-white font-weight-bold">
                  <v-icon class="ml-2">mdi-chat-processing</v-icon>
                  صف چت‌ها
                </span>
                <v-chip
                  v-if="unreadCount > 0"
                  size="small"
                  color="error"
                  class="pulse-chip"
                >
                  {{ unreadCount }}
                </v-chip>
              </div>
              
              <!-- Search -->
              <v-text-field
                v-model="searchQuery"
                placeholder="جستجو..."
                variant="outlined"
                density="compact"
                hide-details
                clearable
                prepend-inner-icon="mdi-magnify"
                class="search-field"
                bg-color="white"
              />
            </div>
          </v-card-title>

          <!-- Filter chips -->
          <div class="px-3 py-2 filter-section">
            <v-chip-group v-model="selectedFilter" mandatory>
              <v-chip
                value="all"
                size="small"
                filter
              >
                همه ({{ rooms.length }})
              </v-chip>
              <v-chip
                value="unread"
                size="small"
                filter
                :color="unreadCount > 0 ? 'error' : 'default'"
              >
                خوانده نشده ({{ unreadCount }})
              </v-chip>
            </v-chip-group>
          </div>

          <v-divider />

          <v-card-text class="pa-0 chat-list-content">
            <v-list v-if="!loading && filteredRooms.length > 0" class="py-0">
              <v-slide-y-transition group>
                <v-list-item
                  v-for="room in filteredRooms"
                  :key="room.room_id"
                  @click="selectRoom(room)"
                  :class="{
                    'chat-item-selected': selectedRoom?.room_id === room.room_id,
                    'chat-item-unread': room.unread_count > 0
                  }"
                  class="chat-list-item"
                >
                  <template #prepend>
                    <v-badge
                      :model-value="room.unread_count > 0"
                      :content="room.unread_count"
                      color="error"
                      overlap
                    >
                      <v-avatar :color="getAvatarColor(room.other_participant)" size="48">
                        <span class="text-white font-weight-bold">
                          {{ getInitials(room.other_participant) }}
                        </span>
                      </v-avatar>
                    </v-badge>
                  </template>

                  <v-list-item-title class="mb-1">
                    <span class="font-weight-bold">
                      {{ room.other_participant?.username || room.other_participant?.first_name || 'مشتری' }}
                    </span>
                    <span class="text-caption text-grey mr-2">
                      {{ formatTime(room.updated_at) }}
                    </span>
                  </v-list-item-title>

                  <v-list-item-subtitle v-if="room.product_name" class="mb-1">
                    <v-chip
                      size="x-small"
                      color="primary"
                      variant="tonal"
                      prepend-icon="mdi-package-variant"
                    >
                      {{ room.product_name }}
                    </v-chip>
                  </v-list-item-subtitle>

                  <v-list-item-subtitle v-if="room.last_message" class="last-message-preview">
                    {{ room.last_message.content }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-slide-y-transition>
            </v-list>

            <div v-else-if="loading" class="empty-state">
              <v-progress-circular indeterminate color="primary" size="48" />
              <p class="text-grey mt-4">در حال بارگذاری...</p>
            </div>

            <div v-else class="empty-state">
              <v-icon size="80" color="grey-lighten-2">mdi-chat-outline</v-icon>
              <p class="text-h6 text-grey mt-4">
                {{ searchQuery ? 'چتی یافت نشد' : 'هنوز چتی ندارید' }}
              </p>
              <p class="text-caption text-grey">
                مشتریان می‌توانند از صفحه محصول با شما چت کنند
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Chat Conversation -->
      <v-col cols="12" md="8">
        <v-card v-if="selectedRoom" height="700" elevation="3" class="chat-room-card">
          <v-card-title class="chat-room-header">
            <v-avatar :color="getAvatarColor(selectedRoom.other_participant)" size="40" class="ml-2">
              <span class="text-white font-weight-bold">
                {{ getInitials(selectedRoom.other_participant) }}
              </span>
            </v-avatar>
            <div class="flex-grow-1">
              <div class="font-weight-bold">
                {{ selectedRoom.other_participant?.username || selectedRoom.other_participant?.first_name || 'مشتری' }}
              </div>
              <div v-if="selectedRoom.product_name" class="text-caption text-grey">
                درباره: {{ selectedRoom.product_name }}
              </div>
            </div>
            <v-btn
              v-if="selectedRoom.product_id"
              size="small"
              variant="tonal"
              color="primary"
              :to="`/products/${selectedRoom.product_id}`"
              target="_blank"
            >
              <v-icon class="ml-1" size="small">mdi-open-in-new</v-icon>
              مشاهده محصول
            </v-btn>
          </v-card-title>

          <v-card-text class="pa-0">
            <ChatRoom :room-id="selectedRoom.room_id" @back="() => {}" />
          </v-card-text>
        </v-card>

        <v-card v-else height="700" elevation="3" class="empty-chat-card">
          <div class="empty-state">
            <v-icon size="120" color="primary" class="empty-icon">mdi-chat-processing-outline</v-icon>
            <p class="text-h5 text-grey mt-6 mb-2">یک چت را انتخاب کنید</p>
            <p class="text-body-2 text-grey">
              مشتریان شما می‌توانند از صفحه محصول با شما چت کنند
            </p>
            <v-btn
              color="primary"
              variant="tonal"
              class="mt-4"
              prepend-icon="mdi-help-circle"
              href="/docs/chat-guide"
              target="_blank"
            >
              راهنمای چت
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="mt-4">
      <v-col cols="12" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="primary" class="ml-3">mdi-chat</v-icon>
              <div>
                <div class="text-h5">{{ rooms.length }}</div>
                <div class="text-caption text-grey">کل چت‌ها</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="warning" class="ml-3">mdi-email-alert</v-icon>
              <div>
                <div class="text-h5">{{ unreadCount }}</div>
                <div class="text-caption text-grey">پیام‌های جدید</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" color="success" class="ml-3">mdi-clock-outline</v-icon>
              <div>
                <div class="text-h5">{{ activeToday }}</div>
                <div class="text-caption text-grey">فعال امروز</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Response Templates (Optional) -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>پاسخ‌های سریع</v-card-title>
          <v-card-text>
            <v-chip-group>
              <v-chip
                v-for="(template, index) in quickResponses"
                :key="index"
                @click="useQuickResponse(template)"
              >
                {{ template }}
              </v-chip>
            </v-chip-group>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

definePageMeta({
  middleware: ['authenticated', 'vendor'],
  layout: 'default',
})

const rooms = ref<any[]>([])
const selectedRoom = ref<any>(null)
const loading = ref(true)
const searchQuery = ref('')
const selectedFilter = ref<'all' | 'unread'>('all')
const refreshInterval = ref<NodeJS.Timeout | null>(null)

const quickResponses = ref([
  'سلام، چطور می‌تونم کمکتون کنم؟',
  'این محصول موجود هست',
  'زمان ارسال 2-3 روز کاری است',
  'برای اطلاعات بیشتر تماس بگیرید',
  'متشکرم از خریدتون',
])

const unreadCount = computed(() => {
  return rooms.value.reduce((sum, room) => sum + room.unread_count, 0)
})

const activeToday = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return rooms.value.filter(r => new Date(r.updated_at) >= today).length
})

const filteredRooms = computed(() => {
  let filtered = rooms.value

  // Apply filter
  if (selectedFilter.value === 'unread') {
    filtered = filtered.filter(r => r.unread_count > 0)
  }

  // Apply search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(r => {
      const username = (r.other_participant?.username || r.other_participant?.first_name || '').toLowerCase()
      const productName = (r.product_name || '').toLowerCase()
      return username.includes(query) || productName.includes(query)
    })
  }

  return filtered
})

const getInitials = (user: any) => {
  if (!user) return '؟'
  const name = user.username || user.first_name || 'مشتری'
  
  if (/[\u0600-\u06FF]/.test(name)) {
    return name.charAt(0)
  }
  
  return name.charAt(0).toUpperCase()
}

const getAvatarColor = (user: any) => {
  const colors = [
    '#4CAF50', '#388E3C', '#2E7D32', '#66BB6A',
    '#81C784', '#00796B', '#0097A7', '#689F38'
  ]
  
  const username = user?.username || user?.first_name || 'user'
  const hash = username.split('').reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc)
  }, 0)
  
  return colors[Math.abs(hash) % colors.length]
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'الان'
  if (minutes < 60) return `${minutes}د`
  if (hours < 24) return `${hours}س`
  if (days < 7) return `${days}روز`
  
  return date.toLocaleDateString('fa-IR', { month: 'numeric', day: 'numeric' })
}

const selectRoom = (room: any) => {
  selectedRoom.value = room
}

const useQuickResponse = (template: string) => {
  // TODO: Insert template into chat input
  console.log('Quick response:', template)
}

const fetchRooms = async () => {
  loading.value = true
  try {
    const data = await useApiFetch<any[]>('chat/vendor/rooms/')
    rooms.value = data
    
    // Sort by updated_at descending
    rooms.value.sort((a, b) => {
      return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    })
  } catch (error) {
    console.error('Failed to fetch rooms:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchRooms()
  
  // Auto-refresh every 30 seconds
  refreshInterval.value = setInterval(fetchRooms, 30000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
.vendor-chats-page {
  padding-top: 20px;
  direction: rtl;
}

.chat-list-card,
.chat-room-card,
.empty-chat-card {
  border-radius: 16px !important;
  overflow: hidden;
}

.chat-list-header {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  padding: 16px !important;
}

.search-field {
  border-radius: 8px;
}

.filter-section {
  background-color: rgb(var(--v-theme-surface));
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.pulse-chip {
  animation: pulse-chip 2s infinite;
}

@keyframes pulse-chip {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.chat-list-content {
  height: calc(100% - 180px);
  overflow-y: auto;
}

.chat-list-item {
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  cursor: pointer;
  transition: all 0.2s;
  padding: 12px 16px !important;
}

.chat-list-item:hover {
  background-color: rgba(76, 175, 80, 0.08);
  transform: translateX(-2px);
}

.chat-item-selected {
  background-color: rgba(76, 175, 80, 0.12) !important;
  border-right: 4px solid #4CAF50;
}

.chat-item-unread {
  background-color: rgba(76, 175, 80, 0.05);
}

.last-message-preview {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.chat-room-header {
  background-color: rgb(var(--v-theme-surface));
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
  padding: 16px !important;
}

.empty-chat-card,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 48px 24px;
}

.empty-icon {
  opacity: 0.3;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Custom scrollbar */
.chat-list-content::-webkit-scrollbar {
  width: 6px;
}

.chat-list-content::-webkit-scrollbar-track {
  background: transparent;
}

.chat-list-content::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-on-surface), 0.2);
  border-radius: 3px;
}

.chat-list-content::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-on-surface), 0.3);
}

@media (max-width: 960px) {
  .vendor-chats-page {
    padding-top: 10px;
  }
  
  .chat-list-card,
  .chat-room-card,
  .empty-chat-card {
    height: auto !important;
    min-height: 500px;
  }
}

@media (max-width: 600px) {
  .chat-list-card {
    margin-bottom: 16px;
  }
}
</style>

