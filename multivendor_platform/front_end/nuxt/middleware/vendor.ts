export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Check if user is a vendor (has role 'seller' or 'both')
  const userRole = authStore.user?.role
  const isVendor = userRole === 'seller' || userRole === 'both'
  
  // Or check if user has vendor_profile
  const hasVendorProfile = authStore.user?.vendor_profile
  
  if (!isVendor && !hasVendorProfile) {
    // Not a vendor, redirect to home
    return navigateTo('/')
  }
})






