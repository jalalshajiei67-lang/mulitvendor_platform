<template>
  <div class="chat-room">
    <!-- Offline Banner -->
    <v-slide-y-transition>
      <div v-if="!chatStore.isConnected" class="offline-banner">
        <v-icon size="small" class="ml-2">mdi-wifi-off</v-icon>
        <span>ارتباط قطع شده است. پیام‌های شما پس از برقراری مجدد ارسال می‌شوند.</span>
      </div>
    </v-slide-y-transition>

    <!-- Header -->
    <div class="chat-room-header">
      <v-btn 
        icon 
        size="small" 
        variant="text"
        @click="emit('back')"
        class="back-btn"
      >
        <v-icon>mdi-arrow-right</v-icon>
      </v-btn>
      
      <v-avatar 
        :color="getAvatarColor(room?.other_participant)"
        size="40"
        class="mr-2"
      >
        <span class="text-white font-weight-bold">
          {{ getInitials(room?.other_participant) }}
        </span>
      </v-avatar>

      <div class="flex-grow-1">
        <div class="font-weight-bold">
          {{ room?.other_participant?.username || room?.other_participant?.first_name || 'کاربر' }}
        </div>
        <div class="text-caption" :class="isOtherUserTyping ? 'text-primary' : 'text-grey'">
          <span v-if="isOtherUserTyping">
            <v-icon size="x-small" class="typing-icon">mdi-circle</v-icon>
            در حال نوشتن...
          </span>
          <span v-else-if="room?.product_name">
            <v-icon size="x-small">mdi-package-variant</v-icon>
            {{ room.product_name }}
          </span>
        </div>
      </div>

      <v-menu>
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
          <v-list-item @click="clearMessages">
            <template #prepend>
              <v-icon size="small">mdi-delete-sweep</v-icon>
            </template>
            <v-list-item-title>پاک کردن پیام‌ها</v-list-item-title>
          </v-list-item>
          <v-list-item @click="viewProductDetails" v-if="room?.product">
            <template #prepend>
              <v-icon size="small">mdi-information</v-icon>
            </template>
            <v-list-item-title>مشاهده محصول</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>

    <!-- Messages -->
    <div ref="messagesContainer" class="chat-messages">
      <div v-if="loading" class="text-center pa-8">
        <v-progress-circular indeterminate color="primary" size="32" />
        <p class="text-grey mt-2">در حال بارگذاری پیام‌ها...</p>
      </div>

      <div v-else-if="messages.length === 0" class="empty-messages">
        <v-icon size="64" color="grey-lighten-2">mdi-chat-processing-outline</v-icon>
        <p class="text-grey mt-4">هنوز پیامی ارسال نشده است</p>
        <p class="text-caption text-grey">اولین پیام را ارسال کنید!</p>
      </div>

      <div v-else class="messages-list">
        <template v-for="(group, date) in groupedMessages" :key="date">
          <!-- Date Divider -->
          <div class="date-divider">
            <v-chip size="x-small" variant="tonal">
              {{ date }}
            </v-chip>
          </div>

          <!-- Messages for this date -->
          <div
            v-for="message in group"
            :key="message.id"
            :class="['message', isOwnMessage(message) ? 'message-own' : 'message-other']"
          >
            <!-- Avatar for own messages (shown on right in RTL) -->
            <v-avatar 
              v-if="isOwnMessage(message)"
              :color="getAvatarColor(authStore.user)"
              size="32"
              class="message-avatar message-avatar-own"
            >
              <span class="text-white text-caption font-weight-bold">
                {{ getInitials(authStore.user) }}
              </span>
            </v-avatar>

            <!-- Message Bubble -->
            <div class="message-bubble" :class="{'message-bubble-pending': message.status === 'pending', 'message-bubble-failed': message.status === 'failed'}">
              <div class="message-sender" v-if="!isOwnMessage(message)">
                {{ message.sender_username }}
              </div>
              <div class="message-content">{{ message.content }}</div>
              <div class="message-time">
                {{ formatMessageTime(message.created_at) }}
                <!-- Status indicators for own messages -->
                <template v-if="isOwnMessage(message)">
                  <!-- Sending/Pending -->
                  <v-icon
                    v-if="message.status === 'pending'"
                    size="x-small"
                    color="rgba(255,255,255,0.6)"
                    class="mr-1 rotating"
                  >
                    mdi-clock-outline
                  </v-icon>
                  <!-- Failed -->
                  <v-icon
                    v-else-if="message.status === 'failed'"
                    size="x-small"
                    color="rgba(255,100,100,0.9)"
                    class="mr-1"
                  >
                    mdi-alert-circle
                  </v-icon>
                  <!-- Sent (read/unread) -->
                  <v-icon
                    v-else
                    size="x-small"
                    :color="message.is_read ? 'white' : 'rgba(255,255,255,0.6)'"
                    class="mr-1"
                  >
                    {{ message.is_read ? 'mdi-check-all' : 'mdi-check' }}
                  </v-icon>
                </template>
              </div>
              
              <!-- Retry/Delete buttons for failed messages -->
              <div v-if="message.status === 'failed' && isOwnMessage(message)" class="message-actions">
                <v-btn
                  size="x-small"
                  variant="text"
                  color="white"
                  @click="retryMessage(message)"
                  class="retry-btn"
                >
                  <v-icon size="small">mdi-refresh</v-icon>
                  <span class="mr-1">تلاش مجدد</span>
                </v-btn>
                <v-btn
                  size="x-small"
                  variant="text"
                  color="white"
                  @click="deleteMessage(message)"
                  class="delete-btn"
                >
                  <v-icon size="small">mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>

            <!-- Avatar for other's messages (shown on left in RTL) -->
            <v-avatar 
              v-if="!isOwnMessage(message)"
              :color="getAvatarColor(room?.other_participant)"
              size="32"
              class="message-avatar message-avatar-other"
            >
              <span class="text-white text-caption font-weight-bold">
                {{ getInitials(room?.other_participant) }}
              </span>
            </v-avatar>
          </div>
        </template>
      </div>

      <!-- Typing Indicator -->
      <v-fade-transition>
        <div v-if="typingUsers.length > 0" class="message message-other">
          <div class="message-bubble typing-indicator">
            <div class="typing-animation">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
          <v-avatar 
            :color="getAvatarColor(room?.other_participant)"
            size="32"
            class="message-avatar message-avatar-other"
          >
            <span class="text-white text-caption font-weight-bold">
              {{ getInitials(room?.other_participant) }}
            </span>
          </v-avatar>
        </div>
      </v-fade-transition>

      <!-- Scroll to bottom button -->
      <v-fade-transition>
        <v-btn
          v-if="showScrollButton"
          icon
          size="small"
          color="primary"
          class="scroll-to-bottom"
          @click="scrollToBottom"
        >
          <v-icon>mdi-chevron-down</v-icon>
        </v-btn>
      </v-fade-transition>
    </div>

    <!-- Quick Replies -->
    <v-slide-y-reverse-transition>
      <div v-if="showQuickReplies && quickReplies.length > 0" class="quick-replies">
        <v-chip
          v-for="(reply, index) in quickReplies"
          :key="index"
          size="small"
          variant="outlined"
          @click="insertQuickReply(reply)"
          class="ml-1 mb-1"
        >
          {{ reply }}
        </v-chip>
      </div>
    </v-slide-y-reverse-transition>

    <!-- Input -->
    <div class="chat-input">
      <v-btn
        :disabled="!messageText.trim()"
        @click="sendMessage"
        :color="messageText.trim() ? 'primary' : 'grey'"
        class="send-btn"
        size="large"
        icon
        elevation="2"
      >
        <v-icon>mdi-send</v-icon>
      </v-btn>

      <v-textarea
        v-model="messageText"
        placeholder="پیام خود را بنویسید..."
        variant="outlined"
        density="comfortable"
        hide-details
        rows="1"
        auto-grow
        max-rows="4"
        @keydown.enter.exact.prevent="sendMessage"
        @keydown.shift.enter="handleShiftEnter"
        @input="handleTyping"
        class="message-input"
      />

      <v-btn
        icon
        size="small"
        variant="text"
        @click="showQuickReplies = !showQuickReplies"
        class="quick-reply-btn"
      >
        <v-icon>mdi-lightning-bolt</v-icon>
      </v-btn>

      <v-menu
        v-model="showEmojiPicker"
        :close-on-content-click="false"
        location="top"
      >
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            icon
            size="small"
            variant="text"
            class="emoji-btn"
          >
            <v-icon>mdi-emoticon-happy-outline</v-icon>
          </v-btn>
        </template>
        <v-card class="emoji-picker" max-width="300">
          <v-card-text class="pa-2">
            <div class="emoji-grid">
              <span
                v-for="emoji in commonEmojis"
                :key="emoji"
                class="emoji-item"
                @click="insertEmoji(emoji)"
              >
                {{ emoji }}
              </span>
            </div>
          </v-card-text>
        </v-card>
      </v-menu>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
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
const typingTimeout = ref<ReturnType<typeof setTimeout> | null>(null)
const showScrollButton = ref(false)
const showEmojiPicker = ref(false)
const showQuickReplies = ref(false)

