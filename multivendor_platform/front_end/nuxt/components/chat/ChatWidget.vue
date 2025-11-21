<template>
  <div class="chat-widget">
    <!-- Floating Chat Button -->
    <v-btn
      v-if="!panelOpen"
      color="primary"
      size="large"
      elevation="8"
      class="chat-fab"
      @click="togglePanel"
    >
      <v-badge
        v-if="totalUnreadCount > 0"
        :content="totalUnreadCount"
        color="error"
        overlap
      >
        <v-icon size="large">mdi-chat</v-icon>
      </v-badge>
      <v-icon v-else size="large">mdi-chat</v-icon>
    </v-btn>

    <!-- Chat Panel -->
    <v-card
      v-if="panelOpen"
      class="chat-panel"
      elevation="12"
    >
      <!-- Header -->
      <v-card-title class="d-flex justify-space-between align-center bg-primary">
        <span class="text-white">گفتگوها</span>
        <div>
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
      </v-card-title>

      <!-- Content -->
      <v-card-text class="pa-0" style="height: 400px; overflow: hidden;">
        <ChatPanel v-if="!currentRoomId" @select-room="handleRoomSelect" />
        <ChatRoom v-else :room-id="currentRoomId" @back="() => currentRoomId = null" />
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { useChatStore } from '~/stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { widgetOpen, currentRoomId, totalUnreadCount } = storeToRefs(chatStore)

const panelOpen = widgetOpen  // Use store's widgetOpen state

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

// Watch for currentRoomId changes to ensure room is selected
watch(() => chatStore.currentRoomId, (newRoomId) => {
  if (newRoomId && !widgetOpen.value) {
    widgetOpen.value = true
  }
})

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
  bottom: 20px;
  left: 20px;
  z-index: 1000;
  direction: rtl;
}

.chat-fab {
  position: fixed;
  bottom: 20px;
  left: 20px;
}

.chat-panel {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 380px;
  max-width: 90vw;
  height: 500px;
  display: flex;
  flex-direction: column;
}

@media (max-width: 600px) {
  .chat-widget {
    bottom: 10px;
    left: 10px;
  }
  
  .chat-fab {
    bottom: 10px;
    left: 10px;
  }
  
  .chat-panel {
    bottom: 10px;
    left: 10px;
    right: 10px;
    width: auto;
    height: 80vh;
  }
}
</style>

