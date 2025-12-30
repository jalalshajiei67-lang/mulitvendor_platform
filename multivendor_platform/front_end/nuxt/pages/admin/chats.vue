<template>
  <v-container fluid class="admin-chats-page">
    <!-- Header -->
    <v-row>
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h1 class="text-h4 mb-2">
              <v-icon class="ml-2" color="primary">mdi-shield-account</v-icon>
              مدیریت چتها
            </h1>
            <p class="text-grey">نظارت و مدیریت تمام چتها</p>
          </div>
          <div class="d-flex gap-2">
            <v-btn
              color="primary"
              prepend-icon="mdi-refresh"
              @click="fetchRooms"
              :loading="loading"
              variant="tonal"
            >
              بروزرسانی
            </v-btn>
            <v-btn
              color="success"
              prepend-icon="mdi-download"
              variant="outlined"
            >
              خروجی Excel
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row class="mb-4">
      <v-col cols="12" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text>
            <div class="d-flex align-center">
              <v-avatar color="primary" size="48" class="ml-3">
                <v-icon color="white">mdi-chat</v-icon>
              </v-avatar>
              <div>
                <div class="text-h5 font-weight-bold">{{ totalRooms }}</div>
                <div class="text-caption text-grey">کل چتها</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text>
            <div class="d-flex align-center">
              <v-avatar color="warning" size="48" class="ml-3">
                <v-icon color="white">mdi-email-alert</v-icon>
              </v-avatar>
              <div>
                <div class="text-h5 font-weight-bold">{{ totalUnread }}</div>
                <div class="text-caption text-grey">خوانده نشده</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text>
            <div class="d-flex align-center">
              <v-avatar color="success" size="48" class="ml-3">
                <v-icon color="white">mdi-clock-check</v-icon>
              </v-avatar>
              <div>
                <div class="text-h5 font-weight-bold">{{ activeToday }}</div>
                <div class="text-caption text-grey">فعال امروز</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="stat-card" elevation="2">
          <v-card-text>
            <div class="d-flex align-center">
              <v-avatar color="info" size="48" class="ml-3">
                <v-icon color="white">mdi-message-text</v-icon>
              </v-avatar>
              <div>
                <div class="text-h5 font-weight-bold">{{ totalMessages }}</div>
                <div class="text-caption text-grey">کل پیام‌ها</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Chat Rooms List -->
      <v-col cols="12" md="4">
        <v-card height="700" elevation="3" class="chat-list-card">
          <!-- Header with search -->
          <v-card-title class="chat-list-header">
            <div class="w-100">
              <div class="d-flex align-center justify-space-between mb-3">
                <span class="text-white font-weight-bold">
                  <v-icon class="ml-2">mdi-format-list-bulleted</v-icon>
                  لیست چتها
                </span>
                <v-chip size="small" color="white" text-color="primary">
                  {{ filteredRooms.length }}
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
                @update:model-value="handleSearch"
              />
            </div>
          </v-card-title>

          <v-divider />

          <v-card-text class="pa-0 chat-list-content">
            <v-list v-if="!loading && filteredRooms.length > 0" class="py-0">
              <v-slide-y-transition group>
                <v-list-item
                  v-for="room in filteredRooms"
                  :key="room.room_id"
                  @click="selectRoom(room)"
                  :class="{ 'chat-item-selected': selectedRoom?.room_id === room.room_id }"
                  class="chat-list-item"
                >
                  <template #prepend>
                    <v-badge
                      :model-value="room.unread_count > 0"
                      :content="room.unread_count"
                      color="error"
                      overlap
                    >
                      <v-avatar color="primary" size="48">
                        <v-icon color="white">mdi-account-group</v-icon>
                      </v-avatar>
                    </v-badge>
                  </template>

                  <v-list-item-title class="mb-1">
                    <span class="font-weight-bold">{{ getRoomTitle(room) }}</span>
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

                  <template #append>
                    <div class="text-caption text-grey">
                      {{ formatDate(room.updated_at) }}
                    </div>
                  </template>
                </v-list-item>
              </v-slide-y-transition>
            </v-list>

            <div v-else-if="loading" class="empty-state">
              <v-progress-circular indeterminate color="primary" size="48" />
              <p class="text-grey mt-4">در حال بارگذاری...</p>
            </div>

            <div v-else class="empty-state">
              <v-icon size="80" color="grey-lighten-2">mdi-chat-search</v-icon>
              <p class="text-h6 text-grey mt-4">چتی یافت نشد</p>
              <p class="text-caption text-grey">
                {{ searchQuery ? 'عبارت دیگری جستجو کنید' : 'هنوز چتی وجود ندارد' }}
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Selected Chat -->
      <v-col cols="12" md="8">
        <v-card v-if="selectedRoom" height="700" elevation="3" class="chat-room-card">
          <v-card-title class="chat-room-header">
            <v-avatar color="primary" size="40" class="ml-2">
              <v-icon color="white">mdi-account-group</v-icon>
            </v-avatar>
            <div class="flex-grow-1">
              <div class="font-weight-bold">{{ getRoomTitle(selectedRoom) }}</div>
              <div v-if="selectedRoom.product_name" class="text-caption text-grey">
                محصول: {{ selectedRoom.product_name }}
              </div>
            </div>
            <v-chip
              size="small"
              :color="selectedRoom.is_archived ? 'grey' : 'success'"
              variant="flat"
            >
              {{ selectedRoom.is_archived ? 'بایگانی شده' : 'فعال' }}
            </v-chip>
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
              برای مشاهده جزئیات چت، از لیست سمت راست انتخاب کنید
            </p>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Statistics -->
    <v-row class="mt-4">
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-primary">{{ totalRooms }}</div>
            <div class="text-caption text-grey">کل چتها</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-warning">{{ totalUnread }}</div>
            <div class="text-caption text-grey">پیام‌های خوانده نشده</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-success">{{ activeToday }}</div>
            <div class="text-caption text-grey">فعال امروز</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h4 text-info">{{ totalMessages }}</div>
            <div class="text-caption text-grey">کل پیام‌ها</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

