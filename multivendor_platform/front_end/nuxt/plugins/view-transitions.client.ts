export default defineNuxtPlugin({
  name: 'view-transitions-error-handler',
  setup() {
    // Suppress ViewTransition errors when document is hidden
    // This is a known issue with the View Transition API during HMR updates
    if (process.client) {
      // Handle unhandled promise rejections for view transitions
      window.addEventListener('unhandledrejection', (event) => {
        const error = event.reason
        const errorMessage = error?.message || error?.toString() || ''
        
        // Suppress the specific view transition error when document is hidden
        if (
          errorMessage.includes('Skipped ViewTransition due to document being hidden') ||
          (errorMessage.includes('ViewTransition') && errorMessage.includes('document being hidden'))
        ) {
          event.preventDefault()
          // Silently handle this harmless error
          return
        }
      })

      // Also catch DOMException errors related to view transitions
      window.addEventListener('error', (event) => {
        const error = event.error
        const errorMessage = error?.message || event.message || ''
        
        if (
          errorMessage.includes('Skipped ViewTransition due to document being hidden') ||
          (errorMessage.includes('ViewTransition') && errorMessage.includes('document being hidden'))
        ) {
          event.preventDefault()
          // Silently handle this harmless error
          return
        }
      }, true)
    }
  }
})

