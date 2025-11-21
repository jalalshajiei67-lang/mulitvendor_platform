<template>
  <v-btn
    color="success"
    variant="outlined"
    :loading="loading"
    :block="block"
    :size="size"
    @click="startChat"
  >
    <v-icon class="ml-2">mdi-chat</v-icon>
    گفتگو با فروشنده
  </v-btn>

  <!-- Success snackbar -->
  <v-snackbar v-model="showSuccess" color="success" :timeout="3000">
    گفتگو شروع شد! پنجره چت را در پایین صفحه ببینید
  </v-snackbar>

  <!-- Error snackbar -->
  <v-snackbar v-model="showError" color="error" :timeout="3000">
    خطا در شروع گفتگو. لطفا دوباره تلاش کنید
  </v-snackbar>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from '~/stores/chat'
import { useAuthStore } from '~/stores/auth'

const props = withDefaults(defineProps<{
  productId: number
  vendorId: number
  block?: boolean
  size?: 'x-small' | 'small' | 'default' | 'large' | 'x-large'
}>(), {
  block: false,
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
    
    // If not authenticated, create guest session first
    if (!authStore.isAuthenticated && !chatStore.guestSessionId) {
      console.log('Creating guest session...')
      await chatStore.createGuestSession()
    }
    
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
/* Add any custom styles if needed */
</style>

