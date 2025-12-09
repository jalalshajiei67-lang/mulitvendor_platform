export default defineNuxtPlugin({
  name: 'vuetify-locale-fix',
  enforce: 'post', // Run after Vuetify module is initialized
  setup(nuxtApp) {
    // Wait for client-side only
    if (process.client) {
      // Use app:mounted hook to ensure Vuetify is fully initialized
      nuxtApp.hook('app:mounted', () => {
        try {
          const vuetify = (nuxtApp as any).$vuetify

          if (!vuetify?.locale) {
            return
          }

          // Get current messages
          const messages = vuetify.locale.messages?.value || vuetify.locale.messages || {}
          const faMessages = messages.fa || {}
          const currentVuetify = faMessages.$vuetify || {}

          // Ensure input object exists with all required keys
          if (!currentVuetify.input) {
            currentVuetify.input = {}
          }

          // Set missing input keys
          currentVuetify.input = {
            clear: 'پاک کردن',
            appendAction: 'عملیات اضافی',
            prependAction: 'عملیات اولیه',
            otp: 'لطفاً کد OTP خود را وارد کنید',
            ...currentVuetify.input // Preserve existing keys
          }

          // Ensure other top-level keys exist
          if (!currentVuetify.open) {
            currentVuetify.open = 'باز کردن'
          }
          if (!currentVuetify.close) {
            currentVuetify.close = 'بستن'
          }

          // Update messages with the fixed translations
          const updatedMessages = {
            ...messages,
            fa: {
              ...faMessages,
              $vuetify: currentVuetify
            }
          }

          // Update reactive structure
          if (vuetify.locale.messages?.value !== undefined) {
            vuetify.locale.messages.value = updatedMessages
          } else if (vuetify.locale.messages) {
            vuetify.locale.messages = updatedMessages
          }
        } catch (error) {
          // Silently fail - translations should be set in nuxt.config.ts anyway
          console.debug('Vuetify locale plugin:', error)
        }
      })
    }
  }
})