const commonEmojis = [
  '😀', '😃', '😄', '😁', '😅', '😂', '🤣', '😊',
  '😇', '🙂', '😉', '😌', '😍', '🥰', '😘', '😗',
  '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨',
  '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞',
  '😔', '😟', '😕', '🙁', '😢', '😭', '😤', '😠',
  '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨',
  '👍', '👎', '👌', '✌️', '🤞', '🤟', '🤘', '👏',
  '🙌', '👐', '🤲', '🤝', '🙏', '💪', '❤️', '🧡',
  '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔',
  '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝',
  '✅', '❌', '⭐', '🌟', '💫', '✨', '🔥', '💯'
]

const quickReplies = [
  'سلام',
  'ممنون',
  'وقت بخیر',
  'ممنون میشم قیمت رو بفرمایید.',
  'موجود هست؟',
  'چه زمانی می تونید تحویل بدید؟',
]

const room = computed(() => chatStore.rooms.find(r => r.room_id === props.roomId))
const messages = computed(() => chatStore.messages[props.roomId] || [])
const typingUsers = computed(() => {
  const statuses = chatStore.typingStatuses[props.roomId] || []
  // Filter out own typing status
  return statuses.filter(s => s.user_id !== authStore.user?.id)
})

const isOtherUserTyping = computed(() => typingUsers.value.length > 0)

