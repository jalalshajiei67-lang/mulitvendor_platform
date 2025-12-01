<template>
  <div class="chat-room">
    <!-- Header -->
    <div class="chat-room-header">
      <v-btn icon size="small" @click="emit('back')">
        <v-icon>mdi-arrow-right</v-icon>
      </v-btn>
      <div class="flex-grow-1 mr-2">
        <div class="font-weight-bold">
          {{ room?.other_participant?.username || 'کاربر' }}
        </div>
        <div v-if="room?.product_name" class="text-caption text-grey">
          {{ room.product_name }}
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div ref="messagesContainer" class="chat-messages">
      <div v-if="loading" class="text-center pa-4">
        <v-progress-circular indeterminate color="primary" size="32" />
      </div>

      <div v-else-if="messages.length === 0" class="text-center pa-4 text-grey">
        هنوز پیامی ارسال نشده است
      </div>

      <div v-else>
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', isOwnMessage(message) ? 'message-own' : 'message-other']"
        >
          <div class="message-bubble">
            <div class="message-sender" v-if="!isOwnMessage(message)">
              {{ message.sender_username }}
            </div>
            <div class="message-content">{{ message.content }}</div>
            <div class="message-time">
              {{ formatMessageTime(message.created_at) }}
              <v-icon
                v-if="isOwnMessage(message)"
                size="small"
                :color="message.is_read ? 'primary' : 'grey'"
                class="mr-1"
              >
                {{ message.is_read ? 'mdi-check-all' : 'mdi-check' }}
              </v-icon>
            </div>
          </div>
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="typingUsers.length > 0" class="message message-other">
        <div class="message-bubble typing-indicator">
          <span>{{ typingUsers[0].username }} در حال نوشتن</span>
          <span class="typing-dots">
            <span>.</span><span>.</span><span>.</span>
          </span>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="chat-input">
      <v-text-field
        v-model="messageText"
        placeholder="پیام خود را بنویسید..."
        variant="outlined"
        density="compact"
        hide-details
        @keydown.enter="sendMessage"
        @input="handleTyping"
      >
        <template #append-inner>
          <v-btn
            icon
            size="small"
            color="primary"
            :disabled="!messageText.trim()"
            @click="sendMessage"
          >
            <v-icon>mdi-send</v-icon>
          </v-btn>
        </template>
      </v-text-field>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useChatStore } from '~/stores/chat'
import { useAuthStore } from '~/stores/auth'

const props = defineProps<{
  roomId: string
}>()

const emit = defineEmits<{
  back: []
}>()

const chatStore = useChatStore()
const authStore = useAuthStore()

const messageText = ref('')
const loading = ref(true)
const messagesContainer = ref<HTMLElement | null>(null)
const typingTimeout = ref<NodeJS.Timeout | null>(null)

const room = computed(() => chatStore.rooms.find(r => r.room_id === props.roomId))
const messages = computed(() => chatStore.messages[props.roomId] || [])
const typingUsers = computed(() => chatStore.typingStatuses[props.roomId] || [])

const isOwnMessage = (message: any) => {
  if (authStore.user) {
    return message.sender === authStore.user.id
  }
  return false
}

const formatMessageTime = (timestamp: string) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' })
}

const sendMessage = () => {
  if (!messageText.value.trim()) return

  chatStore.sendMessage(props.roomId, messageText.value.trim())
  messageText.value = ''

  // Stop typing indicator
  chatStore.setTyping(props.roomId, false)
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
    typingTimeout.value = null
  }

  scrollToBottom()
}

const handleTyping = () => {
  // Send typing indicator
  chatStore.setTyping(props.roomId, true)

  // Clear previous timeout
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
  }

  // Stop typing after 3 seconds of inactivity
  typingTimeout.value = setTimeout(() => {
    chatStore.setTyping(props.roomId, false)
  }, 3000)
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(async () => {
  try {
    // Join room
    chatStore.joinRoom(props.roomId)

    // Fetch messages
    await chatStore.fetchMessages(props.roomId)

    // Mark as read
    chatStore.markAsRead(props.roomId)

    scrollToBottom()
  } catch (error) {
    console.error('Failed to load chat room:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.chat-room {
  display: flex;
  flex-direction: column;
  height: 100%;
  direction: rtl;
}

.chat-room-header {
  display: flex;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  background-color: #f5f5f5;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #fafafa;
}

.message {
  margin-bottom: 12px;
  display: flex;
}

.message-own {
  justify-content: flex-start;
}

.message-other {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 70%;
  padding: 8px 12px;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-own .message-bubble {
  background-color: #4caf50;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-other .message-bubble {
  background-color: white;
  color: #333;
  border-bottom-left-radius: 4px;
}

.message-sender {
  font-size: 12px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #666;
}

.message-content {
  word-wrap: break-word;
  line-height: 1.4;
}

.message-time {
  font-size: 11px;
  margin-top: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.message-own .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.message-other .message-time {
  color: #999;
}

.typing-indicator {
  background-color: #e0e0e0;
  color: #666;
}

.typing-dots span {
  animation: typing 1.4s infinite;
  margin-left: 2px;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.3;
  }
  30% {
    opacity: 1;
  }
}

.chat-input {
  padding: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
  background-color: white;
}
</style>







