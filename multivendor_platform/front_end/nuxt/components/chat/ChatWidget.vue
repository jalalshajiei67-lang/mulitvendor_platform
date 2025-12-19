<template>
  <div class="chat-widget">
    <!-- Connection Status Indicator -->
    <v-slide-y-transition>
      <v-alert
        v-if="!isConnected && panelOpen"
        type="warning"
        density="compact"
        class="connection-alert"
        closable
      >
        <template #prepend>
          <v-progress-circular indeterminate size="16" width="2" />
        </template>
        در حال اتصال مجدد...
      </v-alert>
    </v-slide-y-transition>

    <!-- Floating Chat Button - Perfect Round -->
    <v-scale-transition>
      <button
        v-if="!panelOpen"
        class="chat-fab"
        @click="togglePanel"
        :class="{ 'has-unread': totalUnreadCount > 0 }"
      >
        <v-badge
          v-if="totalUnreadCount > 0"
          :content="totalUnreadCount > 99 ? '99+' : totalUnreadCount"
          color="error"
          overlap
          floating
          class="chat-badge"
        >
          <div class="chat-icon-wrapper">
            <v-icon size="28" color="white">mdi-chat</v-icon>
          </div>
        </v-badge>
        <div v-else class="chat-icon-wrapper">
          <v-icon size="28" color="white">mdi-chat</v-icon>
        </div>
        
        <!-- Online Status Dot -->
        <span 
          class="status-dot"
          :class="{ 'status-online': isConnected, 'status-offline': !isConnected }"
        />
        
        <!-- Ripple Effect -->
        <span class="ripple-effect"></span>
      </button>
    </v-scale-transition>

    <!-- Chat Panel -->
    <v-slide-y-reverse-transition>
      <v-card
        v-if="panelOpen"
        class="chat-panel"
        elevation="24"
      >
        <!-- Header -->
        <v-card-title class="chat-header">
          <div class="d-flex align-center w-100">
            <v-icon class="ml-2" color="white">mdi-chat-processing</v-icon>
            <span class="text-white flex-grow-1">چت‌ها</span>
            
            <!-- Connection Status -->
            <v-tooltip location="bottom">
              <template #activator="{ props }">
                <v-chip
                  v-bind="props"
                  size="x-small"
                  :color="isConnected ? 'success' : 'error'"
                  variant="flat"
                  class="ml-2 status-chip"
                >
                  <v-icon start size="x-small">
                    {{ isConnected ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                  </v-icon>
                  {{ isConnected ? 'آنلاین' : 'آفلاین' }}
                </v-chip>
              </template>
              <span>{{ isConnected ? 'متصل به سرور' : 'در حال اتصال مجدد...' }}</span>
            </v-tooltip>

            <!-- Actions -->
            <div class="header-actions">
              <v-btn
                icon
                size="small"
                variant="text"
                class="text-white"
                @click="minimizePanel"
              >
                <v-icon>mdi-minus</v-icon>
              </v-btn>
              <v-btn
                icon
                size="small"
                variant="text"
                class="text-white"
                @click="closePanel"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
          </div>
        </v-card-title>

        <!-- Content -->
        <v-card-text class="pa-0 chat-content">
          <v-fade-transition mode="out-in">
            <ChatPanel 
              v-if="!currentRoomId" 
              @select-room="handleRoomSelect"
              :key="'panel'"
            />
            <ChatRoom 
              v-else 
              :room-id="currentRoomId" 
              @back="handleBack"
              :key="'room-' + currentRoomId"
            />
          </v-fade-transition>
        </v-card-text>

        <!-- Footer with Quick Actions -->
        <v-divider />
        <div class="chat-footer">
          <v-btn
            variant="text"
            size="small"
            @click="handleRefresh"
            :loading="refreshing"
          >
            <v-icon start>mdi-refresh</v-icon>
            بروزرسانی
          </v-btn>
          
          <v-spacer />
          
          <v-menu location="top">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                icon
                size="small"
                variant="text"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list density="compact">
              <v-list-item @click="toggleSoundNotifications">
                <template #prepend>
                  <v-icon>{{ soundEnabled ? 'mdi-volume-high' : 'mdi-volume-off' }}</v-icon>
                </template>
                <v-list-item-title>
                  {{ soundEnabled ? 'غیرفعال کردن صدا' : 'فعال کردن صدا' }}
                </v-list-item-title>
              </v-list-item>
              <v-list-item @click="markAllAsRead">
                <template #prepend>
                  <v-icon>mdi-check-all</v-icon>
                </template>
                <v-list-item-title>خواندن همه</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </v-card>
    </v-slide-y-reverse-transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useChatStore } from '~/stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { widgetOpen, currentRoomId, totalUnreadCount, isConnected } = storeToRefs(chatStore)

const panelOpen = widgetOpen
const refreshing = ref(false)
const soundEnabled = ref(true)

// Load sound preference from localStorage
onMounted(() => {
  if (process.client) {
    const savedPref = localStorage.getItem('chatSoundEnabled')
    if (savedPref !== null) {
      soundEnabled.value = savedPref === 'true'
    }
  }
})

const togglePanel = () => {
  chatStore.toggleWidget()
}

const minimizePanel = () => {
  chatStore.closeWidget()
}

const closePanel = () => {
  chatStore.closeWidget()
}

const handleRoomSelect = (roomId: string) => {
  chatStore.openRoom(roomId)
}

const handleBack = () => {
  currentRoomId.value = null
}

const handleRefresh = async () => {
  refreshing.value = true
  try {
    await chatStore.fetchRooms()
  } catch (error) {
    console.error('Failed to refresh rooms:', error)
  } finally {
    refreshing.value = false
  }
}

const toggleSoundNotifications = () => {
  soundEnabled.value = !soundEnabled.value
  if (process.client) {
    localStorage.setItem('chatSoundEnabled', soundEnabled.value.toString())
  }
}

const markAllAsRead = () => {
  chatStore.rooms.forEach(room => {
    if (room.unread_count > 0) {
      chatStore.markAsRead(room.room_id)
    }
  })
}

// Watch for currentRoomId changes
watch(() => chatStore.currentRoomId, (newRoomId) => {
  if (newRoomId && !widgetOpen.value) {
    widgetOpen.value = true
  }
})

// Watch for new messages to play sound
watch(() => chatStore.totalUnreadCount, (newCount, oldCount) => {
  if (newCount > oldCount && soundEnabled.value && process.client) {
    playNotificationSound()
  }
})

const playNotificationSound = () => {
  try {
    const audio = new Audio('/sounds/notification.mp3')
    audio.volume = 0.5
    audio.play().catch(() => {
      // Silent fail if audio doesn't play
    })
  } catch (error) {
    // Silent fail
  }
}

onMounted(() => {
  chatStore.initializeChat()
})

onUnmounted(() => {
  chatStore.disconnectWebSocket()
})
</script>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 80px;
  right: 20px;
  z-index: 2000 !important;
  direction: rtl;
}

  .chat-fab {
    width: 64px;
    height: 64px;
    min-width: 64px;
    padding: 0;
    margin: 0;
    border: none;
    border-radius: 50%;
    background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 8px 24px rgba(76, 175, 80, 0.4), 
                0 4px 8px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: visible;
  }
  
  .chat-fab:hover {
    transform: scale(1.08);
    box-shadow: 0 12px 32px rgba(76, 175, 80, 0.5), 
                0 6px 12px rgba(0, 0, 0, 0.3);
  }
  
  .chat-fab:active {
    transform: scale(0.95);
  }
  
  .chat-fab.has-unread {
    animation: pulse-glow 2s ease-in-out infinite;
  }