definePageMeta({
  middleware: ['authenticated', 'admin'],
  layout: 'default',
})

const searchQuery = ref('')
const rooms = ref<any[]>([])
const selectedRoom = ref<any>(null)
const loading = ref(true)
const refreshInterval = ref<NodeJS.Timeout | null>(null)

const totalRooms = computed(() => rooms.value.length)
const totalUnread = computed(() => rooms.value.reduce((sum, r) => sum + r.unread_count, 0))
const activeToday = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return rooms.value.filter(r => new Date(r.updated_at) >= today).length
})
const totalMessages = computed(() => {
  return rooms.value.reduce((sum, r) => {
    return sum + (r.last_message ? 1 : 0)
  }, 0)
})

const filteredRooms = computed(() => {
  if (!searchQuery.value) return rooms.value

  const query = searchQuery.value.toLowerCase()
  return rooms.value.filter(r => {
    const title = getRoomTitle(r).toLowerCase()
    const productName = (r.product_name || '').toLowerCase()
    const lastMessage = (r.last_message?.content || '').toLowerCase()
    
    return title.includes(query) || 
           productName.includes(query) || 
           lastMessage.includes(query)
  })
})

const getRoomTitle = (room: any) => {
  const participants = room.participants_details || []
  if (participants.length === 0) return 'چت'
  
  return participants
    .map((p: any) => p.username || p.first_name || 'کاربر')
    .join(' و ')
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (hours < 1) return 'الان'
  if (hours < 24) return `${hours}س پیش`
  if (days < 7) return `${days}روز پیش`
  
  return date.toLocaleDateString('fa-IR', { month: 'short', day: 'numeric' })
}

const selectRoom = (room: any) => {
  selectedRoom.value = room
}

const handleSearch = () => {
  // Search is now handled by computed property
}

const fetchRooms = async () => {
  loading.value = true
  try {
    const data = await useApiFetch<any[]>('chat/admin/rooms/')
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
  
  // Auto-refresh every 45 seconds
  refreshInterval.value = setInterval(fetchRooms, 45000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
.admin-chats-page {
  padding-top: 80px;
  direction: rtl;
}

.stat-card {
  border-radius: 12px !important;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
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

.chat-list-content {
  height: calc(100% - 130px);
  overflow-y: auto;
}

.chat-list-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
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

.last-message-preview {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #666;
}

.chat-room-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
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
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.chat-list-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

@media (max-width: 960px) {
  .admin-chats-page {
    padding-top: 72px;
  }
  
  .chat-list-card,
  .chat-room-card,
  .empty-chat-card {
    height: auto !important;
    min-height: 500px;
  }
}

@media (max-width: 600px) {
  .admin-chats-page {
    padding-top: 64px;
  }

  .stat-card {
    margin-bottom: 12px;
  }
  
  .chat-list-card {
    margin-bottom: 16px;
  }
}
</style>

