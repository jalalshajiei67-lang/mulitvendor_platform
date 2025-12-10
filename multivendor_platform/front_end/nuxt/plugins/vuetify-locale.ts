export default defineNuxtPlugin({
  name: 'vuetify-locale-fix',
  enforce: 'pre', // Run before other plugins to ensure translations are set early
  setup(nuxtApp) {
    // Set up translations immediately on both client and server
    const setupTranslations = () => {
      try {
        const vuetify = (nuxtApp as any).$vuetify || (nuxtApp.vueApp?.config?.globalProperties?.$vuetify)

        if (!vuetify?.locale) {
          // If Vuetify isn't ready yet, try again on next tick
          if (process.client) {
            setTimeout(setupTranslations, 100)
          }
          return
        }

        // Get current messages with proper reactive handling
        let messages = vuetify.locale.messages
        if (messages?.value) {
          messages = messages.value
        }

        const faMessages = messages?.fa || messages?.default || {}
        const currentVuetify = faMessages.$vuetify || {}

        // Ensure input object exists with all required keys
        if (!currentVuetify.input) {
          currentVuetify.input = {}
        }

        // Set missing input keys - these are the keys Vuetify looks for
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

        // Update reactive structure properly
        if (vuetify.locale.messages?.value !== undefined) {
          vuetify.locale.messages.value = updatedMessages
        } else if (vuetify.locale.messages) {
          vuetify.locale.messages = updatedMessages
        }

        // Also set as default/fallback
        if (!updatedMessages.default) {
          updatedMessages.default = updatedMessages.fa
        }
      } catch (error) {
        // Silently fail - translations should be set in nuxt.config.ts anyway
        if (process.dev) {
          console.debug('Vuetify locale plugin:', error)
        }
      }
    }

    // Try to set up immediately
    if (process.client) {
      // On client, wait for app to be ready
      nuxtApp.hook('app:mounted', () => {
        setupTranslations()
      })
      // Also try immediately in case Vuetify is already initialized
      setupTranslations()
    } else {
      // On server, try immediately
      setupTranslations()
    }
  }
})