const groupedMessages = computed(() => {
  const grouped: Record<string, any[]> = {}
  
  messages.value.forEach(message => {
    const date = new Date(message.created_at)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    
    let dateKey = ''
    if (date.toDateString() === today.toDateString()) {
      dateKey = 'امروز'
    } else if (date.toDateString() === yesterday.toDateString()) {
      dateKey = 'دیروز'
    } else {
      dateKey = date.toLocaleDateString('fa-IR', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })
    }
    
    if (!grouped[dateKey]) {
      grouped[dateKey] = []
    }
    grouped[dateKey].push(message)
  })
  
  return grouped
})

const isOwnMessage = (message: any) => {
  if (authStore.user) {
    return message.sender === authStore.user.id
  }
  return false
}

const getInitials = (user: any) => {
  if (!user) return '؟'
  const name = user.username || user.first_name || user.email || 'کاربر'
  
  // For Persian/Arabic names, take first character
  if (/[\u0600-\u06FF]/.test(name)) {
    return name.charAt(0)
  }
  
  // For English names, take first character uppercase
  return name.charAt(0).toUpperCase()
}

const getAvatarColor = (user: any) => {
  const colors = [
    '#4CAF50', '#388E3C', '#2E7D32', '#66BB6A',
    '#81C784', '#00796B', '#0097A7', '#F57C00'
  ]
  
  const username = user?.username || user?.first_name || 'user'
  const hash = username.split('').reduce((acc: number, char: string) => {
    return char.charCodeAt(0) + ((acc << 5) - acc)
  }, 0)
  
  return colors[Math.abs(hash) % colors.length]
}

const formatMessageTime = (timestamp: string) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' })
}

const sendMessage = () => {
  // Prevent empty messages
  if (!messageText.value.trim()) return

  const content = messageText.value.trim()
  
  // Clear input immediately for better UX
  messageText.value = ''

  // Send message (now returns tempId)
  chatStore.sendMessage(props.roomId, content)

  // Stop typing indicator
  chatStore.setTyping(props.roomId, false)
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
    typingTimeout.value = null
  }

  scrollToBottom()
}

