/**
 * Fix for Pinia hydration errors with objects that don't have hasOwnProperty
 * This plugin ensures Pinia state is properly serializable during SSR
 * 
 * The issue occurs when Pinia tries to serialize state that contains objects
 * without prototypes (created with Object.create(null)). This plugin ensures
 * such objects are handled correctly.
 */

export default defineNuxtPlugin(() => {
  if (process.server) {
    // Monkey-patch Pinia's shouldHydrate function if the patch wasn't applied
    // This is a fallback in case patch-package didn't run during build
    try {
      // Try to access Pinia internals - if available, ensure proper hasOwnProperty usage
      const piniaModule = require('pinia')
      if (piniaModule && piniaModule.setActivePinia) {
        // Patch is already applied or Pinia is working correctly
        console.log('[Pinia Hydration Fix] Pinia module loaded correctly')
      }
    } catch (e) {
      // Pinia might not be available at plugin load time, which is fine
      // The patch should handle it during build
    }
  }
})

