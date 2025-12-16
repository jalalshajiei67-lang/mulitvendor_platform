<template>
  <div class="chat-panel-content">
    <!-- Search and Filter Bar -->
    <div class="search-bar">
      <v-text-field
        v-model="searchQuery"
        placeholder="جستجوی گفتگو..."
        variant="outlined"
        density="compact"
        hide-details
        clearable
        prepend-inner-icon="mdi-magnify"
        class="search-field"
      />
      
      <!-- Filter Chips -->
      <div class="filter-chips">
        <v-chip
          size="small"
          :color="filterType === 'all' ? 'primary' : 'default'"
          @click="filterType = 'all'"
          class="ml-1"
        >
          همه ({{ rooms.length }})
        </v-chip>
        <v-chip
          size="small"
          :color="filterType === 'unread' ? 'primary' : 'default'"
          @click="filterType = 'unread'"
          class="ml-1"
        >
          <v-badge
            v-if="unreadCount > 0"
            :content="unreadCount"
            color="error"
            inline
          >
            خوانده نشده
          </v-badge>
          <span v-else>خوانده نشده</span>
        </v-chip>
        <v-chip
          size="small"
          :color="filterType === 'archived' ? 'primary' : 'default'"
          @click="filterType = 'archived'"
          class="ml-1"
        >
          بایگانی
        </v-chip>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="d-flex justify-center align-center pa-8">
      <div class="text-center">
        <v-progress-circular indeterminate color="primary" size="48" />
        <p class="text-grey mt-4">در حال بارگذاری گفتگوها...</p>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredRooms.length === 0" class="empty-state">
      <v-icon size="80" color="grey-lighten-2">
        {{ searchQuery ? 'mdi-chat-search' : 'mdi-chat-outline' }}
      </v-icon>
      <p class="text-h6 text-grey mt-4 mb-2">
        {{ searchQuery ? 'گفتگویی یافت نشد' : 'هنوز گفتگویی ندارید' }}
      </p>
      <p class="text-caption text-grey">
        {{ searchQuery ? 'عبارت دیگری جستجو کنید' : 'برای شروع گفتگو، به صفحه محصول بروید' }}
      </p>
    </div>

    <!-- Room List -->
    <v-list v-else class="room-list">
      <v-slide-y-transition group>
        <v-list-item
          v-for="room in filteredRooms"
          :key="room.room_id"
          @click="selectRoom(room.room_id)"
          :class="{ 
            'room-unread': room.unread_count > 0,
            'room-item': true
          }"
          class="room-list-item"
        >
          <template #prepend>
            <v-badge
              :model-value="room.unread_count > 0"
              :content="room.unread_count"
              color="error"
              overlap
              offset-x="-5"
              offset-y="-5"
            >
              <v-avatar 
                :color="getAvatarColor(room.other_participant)"
                size="48"
              >
                <span class="text-white font-weight-bold text-h6">
                  {{ getInitials(room.other_participant) }}
                </span>
              </v-avatar>
            </v-badge>
          </template>

          <v-list-item-title class="d-flex align-center mb-1">
            <span class="font-weight-bold">
              {{ room.other_participant?.username || room.other_participant?.first_name || 'کاربر' }}
            </span>
            <v-spacer />
            <span class="text-caption text-grey">
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

          <v-list-item-subtitle v-if="room.last_message" class="last-message">
            <v-icon 
              v-if="isOwnMessage(room.last_message)"
              size="small" 
              class="ml-1"
              :color="room.last_message.is_read ? 'primary' : 'grey'"
            >
              {{ room.last_message.is_read ? 'mdi-check-all' : 'mdi-check' }}
            </v-icon>
            <span :class="{ 'font-weight-bold': room.unread_count > 0 }">
              {{ room.last_message.content }}
            </span>
          </v-list-item-subtitle>

          <template #append>
            <v-menu>
              <template #activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon
                  size="x-small"
                  variant="text"
                  @click.stop
                >
                  <v-icon size="small">mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list density="compact">
                <v-list-item @click="markAsRead(room.room_id)" v-if="room.unread_count > 0">
                  <template #prepend>
                    <v-icon size="small">mdi-check</v-icon>
                  </template>
                  <v-list-item-title>علامت خوانده شده</v-list-item-title>
                </v-list-item>
                <v-list-item @click="archiveRoom(room.room_id)">
                  <template #prepend>
                    <v-icon size="small">mdi-archive</v-icon>
                  </template>
                  <v-list-item-title>بایگانی</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-list-item>
      </v-slide-y-transition>
    </v-list>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '~/stores/chat'
