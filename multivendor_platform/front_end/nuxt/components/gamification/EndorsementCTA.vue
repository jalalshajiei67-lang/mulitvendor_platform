<template>
  <v-card
    v-if="canEndorse"
    elevation="2"
    rounded="xl"
    class="pa-6 mb-4"
    color="primary"
    variant="tonal"
  >
    <div class="d-flex align-center justify-space-between flex-wrap gap-4">
      <div class="d-flex align-center gap-4">
        <v-avatar color="primary" size="64" variant="flat">
          <v-icon size="32" color="white">mdi-hand-heart</v-icon>
        </v-avatar>
        <div>
          <h3 class="text-h6 font-weight-bold mb-1">تأیید دعوت‌کننده خود</h3>
          <p class="text-body-2 text-medium-emphasis">
            {{ inviterName }} شما را به این پلتفرم دعوت کرده است. با تأیید او، ۵۰ امتیاز به او اهدا می‌شود.
          </p>
        </div>
      </div>
      <v-btn
        color="primary"
        size="large"
        rounded="lg"
        prepend-icon="mdi-check-circle"
        :loading="endorsing"
        @click="handleEndorse"
      >
        تأیید دعوت‌کننده
      </v-btn>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useGamificationApi } from '~/composables/useGamification'
import { useGamificationStore } from '~/stores/gamification'

const api = useGamificationApi()
const gamificationStore = useGamificationStore()

const canEndorse = ref(false)
const inviterName = ref('')
const endorsing = ref(false)

const checkCanEndorse = async () => {
  try {
    const response = await api.canEndorse()
    canEndorse.value = response.can_endorse
    if (response.inviter_name) {
      inviterName.value = response.inviter_name
    }
  } catch (error: any) {
    console.error('Failed to check endorsement status:', error)
    canEndorse.value = false
  }
}

const handleEndorse = async () => {
  endorsing.value = true
  try {
    await api.endorseInviter()
    canEndorse.value = false
    // Refresh engagement to show updated points
    await gamificationStore.fetchEngagement()
    // Show success message (you might want to use a snackbar here)
    alert('تأیید با موفقیت ثبت شد!')
  } catch (error: any) {
    console.error('Failed to endorse:', error)
    alert('خطا در ثبت تأیید. لطفاً دوباره تلاش کنید.')
  } finally {
    endorsing.value = false
  }
}

onMounted(() => {
  checkCanEndorse()
})
</script>

<style scoped>
.v-card {
  border: 2px solid rgba(var(--v-theme-primary), 0.2);
}
</style>