const handleShiftEnter = (event: KeyboardEvent) => {
  // Allow shift+enter to add new line (default textarea behavior)
  return true
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

const insertEmoji = (emoji: string) => {
  messageText.value += emoji
  showEmojiPicker.value = false
  // Focus back on input
  nextTick(() => {
    const textarea = document.querySelector('.message-input textarea') as HTMLTextAreaElement
    textarea?.focus()
  })
}

const insertQuickReply = (reply: string) => {
  messageText.value = reply
  showQuickReplies.value = false
}

const scrollToBottom = (smooth = true) => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({
        top: messagesContainer.value.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto'
      })
    }
  })
}

const handleScroll = () => {
  if (messagesContainer.value) {
    const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
    showScrollButton.value = scrollHeight - scrollTop - clientHeight > 100
  }
}

const clearMessages = () => {
  // TODO: Implement clear messages functionality
  console.log('Clear messages')
}

const viewProductDetails = () => {
  if (room.value?.product_id) {
    // Navigate to product page
    navigateTo(`/products/${room.value.product_id}`)
  }
}

const retryMessage = (message: any) => {
  if (message.tempId) {
    chatStore.retryFailedMessage(message.tempId)
  }
}

const deleteMessage = (message: any) => {
  if (message.tempId) {
    chatStore.deleteFailedMessage(props.roomId, message.tempId)
  }
}

watch(messages, () => {
  // Only auto-scroll if user is near bottom
  if (messagesContainer.value) {
    const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
    const isNearBottom = scrollHeight - scrollTop - clientHeight < 100
    if (isNearBottom) {
      scrollToBottom()
    }
  }
}, { deep: true })

onMounted(async () => {
  try {
    // Join room
    chatStore.joinRoom(props.roomId)

    // Fetch messages
    await chatStore.fetchMessages(props.roomId)

    // Mark as read
    chatStore.markAsRead(props.roomId)

    scrollToBottom(false)

    // Add scroll listener
    if (messagesContainer.value) {
      messagesContainer.value.addEventListener('scroll', handleScroll)
    }
  } catch (error) {
    console.error('Failed to load chat room:', error)
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  // Clean up
  if (messagesContainer.value) {
    messagesContainer.value.removeEventListener('scroll', handleScroll)
  }
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value)
  }
})
</script>

<style scoped>
.chat-room {
  display: flex;
  flex-direction: column;
  height: 100%;
  direction: rtl;
  background-color: #fafafa;
}

.offline-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  color: white;
  font-size: 13px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 11;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.chat-room-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 10;
}

.back-btn {
  margin-left: 8px;
}

