/**
 * Client-side plugin to initialize theme from localStorage
 * This prevents flash of wrong theme on page load
 * Runs after Vuetify is initialized to ensure theme API is available
 */
export default defineNuxtPlugin({
  name: 'init-theme',
  enforce: 'post', // Run after Vuetify is initialized
  setup() {
    if (process.client) {
      // Use nextTick to ensure Vuetify is fully initialized
      nextTick(() => {
        const { initializeTheme } = useAppTheme()
        initializeTheme()
      })
    }
  }
})