.chat-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 2;
}

.chat-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  z-index: 10;
}

.chat-badge :deep(.v-badge__badge) {
  font-size: 11px;
  font-weight: 700;
  min-width: 22px;
  height: 22px;
  padding: 0 6px;
  border: 2px solid white;
  background-color: #f44336 !important;
  color: white !important;
  animation: badge-bounce 0.5s ease-out;
}

  @keyframes pulse-glow {
    0%, 100% {
      box-shadow: 0 8px 24px rgba(76, 175, 80, 0.4), 
                  0 4px 8px rgba(0, 0, 0, 0.2);
    }
    50% {
      box-shadow: 0 8px 32px rgba(76, 175, 80, 0.6), 
                  0 4px 12px rgba(0, 0, 0, 0.25),
                  0 0 20px rgba(76, 175, 80, 0.3);
    }
  }

@keyframes badge-bounce {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.ripple-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  pointer-events: none;
  opacity: 0;
}

.chat-fab:active .ripple-effect {
  animation: ripple 0.6s ease-out;
}

@keyframes ripple {
  0% {
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    width: 100px;
    height: 100px;
    opacity: 0;
  }
}

.status-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2.5px solid white;
  background-color: #4caf50;
  transition: all 0.3s ease;
  z-index: 3;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.status-online {
  background-color: #4caf50;
  animation: status-pulse-online 2s ease-in-out infinite;
}

.status-offline {
  background-color: #f44336;
  animation: status-pulse-offline 2s ease-in-out infinite;
}

@keyframes status-pulse-online {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  50% {
    transform: scale(1.4);
    box-shadow: 0 0 0 4px rgba(76, 175, 80, 0);
  }
}

@keyframes status-pulse-offline {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
    box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.7);
  }
  50% {
    transform: scale(1.4);
    opacity: 0.7;
    box-shadow: 0 0 0 4px rgba(244, 67, 54, 0);
  }
}

.chat-panel {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 420px;
  max-width: 90vw;
  height: 600px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  border-radius: 16px !important;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3) !important;
  z-index: 2000 !important;
}

.chat-header {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  padding: 16px !important;
}

.status-chip {
  font-size: 10px !important;
  height: 20px !important;
}

.header-actions {
  display: flex;
  gap: 4px;
}

.chat-content {
  height: calc(600px - 130px);
  overflow: hidden;
  background-color: #f5f5f5;
}

.chat-footer {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: white;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}

.connection-alert {
  position: fixed;
  bottom: 700px;
  right: 20px;
  width: 420px;
  max-width: 90vw;
  z-index: 2001 !important;
}

@media (max-width: 600px) {
  .chat-widget {
    bottom: 80px;
    right: 16px;
  }
  
  .chat-fab {
    width: 56px;
    height: 56px;
    min-width: 56px;
  }
  
  .chat-fab .chat-icon-wrapper .v-icon {
    font-size: 24px !important;
  }
  
  .status-dot {
    width: 12px;
    height: 12px;
    top: 4px;
    right: 4px;
    border-width: 2px;
  }
  
  .chat-panel {
    top: 0 !important;
    bottom: 0;
    right: 0;
    left: 0;
    width: 100vw;
    max-width: 100vw;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0 !important;
    z-index: 2000 !important;
  }

  .chat-content {
    height: calc(100vh - 130px);
  }

  .connection-alert {
    bottom: auto;
    top: 70px;
    right: 10px;
    left: 10px;
    width: auto;
    z-index: 2001 !important;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .chat-panel {
    background-color: #1e1e1e;
  }
  
  .chat-content {
    background-color: #121212;
  }
  
  .chat-footer {
    background-color: #1e1e1e;
    border-top-color: rgba(255, 255, 255, 0.12);
  }
}
</style>

