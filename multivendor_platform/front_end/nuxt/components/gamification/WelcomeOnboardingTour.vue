<template>
  <div>
    <!-- Welcome Dialog (First Step) -->
    <v-dialog
      v-model="showWelcome"
      max-width="700"
      persistent
      :scrim="false"
    >
      <v-card class="welcome-card" elevation="8" rounded="xl">
        <v-card-title class="text-center pa-8 bg-primary text-white">
          <div class="w-100">
            <v-icon size="64" color="white" class="mb-4">mdi-hand-wave</v-icon>
            <div class="text-h4 font-weight-bold">به ایندکسو خوش آمدید !</div>
          </div>
        </v-card-title>

        <v-card-text class="pa-8 text-center">
          <p class="text-h6 mb-6 line-height-relaxed">
            ایندکسو ابزاری است که به شما برای فروش بیشتر کمک می‌کند، تمام مراحل و اقداماتی که انجام می‌دهید، برای ایجاد اعتماد و معرفی حرفه‌ای شما به مشتریان طراحی شده است.
          </p>

          <div class="illustration-icons mb-6">
            <v-icon size="80" color="primary" class="mx-2">mdi-trophy</v-icon>
            <v-icon size="80" color="success" class="mx-2">mdi-currency-usd</v-icon>
            <v-icon size="80" color="info" class="mx-2">mdi-navigation</v-icon>
          </div>

          <div class="mt-6 pa-4 bg-blue-lighten-5 rounded-lg">
            <p class="text-body-2 text-primary font-weight-bold mb-2">
              💡 نکته:
            </p>
            <p class="text-caption">
              این راهنما شما را با بخش‌های مهم پلتفرم آشنا می‌کند.
            </p>
          </div>
        </v-card-text>

        <v-card-actions class="pa-6 pt-0">
          <v-row dense>
            <v-col cols="12">
              <v-checkbox
                v-model="dontShowAgain"
                label="دیگر نشان نده"
                color="primary"
                hide-details
                class="mb-4"
              ></v-checkbox>
            </v-col>
            <v-col cols="12">
              <v-btn
                color="primary"
                size="x-large"
                block
                elevation="2"
                rounded="lg"
                @click="startTour"
                class="text-h6"
              >
                <v-icon start>mdi-play-circle</v-icon>
                شروع راهنما
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
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'
import { useGamificationDashboard } from '~/composables/useGamificationDashboard'

const emit = defineEmits<{
  tourCompleted: []
  tourDismissed: []
}>()

const props = withDefaults(defineProps<{
  forceShow?: boolean
}>(), {
  forceShow: false
})

const showWelcome = ref(false)
const dontShowAgain = ref(false)
const dashboardApi = useGamificationDashboard()
let driverInstance: any = null

const STORAGE_KEY = 'welcome_onboarding_quest_completed'

// Check if tour should be shown
const shouldShowTour = () => {
  if (typeof window === 'undefined') return false
  if (props.forceShow) return true
  return localStorage.getItem(STORAGE_KEY) !== 'true'
}

// Mark tour as completed
const markTourCompleted = () => {
  if (typeof window === 'undefined') return
  localStorage.setItem(STORAGE_KEY, 'true')
}

// Check on mount
onMounted(() => {
  setTimeout(() => {
    // Check if we're continuing a tour from another page
    const tourStep = sessionStorage.getItem('welcome_tour_step')
    if (tourStep) {
      // Continue tour on this page (don't remove sessionStorage yet)
      startTour()
    } else if (shouldShowTour() && !sessionStorage.getItem('welcome_tour_in_progress')) {
      showWelcome.value = true
    }
  }, 1000)
})

