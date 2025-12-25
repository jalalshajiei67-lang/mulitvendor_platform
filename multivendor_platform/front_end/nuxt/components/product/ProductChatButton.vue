<template>
  <div>
    <v-btn
      color="success"
      :variant="outlined ? 'outlined' : 'flat'"
      :loading="loading"
      :block="block"
      :size="size"
      @click="startChat"
      class="chat-button"
      elevation="2"
    >
      <v-icon class="ml-2">mdi-message-text</v-icon>
      <span class="button-text">گفتگو با فروشنده</span>
      <v-icon class="mr-2" size="x-small">mdi-chevron-left</v-icon>
    </v-btn>

    <!-- Success snackbar with icon -->
    <v-snackbar 
      v-model="showSuccess" 
      color="success" 
      :timeout="4000"
      location="top"
    >
      <div class="d-flex align-center">
        <v-icon class="ml-2">mdi-check-circle</v-icon>
        <div>
          <div class="font-weight-bold">گفتگو شروع شد!</div>
          <div class="text-caption">پنجره چت را در پایین صفحه ببینید</div>
        </div>
      </div>
    </v-snackbar>

    <!-- Error snackbar with icon -->
    <v-snackbar 
      v-model="showError" 
      color="error" 
      :timeout="4000"
      location="top"
    >
      <div class="d-flex align-center">
        <v-icon class="ml-2">mdi-alert-circle</v-icon>
        <div>
          <div class="font-weight-bold">خطا در شروع گفتگو</div>
          <div class="text-caption">لطفا دوباره تلاش کنید</div>
        </div>
      </div>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from '~/stores/chat'
import { useAuthStore } from '~/stores/auth'

const props = withDefaults(defineProps<{
  productId: number
  vendorId: number
  block?: boolean
  outlined?: boolean
  size?: 'x-small' | 'small' | 'default' | 'large' | 'x-large'
}>(), {
  block: false,
  outlined: false,
  size: 'large'
})

const chatStore = useChatStore()
const authStore = useAuthStore()
const loading = ref(false)
const showSuccess = ref(false)
const showError = ref(false)

const startChat = async () => {
  loading.value = true
  
  try {
    // Debug logging
    console.log('Starting chat with:', {
      vendorId: props.vendorId,
      productId: props.productId,
      isAuthenticated: authStore.isAuthenticated,
      hasGuestSession: !!chatStore.guestSessionId
    })
    
    // Validate vendor ID
    if (!props.vendorId) {
      console.error('No vendor ID provided!')
      showError.value = true
      return
    }
    
    // If not authenticated, open chat widget with pending chat request
    if (!authStore.isAuthenticated) {
      console.log('User not authenticated, opening chat widget for guest auth...')
      // Store pending chat request
      chatStore.setPendingChatRequest(
        props.vendorId,
        props.productId,
        'سلام، درباره این محصول سوال دارم.'
      )
      // Open the chat widget (will show guest auth form)
      chatStore.toggleWidget()
      loading.value = false
      return
    }
    
    // User is authenticated, proceed with starting chat
    // Connect WebSocket if not connected
    if (!chatStore.isConnected) {
      console.log('Connecting WebSocket...')
      await chatStore.connectWebSocket()
    }
    
    // Start or get existing chat
    console.log('Starting chat...')
    const room = await chatStore.startChat(
      props.vendorId,
      props.productId,
      'سلام، درباره این محصول سوال دارم.'
    )
    
    if (room) {
      // Join the room and open widget
      chatStore.joinRoom(room.room_id)
      chatStore.openRoom(room.room_id)
      
      // Show success message
      showSuccess.value = true
      
      console.log('Chat started successfully:', room)
    }
  } catch (error: any) {
    console.error('Failed to start chat:', error)
    console.error('Error details:', error.data || error.response || error)
    showError.value = true
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-button {
  transition: all 0.3s ease;
  text-transform: none !important;
  letter-spacing: normal !important;
}

.chat-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
}

.button-text {
  font-weight: 600;
}

/* Animate the chevron on hover */
.chat-button:hover .mdi-chevron-left {
  animation: slideLeft 0.6s ease-in-out infinite;
}

@keyframes slideLeft {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(-4px);
  }
}
</style>

