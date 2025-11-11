export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  try {
    await authStore.initializeAuth()
  } catch (error) {
    console.warn('Auth initialization failed:', error)
    // Don't throw - allow the app to continue loading
  }
})