// Start the tour
const startTour = () => {
  showWelcome.value = false
  
  // If "don't show again" is checked, mark as completed immediately
  if (dontShowAgain.value) {
    markTourCompleted()
    sessionStorage.removeItem('welcome_tour_step')
    sessionStorage.removeItem('welcome_tour_in_progress')
    emit('tourDismissed')
    return
  }

  // Mark tour as in progress and set initial step if not set
  sessionStorage.setItem('welcome_tour_in_progress', 'true')
  if (!sessionStorage.getItem('welcome_tour_step')) {
    sessionStorage.setItem('welcome_tour_step', '1')
  }

  const startTourSteps = () => {
    // Destroy any existing instance
    if (driverInstance) {
      try {
        driverInstance.destroy()
      } catch (e) {
        // Ignore
      }
    }

    // Get current page and tour step
    const currentPath = window.location.pathname
    const isOnDashboard = currentPath.includes('/seller/dashboard') || currentPath === '/seller/dashboard'
    const tourStep = sessionStorage.getItem('welcome_tour_step')

    // Build all 4 steps at once when on dashboard
    const steps: any[] = []

    if (isOnDashboard) {
      // Step 1: Stat Section
      steps.push({
        element: '[data-tour="stat-section"]',
        popover: {
          title: 'وضعیت حرفه‌ای شما',
          description: 'اینجا نشان می‌دهد چقدر در جلب اعتماد مشتریان موفق بوده‌اید. هرچه اطلاعات کامل‌تر باشد، رتبه و فروش شما بالاتر می‌رود.',
          side: 'bottom',
          align: 'start',
          showButtons: ['next'],
          nextBtnText: 'بعدی',
          prevBtnText: 'قبلی'
        }
      })

      // Step 2: Quest Box
      steps.push({
        element: '[data-tour="quest-box"]',
        popover: {
          title: 'مسیر موفقیت',
          description: 'ما قدم به قدم به شما می‌گوییم چه کارهایی انجام دهید تا مشتریان بیشتری به شما اعتماد کنند. این مراحل را دنبال کنید.',
          side: 'bottom',
          align: 'start',
          showButtons: ['next'],
          nextBtnText: 'بعدی',
          prevBtnText: 'قبلی'
        }
      })

      // Step 3: Pricing Button
      steps.push({
        element: '[data-tour="pricing-button"]',
        popover: {
          title: 'برنامه‌های فروش',
          description: 'بسته‌های مختلف برای دیده‌شدن بیشتر محصولات شما.',
          side: 'bottom',
          align: 'start',
          showButtons: ['next'],
          nextBtnText: 'بعدی',
          prevBtnText: 'قبلی'
        }
      })

      // Step 4: Navbar - Final step with finish button
      steps.push({
        element: '[data-tour="navbar-section"]',
        popover: {
          title: 'دسترسی سریع',
          description: 'از اینجا می‌توانید به همه بخش‌های فروشگاه خود دسترسی داشته باشید.',
          side: 'bottom',
          align: 'start',
          showButtons: ['next'],
          nextBtnText: 'اتمام',
          prevBtnText: 'قبلی',
          onNextClick: () => {
            // Clear session storage
            sessionStorage.removeItem('welcome_tour_step')
            sessionStorage.removeItem('welcome_tour_in_progress')
            completeQuest()
          }
        }
      })
    }

    // If no steps, don't start the tour
    if (steps.length === 0) {
      console.warn('Welcome tour: No steps to show')
      return
    }

    // Verify all elements exist before starting
    const allElementsExist = steps.every(step => {
      const el = document.querySelector(step.element)
      return el !== null
    })

    if (!allElementsExist) {
      console.warn('Welcome tour: Some elements not found', steps.map(s => s.element))
      return
    }

    // Configure driver.js for RTL
    driverInstance = driver({
      showProgress: true,
      steps: steps,
      onDestroyStarted: () => {
        // Tour was dismissed
        if (dontShowAgain.value) {
          markTourCompleted()
          emit('tourDismissed')
        }
      },
      onDestroyed: () => {
        driverInstance = null
      },
      onHighlightStarted: (element) => {
        // Update session storage based on which step we're on
        if (element) {
          const dataTour = element.getAttribute('data-tour')
          const stepIndex = steps.findIndex(s => s.element === `[data-tour="${dataTour}"]`)
          if (stepIndex >= 0) {
            sessionStorage.setItem('welcome_tour_step', String(stepIndex + 1))
          }
        }
      }
    })

    // Custom RTL styles
    const style = document.createElement('style')
    style.textContent = `
      .driver-popover {
        direction: rtl;
        text-align: right;
        font-family: 'Vazir', sans-serif;
      }
      .driver-popover-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 12px;
      }
      .driver-popover-description {
        font-size: 16px;
        line-height: 1.6;
      }
      .driver-popover-footer {
        direction: rtl;
      }
      .driver-popover-footer button {
        margin-left: 8px;
        margin-right: 0;
      }
    `
    document.head.appendChild(style)

    driverInstance.drive()
  }

  // Wait for elements to be available before starting tour
  const waitForElements = (maxAttempts = 15, attempt = 0) => {
    const statEl = document.querySelector('[data-tour="stat-section"]')
    const questEl = document.querySelector('[data-tour="quest-box"]')
    const pricingEl = document.querySelector('[data-tour="pricing-button"]')
    const navbarEl = document.querySelector('[data-tour="navbar-section"]')

    if (statEl && questEl && pricingEl && navbarEl) {
      // All elements found, start the tour
      startTourSteps()
    } else if (attempt < maxAttempts) {
      // Elements not ready yet, wait and try again
      setTimeout(() => waitForElements(maxAttempts, attempt + 1), 500)
    } else {
      console.warn('Welcome tour: Some elements not found after waiting', {
        stat: !!statEl,
        quest: !!questEl,
        pricing: !!pricingEl,
        navbar: !!navbarEl
      })
    }
  }

  // Start waiting for elements
  setTimeout(() => {
    waitForElements()
  }, 500)
}

// Complete the quest
const completeQuest = async () => {
  try {
    // Mark tour as completed in localStorage
    markTourCompleted()
    
    // Complete the quest via API
    const result = await dashboardApi.completeTask('onboarding_quest', {
      tour_completed: true
    })
    
    if (result.error.value) {
      console.warn('Failed to complete onboarding quest:', result.error.value)
    } else if (result.data.value) {
      console.log('Onboarding quest completed:', result.data.value)
    }
    
    emit('tourCompleted')
    
    // Destroy driver instance
    if (driverInstance) {
      driverInstance.destroy()
      driverInstance = null
    }
  } catch (error) {
    console.error('Error completing onboarding quest:', error)
    emit('tourCompleted')
  }
}
</script>

<style scoped>
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
  .illustration-icons {
    gap: 8px;
  }
  
  .illustration-icons .v-icon {
    font-size: 60px !important;
  }
}
</style>