.typing-icon {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.rotating {
  animation: rotating 2s linear infinite;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: linear-gradient(to bottom, #fafafa 0%, #f5f5f5 100%);
  position: relative;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.messages-list {
  padding-bottom: 16px;
}

.date-divider {
  display: flex;
  justify-content: center;
  margin: 16px 0;
}

.message {
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start; /* Align avatars to top of bubble */
  animation: slideIn 0.3s ease-out;
  gap: 8px;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Own messages: Avatar (right) → Bubble (left) in RTL */
.message-own {
  justify-content: flex-start;
  flex-direction: row; /* Avatar first, then bubble */
}

/* Other's messages: Bubble (right) → Avatar (left) in RTL */
.message-other {
  justify-content: flex-end;
  flex-direction: row; /* Bubble first, then avatar */
}

.message-avatar {
  flex-shrink: 0;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 2px; /* Align with top of bubble content */
}

.message-avatar:hover {
  transform: scale(1.1);
}

.message-avatar-own {
  /* Avatar for own messages - appears on the right */
  order: -1;
  margin-right: 0;
  margin-left: 0;
}

.message-avatar-other {
  /* Avatar for other's messages - appears on the left */
  order: 1;
  margin-left: 0;
  margin-right: 0;
}

.message-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  position: relative;
  word-wrap: break-word;
}

.message-bubble:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Own messages - Green bubble with tail on right */
.message-own .message-bubble {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  color: white;
  border-top-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
}

/* Pending message style */
.message-bubble-pending {
  opacity: 0.7;
}

/* Failed message style */
.message-bubble-failed {
  background: linear-gradient(135deg, #f44336 0%, #c62828 100%) !important;
  opacity: 0.85;
}

.message-own .message-bubble::before {
  content: '';
  position: absolute;
  top: 0;
  right: -8px;
  width: 0;
  height: 0;
  border-left: 8px solid #4CAF50;
  border-top: 8px solid #4CAF50;
  border-bottom: 8px solid transparent;
  border-right: 8px solid transparent;
}

/* Failed message tail - red to match red bubble */
.message-own .message-bubble-failed::before {
  border-left-color: #f44336;
  border-top-color: #f44336;
}

/* Other's messages - White bubble with tail on left */
.message-other .message-bubble {
  background-color: white;
  color: #333;
  border-top-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-other .message-bubble::before {
  content: '';
  position: absolute;
  top: 0;
  left: -8px;
  width: 0;
  height: 0;
  border-right: 8px solid white;
  border-top: 8px solid white;
  border-bottom: 8px solid transparent;
  border-left: 8px solid transparent;
}

.message-sender {
  font-size: 11px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #666;
}

.message-content {
  word-wrap: break-word;
  line-height: 1.5;
  white-space: pre-wrap;
  font-size: 14px;
}

.message-time {
  font-size: 10px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 2px;
}

.message-own .message-time {
  color: rgba(255, 255, 255, 0.9);
}

.message-other .message-time {
  color: #999;
}

.message-actions {
  display: flex;
  gap: 4px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  justify-content: flex-end;
}

.retry-btn,
.delete-btn {
  font-size: 11px !important;
  height: 24px !important;
  min-width: auto !important;
  padding: 0 8px !important;
}

.retry-btn:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.delete-btn:hover {
  background-color: rgba(255, 0, 0, 0.2) !important;
}

.typing-indicator {
  background-color: #e8e8e8;
  padding: 12px 16px;
}

.typing-animation {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-animation span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #999;
  animation: typing-bounce 1.4s infinite ease-in-out;
}

.typing-animation span:nth-child(1) {
  animation-delay: 0s;
}

.typing-animation span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-animation span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing-bounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

.scroll-to-bottom {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  z-index: 5;
}

.quick-replies {
  padding: 8px 12px;
  background-color: white;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.chat-input {
  display: flex;
  align-items: center; /* Center align all items */
  gap: 8px;
  padding: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  background-color: white;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}

.emoji-btn,
.quick-reply-btn {
  flex-shrink: 0;
  align-self: center; /* Align to center with text box */
}

.message-input {
  flex: 1;
}

.send-btn {
  flex-shrink: 0;
  transition: all 0.3s;
  order: -1; /* Ensure it appears first (rightmost in RTL) */
  min-height: 48px !important;
  height: 48px !important;
  width: 48px !important;
  align-self: flex-end; /* Align to bottom with textarea */
}

.send-btn:not(:disabled) {
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
}

.send-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
}

.send-btn:not(:disabled):active {
  transform: translateY(0);
}

.emoji-picker {
  max-height: 300px;
  overflow-y: auto;
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 4px;
}

.emoji-item {
  font-size: 24px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  text-align: center;
  transition: background-color 0.2s;
}

.emoji-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* Custom scrollbar */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

@media (max-width: 600px) {
  .message-bubble {
    max-width: 85%;
  }

  .emoji-grid {
    grid-template-columns: repeat(6, 1fr);
  }

  .chat-input {
    flex-wrap: wrap;
    align-items: center;
  }

  .send-btn {
    order: 1;
    margin-left: auto;
    min-height: 40px !important;
    height: 40px !important;
    width: 40px !important;
  }

  .message-input {
    flex-basis: 100%;
    order: 2;
  }

  .emoji-btn,
  .quick-reply-btn {
    order: 3;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .chat-room {
    background-color: #121212;
  }

  .chat-room-header {
    background-color: #1e1e1e;
    border-bottom-color: rgba(255, 255, 255, 0.12);
  }

  .chat-messages {
    background: linear-gradient(to bottom, #121212 0%, #1a1a1a 100%);
  }

  .message-other .message-bubble {
    background-color: #2c2c2c;
    color: #e0e0e0;
  }

  .chat-input,
  .quick-replies {
    background-color: #1e1e1e;
    border-top-color: rgba(255, 255, 255, 0.12);
  }
}
</style>









