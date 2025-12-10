<template>
  <div class="onboarding-tour">
    <!-- Floating Help Button -->
    <v-tooltip location="left">
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          class="help-btn"
          color="primary"
          icon
          size="large"
          elevation="8"
          @click="handleStartTour"
        >
          <v-icon size="28">mdi-help-circle</v-icon>
        </v-btn>
      </template>
      <span class="text-body-1">راهنمای استفاده</span>
    </v-tooltip>

    <!-- Welcome Dialog (shows on first visit) -->
    <v-dialog
      v-model="showWelcomeDialog"
      max-width="600"
      persistent
    >
      <v-card class="welcome-card" elevation="8">
        <v-card-title class="text-h4 font-weight-bold text-center pa-8 bg-primary">
          <div class="text-white">
            <v-icon size="64" color="white" class="mb-4">mdi-hand-wave</v-icon>
            <div>خوش آمدید!</div>
          </div>
        </v-card-title>

        <v-card-text class="pa-8 text-center">
          <p class="text-h6 mb-6 line-height-relaxed">
            بیایید فروشگاه آنلاین شما را راه‌اندازی کنیم! ما شما را قدم به قدم راهنمایی می‌کنیم.
          </p>

          <div class="illustration-icons mb-6">
            <v-icon size="80" color="primary" class="mx-2">mdi-store</v-icon>
            <v-icon size="80" color="success" class="mx-2">mdi-chart-line</v-icon>
            <v-icon size="80" color="info" class="mx-2">mdi-package-variant</v-icon>
          </div>

          <p class="text-body-1 text-medium-emphasis mb-4">
            این راهنما شما را کمک می‌کند تا:
          </p>

          <v-list class="bg-transparent text-right">
            <v-list-item class="px-0">
              <template v-slot:prepend>
                <v-icon color="success" size="24">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title class="text-body-1">اولین محصول خود را اضافه کنید</v-list-item-title>
            </v-list-item>
            <v-list-item class="px-0">
              <template v-slot:prepend>
                <v-icon color="success" size="24">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title class="text-body-1">صفحه فروشگاه خود را تنظیم کنید</v-list-item-title>
            </v-list-item>
            <v-list-item class="px-0">
              <template v-slot:prepend>
                <v-icon color="success" size="24">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title class="text-body-1">نمونه کارها و تیم خود را معرفی کنید</v-list-item-title>
            </v-list-item>
          </v-list>

          <div class="mt-6 pa-4 bg-blue-lighten-5 rounded-lg">
            <p class="text-body-2 text-primary font-weight-bold mb-2">
              💡 نکته مهم:
            </p>
            <p class="text-caption">
              در هر مرحله، روی دکمه یا فیلد مورد نظر کلیک کنید تا به مرحله بعدی بروید.
            </p>
          </div>
        </v-card-text>

        <v-card-actions class="pa-6 pt-0">
          <v-row dense>
            <v-col cols="12">
              <v-btn
                color="primary"
                size="x-large"
                block
                elevation="2"
                @click="startWelcomeTour"
                class="text-h6"
              >
                <v-icon start>mdi-play-circle</v-icon>
                شروع راهنما
              </v-btn>
            </v-col>
            <v-col cols="12">
              <v-btn
                color="grey"
                variant="text"
                size="large"
                block
                @click="handleDismiss"
                class="text-body-1"
              >
                دیگر نشان نده
              </v-btn>
            </v-col>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSupplierOnboarding } from '~/composables/useSupplierOnboarding'

const emit = defineEmits<{
  tourStarted: []
  tourCompleted: []
  tourDismissed: []
}>()

const props = withDefaults(defineProps<{
  forceShow?: boolean
}>(), {
  forceShow: false
})

const {
  shouldShowTour,
  markTourCompleted,
  dismissTour,
  startTour
} = useSupplierOnboarding()

const showWelcomeDialog = ref(false)

// Helpers to check completion/dismissal
const isTourCompleted = () => {
  if (typeof window === 'undefined') return false
  return localStorage.getItem('supplier_tour_completed') === 'true'
}

const isTourDismissed = () => {
  if (typeof window === 'undefined') return false
  return localStorage.getItem('supplier_tour_dismissed') === 'true'
}

// Check if should show welcome dialog on mount
onMounted(() => {
  setTimeout(() => {
    const canShow = !isTourCompleted() && !isTourDismissed() && (props.forceShow || shouldShowTour())
    if (canShow) {
      showWelcomeDialog.value = true
    }
  }, 1000) // Delay to ensure page is fully loaded
})

// Start tour from welcome dialog
const startWelcomeTour = () => {
  showWelcomeDialog.value = false
  setTimeout(() => {
    startTour(
      () => {
        markTourCompleted()
        emit('tourCompleted')
      },
      () => {
        emit('tourDismissed')
      }
    )
    emit('tourStarted')
  }, 300)
}

// Start tour from help button
const handleStartTour = () => {
  startTour(
    () => {
      markTourCompleted()
      emit('tourCompleted')
    },
    () => {
      emit('tourDismissed')
    }
  )
  emit('tourStarted')
}

// Dismiss tour permanently
const handleDismiss = () => {
  const confirmed = confirm('آیا مطمئن هستید؟ این راهنما دیگر نمایش داده نخواهد شد.')
  if (confirmed) {
    dismissTour()
    showWelcomeDialog.value = false
    emit('tourDismissed')
  }
}
</script>

<style scoped>
.onboarding-tour {
  position: relative;
}

.help-btn {
  position: fixed;
  bottom: 24px;
  left: 24px;
  z-index: 999;
  transition: all 0.3s ease;
}

.help-btn:hover {
  transform: scale(1.1);
}

.welcome-card {
  border-radius: 20px !important;
}

.line-height-relaxed {
  line-height: 1.8;
}

.illustration-icons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 20px 0;
}

/* Mobile adjustments */
@media (max-width: 600px) {
  .help-btn {
    bottom: 16px;
    left: 16px;
  }
  
  .illustration-icons {
    gap: 8px;
  }
  
  .illustration-icons .v-icon {
    font-size: 60px !important;
  }
}
</style>

