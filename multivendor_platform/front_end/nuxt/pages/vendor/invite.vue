<template>
  <v-container fluid class="pa-4 pa-md-6">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-4">دعوت و کسب امتیاز</h1>
        <p class="text-body-1 text-medium-emphasis mb-6">
          دوستان خود را دعوت کنید و برای هر ثبت‌نام موفق ۱۰۰ امتیاز دریافت کنید
        </p>
      </v-col>
    </v-row>

    <!-- Invite Link Section -->
    <v-row>
      <v-col cols="12" md="8">
        <v-card elevation="2" rounded="xl" class="mb-4">
          <v-card-title class="bg-primary text-white pa-4">
            <v-icon class="ml-2">mdi-share-variant</v-icon>
            لینک دعوت شما
          </v-card-title>
          <v-card-text class="pa-6">
            <div v-if="loadingInvite" class="text-center py-8">
              <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
              <p class="mt-4 text-body-2">در حال ایجاد لینک دعوت...</p>
            </div>

            <div v-else-if="inviteLink" class="mb-4">
              <v-text-field
                :model-value="inviteLink"
                label="لینک دعوت"
                readonly
                variant="outlined"
                rounded="lg"
                density="comfortable"
                class="mb-4"
                dir="ltr"
              >
                <template #append-inner>
                  <v-btn
                    icon="mdi-content-copy"
                    variant="text"
                    size="small"
                    @click="copyInviteLink"
                    :disabled="copying"
                  >
                  </v-btn>
                </template>
              </v-text-field>

              <v-btn
                color="primary"
                size="large"
                block
                prepend-icon="mdi-content-copy"
                @click="copyInviteLink"
                :loading="copying"
                rounded="lg"
              >
                کپی لینک دعوت
              </v-btn>
            </div>

            <div v-else>
              <v-btn
                color="primary"
                size="large"
                block
                prepend-icon="mdi-link-variant-plus"
                @click="generateInviteLink"
                :loading="generating"
                :disabled="inviteLimitReached"
                rounded="lg"
              >
                ایجاد لینک دعوت
              </v-btn>
              <p v-if="inviteLimitReached" class="text-caption mt-2 text-error">
                سقف روزانه دعوت‌ها تکمیل شده است.
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Stats Card -->
      <v-col cols="12" md="4">
        <v-card elevation="2" rounded="xl" class="h-100">
          <v-card-title class="bg-success text-white pa-4">
            <v-icon class="ml-2">mdi-chart-line</v-icon>
            آمار دعوت‌ها
          </v-card-title>
          <v-card-text class="pa-6">
            <div class="text-center mb-6">
              <div class="text-h3 font-weight-bold text-primary mb-2">
                {{ stats.total_points_earned || 0 }}
              </div>
              <div class="text-body-2 text-medium-emphasis">امتیاز کل کسب شده</div>
            </div>

            <v-divider class="my-4"></v-divider>

            <div class="d-flex justify-space-between align-center mb-3">
              <span class="text-body-2">دعوت‌های باقی‌مانده امروز:</span>
              <v-chip color="secondary" variant="flat" size="small">
                {{ remainingInvites }} / {{ inviteLimit }}
              </v-chip>
            </div>

            <div class="d-flex justify-space-between align-center mb-3">
              <span class="text-body-2">کل دعوت‌ها:</span>
              <v-chip color="primary" variant="flat" size="small">
                {{ stats.total_invitations || 0 }}
              </v-chip>
            </div>

            <div class="d-flex justify-space-between align-center mb-3">
              <span class="text-body-2">پذیرفته شده:</span>
              <v-chip color="success" variant="flat" size="small">
                {{ stats.accepted_count || 0 }}
              </v-chip>
            </div>

            <div class="d-flex justify-space-between align-center">
              <span class="text-body-2">در انتظار:</span>
              <v-chip color="warning" variant="flat" size="small">
                {{ stats.pending_count || 0 }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Invitations List -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" rounded="xl">
          <v-card-title class="pa-4">
            <v-icon class="ml-2">mdi-format-list-bulleted</v-icon>
            لیست دعوت‌ها
          </v-card-title>
          <v-card-text class="pa-0">
            <div v-if="loadingStatus" class="text-center py-8">
              <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
              <p class="mt-4 text-body-2">در حال بارگذاری...</p>
            </div>

            <v-list v-else-if="invitations.length > 0" density="comfortable">
              <v-list-item
                v-for="invitation in invitations"
                :key="invitation.id"
                class="border-b"
              >
                <template #prepend>
                  <v-avatar
                    :color="getStatusColor(invitation.status)"
                    size="40"
                    variant="flat"
                  >
                    <v-icon :color="getStatusIconColor(invitation.status)">
                      {{ getStatusIcon(invitation.status) }}
                    </v-icon>
                  </v-avatar>
                </template>

                <v-list-item-title class="font-weight-medium">
                  کد دعوت: {{ invitation.invite_code }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  <div class="mt-1">
                    <span v-if="invitation.invitee_email" class="text-caption">
                      ایمیل: {{ invitation.invitee_email }}
                    </span>
                    <span v-else class="text-caption text-medium-emphasis">
                      بدون ایمیل مشخص
                    </span>
                  </div>
                  <div class="text-caption text-medium-emphasis mt-1">
                    ایجاد شده: {{ formatDate(invitation.created_at) }}
                  </div>
                  <div v-if="invitation.accepted_at" class="text-caption text-success mt-1">
                    پذیرفته شده: {{ formatDate(invitation.accepted_at) }}
                  </div>
                </v-list-item-subtitle>

                <template #append>
                  <div class="d-flex align-center gap-3">
                    <v-chip
                      :color="getStatusColor(invitation.status)"
                      variant="flat"
                      size="small"
                    >
                      {{ getStatusLabel(invitation.status) }}
                    </v-chip>
                    <div v-if="invitation.points_earned > 0" class="text-success font-weight-bold">
                      +{{ invitation.points_earned }} امتیاز
                    </div>
                  </div>
                </template>
              </v-list-item>
            </v-list>

            <div v-else class="text-center py-12">
              <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-email-outline</v-icon>
              <p class="text-h6 text-medium-emphasis mb-2">هنوز دعوتی ارسال نکرده‌اید</p>
              <p class="text-body-2 text-medium-emphasis">
                لینک دعوت خود را ایجاد کنید و با دوستان خود به اشتراک بگذارید
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success Snackbar -->
    <v-snackbar v-model="showSnackbar" :color="snackbarColor" :timeout="3000" location="top">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useGamificationApi } from '~/composables/useGamification'

definePageMeta({
  layout: 'dashboard',
  middleware: ['authenticated', 'vendor']
})

const api = useGamificationApi()

const inviteLink = ref<string>('')
const loadingInvite = ref(false)
const generating = ref(false)
const copying = ref(false)
const loadingStatus = ref(false)
const invitations = ref<any[]>([])
const stats = ref({
  total_points_earned: 0,
  total_invitations: 0,
  accepted_count: 0,
  pending_count: 0
})
const remainingInvites = ref<number>(0)
const inviteLimit = ref<number>(5)
const inviteLimitReached = computed(() => remainingInvites.value <= 0)

const showSnackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref<'success' | 'error'>('success')

const generateInviteLink = async () => {
  if (inviteLimitReached.value) {
    showMessage('سقف روزانه دعوت‌ها پر شده است.', 'error')
    return
  }
  generating.value = true
  loadingInvite.value = true
  try {
    const response = await api.generateInviteCode()
    inviteLink.value = response.invite_link
    inviteLimit.value = response.limit ?? inviteLimit.value
    if (typeof response.remaining_invites === 'number') {
      remainingInvites.value = response.remaining_invites
    }
    showMessage('لینک دعوت با موفقیت ایجاد شد', 'success')
    await loadInvitationStatus()
  } catch (error: any) {
    console.error('Failed to generate invite link', error)
    const detail = error?.data?.detail || 'خطا در ایجاد لینک دعوت'
    showMessage(detail, 'error')
  } finally {
    generating.value = false
    loadingInvite.value = false
  }
}

const copyInviteLink = async () => {
  if (!inviteLink.value) return

  copying.value = true
  try {
    await navigator.clipboard.writeText(inviteLink.value)
    showMessage('لینک دعوت کپی شد', 'success')
  } catch (error) {
    console.error('Failed to copy link', error)
    showMessage('خطا در کپی کردن لینک', 'error')
  } finally {
    copying.value = false
  }
}

const loadInvitationStatus = async () => {
  loadingStatus.value = true
  try {
    const response = await api.getInvitationStatus()
    invitations.value = response.invitations || []
    stats.value = {
      total_points_earned: response.total_points_earned || 0,
      total_invitations: response.total_invitations || 0,
      accepted_count: response.accepted_count || 0,
      pending_count: response.pending_count || 0
    }
    inviteLimit.value = response.invite_limit ?? inviteLimit.value
    remainingInvites.value = response.remaining_invites ?? remainingInvites.value
  } catch (error: any) {
    console.error('Failed to load invitation status', error)
    showMessage('خطا در بارگذاری اطلاعات دعوت‌ها', 'error')
  } finally {
    loadingStatus.value = false
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'accepted':
      return 'success'
    case 'pending':
      return 'warning'
    case 'expired':
      return 'error'
    default:
      return 'grey'
  }
}

const getStatusIconColor = (status: string) => {
  switch (status) {
    case 'accepted':
      return 'white'
    case 'pending':
      return 'white'
    case 'expired':
      return 'white'
    default:
      return 'grey'
  }
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'accepted':
      return 'mdi-check-circle'
    case 'pending':
      return 'mdi-clock-outline'
    case 'expired':
      return 'mdi-close-circle'
    default:
      return 'mdi-help-circle'
  }
}

const getStatusLabel = (status: string) => {
  switch (status) {
    case 'accepted':
      return 'پذیرفته شده'
    case 'pending':
      return 'در انتظار'
    case 'expired':
      return 'منقضی شده'
    default:
      return status
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const showMessage = (message: string, color: 'success' | 'error' = 'success') => {
  snackbarMessage.value = message
  snackbarColor.value = color
  showSnackbar.value = true
}

onMounted(async () => {
  await loadInvitationStatus()
})
</script>

<style scoped>
.border-b {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.gap-3 {
  gap: 12px;
}
</style>