import { useAuthStore } from '~/stores/auth'

const chatStore = useChatStore()
const authStore = useAuthStore()
const loading = ref(true)
const searchQuery = ref('')
const filterType = ref<'all' | 'unread' | 'archived'>('all')

const rooms = computed(() => chatStore.rooms)

const unreadCount = computed(() => {
  return rooms.value.filter(r => r.unread_count > 0).length
})

const filteredRooms = computed(() => {
  let filtered = rooms.value

  // Apply filter type
  if (filterType.value === 'unread') {
    filtered = filtered.filter(r => r.unread_count > 0)
  } else if (filterType.value === 'archived') {
    filtered = filtered.filter(r => r.is_archived)
  } else {
    filtered = filtered.filter(r => !r.is_archived)
  }

  // Apply search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(r => {
      const username = (r.other_participant?.username || r.other_participant?.first_name || '').toLowerCase()
      const productName = (r.product_name || '').toLowerCase()
      const lastMessage = (r.last_message?.content || '').toLowerCase()
      
      return username.includes(query) || 
             productName.includes(query) || 
             lastMessage.includes(query)
    })
  }

  return filtered
})

const selectRoom = (roomId: string) => {
  emit('selectRoom', roomId)
}

const getInitials = (user: any) => {
  if (!user) return '؟'
  const name = user.username || user.first_name || 'کاربر'
  
  // For Persian/Arabic names, take first character
  if (/[\u0600-\u06FF]/.test(name)) {
    return name.charAt(0)
  }
  
  // For English names
  return name.charAt(0).toUpperCase()
}

const getAvatarColor = (user: any) => {
  const colors = [
    '#4CAF50', '#388E3C', '#2E7D32', '#66BB6A',
    '#81C784', '#00796B', '#0097A7', '#F57C00',
    '#689F38', '#558B2F'
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

const isOwnMessage = (message: any) => {
  if (authStore.user) {
    return message.sender === authStore.user.id
  }
  return false
}

const markAsRead = (roomId: string) => {
  chatStore.markAsRead(roomId)
}

const archiveRoom = (roomId: string) => {
  // TODO: Implement archive functionality
  console.log('Archive room:', roomId)
}

const emit = defineEmits<{
  selectRoom: [roomId: string]
}>()

onMounted(async () => {
  try {
    await chatStore.fetchRooms()
  } catch (error) {
    console.error('Failed to load chat rooms:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.chat-panel-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  direction: rtl;
  background-color: #fafafa;
}

.search-bar {
  padding: 12px;
  background-color: white;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.search-field {
  margin-bottom: 8px;
}

.filter-chips {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
  flex: 1;
}

.room-list {
  flex: 1;
  overflow-y: auto;
  background-color: transparent;
  padding: 0 !important;
}

.room-list-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.2s;
  background-color: white;
  margin-bottom: 1px;
  padding: 12px 16px !important;
}

.room-list-item:hover {
  background-color: rgba(76, 175, 80, 0.08);
  transform: translateX(-2px);
}

.room-unread {
  background-color: rgba(76, 175, 80, 0.05);
}

.room-unread:hover {
  background-color: rgba(76, 175, 80, 0.12);
}

.last-message {
  display: flex;
  align-items: center;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 260px;
}

/* Custom scrollbar */
.room-list::-webkit-scrollbar {
  width: 6px;
}

.room-list::-webkit-scrollbar-track {
  background: transparent;
}

.room-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.room-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

@media (max-width: 600px) {
  .last-message {
    max-width: 200px;
  }
}
</style>









