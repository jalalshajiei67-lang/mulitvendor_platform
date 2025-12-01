<template>
  <div class="chat-panel-content">
    <!-- Loading State -->
    <div v-if="loading" class="d-flex justify-center align-center pa-4">
      <v-progress-circular indeterminate color="primary" />
    </div>

    <!-- Empty State -->
    <div v-else-if="rooms.length === 0" class="text-center pa-4">
      <v-icon size="64" color="grey-lighten-1">mdi-chat-outline</v-icon>
      <p class="text-grey mt-2">هنوز گفتگویی ندارید</p>
      <p class="text-caption text-grey">برای شروع گفتگو، به صفحه محصول بروید</p>
    </div>

    <!-- Room List -->
    <v-list v-else class="pa-0">
      <v-list-item
        v-for="room in rooms"
        :key="room.room_id"
        @click="selectRoom(room.room_id)"
        :class="{ 'bg-grey-lighten-4': room.unread_count > 0 }"
      >
        <template #prepend>
          <v-avatar color="primary">
            <span class="text-white">{{ getInitials(room.other_participant) }}</span>
          </v-avatar>
        </template>

        <v-list-item-title>
          {{ room.other_participant?.username || 'کاربر' }}
          <v-chip
            v-if="room.unread_count > 0"
            size="x-small"
            color="primary"
            class="mr-2"
          >
            {{ room.unread_count }}
          </v-chip>
        </v-list-item-title>

        <v-list-item-subtitle v-if="room.product_name">
          <v-icon size="small" class="ml-1">mdi-package-variant</v-icon>
          {{ room.product_name }}
        </v-list-item-subtitle>

        <v-list-item-subtitle v-if="room.last_message">
          <span class="text-truncate d-inline-block" style="max-width: 200px;">
            {{ room.last_message.content }}
          </span>
        </v-list-item-subtitle>

        <template #append>
          <div class="text-caption text-grey">
            {{ formatTime(room.updated_at) }}
          </div>
        </template>
      </v-list-item>
    </v-list>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '~/stores/chat'

const chatStore = useChatStore()
const loading = ref(true)

const rooms = computed(() => chatStore.rooms)

const selectRoom = (roomId: string) => {
  // Emit event to parent to switch to chat room view
  emit('selectRoom', roomId)
}

const getInitials = (user: any) => {
  if (!user) return '?'
  const username = user.username || user.first_name || 'U'
  return username.charAt(0).toUpperCase()
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'الان'
  if (minutes < 60) return `${minutes} دقیقه پیش`
  if (hours < 24) return `${hours} ساعت پیش`
  if (days < 7) return `${days} روز پیش`
  
  return date.toLocaleDateString('fa-IR')
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
  overflow-y: auto;
  direction: rtl;
}

.v-list-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  cursor: pointer;
  transition: background-color 0.2s;
}

.v-list-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}
</style>







